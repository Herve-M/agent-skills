# Agent Skills

This repository is the canonical source for reusable skills for compatible AI
coding and agent environments. Skills should remain agent- and harness-neutral
where practical so one implementation can serve Codex, Claude Code, and other
Agent Skills-compatible tools.

Machine-specific configuration, global agent settings, and installation or
dotfiles bootstrap logic belong in their respective configuration repositories.

## Principles

- Maintain one canonical implementation of each skill.
- Keep skills harness-neutral where practical.
- Use progressive disclosure: keep `SKILL.md` small and move detail into
  `references/`.
- Put deterministic, reusable behavior in `scripts/` instead of lengthy
  procedural prompts.
- Use `templates/` and `assets/` only when the skill needs them.
- Apply separate licenses to expressive content and executable source code.
- Record third-party provenance and preserve upstream notices explicitly.

## Skill structure

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── templates/
├── assets/
└── scripts/
```

Only `SKILL.md` is required. Add the other directories when they improve the
skill's organization or behavior. Agents should follow [AGENTS.md](AGENTS.md);
the detailed authoring reference is [skills/README.md](skills/README.md).

## Licensing

| Material                                                 | License                   |
| -------------------------------------------------------- | ------------------------- |
| Skill instructions, references, templates, documentation | CC BY-NC-SA 4.0           |
| Scripts, executable helpers, tooling                     | MPL 2.0                   |
| Third-party material                                     | Original upstream license |

The complete policy is in [LICENSE.md](LICENSE.md). Copied, adapted, vendored,
or materially incorporated third-party material must also be recorded in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Development

Install [mise](https://mise.jdx.dev/), then run:

```bash
mise run validate
mise run check-licenses
mise run lint-markdown
mise run check-markdown-format
mise run format-markdown
mise run list-skills
```

`validate` checks repository structure, licensing conventions, and Markdown.
Use `lint-markdown` to run the Markdown linter directly,
`check-markdown-format` to verify formatting without changing files, and
`format-markdown` to apply formatting. `check-licenses` runs the licensing
checks directly. `list-skills` prints the names of immediate skill directories
and succeeds without output while the repository contains no skills.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
