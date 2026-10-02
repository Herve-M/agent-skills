# Choosing the authoritative destination

Put knowledge at the narrowest durable scope where it remains discoverable and
authoritative. Inspect the repository's actual hierarchy and conventions; these
are generic decision criteria, not repository-specific policies.

## Destination framework

| Destination                      | Choose when                                                                                                             | Avoid / alternative                                                                                              |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Root `AGENTS.md` or equivalent   | Repository-wide invariants, universally applicable commands/constraints, and instruction-routing rules.                 | Subsystem-only details, procedural manuals, rationale, and reference catalogs; narrow the scope or link instead. |
| Nested `AGENTS.md` or equivalent | Module/technology conventions and subsystem validation should load only for work in that subtree.                       | Rules that actually apply repository-wide; promote to root with scoped references as needed.                     |
| Existing skill                   | A recurring multi-step procedure, branching workflow, orchestration, or platform/tool integration already has an owner. | A single operational rule; put it in scoped guidance.                                                            |
| New skill candidate              | The procedure is reusable and no existing skill owns it.                                                                | Ticket-specific sequences or duplication of existing workflows; creation needs authorization.                    |
| Skill `references/`              | Detailed CLI/API syntax, platform semantics, lookup tables, and lengthy examples used by a skill.                       | Core workflow invariants needed on every invocation; retain those in `SKILL.md`.                                 |
| README / developer docs          | Project usage, environment setup, commands for humans, or troubleshooting.                                              | Agent-wide constraints; route agents to the relevant documentation when needed.                                  |
| `CONTRIBUTING.md`                | Contributor expectations, contribution workflow, and human development checks.                                          | Architectural rationale or long tool manuals; reference their authoritative documents.                           |
| Testing documentation            | Detailed validation matrices, test prerequisites, and test workflow explanations.                                       | Essential scoped validation triggers that agents must see; keep a concise instruction pointing here.             |
| Architecture documentation       | Current architectural boundaries, constraints, system behavior, and rationale requiring context.                        | Operational recipes alone; use scoped guidance or skills.                                                        |
| ADR                              | A decision's rationale, alternatives, trade-offs, and historical context.                                               | A command correction or a minor convention with no architectural decision; amend the relevant existing document. |
| No persistent destination        | Temporary, obvious, already-covered, speculative, or non-reusable learning; context cost exceeds value.                 | Do not force placement just because a candidate was collected.                                                   |

## Decide scope from behavior

Ask who needs the knowledge and under what condition. The component where a
lesson was first discovered is evidence of scope, not proof of its boundary.
Check other components and applicable guidance before selecting root versus
nested placement.

If a rule applies only under one subtree, prefer the nested instruction file.
For relevant files spanning several subtrees, an authoritative shared document
with scoped pointers may work better than copies. Root routing can be concise
when it is necessary to discover that document.

Promote a nested rule only when evidence establishes repository-wide behavior.
Move an overly broad root rule down when it applies only locally. In both cases,
inspect callers and preserve intentional exceptions. Moving knowledge includes
updating its references and removing obsolete copies within authorized scope.

## Discovery versus missing knowledge

A rule adequately documented at the right scope is `already-covered`, even if
it is absent from root `AGENTS.md`. Before proposing a discovery fix, establish
an observed broken/missing route, misleading location, or recurring inability to
find applicable guidance despite following the available routes. Merely not
reading CONTRIBUTING or scoped instructions is an execution omission, not proof
that those documents need more pointers. For a demonstrated discovery defect,
propose a scoped pointer or corrected placement rather than copying the rule
into root context. State the routing evidence separately from the knowledge.

## Authority and overrides

Identify source A, source B, both applicable scopes, and evidence of precedence.
A root default and an explicit nested exception may agree under their own
conditions. Two incompatible requirements applying to the same work are an
actual conflict; neither filename recency nor agent guesswork determines
authority. Use repository hierarchy and documented decisions. If those do not
establish which source governs, report both options for user decision.

For semantically equivalent copies, designate one authoritative source and link
secondary locations to it. Keep intentionally different local rules explicit so
consolidation does not erase an override.

## Respect destination authorization

A request to update `AGENTS.md` authorizes suitable validated changes there, not
an arbitrary new skill or ADR. If the evidence belongs elsewhere, explain the
destination and propose its patch without editing it until authorized. A broader
request to update repository guidance can cover multiple appropriate files;
honor any parent/user restrictions and existing authorization without redundant
approval. Preserve unrelated local changes whichever destination is selected.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
