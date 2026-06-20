# Project Status Template

プロジェクトの現在地を短く残すためのファイルです。
新しいセッションを始めるとき、最初に読むことを想定しています。
ROADMAPが全体計画であるのに対し、PROJECT_STATUSは直近の現在地と次の候補タスクを示します。

初期設定状態の正式な判定元ではありません。
正式な状態は `.ai-workflow/project-state.conf` と判定スクリプトを使います。

## 現在地

Project Initialization: Not started

## 最終セッション

<!-- 日時、作業名、devlogとタスク記録へのリンクを書く -->

```text
YYYY-MM-DD HH:mm: [作業名] -> docs/devlog/YYYY-MM-DD/HHMM-task-name.md
Task records -> docs/tasks/YYYY-MM-DD-HHMM-task-name/
```

## 完了済み

- starter package copied

## 進行中

-

## 次にやる候補タスク

- `workflows/project-initialization.md` を開始する

## 注意点

<!-- 次回の作業者が最初に知るべきことを書く -->

- ユーザー承認前に通常実装へ進まない
- 初期設定statusをPROJECT_STATUSから推測しない

## 検証状態

<!-- 最後に確認したテストやビルドを書く -->

```text
[command/result summary]
```

## 更新ルール

- 履歴をすべて積み上げる場所ではない
- 最新の現在地だけを書く
- 詳しい判断理由はdevlogに書く
- 次のセッションで必要な情報だけ残す
- 初期設定statusの代わりに使わない
