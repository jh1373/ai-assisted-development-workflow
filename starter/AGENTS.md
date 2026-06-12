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
- Requirement Alignment First: do not implement when the user's intent, scope,
  constraints, or completion criteria are ambiguous.
- Before implementation, summarize your understanding, list unclear points,
  identify assumptions, and ask the user for confirmation when needed.
- Never silently fill gaps that could change product behavior, user experience,
  data handling, security, cost, or release scope.
- Keep changes limited to the requested task.
- Do not introduce new dependencies without approval.
- Do not put secrets, tokens, personal data, or internal URLs in committed files.
- Do not edit template files as task records. Create task records under
  `docs/tasks/YYYY-MM-DD-HHMM-task-name/`.

## Workflow

For normal work:

1. Restore context with `workflows/session-start.md`.
2. Align requirements with `templates/requirement-alignment.md` when the task is
   non-trivial or ambiguous.
3. Select the workflow mode. Default to Standard.
4. Downgrade to Minimal only when the task is small, reversible, low-risk, and
   does not affect behavior, data, security, cost, release scope, or production.
5. Upgrade to Strict when the task affects authentication, authorization,
   billing, personal data, data migration, production configuration, external
   dependencies, public release, architecture, or destructive actions.
6. State the reason whenever selecting Minimal or Strict.
7. Create or update task records under `docs/tasks/YYYY-MM-DD-HHMM-task-name/`.
8. Write or update `implementation-plan.md` in the task records folder.
9. Implement in small, reviewable changes.
10. Run relevant tests, builds, or manual checks.
11. Complete `completion-review.md` in the task records folder.
12. Run `workflows/session-end.md` at the end of the task. This includes
    devlog creation, PROJECT_STATUS update decision, and git commit decision.

Do not finish a task until `workflows/session-end.md` is complete, including
completion review, devlog, PROJECT_STATUS update decision, and git commit
decision.

For high-risk work, use Strict mode.
See `docs/ai-workflow/strict-mode.md`.

## Definition of Done

A task is complete only when:

- the requested behavior is implemented
- relevant verification has been run
- skipped checks are explained
- documentation is updated or explicitly marked unnecessary
- remaining risks are recorded
- the next session can resume from tracked files, not chat history

See `docs/ai-workflow/definition-of-done.md`.

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
