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

## Grove workflow sources

### Grove CLI

- **Source:** [Grove](https://github.com/sQVe/grove/tree/b95f6a5a6cd03e220ded2e7fef138d74283183b5), including its README, command implementations, and installed CLI help.
- **Copyright:** Copyright (c) 2025 Oskar Grunning.
- **License:** [MIT](https://github.com/sQVe/grove/blob/b95f6a5a6cd03e220ded2e7fef138d74283183b5/LICENSE) for the upstream implementation and documentation.
- **Used in:** `skills/grove/SKILL.md`
- **Used in:** `skills/grove/references/lifecycle.md`
- **Modifications:** Independently authored command examples and behavioral summaries; no upstream implementation or documentation passages are copied or vendored. Repository-authored prose retains `CC-BY-NC-SA-4.0`.

### Grove skill in sQVe's dotfiles

- **Source:** [Upstream Grove skill](https://github.com/sQVe/dotfiles/blob/efaffa48bd8f622f82f9a1b55ad442771f33c5ad/claude/skills/grove/SKILL.md).
- **License:** No license was identified for this skill in the consulted source; no permission to redistribute its text is assumed.
- **Used in:** `skills/grove/SKILL.md`
- **Used in:** `skills/grove/references/lifecycle.md`
- **Modifications:** Consulted as workflow inspiration only. No text or templates are copied or adapted; operational guidance is independently written and checked against Grove's CLI and upstream sources. Personal naming conventions and terminal orchestration are not incorporated.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
