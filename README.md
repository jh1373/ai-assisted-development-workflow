# AI-assisted Development Workflow

AI駆動開発で、実装速度だけを上げるのではなく、品質、判断理由、検証結果、責任範囲を失わずにプロダクトを作るための実践ガイドです。

このリポジトリは、AIにコード作成を丸投げするためのプロンプト集でも、Markdownテンプレート集でもありません。
Codex、Claude Code、Google Antigravity、GitHub Copilot などのAI開発支援ツールを使うときに、何をAIに任せ、何を人間が判断し、どの証拠を残せば品質を保てるかを整理するためのものです。

## 何を解決するか

AI駆動開発では、実装は速くなります。
一方で、次の問題も速く発生します。

- 何を作るべきかが曖昧なまま、AIがそれらしい実装を始める
- ユーザーとAIの認識がズレたまま、プロダクトが作られていく
- チャットが長くなり、前提や判断理由が埋もれる
- Gitには差分が残るが、なぜその実装にしたかは残らない
- AIが不要なリファクタリングや範囲外の変更を混ぜる
- テスト、ビルド、手動確認が曖昧なまま完了扱いになる
- 別のチャットや別の作業者が再開したとき、現在地を復元できない
- 認証、権限、課金、個人情報などの高リスク変更をAI任せにしてしまう

このガイドの目的は、AIを使わないことではありません。
AIで実装速度を上げながら、人間が品質と公開判断に責任を持てる状態を作ることです。

## 基本思想

このワークフローは、次の考え方を中心にしています。

- チャットは作業場であり、信頼できる記録ではない
- Gitは「何を変えたか」を残すが、「なぜ変えたか」は別に残す
- 認識合わせが終わるまで、実装に進まない
- 実装前に目的、対象範囲、完了条件、検証方法を固定する
- AIの出力は成果物ではなく、レビュー対象の提案として扱う
- 完了とは、実装済みではなく、検証済みで再開可能な状態を指す
- 不確実性、失敗、見送った選択肢を隠さない
- 作業の重さは、リスクの大きさに合わせる

詳しくは [docs/principles.md](docs/principles.md) を参照してください。

## 実践フロー

1つのタスクを、1つの開発セッションとして扱います。

```text
ユーザーの要望を受け取る
→ AI側の理解を要約する
→ 不明点、曖昧な点、懸念点を洗い出す
→ 必要ならユーザーに確認する
→ 合意できた範囲だけをタスク化する
→ タスクを分ける
→ 現在地を復元する
→ 実装計画を作る
→ AIと実装する
→ テストと手動確認を行う
→ 完了前レビューを行う
→ devlogとGitに記録する
→ 必要ならPRでレビューする
```

実際の進め方は [docs/practical-guide.md](docs/practical-guide.md) にまとめています。
要件認識合わせの原則は [docs/requirement-alignment.md](docs/requirement-alignment.md) を参照してください。

## まず使う4ファイル

最初からすべてを導入する必要はありません。
まずは次の3つだけで始められます。

```text
docs/PROJECT_STATUS.md
templates/requirement-alignment.md
templates/implementation-plan.md
templates/devlog.md
```

- `PROJECT_STATUS.md`: 次のセッションで最初に読む現在地メモ
- `requirement-alignment.md`: 実装前にユーザーとAIの認識を揃える確認メモ
- `implementation-plan.md`: 実装前に目的、範囲、検証方法を固定する計画
- `devlog.md`: 作業後に判断理由、検証結果、未完了事項を残す記録

慣れてきたら、`session-start.md`、`completion-review.md`、`AGENTS.md`、PRテンプレート、Strict modeを追加します。

## 品質を守る関門

AI駆動開発では、速く作れるぶん、間違った変更も速く混ざります。
そのため、作業ごとに品質ゲートを決めます。

例:

- requirement alignment gate: ユーザーとAIの認識が揃っているか
- scope gate: 何をやるか、何をやらないかが明確か
- test gate: テスト、ビルド、手動確認を実行したか
- diff gate: 予定外の変更が混ざっていないか
- security gate: 秘密情報、個人情報、権限変更がないか
- recovery gate: 問題が出たときに戻せるか
- review gate: 人間が最終判断すべき変更ではないか

詳しくは [docs/quality-gates.md](docs/quality-gates.md) を参照してください。

## 運用モード

作業の重さに応じて、3段階で使います。
デフォルトは **Standard** です。
AIは作業内容を見て、低リスクなら理由を明示してMinimalに下げ、高リスクなら必ずStrictに上げます。

| モード | 向いている用途 | 目的 |
|---|---|---|
| Minimal | 小さく、戻しやすく、低リスクな作業 | 目的、検証、判断理由だけ残す |
| Standard | 通常の機能追加、バグ修正、UI改善 | 開始、計画、完了レビュー、devlogを回す |
| Strict | 認証、権限、課金、個人情報、本番、公開、設計変更 | リスク、承認、復旧方法まで証拠を残す |

詳しくは [docs/workflow-modes.md](docs/workflow-modes.md) と [docs/strict-mode.md](docs/strict-mode.md) を参照してください。

## 個人開発とチーム開発

個人開発では、現在地、判断理由、検証結果を残すことが主な目的です。
チーム開発では、それに加えて責任範囲、PRレビュー、CI、承認、ロールバックまで必要になります。

チームで使う場合は、最低限次を決めます。

- AIに任せてよい作業と、人間が必ず判断する作業
- PRで必ず書く検証結果
- Strict modeが必要な変更
- 誰がレビューし、誰がマージ判断するか
- 失敗時にどう戻すか

詳しくは [docs/team-development.md](docs/team-development.md) を参照してください。

## リポジトリ構成

```text
.
├── README.md
├── docs/
│   ├── adoption-guide.md
│   ├── ai-human-boundary.md
│   ├── anti-patterns.md
│   ├── definition-of-done.md
│   ├── practical-guide.md
│   ├── principles.md
│   ├── quality-gates.md
│   ├── requirement-alignment.md
│   ├── review-checklist.md
│   ├── security.md
│   ├── strict-mode.md
│   ├── team-development.md
│   └── workflow-modes.md
├── workflows/
│   ├── session-start.md
│   └── session-end.md
├── templates/
│   ├── AGENTS.md
│   ├── adr.md
│   ├── completion-review.md
│   ├── devlog.md
│   ├── implementation-plan.md
│   ├── project-status.md
│   ├── requirement-alignment.md
│   ├── roadmap.md
│   ├── rollback-plan.md
│   ├── security-review.md
│   └── task-brief.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── scripts/
│   └── check-docs.sh
└── examples/
    └── react-app/
```

## 使うべき場面

- AI支援開発でチャットが長くなりすぎる
- 後から「なぜこの実装にしたのか」が分からなくなる
- Gitの差分だけでは判断理由が足りない
- 別チャットや別AIツールで作業を再開したい
- AIエージェントに守らせる開発ルールを明文化したい
- PRやIssueに検証結果と判断理由を接続したい
- 個人開発でもチーム開発に近い品質管理をしたい

## 使わない方がよい場面

- 数分で終わる単純な修正
- 一度きりの実験コード
- Gitやドキュメントで管理する必要がない作業
- ログを残すことで秘密情報が漏れる危険が高い作業

小さい作業に重い手順を強制する必要はありません。
重要なのは、作業のリスクに見合った証拠を残すことです。

## 導入方法

既存プロジェクトに導入する場合は、[docs/adoption-guide.md](docs/adoption-guide.md) から始めてください。

最初に読む順番:

1. [docs/principles.md](docs/principles.md)
2. [docs/requirement-alignment.md](docs/requirement-alignment.md)
3. [docs/practical-guide.md](docs/practical-guide.md)
4. [docs/workflow-modes.md](docs/workflow-modes.md)
5. [docs/quality-gates.md](docs/quality-gates.md)
6. [docs/adoption-guide.md](docs/adoption-guide.md)

AIと人間の役割分担は [docs/ai-human-boundary.md](docs/ai-human-boundary.md) にまとめています。
よくある失敗パターンは [docs/anti-patterns.md](docs/anti-patterns.md) にまとめています。

## セキュリティとプライバシー

devlogやプロジェクト文書には、秘密情報、認証情報、個人情報、管理画面URL、社内固有情報を含めないでください。

詳しくは [docs/security.md](docs/security.md) を参照してください。

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
