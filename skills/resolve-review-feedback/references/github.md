# GitHub review feedback

## Tool routing and terminology

Checked 2026-09-30 (Asia/Ho_Chi_Minh, UTC+07:00). Verify installed schemas and
host support at execution time.
The
[pull_requests MCP endpoint](https://api.githubcopilot.com/mcp/x/pull_requests)
is an authenticated MCP service, not a public REST command catalog. The
[remote-server guide](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)
documents toolset selection and read-only configurations. Missing write tools do
not prevent reading through MCP and using an authorized CLI/API mutation.

A PR review is a submission that can contain review comments. A review
conversation (API review thread) contains related comments and replies, with its
own resolution state. PR timeline/issue comments are general discussion and have
no review-thread resolution action. Review submission bodies may provide context
but are not themselves resolvable conversations. These distinctions follow
[GitHub's commenting guidance](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/commenting-on-a-pull-request).

## Discover and assess

The relevant
[GitHub MCP catalog](https://github.com/github/github-mcp-server/blob/main/README.md#pull-requests)
documents:

- `pull_request_read`: `owner`, `repo`, `pullNumber`, `method`. `get` supplies
  PR identity; `get_diff`/`get_files` supply code context; `get_review_comments`
  returns review threads; `get_reviews` retrieves submissions; `get_comments`
  retrieves timeline discussion. Thread retrieval uses `perPage` and cursor
  `after`; other paged methods use `page`/`perPage`.
- `add_reply_to_pull_request_comment`: `owner`, `repo`, `pullNumber`, numeric
  `commentId`, and `body` for a reply.
- `pull_request_review_write`: `method=resolve_thread`, `threadId`, and required
  `owner`, `repo`, `pullNumber`. Use the GraphQL thread node ID from discovery.

Check the loaded schema: server versions, feature gates, and host namespaces
differ. Review coordinates may be null/outdated. Retrieve all thread pages and
all nested comment pages; supplement any truncated response with the next
capable tool.

For CLI identity fallback, use
[gh pr view](https://cli.github.com/manual/gh_pr_view):

```sh
gh pr view --json number,url,headRefName,headRefOid,headRepository,baseRefOid
```

Verify against git remotes and branch rather than trusting defaults. Use an
explicit PR number and `--repo '[HOST/]OWNER/REPO'` after selection.
`gh pr view --comments` and its `comments`/`reviews` JSON fields do not provide
the complete review-thread resolution model; `reviewThreads` is not a documented
JSON field.

Set `pr_host` from the verified PR URL or remote identity. Pass
`--hostname "$pr_host"` to every `gh api` discovery, nested-comment retrieval,
reply, and resolution command. A previous `gh pr view --repo HOST/...` does not
carry host selection into another invocation. Explicit `--hostname` also avoids
depending on an unset or conflicting `GH_HOST`; the API command otherwise
defaults to github.com. Stop if the returned repository or PR identity does not
match.

When thread-capable MCP is unavailable, use
[gh api](https://cli.github.com/manual/gh_api) with GraphQL. This is the CLI's
API transport, not an invented `gh pr resolve` command. A query shaped as
follows preserves thread status and identity; request additional diff/comment
metadata as needed for lossless context:

```graphql
query($owner: String!, $repo: String!, $number: Int!, $endCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      headRefOid
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved isOutdated viewerCanResolve path line startLine diffSide
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id databaseId body url createdAt updatedAt
              author { login }
              commit { oid }
              originalCommit { oid }
            }
          }
        }
      }
    }
  }
}
```

Save the authored query to a temporary file, then pass it as a field:

```sh
gh api --hostname "$pr_host" graphql --paginate \
  -F owner="$pr_owner" -F repo="$pr_repo" \
  -F number="$pr_number" -F query=@/tmp/review-threads.graphql
```

`--paginate` follows the outer `$endCursor`; it does not exhaust every nested
`comments` connection. Page those separately by thread node ID, fetching
`node(id: $thread)` as `PullRequestReviewThread` with its comments cursor.
Verify schema availability on the target host; the
[MCP implementation](https://github.com/github/github-mcp-server/blob/main/pkg/github/pullrequests.go)
also demonstrates the `resolveReviewThread(input: {threadId: ...})` mutation.
REST review-comment lists alone cannot establish thread resolution state.

## Publish

Read the PR's current head SHA before editing and before pushing. For fork PRs,
identify the source repository/branch and writable remote separately from the
base repository. Use git to publish authorized local commits, preserve
concurrent history, then verify PR head ancestry and changed files against the
recorded SHAs. Updating PR metadata or submitting an approval review is not part
of feedback publication.

## Reconcile

Refresh the original thread and its replies. For an authorized reply use the MCP
operation above, or the documented
[REST reply endpoint](https://docs.github.com/en/rest/pulls/comments#create-a-reply-for-a-review-comment):
`POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies`
with JSON `body`. Use the top-level review comment's numeric REST ID, not a
reply ID or `PRRT_...` node ID. `gh pr comment` creates timeline discussion; it
does not reply to a review conversation.

When MCP cannot reply, use CLI transport with an authored JSON body file:

```sh
pr_reply_endpoint="repos/$pr_owner/$pr_repo/pulls/$pr_number/comments"
gh api --hostname "$pr_host" --method POST \
  "$pr_reply_endpoint/$root_comment_id/replies" \
  --input /tmp/review-reply.json
```

For authorized resolution prefer capable MCP. Otherwise invoke GraphQL through
`gh api --hostname "$pr_host" graphql`, supplying the thread node ID as a
variable:

```graphql
mutation($thread: ID!) {
  resolveReviewThread(input: {threadId: $thread}) {
    thread { id isResolved }
  }
}
```

Save the mutation to a temporary file, then invoke it against the verified host:

```sh
gh api --hostname "$pr_host" graphql -F thread="$thread_id" \
  -F query=@/tmp/resolve-review-thread.graphql
```

If CLI transport is unavailable, use an authenticated direct REST request for a
reply or GraphQL request to the verified host's GraphQL endpoint for resolution.
Derive direct API endpoints from the same verified host, never a hardcoded
github.com default. Preserve
variables and structured JSON; never interpolate review bodies into shell
commands. Read back the thread after mutation. Inspect GraphQL `errors` even
with HTTP 200. After a timeout, read before retrying to avoid duplicate replies.

Resolved and outdated are independent facts. Leave resolved threads untouched by
default; outdated threads still need assessment. GitHub's resolved flag does not
prove a fix: for rejected/unclear requests prefer an authorized explanation and
leave open unless a truthful terminal disposition is specifically authorized.

## Identifiers, permissions, and limits

Retain host, base/source repository identity, PR number/node ID, head SHA,
thread node ID, every comment node and numeric ID, author, URL, current/original
coordinates, and diff/commit context. Resolution requires the actual thread ID,
not a review ID.

Use existing credentials. Discovery needs repository/PR access;
replies/resolution need the corresponding review-write rights. The MCP catalog
reports OAuth `repo`; effective access also depends on token type, repository
rights and host policy. Check `viewerCanResolve` where available; capability
does not grant user authority. Read-only MCP configuration and lockdown
filtering can restrict operations or coverage. Report such limits instead of
claiming all feedback was retrieved.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
