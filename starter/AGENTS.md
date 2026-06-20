# AGENTS.md Template

Use this file at the root of a project to define rules for AI coding agents.
Edit it to match the project before use.

## Supported Scope

- This starter is for a new project being started with this workflow.
- Existing-project adoption is not supported.
- If this starter appears to have been copied into an existing project, stop
  before Project Initialization and tell the user that existing files may have
  been overwritten. Do not treat the existing project as a new project.

## Project Rules

- Read this file before making changes.
- Read `README.md`, `docs/PROJECT_STATUS.md`, `docs/DIRECTORY_MAP.md`, and
  the latest devlog before starting a non-trivial task.
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
- Do not edit `docs/DIRECTORY_MAP.md` directly. Edit
  `.ai-workflow/directory-map.json`, then regenerate the Markdown.

## Project-specific Context

Complete this section during Project Initialization. Do not turn hypotheses into
permanent rules.

- Product goal: Not initialized
- Current maturity: Not initialized
- Runtime and main stack: Not initialized
- Verification commands: Not initialized
- Deployment target: Not initialized
- Security or privacy constraints: Not initialized

## Initialization Routing

At the start of a session, begin with `workflows/session-start.md`. Its Step 0
runs exactly one initialization checker for the current environment:

```bash
bash scripts/check-initialization.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-initialization.ps1
```

Follow the exact output. Do not infer initialization state from prose or from
whether the project looks partially configured.

- `INITIALIZATION_NOT_STARTED`: start `workflows/project-initialization.md`.
- `INITIALIZATION_IN_PROGRESS`: continue the existing initialization records.
- `INITIALIZATION_READY`: normal task work may begin.
- `INITIALIZATION_REVISIT_REQUIRED`: review only the affected project assumptions
  and obtain renewed user approval.
- `INITIALIZATION_INVALID`: report the inconsistent state. Do not restart or mark
  initialization complete.
- `INITIALIZATION_CHECK_FAILED`: report the checker failure. Do not guess.

Only set `initialization_status=ready` and `user_approved=true` after explicit
user approval recorded in `docs/INITIALIZATION_REVIEW.md`.

Treat `Confirmed`, `Hypothesis`, `Unknown`, and `Deferred` as different states.
Never implement a hypothesis as if the user had confirmed it.

## Project Structure Routing

After `INITIALIZATION_READY`, run exactly one structure checker for the current
environment:

```bash
bash scripts/check-directory-map.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-directory-map.ps1
```

Follow the exact output:

- `DIRECTORY_MAP_VERIFIED`: normal task selection may continue.
- `DIRECTORY_MAP_PROVISIONAL`: continue only for the first project construction
  task and plan verification before normal feature work.
- `DIRECTORY_MAP_DRIFT_DETECTED`: inspect the diff and repair the map before
  implementation.
- `DIRECTORY_MAP_INVALID`: report the invalid tracked structure records.
- `DIRECTORY_MAP_CHECK_FAILED`: report the tool or environment failure. Do not
  infer the structure state.

The source of truth is `.ai-workflow/directory-map.json` plus the verified path
snapshot. The localhost viewer is read-only and optional. Never assign a guessed
role merely to make verification pass.

Project Atlas is the default human-facing view. Before reading the full file
tree, use its area map, Guided Tour, and Task Lens to understand the project.

When creating or renaming a file, update its File Passport in the same task.
Entry points and core files require an explicit passport with a beginner summary,
responsibility, non-responsibilities, change triggers, dependencies, area, and
evidence. A support file may inherit an approved parent passport only when that
description is accurate; record that decision in the implementation plan. Never
infer semantics from file contents or names after the fact merely to raise the
coverage score.

## Task Workflow After Initialization

For normal work:

1. Run `workflows/session-start.md`; continue only when its Step 0 returns
   `INITIALIZATION_READY`. Do not run the checker a second time in the same
   session unless the initialization state was intentionally changed.
2. Continue only after the Project Structure Gate returns `DIRECTORY_MAP_VERIFIED`,
   except for the explicitly scoped first construction task while Provisional.
3. After the task is selected, use Project Atlas and its Task Lens, then
   `docs/DIRECTORY_MAP.md`, to identify the areas, responsibilities, boundaries,
   flows, and files to inspect before planning.
4. Align requirements with `templates/requirement-alignment.md` when the task is
   non-trivial or ambiguous.
5. Select the workflow mode. Default to Standard.
6. Downgrade to Minimal only when the task is small, reversible, low-risk, and
   does not affect behavior, data, security, cost, release scope, or production.
7. Upgrade to Strict when the task affects authentication, authorization,
   billing, personal data, data migration, production configuration, external
   dependencies, public release, architecture, or destructive actions.
8. State the reason whenever selecting Minimal or Strict.
9. Create or update task records under `docs/tasks/YYYY-MM-DD-HHMM-task-name/`.
10. Write or update `implementation-plan.md` in the task records folder,
   including Directory Context and Workflow Mode.
11. Implement in small, reviewable changes.
12. Run relevant tests, builds, or manual checks.
13. Complete `completion-review.md` in the task records folder.
14. Run `workflows/session-end.md` at the end of the task. This includes
    devlog creation, PROJECT_STATUS update decision, DIRECTORY_MAP update
    decision, and git commit decision.

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
- DIRECTORY_MAP impact has been checked and recorded
- the project structure checker is Verified, or Provisional is explicitly
  justified for the first construction task
- remaining risks are recorded
- the next session can resume from tracked files, not chat history

See `docs/ai-workflow/definition-of-done.md`.

## Verification Commands

Replace these examples with project-specific commands.

```bash
[project-specific test command]
[project-specific build command]
git diff --check
```

## Prohibited Actions

- Do not run destructive commands without explicit user approval.
- Do not commit generated secrets, logs, credentials, or private data.
- Do not make unrelated formatting or refactoring changes.
- Do not mark a task complete only because code was generated.
- Do not hide failed checks or unresolved risks.
