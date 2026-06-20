# Project Rules Example

## Project-specific Context

- Product goal: 献立提案の価値仮説を検証する
- Current maturity: Discovery
- Runtime and main stack: Provisional web application
- Verification commands: Project-specific commands will be fixed in the first implementation plan
- Deployment target: Deferred
- Security or privacy constraints: Do not collect or store personal data

## Discovery Boundaries

- Treat target users and monetization as hypotheses.
- Do not add authentication, billing, persistence, or public deployment in Phase 1.
- Do not send personal data to an AI API.
- Ask the user before replacing fixed sample data with an external AI service.

## Initialization Routing

- Run `workflows/session-start.md` at the start of a session.
- Continue normal task work only after `INITIALIZATION_READY`.
- Do not infer initialization state from project documents.
- Do not set `ready` without explicit user approval.

## Task Workflow After Initialization

- Select one task from ROADMAP and PROJECT_STATUS.
- Align scope and completion conditions before implementation.
- Keep Phase 1 work inside the confirmed Discovery boundaries.
- Record verification evidence and remaining hypotheses.
