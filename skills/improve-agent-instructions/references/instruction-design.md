# Designing durable instructions

Read when drafting or revising a proposed rule, resolving duplication, or
extracting a decision process. Examples are illustrative and must be adapted
only to behavior demonstrated in the session.

## Choose the knowledge form

| Form             | Appropriate content                                                                                                      | Writing approach                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Invariant        | Architectural boundaries, forbidden dependency directions, mandatory validation conditions, repository-wide constraints. | State the stable requirement concisely, without qualifications that depend on guessing. |
| Conditional rule | A requirement activated by identifiable files, components, or kinds of change.                                           | Write “When <condition>, <action/constraint>.” Keep it at the applicable scope.         |
| Procedure        | A reusable sequence with dependencies or branching decisions.                                                            | Prefer a skill when substantial; keep the agent instruction as a routing pointer.       |
| Reference        | Background, syntax, examples, tables, or rationale needed only sometimes.                                                | Link from the applicable instruction or skill with an explicit loading condition.       |

Separate an operational constraint from its rationale when their audiences or
loading needs differ. Keep the authoritative rule in one location; let linked
architecture documentation explain the decision.

## Write concise, operational rules

Specify a recognizable trigger and an observable action or constraint. Preserve
the actual requirement strength: distinguish mandatory validation from an
optional suggestion or a local convention.

- Vague: “Be careful when changing database code.”
- Operational: “When modifying files under `src/Persistence/`, run
  `dotnet test tests/Architecture.Tests` before considering the change validated.”

The second rule is appropriate only if the session and inspected guidance
establish that condition and command. Verify commands from repository evidence;
do not turn an illustrative command into policy.

Prefer narrow patches over whole-document rewrites. Keep enough context for the
rule to make sense when loaded independently. Avoid speculative interpretation,
restating obvious general knowledge, or specifying one implementation when
several satisfy the demonstrated constraint. Pin versions or tool behavior only
when the requirement depends on them and repository evidence supports the pin.

## Extract decision trees only when useful

Capture a recurring decision process if distinct branches change meaningful
actions and rediscovering those branches caused friction. For example, session
evidence might establish:

```text
Domain model changed?
  no  -> normal validation
  yes -> run architecture tests
         Cross-context dependency introduced?
           yes -> reject the design
           no  -> continue
```

A substantial tree belongs in the relevant skill or reference, with a concise
scoped pointer. Check that each branch is supported and its condition is
observable. Avoid documenting the agent's incidental trial-and-error path.

When there is only one meaningful condition, reduce the tree to a rule such as
“When changing the domain model, run the architecture tests.” Do not add a tree
whose branches merely repeat the same action.

## Control context cost

Keep frequently needed invariants close to their applicable scope. Disclose
lengthy details through pointers naming both the material and when to read it.
Move subsystem-only guidance out of root context when a nested file or scoped
reference remains discoverable. A shorter root file is not an improvement if it
hides a universal requirement or leaves a reference unreachable.

Avoid caches of easily discovered configuration, commands already obvious in a
single manifest, or facts apparent from code unless this session demonstrates a
material discovery problem. Document the non-obvious requirement or route to its
source instead of reproducing catalogs.

## Consolidate without erasing scope

1. Inspect every copy and its callers; identify the intended authoritative source.
2. Distinguish equivalent rules from intentionally different local overrides.
3. Propose one authoritative rule and scoped references; name removed copies.
4. Move/delete guidance only within authorized scope, updating references with it.
5. Verify that affected agents and contributors can still discover the rule.

For actual conflicts, record both sources, applicable scopes, why they disagree,
and the proposed authority. Resolve authority from repository structure and
session evidence; if it remains unknown, keep the issue for user decision.
Combining conflicting requirements into a longer rule does not resolve them.

## Check instruction quality

A future agent should be able to identify when the instruction applies, carry
out its action, and recognize completion or a constraint violation. Review
isolated wording, links, scope, duplication, and consistency. Use the applicable
repository documentation checks; a prose rule does not need a brittle wording
test. Evaluate behavior with realistic cases when changing the skill itself.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
