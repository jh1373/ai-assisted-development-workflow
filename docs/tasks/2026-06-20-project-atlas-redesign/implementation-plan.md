# Project Atlas Redesign Implementation Plan

## 目的

Project Structure Mapを、説明付きファイルツリーから、初心者がプロジェクトの区域、処理、タスク範囲、ファイルの存在理由を理解できるProject Atlasへ再設計する。

## Requirement Alignment

- [x] 全ファイルへ到達できる機能は残す
- [x] デフォルト画面は役割区域の全体マップにする
- [x] File Passport、Guided Tour、Task Lens、Healthを追加する
- [x] ソースコード内容を読まない安全境界を維持する
- [x] starter、examples、workflow、CI、文書を同期する
- [x] 実装、検証、コミット、pushまで行う

## 対象範囲

- `.ai-workflow/directory-map.json` schema version 2
- `scripts/project-structure.py`の意味情報検証とAPI
- localhost viewerの5画面化
- Project Initialization、session-start、session-end、AGENTS、templates
- starter、初期設定例、React例、生成DIRECTORY_MAP、CI検査

## 変更しないもの

- 127.0.0.1限定、token、read-only、固定asset配信
- path-only snapshotと構造差分
- ソースコード内容の解析
- schema version 1の読み取り互換性

## Workflow Mode

- Strict

Mode selection reason:

- JSON契約、UI情報設計、CI判定、初期設定と通常タスクの運用モデルを同時に変更するアーキテクチャ変更のため。

## 実装方針

1. schema v2へareas、Passport、flows、task_lensesを追加する。
2. 意味情報カバレッジと壊れた参照を機械検査する。
3. Atlas、Tour、Lens、Explorer、Healthの5画面を実装する。
4. AIがファイル作成時にPassportを登録する運用へ変更する。
5. starterとexamplesをv2へ移行して生成文書を更新する。
6. 自動テスト、OS別テスト、実画面、localhostセキュリティを確認する。

## Security and Privacy

- 意味情報は人間とAIが作成時に登録したJSONだけを使用し、ソース内容から推測しない。

## Rollback / Recovery

- schema v1読み取り互換性を残す。問題時はUIをExplorer中心へ戻しても構造検証CLIとsnapshotを継続利用できる。

## 完了条件

- starterで区域、Tour、Lensが表示され、意味情報カバレッジ100%、壊れた参照0件となる。
- 5画面とFile Passportがlocalhostで表示される。
- 全テストとGitHub Actionsが成功する。
