# Evidence bundle: catalog inventory

Analyze this synthetic session. The user requested an analysis with a proposed
patch and eval if justified. No external service or original skill file exists
to mutate; use this embedded revision as the artifact under examination.

## Skill artifact

Skill: `catalog-audit`; path: `skills/catalog-audit/SKILL.md`. Revision:
synthetic `catalog-r1`; this is the complete workflow at that revision.

```text
Purpose: inventory every published item and report inconsistent labels.
1. Query the catalog listing API for published items.
2. Inspect returned items for inconsistent labels.
3. Report findings and the total number of published items inspected.
```

No references or scripts exist. Project instructions impose no special listing
convention. The available API accepts a continuation token and returns `items`
plus `next_cursor`; an absent/null cursor marks the final page.

## Session trajectory

Session ID: synthetic `catalog-session-1`; agent: unspecified; task: inventory
all published posters and report inconsistent labels. The skill was appropriate.

- E01: The agent reads the complete `catalog-r1` artifact above.
- E02: Tool call `catalog.list(kind=poster, published=true)` returns two items
  and `next_cursor=p2`.
- E03: Agent reports no inconsistent labels and a total inventory of two
  posters.
- E04: User: “There is another page. Follow the continuation before calling the
  inventory complete.”
- E05: Tool call `catalog.list(kind=poster, published=true, cursor=p2)` returns
  two more items, one with an inconsistent label, and `next_cursor=null`.
- E06: Agent checks all four items, reports the inconsistent label and four-item
  inventory; the user confirms this matches the catalog's published count.

No interruption, tool failure or context truncation is recorded. No independent
sessions have been supplied.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
