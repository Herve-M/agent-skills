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

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
