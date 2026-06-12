# Directory Map

このファイルは、プロジェクトの主要ディレクトリと責務を説明するための地図です。
AIエージェントは、実装前にこのファイルを読み、今回のタスクで確認すべき範囲を絞ります。

コード全体を読むための一覧ではありません。
主要な入口、責務、触ってよい範囲、触ってはいけない境界を短く保つことを優先します。

## Directory Structure

```text
src/
  app/          アプリ全体の初期化、ルーティング
  pages/        ページ単位の画面
  components/   再利用UIコンポーネント
  features/     機能単位の実装
  api/          API通信
  domain/       業務ルール
  types/        型定義
  utils/        汎用ユーティリティ
```

## Responsibilities

| Path | Responsibility | Notes |
|---|---|---|
| `src/app/` | アプリ全体の初期化、ルーティング | 機能固有ロジックを置かない |
| `src/pages/` | ページ単位の画面構成 | 業務ロジックを詰め込みすぎない |
| `src/components/` | 再利用UIコンポーネント | 特定機能専用なら `features/` を検討する |
| `src/features/` | 機能単位の実装 | 関連UI、hooks、testsを機能単位でまとめる |
| `src/api/` | API通信、レスポンス整形 | UI表示判断を持たない |
| `src/domain/` | 業務ルール | ReactなどUIフレームワークに依存しない |
| `src/types/` | 共有型定義 | 特定機能だけの型は機能側に置く |
| `src/utils/` | 汎用ユーティリティ | 特定機能専用の処理を置かない |

## Task Routing Guide

| Task Type | Start Here | Also Check | Avoid |
|---|---|---|---|
| UI表示変更 | `src/pages/`, `src/components/` | `src/features/`, tests | API仕様変更 |
| 機能追加 | `src/features/` | `src/api/`, `src/types/`, tests | 共通層への不要な追加 |
| API接続変更 | `src/api/` | `src/types/`, error handling, tests | UIへの直接実装 |
| 業務ルール変更 | `src/domain/` | related feature tests | UIフレームワーク依存 |
| 認証、権限変更 | auth-related paths | route guards, storage, security notes | ad hoc token handling |

## Boundaries

- UI層はAPIレスポンスの生データ構造に強く依存しない
- Domain層はUIフレームワークに依存しない
- API通信層は表示文言や画面状態を持たない
- 認証情報、トークン、個人情報をログに出さない
- 新しい外部依存や大きな責務変更はADR候補として扱う

## Update Triggers

`DIRECTORY_MAP.md` はsession-startで必ず読みます。
session-endでは更新要否を必ず確認します。
ただし、更新するのは構造や責務に影響があった場合だけです。

更新する例:

- 新しい主要ディレクトリを追加した
- 既存ディレクトリの責務を変えた
- ファイル配置ルールを変えた
- タスク別の参照先が変わった
- 次回のAIが迷いそうな構成変更をした

更新しない例:

- 既存ディレクトリ内の小さなUI変更
- 文言修正
- テスト追加のみ
- README更新のみ
- ディレクトリ責務に影響しない小さな修正
