# docsの読み方

`docs/` は、このリポジトリの考え方、導入手順、品質確認、作業記録をまとめる場所です。

このファイルは、`docs/` フォルダの入口です。
どの文書をどの順番で読めばよいか、各ファイルが何を担っているかを確認できます。

## 最初に読む順番

初めてこのリポジトリを見る場合は、次の順番で読むと全体像を掴みやすくなります。

1. [design-rationale.md](design-rationale.md)
2. [principles.md](principles.md)
3. [adoption-guide.md](adoption-guide.md)
4. [../workflows/project-initialization.md](../workflows/project-initialization.md)
5. [requirement-alignment.md](requirement-alignment.md)
6. [task-records.md](task-records.md)
7. [practical-guide.md](practical-guide.md)
8. [workflow-modes.md](workflow-modes.md)
9. [quality-gates.md](quality-gates.md)
10. [adr-guidelines.md](adr-guidelines.md)

## 目的別の参照先

| 目的 | 読むファイル |
|---|---|
| この構成にしている理由を知りたい | [design-rationale.md](design-rationale.md) |
| AI駆動開発の基本思想を知りたい | [principles.md](principles.md) |
| 新規プロジェクトへ導入したい | [adoption-guide.md](adoption-guide.md) |
| 1タスクの進め方を知りたい | [practical-guide.md](practical-guide.md) |
| 実装前の認識合わせをしたい | [requirement-alignment.md](requirement-alignment.md) |
| 作業の重さを選びたい | [workflow-modes.md](workflow-modes.md) |
| 品質確認の観点を知りたい | [quality-gates.md](quality-gates.md) / [review-checklist.md](review-checklist.md) |
| 完了条件を確認したい | [definition-of-done.md](definition-of-done.md) |
| セキュリティ観点を確認したい | [security.md](security.md) |
| AIと人間の責任範囲を分けたい | [ai-human-boundary.md](ai-human-boundary.md) |
| よくある失敗を避けたい | [anti-patterns.md](anti-patterns.md) |
| PR本文の書き方を知りたい | [pull-request-template.md](pull-request-template.md) |
| プロジェクト案内図を使いたい | [project-structure-map.md](project-structure-map.md) |

## docs内の主要ファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `docs/README.md` | docsの入口 | docs内の読み方、目的別の参照先、主要ファイルの役割を説明する |
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
| `docs/team-development.md` | チーム開発 | チームでこのワークフローを使うときの考え方を説明する |
| `docs/adr-guidelines.md` | 設計判断記録 | 後から見返すべき設計判断をADRとして残す基準を説明する |

## docs/tasks と docs/devlog

| パス | 意味 | 役割 |
|---|---|---|
| `docs/tasks/` | タスクごとの作業記録 | 認識合わせ、実装計画、完了レビューなどをタスク単位で残す |
| `docs/devlog/` | 開発ログ | 変更理由、判断、検証結果、次に見るべきことを残す |

`docs/tasks/` は成果物置き場ではありません。
実際のコード、UI、テスト、設定ファイルは通常のプロジェクト構成に置きます。

## リポジトリ全体の主要ファイル

| ファイル名 | 意味 | 役割 |
|---|---|---|
| `README.md` | 最初に読む説明 | リポジトリの目的、使い方、全体像を説明する |
| `AGENTS.md` | AIに守らせるルール | AIエージェントが作業前に読む必須ルール |
| `LICENSE` | 利用条件 | このリポジトリをどの条件で利用できるかを示す |
| `templates/` | 作業記録のひな型 | 認識合わせ、実装計画、完了確認、devlogなどの形式を揃える |
| `workflows/` | 作業手順 | 初期設定、タスク開始、タスク終了の順番を定義する |
| `scripts/` | 自動化 | 初期設定確認、構成確認、localhost画面の起動を担当する |
| `.github/pull_request_template.md` | Pull Request確認シート | PR作成時に、変更内容、検証結果、残るリスクを書く型を表示する |
| `.github/ISSUE_TEMPLATE/bug.md` | バグ報告のひな型 | 不具合の内容、再現手順、期待する動き、確認方法を揃える |
| `.github/ISSUE_TEMPLATE/task.md` | タスク作成のひな型 | 作業の目的、範囲、完了条件、確認方法を揃える |
| `.github/workflows/docs-check.yml` | 自動チェック | pushやPull Request時にドキュメント構造を検証する |
| `starter/` | 導入パッケージ | 新規プロジェクトへコピーする一式を保存する |
| `examples/` | 利用例 | 実際にこのワークフローを使うとどう見えるかを示す |
