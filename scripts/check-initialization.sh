#!/usr/bin/env bash
set -u

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "$script_dir/.." && pwd)"
state_file="$project_root/.ai-workflow/project-state.conf"

emit() {
  printf '%s\n' "$1"
  exit 0
}

if [[ ! -e "$state_file" ]]; then
  emit "INITIALIZATION_CHECK_FAILED"
fi

if [[ ! -f "$state_file" || ! -r "$state_file" ]]; then
  emit "INITIALIZATION_CHECK_FAILED"
fi

normalized="$(tr -d '\r' < "$state_file")"

if [[ "$(printf '%s\n' "$normalized" | sed '/^$/d' | wc -l | tr -d ' ')" != "3" ]]; then
  emit "INITIALIZATION_INVALID"
fi

if printf '%s\n' "$normalized" | grep -Ev '^(schema_version|initialization_status|user_approved)=[^[:space:]]+$' >/dev/null; then
  emit "INITIALIZATION_INVALID"
fi

read_value() {
  local key="$1"
  local matches
  matches="$(printf '%s\n' "$normalized" | grep -E "^${key}=" || true)"
  if [[ "$(printf '%s\n' "$matches" | sed '/^$/d' | wc -l | tr -d ' ')" != "1" ]]; then
    return 1
  fi
  printf '%s' "${matches#*=}"
}

schema_version="$(read_value schema_version)" || emit "INITIALIZATION_INVALID"
initialization_status="$(read_value initialization_status)" || emit "INITIALIZATION_INVALID"
user_approved="$(read_value user_approved)" || emit "INITIALIZATION_INVALID"

if [[ "$schema_version" != "1" ]]; then
  emit "INITIALIZATION_INVALID"
fi

case "$initialization_status" in
  not_started)
    [[ "$user_approved" == "false" ]] || emit "INITIALIZATION_INVALID"
    if [[ -f "$project_root/docs/INITIALIZATION_REVIEW.md" ]] && grep -Fxq 'Initialization Decision: Ready' "$project_root/docs/INITIALIZATION_REVIEW.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    emit "INITIALIZATION_NOT_STARTED"
    ;;
  in_progress)
    [[ "$user_approved" == "false" ]] || emit "INITIALIZATION_INVALID"
    emit "INITIALIZATION_IN_PROGRESS"
    ;;
  revisit_required)
    [[ "$user_approved" == "false" ]] || emit "INITIALIZATION_INVALID"
    emit "INITIALIZATION_REVISIT_REQUIRED"
    ;;
  ready)
    [[ "$user_approved" == "true" ]] || emit "INITIALIZATION_INVALID"
    required_files=(
      "AGENTS.md"
      "docs/PROJECT_BRIEF.md"
      "docs/ROADMAP.md"
      "docs/PROJECT_STATUS.md"
      "docs/DIRECTORY_MAP.md"
      "docs/INITIALIZATION_REVIEW.md"
    )
    for relative_path in "${required_files[@]}"; do
      [[ -s "$project_root/$relative_path" ]] || emit "INITIALIZATION_INVALID"
    done
    if ! grep -Fxq 'Initialization Decision: Ready' "$project_root/docs/INITIALIZATION_REVIEW.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if grep -Fq 'Not initialized' "$project_root/AGENTS.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if ! grep -Eq '^- Initialization track: (Discovery|Build-ready)$' "$project_root/docs/PROJECT_BRIEF.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if grep -Fq 'Last confirmed by user: Not confirmed' "$project_root/docs/PROJECT_BRIEF.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if ! grep -Eq '^- Initialization track: (Discovery|Build-ready)$' "$project_root/docs/ROADMAP.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if grep -Fq 'Project Initialization: Not started' "$project_root/docs/PROJECT_STATUS.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    if ! grep -Eq '^Map Status: (Provisional|Verified)$' "$project_root/docs/DIRECTORY_MAP.md"; then
      emit "INITIALIZATION_INVALID"
    fi
    emit "INITIALIZATION_READY"
    ;;
  *)
    emit "INITIALIZATION_INVALID"
    ;;
esac
