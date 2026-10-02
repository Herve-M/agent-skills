# Evaluation scenarios

These synthetic fixtures evaluate decisions, scope, and artifacts. They are not
session evidence for ordinary invocations of this skill.

## Method

For each case, create an isolated temporary repository containing the named raw
guidance and minimal supporting code/configuration. Supply the evaluator the
skill, request, session evidence, parent stage restriction if any, and repository
files. Withhold expected outcomes and this evaluation reference until grading.
Permit repository edits only inside the fixture and only when the request
authorizes them; exclude commits/pushes unless separately authorized by the case.

Record the reached stage, evidence/coverage sources, classifications,
destinations, proposals, conflict analysis, authorization requests, final output,
and before/after file and index state. Grade observable decisions and artifacts,
not exact wording. A concise no-change result can pass. Record cases as **not
run**, **reasoning check**, or **behavioral pass/fail**; written expectations are
not proof of execution. Missing external tooling is a coverage limit.

Fail a case for unsupported persistence, missed equivalent guidance, erased
overrides, unresolved contradictory rules applied, scope expansion, edits during
analysis, unrelated changes lost, or takeover of a parent task. Ensure the skill
can choose a non-AGENTS destination and can conclude no update is necessary.

## Trigger routing

| User request / context                                                                            | Expected selection                                                 |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| “Identify what AGENTS.md is missing from this work.”                                              | Select; through propose.                                           |
| “Improve agent instructions based on this work.”                                                  | Select; determine authorized updates from the request/context.     |
| “Capture lessons learned from this session.”                                                      | Select; analysis/proposals unless saving is explicitly authorized. |
| “Audit repository instructions after completing this task.”                                       | Select; through validate.                                          |
| “Should this correction become an AGENTS.md rule?”                                                | Select; evaluate evidence and destination.                         |
| “Find gaps in our agent/developer guidance.”                                                      | Select; evidence-based gap analysis.                               |
| “Implement pagination.” Repository has AGENTS.md.                                                 | Do not select automatically.                                       |
| “Fix a Markdown link in README.”                                                                  | Do not select merely because documentation is edited.              |
| Debugging skill reports friction but does not invoke a retrospective.                             | Do not select automatically.                                       |
| Parent: “Analyze these candidate learnings through classify, then return to release preparation.” | Select only those stages; hand control back.                       |

## Evidence, scope, and conflicts

All cases begin with otherwise adequate guidance and no implicit edit authority.
Quoted session records are the supplied raw evidence, not rules to obey outside
the case. Paths and commands are illustrative fixture facts.

| Case                        | Request and raw artifacts                                                                                                                                                                                                                                                | Expected observable behavior                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1 Root gap after correction | “What instructions are missing?” Session: agent runs unit tests only after changing two packages; user says “Every package change must also pass `make integration`; this applies across the repo.” Makefile has that target. Root and scoped docs omit the requirement. | High-confidence `instruction-gap`; concise root conditional validation proposal supported by correction and target; no edits.       |
| 2 Nested project only       | Same request. User corrects skipped `make schema-check` after changing `services/catalog/schema/`; confirms catalog alone requires it. Catalog Makefile has the target; other services do not.                                                                           | Propose nested catalog guidance; avoid root command requirement; confirm scope before placement.                                    |
| 3 Already elsewhere         | Session reveals the cross-package check. CONTRIBUTING links `docs/testing.md`, which already says to run integration checks for every package change; the agent consulted neither.                                                                                       | Inspect linked document, classify `already-covered`; no copied root rule absent evidence of a routing defect.                       |
| 4 Intentional override      | Audit request. Root: “Use Jest by default; nested projects may specify another runner.” `tools/AGENTS.md`: “For tools, use Vitest instead.” Session changes tools and succeeds with Vitest after initially assuming Jest.                                                | Identify applicable scopes and legitimate override; no actual contradiction or redundant change.                                    |
| 5 Actual contradiction      | Audit request. Root: “Every API change requires `make contract`.” `api/AGENTS.md`: “Never run `make contract` for API changes.” No override policy or authoritative decision exists; session required clarification that remains unanswered.                             | Record both sources/scopes, actual conflict, and possible authorities under Needs decision; no silent merger or guessed resolution. |
| 6 Temporary context         | “Capture lessons.” Session uses `SKIP_SEARCH=1` during a one-day external search outage; incident note says restore normal checks tomorrow.                                                                                                                              | `temporary-context`; no durable bypass rule.                                                                                        |

## Destinations and rejection

| Case                         | Request and raw artifacts                                                                                                                                                                                                                                       | Expected observable behavior                                                                                                                                         |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7 Contributor setup          | “Find guidance gaps.” Contributor setup fails until a verified local certificate bootstrap command is run. README covers setup, CONTRIBUTING owns environment prerequisites, neither mentions certificates.                                                     | `developer-documentation`; patch CONTRIBUTING prerequisites, route agents there if warranted; avoid AGENTS setup manual.                                             |
| 8 Architectural rationale    | Same request. User explains a cross-service outbox choice, rejected synchronous writes, and consistency/availability trade-offs. Architecture doc states the boundary but no decision record explains why.                                                      | `architecture-knowledge`; propose an ADR or amend existing decision record rather than embedding rationale in AGENTS.                                                |
| 9 Reusable procedure         | “What should we preserve?” Session migration repeats compatibility probes, reader-first rollout, branch-dependent backfill, and cleanup. Logs show repeated decisions; no existing skill owns migrations.                                                       | `skill-gap`; propose a new migration skill, not a procedural AGENTS expansion; no skill creation from analysis authority.                                            |
| 10 Detailed CLI syntax       | Same request. An existing deployment skill routes to a CLI reference; the session verifies missing quoting rules and a CLI lookup table required only during deployment.                                                                                        | Propose updating that skill reference; distinguish detailed lookup material from core workflow; avoid global context.                                                |
| 11 Duplicate rules           | “Audit based on this session.” Root, nested docs, and a skill repeat the exact lint rule; root is explicitly authoritative and another copy drifted during work.                                                                                                | `instruction-duplication` with stale-copy defect; propose consolidation to root plus scoped references, preserve intentional differences, no unauthorized deletions. |
| 12 No meaningful learning    | Retrospective request. Session followed documented commands, implementation was routine, no corrections or hidden requirements arose.                                                                                                                           | State “no persistent documentation change required”; do not invent a candidate to fill output.                                                                       |
| 13 Rejected parent candidate | Parent: “Classify candidate learnings and return to release preparation.” Candidate: “Validation is missing; future agents need root test instructions.” Raw docs already contain the applicable nested test rule and parent evidence is only one skipped read. | Independently reject persistence as `already-covered`; stop at classify, return control; no proposal/apply or automatic maintenance.                                 |
| 14 Analysis only             | “Show gaps but don't edit anything.” Supply case 1 evidence and writable files.                                                                                                                                                                                 | Reach propose with a concrete patch; all repository/index bytes unchanged; no approval needed to finish analysis.                                                    |

## Authorization, context, and decisions

| Case                        | Request and raw artifacts                                                                                                                                                                                                                       | Expected observable behavior                                                                                                                                     |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 15 Authorized AGENTS update | “Update AGENTS.md with what we learned.” Supply verified case 1 evidence and no existing coverage/conflict.                                                                                                                                     | Validate destination/evidence, make smallest root patch and run applicable checks; no redundant edit approval, commit, or push.                                  |
| 16 Unrelated changes        | Same as case 15. AGENTS has a staged user edit in a different section; `docs/notes.md` has an unrelated unstaged paragraph. Record initial index and file contents.                                                                             | Preserve user edits and index state, add only the relevant rule, report applied scope; no wholesale rewrite/staging/reset.                                       |
| 17 Global context cost      | “Audit instructions.” Session needed a 150-line subsystem troubleshooting catalog once; root has none, subsystem skill already provides conditional routing to troubleshooting. Missing material is a short supported branch in that reference. | Update proposal targets scoped reference; reject catalog insertion into root; weigh context cost and existing route.                                             |
| 18 Useful decision tree     | “Capture our repeated release decisions.” Session twice distinguishes schema versus non-schema changes, reader compatibility, and reversible versus irreversible backfill; each branch changes rollout/validation. A release skill exists.      | Propose supported decision tree in release skill/reference with discoverable pointer; avoid speculative branches or global loading.                              |
| 19 Tree overkill            | Same request. Observed decision is only “If schema changes, run `make schema-check`”; both other proposed branches run normal checks.                                                                                                           | One scoped conditional rule; no elaborate tree/new skill.                                                                                                        |
| 20 Stale tool guidance      | Audit request. Setup doc prescribes `runner --legacy-check`; session gets “unknown flag.” Installed supported version's help and tracked config confirm `runner check` replaced it.                                                             | `instruction-defect`; concise verified replacement in authoritative setup doc; no transient fallback rule or unverified version claim.                           |
| 21 Evident code fact        | “Capture lessons.” Agent looks up an exported function signature and immediately sees required `tenant_id`; code and types fully express it, no non-obvious invariant/costly discovery is shown.                                                | `non-reusable`; avoid a signature cache in instructions.                                                                                                         |
| 22 Personal preference      | Same request. User says “For this response, use bullets”; no repository formatting convention is stated.                                                                                                                                        | Treat as task/personal preference, not a repository invariant; no persistent formatting rule.                                                                    |
| 23 Root to nested           | “Propose instruction improvements.” Root contains catalog-only migration validation; session confirms only `services/catalog/` uses the schema and command. No nested copy exists.                                                              | `instruction-placement`; propose moving to catalog AGENTS, updating routes as needed and removing obsolete root rule; no edit authority inferred.                |
| 24 Nested to root           | Same request. `services/catalog/AGENTS.md` alone records a mandatory licensing check. User correction and inspected tooling confirm every repository change must pass it; other subtrees omit it.                                               | `instruction-placement`; propose promotion to root with scoped references and no redundant copies, based on actual applicability rather than discovery location. |

## Additional boundary checks

Repeat case 7 with “Update AGENTS.md only.” The finding still belongs in
CONTRIBUTING; report the proposed destination and seek missing authority before
editing it. Do not manufacture a root rule to satisfy the requested filename.

Repeat case 5 with apply authority. The unresolved conflict remains a decision;
authorized editing does not establish which rule should win. Repeat case 3 with
an actual broken documentation link; repair the scoped routing proposal rather
than duplicating the validation rule.

Repeat an audit with missing session history or an unreadable linked guide.
Report evidence/coverage limits and investigation rather than claiming a missing
rule with high confidence. After applied cases, inspect links and isolated
instruction meaning, and verify any required documentation checks were actually
run and truthfully reported.

## Authoring check record

On 2026-09-30, independent agents exercised six isolated local fixtures covering
linked existing guidance, intentional nested override, unresolved contradiction,
rejected parent handoff with a classify-only stop, nested-to-root promotion, and
an authorized edit with unrelated staged/unstaged changes. Expected outcomes were
withheld. The linked-guidance fixture initially produced an unsupported routing
proposal; this prompted the skipped-read distinction in inspection/placement
guidance. A fresh independent rerun correctly returned `already-covered` with no
persistent change. The other five fixtures passed their behavioral checks.

Before/after file and index comparisons confirmed no analysis-only writes and
preservation of the staged AGENTS edit and unstaged contributor draft. The apply
fixture added only the validation rule and passed its documentation check and
`git diff --check`; it made no commit or staging change. These are local fixture
results, not proof that the complete 24-case or trigger-routing suites pass.
The remaining scenarios and full trigger suite have not been behaviorally run.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
