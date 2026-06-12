# Directory Map Example

この例では、検索機能を持つReactアプリの主要ディレクトリと責務を示します。

## Directory Structure

```text
src/
  components/   再利用UIコンポーネント
  features/     機能単位の実装
  data/         モックデータ
  types/        共有型定義
```

## Responsibilities

| Path | Responsibility | Notes |
|---|---|---|
| `src/components/` | 再利用UIコンポーネント | 機能固有の状態管理を持ちすぎない |
| `src/features/search/` | 検索画面、検索結果表示、検索状態 | API接続は次フェーズまで追加しない |
| `src/data/` | モックデータ | 本番APIレスポンスの代わりに使う |
| `src/types/` | 検索結果などの共有型 | UI文言や表示判断を置かない |

## Task Routing Guide

| Task Type | Start Here | Also Check | Avoid |
|---|---|---|---|
| 検索結果の表示変更 | `src/features/search/`, `src/components/` | tests | API仕様変更 |
| 0件時のUI改善 | `src/features/search/` | `src/components/`, tests | 検索精度改善 |
| API接続 | API integration path | `src/types/`, loading/error states | モック前提のまま公開 |

## Boundaries

- Phase 2ではAPI接続を追加しない
- 検索条件のURL同期は今回のタスクに含めない
- 0件時の表示改善と検索精度改善を混ぜない

## Update Triggers

- `src/features/search/` の責務が変わった場合は更新する
- API接続用の主要ディレクトリを追加した場合は更新する
- 既存コンポーネント内の小さな文言修正だけなら更新不要
