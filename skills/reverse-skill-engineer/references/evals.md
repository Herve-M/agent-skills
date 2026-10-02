# Regression evals

## From failure mechanism to behavior

For each accepted behavioral patch, attempt an eval **before** applying it.
Specify: failure condition, different task/input, fixtures, available tools,
observable assertions, applicability boundary, and baseline/patched skill
revisions. Keep original answer details out of fixtures. An eval for an
adherence failure should test compliance with the existing skill, even without a
patch.

Prefer assertions on inspected prerequisites, call/result ordering, tool choice,
unnecessary calls, verification, recovery and final artifacts. Exact answer
prose rarely establishes the desired behavior. State tolerances and permitted
alternate tools; avoid requiring one trajectory when multiple correct paths
exist.

Use a control when the rule has a nontrivial activation boundary: the
prerequisite is already satisfied, a similar-looking task falls outside the
rule, or the rule would cause unnecessary operations. A useful rule helps the
failure case without regressing that control. A control is different from
evidence of an independent recurrence.

Run isolated baseline and patched trials with equivalent task/tool conditions
and record outcomes separately. Stochastic agents may require repetitions;
report observed counts rather than claiming certainty from a single pass.
Supply evaluation agents only the skill, task and minimum raw artifacts. Keep
diagnoses, expected decisions and grader rubrics outside their context. Follow
the environment's delegation/side-effect authorization; if execution is
unavailable, deliver an authored case and report the execution gap.

If baseline succeeds, the eval has not reproduced the observed regression in
that trial. If patched behavior fails, inspect the trajectory before adding
more prose. Run existing compatible evals to check collateral effects. Record
blocked evaluations with their missing tool, fixture or evidence dependency.

## Initial retrospective eval suite

The two synthetic inputs under `assets/evals/` test this skill's attribution
behavior. They are not copies of private sessions. Each embeds an affected skill
revision and a small trajectory, so no real vendor history is needed.

Give a fresh evaluator this request and **one input only**:

```text
Use reverse-skill-engineer in Analyze mode on the supplied evidence.
Produce a retrospective and any justified minimal patch and behavioral eval.
Keep original evidence unchanged; write artifacts only in the evaluation folder.
```

Score completed outputs using [the separate rubric](../assets/evals/rubric.md).
That file is for the scorer only. Stage an evaluation copy without the rubric
and supply one evidence input; do not expose other test cases or expected
decisions to the evaluator.

## Design critique before accepting a change

Apply these checks to proposed patches, including edits to this skill:

- **Overfitting:** Change task names, data, environment and wording. Does the
  rule still explain the failure? Are its boundary and control meaningful?
- **Duplication/bloat:** Can an existing rule/pointer be clarified? Does each
  new resource earn its loading/maintenance cost?
- **Hindsight:** Could the agent have applied the rule before seeing the answer?
- **Contamination:** Is fresh analysis using original artifacts, rather than
  carrying forward the live agent's rationale as fact?
- **Format brittleness:** Are unstable storage assumptions behind verified
  adapters? Are unknowns and version gaps visible?
- **Context cost:** Do deterministic filtering and explicit budgets keep the
  semantic diagnosis window small without hiding causal prerequisites?
- **Secret exposure:** Are originals untouched, private artifacts kept out of
  version control, and omitted/redacted evidence reviewed before disclosure?

Run `python3 scripts/test_history.py` to test extraction mechanics. Those tests
do not validate semantic attribution or vendor compatibility beyond the tested
shapes. Run the independent retrospective suite separately for that coverage.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
