# Repository instructions

Maintain this repository as the canonical source for reusable, agent-neutral AI
skills. Keep machine-specific configuration and secrets outside the repository.

## Add or change a skill

1. Keep one canonical implementation in a lowercase kebab-case directory under
   `skills/`. Create a harness-specific copy only for a demonstrated
   incompatibility.
2. Read `skills/README.md` before adding a skill. Every skill requires
   `skills/<skill-name>/SKILL.md`; add `references/`, `templates/`, `assets/`,
   or `scripts/` only when the skill needs them.
3. In `SKILL.md`, include the required metadata, purpose and triggers, primary
   workflow, essential constraints, and pointers to supporting material. Keep
   it concise and move detailed standards, examples, and decision material into
   `references/`.
4. Put output skeletons in `templates/`, non-executable resources in `assets/`,
   and deterministic executable behavior in `scripts/`.

## Licensing and provenance

- License repository-authored Markdown skill content as `CC-BY-NC-SA-4.0` and
  add its SPDX identifier after any frontmatter, near the end of the file.
- License repository-authored scripts and executable helpers as `MPL-2.0` and
  add its SPDX identifier using the language's comment syntax.
- Preserve any differing file-specific license.
- Preserve upstream notices and record copied, adapted, vendored, or materially
  incorporated third-party material in `THIRD_PARTY_NOTICES.md`. Store local
  upstream license material under `third_party/<project>/` when appropriate.

## Complete the change

1. Run `mise run format-markdown` after editing Markdown.
2. Run `mise run validate` and `mise run check-markdown-format`. If required
   external tooling is unavailable, perform local structural checks and report
   the missing coverage.
3. Review the final diff for correctness, scope, licensing, and provenance.
   Keep unrelated edits separate.
4. When preparing a pull request, explain its purpose and scope, identify any
   licensing or provenance considerations, and report the validation results.

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
