# docs READMEへの役割ガイド統合

## Summary

`docs/README.md` を新設し、docsの入口と主要ファイルの役割説明を統合した。

## Context

`docs/` には多くの説明文書があるが、フォルダ直下に入口となるREADMEが存在しなかった。
そのため、初心者が `docs/` を開いたときに、読む順番や各ファイルの役割を判断しにくい状態だった。

## Decision

以下の方針で整理した。

- `docs/README.md` をdocsの入口にする
- 旧 `docs/file-role-guide.md` の役割を `docs/README.md` に統合する
- starter側も `starter/docs/README.md` に統合する
- 旧 `starter/docs/ai-workflow/file-role-guide.md` は廃止する
- README、必須チェック、Project Structure Mapを新しい入口に合わせる

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

追加の整合性確認で、`starter/docs/README.md` の `docs/ai-workflow` 一覧に `team-development.md` だけが載っていないことを確認した。
導入先のdocs入口として全体を把握できるよう、`docs/ai-workflow/team-development.md` の行を追記した。

## Follow-up

現時点ではなし。
