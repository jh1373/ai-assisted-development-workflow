# AI-assisted Development Starter

このディレクトリは、既存プロジェクトへそのままコピーして使うための導入パッケージです。

## 使い方

`starter/` の中身を、導入したいプロジェクトのルートにコピーします。

`.github/` は隠しディレクトリです。
コピー時に漏れないようにしてください。

Bash:

```bash
cp -R starter/. /path/to/project/
```

PowerShell:

```powershell
Copy-Item -Path .\starter\* -Destination C:\path\to\project -Recurse -Force
Copy-Item -Path .\starter\.github -Destination C:\path\to\project -Recurse -Force
```

コピー後の構成:

```text
AGENTS.md
docs/
  PROJECT_STATUS.md
  ROADMAP.md
  ai-workflow/
  tasks/
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
- `docs/ai-workflow/task-artifacts.md`
- `docs/ai-workflow/workflow-modes.md`
- `docs/ai-workflow/quality-gates.md`
- `docs/ai-workflow/adr-guidelines.md`
- `workflows/session-start.md`

## 最初の作業で使うもの

通常は次の順番で使います。

1. `workflows/session-start.md` に沿って現在地を復元する
2. 導入直後は `docs/PROJECT_STATUS.md` と `docs/ROADMAP.md` を現状に合わせる
3. `docs/tasks/YYYY-MM-DD-HHMM-task-name/` を作る
4. `templates/requirement-alignment.md` で認識合わせを行い、タスク成果物として保存する
5. `templates/implementation-plan.md` で実装計画を作り、タスク成果物として保存する
6. `templates/completion-review.md` で完了前レビューを行い、タスク成果物として保存する
7. `workflows/session-end.md` を実行し、DevlogとGit記録まで確認する

Devlogは1タスクにつき1つ残します。
保存先は `docs/devlog/YYYY-MM-DD/HHMM-task-name.md` を基本にします。

## 注意

- `AGENTS.md` はプロジェクトに合わせて編集してください。
- `PROJECT_STATUS.md` と `ROADMAP.md` は導入時に現状へ書き換えてください。
- 認識合わせが終わるまで、実装に進まないでください。
- デフォルトのworkflow modeはStandardです。
- 認証、権限、課金、個人情報、本番設定、公開リリースに触れる場合はStrict modeに上げます。
