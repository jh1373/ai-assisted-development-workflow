# PRテンプレート説明ドキュメント追加

## Summary

PRテンプレートの目的と使い方を初心者にも分かるように説明する専用ドキュメントを追加した。

## Context

`.github/pull_request_template.md` は、AI駆動開発において変更範囲、検証結果、セキュリティ確認、残るリスクをPR本文に残す重要な品質ゲートである。
しかし、既存ドキュメントでは「PRテンプレートを使うと確認項目を揃えられる」という説明に留まり、初心者が各項目の意味を理解するには弱かった。

## Decision

root側には `docs/pull-request-template.md`、starter側には `starter/docs/ai-workflow/pull-request-template.md` を追加した。

設計判断:

- PRテンプレート本体には長い説明を入れず、説明ドキュメントへのリンクだけを追加した
- root側とstarter側の説明を揃え、導入先プロジェクトにも説明が渡るようにした
- mainへ直接pushする場合はテンプレートが自動発動しないことを明記した
- `docs/tasks/` は実成果物ではなくタスク記録の置き場であることを説明内でも明記した
- starterのProject Structure Mapに新規ファイルの役割説明を登録した

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

現時点ではなし。
