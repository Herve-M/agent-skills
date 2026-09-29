# Attribution and generalization

## Reconstruct before interpreting

Use the exact executed revision, including its references and scripts. Record
commit plus content digest/local diff if uncommitted changes existed. A current
checkout is not evidence of past instructions. Capture records are finding aids;
check their claims against original session events and artifacts. A later agent
summary or claim that a skill was loaded is weaker than a recorded loading
event.

Build a four-column comparison: prescribed rule and locator; actual action and
locator; correction and locator; changed action and observed result. Include the
original task, applicable higher-priority instructions, tools available at the
time, interruptions, compaction and relevant project constraints. Mark absent
events, redactions and clipped outputs as evidence gaps. Enlarge only the window
needed to resolve them. Absence from an incomplete transcript is not proof an
action never occurred.

User dissatisfaction is evidence of an expectation, not proof of task failure.
Check the correction against task intent and observable correctness. A
successful recovery establishes sequence; attributing its success to the
correction still requires a plausible mechanism and consideration of other
changed conditions.

## Classify the cause

Choose a primary classification and contributing causes where supported.

| Classification                         | Evidence needed                                                                                   | Usual destination                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Missing instruction                    | A general prerequisite/invariant absent from the executed skill; its absence explains the failure | `SKILL.md` for shared decisions, otherwise reference                       |
| Ambiguous instruction                  | Two plausible readings with different outcomes; identify the ambiguous wording and failed reading | Clarify the existing rule or its pointer                                   |
| Adherence failure                      | The loaded rule already clearly prescribed the corrected behavior                                 | Eval/fixture; investigate salience or context before changing instructions |
| Missing knowledge                      | The procedure was adequate but necessary domain facts were missing/outdated                       | Reference or linked authoritative source                                   |
| Deterministic operation                | Repeated parsing, validation or transformation belongs in executable behavior                     | Script/tool, with a concise invocation pointer                             |
| Project convention                     | Requirement arises from this repository's conventions                                             | Project instructions such as `AGENTS.md` or `CLAUDE.md`                    |
| User preference                        | Correction expresses a personal presentation/workflow preference                                  | User preference storage if requested; no reusable skill patch              |
| One-off correction                     | Task-local detail or changed requirement without a reusable invariant                             | Nowhere/discard; retain private evidence if useful                         |
| Eval gap                               | Observable failure deserves coverage, including when the skill was adequate                       | Eval/fixture only; may accompany another cause                             |
| Insufficient evidence / external cause | Revision, trajectory or outcome missing; tool/environment failure better explains behavior        | Unresolved question or eval; defer skill attribution                       |

Answer: **Does this correction provide evidence that the reusable skill itself
is deficient?** Support yes/no/undetermined with the comparison, not the user's
certainty or the analyst's hindsight. Correct skill selection does not establish
instruction delivery or adherence.

For a clear existing rule, investigate whether it was loaded, truncated,
conflicted, buried behind a weak pointer or lost after compaction. Record what
could distinguish these hypotheses. A salience/pointer change is appropriate
only with evidence that delivery or discoverability caused the failure. Stronger
language and duplicate imperatives are not default fixes for noncompliance.

## Generalize and aggregate

Propose a rule that would help an agent facing a different task with the same
failure condition. Identify trigger, required behavior and boundary. Remove
names, exact paths, tool brands and answer details unless intrinsically
required. Prefer editing the existing decision point to appending another
instruction.

Ask what an agent could have known **before** the correction. Would the proposed
rule be useful without knowing the successful answer? Does it impose work on
unrelated cases? Could the correction itself be wrong or conflict with stronger
instructions? Look for contrary successful executions and failed recoveries.

Group sessions by skill revision, failure mechanism, operating conditions and
applicable constraints. List evidence IDs per group and distinguish independent
tasks from shared ancestors, duplicated exports, mirrored events or repeated
attempts. Count independent opportunities as well as failures when available;
do not invent a failure rate from correction-only samples. Keep contradictory
contexts separate rather than averaging incompatible requirements into a rule.

State strength with a rationale: independent recurrence; single clear invariant;
single suggestive observation; or incomplete/contradictory evidence. Confidence
in classification and confidence in patch effectiveness may differ. More cases
are useful, but not required for a directly demonstrated correctness defect.

Conclude each candidate with a completed retrospective. **Decision: no skill
change** is a desirable result when adherence, preferences, project context or
one-off requirements explain the correction. A rejected patch can still produce
a valuable eval. An undetermined result should name the missing discriminator.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
