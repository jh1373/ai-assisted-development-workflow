# docsの読み方

`docs/` は、このプロジェクトの目的、現在地、計画、判断記録、AI開発ワークフローをまとめる場所です。

このファイルは、導入先プロジェクトで最初に見る `docs/` の入口です。
どの文書をどの順番で読めばよいか、各ファイルが何を担っているかを確認できます。

## 最初に読む順番

新規プロジェクトを開始した直後は、次の順番で確認します。

1. [PROJECT_BRIEF.md](PROJECT_BRIEF.md)
2. [ROADMAP.md](ROADMAP.md)
3. [PROJECT_STATUS.md](PROJECT_STATUS.md)
4. [DIRECTORY_MAP.md](DIRECTORY_MAP.md)
5. [INITIALIZATION_REVIEW.md](INITIALIZATION_REVIEW.md)
6. [ai-workflow/design-rationale.md](ai-workflow/design-rationale.md)
7. [ai-workflow/principles.md](ai-workflow/principles.md)
8. [ai-workflow/practical-guide.md](ai-workflow/practical-guide.md)
9. [../workflows/session-start.md](../workflows/session-start.md)

## 目的別の参照先

| 目的 | 読むファイル |
|---|---|
| プロジェクトの概要を確認したい | [PROJECT_BRIEF.md](PROJECT_BRIEF.md) |
| 全体計画を確認したい | [ROADMAP.md](ROADMAP.md) |
| 現在地と次の候補を確認したい | [PROJECT_STATUS.md](PROJECT_STATUS.md) |
| ディレクトリ構成と役割を確認したい | [DIRECTORY_MAP.md](DIRECTORY_MAP.md) / [project-structure-map.md](project-structure-map.md) |
| 初期設定が通常タスクへ進める状態か確認したい | [INITIALIZATION_REVIEW.md](INITIALIZATION_REVIEW.md) |
| AI開発ワークフローの考え方を知りたい | [ai-workflow/design-rationale.md](ai-workflow/design-rationale.md) / [ai-workflow/principles.md](ai-workflow/principles.md) |
| 1タスクの進め方を知りたい | [ai-workflow/practical-guide.md](ai-workflow/practical-guide.md) |
| 実装前の認識合わせをしたい | [ai-workflow/requirement-alignment.md](ai-workflow/requirement-alignment.md) |
| 作業の重さを選びたい | [ai-workflow/workflow-modes.md](ai-workflow/workflow-modes.md) |
| 品質確認の観点を知りたい | [ai-workflow/quality-gates.md](ai-workflow/quality-gates.md) / [ai-workflow/review-checklist.md](ai-workflow/review-checklist.md) |
| セキュリティ観点を確認したい | [ai-workflow/security.md](ai-workflow/security.md) |
| PR本文の書き方を知りたい | [ai-workflow/pull-request-template.md](ai-workflow/pull-request-template.md) |

## docs直下の主要ファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `docs/README.md` | docsの入口 | docs内の読み方、目的別の参照先、主要ファイルの役割を説明する |
| `docs/PROJECT_BRIEF.md` | プロジェクト概要 | 確定事項、仮説、不明点、後で決めることを整理する |
| `docs/ROADMAP.md` | 全体計画 | プロジェクト全体で何をどの順番で作るかを示す |
| `docs/PROJECT_STATUS.md` | 現在地 | 今どこまで終わり、次に何をする可能性があるかを記録する |
| `docs/INITIALIZATION_REVIEW.md` | 初期設定レビュー | 通常タスクへ進んでよいかを確認する |
| `docs/DIRECTORY_MAP.md` | プロジェクト案内図 | 構成と役割を人間が読める形で表示する生成文書 |
| `docs/project-structure-map.md` | 案内図の説明 | 構成検証とlocalhost画面の使い方を説明する |

## docs/ai-workflow

`docs/ai-workflow/` は、導入済みのAI開発ワークフローを確認する場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `docs/ai-workflow/principles.md` | 基本思想 | AI駆動開発で守る考え方をまとめる |
| `docs/ai-workflow/design-rationale.md` | 設計理由 | なぜこのワークフロー構成にしているかを説明する |
| `docs/ai-workflow/practical-guide.md` | 実践手順 | 1タスクをどう進めるかを説明する |
| `docs/ai-workflow/requirement-alignment.md` | 認識合わせ | 実装前にユーザーとAIの理解を揃える方法を説明する |
| `docs/ai-workflow/quality-gates.md` | 品質チェック | 作業前後に確認する関門を説明する |
| `docs/ai-workflow/review-checklist.md` | レビュー項目 | 初期設定、実装前、実装中、完了前、公開前の確認項目をまとめる |
| `docs/ai-workflow/definition-of-done.md` | 完了基準 | 何をもって完了と判断するかを説明する |
| `docs/ai-workflow/workflow-modes.md` | 作業の重さ | Minimal、Standard、Strictの使い分けを説明する |
| `docs/ai-workflow/strict-mode.md` | 厳格モード | 高リスク変更で必要な確認を説明する |
| `docs/ai-workflow/security.md` | セキュリティ確認 | 秘密情報、個人情報、権限変更などの扱いを説明する |
| `docs/ai-workflow/ai-human-boundary.md` | AIと人間の責任範囲 | AIに任せてよいこと、人間が判断することを分ける |
| `docs/ai-workflow/anti-patterns.md` | 避けるべき失敗 | AI駆動開発で起きやすい失敗例をまとめる |
| `docs/ai-workflow/task-records.md` | タスク記録 | `docs/tasks/` に何を残すかを説明する |
| `docs/ai-workflow/pull-request-template.md` | PR確認シートの説明 | Pull Request本文に何を書くかを説明する |
| `docs/ai-workflow/adr-guidelines.md` | 設計判断記録 | 後から見返すべき設計判断をADRとして残す基準を説明する |
| `docs/ai-workflow/team-development.md` | チーム開発 | チームでこのワークフローを使うときの考え方を説明する |

## docs/tasks と docs/devlog

| パス | 意味 | 役割 |
|---|---|---|
| `docs/tasks/` | タスクごとの作業記録 | 認識合わせ、実装計画、完了レビューなどをタスク単位で残す |
| `docs/devlog/` | 開発ログ | 変更理由、判断、検証結果、次に見るべきことを残す |

`docs/tasks/` は成果物置き場ではありません。
実際のコード、UI、テスト、設定ファイルは通常のプロジェクト構成に置きます。

## プロジェクト全体の主要ファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `README.md` | 最初に読む説明 | プロジェクトの目的、使い方、全体像を説明する |
| `AGENTS.md` | AIに守らせるルール | AIエージェントが作業前に読む必須ルール |
| `templates/` | 作業記録のひな型 | 認識合わせ、実装計画、完了確認、devlogなどの形式を揃える |
| `workflows/` | 作業手順 | 初期設定、タスク開始、タスク終了の順番を定義する |
| `scripts/` | 自動化 | 初期設定確認、構成確認、localhost画面の起動を担当する |
| `open-project-structure-map.cmd` | 案内図の起動ボタン | Windowsでlocalhost画面をワンクリック起動する |
| `.ai-workflow/project-state.conf` | 初期設定状態 | 初期設定が未開始、作業中、完了のどれかを判定する |
| `.ai-workflow/directory-map.json` | 案内図の正本 | 役割グループ、ファイル説明、作業場所の案内を保存する |
| `.github/pull_request_template.md` | Pull Request確認シート | PR作成時に、変更内容、検証結果、残るリスクを書く型を表示する |
| `.github/ISSUE_TEMPLATE/bug.md` | バグ報告のひな型 | 不具合の内容、再現手順、期待する動き、確認方法を揃える |
| `.github/ISSUE_TEMPLATE/task.md` | タスク作成のひな型 | 作業の目的、範囲、完了条件、確認方法を揃える |
| `.github/workflows/project-structure-check.yml` | 自動チェック | pushやPull Request時にプロジェクト案内図を検証する |
