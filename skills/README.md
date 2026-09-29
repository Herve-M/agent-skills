# Authoring skills

Create each reusable skill in a lowercase kebab-case directory:

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── templates/
├── assets/
└── scripts/
```

Only `SKILL.md` is mandatory. The remaining directories are optional.

## `SKILL.md`

Include metadata/frontmatter required by the target Agent Skills format, the
skill's purpose, clear trigger or use conditions, its primary workflow,
essential constraints, and pointers to supporting material. Keep it focused on
the decisions and steps the agent needs on every invocation rather than turning
it into a large knowledge dump.

## `references/`

Store standards, extended guidance, decision tables, domain documentation, and
detailed examples that are needed only on relevant branches of the workflow.

## `templates/`

Store reusable output skeletons.

## `assets/`

Store non-executable resources consumed by the skill.

## `scripts/`

Store deterministic or reusable executable behavior. Scripts are licensed under
`MPL-2.0` unless a file explicitly states otherwise.

## Progressive disclosure

Prefer this loading path:

```text
SKILL.md
    ↓
references when needed
    ↓
scripts/templates/assets when needed
```

This keeps the primary workflow legible while making deeper material available
when it is relevant.

## Authoring references

Consult these sources when designing or reviewing a skill:

1. The [Agent Skills specification](https://agentskills.io/specification)
   defines the portable format requirements.
2. [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices)
   provide agent-neutral design guidance.
3. [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills)
   documents ChatGPT and Codex behavior.
4. [OpenAI's skill evaluation guide](https://developers.openai.com/blog/eval-skills)
   describes systematic, eval-driven iteration.

For contributions to this repository, follow its conventions where the sources
allow implementation choices. The
[Agent Skills documentation index](https://agentskills.io/llms.txt) provides
machine-readable links to further guidance.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
