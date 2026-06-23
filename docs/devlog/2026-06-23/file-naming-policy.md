# ファイル名方針の明文化

## Summary

ファイル名とディレクトリ名は英語で維持し、初心者向けの意味説明を日本語で補う方針を明文化した。

## Context

このリポジトリは日本語で説明するポートフォリオ用途だが、GitHub、CI、CLI、AIエージェント、スクリプトで扱うファイルが多い。
日本語ファイル名に寄せると一見分かりやすく見えるが、公開リポジトリとしての扱いやすさや自動化の安定性が下がる可能性がある。

## Decision

次の方針を採用した。

```text
ファイル名とディレクトリ名: 英語
本文と説明: 日本語
初心者向けの意味説明: README、DIRECTORY_MAP、localhost画面で補う
```

追加した内容:

- `docs/file-naming-policy.md`
- `starter/docs/ai-workflow/file-naming-policy.md`
- READMEからの導線
- design-rationale上の設計理由
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
