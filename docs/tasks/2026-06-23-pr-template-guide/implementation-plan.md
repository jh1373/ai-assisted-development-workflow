# Implementation Plan: PRテンプレート説明ドキュメント追加

## Task

`.github/pull_request_template.md` の目的、思想、各項目の意味を初心者にも分かるように説明する。

## Background

PRテンプレート自体は存在しているが、初心者が「なぜ必要か」「いつ使うか」「各項目に何を書くか」を理解できる専用説明がなかった。
README、practical guide、team developmentにはPR運用への言及があるが、説明が分散している。

## Scope

- `docs/pull-request-template.md` を追加する
- `starter/docs/ai-workflow/pull-request-template.md` を追加する
- rootとstarterのPRテンプレートから説明ページへ案内する
- README、practical guide、team developmentから説明ページへリンクする
- starterのDirectory Mapに新規ファイルの役割説明を追加する
- 生成済み `starter/docs/DIRECTORY_MAP.md` を更新する

## Out of scope

- PRテンプレートのチェック項目そのものを大きく変更する
- GitHub branch protectionやPR必須運用を追加する
- 既存のWorkflow Mode定義を変更する

## Workflow Mode

Standard

理由:

ドキュメント中心の変更だが、GitHub運用、starter配布物、Project Structure Mapに影響するためMinimalではなくStandardで扱う。

## Directory Map impact

- `starter/docs/ai-workflow/pull-request-template.md` を追加する
- `starter/.github/pull_request_template.md` の説明先を追加する
- `starter/.ai-workflow/directory-map.json` に新規ファイルの役割説明を登録する
- `starter/docs/DIRECTORY_MAP.md` を再生成する

## Verification plan

- `bash scripts/check-docs.sh`
- `bash scripts/test-initialization-checker.sh`
- `./scripts/test-initialization-checker.ps1`
- `python scripts/test-project-structure.py`
- `node --check scripts/project-structure-viewer/app.js`
- `git diff --check`

## Security and Privacy

秘密情報、個人情報、認証情報を追加しない。
PRテンプレートの説明ではセキュリティ確認の例を扱うが、実在する秘密情報は記載しない。
