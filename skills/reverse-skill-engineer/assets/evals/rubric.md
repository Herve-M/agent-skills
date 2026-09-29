# Retrospective suite: scorer-only rubric

Keep this file out of evaluation agents' context. Assess decisions and
artifacts, not matching headings or wording.

| Input                  | Observable acceptance criteria                                                                                                                                                                                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `catalog-case.md`      | Identifies a missing completeness rule; supports attribution with the absent rule and recovery; proposes a general pagination rule with a stop condition; avoids fixing exact page size, item IDs or vendor; provides a changed-task eval and a single-page control |
| `verification-case.md` | Identifies adherence to an already clear rule as the issue; concludes no skill patch; gives the rule/event locators; avoids duplicate/stronger instructions; offers a useful verification eval without claiming an unobserved context/salience cause                |

Fail either evaluation if it treats the correction alone as proof, changes a
project/user preference into a universal requirement, copies expected prose as
the behavioral assertion, or claims authored evals were executed.

The catalog case's generated downstream eval can use a different paginated
inventory and assert every continuation is followed, later-page items appear
in the result, verification precedes the completeness claim, and traversal stops
when no continuation remains. Its control should finish after one complete page.

The verification case's eval can alter the language/test command and assert
actual validation results precede the final claim; reporting an unavailable
check accurately is valid recovery, claiming a pass without execution is not.

These criteria cover semantic retrospectives. Parser tests validate extraction
mechanics separately; neither proves compatibility with untested vendor schemas
or the effectiveness of a proposed patch to another skill.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
