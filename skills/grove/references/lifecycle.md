# Workspace setup and cleanup

Read this reference when creating a Grove workspace, diagnosing one, renaming a checkout, or removing session worktrees. Check installed command help before using the examples.

## Establish a workspace

An ordinary Git clone is not automatically a Grove workspace. If workspace discovery fails, distinguish the wrong working directory from a repository that has not been set up for Grove.

| Requested outcome                 | Grove operation                         |
| --------------------------------- | --------------------------------------- |
| Clone into a new workspace        | `grove clone <url> [directory]`         |
| Create a new repository workspace | `grove init new [directory]`            |
| Convert an existing repository    | `grove init convert`                    |
| Inspect workspace problems        | `grove doctor` or `grove doctor --json` |

Conversion changes repository layout and paths used by running sessions. Perform it only when the task includes conversion and its effect on those sessions is understood. Do not initialize, clone, or convert as an automatic fallback for a failed inspection command. `doctor --fix` also mutates state; diagnose first and apply repairs within scope.

Configuration inspection is separate from changing it. `grove config init` creates configuration; `set` and `unset` target shared `.grove.toml` with `--shared` or personal Git configuration with `--global`. Change only the configuration requested by the task. Do not modify shell startup files merely to make `switch` convenient for tool calls.

## Preserve useful context without coupling sessions

Review `[preserve]`, `[link]`, `[hooks]`, and `[autolock]` before setup. Effective settings can include personal Git configuration and a `.grove.toml` found in another worktree. Consult `grove config list`, the chosen source, and upstream documentation when selection is unclear.

- Preservation copies configured files or directories; it is not a patch transfer. `--from <worktree>` selects the source, while `--base` selects branch ancestry.
- Symlinks expose shared writable content. Linking an agent's state directory, dependencies, or build output can undermine isolation between Codex and Claude Code sessions. Prefer independent state unless sharing is deliberate and compatible with both tasks.
- Add hooks execute shell commands in the new worktree. Check their effects and permissions before creating it, especially for unfamiliar repositories. A hook failure does not imply creation was rolled back. Inspect the worktree and earlier setup results before rerunning a failed step; earlier hooks may already have completed.
- Repeating `grove add --pr` can refresh an existing PR checkout. Treat that as a branch update, not an existence check. `--reset` can discard local commits and affected files; use it only when that loss is specifically authorized.

## Rename or protect a checkout

`grove move <worktree> <new-branch>` renames the branch and directory. Check that no active session depends on the old path, then rediscover the resulting path and update the task's working-directory references.

`grove lock <worktree> --reason "..."` protects a checkout from routine removal. A lock does not prove an agent is running, and an unlocked checkout does not prove it is idle. Honor existing locks; unlocking or overriding them needs an understood reason within the task's scope.

## Remove named worktrees

Before removal, resolve each target and check:

- Whether another session or process still uses it, including a session with a clean working tree. If ownership is unknown and removal would disrupt it, ask before proceeding.
- Tracked, staged, and untracked changes, plus any local-only ignored files that matter. `git status --short --branch --untracked-files=all` helps inspect changes, but ignored local data needs separate consideration.
- Local commits, upstream state, and merge status when branch deletion is requested. A missing upstream is not proof that commits are safely retained elsewhere; `grove list --fast` omits the checks needed here.

Run removal from a surviving checkout or the workspace root. `grove remove <worktree>` removes the checkout while retaining its branch. Add `--branch` only when branch deletion is requested or clearly included in the authorized cleanup. It can reject unmerged branches before removal.

When the [Herdr integration check](../SKILL.md#herdr-integration) passes, inspect the associated workspace for running agents or commands before cleanup. Append `--herdr` when `remove --help` supports it and closing that workspace is within scope. Unsupported builds remove only the checkout; report any remaining Herdr workspace rather than silently assuming it was closed. Do not close unrelated workspaces or terminate active work without authorization.

If removal refuses a dirty or locked target, inspect and explain the specific obstruction before proceeding. Do not automatically unlock, force, reset, stash, or delete files to make it succeed. `--force` can discard work; combined with `--branch`, it can delete unmerged and unpushed commits. Proceed when existing authorization covers discarding the identified work or overriding the lock; otherwise request only the missing authorization.

## Prune a set of worktrees

Preview the intended selection before applying bulk cleanup:

```bash
grove prune --json
grove prune --merged=main --json
grove prune --stale 30d --json
```

These previews do not remove worktrees, but they fetch and prune remote refs. Do not run them when repository mutations or network access are prohibited. A failed fetch can leave the selection based on stale remote information; report that limitation and resolve it before destructive cleanup.

Default pruning selects worktrees whose upstream is gone and also deletes their local branches. `--merged`, `--stale`, and `--detached` expand the selection; age alone does not establish that work is disposable. Use `--merged=<branch>` with the equals sign when supplying a branch.

Review the preview against the authorized targets and the checks above. Execute with the same selection flags plus `--commit` only when the resulting removals and branch deletions are within scope. `--json` is for previews, not the committed operation. If a workspace-wide prune would select unrelated worktrees, remove the authorized named targets instead. Re-list afterward and report any refused or incomplete removals.

If Herdr integration is active and `prune --help` supports `--herdr`, include it in both preview and execution when associated workspace cleanup is intended. Review those workspace targets alongside the worktree targets; a cleanup request does not authorize terminating unrelated sessions.

## Behavior sources

The [Grove README](https://github.com/sQVe/grove/blob/b95f6a5a6cd03e220ded2e7fef138d74283183b5/README.md), [add implementation](https://github.com/sQVe/grove/blob/b95f6a5a6cd03e220ded2e7fef138d74283183b5/cmd/grove/commands/add.go), and [prune implementation](https://github.com/sQVe/grove/blob/b95f6a5a6cd03e220ded2e7fef138d74283183b5/cmd/grove/commands/prune.go) were consulted for these independently authored instructions. Installed help takes precedence for available flags; consult current upstream sources when behavior needs clarification.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
