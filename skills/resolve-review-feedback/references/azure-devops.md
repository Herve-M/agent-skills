# Azure DevOps review feedback

## Tool routing and domain

Checked 2026-09-30 against the
[Azure DevOps MCP project](https://github.com/microsoft/azure-devops-mcp) and
[az repos reference](https://learn.microsoft.com/en-us/cli/azure/repos).
Inspect actual exposed schemas: local/remote server versions and namespaces
vary. Select capable MCP separately for reads and writes, then CLI, then direct
REST.

The interaction unit is a pull-request thread, containing an initial comment and
replies. Threads can be attached to code or have no file context. A fileless
thread can still contain concrete review feedback; status alone does not make
general discussion actionable. System messages, deleted content and
non-actionable events are separately classified. Preserve iteration/tracking
context across PR updates. See the
[thread-list schema](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/list?view=azure-devops-rest-7.1).

## Discover and assess

The current
[MCP toolset](https://github.com/microsoft/azure-devops-mcp/blob/main/docs/TOOLSET.md#repositories)
uses `action`-based operations:

| Tool                             | Relevant actions         |
| -------------------------------- | ------------------------ |
| `repo_repository`                | `get`, `list`            |
| `repo_pull_request`              | `get`, `list`            |
| `repo_pull_request_thread`       | `list`, `list_comments`  |
| `repo_pull_request_thread_write` | `reply`, `update_status` |

For thread operations provide `repositoryId`, `pullRequestId`, and `project`
when using a repository name rather than GUID. `list_comments` needs `threadId`;
`reply` needs `threadId`/`content`; `update_status` needs `threadId`/`status`.
Thread reads support `top`/`skip`. The
[repository tool schemas](https://github.com/microsoft/azure-devops-mcp/blob/main/src/tools/repositories.ts)
use SDK enum names for status (for example `Fixed`, rather than REST `fixed`).
Inspect the loaded enum and supply status explicitly: a default of `Active` must
not reopen a thread accidentally. Trimmed MCP responses can omit comment type,
deletion flags and identity fields; request `fullResponse: true` on reads when
classification or traceability needs them. Fall back only if the available MCP
schema cannot supply the required metadata. Retrieve all pages and replies.

For CLI identity fallback, the
[az repos pr manual](https://learn.microsoft.com/en-us/cli/azure/repos/pr)
documents:

```sh
az repos pr list --org "$ado_org_url" --project "$ado_project" \
  --repository "$ado_repository" --source-branch "$pr_branch" --status active
az repos pr show --org "$ado_org_url" --id "$pr_id"
```

Verify returned repository, `sourceRefName`, `targetRefName`, and
`lastMergeSourceCommit.commitId` against git and the selected PR. Pagination
matters when listing candidates. `az repos pr update` changes PR metadata/state,
not review thread status. The documented command group has no dedicated
review-thread command.

For missing thread MCP use
[az devops invoke](https://learn.microsoft.com/en-us/cli/azure/devops#az-devops-invoke),
the CLI's generic REST transport:

```sh
az devops invoke --org "$ado_org_url" --area git --resource pullRequestThreads \
  --route-parameters project="$ado_project" repositoryId="$ado_repository_id" \
  pullRequestId="$pr_id" --http-method GET --api-version 7.1
```

Inspect `az devops invoke --help` and available resource definitions if the
installed extension cannot route the operation. Use direct authenticated REST
only when MCP/CLI coverage is insufficient or unavailable. The threads endpoint
is:

```text
{organization}/{project}/_apis/git/repositories/{repositoryId}/pullRequests/{pullRequestId}/threads?api-version=7.1
```

URL-encode path parameters and use the verified organization URL. Preserve the
complete thread/comments/context response, and follow any paging/continuation
instructions from the actual endpoint. A missing/deleted comment is not empty
intent.

## Publish

Refresh source branch SHA and iteration context before editing/pushing. PR IDs
do not encode branch identity. Publish authorized commits with git to the
verified source remote/ref, then verify the PR source history contains them. A
changed iteration can invalidate old file/range mappings even when a thread ID
survives.

## Reconcile and status semantics

The REST
[thread-update schema](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-threads/update?view=azure-devops-rest-7.1)
defines these statuses; the disposition column is this skill's choice guidance:

| REST status | Platform meaning      | Appropriate disposition                                        |
| ----------- | --------------------- | -------------------------------------------------------------- |
| `unknown`   | Unknown status        | Investigate; never select as a completion shortcut             |
| `active`    | Active                | Pending work or failed implementation remains open             |
| `fixed`     | Resolved as fixed     | Implemented, validated and visible in remote PR history        |
| `wontFix`   | Resolved as won't fix | Intentionally declined change                                  |
| `closed`    | Closed                | Truthful generic terminal closure, such as obsolete discussion |
| `byDesign`  | Resolved as by design | Existing behavior is intentional and supported by requirements |
| `pending`   | Pending               | Awaiting information or deferred work                          |

MCP SDK responses may encode status numerically. The
[SDK enum](https://github.com/microsoft/azure-devops-node-api/blob/master/api/interfaces/GitInterfaces.ts)
maps `0=Unknown`, `1=Active`, `2=Fixed`, `3=WontFix`, `4=Closed`, `5=ByDesign`,
`6=Pending`. Preserve the raw value alongside its normalized meaning.

Retrieve `active` and `pending` review findings; investigate unknown status
rather than assuming it is resolved. Account separately for `fixed`, `wontFix`,
`closed` and `byDesign`, leaving them unchanged by default. Status is not proof
of technical validity. Deferred/unclear/failed feedback cannot become `fixed`. A
rejected request is `byDesign` only with design evidence; otherwise `wontFix`
may fit. Keep `active` or use authorized `pending` for incomplete work. Do not
automatically close every interaction or automatically transition general
discussion.

Prefer capable MCP for authorized reply/status updates. CLI fallback:

```sh
az devops invoke --org "$ado_org_url" --area git \
  --resource pullRequestThreadComments \
  --route-parameters project="$ado_project" repositoryId="$ado_repository_id" \
  pullRequestId="$pr_id" threadId="$thread_id" \
  --http-method POST --api-version 7.1 --in-file /tmp/review-reply.json
az devops invoke --org "$ado_org_url" --area git --resource pullRequestThreads \
  --route-parameters project="$ado_project" repositoryId="$ado_repository_id" \
  pullRequestId="$pr_id" threadId="$thread_id" \
  --http-method PATCH --api-version 7.1 --in-file /tmp/review-status.json
```

Author structured JSON files rather than shell-interpolated bodies. For replies,
[the comment-create endpoint](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/pull-request-thread-comments/create?view=azure-devops-rest-7.1)
accepts `content`, `parentCommentId`, and `commentType`; use the original
comment ID where reply linkage is needed and `commentType: "text"`. Direct REST
fallback uses
`POST {threads-url-without-query}/{threadId}/comments?api-version=7.1`. Status
updates use `PATCH {threads-url-without-query}/{threadId}?api-version=7.1` with
a body such as `{"status":"fixed"}`. Use the transport's documented spelling,
not the SDK enum spelling from MCP. Do not edit reviewer comments as a reply.

Re-fetch the thread after every mutation and compare actual status/reply
content. An ambiguous timeout requires read-back before retry. Evaluate every
source thread independently; grouped findings do not imply identical final
statuses.

## Identifiers, permissions, and limits

Retain organization/collection URL, project ID/name, repository GUID/name, PR
ID, source/base refs and SHAs, thread ID, comment IDs/parent linkage,
authors/timestamps, thread and iteration/tracking context, status and available
`_links`/URLs. Do not invent a permalink if none is supplied; report composite
source identity instead.

Use existing authenticated MCP/CLI/API access. Thread-list docs identify
`vso.code` for reading. Mutation docs list `vso.code_write` and
`vso.threads_full`; actual token and repository permissions still govern access.
Git push permission is separate from thread mutation authority. CLI commands
require the Azure DevOps extension; verify availability, credentials,
organization access, and target server support. When metadata or rights are
unavailable, leave the source unreconciled and report the exact missing
capability.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
