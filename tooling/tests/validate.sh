#!/bin/sh
# SPDX-License-Identifier: MPL-2.0

set -eu

repo_root=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
test_root=$(mktemp -d)
trap 'rm -rf "$test_root"' EXIT HUP INT TERM

fail() {
    printf 'FAIL: %s\n' "$1" >&2
    exit 1
}

new_repository() {
    case_dir="$test_root/$1"
    mkdir "$case_dir"
    cp -R "$repo_root/." "$case_dir"
}

expect_validation_failure() {
    expected_message=$1

    if output=$(cd "$case_dir" && tooling/validate.sh validate 2>&1); then
        fail "validation unexpectedly passed"
    fi

    case "$output" in
        *"$expected_message"*) ;;
        *) fail "validation failed without expected message: $expected_message" ;;
    esac
}

test_invalid_skill_name_is_rejected() {
    new_repository invalid-skill-name
    mkdir "$case_dir/skills/Bad_Name"
    cat >"$case_dir/skills/Bad_Name/SKILL.md" <<'EOF'
---
name: Bad_Name
description: A valid description attached to an invalid skill name.
---

# Invalid skill name fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "invalid skill name"
}

test_missing_frontmatter_is_rejected() {
    new_repository missing-frontmatter
    mkdir "$case_dir/skills/missing-frontmatter"
    cat >"$case_dir/skills/missing-frontmatter/SKILL.md" <<'EOF'
# Missing frontmatter fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "invalid SKILL.md frontmatter"
}

test_malformed_frontmatter_is_rejected() {
    new_repository malformed-frontmatter
    mkdir "$case_dir/skills/malformed-frontmatter"
    cat >"$case_dir/skills/malformed-frontmatter/SKILL.md" <<'EOF'
---
name: malformed-frontmatter
description: [unclosed
---

# Malformed frontmatter fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "invalid SKILL.md frontmatter"
}

test_missing_name_is_rejected() {
    new_repository missing-name
    mkdir "$case_dir/skills/missing-name"
    cat >"$case_dir/skills/missing-name/SKILL.md" <<'EOF'
---
description: A skill without required name metadata.
---

# Missing name fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "invalid required skill metadata"
}

test_non_string_description_is_rejected() {
    new_repository non-string-description
    mkdir "$case_dir/skills/non-string-description"
    cat >"$case_dir/skills/non-string-description/SKILL.md" <<'EOF'
---
name: non-string-description
description: 123
---

# Non-string description fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "invalid required skill metadata"
}

test_name_must_match_directory() {
    new_repository mismatched-name
    mkdir "$case_dir/skills/directory-name"
    cat >"$case_dir/skills/directory-name/SKILL.md" <<'EOF'
---
name: metadata-name
description: A valid description with a mismatched skill name.
---

# Mismatched name fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    expect_validation_failure "skill name does not match directory"
}

test_list_skills_rejects_invalid_skill() {
    new_repository invalid-listed-skill
    mkdir "$case_dir/skills/Bad_Name"
    cat >"$case_dir/skills/Bad_Name/SKILL.md" <<'EOF'
---
name: Bad_Name
description: A valid description attached to an invalid skill name.
---

# Invalid listed skill fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    if output=$(cd "$case_dir" && tooling/validate.sh list-skills 2>&1); then
        fail "list-skills unexpectedly published an invalid skill: $output"
    fi
}

test_unlisted_alternate_license_is_rejected() {
    new_repository unlisted-alternate-license
    mkdir "$case_dir/skills/alternate-license"
    cat >"$case_dir/skills/alternate-license/SKILL.md" <<'EOF'
---
name: alternate-license
description: A valid skill carrying an unapproved alternate license.
---

# Alternate license fixture

<!-- SPDX-License-Identifier: MIT -->
EOF

    if output=$(cd "$case_dir" && tooling/validate.sh check-licenses 2>&1); then
        fail "license validation unexpectedly accepted an unlisted alternate license"
    fi

    case "$output" in
        *"unapproved skill Markdown license"*) ;;
        *) fail "license validation failed without the expected alternate-license error" ;;
    esac
}

test_noticed_alternate_license_is_accepted() {
    new_repository noticed-alternate-license
    mkdir "$case_dir/skills/alternate-license"
    cat >"$case_dir/skills/alternate-license/SKILL.md" <<'EOF'
---
name: alternate-license
description: A valid third-party skill retaining its original license.
---

# Noticed alternate license fixture

<!-- SPDX-License-Identifier: MIT -->
EOF
    cat >>"$case_dir/THIRD_PARTY_NOTICES.md" <<'EOF'

### Alternate license fixture

- **Source:** https://example.com/alternate-license
- **License:** MIT
- **Used in:** `skills/alternate-license/SKILL.md`
- **Modifications:** none
EOF

    if ! output=$(cd "$case_dir" && tooling/validate.sh check-licenses 2>&1); then
        fail "license validation rejected a noticed alternate license: $output"
    fi
}

test_multiline_description_is_accepted() {
    new_repository multiline-description
    mkdir "$case_dir/skills/multiline-description"
    cat >"$case_dir/skills/multiline-description/SKILL.md" <<'EOF'
---
name: multiline-description
description: >-
  A valid multiline description that explains what the skill does and when to
  use it.
---

# Multiline description fixture

<!-- SPDX-License-Identifier: CC-BY-NC-SA-4.0 -->
EOF

    if ! output=$(cd "$case_dir" && tooling/validate.sh list-skills 2>&1); then
        fail "list-skills rejected valid multiline metadata: $output"
    fi
    case "$output" in
        *"multiline-description"*) ;;
        *) fail "list-skills omitted a valid skill" ;;
    esac
}

test_invalid_skill_name_is_rejected
test_missing_frontmatter_is_rejected
test_malformed_frontmatter_is_rejected
test_missing_name_is_rejected
test_non_string_description_is_rejected
test_name_must_match_directory
test_list_skills_rejects_invalid_skill
test_unlisted_alternate_license_is_rejected
test_noticed_alternate_license_is_accepted
test_multiline_description_is_accepted
printf 'validator tests: PASS\n'
