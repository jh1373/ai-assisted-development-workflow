# Project Structure Map

新規プロジェクトの全ファイル構造、主要な責務、構造差分を、人間とAIが同じ情報から確認するための機能です。

## 目的

- 全ファイルと全ディレクトリをlocalhostで見やすく確認する
- 主要ディレクトリと重要ファイルの役割を明文化する
- AIが古いDIRECTORY_MAPを信じて誤った場所を変更することを防ぐ
- 追加、削除、移動を機械的に検出する
- Project Initialization、session-start、session-end、CIで同じ判定を使う

ファイル内容は走査、保存、配信しません。扱うのは相対パス、種類、合意済みの役割と境界だけです。

## 設計上の参考

[Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) の「プロジェクト全体を視覚的に把握できる」「変更後も表示を更新する」「選択項目の詳細を確認できる」という考え方を参考にしています。

コード、依存パッケージ、知識グラフ、AI解析処理はコピーしていません。このリポジトリでは、ソースコードの意味解析ではなく、全パス、合意済みの責務、禁止事項、構造差分を安全かつ決定的に扱う独自実装にしています。

## 正式な情報源

### `.ai-workflow/directory-map.json`

人間とAIが合意した役割、境界、タスク別の参照先を保存する正本です。

### `.ai-workflow/directory-snapshot.json`

`Verified`時点の全パスと種類を保存する生成ファイルです。ファイル内容や内容ハッシュは含みません。

### `docs/DIRECTORY_MAP.md`

JSON正本から生成する、人間とAI向けの要約です。直接編集しません。

### `.ai-workflow/directory-map.ignore`

`.gitignore`に加えて、構造走査から除外するパターンを保存します。

## 状態

| Fixed output | Meaning |
|---|---|
| `DIRECTORY_MAP_PROVISIONAL` | コード作成前または実構成との照合前 |
| `DIRECTORY_MAP_VERIFIED` | 現在の構造が承認済み基準線と一致している |
| `DIRECTORY_MAP_DRIFT_DETECTED` | Verified後に追加、削除、移動、種類変更がある |
| `DIRECTORY_MAP_INVALID` | JSON、snapshot、役割定義などが不正 |
| `DIRECTORY_MAP_CHECK_FAILED` | Python、権限、ファイル読み取りなどで検査できない |

状態はAIが文書の雰囲気から推測しません。

## 役割の決め方

画面では、すべての項目に役割と根拠を表示します。

1. `explicit`: JSONに個別登録された役割
2. `explicit-pattern`: JSONのパターンに一致した役割
3. `convention`: READMEや拡張子などの一般的な規則
4. `inherited`: 最も近い親ディレクトリから継承した役割
5. `unclassified`: 根拠のある役割を割り当てられない

AIは`unclassified`を推測で確定しません。基準線を`Verified`にする前に、明示、パターン、慣例、親からの継承のいずれかで役割を説明できる状態にします。

## コマンド

状態確認:

```bash
python scripts/project-structure.py validate
```

差分確認:

```bash
python scripts/project-structure.py diff
```

Markdown再生成:

```bash
python scripts/project-structure.py generate
```

初回の構造承認後にVerifiedへ変更:

```bash
python scripts/project-structure.py verify --verified-by "User"
```

Verified後、確認済みの構造差分を新しい基準線として受け入れる:

```bash
python scripts/project-structure.py refresh --by "User"
```

localhost画面:

```bash
python scripts/project-structure.py serve --open-browser
```

起動時に、一時トークンを含む`http://127.0.0.1:4173/`のURLを表示します。

### Windowsでワンクリック起動する

新規プロジェクトのルートにある`open-project-structure-map.cmd`をダブルクリックします。

1. `py -3`または`python`を検出する
2. Python 3.10以降か確認する
3. localhostサーバーを起動する
4. token付きURLを既定ブラウザで開く

起動中はコマンド画面を閉じません。終了するときは、その画面で`Ctrl+C`を押します。

Pythonがない、Pythonが古い、ポートが使用中、JSONが不正などの場合は、エラー内容を表示して画面を保持します。ツールを自動インストールすることはありません。

## localhost画面

- 全ファイルと全ディレクトリを表示する
- 2秒ごとに構造変更を確認する
- 構造が変わった場合だけツリーを更新する
- パス、役割、役割の根拠で検索・絞り込みできる
- 追加、削除、未分類を強調する
- 選択項目の責務、境界、関連タスクを表示する
- ページ再読み込みなしで更新する

画面は閲覧専用です。ブラウザから役割や基準線を書き換えることはできません。

## Project Initialization

コード作成前は、予定している主要構造と責務をJSONへ記録し、`status`を`provisional`にします。

存在しない予定パスがあっても、Provisionalでは失敗にしません。

## 最初の構築タスク

実際のプロジェクト構成を作成した後、次を行います。

1. `diff`で実構成を確認する
2. 未分類項目へ役割を追加するか、親の役割を適用する
3. 登録済みパスの欠落を解消する
4. ユーザーが構造と責務を確認する
5. `verify --verified-by`を実行する

未分類、登録済みパス欠落、走査警告が残る場合、`verify`は失敗します。

## session-start

Initialization Gateの後で構造チェッカーを1回実行します。

- Provisional: 初期構築タスクに限り進める
- Verified: 通常タスクへ進める
- Drift Detected: 差分を確認し、地図を修復するまで実装へ進まない
- Invalid / Check Failed: 原因を報告し、状態を推測しない

## session-end

構造差分がある場合、追加・削除・移動と役割への影響を確認します。

承認済みの構造変更ならJSONを更新し、`refresh`でsnapshotとMarkdownを再生成します。

## CI

CIではlocalhostを起動せず、次だけを実行します。

```bash
python scripts/project-structure.py validate --ci
```

Provisionalは許容します。Verified後のドリフト、Invalid、Check FailedはCIを失敗させます。

## セキュリティ

- サーバーは`127.0.0.1`だけで待ち受ける
- 起動ごとに新しい一時トークンを生成する
- APIはトークンなしのアクセスを拒否する
- ファイル内容を読まない、保存しない、配信しない
- シンボリックリンク先を走査しない
- 上位ディレクトリへ出るパスを拒否する
- リポジトリ全体を静的配信しない
- Content Security Policyなどの保護ヘッダーを付ける

## Python

Python 3.10以降を推奨します。外部Pythonパッケージは使用しません。

Pythonが利用できない場合、構造チェッカーは`DIRECTORY_MAP_CHECK_FAILED`を返します。AIはツールを勝手にインストールせず、ユーザーへ確認します。
