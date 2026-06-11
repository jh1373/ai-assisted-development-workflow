# AI-assisted Development Workflow

AI開発支援ツールを使う開発で、文脈、計画、検証、判断理由を失わないためのワークフローテンプレート集です。

このリポジトリは、AIにコード作成を丸投げするためのプロンプト集ではありません。
Gitが「何を変えたか」を残すのに対して、このワークフローは「なぜ変えたか」「何を試したか」「次に何を見るべきか」を残すためのものです。

## 30秒で分かる概要

AI支援開発では、実装は速くなります。一方で、判断理由や失敗した試行がチャット内に埋もれやすくなります。

このリポジトリでは、1つのタスクを1つの開発セッションとして扱います。
作業開始時に現在地を復元し、実装前に計画を作り、完了前にレビューし、最後にdevlogとGitで記録します。

```text
要件定義
→ ロードマップ
→ タスク分割
→ session start
→ implementation plan
→ implementation
→ completion review
→ session end
→ devlog + git commit
```

## 何のためのリポジトリか

目的は、AI支援開発を「その場のチャット」ではなく「追跡できる開発プロセス」にすることです。

解決したい課題:

- チャットが長くなり、前提や判断理由が埋もれる
- Gitには差分は残るが、実装理由や失敗した試行は残りにくい
- 別のチャットで再開したとき、現在地を復元しにくい
- AIの提案を採用した理由、採用しなかった理由が残らない
- テスト、ビルド、レビューが曖昧なまま完了扱いになりやすい

## このリポジトリでできること

- AI支援開発の作業開始手順を標準化する
- 実装前の計画をテンプレート化する
- 完了前レビューの観点を固定する
- devlogで判断理由を残す
- 次のチャットや次の作業者が再開しやすい状態を作る
- 小さく導入し、必要に応じて厳格な運用へ拡張する

## これは何ではないか

- 万能な開発手法ではありません
- 特定のAIツール専用ではありません
- コード品質を自動で保証するものではありません
- テストやレビューを不要にするものではありません
- チャット全文を保存するための仕組みではありません

人間が要件、判断、検証、公開可否を管理し、AIを調査や実装の補助として使うことを前提にしています。

## Quick Start

最初はすべてを導入する必要はありません。まずは最小構成で始めます。

### 1. 必要なテンプレートをコピーする

自分のプロジェクトに次のファイルを置きます。

```text
docs/PROJECT_STATUS.md
docs/devlog/
workflows/session-start.md
workflows/session-end.md
templates/implementation-plan.md
templates/devlog.md
templates/completion-review.md
```

### 2. プロジェクトの現在地を書く

`docs/PROJECT_STATUS.md` に、今の状態、次にやること、最後に確認したテストを書きます。

### 3. タスクごとにセッションを分ける

大きなチャットで複数タスクを続けず、1タスクごとに新しいセッションを使います。

### 4. 作業開始時に現在地を復元する

`workflows/session-start.md` に沿って、Git状態、現在地、直近devlog、テスト状態を確認します。

### 5. 実装前に計画を作る

`templates/implementation-plan.md` を使い、目的、対象範囲、実装手順、検証方法、完了条件を決めます。

### 6. 完了前にレビューする

`templates/completion-review.md` を使い、漏れ、余計な変更、未検証、次回への引き継ぎを確認します。

### 7. session endで記録する

`workflows/session-end.md` と `templates/devlog.md` を使い、判断理由、試したこと、検証結果、残課題を残します。

## 運用モード

プロジェクトの重さに応じて、3段階で使えます。

| モード | 向いている用途 | 使うもの |
|---|---|---|
| Minimal | 学習、小さな個人開発、短いタスク | `PROJECT_STATUS.md`, `implementation-plan.md`, `devlog.md` |
| Standard | 継続的な個人開発、面接で見せるポートフォリオ | Minimal + `session-start.md`, `session-end.md`, `completion-review.md` |
| Strict | 公開前、複数人開発、重要な設計変更 | Standard + `roadmap.md`, `review-checklist.md`, security review |

詳しくは [docs/workflow-modes.md](docs/workflow-modes.md) を参照してください。

## リポジトリ構成

```text
.
├── README.md
├── workflows/
│   ├── session-start.md
│   └── session-end.md
├── templates/
│   ├── completion-review.md
│   ├── devlog.md
│   ├── implementation-plan.md
│   ├── project-status.md
│   ├── roadmap.md
│   └── task-brief.md
├── docs/
│   ├── adoption-guide.md
│   ├── ai-human-boundary.md
│   ├── review-checklist.md
│   ├── security.md
│   └── workflow-modes.md
└── examples/
    └── react-app/
        ├── README.md
        ├── PROJECT_STATUS.md
        ├── completion-review-example.md
        ├── devlog-example.md
        └── implementation-plan-example.md
```

## 使うべき場面

- AI支援開発でチャットが長くなりすぎる
- 後から「なぜこの実装にしたのか」が分からなくなる
- Gitの差分だけでは判断理由が足りない
- 個人開発でもチーム開発に近い形で進めたい
- 面接やレビューで、開発プロセスを説明できる状態にしたい

## 使わない方がよい場面

- 数分で終わる単純な修正
- 一度きりの実験コード
- そもそもGitやドキュメントで管理する必要がない作業
- ログを残すことで秘密情報が漏れる危険が高い作業

## 導入ガイド

既存プロジェクトに導入する場合は、[docs/adoption-guide.md](docs/adoption-guide.md) から始めてください。

レビュー観点だけ使いたい場合は、[docs/review-checklist.md](docs/review-checklist.md) を参照してください。

AIと人間の役割分担は、[docs/ai-human-boundary.md](docs/ai-human-boundary.md) にまとめています。

## セキュリティとプライバシー

devlogやプロジェクト文書には、秘密情報、認証情報、個人情報、管理画面URL、社内固有情報を含めないでください。

詳しくは [docs/security.md](docs/security.md) を参照してください。

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
