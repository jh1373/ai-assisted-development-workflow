# Directory Map Template

このファイルは、プロジェクトの主要ディレクトリと責務を説明するための地図です。
AIエージェントは、実装前にこのファイルを読み、今回のタスクで確認すべき範囲を絞ります。

Map Status: Provisional / Verified

- `Provisional`: コード作成前の予定構成、または実構成との照合前
- `Verified`: 実際のプロジェクト構成と照合済み

初期設定では、技術スタックが決まる前にWeb、モバイル、APIなどの構成を推測で埋めません。
PROJECT_BRIEFと技術方針に基づき、必要な主要ディレクトリだけを記録します。

## Directory Structure

```text
[PROJECT_ROOT]/
  [path]/    [responsibility]
```

## Responsibilities

| Path | Responsibility | Notes |
|---|---|---|
| `[path]` | `[responsibility]` | `[boundary or important note]` |

## Task Routing Guide

| Task Type | Start Here | Also Check | Avoid |
|---|---|---|---|
| `[task type]` | `[primary path]` | `[related paths or tests]` | `[boundary not to cross]` |

## Boundaries

- 秘密情報、認証情報、個人情報をログや公開文書へ出さない
- プロジェクト固有の責務境界は初期設定で追加する
- 未確定の構成はConfirmedとして固定せず、Provisionalであることを残す

## Update Triggers

`DIRECTORY_MAP.md` はsession-startで読みます。
session-endでは更新要否を確認します。
ただし、更新するのは構造や責務に影響があった場合だけです。

初期構築後に実構成と照合した場合は、`Map Status` を `Verified` に更新します。

更新する例:

- 新しい主要ディレクトリを追加した
- 既存ディレクトリの責務を変えた
- ファイル配置ルールを変えた
- タスク別の参照先が変わった
- 次回のAIが迷いそうな構成変更をした

更新しない例:

- 既存ディレクトリ内の小さな変更
- 文言修正
- テスト追加のみ
- README更新のみ
- ディレクトリ責務に影響しない修正
