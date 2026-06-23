# Completion Review: docs READMEへの役割ガイド統合

## Summary

`docs/README.md` を新設し、docsの読み方、目的別の参照先、主要ファイルの役割一覧を統合した。
あわせてstarter側も `starter/docs/README.md` に統合し、旧 `file-role-guide.md` は廃止した。

## Workflow Mode

Standard

理由:

ドキュメント中心の変更だが、入口文書、starter配布物、構成マップ、必須チェックに影響するため。

## Scope check

- [x] `docs/README.md` を追加した
- [x] `docs/file-role-guide.md` を削除した
- [x] `starter/docs/README.md` を追加した
- [x] `starter/docs/ai-workflow/file-role-guide.md` を削除した
- [x] README内の旧リンクを `docs/README.md` に更新した
- [x] starter README内の旧リンクを `docs/README.md` に更新した
- [x] `scripts/check-docs.sh` の必須ファイル一覧を更新した
- [x] starterのProject Structure Map正本と生成文書を更新した

## Changed files

- `README.md`
- `docs/README.md`
- `docs/file-role-guide.md`
- `starter/README.md`
- `starter/docs/README.md`
- `starter/docs/ai-workflow/file-role-guide.md`
- `starter/.ai-workflow/directory-map.json`
- `starter/docs/DIRECTORY_MAP.md`
- `scripts/check-docs.sh`
- `docs/tasks/2026-06-23-docs-readme-integration/implementation-plan.md`
- `docs/tasks/2026-06-23-docs-readme-integration/completion-review.md`
- `docs/devlog/2026-06-23/docs-readme-integration.md`

## Verification

```text
bash scripts/check-docs.sh: passed
bash scripts/test-initialization-checker.sh: passed
./scripts/test-initialization-checker.ps1: passed
python scripts/test-project-structure.py: passed, 1 symlink test skipped because symlink creation is not permitted
node --check scripts/project-structure-viewer/app.js: passed
git diff --check: passed
```

## Follow-up correction

追加の整合性確認で、`starter/docs/README.md` に `docs/ai-workflow/team-development.md` の案内が漏れていることを確認した。
starter側のdocs入口として案内粒度を揃えるため、該当行を追記した。

## Security and Privacy

- [x] 秘密情報、個人情報、認証情報を追加していない
- [x] ログやスクリーンショットを追加していない

## Remaining risk

なし。
