#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checker="$repo_root/scripts/check-initialization.sh"
fixture="$(mktemp -d)"
trap 'rm -rf "$fixture"' EXIT

mkdir -p "$fixture/scripts"
cp "$checker" "$fixture/scripts/check-initialization.sh"

assert_result() {
  local expected="$1"
  local actual
  actual="$(bash "$fixture/scripts/check-initialization.sh")"
  if [[ "$actual" != "$expected" ]]; then
    printf 'Expected %s, got %s\n' "$expected" "$actual" >&2
    exit 1
  fi
}

write_state() {
  mkdir -p "$fixture/.ai-workflow"
  printf 'schema_version=1\ninitialization_status=%s\nuser_approved=%s\n' "$1" "$2" > "$fixture/.ai-workflow/project-state.conf"
}

assert_result "INITIALIZATION_CHECK_FAILED"

write_state not_started false
assert_result "INITIALIZATION_NOT_STARTED"

mkdir -p "$fixture/docs"
printf 'Initialization Decision: Ready\n' > "$fixture/docs/INITIALIZATION_REVIEW.md"
assert_result "INITIALIZATION_INVALID"
printf 'Initialization Decision: Not Ready\n' > "$fixture/docs/INITIALIZATION_REVIEW.md"

write_state in_progress false
assert_result "INITIALIZATION_IN_PROGRESS"

write_state revisit_required false
assert_result "INITIALIZATION_REVISIT_REQUIRED"

write_state ready false
assert_result "INITIALIZATION_INVALID"

printf 'schema_version=1\ninitialization_status=unknown\nuser_approved=false\n' > "$fixture/.ai-workflow/project-state.conf"
assert_result "INITIALIZATION_INVALID"

write_state READY true
assert_result "INITIALIZATION_INVALID"

write_state ready True
assert_result "INITIALIZATION_INVALID"

printf 'Schema_version=1\ninitialization_status=not_started\nuser_approved=false\n' > "$fixture/.ai-workflow/project-state.conf"
assert_result "INITIALIZATION_INVALID"

printf 'schema_version=2\ninitialization_status=not_started\nuser_approved=false\n' > "$fixture/.ai-workflow/project-state.conf"
assert_result "INITIALIZATION_INVALID"

printf 'schema_version=1\nschema_version=1\ninitialization_status=not_started\nuser_approved=false\n' > "$fixture/.ai-workflow/project-state.conf"
assert_result "INITIALIZATION_INVALID"

write_state ready true
assert_result "INITIALIZATION_INVALID"

mkdir -p "$fixture/docs"
printf '%s\n' '## Project-specific Context' 'Product goal: configured' '## Initialization Routing' '## Task Workflow After Initialization' > "$fixture/AGENTS.md"
printf '%s\n' '- Initialization track: Discovery' '- Last confirmed by user: 2026-06-20' > "$fixture/docs/PROJECT_BRIEF.md"
printf '%s\n' '- Initialization track: Discovery' '## Phase 1: Validation' > "$fixture/docs/ROADMAP.md"
printf 'Current phase: Discovery\n' > "$fixture/docs/PROJECT_STATUS.md"
printf 'Map Status: Provisional\n' > "$fixture/docs/DIRECTORY_MAP.md"
printf '%s\n' 'Initialization Decision: Ready' '- Approved by: User' '- Approved at: 2026-06-20' '- Confirmation summary: Approved for validation' > "$fixture/docs/INITIALIZATION_REVIEW.md"
assert_result "INITIALIZATION_READY"

printf '%s\n' '## Project-specific Context' 'Product goal: Not initialized' '## Initialization Routing' '## Task Workflow After Initialization' > "$fixture/AGENTS.md"
assert_result "INITIALIZATION_INVALID"
printf '%s\n' '## Project-specific Context' 'Product goal: configured' '## Initialization Routing' '## Task Workflow After Initialization' > "$fixture/AGENTS.md"

printf '%s\n' 'Map Status: Provisional' '[PROJECT_ROOT]/' > "$fixture/docs/DIRECTORY_MAP.md"
assert_result "INITIALIZATION_INVALID"
printf 'Map Status: Provisional\n' > "$fixture/docs/DIRECTORY_MAP.md"

printf '%s\n' 'Initialization Decision: Ready' '- Approved by:    ' '- Approved at: 2026-06-20' '- Confirmation summary: Approved for validation' > "$fixture/docs/INITIALIZATION_REVIEW.md"
assert_result "INITIALIZATION_INVALID"

printf 'Initialization Decision: Not Ready\n' > "$fixture/docs/INITIALIZATION_REVIEW.md"
assert_result "INITIALIZATION_INVALID"

rm -rf "$fixture"
mkdir -p "$fixture/scripts"
cp -R "$repo_root/examples/project-initialization/." "$fixture/"
cp "$checker" "$fixture/scripts/check-initialization.sh"
assert_result "INITIALIZATION_READY"

printf 'Initialization checker Bash tests passed.\n'
