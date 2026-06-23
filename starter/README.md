# AI-assisted Development Starter

> [!IMPORTANT]
> **このstarterは、新規プロジェクト専用です。**
> 既存プロジェクトへはコピーしないでください。同名のREADME、AGENTS.md、`.github/`、`docs/` などを上書きする可能性があります。

このディレクトリは、新規プロジェクトの立ち上げ時にコピーして使うための導入パッケージです。

## 使い方

推奨手順は、このリポジトリのルートで導入スクリプトを実行する方法です。
導入先は、空フォルダ、または `.git` だけが入った空リポジトリにしてください。

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create-new-project.ps1 C:\path\to\project
```

Bash:

```bash
bash scripts/create-new-project.sh /path/to/project
```

導入スクリプトは、`starter/` の中身を導入先プロジェクトのルートへ展開します。
このディレクトリは開発運用の導入パッケージです。
プロダクト本体は、導入先プロジェクト側で開発します。

プロジェクト案内図はPython 3.10以降を推奨します。外部Pythonパッケージは使いません。
Pythonがない場合、AIは勝手にインストールせず、ユーザーへ確認します。

コピー直後は通常タスクを始めません。
まず `workflows/project-initialization.md` でユーザーとAIが壁打ちし、プロジェクトの基準線を作ります。

`.github/` は隠しディレクトリです。
初期設定状態を保存する `.ai-workflow/` も隠しディレクトリです。
導入スクリプトを使うと、両方とも漏れずに展開されます。

手動コピーは代替手段です。
通常は導入スクリプトを使ってください。

手動でコピーする場合のBash例:

```bash
cp -R starter/. /path/to/project/
```

手動でコピーする場合のPowerShell例:

```powershell
Get-ChildItem -LiteralPath .\starter -Force | Copy-Item -Destination C:\path\to\project -Recurse -Force
```

コピー後の構成:

```text
.ai-workflow/
  project-state.conf
  directory-map.json
  directory-map.ignore
AGENTS.md
docs/
  PROJECT_BRIEF.md
  INITIALIZATION_REVIEW.md
  PROJECT_STATUS.md
  ROADMAP.md
  DIRECTORY_MAP.md
  ai-workflow/
  tasks/
  devlog/
  adr/
templates/
workflows/
scripts/
.github/
```

## AIに最初に読ませるもの

AIエージェントには、まずルートの `AGENTS.md` を読ませます。

次に、必要に応じて以下を読ませます。

- `docs/DIRECTORY_MAP.md`
- `docs/README.md`
- `docs/PROJECT_BRIEF.md`
- `docs/ai-workflow/design-rationale.md`
- `docs/ai-workflow/principles.md`
- `docs/ai-workflow/requirement-alignment.md`
- `docs/ai-workflow/task-records.md`
- `docs/ai-workflow/workflow-modes.md`
- `docs/ai-workflow/quality-gates.md`
- `docs/ai-workflow/pull-request-template.md`
- `docs/project-structure-map.md`
- `docs/ai-workflow/adr-guidelines.md`
- `workflows/session-start.md`
- `workflows/project-initialization.md`

## 導入直後に一度だけ行うこと

通常タスクの前に、次の順番で初期設定します。

1. 初期設定チェッカーで `INITIALIZATION_NOT_STARTED` を確認する
2. 状態を `in_progress` にする
3. ユーザーとAIがプロダクト構想を壁打ちする
4. `docs/PROJECT_BRIEF.md` にConfirmed、Hypothesis、Unknown、Deferredを記録する
5. DiscoveryまたはBuild-readyの経路を選ぶ
6. `docs/ROADMAP.md` に全体計画または検証計画を書く
7. `AGENTS.md` をプロジェクト向けに正式化する
8. `docs/PROJECT_STATUS.md` と `.ai-workflow/directory-map.json` を初期化し、`docs/DIRECTORY_MAP.md` を生成する
9. プロジェクト案内図の検査が `DIRECTORY_MAP_PROVISIONAL` を返すことを確認する
10. `docs/INITIALIZATION_REVIEW.md` でレビューする
11. ユーザーの明示承認後だけ状態を `ready` にする
12. チェッカーが `INITIALIZATION_READY` を返すことを確認する

初期設定は、すべての事業・製品要件を確定する工程ではありません。
曖昧なアイデアから始める場合はDiscoveryを選び、最初の検証タスクを決めます。

## 初期設定後に各タスクで行うこと

1. `workflows/session-start.md` のStep 0で `INITIALIZATION_READY` を確認する
2. 構成チェックで、確認後にファイルの追加・削除がないか調べる
3. 現在の開発状況を把握する
4. ROADMAPとPROJECT_STATUSから今回のタスクを1つ選ぶ
5. DIRECTORY_MAPで今回読むべき範囲を絞る
6. `docs/tasks/YYYY-MM-DD-HHMM-task-name/` を作る
7. ユーザーとの認識を揃える
8. AIがWorkflow Modeを判定する
9. `implementation-plan.md` を作ってから実装する
10. テスト、ビルド、手動確認を行う
11. `completion-review.md` とdevlogを残す
12. `workflows/session-end.md` で終了判断を行う

Devlogは1タスクにつき1つ残します。
保存先は `docs/devlog/YYYY-MM-DD/HHMM-task-name.md` を基本にします。

## 注意

- `AGENTS.md` はプロジェクトに合わせて編集してください。
- 初期設定状態は文書から推測せず、`.ai-workflow/project-state.conf` と判定スクリプトを使ってください。
- `ready` はすべてが確定した意味ではなく、最初のタスクを安全に開始できる意味です。
- `PROJECT_BRIEF.md` では仮説と確定事項を分けてください。
- `PROJECT_STATUS.md` と `ROADMAP.md` は初期設定でプロジェクト内容へ書き換えてください。
- `.ai-workflow/directory-map.json` の主な役割、ファイルの役割説明、処理の流れ、作業場所の案内をプロジェクトに合わせ、`DIRECTORY_MAP.md`を再生成してください。
- 主要ファイルの意味と役割は、README、`docs/README.md`、`DIRECTORY_MAP.md`、localhost画面で確認してください。
- Windowsでは、プロジェクト直下の `open-project-structure-map.cmd` をダブルクリックすると、全ファイルのライブ表示と既定ブラウザが自動で起動します。
- ターミナルから起動する場合は `python scripts/project-structure.py serve --open-browser` を使います。
- 起動中の黒い画面は閉じず、終了するときはその画面で `Ctrl+C` を押します。
- 構造の固定判定は `bash scripts/check-directory-map.sh` または `scripts/check-directory-map.ps1` を使います。
- ROADMAPは全体計画、implementation planは今回の1タスクの実行計画として分けてください。
- 認識合わせが終わるまで、実装に進まないでください。
- Workflow Modeは導入時に固定せず、タスクごとにAIが判定します。
- デフォルトのWorkflow ModeはStandardです。
- 認証、権限、課金、個人情報、本番設定、公開リリースに触れる場合はStrict modeに上げます。
- Pull Requestを使う場合は `.github/pull_request_template.md` を使い、各項目の意味は `docs/ai-workflow/pull-request-template.md` で確認してください。
