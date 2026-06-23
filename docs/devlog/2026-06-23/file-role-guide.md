# ファイル名方針の明文化

## Summary

主要ファイル名の意味と、それぞれが担う役割を初心者向けに一覧化した。

## Context

このリポジトリは日本語で説明するポートフォリオ用途だが、ファイル名だけでは初心者が役割を判断しにくい。
そのため、主要ファイル名の意味と役割を日本語で確認できる一覧を用意した。

## Decision

追加した内容:

- `docs/file-role-guide.md`
- `starter/docs/ai-workflow/file-role-guide.md`
- READMEからの導線
- design-rationaleから命名方針説明を削除
- starter README上の導入先向け注意
- Project Structure Map上の役割説明

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
