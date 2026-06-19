# AI-assisted Development Starter

このディレクトリは、既存プロジェクトへそのままコピーして使うための導入パッケージです。

## 使い方

`starter/` の中身を、導入したいプロジェクトのルートにコピーします。
このディレクトリは開発運用の導入パッケージです。
プロダクト本体は、導入先プロジェクト側で開発します。

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
  DIRECTORY_MAP.md
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

- `docs/DIRECTORY_MAP.md`
- `docs/ai-workflow/design-rationale.md`
- `docs/ai-workflow/principles.md`
- `docs/ai-workflow/requirement-alignment.md`
- `docs/ai-workflow/task-records.md`
- `docs/ai-workflow/workflow-modes.md`
- `docs/ai-workflow/quality-gates.md`
- `docs/ai-workflow/adr-guidelines.md`
- `workflows/session-start.md`

## 最初の作業で使うもの

通常は次の順番で使います。

1. 作りたいものを整理する
2. AIと壁打ちして目的、制約、成功条件を明確にする
3. `docs/ROADMAP.md` に全体計画を書く
4. `docs/PROJECT_STATUS.md` に現在地を書く
5. `docs/DIRECTORY_MAP.md` に主要ディレクトリと責務を書く
6. `workflows/session-start.md` に沿って現在の開発状況を把握する
7. ROADMAPとPROJECT_STATUSから今回のタスクを選ぶ
8. DIRECTORY_MAPで今回読むべき範囲を絞る
9. `docs/tasks/YYYY-MM-DD-HHMM-task-name/` を作る
10. `templates/requirement-alignment.md` で認識合わせを行い、タスク記録として保存する
11. AIがタスク内容とリスクを見てWorkflow Modeを判定する
12. `templates/implementation-plan.md` で今回の1タスクの実装計画を作り、タスク記録として保存する
13. `templates/completion-review.md` で完了前レビューを行い、タスク記録として保存する
14. `workflows/session-end.md` を実行し、DevlogとGit記録まで確認する

Devlogは1タスクにつき1つ残します。
保存先は `docs/devlog/YYYY-MM-DD/HHMM-task-name.md` を基本にします。

## 注意

- `AGENTS.md` はプロジェクトに合わせて編集してください。
- `PROJECT_STATUS.md` と `ROADMAP.md` は導入時に現状へ書き換えてください。
- `DIRECTORY_MAP.md` は主要ディレクトリと責務に合わせて書き換えてください。
- ROADMAPは全体計画、implementation planは今回の1タスクの実行計画として分けてください。
- 認識合わせが終わるまで、実装に進まないでください。
- Workflow Modeは導入時に固定せず、タスクごとにAIが判定します。
- デフォルトのWorkflow ModeはStandardです。
- 認証、権限、課金、個人情報、本番設定、公開リリースに触れる場合はStrict modeに上げます。
