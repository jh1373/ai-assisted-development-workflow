#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 1 ]]; then
  echo "Usage: bash scripts/create-new-project.sh /path/to/new-project" >&2
  exit 2
fi

normalize_target_path() {
  local input="$1"

  if [[ "$input" =~ ^([A-Za-z]):[\\/](.*)$ ]]; then
    local drive="${BASH_REMATCH[1],,}"
    local rest="${BASH_REMATCH[2]//\\//}"
    if [[ -d "/mnt/$drive" ]]; then
      printf '/mnt/%s/%s' "$drive" "$rest"
      return
    fi
  fi

  printf '%s' "$input"
}

target_input="$(normalize_target_path "$1")"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/.." && pwd -P)"
starter_dir="$repo_root/starter"

if [[ ! -d "$starter_dir" ]]; then
  echo "starter directory was not found: $starter_dir" >&2
  exit 1
fi

if [[ -e "$target_input" && ! -d "$target_input" ]]; then
  echo "Target path is a file: $target_input" >&2
  exit 1
fi

if [[ -d "$target_input" ]]; then
  unexpected_item="$(find "$target_input" -mindepth 1 -maxdepth 1 ! -name '.git' -print -quit)"
  if [[ -n "$unexpected_item" ]]; then
    echo "Target directory must be empty, or contain only .git: $target_input" >&2
    exit 1
  fi
else
  mkdir -p "$target_input"
fi

target_dir="$(cd -- "$target_input" && pwd -P)"

cp -a "$starter_dir"/. "$target_dir"/

checker="$target_dir/scripts/check-initialization.sh"
if [[ ! -f "$checker" ]]; then
  echo "Initialization checker was not copied: $checker" >&2
  exit 1
fi

initialization_result="$(bash "$checker")"

cat <<EOF

AI-assisted development workflow was installed.
Project: $target_dir
Initialization check: $initialization_result

Next steps:
1. cd "$target_dir"
2. Open AGENTS.md
3. Start workflows/project-initialization.md
4. Do not start normal tasks until INITIALIZATION_READY
EOF
