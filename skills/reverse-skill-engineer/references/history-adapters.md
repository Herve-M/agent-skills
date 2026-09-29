# History adapters and bounded extraction

## Source status and discovery

Authoritative sources checked on **2026-09-30**. These are implementation
observations, not a permanent storage contract. Recheck the installed version
against current upstream sources when field coverage or discovery changes.
The helper uses explicit paths/configured roots rather than a built-in layout.

### Codex

[Configuration documentation](https://developers.openai.com/codex/config-advanced/)
defines `CODEX_HOME` with a `~/.codex` default. Resolve the actual configured
home; do not assume the shell's `$HOME` identifies the installation being
analyzed.

The
[rollout recorder](https://github.com/openai/codex/blob/main/codex-rs/rollout/src/recorder.rs)
persists replay/inspection JSONL. Its current path constructor uses
`CODEX_HOME/sessions/YYYY/MM/DD/` with rollout filenames. The
[rollout library](https://github.com/openai/codex/blob/main/codex-rs/rollout/src/lib.rs)
also identifies `archived_sessions` and compression support. Treat these as
dated discovery hints. Supply a verified sessions subtree explicitly, including
archives separately when relevant. Compressed rollouts require a separate
decompressed copy; never invoke a vendor materializer that rewrites originals.

The separate
[message-history implementation](https://github.com/openai/codex/blob/main/codex-rs/message-history/src/lib.rs)
stores global entries with `session_id`, `ts`, `text` in `history.jsonl`. These
can help correlate prompts with sessions but do not contain the execution
trajectory. The Codex adapter rejects that shape as a rollout.

The helper recognizes `session_meta`, `response_item` messages and tool events,
and `event_msg` user/agent messages. Verify envelopes using the
[history wire format](https://github.com/openai/codex/blob/main/codex-rs/history/src/rollout_payload.rs)
and
[response models](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/models.rs).
Event messages may mirror response messages: count neither duplicates nor
shared/forked ancestry as independent failures. Compaction, retained-context,
new tool types and other events remain locatable unknown records; inspect those
selectively when attribution depends on delivery/context. No comprehensive
replay or visibility reconstruction is claimed.

### Claude Code

Prefer documented
[`/export [filename]`](https://code.claude.com/docs/en/commands) when plain text
preserves enough evidence. `/resume` restores a session, `/clear` starts empty
context and `/branch` preserves a conversation ancestor; resuming/branching is
not independent analysis. Use a new context for diagnosis. The text adapter
extracts physical line windows without assuming export headings form a stable
role schema. Confirm correction speakers manually.

[Environment documentation](https://code.claude.com/docs/en/env-vars)
documents `CLAUDE_CONFIG_DIR` for a relocated configuration/history directory
and `CLAUDE_CODE_SESSION_ID` for correlation; availability/accuracy depends on
subprocess and resume context. Consult the installed version for persistence
controls. `CLAUDE_CODE_SKIP_PROMPT_HISTORY` was not present in the fetched
English environment page at this check: do not infer its semantics or that a
missing transcript means no execution occurred.

For richer tool evidence, the
[hook interface](https://code.claude.com/docs/en/hooks) provides
`transcript_path` and `session_id`; use a path already supplied by that
interface where available. Do not install hooks merely to analyze history. The
transcript path is documented; its complete local JSONL schema is not a stable
public API.

`claude-local` is an opt-in compatibility parser for records with `type`,
`message.content`, `sessionId`, `uuid` and `parentUuid`. Before using it, verify
a small redacted sample from the actual installed version against its export
and recorded tool events. Supply `--verified-format` with version plus a locator
to that verification. The flag records an operator assertion, not automatic
schema certification. This creation validated synthetic shapes, not a live
Claude installation. Tool-result-only user records, `isMeta` and `isSynthetic`
messages are excluded as correction candidates; inspect other provenance fields
in the original when human authorship is uncertain. New event/block shapes are
retained by locator, not silently interpreted.

## Helper workflow

Requires Python 3.10+; no vendor SDK or third-party package. Run from the skill
directory; replace example paths/line numbers with actual private evidence
paths.

1. Identify candidate sessions from capture IDs, documented exports or a narrow
   verified root. Discovery reads at most 16 records per file for metadata and
   caps scanned files. Supply date/project subtrees to limit disk work.

   ```bash
   python3 scripts/history.py discover --adapter codex \
     --agent-home /private/configured-codex --sessions-subdir sessions \
     --session-id SESSION-ID
   ```

   `--agent-home` can use the relevant `CODEX_HOME`/`CLAUDE_CONFIG_DIR` variable
   when present. Neither default home nor sessions subdirectory is guessed.
   `--root` accepts any verified subtree and avoids layout assumptions.

2. List user turns or narrow by literal correction hints. Semantic diagnosis
   belongs to the analyst; query matches are candidates, with false positives
   and negatives. A multilingual correction may contain none of your hints.

   ```bash
   python3 scripts/history.py candidates --adapter codex \
     --input /private/rollout.jsonl --query 'inspect first' --chars 200
   ```

   Search with `--scope all --query SKILL.md` or the skill path to find loading
   calls outside the correction window. Tool outputs are omitted by default;
   select their locator before requesting a bounded preview. Reconstruct paired
   tool calls/results via call IDs; the helper does not automatically expand
   pairs or prove the absence of missing events.

3. Extract the selected correction window and specific earlier loading/task
   lines. Limits count physical records/lines, not conversation turns.

   ```bash
   python3 scripts/history.py window --adapter codex \
     --input /private/rollout.jsonl --line 240 --before 16 --after 20 \
     --include-line 12 --include-line 18
   python3 scripts/history.py window --adapter text \
     --input /private/claude-export.txt --line 85
   python3 scripts/history.py window --adapter claude-local \
     --verified-format 'installed-version; private verification locator' \
     --input /private/transcript.jsonl --line 240
   ```

   Use `--include-tool-output` only for a necessary selected result. Narrow
   selection before raising limits. Exit 0 means selection completed, 2 means
   invalid input/error, 3 means an output budget/event cap stopped selection;
   partial output is not complete evidence. Check clipping/unknown notices even
   on exit 0. Correlate multiple extracts in the retrospective by source and ID.

## Extraction contract and sensitivity

Output is JSONL with a `skill-evidence/v1` header and normalized events: source
line, byte offset, original line digest/size, type, role or tool linkage when
known, and a bounded preview. Limits apply per line, preview, event count and
total output characters. Oversized/malformed records are omitted with locators.
Unknown events/fields remain in the untouched source; names and digests retain
their presence without copying arbitrary payloads. Digests identify records,
not a snapshot of the whole file; live appends may change later extracts.

The tool opens inputs read-only, does not execute transcript commands, makes no
network calls and emits only to stdout. Store redirected extracts privately.
Automatic redaction masks common credential forms, secret fields and environment
assignments; it may also hide benign assignments. It cannot guarantee secrecy
for arbitrary values, personal data, filenames or unfamiliar credential formats.
Inspect excerpts before sharing. Missing/redacted facts reduce confidence; use
private inspection rather than expanding raw outputs indiscriminately.

To add an adapter, map its verified input to message, tool call/result, metadata
or unknown events in `ADAPTERS`. Preserve source locators, distinguish human
corrections from tool/system input, test schema drift and privacy, and document
the interface/version boundary here. Core attribution needs no format changes.

All implementation and synthetic fixtures here are repository-authored. Sources
were consulted for interoperability facts; no upstream implementation or manual
was copied or vendored.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
