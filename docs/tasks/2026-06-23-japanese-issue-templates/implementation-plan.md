# Implementation Plan: Issueテンプレートの日本語化

## Task

GitHub Issue作成時に表示される `bug.md` と `task.md` の内容を、日本語で理解しやすい表現に変更する。

## Background

このリポジトリは日本語で説明する新規プロジェクト向けAI駆動開発ワークフローである。
Issueテンプレートだけ英語のままだと、初心者が何を書けばよいか判断しにくく、リポジトリ全体の初心者向け設計ともずれる。

## Scope

- `.github/ISSUE_TEMPLATE/bug.md` を日本語化する
- `.github/ISSUE_TEMPLATE/task.md` を日本語化する
- `starter/.github/ISSUE_TEMPLATE/bug.md` を同じ方針で日本語化する
- `starter/.github/ISSUE_TEMPLATE/task.md` を同じ方針で日本語化する
- `docs/file-role-guide.md` と `starter/docs/ai-workflow/file-role-guide.md` に、各Issueテンプレートの役割を個別に記載する

## Out of scope

- Issueテンプレートの種類追加
- GitHubラベルの新規作成
- GitHub ActionsやPRテンプレートの変更

## Workflow Mode

Standard

理由:

ドキュメント中心の変更だが、GitHub上でユーザーが直接見る入力フォームと、starter配布物の使いやすさに影響するため。

## Verification plan

- `bash scripts/check-docs.sh`
- `bash scripts/test-initialization-checker.sh`
- `./scripts/test-initialization-checker.ps1`
- `python scripts/test-project-structure.py`
- `node --check scripts/project-structure-viewer/app.js`
- `git diff --check`

## Security and Privacy

秘密情報、個人情報、認証情報を追加しない。
