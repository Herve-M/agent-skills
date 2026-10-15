---
name: git-conventions
description: Apply fallback Git conventions when creating or recommending branch names, creating, amending, or recommending commit messages, or classifying changes for Git.
---

# Git conventions

## Resolve conventions

Only when Git conventions are needed, check these repository-root files and read
only those that exist, in descending precedence:

1. `docs/agent/git.md`
2. `docs/engineering/git.md`
3. Defaults below.

Resolve each rule independently: higher-priority documents override conflicting
rules; unspecified rules fall through. Do not search for other Git documentation
unless existing repository instructions explicitly point elsewhere.

## Commits

Use [Angular's types and header conventions](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md#type),
without its project-specific scopes or mandatory body requirements.

- Header: `<type>(<scope>): <summary>`; omit `(<scope>)` unless unambiguous from
  repository structure or defined by repository documentation. Never invent
  repository-specific scopes. Local rules may require a scope.
- Summary: concise, imperative present tense, lowercase initial, no final period.
- Types: `build`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `test`, plus:
  - `chore`: maintenance that fits no other type.
  - `style`: formatting or stylistic changes without behavioral effects.
  - `ai`: changes to agent context or harness infrastructure, including
    `AGENTS.md`, instructions, skills, prompts, memory/context files, and agent
    configuration. Classify by purpose even when these files are Markdown.
- Body optional unless local rules require one.

## Branches

Use [Conventional Branch](https://conventionalbranch.org/): `<type>/<description>`.
Descriptions are concise, lowercase alphanumeric words separated by single
hyphens; release versions may contain dots. No leading, trailing, or consecutive
separators.

Use upstream purpose types `feature/` (`feat/`), `bugfix/` (`fix/`), `hotfix/`,
`release/`, and `chore/`, with these overrides:

- `docs/`: documentation-only work.
- `chore/`: other non-code maintenance, including dependency updates; never
  documentation-only work.

Upstream source prefixes `ai/`, `codex/`, `claude/`, `copilot/`, and `cursor/`
identify AI-generated branches and their source, independent of change purpose.
The `ai` commit type classifies agent-context/harness changes, not authorship;
neither determines the other's prefix/type.

## Override template

Only when asked to document repository deviations, load
[templates/git.md](templates/git.md) for `docs/agent/git.md` or
`docs/engineering/git.md`. Keep only deviations; empty tables add no rules.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
