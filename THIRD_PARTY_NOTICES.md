# Third-Party Notices

This repository may contain, adapt, or depend on material originating from third parties.

Third-party material remains subject to its original copyright and license terms and does not automatically inherit the repository's default licenses.

When third-party material is copied, adapted, vendored, or materially incorporated into this repository, document it below.

Use the exact repository-relative path in each `Used in` entry. License validation uses that entry to approve a non-default SPDX license under `skills/`.

## Notice template

### <Project or source name>

- **Source:** <upstream project or URL>
- **Copyright:** <copyright holder, if applicable>
- **License:** <license identifier/name>
- **Used in:** `<repository path>`
- **Modifications:** <none, or short description>

Where appropriate, retain the upstream license under:

`third_party/<project>/`

## Platform capability references

The references below summarize upstream tool names, parameters, and behavior in
repository-authored prose. No upstream implementation or documentation passages
are copied. The references retain the repository's `CC-BY-NC-SA-4.0` license;
the upstream server licenses identify the consulted sources, not a relicensing
of their implementations or associated platform documentation.

### GitHub MCP Server

- **Source:** [GitHub MCP Server](https://github.com/github/github-mcp-server),
  including its tool catalog, remote-server documentation and PR tool schemas.
- **Copyright:** Copyright (c) 2025 GitHub; see upstream notices.
- **License:**
  [MIT](https://github.com/github/github-mcp-server/blob/main/LICENSE) for the
  upstream server.
- **Used in:** `skills/resolve-review-feedback/references/github.md`
- **Modifications:** Original capability summaries and authored API examples;
  additional GitHub CLI and platform documentation is linked at each relevant
  use.

### Azure DevOps MCP

- **Source:** [Azure DevOps MCP](https://github.com/microsoft/azure-devops-mcp),
  including its toolset documentation and repository tool schemas.
- **Copyright:** Microsoft Corporation and contributors; see upstream notices.
- **License:**
  [MIT](https://github.com/microsoft/azure-devops-mcp/blob/main/LICENSE.md) for
  the upstream server.
- **Used in:** `skills/resolve-review-feedback/references/azure-devops.md`
- **Modifications:** Original capability summaries and authored API examples;
  additional Microsoft CLI and REST documentation is linked at each relevant
  use.

## Git convention references

These specifications are linked and summarized in original repository-authored
prose; no upstream documentation passages or implementation files are copied.
The skill retains the repository's `CC-BY-NC-SA-4.0` license.

### Angular commit message guidelines

- **Source:** [Angular guidelines](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md#type)
- **Copyright:** Copyright (c) 2010–2026 Google LLC.
- **License:** [MIT](https://github.com/angular/angular/blob/main/LICENSE).
- **Used in:** `skills/git-conventions/SKILL.md`
- **Modifications:** Original operational summary of type/header conventions;
  local types added, Angular scopes and mandatory bodies excluded.

### Conventional Branch

- **Source:** [Conventional Branch 1.1.0](https://conventionalbranch.org/)
- **Copyright:** Conventional Branch contributors; see upstream notices.
- **License:** [CC-BY-4.0](https://github.com/conventional-branch/conventional-branch/blob/main/LICENSE).
- **Used in:** `skills/git-conventions/SKILL.md`
- **Modifications:** Original operational summary; `docs/` added and `chore/`
  restricted to exclude documentation-only work.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
