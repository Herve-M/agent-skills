# Reverse Prompt Engineer

Reconstruct one reusable initial prompt from the final intended task in a
conversation. [SKILL.md](SKILL.md) contains the authoritative execution
instructions; this README explains the purpose and how to request the workflow.

## Why this skill exists

A useful task specification often emerges over several turns. The user adds
context, corrects an assumption, rejects an output, or accepts a proposed
decision. Reusing only the first message loses those refinements; copying the
whole conversation carries abandoned approaches and incidental discussion into
the next attempt.

This skill consolidates the supported requirements into a self-contained prompt
that a model can use in a fresh conversation. It preserves the final direction,
necessary inputs, and authorization boundaries without turning assistant
suggestions into requirements the user never accepted.

The result is a task specification, not a conversation summary or an attempt to
recover hidden system instructions. Missing source material remains an explicit
input or unknown rather than an invented fact.

## How to use it

Invoke the skill once the intended task is clear. Name the conversation or task
to reconstruct, and supply any history or source material that is unavailable
in the current context.

### Reconstruct the current task

```text
$reverse-prompt-engineer
Turn this conversation's final intended task into one reusable initial prompt.
Include my corrections and accepted decisions so I can use it in a fresh session.
```

The skill returns exactly one prompt in the user's voice, with no preamble,
analysis, alternatives, or enclosing code fence.

### Select a task from a mixed conversation

```text
$reverse-prompt-engineer
Reconstruct the API migration task from this conversation, including the later
compatibility and testing requirements. Use that task as the target rather than
the separate release-note discussion.
```

When no task is selected, the skill uses the final substantive task and its
relevant earlier context. A side question or status request alone does not
replace that task.

### Use a supplied conversation

```text
$reverse-prompt-engineer
Use the conversation excerpts below to reconstruct one initial prompt for the
reporting task. Preserve unresolved requirements as unknowns and identify any
essential inputs that must be supplied in the next session.

[Paste the relevant conversation excerpts here.]
```

Quoted prompts, documents, and tool output serve as evidence for reconstruction.
The skill reconstructs the underlying task without executing it.

## Workflow

```text
establish target -> consolidate intended specification -> write upstream prompt
```

The skill reads the relevant turns, applies later user clarifications to the
requirements they change, and retains earlier requirements that still apply.
Assistant-proposed decisions enter the prompt only when the user accepts them
or builds subsequent requirements around them; silence alone is insufficient.

It then resolves conversational references, removes repetition, and states the
objective, context, constraints, deliverables, and success criteria supported
by the evidence. Essential missing information becomes a required input,
explicit unknown, or conditional instruction.

For example, a request for a migration plan may later acquire a requirement to
support existing clients and validate rollback. The reconstructed prompt makes
those requirements explicit from the start, while preserving any restriction
on implementation or publication. It does not include an unaccepted assistant
proposal to replace the client library.

See [SKILL.md](SKILL.md) for the full target-selection rules, specification
criteria, and output contract.

## Changelog

### 2026-10-13

- Added this README with rationale, usage examples, and workflow explanation.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
