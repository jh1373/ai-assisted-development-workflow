# Implementation Plan: ファイル名方針の明文化

## Task

主要ファイル名の意味と、それぞれが担う役割を初心者向けに一覧化する。

## Background

このリポジトリは日本語で説明するポートフォリオ用途だが、ファイル名だけでは初心者が役割を判断しにくい。
そのため、主要ファイル名の意味と役割を日本語で確認できる一覧を用意する。

## Scope

- `docs/file-naming-policy.md` を追加する
- `starter/docs/ai-workflow/file-naming-policy.md` を追加する
- READMEからファイル名方針へリンクする
- design-rationaleへ追加した命名方針説明は削除し、主要ファイル一覧への導線に留める
- starter READMEに導入先向けの注意を追加する
- starterのProject Structure Mapに新規説明ファイルの役割を登録する
- `starter/docs/DIRECTORY_MAP.md` を再生成する

## Out of scope

- 既存ファイル名の日本語化
- 既存ファイル名の大規模リネーム
- GitHub Actionsやスクリプトの実行方式変更

## Workflow Mode

Standard

理由:

ドキュメント中心だが、リポジトリ全体の命名方針とstarter配布物に関わるため。

## Verification plan

- `bash scripts/check-docs.sh`
- `bash scripts/test-initialization-checker.sh`
- `./scripts/test-initialization-checker.ps1`
- `python scripts/test-project-structure.py`
- `node --check scripts/project-structure-viewer/app.js`
- `git diff --check`

## Security and Privacy

秘密情報、個人情報、認証情報を追加しない。
