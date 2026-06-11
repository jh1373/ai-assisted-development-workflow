# AGENTS.md Template

Use this file at the root of a project to define rules for AI coding agents.
Edit it to match the project before use.

## Project Rules

- Read this file before making changes.
- Read `README.md`, `docs/PROJECT_STATUS.md`, and the latest devlog before
  starting a non-trivial task.
- Run `git status --short --branch` before editing files.
- Do not overwrite or revert user changes unless explicitly instructed.
- Do not start implementation until the task goal, scope, out-of-scope items,
  and completion condition are clear.
- Ask for clarification when requirements are ambiguous.
- Keep changes limited to the requested task.
- Do not introduce new dependencies without approval.
- Do not put secrets, tokens, personal data, or internal URLs in committed files.

## Workflow

For normal work:

1. Restore context with `workflows/session-start.md`.
2. Write or update an implementation plan.
3. Implement in small, reviewable changes.
4. Run relevant tests, builds, or manual checks.
5. Complete `templates/completion-review.md`.
6. Write a devlog.
7. Update `docs/PROJECT_STATUS.md` when project state changes.

For high-risk work, use Strict mode.
See `docs/strict-mode.md`.

## Definition of Done

A task is complete only when:

- the requested behavior is implemented
- relevant verification has been run
- skipped checks are explained
- documentation is updated or explicitly marked unnecessary
- remaining risks are recorded
- the next session can resume from tracked files, not chat history

See `docs/definition-of-done.md`.

## Verification Commands

Replace these examples with project-specific commands.

```bash
npm test
npm run build
git diff --check
```

## Prohibited Actions

- Do not run destructive commands without explicit user approval.
- Do not commit generated secrets, logs, credentials, or private data.
- Do not make unrelated formatting or refactoring changes.
- Do not mark a task complete only because code was generated.
- Do not hide failed checks or unresolved risks.
