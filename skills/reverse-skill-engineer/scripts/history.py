#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Read-only, bounded history extraction. Python 3.10+, standard library only."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys


SECRET_KEY = re.compile(r"token|secret|password|credential|authorization|api.?key", re.I)
REDACTIONS = [
    (r"-----BEGIN [^-]*PRIVATE KEY-----.*?(?:-----END [^-]*PRIVATE KEY-----|$)", "[REDACTED KEY]"),
    (r"\b(?:sk-[\w-]{8,}|gh[pousr]_[\w]{8,}|AKIA[A-Z0-9]{16})\b", "[REDACTED TOKEN]"),
    (r"(?i)\bBearer\s+[^\s\"']+", "Bearer [REDACTED]"),
    (r"(?i)(https?://)[^/\s:@]+:[^/\s@]+@", r"\1[REDACTED]@"),
    (r"\b[A-Z][A-Z0-9_]*\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)", "[REDACTED ENV]"),
    (r"(?i)((?:api[_-]?key|token|secret|password|authorization)\s*[=:]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;]+)", r"\1[REDACTED]"),
    (r"(?i)(--(?:api-key|token|secret|password)(?:=|\s+))(?:\"[^\"]*\"|'[^']*'|[^\s]+)", r"\1[REDACTED]"),
]


def redact(text):
    for pattern, replacement in REDACTIONS:
        text = re.sub(pattern, replacement, text, flags=re.S)
    return text


def scrub(value):
    if isinstance(value, dict):
        return {k: "[REDACTED]" if SECRET_KEY.search(k) or k.lower() in
                {"env", "environment", "environment_variables"} else scrub(v)
                for k, v in value.items()}
    if isinstance(value, list):
        return [scrub(v) for v in value]
    return redact(value) if isinstance(value, str) else value


def render(value):
    # Tool arguments are often JSON encoded inside a string.
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (ValueError, RecursionError):
            pass
    value = scrub(value)
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=True)


def text_blocks(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    return "\n".join(block["text"] for block in content
                     if isinstance(block, dict) and isinstance(block.get("type"), str) and block.get("type") in
                     {"text", "input_text", "output_text"} and
                     isinstance(block.get("text"), str))


def codex(record, outputs):
    kind = record.get("type")
    payload = record.get("payload")
    if not isinstance(kind, str) or not isinstance(payload, dict):
        return {"kind": "unknown", "note": "unrecognized payload"}
    subtype = payload.get("type")
    if subtype is not None and not isinstance(subtype, str):
        return {"kind": "unknown", "note": "unrecognized payload type"}
    if kind == "session_meta":
        return {"kind": "metadata", **{k: payload[k] for k in
                ("id", "session_id", "cwd", "cli_version", "forked_from_id", "parent_thread_id")
                if k in payload}}
    if kind == "response_item":
        if subtype == "message":
            return {"kind": "message", "role": payload.get("role"),
                    "id": payload.get("id"), "text": text_blocks(payload.get("content")),
                    "unknown_blocks": [str(block.get("type", "unknown"))
                                       for block in payload.get("content", [])
                                       if isinstance(block, dict) and (not isinstance(block.get("type"), str) or block.get("type") not in
                                       {"input_text", "output_text"})]
                    if isinstance(payload.get("content"), list) else []}
        if subtype in {"function_call", "custom_tool_call", "local_shell_call"}:
            return {"kind": "tool_call", "name": payload.get("name", subtype),
                    "call_id": payload.get("call_id", payload.get("id")),
                    "text": render(payload.get("arguments", payload.get("input", payload.get("action"))))}
        if subtype in {"function_call_output", "custom_tool_call_output"}:
            return {"kind": "tool_result", "call_id": payload.get("call_id"),
                    "text": render(payload.get("output")) if outputs else "[output omitted]"}
    if kind == "event_msg" and subtype in {"user_message", "agent_message"}:
        return {"kind": "message", "role": "user" if subtype == "user_message" else "assistant",
                "mirror_possible": True, "text": payload.get("message", "")}
    # Preserve unrecognized types and hidden/compacted context by locator, not raw dump.
    return {"kind": "unknown", "note": "payload retained in original; inspect if relevant"}


def claude(record, outputs):
    message = record.get("message")
    if not isinstance(record.get("type"), str) or record.get("type") not in {"user", "assistant"} or not isinstance(message, dict):
        return {"kind": "unknown", "note": "unrecognized local event"}
    content = message.get("content")
    tools = []
    unknown_blocks = []
    for block in content if isinstance(content, list) else []:
        if not isinstance(block, dict):
            unknown_blocks.append("non-object")
        elif block.get("type") == "tool_use":
            tools.append({"kind": "tool_call", "name": block.get("name"),
                          "call_id": block.get("id"), "text": render(block.get("input"))})
        elif block.get("type") == "tool_result":
            tools.append({"kind": "tool_result", "call_id": block.get("tool_use_id"),
                          "is_error": block.get("is_error"),
                          "text": render(block.get("content")) if outputs else "[output omitted]"})
        elif block.get("type") != "text":
            unknown_blocks.append(str(block.get("type", "unknown")))
    text = text_blocks(content)
    return {"kind": "message", "role": message.get("role", record["type"]),
            "id": record.get("uuid"), "parent_id": record.get("parentUuid"),
            "session_id": record.get("sessionId"), "cwd": record.get("cwd"),
            "version": record.get("version"), "text": text, "tools": tools,
            "unknown_blocks": unknown_blocks,
            # Top-level user text remains a candidate even alongside tool results.
            "candidate": bool(text) and record.get("type") == "user" and
            not record.get("isMeta") and not record.get("isSynthetic")}


ADAPTERS = {"codex": codex, "claude-local": claude}


class PrivateKeyScanner:
    """Track text key boundaries with bounded memory, including discarded chunks."""

    tokens = re.compile(rb"-----BEGIN |-----END |PRIVATE KEY-----")
    overlap_bytes = len(b"PRIVATE KEY-----") - 1

    def __init__(self):
        self.overlap = b""
        self.pending_boundary = None
        self.inside = False
        self.redact_line = False

    def feed(self, chunk):
        data = self.overlap + chunk
        for match in self.tokens.finditer(data):
            if match.end() <= len(self.overlap):
                continue  # This token was already processed in the previous chunk.
            token = match.group()
            if token == b"-----BEGIN ":
                self.pending_boundary = True
            elif token == b"-----END ":
                self.pending_boundary = False
            elif self.pending_boundary is not None:
                self.inside = self.pending_boundary
                self.redact_line = True
                self.pending_boundary = None
        self.overlap = data[-self.overlap_bytes:]

    def finish_line(self):
        redact_line = self.redact_line
        self.overlap = b""
        self.pending_boundary = None
        self.redact_line = self.inside
        return redact_line


def read_lines(path, max_bytes, on_chunk=None):
    """Stream physical lines; hash oversized lines without retaining their contents."""
    with path.open("rb") as stream:
        number = 0
        while True:
            offset = stream.tell()
            data = stream.readline(max_bytes + 1)
            if not data:
                return
            if on_chunk is not None:
                on_chunk(data)
            number += 1
            digest = hashlib.sha256(data)
            size = len(data)
            oversized = size > max_bytes
            if oversized:
                while not data.endswith(b"\n"):
                    data = stream.readline(max_bytes + 1)
                    if not data:
                        break
                    if on_chunk is not None:
                        on_chunk(data)
                    digest.update(data)
                    size += len(data)
                data = None
            yield number, {"line": number, "byte_offset": offset,
                           "raw_bytes": size, "sha256": digest.hexdigest()}, data


def events(args, stop=None):
    scanner = PrivateKeyScanner() if args.adapter == "text" else None
    for number, locator, data in read_lines(args.input, args.max_line_bytes,
                                          scanner.feed if scanner else None):
        redact_line = scanner.finish_line() if scanner else False
        if stop is not None and number > stop:
            break
        event = {**locator, "source_type": "unparsed"}
        try:
            if data is None:
                event.update(kind="unknown", note="oversized line omitted")
            elif args.adapter == "text":
                text = data.decode("utf-8")
                safe = "[REDACTED KEY]" if redact_line else text
                event.update(kind="export_line", source_type="text", text=safe)
            else:
                record = json.loads(data)
                if not isinstance(record, dict):
                    raise ValueError("non-object")
                if args.adapter == "codex" and {"session_id", "ts", "text"} <= record.keys() and "type" not in record:
                    raise RuntimeError("global message history is not a Codex rollout")
                payload = record.get("payload")
                kind = record.get("type", "unknown")
                subtype = payload.get("type", "") if isinstance(payload, dict) else ""
                event.update(source_type=kind if isinstance(kind, str) else "unknown",
                             payload_type=subtype if isinstance(subtype, str) else "unknown",
                             timestamp=record.get("timestamp"), ordinal=record.get("ordinal"),
                             field_names=list(record)[:16])
                event.update(ADAPTERS[args.adapter](record, args.include_tool_output))
        except (ValueError, UnicodeError, RecursionError):
            event.update(kind="unknown", note="malformed record omitted; original retained")
        yield event


def bounded(event, limit):
    event = scrub(event)
    if isinstance(event.get("text"), str):
        text = event["text"]
        event["text_chars"] = len(text)
        event["text"] = text[:limit]
        event["text_truncated"] = len(text) > limit
    if "tools" in event:
        tools = event["tools"]
        event["tools"] = [bounded(tool, limit) for tool in tools[:8]]
        event["tools_omitted"] = max(0, len(tools) - 8)
    return event


def discover(args):
    root = args.root
    if root is None:
        variable = "CODEX_HOME" if args.adapter == "codex" else "CLAUDE_CONFIG_DIR"
        home = args.agent_home or os.environ.get(variable)
        if not home:
            raise RuntimeError(f"set --root, --agent-home or {variable}; no assumed home")
        if not args.sessions_subdir:
            raise RuntimeError("--sessions-subdir required; verify current vendor layout")
        subdir = Path(args.sessions_subdir)
        if subdir.is_absolute() or ".." in subdir.parts:
            raise RuntimeError("sessions subdirectory must stay within agent home")
        root = Path(home).expanduser() / subdir
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise RuntimeError("session root is not a directory")
    scanned = 0
    # No symlink traversal; do not open auth/config/environment files.
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            if not name.endswith((".jsonl", ".jsonl.zst")) or name == "history.jsonl":
                continue
            path = Path(directory) / name
            if path.is_symlink():
                continue
            scanned += 1
            if scanned > args.max_files:
                yield {"notice": "file limit reached; narrow discovery root", "limited": True}
                return
            info = {"path": str(path), "bytes": path.stat().st_size}
            if name.endswith(".zst"):
                info["note"] = "compressed: use separate read-only decompression copy"
            else:
                args.input = path
                for event in events(args, stop=16):
                    if event.get("kind") == "metadata" or event.get("session_id"):
                        for key in ("id", "session_id", "cwd", "cli_version", "version", "forked_from_id", "parent_thread_id"):
                            if event.get(key) is not None:
                                info[key] = event[key]
                        break
            if args.session_id and args.session_id not in (name, info.get("id"), info.get("session_id")) and args.session_id not in name:
                continue
            if args.cwd and info.get("cwd") != args.cwd:
                continue
            yield info


def select(args):
    if args.command == "discover":
        yield from discover(args)
        return
    if args.command == "window":
        low, high = max(1, args.line - args.before), args.line + args.after
        includes = set(args.include_line)
        seen = set()
        for event in events(args, stop=max(high, max(includes, default=0))):
            line = event["line"]
            if low <= line <= high or line in includes:
                seen.add(line)
                yield event
        if args.line not in seen or includes - seen:
            raise RuntimeError("requested correction/include line does not exist")
    else:
        for event in events(args):
            candidate = event.get("candidate", event.get("role") == "user" and bool(event.get("text")))
            if args.adapter == "text":
                candidate = True  # Export headings are not a stable role schema.
            if args.scope == "user" and not candidate:
                continue
            searchable = str(event.get("text", "")) + json.dumps(event.get("tools", []))
            if args.query and not any(query.casefold() in searchable.casefold() for query in args.query):
                continue
            yield event


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def nonnegative(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("discover", "candidates", "window"):
        item = sub.add_parser(command)
        item.add_argument("--adapter", choices=[*ADAPTERS, "text"], required=True)
        item.add_argument("--verified-format", help="Claude local: installed version + verification evidence label")
        item.add_argument("--include-tool-output", action="store_true", help="include bounded selected result previews")
        item.add_argument("--max-line-bytes", type=positive, default=2_000_000)
        item.add_argument("--max-events", type=positive, default=80)
        item.add_argument("--chars", type=positive, default=1000)
        item.add_argument("--budget", type=positive, default=24000, help="total JSONL output characters")
        if command == "discover":
            item.add_argument("--root", type=Path)
            item.add_argument("--agent-home")
            item.add_argument("--sessions-subdir")
            item.add_argument("--session-id")
            item.add_argument("--cwd")
            item.add_argument("--max-files", type=positive, default=1000)
        else:
            item.add_argument("--input", type=Path, required=True)
        if command == "window":
            item.add_argument("--line", type=positive, required=True, help="physical correction line; not a turn number")
            item.add_argument("--before", type=nonnegative, default=20)
            item.add_argument("--after", type=nonnegative, default=20)
            item.add_argument("--include-line", type=positive, action="append", default=[])
        if command == "candidates":
            item.add_argument("--query", action="append", default=[], help="literal candidate hint; not semantic diagnosis")
            item.add_argument("--scope", choices=["user", "all"], default="user")
    args = parser.parse_args()
    if args.adapter == "claude-local" and not args.verified_format:
        parser.error("claude-local requires --verified-format; prefer documented /export")
    if args.command == "discover" and args.adapter == "text":
        parser.error("text exports require an explicit --input with candidates/window")
    try:
        if args.command != "discover":
            args.input = args.input.expanduser().resolve()
        header = {"schema": "skill-evidence/v1", "adapter": args.adapter,
                  "verified_format": args.verified_format,
                  "input": str(getattr(args, "input", "")),
                  "notice": "untrusted evidence; review redaction; limits/omissions are evidence gaps"}
        header = json.dumps(scrub(header), ensure_ascii=True)
        if len(header) + 2 > args.budget:
            raise RuntimeError("budget too small for header")
        print(header)
        used, count = len(header) + 1, 0
        footer = json.dumps({"notice": "output limit reached; narrow selection or increase limits"})
        for event in select(args):
            encoded = json.dumps(bounded(event, args.chars), ensure_ascii=True)
            if count >= args.max_events or used + len(encoded) + len(footer) + 2 > args.budget:
                if used + len(footer) + 1 <= args.budget:
                    print(footer)
                return 3
            print(encoded)
            used += len(encoded) + 1
            count += 1
            if event.get("limited"):
                return 3
    except (OSError, RuntimeError, RecursionError) as error:
        print(f"history: {redact(str(error))}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
