#!/bin/sh
# SPDX-License-Identifier: MPL-2.0

set -eu

failures=0

fail() {
    printf 'ERROR: %s\n' "$*" >&2
    failures=$((failures + 1))
}

require_file() {
    if [ ! -f "$1" ]; then
        fail "required file is missing: $1"
    fi
}

validate_skill_metadata() {
    skill_file=$1

    if ! command -v yq >/dev/null 2>&1; then
        fail "yq is unavailable; run 'mise install'"
        return
    fi

    if ! sed -n '1p' "$skill_file" | grep -qx -- '---' ||
        ! yq --exit-status --front-matter=extract 'tag == "!!map"' "$skill_file" >/dev/null 2>&1
    then
        fail "invalid SKILL.md frontmatter: $skill_file"
        return
    fi

    if ! yq --exit-status --front-matter=extract '
        ((.name | tag) == "!!str") and
        ((.name | length) > 0) and
        ((.name | length) <= 64) and
        (.name | test("^[a-z0-9]+(-[a-z0-9]+)*$")) and
        ((.description | tag) == "!!str") and
        ((.description | sub("^[[:space:]]+|[[:space:]]+$"; "") | length) > 0) and
        ((.description | length) <= 1024)
    ' "$skill_file" >/dev/null 2>&1
    then
        fail "invalid required skill metadata: $skill_file"
        return
    fi

    metadata_name=$(yq --unwrapScalar --front-matter=extract '.name' "$skill_file")
    directory_name=$(basename "$(dirname "$skill_file")")
    if [ "$metadata_name" != "$directory_name" ]; then
        fail "skill name does not match directory: $skill_file"
    fi
}

check_skills() {
    for skill_dir in skills/*/
    do
        [ -d "$skill_dir" ] || continue
        skill_name=$(basename "$skill_dir")
        if [ "${#skill_name}" -gt 64 ] ||
            ! printf '%s\n' "$skill_name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'
        then
            fail "invalid skill name: $skill_name"
        fi
        require_file "${skill_dir}SKILL.md"
        if [ -f "${skill_dir}SKILL.md" ]; then
            validate_skill_metadata "${skill_dir}SKILL.md"
        fi
    done
}

check_structure() {
    for path in \
        .editorconfig \
        .gitattributes \
        .gitignore \
        .rumdl.toml \
        .vscode/extensions.json \
        AGENTS.md \
        LICENSE.md \
        README.md \
        THIRD_PARTY_NOTICES.md \
        mise.lock \
        mise.toml \
        prek.toml \
        LICENSES/CC-BY-NC-SA-4.0.txt \
        LICENSES/MPL-2.0.txt \
        skills/README.md \
        tooling/README.md \
        third_party/README.md \
        .github/workflows/validate.yml \
        .github/pull_request_template.md
    do
        require_file "$path"
    done

    check_skills

    nested_harness_dirs=$(find skills -type d \( -name .claude -o -name .agents \) -print)
    if [ -n "$nested_harness_dirs" ]; then
        fail "harness-specific directories found under skills:\n$nested_harness_dirs"
    fi
}

check_licenses() {
    require_file LICENSES/CC-BY-NC-SA-4.0.txt
    require_file LICENSES/MPL-2.0.txt

    for path in \
        README.md \
        AGENTS.md \
        LICENSE.md \
        THIRD_PARTY_NOTICES.md \
        skills/README.md \
        tooling/README.md \
        third_party/README.md \
        .github/pull_request_template.md
    do
        if [ -f "$path" ] && ! grep -q 'SPDX-License-Identifier: CC-BY-NC-SA-4.0' "$path"; then
            fail "repository-authored content lacks CC-BY-NC-SA-4.0 SPDX identifier: $path"
        fi
    done

    find skills -type f -name '*.md' -print | while IFS= read -r path
    do
        if grep -q 'SPDX-License-Identifier: CC-BY-NC-SA-4.0' "$path"; then
            continue
        fi

        if grep -q 'SPDX-License-Identifier:' "$path"; then
            notice_entry="- **Used in:** \`$path\`"
            if grep -Fq -- "$notice_entry" THIRD_PARTY_NOTICES.md; then
                continue
            fi
            printf 'ERROR: unapproved skill Markdown license: %s\n' "$path" >&2
        else
            printf 'ERROR: skill Markdown lacks an SPDX identifier: %s\n' "$path" >&2
        fi
        exit 1
    done || failures=$((failures + 1))

    find skills tooling -type f \( \
        -name '*.py' -o -name '*.sh' -o -name '*.ps1' -o \
        -name '*.js' -o -name '*.ts' -o -name '*.cs' -o -name '*.go' \
    \) -print | while IFS= read -r path
    do
        if ! grep -q 'SPDX-License-Identifier: MPL-2.0' "$path"; then
            printf 'ERROR: executable source lacks MPL-2.0 SPDX identifier: %s\n' "$path" >&2
            exit 1
        fi
    done || failures=$((failures + 1))
}

check_markdown() {
    if ! command -v rumdl >/dev/null 2>&1; then
        fail "rumdl is unavailable; run 'mise install'"
        return
    fi

    if ! rumdl check .; then
        failures=$((failures + 1))
    fi
}

list_skills() {
    check_skills
    if [ "$failures" -ne 0 ]; then
        return
    fi

    for skill_dir in skills/*/
    do
        [ -d "$skill_dir" ] || continue
        basename "$skill_dir"
    done | LC_ALL=C sort
}

case "${1:-validate}" in
    validate)
        check_structure
        check_licenses
        check_markdown
        ;;
    check-licenses)
        check_licenses
        ;;
    lint-markdown)
        check_markdown
        ;;
    list-skills)
        list_skills
        ;;
    *)
        printf 'Usage: %s {validate|check-licenses|lint-markdown|list-skills}\n' "$0" >&2
        exit 2
        ;;
esac

if [ "$failures" -ne 0 ]; then
    printf 'Validation failed with %s error(s).\n' "$failures" >&2
    exit 1
fi

if [ "${1:-validate}" != 'list-skills' ]; then
    printf '%s: PASS\n' "${1:-validate}"
fi
