# Agent Skills

This repository is the canonical source for reusable skills for compatible AI coding and agent environments. Skills should remain agent- and harness-neutral where practical so one implementation can serve Codex, Claude Code, and other Agent Skills-compatible tools.

Machine-specific configuration, global agent settings, and installation or dotfiles bootstrap logic belong in their respective configuration repositories.

## Install and update

Use [GitHub CLI](https://cli.github.com/) with the [`gh skill` commands](https://github.com/cli/cli/blob/trunk/skills/gh-skill/SKILL.md). Replace `<agent-id>` with your agent's identifier and `git-conventions` with any skill listed below:

```bash
gh skill preview Herve-M/agent-skills git-conventions
gh skill install Herve-M/agent-skills git-conventions --agent <agent-id> --scope user
gh skill update git-conventions
```

`--scope user` makes the skill available across projects; use `--scope project` to install in the current Git repository. Set `--agent` explicitly to select the target environment. Run `gh skill update --all` to refresh all installed skills.

## Skills table of contents

| Skill                                                                     | TLDR: when to use                                                                                                                                           |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [git-conventions](skills/git-conventions/SKILL.md)                        | Apply default commit and branch conventions when repository Git documentation does not override them.                                                       |
| [grove](skills/grove/SKILL.md)                                            | Create, locate, use, and clean up Grove worktrees for Codex and Claude Code sessions.                                                                       |
| [improve-agent-instructions](skills/improve-agent-instructions/readme.md) | After repository work, audit lessons and propose or apply durable improvements to agent and developer guidance.                                             |
| [resolve-review-feedback](skills/resolve-review-feedback/readme.md)       | Assess and address received pull-request review comments on GitHub or Azure DevOps, then validate fixes and reconcile threads within the requested scope.   |
| [reverse-prompt-engineer](skills/reverse-prompt-engineer/readme.md)       | Turn a conversation's final intended task, corrections, and accepted decisions into one reusable, self-contained initial prompt.                            |
| [reverse-skill-engineer](skills/reverse-skill-engineer/readme.md)         | Capture corrections during skill execution or analyze session evidence to decide whether an existing skill needs a minimal improvement and regression eval. |

## Principles

- Maintain one canonical implementation of each skill.
- Keep skills harness-neutral where practical.
- Use progressive disclosure: keep `SKILL.md` small and move detail into `references/`.
- Put deterministic, reusable behavior in `scripts/` instead of lengthy procedural prompts.
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

Only `SKILL.md` is required. Add the other directories when they improve the skill's organization or behavior. Agents should follow [AGENTS.md](AGENTS.md); the detailed authoring reference is [skills/README.md](skills/README.md).

## Licensing

| Material                                                 | License                   |
| -------------------------------------------------------- | ------------------------- |
| Skill instructions, references, templates, documentation | CC BY-NC-SA 4.0           |
| Scripts, executable helpers, tooling                     | MPL 2.0                   |
| Third-party material                                     | Original upstream license |

The complete policy is in [LICENSE.md](LICENSE.md). Copied, adapted, vendored, or materially incorporated third-party material must also be recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Development

Install [mise](https://mise.jdx.dev/), then run:

```bash
mise install
mise run install-hooks
```

The installed pre-commit hook removes trailing whitespace, checks Markdown with rumdl, and then formats Markdown with rumdl. If a commit changes files, review and stage the changes before committing again. Run the hooks manually against the whole repository with:

```bash
mise run check-hooks
```

The remaining repository checks and maintenance tasks are:

```bash
mise run validate
mise run check-licenses
mise run lint-markdown
mise run check-markdown-format
mise run format-markdown
mise run list-skills
mise run test-validator
```

`validate` checks repository structure, licensing conventions, and Markdown. Use `lint-markdown` to run the Markdown linter directly, `check-markdown-format` to verify formatting without changing files, and `format-markdown` to apply formatting. `check-licenses` runs the licensing checks directly. `list-skills` validates and prints the names of immediate skill directories, and succeeds without output while the repository contains no skills. `test-validator` runs the validator's regression tests.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
