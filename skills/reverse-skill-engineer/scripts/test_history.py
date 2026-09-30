#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Synthetic integration checks for read-only extraction and privacy boundaries."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("history.py")


def message(role, text):
    return {"type": "response_item", "payload": {"type": "message", "role": role,
            "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]}}


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "rollout.jsonl"
        self.write([
            {"type": "session_meta", "payload": {"id": "s1", "cwd": "/project", "cli_version": "synthetic"}},
            message("user", "Inventory the published items."),
            {"type": "response_item", "payload": {"type": "function_call", "name": "read",
             "call_id": "c1", "arguments": '{"path":"skills/catalog/SKILL.md"}'}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "c1",
             "output": "Large private output: hidden-result"}},
            message("assistant", "There are two items."),
            message("user", "Inspect the next page first."),
            {"type": "future_event", "payload": {"secret": "unknown-secret"}},
            message("assistant", "Four items inspected."),
        ])

    def write(self, records):
        self.source.write_text("".join(json.dumps(record) + "\n" for record in records))

    def run_helper(self, *args, adapter="codex", input_path=None, env=None):
        completed = subprocess.run([sys.executable, str(SCRIPT), args[0], "--adapter", adapter,
                                    "--input", str(input_path or self.source), *args[1:]],
                                   capture_output=True, text=True, env=env)
        output = [json.loads(line) for line in completed.stdout.splitlines()]
        return completed, output

    def test_order_linkage_unknown_and_read_only(self):
        original = self.source.read_bytes()
        result, output = self.run_helper("window", "--line", "6", "--before", "2", "--after", "2",
                                         "--include-line", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        events = output[1:]
        self.assertEqual([e["line"] for e in events], [3, 4, 5, 6, 7, 8])
        self.assertEqual(events[0]["call_id"], events[1]["call_id"])
        self.assertNotIn("hidden-result", result.stdout)
        self.assertNotIn("unknown-secret", result.stdout)
        self.assertEqual(events[4]["kind"], "unknown")
        self.assertEqual(events[4]["source_type"], "future_event")
        line = original.splitlines(keepends=True)[6]
        self.assertEqual(events[4]["sha256"], hashlib.sha256(line).hexdigest())
        self.assertEqual(self.source.read_bytes(), original)

    def test_user_candidates_and_loading_search(self):
        result, output = self.run_helper("candidates", "--query", "next page")
        self.assertEqual(result.returncode, 0)
        self.assertEqual([e["line"] for e in output[1:]], [6])
        result, output = self.run_helper("candidates", "--scope", "all", "--query", "SKILL.md")
        self.assertEqual([e["line"] for e in output[1:]], [3])

    def test_redaction_precedes_truncation(self):
        self.write([message("user", "Bearer private-bearer-value TOKEN=env-secret-value "
                            "api_key=credential-value sk-abcdefghijklmno "
                            "https://user:password@example.test/data")])
        result, output = self.run_helper("window", "--line", "1", "--chars", "75")
        for secret in ("private-bearer-value", "env-secret-value", "credential-value", "abcdefghijklmno", "user:password"):
            self.assertNotIn(secret, result.stdout)
        self.assertTrue(output[1]["text_truncated"])

    def test_tool_arguments_and_results_scrub_nested_secrets(self):
        self.write([
            {"type": "response_item", "payload": {"type": "function_call", "name": "exec",
             "arguments": json.dumps({"api_key": "nested-secret", "env": {"OTHER": "environment-secret"},
                                      "command": "run --password flag-secret"})}},
            {"type": "response_item", "payload": {"type": "function_call_output", "output":
             {"credential": "result-secret", "content": "-----BEGIN PRIVATE KEY-----\nprivate-key-body\n-----END PRIVATE KEY-----"}}},
        ])
        result, output = self.run_helper("window", "--line", "1", "--include-tool-output")
        self.assertEqual(result.returncode, 0)
        for secret in ("nested-secret", "environment-secret", "flag-secret", "result-secret", "private-key-body"):
            self.assertNotIn(secret, result.stdout)

    def test_structured_tool_result_with_split_key_is_redacted_as_a_whole(self):
        self.write([
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "split-key-call",
             "output": {"lines": ["-----BEGIN PRIVATE KEY-----", "SYNTHETICPRIVATEKEYBODY",
                                   "-----END PRIVATE KEY-----"], "other": "unrelated output"}}},
        ])
        original = self.source.read_bytes()
        result, output = self.run_helper("window", "--line", "1", "--include-tool-output")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("SYNTHETICPRIVATEKEYBODY", result.stdout)
        self.assertNotIn("unrelated output", result.stdout)
        self.assertEqual(output[1]["text"], "[REDACTED KEY]")
        self.assertEqual(output[1]["call_id"], "split-key-call")
        self.assertEqual(output[1]["sha256"], hashlib.sha256(original).hexdigest())
        self.assertEqual(output[1]["byte_offset"], 0)
        self.assertEqual(self.source.read_bytes(), original)

    def test_structured_key_redaction_covers_arguments_and_unordered_results(self):
        begin = "-----BEGIN OPENSSH PRIVATE KEY-----"
        end = "-----END OPENSSH PRIVATE KEY-----"
        body = "SYNTHETICPRIVATEKEYBODY"
        cases = {
            "list": [begin, body, end],
            "body-first-dictionary": {"body": body, "header": begin, "footer": end},
            "nested-siblings": {"header": {"text": begin}, "body": {"lines": [body]}, "footer": end},
            "json-encoded": json.dumps({"lines": [begin, body, end]}),
            "opening-only": {"header": begin, "body": body},
            "closing-only": {"body": body, "footer": end},
            "delimiter-in-key": {begin: body},
        }
        for name, value in cases.items():
            for event_type, field in (("function_call", "arguments"), ("function_call_output", "output")):
                with self.subTest(case=name, event_type=event_type):
                    self.write([
                        {"type": "response_item", "payload": {"type": event_type, "name": "fixture-tool",
                         "call_id": "sensitive-call", field: value}},
                        {"type": "response_item", "payload": {"type": event_type, "name": "fixture-tool",
                         "call_id": "clean-call", field: {"text": "ordinary output"}}},
                    ])
                    flags = ("--include-tool-output",) if event_type == "function_call_output" else ()
                    result, output = self.run_helper("window", "--line", "1", *flags)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertNotIn(body, result.stdout)
                    self.assertEqual(output[1]["text"], "[REDACTED KEY]")
                    self.assertEqual(output[1]["call_id"], "sensitive-call")
                    self.assertEqual(json.loads(output[2]["text"]), {"text": "ordinary output"})
                    if event_type == "function_call":
                        self.assertEqual(output[1]["name"], "fixture-tool")

    def test_split_keys_in_claude_content_blocks_are_redacted(self):
        content = [{"type": "text", "text": text} for text in
                   ("-----BEGIN RSA PRIVATE KEY-----", "SYNTHETICCLAUDEKEYBODY", "-----END RSA PRIVATE KEY-----")]
        self.write([
            {"type": "user", "message": {"role": "user", "content":
             [{"type": "tool_result", "tool_use_id": "claude-call", "content": content}]}},
            {"type": "assistant", "message": {"role": "assistant", "content":
             [{"type": "tool_use", "id": "claude-input", "name": "fixture-tool", "input": {"lines": content}}]}},
        ])
        result, output = self.run_helper("window", "--line", "1", "--include-tool-output",
                                         "--verified-format", "synthetic fixture", adapter="claude-local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("SYNTHETICCLAUDEKEYBODY", result.stdout)
        self.assertEqual(output[1]["tools"][0]["text"], "[REDACTED KEY]")
        self.assertEqual(output[1]["tools"][0]["call_id"], "claude-call")
        self.assertEqual(output[2]["tools"][0]["text"], "[REDACTED KEY]")
        self.assertEqual(output[2]["tools"][0]["name"], "fixture-tool")
        result, output = self.run_helper("window", "--line", "1", "--verified-format", "synthetic fixture", adapter="claude-local")
        self.assertEqual(output[1]["tools"][0]["text"], "[output omitted]")

    def test_structured_redaction_preserves_ordinary_values_and_output_limits(self):
        public_key = "-----BEGIN PUBLIC KEY-----\npublic-material\n-----END PUBLIC KEY-----"
        ordinary = {"lines": ["item one", "item two"], "count": 2, "public": public_key}
        single_string = ("before\n-----BEGIN PRIVATE KEY-----\nSYNTHETICSTRINGKEYBODY\n"
                         "-----END PRIVATE KEY-----\nafter")
        self.write([
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "ordinary", "output": ordinary}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "single", "output": single_string}},
            {"type": "response_item", "payload": {"type": "function_call_output", "call_id": "split",
             "output": ["-----BEGIN ENCRYPTED PRIVATE KEY-----", "SYNTHETICSPLITKEYBODY", "-----END ENCRYPTED PRIVATE KEY-----"]}},
        ])
        result, output = self.run_helper("window", "--line", "1", "--include-tool-output")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(output[1]["text"]), ordinary)
        self.assertEqual(output[2]["text"], "before\n[REDACTED KEY]\nafter")
        self.assertEqual(output[3]["text"], "[REDACTED KEY]")
        result, output = self.run_helper("window", "--line", "1")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(all(event["text"] == "[output omitted]" for event in output[1:]))
        result, output = self.run_helper("window", "--line", "3", "--before", "0", "--after", "0",
                                         "--include-tool-output", "--chars", "5")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(output[1]["text_truncated"])
        self.assertEqual(len(output[1]["text"]), 5)
        self.assertNotIn("SYNTHETICSPLITKEYBODY", result.stdout)
        result, output = self.run_helper("window", "--line", "1", "--include-tool-output", "--budget", "1200")
        self.assertEqual(result.returncode, 3)
        self.assertLessEqual(len(result.stdout), 1200)
        self.assertNotIn("SYNTHETICSTRINGKEYBODY", result.stdout)

    def test_claude_tool_results_are_not_corrections(self):
        self.write([
            {"type": "assistant", "uuid": "a1", "message": {"role": "assistant", "content":
             [{"type": "tool_use", "id": "tc1", "name": "Read", "input": {"path": "skill.md"}}]}},
            {"type": "user", "uuid": "u1", "message": {"role": "user", "content":
             [{"type": "tool_result", "tool_use_id": "tc1", "content": "correct this result"}]}},
            {"type": "user", "isMeta": True, "message": {"content": "correct system detail"}},
            {"type": "user", "isSynthetic": True, "message": {"content": "correct synthesized detail"}},
            {"type": "user", "uuid": "u2", "parentUuid": "a1", "sessionId": "s1", "message":
             {"role": "user", "content": [{"type": "text", "text": "Correct the validation claim."}]}},
        ])
        args = ("--verified-format", "synthetic fixture")
        result, output = self.run_helper("candidates", *args, adapter="claude-local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([e["line"] for e in output[1:]], [5])
        result, output = self.run_helper("window", "--line", "2", *args, adapter="claude-local")
        self.assertEqual(output[1]["tools"][0]["call_id"], output[2]["tools"][0]["call_id"])
        self.assertNotIn("correct this result", result.stdout)

    def test_claude_requires_verification_assertion(self):
        result, output = self.run_helper("window", "--line", "1", adapter="claude-local")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output, [])

    def test_malformed_nonobject_oversized_and_schema_drift(self):
        self.source.write_bytes(b'{broken\n[]\n' + b'x' * 250 + b'\n' +
                                json.dumps(message("user", "correction")).encode() + b'\n')
        result, output = self.run_helper("window", "--line", "4", "--max-line-bytes", "200")
        self.assertEqual(result.returncode, 0)
        self.assertEqual([e["kind"] for e in output[1:]], ["unknown", "unknown", "unknown", "message"])
        self.assertEqual(output[3]["raw_bytes"], 251)
        self.assertEqual(output[4]["line"], 4)
        self.write([message("user", "safe"), {"type": "response_item", "payload":
                    {"type": "message", "role": "assistant", "content": [{"type": "future_block", "data": "secret"}]}}])
        result, output = self.run_helper("window", "--line", "1")
        self.assertEqual(output[2]["unknown_blocks"], ["future_block"])
        self.assertNotIn('"secret"', result.stdout)

    def test_global_history_rejected(self):
        self.write([{"session_id": "s1", "ts": 1, "text": "prompt-only"}])
        result, output = self.run_helper("window", "--line", "1")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("prompt-only", result.stdout)

    def test_invalid_field_types_remain_locatable(self):
        self.write([
            {"type": ["unrecognized"], "payload": {}},
            {"type": "response_item", "payload": {"type": ["unrecognized"]}},
            {"type": "response_item", "payload": {"type": "message", "role": "user", "content":
             [{"type": {}, "text": "unrecognized-block"}, {"type": "input_text", "text": "inspect first"}]}},
            message("assistant", "recovered"),
        ])
        result, output = self.run_helper("window", "--line", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([e["kind"] for e in output[1:]], ["unknown", "unknown", "message", "message"])
        self.assertEqual(output[3]["text"], "inspect first")
        self.assertNotIn("unrecognized-block", result.stdout)

    def test_budgets_and_invalid_windows(self):
        result, output = self.run_helper("window", "--line", "6", "--max-events", "2")
        self.assertEqual(result.returncode, 3)
        self.assertIn("limit", output[-1]["notice"])
        result, output = self.run_helper("window", "--line", "6", "--budget", "1100")
        self.assertLessEqual(len(result.stdout), 1100)
        self.assertEqual(result.returncode, 3)
        result, output = self.run_helper("window", "--line", "900")
        self.assertEqual(result.returncode, 2)
        result, output = self.run_helper("window", "--line", "6", "--before", "-1")
        self.assertEqual(result.returncode, 2)

    def test_text_exports_and_multiline_keys(self):
        self.source.write_text("Human: inspect first\n-----BEGIN PRIVATE KEY-----\n"
                               "sensitive-body\n-----END PRIVATE KEY-----\nAssistant: done\n")
        result, output = self.run_helper("window", "--line", "3", adapter="text")
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("sensitive-body", result.stdout)
        self.assertEqual(output[1]["kind"], "export_line")
        self.assertNotIn("role", output[1])

    def test_oversized_key_delimiters_still_redact_text(self):
        original = (b"-----BEGIN OPENSSH PRIVATE KEY-----\nABC123\n"
                    b"-----END OPENSSH PRIVATE KEY-----\nafter\n")
        self.source.write_bytes(original)
        result, output = self.run_helper("window", "--line", "2", "--max-line-bytes", "10", adapter="text")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("ABC123", result.stdout)
        self.assertEqual(output[2]["text"], "[REDACTED KEY]")
        self.assertEqual(output[4]["text"], "after\n")
        self.assertEqual(output[1]["kind"], "unknown")
        offset = 0
        for event, line in zip(output[1:], original.splitlines(keepends=True)):
            self.assertEqual(event["sha256"], hashlib.sha256(line).hexdigest())
            self.assertEqual(event["raw_bytes"], len(line))
            self.assertEqual(event["byte_offset"], offset)
            offset += len(line)
        self.assertEqual(self.source.read_bytes(), original)

    def test_key_redaction_is_independent_of_chunk_and_line_caps(self):
        for label in ("", "RSA ", "EC ", "ENCRYPTED ", "OPENSSH "):
            for cap in (1, 2, 7, 10, 16, 200):
                with self.subTest(label=label, cap=cap):
                    self.source.write_text(f"-----BEGIN {label}PRIVATE KEY-----\nK\n"
                                           f"-----END {label}PRIVATE KEY-----\n.")
                    result, output = self.run_helper("window", "--line", "2", "--max-line-bytes", str(cap), adapter="text")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    body = output[2]
                    if cap >= 2:
                        self.assertEqual(body["text"], "[REDACTED KEY]")
                    else:
                        self.assertEqual(body["kind"], "unknown")
                    self.assertEqual(output[4]["text"], ".")

    def test_key_markers_after_long_prefixes_and_across_long_labels(self):
        for prefix, label in (("." * 4096, "RSA "), ("", "A" * 4096 + " ")):
            with self.subTest(prefix_length=len(prefix), label_length=len(label)):
                self.source.write_text(f"{prefix}-----BEGIN {label}PRIVATE KEY-----\nABC123\n"
                                       f"{prefix}-----END {label}PRIVATE KEY-----\nafter\n")
                result, output = self.run_helper("window", "--line", "2", "--max-line-bytes", "10", adapter="text")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn("ABC123", result.stdout)
                self.assertEqual(output[4]["text"], "after\n")
                # Boundaries outside the selected window still control its redaction.
                result, output = self.run_helper("window", "--line", "2", "--before", "0", "--after", "0",
                                                 "--max-line-bytes", "10", adapter="text")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output[1]["text"], "[REDACTED KEY]")

    def test_key_boundaries_follow_byte_order_and_reset_at_line_end(self):
        self.source.write_text(
            "-----BEGIN PRIVATE KEY----- inline-body -----END PRIVATE KEY-----\n"
            "ordinary\n-----BEGIN RSA PRIVATE KEY-----\ninside-one\n"
            "-----END RSA PRIVATE KEY----- gap -----BEGIN ENCRYPTED PRIVATE KEY-----\n"
            "inside-two\n-----END ENCRYPTED PRIVATE KEY-----\nordinary-again\n"
            "-----BEGIN RSA\nPRIVATE KEY-----\nvisible\n"
            "-----BEGIN OPENSSH PRIVATE KEY-----\nunterminated")
        result, output = self.run_helper("window", "--line", "6", adapter="text")
        self.assertEqual(result.returncode, 0, result.stderr)
        for secret in ("inline-body", "inside-one", "inside-two", "unterminated"):
            self.assertNotIn(secret, result.stdout)
        for line in (1, 3, 4, 5, 6, 7, 12, 13):
            self.assertEqual(output[line]["text"], "[REDACTED KEY]")
        for line, expected in ((2, "ordinary\n"), (8, "ordinary-again\n"),
                               (10, "PRIVATE KEY-----\n"), (11, "visible\n")):
            self.assertEqual(output[line]["text"], expected)
        result, output = self.run_helper("window", "--line", "6", "--budget", "1400", adapter="text")
        self.assertEqual(result.returncode, 3)
        self.assertLessEqual(len(result.stdout), 1400)
        self.assertNotIn("inline-body", result.stdout)
        result, output = self.run_helper("window", "--line", "6", "--max-events", "2", adapter="text")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(len(output), 4)  # Header, two events, limit notice.

    def test_mixed_claude_records_preserve_top_level_corrections(self):
        text = {"type": "text", "text": "Please inspect the next page first."}
        tool = {"type": "tool_result", "tool_use_id": "tc1", "content":
                [{"type": "text", "text": "private tool-result text"}]}
        self.write([
            {"type": "user", "message": {"role": "user", "content": [tool, text]}},
            {"type": "user", "message": {"role": "user", "content": [text, tool]}},
            {"type": "user", "message": {"role": "user", "content": [tool]}},
            {"type": "user", "isMeta": True, "message": {"content": [tool, text]}},
            {"type": "user", "isSynthetic": True, "message": {"content": [tool, text]}},
            {"type": "assistant", "message": {"role": "assistant", "content": [tool, text]}},
        ])
        args = ("--verified-format", "synthetic fixture")
        result, output = self.run_helper("candidates", "--query", "next page", *args, adapter="claude-local")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([event["line"] for event in output[1:]], [1, 2])
        for event in output[1:]:
            self.assertTrue(event["candidate"])
            self.assertEqual(event["text"], text["text"])
            self.assertEqual(event["tools"][0]["call_id"], "tc1")
            self.assertEqual(event["tools"][0]["text"], "[output omitted]")
        self.assertNotIn("private tool-result text", result.stdout)
        result, output = self.run_helper("candidates", *args, adapter="claude-local")
        self.assertEqual([event["line"] for event in output[1:]], [1, 2])
        result, output = self.run_helper("candidates", "--query", "private tool-result", *args, adapter="claude-local")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(output), 1)  # Nested tool-result text is not correction text.

    def test_configured_discovery_no_assumed_home_or_symlinks(self):
        sessions = self.root / "verified-sessions"
        sessions.mkdir()
        (sessions / "rollout.jsonl").write_bytes(self.source.read_bytes())
        (sessions / "history.jsonl").write_text('{"session_id":"s1","ts":1,"text":"secret"}\n')
        (sessions / "auth.json").write_text('secret')
        (sessions / "link.jsonl").symlink_to(self.source)
        environment = {**os.environ, "CODEX_HOME": str(self.root)}
        command = [sys.executable, str(SCRIPT), "discover", "--adapter", "codex",
                   "--sessions-subdir", "verified-sessions", "--cwd", "/project"]
        result = subprocess.run(command, capture_output=True, text=True, env=environment)
        output = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[1]["id"], "s1")
        self.assertNotIn("secret", result.stdout)
        (sessions / "another.jsonl").write_bytes(self.source.read_bytes())
        result = subprocess.run(command + ["--max-files", "1"], capture_output=True, text=True, env=environment)
        self.assertEqual(result.returncode, 3)
        self.assertIn("file limit", result.stdout)
        del environment["CODEX_HOME"]
        result = subprocess.run(command, capture_output=True, text=True, env=environment)
        self.assertEqual(result.returncode, 2)

    def test_many_records_keep_output_bounded(self):
        self.write([message("assistant", "filler")] * 10000 + [message("user", "Please verify first.")])
        result, output = self.run_helper("candidates", "--query", "verify")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[1]["line"], 10001)
        self.assertLess(len(result.stdout), 2000)


if __name__ == "__main__":
    unittest.main()
