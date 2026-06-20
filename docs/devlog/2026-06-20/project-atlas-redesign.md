# Project Atlas再設計

## 作業テーマ

全ファイルツリー中心の構造ビューアを、初心者がプロジェクトの意味から理解できるProject Atlasへ変更した。

## 関連するタスク記録

```text
docs/tasks/2026-06-20-project-atlas-redesign/
```

## なぜやったか

従来画面は役割説明が付いていても、基本的にはフォルダを開いて見る操作と同じだった。初心者が最初に知りたいのはファイル数や配置ではなく、プロジェクトの区域、入口、処理の順番、今回見る範囲である。

## 判断したこと

### Workflow Mode

- Selected mode: Strict
- Reason: JSON契約、UI、CI、初期設定、通常タスク運用を変更するアーキテクチャ変更のため

### Directory Map

- Impact: updated
- Checker result: DIRECTORY_MAP_PROVISIONAL
- Updated JSON / snapshot / generated Markdown: schema v2 JSONと生成Markdownを更新。初回構築前のためsnapshotは未作成
- Atlas areas / Guided Tours / Task Lenses changed: 5区域、2フロー、2 Lensをstarterへ追加
- File Passports changed or intentionally inherited: 入口と中心ファイルを個別登録し、補助ファイルは親区域を継承

### 採用した方針

- 全ファイルツリーはExplorerタブとして残す。
- デフォルトを区域ベースのAtlasにする。
- 処理は自由グラフではなく、順番が明確なGuided Tourとして表示する。
- AIがファイルを作成した同じタスクでPassportを登録する。
- 一般拡張子説明より親区域のプロジェクト固有説明を優先する。
- 個別Passport100%を目的化せず、正確な継承と明示Passportを区別する。

### 見送った選択肢

- ファイル間の自由配置ネットワークグラフ
- ソースコードを読み取る依存解析
- LLM、embedding、外部データベース
- schema v1の即時廃止

### 理由

- 自由グラフは規模が増えると線が交差して初心者に読めない。作成時の意図をJSONへ残す方が、コード内容を後から推測するより安全である。

## 発生した問題と対応

- starterにUI、機能、データ区域がないため固定番号が4から始まり、欠落に見えた。層の固定番号を外し、表示中の区域数だけを示すよう修正した。
- schema v1 fixtureでは一般説明が意味情報問題となりverifyが失敗した。意味情報の強制はschema v2だけに限定して後方互換性を維持した。

## 検証

```text
自動テスト、OS別初期化テスト、文書検査、構文検査、生成物検査に成功。
localhost APIで5区域、2フロー、2 Lens、意味情報100%、問題0を確認。
1440pxと500pxのProject Atlasを画像で確認。
```

## 未完了・注意点

- Product Designスキルのローカルキャッシュが存在しなかったため、現行リポジトリと確定済み設計要件を正本として実装した。

## Definition of Done確認

- デフォルト画面が全体マップになり、処理、タスク、全ファイル、健康状態へ切り替えられる。starter、examples、運用、CI、文書、テストが同期している。

## 次にやること

- コミット、push後にGitHub Actionsを確認する。
