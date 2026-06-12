# Example: React App Workflow

Reactアプリ開発で、このワークフローを使う場合の例です。

## 想定

- Vite + React の個人開発プロジェクト
- フェーズごとに機能を分けて開発する
- 1タスク1セッションで作業する
- 作業終了時にdevlogを残す

## この例で扱うタスク

検索結果が0件のときに、空状態メッセージを表示するタスクを例にしています。

流れ:

```text
PROJECT_STATUSを読む
→ ユーザー要望とAI側の理解を揃える
→ implementation-plan-example.md で計画する
→ 実装する
→ completion-review-example.md で漏れを確認する
→ devlog-example.md で判断理由を残す
```

## セッション開始時

```bash
git status --short --branch
npm test
```

確認するドキュメント:

- `docs/PROJECT_STATUS.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- 最新の `docs/devlog/`

## セッション終了時

```bash
npm test
npm run build
git diff --check
```

作成または更新するもの:

- `docs/devlog/YYYY-MM-DD/HHMM-task.md`
- 必要に応じて `docs/PROJECT_STATUS.md`
- 必要に応じて `docs/ROADMAP.md`

## 例ファイル

- `implementation-plan-example.md`: 実装前の計画例
- `completion-review-example.md`: 完了前レビュー例
- `devlog-example.md`: 作業後の判断ログ例
