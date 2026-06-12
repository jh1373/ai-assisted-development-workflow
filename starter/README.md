# AI-assisted Development Starter

このディレクトリは、既存プロジェクトへそのままコピーして使うための導入パッケージです。

## 使い方

`starter/` の中身を、導入したいプロジェクトのルートにコピーします。

コピー後の構成:

```text
AGENTS.md
docs/
  PROJECT_STATUS.md
  ROADMAP.md
  ai-workflow/
  devlog/
  adr/
templates/
workflows/
.github/
```

## AIに最初に読ませるもの

AIエージェントには、まずルートの `AGENTS.md` を読ませます。

次に、必要に応じて以下を読ませます。

- `docs/ai-workflow/principles.md`
- `docs/ai-workflow/requirement-alignment.md`
- `docs/ai-workflow/workflow-modes.md`
- `docs/ai-workflow/quality-gates.md`
- `workflows/session-start.md`

## 最初の作業で使うもの

通常は次の順番で使います。

1. `docs/PROJECT_STATUS.md` を更新する
2. `templates/requirement-alignment.md` で認識合わせを行う
3. `templates/implementation-plan.md` で実装計画を作る
4. `workflows/session-start.md` に沿って作業を開始する
5. `templates/completion-review.md` で完了前レビューを行う
6. `templates/devlog.md` で判断理由を残す

## 注意

- `AGENTS.md` はプロジェクトに合わせて編集してください。
- `PROJECT_STATUS.md` と `ROADMAP.md` は導入時に現状へ書き換えてください。
- 認識合わせが終わるまで、実装に進まないでください。
- デフォルトのworkflow modeはStandardです。
- 認証、権限、課金、個人情報、本番設定、公開リリースに触れる場合はStrict modeに上げます。
