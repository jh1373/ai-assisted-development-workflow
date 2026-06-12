# Task Records

タスク記録は、1タスクの認識合わせ、計画、完了レビューをチャット履歴ではなくファイルとして残すための置き場です。

devlogは作業後の判断ログです。
タスク記録は、実装前後の合意内容と確認結果を残します。

実際の成果物はこの場所には置きません。
コード、テスト、画像、設定ファイルなどの成果物は、通常どおりプロジェクト本来の場所に置きます。
`docs/tasks/` に置くのは、その成果物を作るまでに何を確認し、どう判断し、どう完了確認したかの記録です。

## 基本ルール

- 1タスクにつき1つのタスク記録フォルダを作る
- requirement alignment、implementation plan、completion reviewはチャットだけに残さない
- 小さいMinimal作業では短くしてよいが、目的、範囲、検証方法、完了判断は残す
- devlogは従来どおり `docs/devlog/` に残し、タスク記録からリンクする
- ADRを作成した場合は、タスク記録とdevlogの両方からリンクする

## 保存先

```text
docs/tasks/YYYY-MM-DD-HHMM-task-name/
```

例:

```text
docs/tasks/2026-06-12-1430-add-empty-search-state/
```

## 作成するファイル

通常は次を作成します。

```text
docs/tasks/YYYY-MM-DD-HHMM-task-name/
  requirement-alignment.md
  implementation-plan.md
  completion-review.md
```

作成時は、`templates/` のファイルをコピーして使います。

例:

```bash
mkdir -p docs/tasks/2026-06-12-1430-add-empty-search-state
cp templates/requirement-alignment.md docs/tasks/2026-06-12-1430-add-empty-search-state/requirement-alignment.md
cp templates/implementation-plan.md docs/tasks/2026-06-12-1430-add-empty-search-state/implementation-plan.md
cp templates/completion-review.md docs/tasks/2026-06-12-1430-add-empty-search-state/completion-review.md
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force docs\tasks\2026-06-12-1430-add-empty-search-state
Copy-Item templates\requirement-alignment.md docs\tasks\2026-06-12-1430-add-empty-search-state\requirement-alignment.md
Copy-Item templates\implementation-plan.md docs\tasks\2026-06-12-1430-add-empty-search-state\implementation-plan.md
Copy-Item templates\completion-review.md docs\tasks\2026-06-12-1430-add-empty-search-state\completion-review.md
```

必要に応じて追加します。

```text
docs/tasks/YYYY-MM-DD-HHMM-task-name/
  security-review.md
  rollback-plan.md
  references.md
```

## devlogとの関係

devlogは次の場所に残します。

```text
docs/devlog/YYYY-MM-DD/HHMM-task-name.md
```

タスク記録とdevlogは相互に参照します。

例:

```text
Task records:
- docs/tasks/2026-06-12-1430-add-empty-search-state/

Devlog:
- docs/devlog/2026-06-12/1430-add-empty-search-state.md
```

## 使い分け

| ファイル | 目的 |
|---|---|
| requirement-alignment.md | ユーザーとAIの認識合わせを残す |
| implementation-plan.md | 実装前の目的、範囲、検証方法を固定する |
| completion-review.md | 完了前に計画との差分、検証、残課題を確認する |
| devlog.md | 作業後の判断理由、検証結果、未完了事項を残す |
| ADR | 長期的な設計判断を残す |

## やってはいけないこと

- テンプレート本体を直接編集して作業記録にする
- requirement alignmentやimplementation planをチャットだけに残す
- completion reviewを省略してdevlogだけ残す
- devlogに長いコマンド出力やチャット全文を貼る
- 秘密情報、個人情報、管理画面URLを残す
