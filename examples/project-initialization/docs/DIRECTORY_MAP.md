# Directory Map: AI Meal Planning Experiment

Map Status: Provisional

コード作成前の予定構成です。最初の実装後に実構成と照合します。

## Directory Structure

```text
src/
  app/          アプリの入口
  features/     献立入力と提案表示
  components/   再利用UI
  data/         初期検証用の固定サンプル
tests/          主要利用フローのテスト
```

## Responsibilities

| Path | Responsibility | Notes |
|---|---|---|
| `src/app/` | 初期化と画面構成 | 機能ロジックを置きすぎない |
| `src/features/` | 献立入力と提案表示 | 初期検証の中心 |
| `src/components/` | 再利用UI | 機能固有ならfeaturesへ置く |
| `src/data/` | 固定サンプル | 個人情報を置かない |

## Boundaries

- 最初のタスクで認証、保存、課金を追加しない
- AI API接続を固定サンプル表示と混ぜない
- 個人情報を収集しない

## Update Triggers

- 最初の実装後に実際の構成と照合する
- AI API接続用の責務を追加するときに更新する
