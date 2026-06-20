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
ROADMAPとPROJECT_STATUSを読む
→ Project Structure Gateを実行する
→ 今回扱うタスクを選ぶ
→ DIRECTORY_MAPで今回読むべき範囲を絞る
→ ユーザー要望とAI側の理解を揃える
→ docs/tasks/ にタスク記録を作る
→ Workflow Modeを判定する
→ implementation-plan-example.md で計画する
→ 実装する
→ completion-review-example.md で漏れを確認する
→ devlog-example.md で判断理由を残す
```

## セッション開始時

```bash
git status --short --branch
python ../../scripts/project-structure.py --root . validate --require-generated
npm test
```

確認するドキュメント:

- `docs/PROJECT_STATUS.md`
- `docs/ROADMAP.md`
- `docs/DIRECTORY_MAP.md`
- `docs/ARCHITECTURE.md` がある場合
- 最新の `docs/devlog/`

## セッション終了時

```bash
npm test
npm run build
git diff --check
```

作成または更新するもの:

- `docs/tasks/YYYY-MM-DD-HHMM-task-name/`
- `docs/devlog/YYYY-MM-DD/HHMM-task-name.md`
- 必要に応じて `docs/PROJECT_STATUS.md`
- 必要に応じて `docs/ROADMAP.md`
- 構造や責務が変わる場合は `.ai-workflow/directory-map.json`
- JSON正本を変えた場合は、生成された `docs/DIRECTORY_MAP.md`

## 例ファイル

- `implementation-plan-example.md`: 実装前の計画例
- `completion-review-example.md`: 完了前レビュー例
- `devlog-example.md`: 作業後の判断ログ例
- `.ai-workflow/directory-map.json`: この例の構造と責務の正本
- `docs/DIRECTORY_MAP.md`: JSON正本から生成した例
