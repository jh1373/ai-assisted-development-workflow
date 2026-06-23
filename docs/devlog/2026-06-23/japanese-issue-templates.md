# Issueテンプレートの日本語化

## Summary

GitHub Issue作成時に使う `bug.md` と `task.md` を日本語化した。

## Context

このリポジトリは日本語で説明する新規プロジェクト向けAI駆動開発ワークフローである。
Issueテンプレートが英語のままだと、初心者が何を書けばよいか判断しにくく、リポジトリ全体の見せ方にも一貫性が出ない。

## Decision

以下を変更した。

- Issueテンプレート名、説明文、タイトル接頭辞を日本語化
- `bug.md` の入力項目を、不具合の再現と修正確認に必要な日本語表現へ変更
- `task.md` の入力項目を、目的、範囲、完了条件、確認方法が分かる日本語表現へ変更
- root側とstarter側のIssueテンプレートを同じ内容に統一
- 主要ファイルの役割説明に `bug.md` と `task.md` を個別に追記

## Verification

```text
bash scripts/check-docs.sh: passed
bash scripts/test-initialization-checker.sh: passed
./scripts/test-initialization-checker.ps1: passed
python scripts/test-project-structure.py: passed, 1 symlink test skipped because symlink creation is not permitted
node --check scripts/project-structure-viewer/app.js: passed
git diff --check: passed
```

## Follow-up

必要であれば、GitHub上の `bug` / `task` ラベルが存在するかを別タスクで確認する。
