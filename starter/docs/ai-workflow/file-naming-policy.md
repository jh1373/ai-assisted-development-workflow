# File Naming Policy

このドキュメントは、このプロジェクトでファイル名とディレクトリ名を英語で統一する理由を説明します。

結論として、ファイル名は英語のままにします。
その代わり、README、各ドキュメント本文、Project Structure Map、`DIRECTORY_MAP.md`、localhost画面では日本語で役割を説明します。

## 基本方針

```text
ファイル名とディレクトリ名: 英語
本文と説明: 日本語
初心者向けの意味説明: README、DIRECTORY_MAP、localhost画面で補う
```

この方針は、見た目を英語に寄せるためではありません。
GitHub、CI、CLI、AIエージェント、エディタ、スクリプトで安定して扱うためです。

## なぜ英語名にするか

### 1. GitHubと開発ツールで扱いやすい

GitHub、GitHub Actions、PowerShell、Bash、Python、Node.js、VS Codeなどは、日本語ファイル名も扱えます。
しかし、公開リポジトリや自動化では英語ファイル名の方が事故が少なくなります。

日本語ファイル名では、環境によって次の問題が起きることがあります。

- URLが長く読みにくくなる
- CLIで入力しにくい
- ログやエラー表示で文字化けする
- 外部ツールがパスを正しく扱えない場合がある
- AIや検索ツールへの指示が不安定になる場合がある

### 2. GitHubが決めている名前がある

一部のファイルは、GitHubや開発ツールが特定の名前で認識します。

例:

| ファイル | 理由 |
|---|---|
| `README.md` | GitHubでリポジトリのトップ説明として自動表示される |
| `LICENSE` | GitHubでライセンスとして認識される |
| `.github/pull_request_template.md` | Pull Request作成時の本文テンプレートとして認識される |
| `.github/workflows/*.yml` | GitHub Actionsのワークフローとして実行される |
| `AGENTS.md` | AIエージェントが最初に読むルールとして扱う |

これらは日本語名にすると、期待した機能が動かなくなる可能性があります。

### 3. AIエージェントに指示しやすい

このプロジェクトは、AI駆動開発を前提にしています。
AIに対しては、英語のパスを指定した方が安定します。

例:

```text
docs/ai-workflow/quality-gates.md を確認してください。
```

このように指示できると、AI、ターミナル、エディタ、GitHubの表示が揃います。

### 4. 日本語で分かりやすくする場所を分ける

初心者にとって重要なのは、ファイル名が日本語であることではありません。
そのファイルが何のためにあるかを、すぐ理解できることです。

このプロジェクトでは、英語ファイル名の意味を次の場所で補います。

- README: 主要ファイルの役割を日本語で説明する
- `docs/DIRECTORY_MAP.md`: 構成と役割を日本語で表示する
- localhost画面: ファイル名、役割、説明の根拠を日本語で表示する
- 各ドキュメント冒頭: そのファイルの目的を日本語で説明する

## 主要ファイル名の意味

| ファイル名 | 日本語での意味 | 役割 |
|---|---|---|
| `README.md` | 最初に読む説明 | プロジェクトの目的、使い方、全体像を説明する |
| `AGENTS.md` | AIに守らせるルール | AIエージェントが作業前に読む必須ルール |
| `docs/ai-workflow/principles.md` | 基本思想 | AI駆動開発で守る考え方をまとめる |
| `docs/ai-workflow/design-rationale.md` | 設計理由 | なぜこの構成にしているかを説明する |
| `docs/ai-workflow/practical-guide.md` | 実践手順 | 1タスクをどう進めるかを説明する |
| `docs/ai-workflow/file-naming-policy.md` | ファイル名の方針 | 英語ファイル名を使う理由と対応表を説明する |
| `docs/ai-workflow/quality-gates.md` | 品質チェック | 作業前後に確認すべき関門を説明する |
| `docs/ai-workflow/workflow-modes.md` | 作業の重さ | Minimal、Standard、Strictの使い分けを説明する |
| `docs/ai-workflow/strict-mode.md` | 厳格モード | 高リスク変更で必要な確認を説明する |
| `docs/ai-workflow/task-records.md` | タスク記録 | `docs/tasks/` に何を残すかを説明する |
| `docs/ai-workflow/pull-request-template.md` | PR確認シートの説明 | PR本文に何を書くかを説明する |
| `docs/project-structure-map.md` | プロジェクト案内図 | 構成の検証とlocalhost画面の使い方を説明する |
| `templates/implementation-plan.md` | 実装計画のひな型 | 作業前に目的、範囲、検証方法を固定する |
| `templates/completion-review.md` | 完了確認のひな型 | 作業後に検証結果、残るリスク、完了判断を残す |
| `templates/devlog.md` | 開発記録のひな型 | 判断理由、検証結果、次に見るべきことを残す |
| `workflows/session-start.md` | タスク開始手順 | 作業開始時に現在地、構造、対象範囲を確認する |
| `workflows/session-end.md` | タスク終了手順 | 作業終了時に検証、記録、構造更新を確認する |
| `workflows/project-initialization.md` | 初回設定手順 | 新規プロジェクト開始時に目的、仮説、計画を整理する |

## 命名ルール

新しいファイルやディレクトリを作るときは、次のルールに従います。

- 英小文字を基本にする
- 単語はハイフンで区切る
- 役割が分かる名前にする
- 略語を増やしすぎない
- 日本語名は原則使わない
- GitHubやツールが認識する既定名は変えない

良い例:

```text
docs/ai-workflow/security.md
docs/ai-workflow/file-naming-policy.md
templates/rollback-plan.md
workflows/session-start.md
```

避ける例:

```text
docs/セキュリティ.md
docs/fileNamingPolicy.md
docs/fnp.md
workflows/start.md
```

`start.md` のように短すぎる名前は、何を開始するのかが分かりにくくなります。
`fileNamingPolicy.md` のようなcamelCaseは、Markdown文書の命名としてこのプロジェクトでは使いません。

## 日本語名を使ってよい場合

原則としてファイル名は英語にします。

ただし、次のように日本語名そのものが成果物の意味を持つ場合は例外です。

- ユーザーに配布する日本語資料
- 日本語タイトルが正式名称の文書
- 画像、PDF、提出物など、コードや自動化の対象ではない成果物

この例外を使う場合も、スクリプトやCIが直接参照するパスには日本語名を使わない方が安全です。

## 判断基準

迷った場合は、次の基準で決めます。

```text
機械が読む、AIに指示する、GitHubで自動認識する、CLIで扱う
→ 英語名にする

人間が意味を理解する
→ 本文、README、DIRECTORY_MAP、localhost画面で日本語説明を補う
```

このプロジェクトでは、英語ファイル名を使うこと自体が目的ではありません。
開発運用を安定させたうえで、日本語説明によって初心者にも意味が伝わる状態を作ることが目的です。
