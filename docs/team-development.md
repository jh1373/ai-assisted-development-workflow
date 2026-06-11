# Team Development

チームでAI駆動開発を使う場合、個人開発よりも厳しく管理する必要があります。

理由は単純です。
AIが作った変更の影響が、自分だけでなく、他の開発者、レビュー担当者、CI、リリース、顧客、セキュリティに広がるからです。

## 個人開発との違い

個人開発で重要なのは、現在地、判断理由、検証結果を残すことです。

チーム開発では、それに加えて次が必要です。

- 誰が作業責任を持つか
- 誰がレビュー責任を持つか
- どの変更は人間承認が必須か
- どのCIが落ちたらマージ禁止か
- どの情報をAIに渡してよいか
- 問題が起きたときに誰が戻すか

## チームで決めるべきこと

### 1. AIに任せてよい作業

例:

- 既存コードの調査
- 小さな機能追加
- テストケースの追加
- ドキュメントの下書き
- リファクタリング候補の提示
- エラー原因の仮説出し

### 2. 人間が必ず判断する作業

例:

- 要件の確定
- アーキテクチャ変更
- 認証、権限、課金、個人情報に関わる変更
- 新しい依存ライブラリの採用
- 本番リリース判断
- ロールバック判断

詳細は [ai-human-boundary.md](ai-human-boundary.md) を参照してください。

## PR運用

AIを使った変更でも、PRでは通常の開発と同じか、それ以上に証拠を残します。

PRに書くこと:

- 何を変えたか
- なぜ変えたか
- どのAIツールを使ったか
- どの範囲をAIに任せたか
- 人間が確認した観点
- 実行したテスト、ビルド、手動確認
- 残るリスク
- 関連するtask brief、implementation plan、completion review、devlog、ADR

`.github/pull_request_template.md` を使うと、最低限の確認項目を揃えられます。

## CIと必須チェック

チーム開発では、各自の注意だけに依存しないようにします。

最低限決めること:

- lintを必須にするか
- typecheckを必須にするか
- unit testを必須にするか
- buildを必須にするか
- secret scanを必須にするか
- E2E testをどの変更で必須にするか

このリポジトリでは、文書構造と秘密情報らしき文字列を確認する入口として `scripts/check-docs.sh` と `.github/workflows/docs-check.yml` を用意しています。

## Strict Mode対象

次の変更は、チームではStrict modeにします。

- 認証
- 権限
- 課金
- 個人情報
- データ移行
- 本番設定
- 外部サービス連携
- 依存ライブラリ追加
- 大きな設計変更
- 公開リリース

Strict modeでは、少なくとも次を残します。

- implementation plan
- security review
- rollback plan
- completion review
- devlog
- 必要ならADR
- 人間の承認

## レビュー担当者が見ること

レビュー担当者は、AIが使われたかどうかより、次を確認します。

- 目的に対して実装が合っているか
- 範囲外の変更がないか
- AI生成コードを人間が読んでいるか
- テストと手動確認が十分か
- 失敗やスキップが隠されていないか
- セキュリティとプライバシーの影響が確認されているか
- 次の作業者が履歴を追えるか

## チーム導入時の最小構成

最初から重い運用にする必要はありません。

チームで始めるなら、最低限これだけ導入します。

```text
AGENTS.md
docs/PROJECT_STATUS.md
docs/devlog/
templates/implementation-plan.md
templates/completion-review.md
.github/pull_request_template.md
```

Strict modeが必要なプロジェクトでは、次も追加します。

```text
docs/strict-mode.md
docs/quality-gates.md
templates/security-review.md
templates/rollback-plan.md
templates/adr.md
```

## 注意

AIを導入しても、チームの開発力が自動で上がるわけではありません。

AIは、既にある開発プロセスの強みも弱みも増幅します。
レビュー、テスト、CI、ドキュメント、責任範囲が弱いチームでは、AIによって不明瞭な変更が増える可能性があります。

チームでAI駆動開発を使うなら、まず「誰が何を判断するか」と「何を証拠として残すか」を決めてください。
