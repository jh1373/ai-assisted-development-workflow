# Completion Review: Issueテンプレートの日本語化

## Summary

GitHub Issue作成時に表示される `bug.md` と `task.md` を日本語化した。
root側とstarter側の内容を揃え、主要ファイルの役割説明にも各Issueテンプレートの役割を追記した。

## Workflow Mode

Standard

理由:

ドキュメント中心の変更だが、GitHub上でユーザーが直接見る入力フォームと、starter配布物の使いやすさに影響するため。

## Scope check

- [x] `.github/ISSUE_TEMPLATE/bug.md` を日本語化した
- [x] `.github/ISSUE_TEMPLATE/task.md` を日本語化した
- [x] `starter/.github/ISSUE_TEMPLATE/bug.md` を日本語化した
- [x] `starter/.github/ISSUE_TEMPLATE/task.md` を日本語化した
- [x] `docs/file-role-guide.md` にIssueテンプレートごとの役割を追記した
- [x] `starter/docs/ai-workflow/file-role-guide.md` にIssueテンプレートごとの役割を追記した

## Changed files

- `.github/ISSUE_TEMPLATE/bug.md`
- `.github/ISSUE_TEMPLATE/task.md`
- `starter/.github/ISSUE_TEMPLATE/bug.md`
- `starter/.github/ISSUE_TEMPLATE/task.md`
- `docs/file-role-guide.md`
- `starter/docs/ai-workflow/file-role-guide.md`
- `docs/tasks/2026-06-23-japanese-issue-templates/implementation-plan.md`
- `docs/tasks/2026-06-23-japanese-issue-templates/completion-review.md`
- `docs/devlog/2026-06-23/japanese-issue-templates.md`

## Verification

```text
bash scripts/check-docs.sh: passed
bash scripts/test-initialization-checker.sh: passed
./scripts/test-initialization-checker.ps1: passed
python scripts/test-project-structure.py: passed, 1 symlink test skipped because symlink creation is not permitted
node --check scripts/project-structure-viewer/app.js: passed
git diff --check: passed
```

## Security and Privacy

- [x] 秘密情報、個人情報、認証情報を追加していない
- [x] ログやスクリーンショットを追加していない

## Remaining risk

GitHubラベル `bug` と `task` がリポジトリ上に存在しない場合、Issue作成時にラベルが自動付与されない可能性がある。
ただし、今回の変更はテンプレート本文の日本語化であり、ラベル管理は範囲外。
