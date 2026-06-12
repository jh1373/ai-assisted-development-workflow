# Implementation Plan Example: Search Empty State

## 目的

検索結果が0件のときに、空白画面ではなく空状態メッセージを表示する。

## 背景

検索フォームの初期実装では、結果がある場合の表示だけを確認していた。
0件時に何も表示されないと、検索が動いていないのか、結果がないのか判断しにくい。

## Requirement Alignment

- [x] ユーザーの元要望を確認した
- [x] AI側の理解を要約した
- [x] 不明点、曖昧な点、懸念点を洗い出した
- [x] AIが置いた仮定を明示した
- [x] 必要なユーザー確認を行った
- [x] 未回答の重要な不明点が残っていない

確認メモ:

- ユーザー要望は「検索結果がないときに空白ではなく状態が分かる表示にしたい」
- 今回はUI表示のみを対象にし、API接続や検索条件のURL同期は対象外とする
- ローディング状態との分岐はAPI接続時に改めて扱う

## 対象範囲

### 変更するもの

- `SearchResults` component
- `SearchResults` test
- 必要に応じて空状態用の文言

### 変更しないもの

- API接続
- 検索条件のURL同期
- デザイン全体の変更

## Directory Context

Related directories:

- `src/features/search/`
- `src/components/`
- `src/types/`

Responsibilities:

- `src/features/search/` は検索画面、検索結果表示、検索状態を扱う
- `src/components/` は再利用UIを扱う
- `src/types/` は検索結果の共有型を扱う

Boundaries not to cross:

- API接続は今回追加しない
- 検索条件のURL同期は今回扱わない
- 検索精度改善と0件時の表示改善を混ぜない

Files to inspect before implementation:

- `src/features/search/`
- `src/components/SearchResults.tsx`
- `src/components/SearchResults.test.tsx`

Directory Map update candidate:

- none: 既存の検索機能ディレクトリ内のUI改善であり、主要ディレクトリや責務は変わらない

## Workflow Mode

Standard

Mode selection reason:

- 通常のUI機能追加であり、複数ファイルの変更とテスト追加を含むため、デフォルトのStandard modeで進める
- 認証、権限、課金、個人情報、データ移行、本番設定には触れないため、Strict modeには上げない
- 挙動変更を含むため、Minimal modeには下げない

Mode change during work:

- なし

理由:

- 検索結果UIの通常機能追加であり、複数ファイルの変更とテスト追加を含む
- 認証、課金、個人情報、データ移行、本番設定には触れない

## 実装方針

1. 検索結果が0件の条件を確認する
2. 0件時のメッセージを表示する
3. 結果あり、結果なしのテストを追加する
4. 手動で検索結果0件の状態を確認する

## 影響範囲

- 検索結果表示
- 0件時のユーザー体験
- テストケース

## リスク

- 結果取得前のローディング状態と0件状態を混同する可能性がある
- 文言に依存しすぎたテストになる可能性がある

## Security and Privacy

- 秘密情報、個人情報、認証、権限への影響はない
- ログ出力や外部APIレスポンスの保存は行わない

## Rollback / Recovery

- 問題が出た場合は `SearchResults` の空状態表示変更と追加テストを戻す
- データ変更はないため、データ復旧は不要

## 検証方法

```bash
npm test
npm run build
```

手動確認:

- 結果があるキーワードで検索する
- 結果がないキーワードで検索する

## 完了条件

- 結果0件時に空状態メッセージが表示される
- 結果ありの表示が壊れていない
- テストとビルドが通る
