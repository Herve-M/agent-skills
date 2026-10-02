# Reverse Skill Engineer

Improve an existing agent skill using evidence from real execution sessions.
The agent-facing entrypoint is [SKILL.md](SKILL.md); this README explains the
motivation and how to use the skill.

## Why this skill exists

An agent can select the right skill, make a mistake, receive a user correction,
and then succeed. That sequence is a useful starting point for improvement,
but it does not prove that the skill caused the mistake.

The instruction might be missing or ambiguous. It might already be clear and
the agent failed to follow it. The correction could also express a project
convention, a personal preference, or a requirement unique to that task.
Turning every correction into a reusable instruction creates duplication,
unnecessary work, and rules that fit one conversation rather than future tasks.

This skill separates evidence capture from diagnosis. It asks whether the
reusable skill is deficient, identifies where an improvement belongs, and
connects accepted behavioral changes to regression evals. **Decision: no skill
change** is a successful outcome, including when an eval is still warranted.

## Workflow

```text
Skill execution → observed failure → user correction → improved execution
                                      ↓
                            Capture compact evidence
                                      ↓
                         Analyze in a fresh context
                                      ↓
                       Compare rule, action, recovery
                                      ↓
                           Classify the root cause
                                      ↓
                      Does the reusable skill need a change?
                         ↙                         ↘
                       Yes                     No / uncertain
                        ↓                           ↓
              Smallest general rule       Eval only, another destination,
              + regression/control eval   or unresolved evidence question
                        ↓
                 Minimal patch → validation
```

Independent recurring failures strengthen a diagnosis. A single case can
suffice when it demonstrates a clear invariant or correctness defect. Related
sessions still need compatible contexts; copied or forked histories do not
establish independent recurrence.

## How to use it

### Capture a correction in the live session

After a correction, ask the agent:

```text
Use reverse-skill-engineer in Capture mode for the correction I just made.
The affected skill is skills/catalog/SKILL.md. Preserve the relevant rule,
behavior before and after my correction, outcome, and session/tool locators.
Return a compact candidate inline. Leave the affected skill unchanged.
```

Capture uses [the candidate template](templates/capture.md). It records the
skill revision and available evidence, marks unknowns, and preserves a
hypothesis for later investigation. If you want a saved record, specify a
private destination outside version control.

### Analyze the evidence in a fresh session

Supply the capture record, original history or bounded excerpts, the exact
executed skill revision, and relevant project instructions or existing evals.
Then ask:

```text
Use reverse-skill-engineer in Analyze mode on the supplied capture record,
session excerpts, and executed catalog skill revision.
Decide whether the correction exposes a reusable skill deficiency. Compare
the original rule, observed action, correction, and recovery. Produce a
retrospective, the smallest justified patch, and a behavioral regression eval.
Include a control when useful. Propose changes for review before applying them.
```

The output follows [the retrospective template](templates/retrospective.md):
root cause, evidence, decision, destination, patch if justified, evals,
confidence, and unresolved questions. Destinations include the skill entrypoint,
reference material, a script/tool, evals only, project instructions, or nowhere.
See [the analysis guide](references/analysis.md) for attribution criteria.

### Narrow a large history first

From this skill directory, the helper can locate candidate corrections and
extract a bounded window:

```bash
python3 scripts/history.py candidates --adapter codex \
  --input /private/rollout.jsonl --query 'inspect the next page' --chars 200
python3 scripts/history.py window --adapter codex \
  --input /private/rollout.jsonl --line 240 --before 16 --after 20
```

Use session rollouts rather than Codex's global prompt history. For Claude Code,
prefer a documented export when sufficient; richer local transcripts require
format verification. See [history handling](references/history-adapters.md) for
adapters, discovery, limits, and compatibility requirements.

Keep originals read-only and private. Tool results are omitted by default;
include only necessary selected output. Automatic redaction is incomplete,
so review excerpts before sharing them. Clipping and omitted records are
evidence gaps, even when extraction succeeds.

## Example decisions

- **Patch justified:** A catalog skill explains how to list results but omits
  how to handle pagination. The agent stops at page one; inspecting subsequent
  pages reveals missing items. Add the smallest completeness rule, then eval
  it using a different dataset with multiple pages. A single-page control
  checks that the rule does not cause unnecessary calls.
- **No skill change:** A skill already clearly requires verification before
  claiming success. The agent skips it and the user corrects that behavior.
  Diagnose adherence or context delivery, and add an eval requiring observable
  verification. Duplicating the existing instruction needs separate evidence.

Synthetic retrospective cases are available in
[the eval guide](references/evals.md). Parser tests verify extraction mechanics;
they do not establish that an agent makes the right semantic diagnosis.

## Changelog

### 2026-10-02

- Added this rationale, workflow, usage examples, and changelog.

### 2026-09-30

- `9f69eb2`: Detect private-key delimiters split across ordered string chunks;
  enforce record limits before reading the next record.
- `3bd5019`: Redact whole structured tool values containing private-key
  delimiters, including tool arguments.
- `0d9e17e`: Preserve private-key detection on oversized plaintext lines and
  correction candidates in mixed Claude user records.
- `4011d1e`: Introduce capture and analysis modes, history extraction helpers,
  templates, references, and initial retrospective eval cases.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->

## Notes
