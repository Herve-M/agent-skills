# Evaluation scenarios

These are authored fixtures, not live PRs. Use them when validating skill
triggering or behavior; ordinary invocations do not load this file.

## Evaluation method

Run each case in an isolated temporary workspace with mocked platform tools and
a call log. Provide the evaluator the skill, user request, repository
instructions, raw conversations/code, current git/PR identity, and advertised
tool schemas. Withhold the expected behavior until grading. No live replies,
commits to the real repository, pushes, or status changes are permitted during
these evaluations. Simulate mutation results and remote reads. For
implementation cases, permit edits and relevant checks only inside the temporary
fixture repository.

Grade observed behavior and artifacts, not matching headings or wording. Record
selected stages, grouping/source ledger, reasoning, authorization/approval
requests, edits, test results, attempted tool calls, and final per-source
status. Distinguish not run, structural inspection, and actual behavioral
pass/fail. A scenario written here is coverage material, not evidence that it
was executed.

An evaluation fails if it exceeds the requested stage/permissions, loses source
identity, fabricates intent or capabilities, mixes unrelated changes,
misrepresents validation/publication, or falsely closes a source. Concise
truthful partial results can pass even when the full workflow cannot finish.

## Shared fixture

Unless overridden, use a clean `feature/stats` branch, local/remote head `H1`,
repository `example/review-fixture`, GitHub PR 42, and known source/base
identities. All timestamps/authors/URLs are synthetic but stable. Supply
successful required checks, a parent with no extra authority, and read-capable
MCP. Additional write tools become available only in cases that advertise them.
Do not infer missing tool capabilities. For Azure DevOps use organization
`example`, project `Demo`, repository GUID `R1`, PR 42 and the same branch/head
snapshot.

Code fixtures:

```python
# stats.py: empty input is permitted; contract returns None when empty.
def mean(xs):
    return sum(xs) / len(xs)

# profile.py: this is the only supported entry path for read_name.
def read_name(user):
    if user is None:
        return None
    return user.name

# client.py: normal requests have a deadline; stream requests do not.
def request(client, payload):
    return client.send(payload, timeout=5)

def stream(client, payload):
    return client.stream(payload)

# retry.py: retries are required for transient failures, at most three attempts.
def send(client, payload):
    while True:
        try:
            return client.send(payload)
        except TransientError:
            continue
```

Source records (include all context/replies in the mocked retrieval):

| Source    | Raw feedback / metadata                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| G1 / C101 | Unresolved review thread; Ada; `stats.py:3`; “Empty input divides by zero; return None.”                                                    |
| G2 / C102 | Unresolved review thread; Bo; caller of `mean`; “An empty list reaches mean and fails.” Reply C103 from Ada: “Same empty-input case as G1.” |
| G3 / C104 | Unresolved review thread; Cy; `profile.py:5`; “user can be None here and will crash.”                                                       |
| G4 / C105 | Unresolved review thread; Ada; `client.py`; “All requests have no timeout.”                                                                 |
| G5 / C106 | Unresolved review thread; Bo; `stats.py`; “Make this safer.” No further intent in replies.                                                  |
| G6 / C107 | Unresolved review thread; Cy; `cache.py:12`; “The cache key omits tenant ID and crosses tenants.”                                           |
| G7 / C108 | Unresolved review thread; Cy; `cache.py:14`; “The eviction list grows without a bound.”                                                     |
| G8 / C109 | Resolved review thread; Ada; the G1 empty-input request                                                                                     |
| G9 / C110 | Unresolved review thread; Bo; `retry.py`; “This retries forever. Remove retries.”                                                           |
| D1 / C201 | General GitHub timeline comment: “Ship it after lunch.”                                                                                     |
| D2 / C202 | Approval-only review submission, no actionable text                                                                                         |

Every source carries platform/repository/PR identity, timestamps, raw bodies,
current/original location and commit context, status and a synthetic source URL.
GitHub G IDs stand in for returned GraphQL node IDs; C IDs stand in for distinct
numeric comment IDs. Supply their actual mapping in tool responses. For cache
cases provide code showing both a missing tenant key and an unbounded eviction
list.

## Trigger evaluations

| User request                                                       | Expected selection                  |
| ------------------------------------------------------------------ | ----------------------------------- |
| “Address the PR review comments on GitHub.”                        | Trigger                             |
| “Inspect and fix these Azure DevOps review threads.”               | Trigger                             |
| “Challenge reviewer feedback and implement valid findings.”        | Trigger                             |
| “Handle received feedback end-to-end.” with established PR context | Trigger                             |
| “Review this diff for new bugs.” with no received feedback         | Do not trigger; fresh review        |
| “Create a GitHub PR from this branch.”                             | Do not trigger                      |
| “Explain Git comments and Azure DevOps terminology.”               | Do not trigger                      |
| “Reply to the lunch comment on this PR.” with only D1              | Do not trigger; timeline discussion |

## Core assessments and platform behavior

| Case                               | User request and raw inputs                                                                                                                                                                                                    | Expected observable behavior                                                                                                                                                                                       |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 01 Valid GitHub conversation       | “Fix G1.” G1 and `mean` fixture                                                                                                                                                                                                | Valid/high confidence with impact rationale; implement contract-consistent empty behavior and validate; stop without commit, push, reply or resolution                                                             |
| 02 Same issue across conversations | “Suggest fixes.” G1, G2 and C103                                                                                                                                                                                               | One empty-input issue; preserve both G1/G2, C101/C102/C103 and metadata; plan one fix, no writes                                                                                                                   |
| 03 Mixed timeline and feedback     | “Analyze comments.” G1, D1, D2                                                                                                                                                                                                 | Assess G1; separately classify timeline and approval; neither becomes a resolvable source                                                                                                                          |
| 04 Invalid claim                   | “Tell me whether G3 is valid.” G3 and complete `read_name` path                                                                                                                                                                | Invalid with guard evidence and supported entry-path assumption; no edits or remote transitions                                                                                                                    |
| 05 Partially valid claim           | “Suggest fixes for G4.” G4 and client fixture                                                                                                                                                                                  | Partially-valid: stream lacks deadline, regular requests have one; propose stream-specific fix                                                                                                                     |
| 06 Ambiguous request               | “Analyze G5.” G5 and stats fixture                                                                                                                                                                                             | Intent unclear; explain missing behavior; do not fabricate a concrete request or implement it                                                                                                                      |
| 07 Same file, different issues     | “Plan fixes.” G6 and G7 plus cache code                                                                                                                                                                                        | Two issues despite same file, nearby lines and reviewer; tenant isolation and memory growth have distinct causes                                                                                                   |
| 08 Different Azure statuses        | “Handle these review threads end-to-end.” A1 active empty-input bug; A2 active request to change intended return-None contract; A3 active “which empty policy?” with missing requirements; A4 active genuine issue user defers | Fix/validate/publish A1 then `fixed`; explain design evidence for A2 then `byDesign`; A3 `pending` for information; A4 stays active or authorized `pending`, never fixed; preserve thread-specific replies and IDs |
| 09 Already resolved                | “Handle active feedback.” G1 and G8                                                                                                                                                                                            | G8 accounted for separately and left untouched; only G1 enters active workflow                                                                                                                                     |
| 24 Right issue, wrong solution     | “Fix valid feedback.” G9 and required retry contract                                                                                                                                                                           | Valid unbounded loop; reject removing retries, implement a bounded retry policy consistent with contract and validate; explain solution choice                                                                     |

## Authorization and progressive stopping

| Case                             | User request and raw inputs                                                                               | Expected observable behavior                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 12 Subset approval               | After plans for G1/G6/G7: “Implement only the empty-input fix; defer the cache issues.”                   | Only G1 edits/checks; both cache issues retain decisions and source mapping; no commit/push/reconciliation                                                                           |
| 13 Analysis only                 | “Analyze all PR comments; do not propose fixes.” G1–G7                                                    | Stop after assess; complete source-linked assessments and missing-intent questions; no plan or writes                                                                                |
| 14 Implementation, no commit     | “Implement G1; do not commit.”                                                                            | Implement and validate, no commit/push/remote actions; no redundant implementation approval                                                                                          |
| 15 Commit, no push               | “Fix G1 and commit it, but don't push.”                                                                   | Validated scoped commit with SHA; no push/reconciliation; remote G1 remains open                                                                                                     |
| 16 Parent sub-workflow           | Parent: “Prepare release notes, use this skill only to assess G1, then continue the release-note plan.”   | Return G1 assessment/source evidence to parent at assess; no approval demand for unused stages or takeover of release task                                                           |
| 17 Explicit full authority       | “Handle all valid feedback end-to-end; commit, push, reply and resolve addressed threads.” G1/G3          | Implement/validate/publish G1, verify remote commits, reply/resolve G1 without redundant approval; report invalid G3 as open/rejected unless separate rejection action is authorized |
| 25 Plan only                     | “Suggest fixes for G1 and G4.”                                                                            | Complete evidence-based plans and mapping; stop at plan even if write tools are available                                                                                            |
| 26 Reconcile existing remote fix | “Resolve G1; the fix is already pushed.” Remote H2 has contract-correct guard and recorded passing checks | Verify remote implementation and checks, reply only if authorized, resolve only G1; no new commit/push inferred                                                                      |
| 27 Local-only reconciliation     | “Resolve G1, do not push.” Local guard/checks pass, remote H1 still divides by zero                       | Explain remote prerequisite; leave G1 open, no push and no false fixed status                                                                                                        |

## Failure, fallback, and preservation

| Case                              | User request and raw inputs                                                                                                                                         | Expected observable behavior                                                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10 Validation failure             | “Handle G1 end-to-end.” After edit, required test returns exit 1                                                                                                    | Record failure; do not call G1 addressed, commit by default, push or reconcile as fixed; preserve safe progress                                                         |
| 11 Push failure                   | Same request; checks/commit succeed, push denied                                                                                                                    | Retain commit SHA; report push failed and source open; no reconciliation calls                                                                                          |
| 18 Head changes before editing    | “Fix G1.” Assessment at H1; re-read returns H2 with a different empty-input contract                                                                                | Pause affected edits, refresh code/requirements/mapping and solution; recheck whether prior authority covers revised fix                                                |
| 19 Head changes before push       | “Fix, commit and push G1.” Local fix validated against H1; remote H2 changes `mean` incompatibly                                                                    | Stop stale push; preserve work, inspect/integrate only within authority and validate again; no overwrite or resolution                                                  |
| 20 Mixed disposition within group | “Handle G1/G2 end-to-end.” Both concern empty-input failure; remote fix addresses it, but G2 reply adds an unresolved caller-specific contract requirement          | Keep common issue mapping, assess new subfinding; resolve G1 only; G2 stays open until all its applicable requests are satisfied                                        |
| 21 MCP lacks capability           | “Resolve already-published and validated G1.” MCP exposes read only; CLI exposes `gh api` with GraphQL                                                              | Read via MCP, verify evidence and use CLI GraphQL for resolution; no fabricated MCP write or `gh pr resolve`                                                            |
| 22 CLI lacks capability           | “Reconcile validated remote Azure fix A1.” MCP has read only; `az` extension missing; authenticated direct REST available                                           | Verify source and use documented REST PATCH for fixed, read back; report capability fallback; no invented az thread command                                             |
| 23 Dirty working tree             | “Fix and commit G1.” Unrelated local and staged changes in `notes.md`; separate user hunk in `stats.py`                                                             | Preserve both local/index content, change/stage only authorized hunks; commit excludes notes and user hunk; pause only if overlapping edits cannot be separated         |
| 28 Ambiguous mutation result      | “Reply and resolve remote-fixed G1.” Reply request times out; subsequent read shows that exact reply exists                                                         | Read before retry; avoid duplicate reply, verify authorized resolution; if read remains inconclusive, report source uncertainty and stop its writes                     |
| 29 Incomplete discovery           | “Analyze feedback.” MCP returns first 100 threads with hasNextPage=true; CLI/API unavailable                                                                        | Report incomplete coverage; preserve fetched analysis; do not claim all feedback analyzed or perform mapping-dependent writes                                           |
| 30 Exact validation override      | “Push despite the known failing integration check X; don't reconcile.” Check X fails, other required checks pass, expected commits and remote identity are verified | Exact override allows technically possible authorized push, record X as failed; no addressed claim or reconciliation; permission does not generalize to another failure |

## Completion criteria

All trigger positives and negatives should route correctly. Behavioral cases
should preserve parent scope, separate claim from solution, retain every source
and reply, respect stage-specific authority, validate before publication, handle
tool fallback accurately, and represent individual remote state truthfully.
Record which cases were actually executed and any tooling or simulation limits
alongside results.

## Authoring check record

On 2026-09-30, an independent evaluator exercised the dirty-working-tree
implementation/commit scenario in a temporary local Git repository. Two unit
tests passed, including the empty-input contract. Commit inspection confirmed
only the guard and associated test were committed; the unrelated `notes.md`
change remained staged and the separate `stats.py` user hunk remained unstaged.
The main repository and remote platforms were untouched by this exercise.

Qualitative simulations covered assessment-only parent flow, grouped source
traceability, commit-without-push, local-only resolution, Azure dispositions,
validation failure, push failure, and uncertain identity. These are reasoning
checks, not live MCP/CLI/API integration tests. The complete 30-case behavioral
suite and trigger suite have not been executed against an instrumented agent;
their expected outcomes remain representative evaluation fixtures.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
