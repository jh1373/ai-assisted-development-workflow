# Devlog Examples

devlogは、チャットの要約ではなく、後から判断を追うための作業記録です。

このディレクトリには、どのくらいの粒度で残すと再開しやすいかの見本を置いています。

## 基本ルール

- 1タスクにつき1つのdevlogを残す
- 関連する `docs/tasks/YYYY-MM-DD-HHMM-task-name/` をdevlogから参照する
- 1チャットで複数タスクを扱った場合は、タスクごとに分ける
- 小さい修正でも、判断理由、検証結果、未完了事項は残す
- コマンド出力全文ではなく、実行したコマンドと結果を要約する
- 秘密情報、個人情報、管理画面URL、チャット全文は書かない

## 保存先の例

```text
docs/devlog/YYYY-MM-DD/HHMM-task-name.md
```

例:

```text
docs/devlog/2026-06-12/1430-add-empty-search-state.md
```

## 見本

- [standard-task-devlog.md](standard-task-devlog.md): Standard modeで通常の機能修正を行った場合の見本
