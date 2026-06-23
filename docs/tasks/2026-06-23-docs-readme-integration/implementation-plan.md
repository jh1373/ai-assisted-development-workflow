# Implementation Plan: docs READMEへの役割ガイド統合

## Task

`docs/file-role-guide.md` を `docs/README.md` に統合し、`docs/` フォルダの入口を明確にする。
starter側も同じ方針で `starter/docs/README.md` に統合する。

## Background

`docs/` には多くの説明文書があるが、フォルダ直下に入口となるREADMEが存在しなかった。
一方で、主要ファイルの役割説明は `file-role-guide.md` に分かれていたため、初心者が最初に何を見るべきか分散していた。

## Scope

- `docs/README.md` を追加する
- `docs/file-role-guide.md` を削除する
- `starter/docs/README.md` を追加する
- `starter/docs/ai-workflow/file-role-guide.md` を削除する
- root READMEのリンクと構成例を更新する
- starter READMEのリンクを更新する
- `scripts/check-docs.sh` の必須ファイル一覧を更新する
- `starter/.ai-workflow/directory-map.json` を更新する
- `starter/docs/DIRECTORY_MAP.md` を再生成する

## Out of scope

- 過去の作業記録に残っている旧ファイル名の履歴修正
- docs全体の内容再設計
- Project Structure MapのUI変更

## Workflow Mode

Standard

理由:

ドキュメント中心の変更だが、入口文書、starter配布物、構成マップ、必須チェックに影響するため。

## Verification plan

- `bash scripts/check-docs.sh`
- `bash scripts/test-initialization-checker.sh`
- `./scripts/test-initialization-checker.ps1`
- `python scripts/test-project-structure.py`
- `node --check scripts/project-structure-viewer/app.js`
- `git diff --check`

## Security and Privacy

秘密情報、個人情報、認証情報を追加しない。
