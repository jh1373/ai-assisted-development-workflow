#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "README.md"
  "starter/README.md"
  "starter/AGENTS.md"
  "starter/.ai-workflow/project-state.conf"
  "starter/.ai-workflow/directory-map.json"
  "starter/.ai-workflow/directory-map.ignore"
  "starter/docs/PROJECT_BRIEF.md"
  "starter/docs/INITIALIZATION_REVIEW.md"
  "starter/docs/PROJECT_STATUS.md"
  "starter/docs/ROADMAP.md"
  "starter/docs/DIRECTORY_MAP.md"
  "starter/docs/project-structure-map.md"
  "starter/docs/adr/.gitkeep"
  "starter/docs/devlog/.gitkeep"
  "starter/docs/tasks/.gitkeep"
  "starter/docs/ai-workflow/principles.md"
  "starter/docs/ai-workflow/design-rationale.md"
  "starter/docs/ai-workflow/adr-guidelines.md"
  "starter/docs/ai-workflow/task-records.md"
  "starter/docs/ai-workflow/requirement-alignment.md"
  "starter/templates/requirement-alignment.md"
  "starter/templates/project-brief.md"
  "starter/templates/initialization-review.md"
  "starter/templates/implementation-plan.md"
  "starter/templates/completion-review.md"
  "starter/workflows/session-start.md"
  "starter/workflows/session-end.md"
  "starter/workflows/project-initialization.md"
  "starter/scripts/check-initialization.sh"
  "starter/scripts/check-initialization.ps1"
  "starter/scripts/check-directory-map.sh"
  "starter/scripts/check-directory-map.ps1"
  "starter/scripts/project-structure.py"
  "starter/scripts/project-structure-viewer/index.html"
  "starter/scripts/project-structure-viewer/app.js"
  "starter/scripts/project-structure-viewer/styles.css"
  "starter/.github/workflows/project-structure-check.yml"
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
  "docs/project-structure-map.md"
  "templates/AGENTS.md"
  "templates/project-brief.md"
  "templates/initialization-review.md"
  "templates/requirement-alignment.md"
  "templates/implementation-plan.md"
  "templates/completion-review.md"
  "templates/devlog.md"
  "templates/directory-map.md"
  "templates/adr.md"
  "templates/security-review.md"
  "templates/rollback-plan.md"
  "workflows/project-initialization.md"
  "scripts/check-initialization.sh"
  "scripts/check-initialization.ps1"
  "scripts/test-initialization-checker.sh"
  "scripts/test-initialization-checker.ps1"
  "scripts/check-directory-map.sh"
  "scripts/check-directory-map.ps1"
  "scripts/project-structure.py"
  "scripts/project-structure-viewer/index.html"
  "scripts/project-structure-viewer/app.js"
  "scripts/project-structure-viewer/styles.css"
  "scripts/test-project-structure.py"
  "examples/project-initialization/README.md"
  "examples/project-initialization/docs/PROJECT_BRIEF.md"
  "examples/project-initialization/docs/INITIALIZATION_REVIEW.md"
  "examples/project-initialization/docs/ROADMAP.md"
  "examples/project-initialization/docs/PROJECT_STATUS.md"
  "examples/project-initialization/docs/DIRECTORY_MAP.md"
  "examples/project-initialization/AGENTS.md"
  "examples/project-initialization/.ai-workflow/project-state.conf"
  "examples/project-initialization/.ai-workflow/directory-map.json"
  "examples/project-initialization/.ai-workflow/directory-map.ignore"
  "examples/react-app/.ai-workflow/directory-map.json"
  "examples/react-app/.ai-workflow/directory-map.ignore"
  "examples/react-app/docs/DIRECTORY_MAP.md"
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

echo "Checking synchronized initialization assets..."
sync_pairs=(
  "templates/AGENTS.md:starter/AGENTS.md"
  "workflows/project-initialization.md:starter/workflows/project-initialization.md"
  "templates/project-brief.md:starter/templates/project-brief.md"
  "templates/initialization-review.md:starter/templates/initialization-review.md"
  "scripts/check-initialization.sh:starter/scripts/check-initialization.sh"
  "scripts/check-initialization.ps1:starter/scripts/check-initialization.ps1"
  "scripts/check-directory-map.sh:starter/scripts/check-directory-map.sh"
  "scripts/check-directory-map.ps1:starter/scripts/check-directory-map.ps1"
  "scripts/project-structure.py:starter/scripts/project-structure.py"
  "scripts/project-structure-viewer/index.html:starter/scripts/project-structure-viewer/index.html"
  "scripts/project-structure-viewer/app.js:starter/scripts/project-structure-viewer/app.js"
  "scripts/project-structure-viewer/styles.css:starter/scripts/project-structure-viewer/styles.css"
  "docs/project-structure-map.md:starter/docs/project-structure-map.md"
  "docs/principles.md:starter/docs/ai-workflow/principles.md"
  "docs/design-rationale.md:starter/docs/ai-workflow/design-rationale.md"
  "docs/quality-gates.md:starter/docs/ai-workflow/quality-gates.md"
  "docs/ai-human-boundary.md:starter/docs/ai-workflow/ai-human-boundary.md"
  "docs/review-checklist.md:starter/docs/ai-workflow/review-checklist.md"
  "docs/anti-patterns.md:starter/docs/ai-workflow/anti-patterns.md"
  "docs/requirement-alignment.md:starter/docs/ai-workflow/requirement-alignment.md"
  "docs/task-records.md:starter/docs/ai-workflow/task-records.md"
)

for pair in "${sync_pairs[@]}"; do
  left="${pair%%:*}"
  right="${pair#*:}"
  if ! cmp -s "$left" "$right"; then
    echo "Synchronized files differ: $left and $right" >&2
    exit 1
  fi
done

expected_state=$'schema_version=1\ninitialization_status=not_started\nuser_approved=false'
actual_state="$(tr -d '\r' < starter/.ai-workflow/project-state.conf)"
if [[ "$actual_state" != "$expected_state" ]]; then
  echo "Starter initialization state must remain not_started and unapproved." >&2
  exit 1
fi

if ! grep -Fq '## Initialization Routing' starter/AGENTS.md; then
  echo "starter/AGENTS.md is missing Initialization Routing." >&2
  exit 1
fi

scope_files=(
  "README.md"
  "starter/README.md"
  "docs/adoption-guide.md"
  "workflows/project-initialization.md"
  "starter/workflows/project-initialization.md"
)

for file in "${scope_files[@]}"; do
  if ! grep -Fq '新規プロジェクト専用' "$file"; then
    echo "New-project-only scope is missing from: $file" >&2
    exit 1
  fi
done

if ! grep -Fq 'Existing-project adoption is not supported.' starter/AGENTS.md; then
  echo "starter/AGENTS.md must stop unsupported existing-project adoption." >&2
  exit 1
fi

if ! grep -Fq '### 0. Initialization Gateを確認する' starter/workflows/session-start.md; then
  echo "starter session-start is missing the Initialization Gate." >&2
  exit 1
fi

if ! grep -Fq '### 0.5. Project Structure Gateを確認する' starter/workflows/session-start.md; then
  echo "starter session-start is missing the Project Structure Gate." >&2
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
if grep -RIn --exclude-dir='.git' --include='*.md' --include='*.json' --include='*.js' --include='*.html' --include='*.yml' --include='*.yaml' --include='*.sh' --include='*.ps1' --include='*.conf' \
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

echo "Checking starter Project Structure Map..."
structure_result="$($python_bin starter/scripts/project-structure.py --root starter validate)"
if [[ "$structure_result" != "DIRECTORY_MAP_PROVISIONAL" ]]; then
  echo "Starter structure must remain provisional, got: $structure_result" >&2
  exit 1
fi

"$python_bin" starter/scripts/project-structure.py --root starter generate --check
"$python_bin" scripts/project-structure.py --root examples/react-app generate --check

echo "Documentation checks passed."
