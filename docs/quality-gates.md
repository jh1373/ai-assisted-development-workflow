# Quality Gates

品質ゲートとは、作業を次に進める前に確認する関門です。

AI駆動開発では、実装速度が上がる一方で、誤った変更や範囲外の変更も速く混ざります。
そのため、作業の途中と完了前に、証拠をもって確認する関門を置きます。

## 0. Requirement Alignment Gate

すべての作業で最初に確認します。

- ユーザーの元要望をAIが正しく要約したか
- AI側の理解をユーザーに見える形で示したか
- 不明点、曖昧な点、懸念点を洗い出したか
- AIが置いた仮定を明示したか
- ユーザー確認が必要な点を質問したか
- 未回答の重要な不明点が残ったまま実装へ進んでいないか

証拠:

- requirement alignment
- task brief
- issue
- user confirmation note

このゲートを通過できない場合、implementation planや実装に進みません。

## 1. Scope Gate

実装前に確認します。

- 目的は明確か
- 完了条件は明確か
- 変更する範囲は明確か
- 変更しない範囲は明確か
- 不明点をAIが勝手に補完していないか

証拠:

- task brief
- implementation plan
- issue

## 2. Context Gate

作業開始時に確認します。

- Git状態を確認したか
- プロジェクトルールを読んだか
- 現在地を復元したか
- 直近のdevlogや未完了事項を確認したか
- 既存のテスト状態を把握したか

証拠:

- session start summary
- `git status --short --branch`
- `PROJECT_STATUS.md`

## 3. Diff Gate

実装中または完了前に確認します。

- 予定外のファイルが変わっていないか
- 不要なリファクタリングが混ざっていないか
- AIが既存の設計を無視していないか
- 生成コードを人間が読んだか
- 失敗した試行や方針変更を記録したか

証拠:

- git diff
- completion review
- devlog

## 4. Verification Gate

完了前に確認します。

- テストを実行したか
- ビルドを実行したか
- 型チェックやlintを実行したか
- UIや操作が関係する場合、手動確認したか
- 失敗やスキップを隠していないか

例:

```bash
npm test
npm run build
npm run lint
git diff --check
```

証拠:

- 実行コマンド
- pass/fail/skippedの結果
- スキップ理由
- 手動確認の観察結果

## 5. Security Gate

公開前、PR前、Strict modeで確認します。

- APIキー、トークン、Cookie、秘密鍵が含まれていないか
- 個人情報や顧客情報が含まれていないか
- 認証や権限の動作が変わっていないか
- ログやスクリーンショットに秘密情報がないか
- 外部サービスに送るデータが増えていないか

証拠:

- security review
- secret scan
- PR security section

## 6. Recovery Gate

本番影響、データ影響、課金、権限、公開リリースがある場合に確認します。

- 問題が起きたときに戻せるか
- feature flagや設定で無効化できるか
- データを戻せるか
- ロールバック後に何を確認すればよいか
- 誰がロールバック判断をするか

証拠:

- rollback plan
- release note
- monitoring or manual check notes

## 7. Review Gate

PRまたは作業完了前に確認します。

- AI生成コードを人間がレビューしたか
- Strict mode対象なのに通常レビューで済ませていないか
- 残るリスクをレビュー担当者が理解できるか
- 最終判断者が明確か

証拠:

- PR review
- completion review
- human approval note

## モード別の最低ライン

| Gate | Minimal | Standard | Strict |
|---|---|---|---|
| Requirement Alignment | 必須 | 必須 | 必須 |
| Scope | 必須 | 必須 | 必須 |
| Context | 推奨 | 必須 | 必須 |
| Diff | 推奨 | 必須 | 必須 |
| Verification | 必須 | 必須 | 必須 |
| Security | 推奨 | 影響があれば必須 | 必須 |
| Recovery | 不要なことが多い | 影響があれば必須 | 必須 |
| Review | 自己確認 | 自己確認またはPR | 人間承認必須 |

## 悪い完了判断

次の状態は完了ではありません。

- AIが実装したので完了
- 画面を一度見たので完了
- テストは未実行だが小さい変更なので完了
- 失敗したチェックをPRに書いていない
- 認証や権限に触れたがセキュリティ確認がない
- 変更理由がチャットにしか残っていない

完了とは、実装が終わった状態ではなく、検証され、説明でき、必要なら戻せる状態です。
