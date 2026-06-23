# Implementation Plan: ファイル名方針の明文化

## Task

英語ファイル名を維持する理由と、初心者向けの日本語対応表をドキュメント化する。

## Background

このリポジトリは日本語で説明するポートフォリオ用途だが、ファイル名とディレクトリ名は英語中心になっている。
公開リポジトリ、GitHub Actions、CLI、AIエージェント、スクリプト運用を考えると英語名は維持する方が安全である。
一方で、初心者が英語名だけを見て役割を判断するのは難しいため、日本語の説明導線を強化する。

## Scope

- `docs/file-naming-policy.md` を追加する
- `starter/docs/ai-workflow/file-naming-policy.md` を追加する
- READMEからファイル名方針へリンクする
- design-rationaleに「ファイル名は英語、説明は日本語」の設計理由を追加する
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
