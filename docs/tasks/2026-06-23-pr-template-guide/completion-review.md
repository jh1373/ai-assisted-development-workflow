# Completion Review: PRテンプレート説明ドキュメント追加

## Summary

`.github/pull_request_template.md` の目的、使うタイミング、各項目の意味、初心者向けの記入例を説明するドキュメントを追加した。

## Workflow Mode

Standard

理由:

GitHub運用とstarter配布物に影響する説明追加であり、README、関連ガイド、Project Structure Mapとの整合性確認が必要だったため。

## Scope check

- [x] PRテンプレートの説明に限定した
- [x] PRテンプレート本体の構造は大きく変更していない
- [x] root側とstarter側の説明を揃えた
- [x] starterのDirectory Mapに新規ファイルの役割説明を追加した

## Changed files

- `docs/pull-request-template.md`
- `starter/docs/ai-workflow/pull-request-template.md`
- `.github/pull_request_template.md`
- `starter/.github/pull_request_template.md`
- `README.md`
- `docs/practical-guide.md`
- `docs/team-development.md`
- `starter/README.md`
- `starter/docs/ai-workflow/practical-guide.md`
- `starter/docs/ai-workflow/team-development.md`
- `starter/.ai-workflow/directory-map.json`
- `starter/docs/DIRECTORY_MAP.md`
- `docs/devlog/2026-06-23/pr-template-guide.md`

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
- [x] サンプルは架空のファイル名と一般的な確認項目だけを使った
- [x] ログやスクリーンショットは追加していない

## Remaining risk

なし。
