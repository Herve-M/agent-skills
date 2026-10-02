# Improve agent instructions

Turn lessons from completed repository work into better guidance for future
agents and developers. [SKILL.md](SKILL.md) contains the authoritative execution
instructions; this README explains the purpose and how to request the workflow.

## Why this skill exists

Real work exposes gaps that a general documentation review can miss: a user
corrects a skipped check, setup instructions use a removed flag, or a subsystem's
rules are buried in globally loaded guidance. Without a retrospective, future
agents may repeat the same discovery and require the same corrections.

Persisting every observation creates a different problem: duplicated rules,
stale workarounds, and an expanding `AGENTS.md` that makes important constraints
harder to find. This skill evaluates whether a reusable gap exists before
deciding what to preserve and where it belongs.

The goal is fewer repeated mistakes and smaller, more precise context. Useful
knowledge may belong in nested instructions, a skill reference, CONTRIBUTING,
developer documentation, or an ADR. Sometimes the correct result is
**no persistent documentation change required**, including when an agent simply
failed to read guidance that already covers the lesson.

## How to use it

Invoke the skill after relevant work, while the session evidence is available.
State whether you want proposals, a validated audit, or file edits. If the work
was performed in another session, provide the observations, evidence, affected
scope, and expected future benefit; the skill will evaluate that handoff.

### Find gaps without editing

```text
$improve-agent-instructions
What did we learn from this task that our agent/developer guidance is missing?
Show concrete proposals and their best destinations. Do not edit any files.
```

This runs through proposal: it inspects existing coverage and returns findings
with evidence, classification, destination, confidence, and suggested patches.

### Audit and challenge proposed changes

```text
$improve-agent-instructions
Audit our repository instructions based on this session. Validate each proposed
improvement for evidence, scope, durability, duplication, and context cost.
Do not edit files.
```

This runs through validation, rejecting weak proposals and surfacing unresolved
conflicts for a decision.

### Apply improvements

```text
$improve-agent-instructions
Update repository guidance with the durable lessons from this task. Choose the
appropriate files, validate the changes, and preserve unrelated edits.
Do not commit or push.
```

This authorizes edits to suitable repository guidance. To restrict the work,
name the allowed files instead, such as “Update AGENTS.md only.” If a finding
belongs elsewhere, the skill proposes that destination and waits for authority
to edit it. A request for analysis alone does not authorize writes.

### Use within a larger workflow

```text
After fixing the migration, invoke improve-agent-instructions with the candidate
learnings. Run only through classify, then return to the release preparation
workflow. Do not change documentation.
```

The parent chooses the stages and retains control of its primary task. Candidate
learnings from another skill are hypotheses, not automatic documentation updates.

## Workflow

```text
collect -> inspect -> classify -> locate -> propose -> validate -> apply
```

The flow stops at the requested stage. Validation challenges the proposals;
application requires explicit edit authority. Candidates can be discarded as
already covered, temporary, or non-reusable without producing a patch.

For example, suppose a user corrects a missed schema check after a catalog
change. The skill first checks whether the requirement is already documented.
If it is covered adequately, no persistent change is needed. If the requirement
is durable, missing, and catalog-specific, the proposal targets nested catalog
guidance. It becomes a patch only when editing that destination is authorized.

Findings are grouped as **Recommended changes**, **Needs decision**, and
**No change**. An actual unresolved contradiction remains a decision even when
editing is authorized. Applied results identify the files and rules changed,
validation results, and findings intentionally left out.

For deeper guidance, see [classification](references/classification.md),
[instruction design](references/instruction-design.md), and
[placement](references/placement.md). The
[evaluation scenarios](references/evaluations.md) document behavioral coverage
and the checks actually performed.

## Changelog

### 2026-10-02

- Added this README with rationale, usage examples, and workflow explanation.

### 2026-09-30

- Created the seven-stage retrospective skill with classification, instruction
  design, and placement references.
- Added 24 evaluation scenarios and recorded independent fixture checks.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->

## Notes
