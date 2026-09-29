# Assessment and traceability

## Normalize without losing evidence

Use stable issue IDs and retain raw platform records, or lossless references to
accessible records in the parent workflow. Keep an in-memory ledger unless the
parent requests an artifact; do not add internal tracking files to the PR by
default.

| Record              | Required content when available                                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Snapshot            | Platform/host, repository ID and remote identity, PR ID/URL, source/base branches and SHAs, retrieval time and coverage limits                                        |
| Source conversation | Composite platform/repository/PR/thread identity; status; path/current and original range; diff side, commit/iteration context; URL; all retrievable comments/replies |
| Source comment      | Comment ID and parent/reply linkage, author identity, timestamps, original body, location/context and URL; deleted/missing metadata explicitly recorded               |
| Normalized issue    | Stable issue ID, source identities, summary, evidenced intent, assessment and evidence, confidence, risk, affected components, implementation needed                  |
| Execution           | Proposed solution, user decision/authority, changed files/hunks, validation commands/results and tested SHA, commit SHAs, push verification                           |
| Reconciliation      | Per-source disposition, supporting evidence, authorized action, attempted reply/status change, verified remote result or uncertainty                                  |

Unavailable metadata is unknown, never invented. Preserve original and current
locations; outdated coordinates do not prove an issue disappeared. A platform
event and its underlying comment are one source, not two findings. Deduplicate
by source identity while retaining distinct replies and changed context. A
comment ID alone may be unique only within its thread; use composite identities.

The primary unit is the conversation. If it contains several distinct requests,
record them as subfindings and require all applicable requests to be accounted
for before a terminal action. Assign each source to one normalized issue,
retaining distinct requests as source-specific subfindings rather than
duplicating its identity across issues. Reconciliation requires every applicable
subfinding to be accounted for.

## Separate four concepts

- **Observation:** What the reviewer saw, such as a missing deadline argument.
- **Interpretation:** What they infer, such as a request that could wait
  indefinitely.
- **Underlying issue:** The codebase-supported failure or requirement gap.
- **Proposed solution:** Their suggested mechanism, such as retrying without a
  bound.

Validate the observation and inference against the inspected revision and
repository requirements. A true claim can have a harmful proposed solution.
Assess and plan independently; quote only enough source text to establish
intent, and label inference. Look for evidence that could falsify the claim,
including earlier guards, callers, tests and contracts. Lack of a reproducer is
not proof of invalidity. Ask for missing intent only after useful inspection; do
not turn personal preference into a requirement.

## Grouping

Group conversations only with positive evidence of the same cause and corrective
behavior, for example two reports of the same unbounded retry loop in two
callers. Retain both source records and explain the grouping. Similar symptoms
with different causes, nearby lines, the same file/class/reviewer, or similar
wording do not suffice. If unsure, keep separate issues. Reassess grouping when
replies or code reveal a different requirement. Grouping reduces duplicated
analysis, never remote actions.

## Assessment and confidence

| Assessment        | Meaning                                                                                                        |
| ----------------- | -------------------------------------------------------------------------------------------------------------- |
| `valid`           | Evidence supports the underlying claim in relevant code and requirements                                       |
| `partially-valid` | A real concern exists, but its extent, condition, or requested behavior is overstated or only partly supported |
| `invalid`         | Evidence contradicts the underlying claim; cite the guard, behavior, or contract                               |
| `unclear`         | Intent or required behavior cannot be established confidently; name the missing information                    |
| `out-of-scope`    | The concern lies outside the authorized task; preserve its technical merits separately                         |

Confidence describes the evidence, independently of validity and impact:

- `high`: Direct reproduction, test, contract, or decisive code-path evidence.
- `medium`: Strong inspection evidence with an explicit unverified assumption.
- `low`: Missing context, ambiguous intent, or unresolved competing
  explanations.

An invalid claim can have high confidence. An unclear requirement can concern a
critical risk. Implementation necessity is a separate field: valid feedback may
already be satisfied in the current remote revision.

## Risk rubric

| Score | Underlying impact                                                                 |
| ----- | --------------------------------------------------------------------------------- |
| 1–2   | Cosmetic or negligible                                                            |
| 3–4   | Low impact                                                                        |
| 5–6   | Meaningful correctness or maintainability impact                                  |
| 7–8   | Significant functional, compatibility, performance, reliability, or security risk |
| 9–10  | Critical correctness, data-loss, security, or production risk                     |

Explain the score using affected users/paths, likelihood and severity. Reviewer
seniority, tone, wording, and comment count do not influence risk. For invalid
claims, distinguish alleged impact from the actual supported issue (possibly
none). Still report an integer from 1 to 10 for unclear feedback; label it
provisional and state the impact assumptions rather than presenting uncertainty
as measured risk.

## Examples

| Feedback and code evidence                                                                        | Assessment / action                                                                 |
| ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| “Empty input divides by zero.” `sum(xs) / len(xs)` has no guard and empty input is allowed        | Valid, high confidence; reproduce and define empty-input behavior from the contract |
| “All requests hang.” Only the streaming path lacks a deadline; ordinary requests have one         | Partially-valid; fix the affected path and report the narrower impact               |
| “This dereferences null.” Every reachable caller checks null before entering the block            | Invalid with high confidence if those callers exhaust the supported entry paths     |
| “Make this safer.” No failure case, desired behavior, or contract can be established              | Unclear; record inspection and request the missing intent                           |
| Threads T1 and T2 each identify the same shared cache key omitting tenant ID                      | One issue with T1 and T2 retained independently                                     |
| Two nearby comments in `cache.py`: missing tenant key and unbounded eviction growth               | Separate issues: isolation and memory retention have different causes/fixes         |
| “This retry loop never terminates; remove retries.” A transient-failure contract requires retries | Valid underlying issue; reject removing retries and propose a bounded policy        |

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
