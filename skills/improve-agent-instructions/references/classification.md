# Classification and persistence

Use these distinctions after inspecting applicable guidance. A finding's
classification describes the underlying problem; its destination is a separate
decision. The examples below are synthetic, not evidence about the repository
being analyzed.

## Finding categories

| Classification            | Positive example                                                                                                                                                            | Boundary / negative example                                                                                                                  |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `instruction-gap`         | A user corrects skipped cross-package validation; repository policy requires it for every dependency change, but no applicable guidance records it.                         | A nested testing document already names the required check: `already-covered`, unless discovery or routing itself failed.                    |
| `instruction-defect`      | Setup docs prescribe a removed CLI flag; the session verifies the supported replacement. Also covers ambiguity, incomplete conditions, contradictions, and incorrect scope. | A narrower file explicitly overrides the root default for its subtree: intentional scope, not a contradiction.                               |
| `instruction-duplication` | Three files repeat the same validation rule and one copy has drifted.                                                                                                       | A short link to the authoritative rule is routing, not duplication; intentional local differences should remain.                             |
| `instruction-placement`   | A root instruction contains lengthy rules used only by the mobile project.                                                                                                  | A repository-wide invariant belongs at root even if first discovered in one module.                                                          |
| `skill-gap`               | Repeated migrations require a compatibility decision, staged rollout, and validation branches.                                                                              | One condition with one validation command is usually a scoped instruction, not a new skill.                                                  |
| `architecture-knowledge`  | The session uncovers why writes cross a service boundary only through an outbox and the trade-off that established it.                                                      | “When changing outbox code, run the contract tests” is operational guidance; link architectural rationale separately if needed.              |
| `developer-documentation` | New contributors must perform a non-obvious local bootstrap step before the documented setup works.                                                                         | A constraint governing every agent change belongs in applicable agent guidance; setup steps primarily for humans belong in contributor docs. |
| `temporary-context`       | A release freeze permits a workaround until a tracked cutover completes.                                                                                                    | A recurring, supported fallback may deserve conditional guidance after verification.                                                         |
| `already-covered`         | CONTRIBUTING and its linked testing guide already explain the discovered convention adequately.                                                                             | The instruction exists but is outdated or hard to discover in the applicable workflow: consider defect or placement.                         |
| `non-reusable`            | A single-ticket fixture ID or immediately visible function signature caused an incidental lookup.                                                                           | A non-obvious invariant with expensive rediscovery can be durable even after one occurrence.                                                 |

Use one primary category and mention secondary effects where needed. For example,
a duplicated rule with a stale copy may require consolidation and correction;
identify which source remains authoritative before proposing either.

## Instruction gap versus skill gap

An instruction gap is usually a compact rule changing behavior at an identifiable
scope. A skill gap describes a reusable procedure with meaningful sequencing,
branching, orchestration, or tool integration. Prefer an existing skill or
reference when it already owns that procedure. A new skill is a candidate for
separately authorized creation, not a reason to expand the current retrospective.
Detailed CLI syntax within a known procedure belongs in that skill's references.

## Reusable versus temporary

Persistence generally needs at least one demonstrated value: a repository
invariant, likely recurrence, expensive rediscovery, prevention of incorrect
implementation or failed validation, an explicit user correction, repeated
misunderstanding, or materially better routing/conditional loading. A single
costly discovery can qualify; repetition is evidence, not a required count.

Filter out ticket-specific facts, transient state, speculation, well-documented
knowledge, one-off external failures, and details apparent from code. Compare
future benefit with the ongoing context and maintenance cost. If no change would
have improved execution, retain the observation only in the retrospective.

A user correction is evidence to investigate, not automatic repository policy.
“For this response, use bullets” expresses a task/personal preference unless the
user establishes a durable contributor convention. Classify accordingly rather
than adding a universal formatting rule.

## Confidence

- **High:** direct session evidence and inspected authoritative sources establish
  the behavior, gap, and scope.
- **Medium:** evidence supports persistence, but some bounded uncertainty remains;
  identify it and verify anything affecting authority or destination before apply.
- **Low:** missing history, unavailable guidance, or an unverified assumption
  prevents a reliable recommendation. Mark for investigation; do not recommend a
  persistent change on that basis.

Candidates from another skill receive the same scrutiny. If inspection rejects
them, report the evidence and return control without modifying guidance.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
