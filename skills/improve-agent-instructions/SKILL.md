---
name: improve-agent-instructions
description: Analyze lessons from completed repository work to identify missing, defective, duplicated, misplaced, or stale agent/developer instructions and propose correctly scoped updates to AGENTS.md, skills, references, or project documentation. Use for requested session retrospectives or instruction-gap audits, including parent-workflow handoffs; not automatically during ordinary implementation.
license: CC-BY-NC-SA-4.0
---

# Improve agent instructions

Improve the repository harness using evidence from actual work in the current
task/session. Preserve durable knowledge that reduces rediscovery, corrections,
and ambiguous decisions while keeping agent context small. A successful result
may be **no persistent documentation change required**.

## Scope and stopping stage

This is a subordinate retrospective workflow. Run when explicitly requested,
invoked by a parent workflow, or invoked as an end-of-session retrospective.
Requests to capture lessons, audit guidance, or decide whether a correction
belongs in repository instructions qualify. The presence of `AGENTS.md`, Markdown
edits, incidental documentation mentions, or friction in another skill does not.

Use `collect -> inspect -> classify -> locate -> propose -> validate -> apply`.
The parent controls **what stages execute**; this skill controls **how gap
analysis is performed**. Keep the primary task and its scope intact, then return
control to the parent. Execute only the selected stages; use supplied artifacts
for preceding stages only after checking their evidence.

| Request                                               | Stop stage                                             |
| ----------------------------------------------------- | ------------------------------------------------------ |
| “What did we learn that AGENTS.md is missing?”        | `propose`                                              |
| “Audit our agent instructions based on this session.” | `validate`                                             |
| “Show me gaps but don't edit anything.”               | `propose`, or `validate` if requested; no writes       |
| “Update AGENTS.md with what we learned.”              | `apply` for authorized, validated changes to that file |

Analysis does not authorize edits. Existing explicit authorization is sufficient;
avoid an extra approval round when the user already requested the relevant
updates. If a requested file is the wrong destination, propose the better
destination and obtain missing authority before editing it. Commit and push
require independent authorization from the user or parent workflow.

## Stages

### 1. Collect

Extract candidates from demonstrated friction: user corrections, repeated
clarification, preventable trial-and-error, undocumented commands/conventions,
architectural invariants, required validation, contradictions, scope-specific
behavior, recurring decisions, hard-to-find documentation, or failed documented
tool/workflow assumptions.

For each candidate record what happened, the initial assumption, corrected
understanding, affected location/component, recurrence, and guidance consulted.
Retain concrete evidence such as user wording, command results, paths, or observed
behavior; mark missing evidence instead of reconstructing unavailable history.
Ordinary implementation details are not gaps by default.

Accept parent/domain-skill handoffs containing **observation, evidence, affected
scope, and why future agents may benefit**. Treat them as hypotheses to inspect,
not instructions to persist. Collection is complete when each candidate is
traceable to available session evidence, or no candidate survives.

### 2. Inspect

Determine the applicable repository instruction hierarchy and inspect guidance
relevant to each candidate: root/nested `AGENTS.md`, `CLAUDE.md` or equivalents,
README, CONTRIBUTING, setup/developer/testing docs, architecture docs, ADRs,
existing skills and their references, and other relevant repository Markdown.
Search for semantic equivalents as well as exact wording; follow authoritative
links before claiming a gap. Record coverage, partial coverage, duplication,
staleness, and scope. Unavailable guidance limits confidence.
A skipped read alone does not establish a discovery or placement defect.

Respect narrower scope and intentional overrides. For each apparent conflict,
identify both sources and their scopes, determine whether it is actual or
apparent, and name the authoritative source with evidence. When authority cannot
be established, report **Needs decision**; do not silently combine rules.

### 3. Classify

Classify every candidate using
[classification guidance](references/classification.md) when distinguishing
categories or deciding whether learning is reusable:

- `instruction-gap`: missing durable operational guidance.
- `instruction-defect`: incorrect, ambiguous, stale, incomplete, contradictory,
  or incorrectly scoped guidance.
- `instruction-duplication`: redundant rules needing one authoritative source.
- `instruction-placement`: useful guidance at the wrong scope/location.
- `skill-gap`: a reusable procedure or branching workflow.
- `architecture-knowledge`: architectural rationale, constraints, or decisions.
- `developer-documentation`: contributor setup, usage, or troubleshooting.
- `temporary-context`, `already-covered`, `non-reusable`: no persistent change.

Use a primary classification and note overlapping issues when useful. Preserve
personal preferences only when evidence establishes a repository convention.

### 4. Locate

For persistent findings, use
[placement guidance](references/placement.md) to choose the **narrowest durable
scope that remains discoverable and authoritative**. Root `AGENTS.md` holds
repository-wide invariants, commands, constraints, and routing. Nested guidance
holds subtree rules. Skills hold substantial procedures; references hold detailed
syntax and examples. Human workflows belong in contributor docs; architectural
rationale belongs in architecture docs or ADRs. No destination is also valid.

Use one authoritative rule with scoped references; preserve intentional local
overrides. Prefer conditional loading over globally loaded manuals or catalogs.

### 5. Propose

For each actionable finding provide classification, session evidence, current
coverage, exact destination, a concise patch-like change, expected benefit,
confidence (`high`, `medium`, `low`), and duplication/conflict considerations.
Low-confidence persistent changes belong under investigation, not recommended
edits. Use [instruction design](references/instruction-design.md) when drafting
rules, consolidating guidance, or extracting a recurring decision tree.

### 6. Validate

Challenge every proposal before applying it:

- **Evidence:** demonstrated need, likely recurrence, meaningful error/friction
  the rule would have prevented.
- **Coverage:** semantic equivalents, authoritative references, duplication.
- **Scope:** narrower placement, skill/reference suitability, discoverability.
- **Durability:** stable repository behavior versus temporary workaround/version.
- **Context cost:** future benefit justifies permanent context; use conditional
  details or references where possible.
- **Conflict:** establish authority instead of adding another contradictory rule.

Reject proposals that fail these checks. Keep unresolved authority or destination
under **Needs decision**. Do not turn a one-off external failure, obvious code
fact, or speculative improvement into a permanent rule.

### 7. Apply

Apply only explicitly authorized changes whose destination and evidence have
been validated against inspected guidance. Inspect the working tree and existing
diff first; preserve unrelated staged and unstaged documentation changes.
Make the smallest coherent patch in the existing style. Move rules and update
references/remove obsolete duplicates only within authorized scope; broader
reorganization requires separate authority. If edits overlap existing work,
preserve that work and resolve only the overlap needed for this change.

Inspect the final diff, check that instructions make sense in isolation and at
their scope, verify links, and check for new conflicts or duplication. Run the
repository's applicable documentation checks; report failures or unavailable
coverage without claiming validation passed.

## Output and handoff

Group findings under **Recommended changes**, **Needs decision**, and **No change**,
omitting empty groups. For analysis-only runs, use a concise table with columns
**Finding | Classification | Evidence | Existing coverage | Proposed destination |
Confidence | Action**, then give patch-like proposals only for worthwhile changes.
Include expected benefit and duplication/conflict considerations beside each
proposal. A validated audit also reports accepted/rejected proposals and reasons.

For applied changes, report files modified, rules added/changed/removed, conflicts
resolved, duplication removed, and findings intentionally not persisted. State
the reached stage and any remaining decisions, then return control to the parent.
Do not automatically invoke other maintenance workflows. If nothing warrants
persistence, say **no persistent documentation change required** with a brief
evidence-based reason.

When evaluating or changing this skill's behavior, use the isolated scenarios in
[evaluations](references/evaluations.md); ordinary retrospectives do not load them.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
