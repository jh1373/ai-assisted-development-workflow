#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "starter/README.md"
  "starter/AGENTS.md"
  "starter/docs/PROJECT_STATUS.md"
  "starter/docs/ROADMAP.md"
  "starter/docs/DIRECTORY_MAP.md"
  "starter/docs/adr/.gitkeep"
  "starter/docs/devlog/.gitkeep"
  "starter/docs/tasks/.gitkeep"
  "starter/docs/ai-workflow/principles.md"
  "starter/docs/ai-workflow/design-rationale.md"
  "starter/docs/ai-workflow/adr-guidelines.md"
  "starter/docs/ai-workflow/task-records.md"
  "starter/docs/ai-workflow/requirement-alignment.md"
  "starter/templates/requirement-alignment.md"
  "starter/templates/implementation-plan.md"
  "starter/templates/completion-review.md"
  "starter/workflows/session-start.md"
  "starter/workflows/session-end.md"
  "starter/.github/pull_request_template.md"
  "examples/devlog/README.md"
  "examples/devlog/standard-task-devlog.md"
  "docs/principles.md"
  "docs/design-rationale.md"
  "docs/adr-guidelines.md"
  "docs/task-records.md"
  "docs/tasks/.gitkeep"
  "docs/requirement-alignment.md"
  "docs/practical-guide.md"
  "docs/quality-gates.md"
  "docs/team-development.md"
  "docs/definition-of-done.md"
  "docs/anti-patterns.md"
  "docs/strict-mode.md"
  "docs/security.md"
  "templates/AGENTS.md"
  "templates/requirement-alignment.md"
  "templates/implementation-plan.md"
  "templates/completion-review.md"
  "templates/devlog.md"
  "templates/directory-map.md"
  "templates/adr.md"
  "templates/security-review.md"
  "templates/rollback-plan.md"
  ".github/pull_request_template.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [[ ! -s "$file" ]]; then
    echo "Missing or empty required file: $file" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

echo "Checking for unresolved template placeholders in published docs..."
if grep -RIn --exclude-dir='.git' --include='*.md' \
  -e 'TODO' \
  -e 'TBD' \
  -e 'ここに' \
  docs README.md; then
  echo "Unresolved placeholder found in published documentation." >&2
  exit 1
fi

echo "Checking for common secret-like strings..."
if grep -RIn --exclude-dir='.git' --include='*.md' --include='*.yml' --include='*.yaml' --include='*.sh' \
  -E '(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----)' \
  .; then
  echo "Potential secret found. Remove it or replace it with a safe example." >&2
  exit 1
fi

echo "Checking markdown link targets for local files..."
python_bin=""
if command -v python3 >/dev/null 2>&1; then
  python_bin="python3"
elif command -v python >/dev/null 2>&1; then
  python_bin="python"
else
  echo "python3 or python is required for local markdown link checks." >&2
  exit 1
fi

"$python_bin" - <<'PY'
from pathlib import Path
import re
import sys

root = Path(".")
errors = []
pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

for path in root.rglob("*.md"):
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    for match in pattern.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "://" in target:
            continue
        clean = target.split("#", 1)[0]
        if not clean:
            continue
        resolved = (path.parent / clean).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{path}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path}: missing link target: {target}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
PY

echo "Documentation checks passed."
