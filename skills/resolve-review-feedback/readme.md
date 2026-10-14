# Resolve review feedback

Analyze and resolve received pull-request review feedback on GitHub or Azure
DevOps. [SKILL.md](SKILL.md) contains the authoritative execution instructions;
this README explains the purpose and how to request the workflow.

## Why this skill exists

Review feedback mixes bug reports, suggested solutions, questions, and comments
that may already be covered by the code. Several conversations can concern one
issue, while nearby comments in the same file can describe unrelated problems.
Implementing every suggestion without checking intent can introduce regressions
or change behavior the project deliberately requires.

This skill checks claims against the code and repository conventions, preserves
every source conversation, and proposes fixes for actionable findings. It keeps
implementation, validation, publication, and remote thread status separate: a
local fix does not establish that a reviewer can see it in the PR.

Use it for received, actionable review feedback. A fresh code review, PR
creation, or general timeline discussion uses a different workflow.

## How to use it

Provide the PR URL or established PR context, identify any selected comments,
and state how far the workflow should go. Existing explicit authorization is
sufficient; the skill asks only for missing authority.

### Assess feedback without editing

```text
$resolve-review-feedback
Analyze the received review comments on <PR URL>. Check each claim against the
code, preserve the source links, and report validity, confidence, and risk.
Stop after assessment; do not edit files or change remote conversations.
```

This discovers review conversations and assesses them. It distinguishes valid,
partially valid, invalid, unclear, and out-of-scope findings without treating
every reviewer suggestion as the correct solution.

### Propose fixes

```text
$resolve-review-feedback
Suggest fixes for the actionable review feedback on <PR URL>. Explain the
approach, affected files, trade-offs, and validation for each issue. Do not edit
files, commit, push, reply, or resolve threads.
```

This stops at planning. Comments about the same underlying issue can share a
fix, but each original conversation and reply remains traceable.

### Implement selected fixes locally

```text
$resolve-review-feedback
Implement the approved empty-input fix on <PR URL>, including necessary tests
and documentation. Run the required checks and preserve unrelated changes.
Do not commit, push, reply, or resolve threads.
```

This authorizes implementation and validation for the selected issue. The report
identifies local changes and check results; remote conversations remain open.

### Handle feedback end-to-end

```text
$resolve-review-feedback
Handle the received actionable feedback on <PR URL> end-to-end. Implement valid
fixes, validate, commit, push, and reply to and resolve addressed conversations.
Explain rejected or unclear findings and keep outstanding requests open.
```

This authorizes the applicable stages, including publication and reconciliation.
The skill verifies that fixes are visible in remote history before marking
feedback addressed. Failed required validation stops publication by default;
failed publication stops reconciliation of the affected feedback.

### Use within a larger workflow

```text
While preparing the release, use resolve-review-feedback only to assess the
selected review threads on <PR URL>. Return the source-linked findings, then
continue release preparation. Do not edit files or change remote state.
```

The parent chooses the stages and retains control of the primary task.

## Workflow

```text
discover -> assess -> plan -> implement -> validate -> publish -> reconcile
```

The flow stops at the requested extent. Code edits, test edits, commits, pushes,
replies, and status transitions have separate authorization boundaries. Supplied
artifacts can support skipped stages after their evidence is verified.

For example, two threads may report the same empty-input failure. The skill
plans one contract-consistent fix while retaining both source conversations.
After validation and authorized publication, it rechecks each thread. If one
has acquired a new caller-specific requirement, that thread stays open until
the outstanding request is handled.

Results distinguish implemented, validated, published, and reconciled work,
including rejected, deferred, unclear, and failed findings. Uncertain PR
identity, incomplete source mapping, or ambiguous remote mutations stop the
affected writes rather than producing a false completion claim.

For deeper guidance, see [assessment](references/assessment.md),
[GitHub handling](references/github.md), and
[Azure DevOps handling](references/azure-devops.md). The
[evaluation scenarios](references/evaluations.md) document behavioral coverage
and the checks actually performed.

## Changelog

### 2026-10-13

- Added this README with rationale, usage examples, and workflow explanation.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
