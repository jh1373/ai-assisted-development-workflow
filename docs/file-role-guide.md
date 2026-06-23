# 主要ファイル名の意味

このドキュメントは、リポジトリ内の主要なファイル名と、その役割を確認するための一覧です。

ファイル名だけでは初心者が意味を判断しにくいため、よく使うファイルを日本語で説明します。
詳しい開発手順は [practical-guide.md](practical-guide.md)、全体の設計理由は [design-rationale.md](design-rationale.md) を参照してください。

## 最初に見るファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `README.md` | 最初に読む説明 | リポジトリの目的、使い方、全体像を説明する |
| `AGENTS.md` | AIに守らせるルール | AIエージェントが作業前に読む必須ルール |
| `LICENSE` | 利用条件 | このリポジトリをどの条件で利用できるかを示す |

## docs

`docs/` は、ワークフローの考え方、使い方、品質確認、作業記録を置く場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `docs/principles.md` | 基本思想 | AI駆動開発で守る考え方をまとめる |
| `docs/design-rationale.md` | 設計理由 | なぜこのワークフロー構成にしているかを説明する |
| `docs/practical-guide.md` | 実践手順 | 1タスクをどう進めるかを説明する |
| `docs/adoption-guide.md` | 導入手順 | 新規プロジェクトへ導入するときの流れを説明する |
| `docs/requirement-alignment.md` | 認識合わせ | 実装前にユーザーとAIの理解を揃える方法を説明する |
| `docs/quality-gates.md` | 品質チェック | 作業前後に確認する関門を説明する |
| `docs/review-checklist.md` | レビュー項目 | 初期設定、実装前、実装中、完了前、公開前の確認項目をまとめる |
| `docs/definition-of-done.md` | 完了基準 | 何をもって完了と判断するかを説明する |
| `docs/workflow-modes.md` | 作業の重さ | Minimal、Standard、Strictの使い分けを説明する |
| `docs/strict-mode.md` | 厳格モード | 高リスク変更で必要な確認を説明する |
| `docs/security.md` | セキュリティ確認 | 秘密情報、個人情報、権限変更などの扱いを説明する |
| `docs/ai-human-boundary.md` | AIと人間の責任範囲 | AIに任せてよいこと、人間が判断することを分ける |
| `docs/anti-patterns.md` | 避けるべき失敗 | AI駆動開発で起きやすい失敗例をまとめる |
| `docs/task-records.md` | タスク記録 | `docs/tasks/` に何を残すかを説明する |
| `docs/pull-request-template.md` | PR確認シートの説明 | Pull Request本文に何を書くかを説明する |
| `docs/project-structure-map.md` | プロジェクト案内図 | 構成の検証とlocalhost画面の使い方を説明する |
| `docs/file-role-guide.md` | 主要ファイル名の意味 | 主要ファイルが何をするものかを一覧で説明する |

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
| `scripts/check-docs.sh` | ドキュメント確認 | 必須ファイル、リンク、秘密情報らしき文字列などを確認する |
| `scripts/check-initialization.sh` | 初期設定確認 | Bash環境で初期設定状態を機械判定する |
| `scripts/check-initialization.ps1` | 初期設定確認 | PowerShell環境で初期設定状態を機械判定する |
| `scripts/check-directory-map.sh` | 構成確認 | Bash環境でプロジェクト案内図の状態を確認する |
| `scripts/check-directory-map.ps1` | 構成確認 | PowerShell環境でプロジェクト案内図の状態を確認する |
| `scripts/project-structure.py` | プロジェクト案内図の本体 | 構成検証、Markdown生成、localhost画面の起動を担当する |
| `scripts/project-structure-viewer/` | localhost画面 | ブラウザでプロジェクト構成と役割を表示する |

## .github

`.github/` は、GitHub上でのIssue、Pull Request、CIを管理する場所です。

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `.github/pull_request_template.md` | Pull Request確認シート | PR作成時に、変更内容、検証結果、残るリスクを書く型を表示する |
| `.github/ISSUE_TEMPLATE/` | Issueひな型 | バグ報告やタスク作成時の入力形式を揃える |
| `.github/workflows/docs-check.yml` | 自動チェック | pushやPull Request時にドキュメント構造を検証する |

## starter

`starter/` は、新規プロジェクトへコピーする導入パッケージです。

| パス | 意味 | 役割 |
|---|---|---|
| `starter/README.md` | starterの使い方 | 新規プロジェクトへコピーする方法を説明する |
| `starter/AGENTS.md` | 導入先AIルール | コピー先プロジェクトでAIが守る基本ルール |
| `starter/docs/` | 導入先ドキュメント | コピー先プロジェクトで使う説明、状態、計画、記録 |
| `starter/templates/` | 導入先テンプレート | コピー先プロジェクトで使う作業記録のひな型 |
| `starter/workflows/` | 導入先手順 | コピー先プロジェクトで使う初期設定とタスク手順 |
| `starter/scripts/` | 導入先スクリプト | コピー先プロジェクトで使う自動確認とlocalhost画面 |
| `starter/.github/` | 導入先GitHub設定 | コピー先プロジェクトで使うPRテンプレートとCI設定 |
| `starter/.ai-workflow/` | 導入先の状態管理 | 初期設定状態とプロジェクト案内図の正本を保存する |

## examples

`examples/` は、実際にこのワークフローを使うとどう見えるかを示す例です。

| パス | 意味 | 役割 |
|---|---|---|
| `examples/project-initialization/` | 初期設定例 | Project Initialization完了後の文書例を示す |
| `examples/react-app/` | Reactアプリ例 | アプリ開発タスクでの記録例を示す |
| `examples/devlog/` | devlog例 | 開発ログの書き方の例を示す |
