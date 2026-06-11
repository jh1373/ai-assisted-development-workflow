# Example: React App Workflow

Reactアプリ開発で、このワークフローを使う場合の例です。

## 想定

- Vite + React の個人開発プロジェクト
- フェーズごとに機能を分けて開発する
- 1タスク1セッションで作業する
- 作業終了時にdevlogを残す

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
