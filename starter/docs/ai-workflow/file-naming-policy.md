# 主要ファイル名の意味

このドキュメントは、プロジェクト内の主要なファイル名と、その役割を確認するための一覧です。

ファイル名だけでは初心者が意味を判断しにくいため、よく使うファイルを日本語で説明します。
詳しい開発手順は [practical-guide.md](practical-guide.md)、全体の設計理由は [design-rationale.md](design-rationale.md) を参照してください。

## 最初に見るファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `README.md` | 最初に読む説明 | プロジェクトの目的、使い方、全体像を説明する |
| `AGENTS.md` | AIに守らせるルール | AIエージェントが作業前に読む必須ルール |

## docs

`docs/` は、プロジェクトの状態、計画、判断、AI開発ワークフローの説明を置く場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
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
| `docs/ai-workflow/file-naming-policy.md` | 主要ファイル名の意味 | 主要ファイルが何をするものかを一覧で説明する |

## docs/tasks と docs/devlog

| パス | 意味 | 役割 |
|---|---|---|
| `docs/tasks/` | タスクごとの作業記録 | 認識合わせ、実装計画、完了レビューなどをタスク単位で残す |
| `docs/devlog/` | 開発ログ | 変更理由、判断、検証結果、次に見るべきことを残す |

`docs/tasks/` は成果物置き場ではありません。
実際のコード、UI、テスト、設定ファイルは通常のプロジェクト構成に置きます。

## templates

`templates/` は、作業記録を同じ形式で残すためのひな型です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `templates/requirement-alignment.md` | 認識合わせのひな型 | 実装前に目的、範囲、不明点を揃える |
| `templates/task-brief.md` | タスク概要のひな型 | 今回のタスクの目的と背景を短く整理する |
| `templates/implementation-plan.md` | 実装計画のひな型 | 作業前に目的、範囲、検証方法を固定する |
| `templates/completion-review.md` | 完了確認のひな型 | 作業後に検証結果、残るリスク、完了判断を残す |
| `templates/devlog.md` | 開発記録のひな型 | 判断理由、検証結果、次に見るべきことを残す |
| `templates/adr.md` | 設計判断記録のひな型 | 後から見返すべき設計判断を残す |
| `templates/security-review.md` | セキュリティ確認のひな型 | 高リスク変更で安全性を確認する |
| `templates/rollback-plan.md` | 戻し方のひな型 | 問題が起きたときの復旧方法を残す |

## workflows

`workflows/` は、AIと人間がどの順番で作業するかを定義する場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `workflows/project-initialization.md` | 初回設定手順 | 新規プロジェクト開始時に目的、仮説、計画を整理する |
| `workflows/session-start.md` | タスク開始手順 | 作業開始時に現在地、構造、対象範囲を確認する |
| `workflows/session-end.md` | タスク終了手順 | 作業終了時に検証、記録、構造更新を確認する |

## scripts

`scripts/` は、初期設定や構成確認を自動化するためのプログラム置き場です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `scripts/check-initialization.sh` | 初期設定確認 | Bash環境で初期設定状態を機械判定する |
| `scripts/check-initialization.ps1` | 初期設定確認 | PowerShell環境で初期設定状態を機械判定する |
| `scripts/check-directory-map.sh` | 構成確認 | Bash環境でプロジェクト案内図の状態を確認する |
| `scripts/check-directory-map.ps1` | 構成確認 | PowerShell環境でプロジェクト案内図の状態を確認する |
| `scripts/project-structure.py` | プロジェクト案内図の本体 | 構成検証、Markdown生成、localhost画面の起動を担当する |
| `scripts/project-structure-viewer/` | localhost画面 | ブラウザでプロジェクト構成と役割を表示する |
| `open-project-structure-map.cmd` | 案内図の起動ボタン | Windowsでlocalhost画面をワンクリック起動する |

## .github

`.github/` は、GitHub上でのIssue、Pull Request、CIを管理する場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `.github/pull_request_template.md` | Pull Request確認シート | PR作成時に、変更内容、検証結果、残るリスクを書く型を表示する |
| `.github/ISSUE_TEMPLATE/` | Issueひな型 | バグ報告やタスク作成時の入力形式を揃える |
| `.github/workflows/project-structure-check.yml` | 自動チェック | pushやPull Request時にプロジェクト案内図を検証する |

## .ai-workflow

`.ai-workflow/` は、AIが推測せずに状態と構成を確認するための機械判定用データを置く場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `.ai-workflow/project-state.conf` | 初期設定状態 | 初期設定が未開始、作業中、完了のどれかを判定する |
| `.ai-workflow/directory-map.json` | 案内図の正本 | 役割グループ、ファイル説明、作業場所の案内を保存する |
| `.ai-workflow/directory-map.ignore` | 除外設定 | 案内図に含めないファイルやフォルダを指定する |
