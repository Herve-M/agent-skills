---
name: grove
description: >-
  Manage Git worktrees with Grove CLI for Codex and Claude Code sessions. Use when creating or locating an isolated branch or PR checkout, working in another worktree, or cleaning up session worktrees. Applies to worktree management with Grove, not ordinary Git edits or agent session orchestration.
license: CC-BY-NC-SA-4.0
---

# Grove

Use Grove to prepare and manage worktrees while keeping each coding session attached to the intended checkout. Prefer Grove for worktree lifecycle operations so its configuration, preservation, hooks, and locks apply; ordinary Git inspection and development commands remain appropriate inside a worktree.

## Inspect before acting

1. Check `grove --version` and the relevant `grove <command> --help`. Installed builds can differ from current upstream documentation; use only supported flags.
2. Establish the repository and current directory, then run `grove list --json` from the workspace or one of its worktrees. Use `--fast` when only names, branches, and paths are needed. Keep stderr separate from JSON stdout.
3. Select an existing worktree by its returned name, branch, and absolute path. Do not derive the path from a branch name: Grove can normalize names and users can override them. Do not create a checkout just to inspect an existing one.

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

Creating a worktree does not start or resume an agent. When asked to prepare a checkout for another session, report its absolute path, branch or detached ref, and setup status. Launching agents, opening terminal workspaces, and using optional `--herdr` integration require that scope in the task; do not infer it from worktree creation. Use `grove exec --all` only when the user intends every worktree to receive the command.

## Finish within scope

Leave the worktree available unless cleanup was requested. For requested cleanup, follow [workspace setup and cleanup](references/lifecycle.md), checking session ownership, local changes, commits, and locks before removal. Report the affected worktrees, retained or deleted branches, and any incomplete setup or cleanup.

## Sources

- [Grove upstream documentation](https://github.com/sQVe/grove): authoritative behavior alongside installed CLI help.
- [Original inspiration](https://github.com/sQVe/dotfiles/blob/master/claude/skills/grove/SKILL.md): consulted for workflow concerns; instructions here are independently written and checked against Grove.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
