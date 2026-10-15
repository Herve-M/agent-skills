---
name: grove
description: >-
  Manage Git worktrees with Grove CLI for Codex and Claude Code sessions, integrating Herdr workspaces when running inside Herdr. Use when creating or locating an isolated branch or PR checkout, working in another worktree, or cleaning up session worktrees. Applies to worktree management with Grove, not ordinary Git edits or general agent orchestration.
license: CC-BY-NC-SA-4.0
user-invocable: false
---

# Grove

Use Grove to prepare and manage worktrees while keeping each coding session attached to the intended checkout. Prefer Grove for worktree lifecycle operations so its configuration, preservation, hooks, and locks apply; ordinary Git inspection and development commands remain appropriate inside a worktree.

This skill is intended for automatic use during worktree tasks. In [Claude Code](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill), `user-invocable: false` disables direct user invocation while preserving model invocation. [Codex](https://developers.openai.com/codex/skills/) does not document an equivalent control; this field does not guarantee that Codex hides or blocks direct invocation.

## Inspect before acting

1. Check `grove --version` and the relevant `grove <command> --help`. Installed builds can differ from current upstream documentation; use only supported flags.
2. Establish the repository and current directory, then run `grove list --json` from the workspace or one of its worktrees. Use `--fast` when only names, branches, and paths are needed. Keep stderr separate from JSON stdout.
3. Select an existing worktree by its returned name, branch, and absolute path. Do not derive the path from a branch name: Grove can normalize names and users can override them. Do not create a checkout just to inspect an existing one.
4. Detect Herdr with `test "${HERDR_ENV:-}" = 1 && command -v herdr >/dev/null 2>&1`. When both checks pass, apply [Herdr integration](#herdr-integration) to supported lifecycle commands by default.

Grove workspaces normally contain a `.bare/` Git repository and sibling worktree directories. The workspace root itself is not a checkout: `grove status --json` needs a worktree directory. If Grove cannot discover the workspace, locate the intended repository first. Read [workspace setup and cleanup](references/lifecycle.md) before initializing, converting, repairing, renaming, or removing anything.

Honor restrictions on repository mutation. `add` may fetch and update branches, and even `prune` without `--commit` fetches and prunes remote refs. Use help and inspection commands when mutation is prohibited.

## Prepare a session checkout

Reuse an existing worktree when it belongs to this task and session. For concurrent independent tasks, choose separate worktrees and branches; a clean checkout can still be in use by another session. Do not switch branches underneath another agent.

Before creation, inspect effective configuration with `grove config list` and the applicable `.grove.toml`. Check preserved files/directories, symlink patterns, and add hooks. Configuration may come from another worktree, not just the current directory. Preserve project instructions and local settings deliberately; avoid sharing writable agent state or dependency directories across independent sessions without understanding the effect.

Choose the branch and base from the task and repository conventions. Omit `--base` only when Grove's default base is appropriate; it is not implicitly the current branch. An existing branch is reused rather than recreated from a supplied base.

| Intended checkout                                   | Example command                                   |
| --------------------------------------------------- | ------------------------------------------------- |
| New branch from a chosen base                       | `grove add feat/session-task --base main`         |
| Existing branch without a worktree                  | `grove add fix/existing`                          |
| Custom directory name                               | `grove add feat/session-task --name session-task` |
| Pull request                                        | `grove add --pr 123`                              |
| Detached tag or ref                                 | `grove add --detach v1.2.3`                       |
| Configured preserved files from a specific worktree | `grove add feat/session-task --from main`         |

These examples describe actions to take only within the user's authorized task. Branch creation normally fetches its base; adding an existing branch can fetch its upstream and fast-forward it. Use `--no-fetch` for branch operations when local refs are explicitly intended, and report any fallback to stale refs. PR operations require GitHub access and `gh`; do not assume `--no-fetch` makes them offline.

When the Herdr check passes, append `--herdr` to these `add` examples unless the user requests creation without switching or changing focus.

`--from` selects the source for configured file preservation and linking. It does not transfer the source worktree's staged or unstaged diff. Moving unfinished code requires a separately scoped transfer that preserves the original work.

After `add`, rediscover the actual path with `grove list --json` and verify the branch and setup result there. A hook failure can leave a created worktree behind: inspect it before retrying, then rerun only the necessary setup in that checkout. Do not recreate it or refresh a PR as a generic retry. If hooks must be skipped, check whether the installed `add` supports `--no-hooks`; if it does not, resolve the constraint before creation.

## Work in the selected checkout

Use the tool's explicit working-directory parameter with the discovered absolute path for subsequent shell commands. For commands routed through Grove, use a selected worktree explicitly:

```bash
grove exec session-task -- git status --short --branch
grove exec session-task -- grove status --json
```

Run the outer Grove command from a known workspace directory. `grove exec` runs the child in the target checkout; it does not retarget later commands or file-editing tools. Use absolute paths or the correct workspace context for edits, and load the target checkout's applicable project instructions before changing files.

`grove switch` relies on shell integration to change that shell's directory. A directory change in a short-lived tool call does not establish the working directory of later calls. Likewise, `grove add --switch` does not migrate the running Codex or Claude Code session. Verify the selected path and branch before writing; filesystem access to the new checkout and shared Git directory must fit the session's permissions.

Creating a worktree or opening its Herdr workspace does not start or resume an agent. When asked to prepare a checkout for another session, report its absolute path, branch or detached ref, and setup status. Launching agents requires that scope in the task. Use `grove exec --all` only when the user intends every worktree to receive the command.

## Herdr integration

Enable integration by default when `HERDR_ENV=1` and `herdr` is on `PATH`. Binary availability alone does not establish a managed session. If either check fails, continue with plain Grove; do not inspect or control a focused Herdr session from outside Herdr.

Check the relevant Grove command's help for `--herdr` before adding it:

| Operation                 | Behavior when integration is available                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Create a checkout         | `grove add feat/session-task --base main --herdr` prepares it, then opens and focuses its Herdr workspace.              |
| Open an existing checkout | `grove switch session-task --herdr` opens or focuses its Herdr workspace without changing the caller's shell directory. |
| Remove a checkout         | Add `--herdr` to `remove` only if supported, after checking the associated workspace and running processes.             |
| Prune checkouts           | Use `--herdr` consistently on preview and committed cleanup if supported and associated workspace closure is in scope.  |

Do not combine `add --herdr` with `--switch`. A request such as "without switching" or "keep focus here" overrides automatic integration: omit `--herdr` because it focuses the target workspace. Do not substitute a focus-changing operation for background creation.

Some Grove builds support integration only on `add` and `switch`. Omit unsupported flags and report when a corresponding Herdr workspace must be handled separately. Use Grove to create and remove worktrees; `herdr worktree create` bypasses Grove's setup behavior.

For direct Herdr inspection or control, read the available Herdr skill, or run `herdr --skill` if none is loaded. Discover syntax with `herdr --help` and relevant command groups; bare `herdr` launches or attaches the terminal UI. Use returned workspace and pane IDs, with explicit targets or caller context, rather than another client's focus. Do not start agents or close unrelated workspaces as part of routine worktree management.

If Herdr handoff fails after creation, inspect Grove's worktree list and Herdr state before retrying. Reuse the created checkout; do not repeat `add` blindly, particularly for PRs where it can refresh the branch. Report worktree creation and Herdr handoff as separate outcomes.

## Finish within scope

Leave the worktree available unless cleanup was requested. For requested cleanup, follow [workspace setup and cleanup](references/lifecycle.md), checking session ownership, local changes, commits, and locks before removal. Report the affected worktrees, retained or deleted branches, and any incomplete setup or cleanup.

## Sources

- [Grove upstream documentation](https://github.com/sQVe/grove): authoritative behavior alongside installed CLI help.
- [Herdr skill](https://github.com/herdrdev/herdr/blob/master/skills/herdr/SKILL.md): managed-session checks and terminal coordination guidance.
- [Original inspiration](https://github.com/sQVe/dotfiles/blob/master/claude/skills/grove/SKILL.md): consulted for workflow concerns; instructions here are independently written and checked against Grove.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
