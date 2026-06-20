#!/usr/bin/env bash
set -u

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$script_dir/project-structure.py" validate --require-generated "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$script_dir/project-structure.py" validate --require-generated "$@"
fi

printf '%s\n' 'DIRECTORY_MAP_CHECK_FAILED'
exit 0
