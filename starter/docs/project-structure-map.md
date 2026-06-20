# Project Atlas

Project Atlasは、ファイルを並べるだけのツリーではありません。新規プロジェクトの「どの区域が何を担当し、処理がどこを通り、今回どこを見るべきか」を初心者向けの言葉で確認するread-only localhost画面です。

## 解決する問題

通常のファイルツリーから分かるのは名前と配置だけです。Project Atlasは次を可視化します。

- どの区域がプロダクトのどの部分を担当するか
- 入口となるファイルはどれか
- ある処理がどの順番で進むか
- 今回のタスクでどこを見て、どこを触らないか
- ファイルの説明が古い、または不足していないか

ソースコード内容は走査、保存、配信しません。

## 5つの画面

### 全体マップ

区域を、ユーザー画面、機能、データ、運用基盤、開発手順、記録の層に分けます。最初から全ファイルを見せず、プロジェクト全体の仕組みを表示します。

### 処理の流れ

Guided Tourとして、ユーザー操作や開発手順を順番に表示します。各ステップから該当ファイルのPassportへ移動できます。

### タスク案内

Task Lensとして、最初に見る場所、関連して確認する場所、今回触らない場所を分けます。

### 全ファイル

従来のツリーです。全項目へ到達できますが、デフォルト画面ではありません。

### 説明の健康状態

説明がない項目、一般説明だけのファイル、壊れた参照、意味情報カバレッジ、個別Passportカバレッジを表示します。

## File Passport

入口、中心ファイル、重要ファイルには個別Passportを登録します。

主な項目:

- path、display_name、beginner_summary
- responsibility、not_responsible_for
- when_to_change、inputs、outputs
- depends_on、area、layer、importance、evidence
- boundaries、task_types

AIはファイルを作成または改名した同じタスク内でPassportを更新します。後からファイル名やコード内容だけを見て、説明を推測で確定しません。

補助ファイルは、正確であれば親区域の説明を継承できます。個別Passportと継承説明は画面上で区別します。

## schema version 2

.ai-workflow/directory-map.jsonが意味情報の正本です。

| Section | Role |
|---|---|
| areas | プロジェクトを役割区域と層に分ける |
| nodes | ディレクトリ責務とFile Passport |
| flows | Guided Tourの処理順序 |
| task_lenses | タスク別の確認範囲 |
| conventions | ほかに説明がない場合の補助規則 |

schema version 1も読み取れますが、区域、Guided Tour、Task Lensは表示されません。新規プロジェクトはversion 2を使用します。

## 役割の根拠

優先順位:

1. 個別File Passport
2. 登録されたパターン
3. 最も近い親区域・ディレクトリ
4. 一般ファイル名・拡張子
5. 説明なし

一般的な「Markdownファイル」より、親区域の「プロジェクト計画を保存する」の方を優先します。

## 構造と意味情報

構造と説明は別に評価します。

- Structure: 承認済みパスと種類が一致するか
- Semantic Coverage: 全項目を根拠付きで説明できるか
- Individual Passport Coverage: ファイル単位の個別説明があるか
- Broken References: Passport、Guided Tour、Task Lensの参照が壊れていないか

予定パスはProvisional中に存在しなくても構いません。JSONのpatternで計画済みなら、壊れた参照として扱いません。

## Project Initialization

コード作成前に次を設計します。

1. 役割区域と層
2. 各区域の初心者向け説明
3. 入口となる予定ファイル
4. 主要な処理や開発手順のGuided Tour
5. 最初のタスク向けTask Lens
6. 触ってはいけない境界

初期状態はDIRECTORY_MAP_PROVISIONALです。実構成と意味情報をユーザーが確認した後だけVerifiedへ進めます。

## 通常タスク

session-startではTask Lensを全ファイルツリーより先に確認します。対応Lensがなければ追加候補としてimplementation planへ記録します。

入口または中心ファイルを作成、改名、責務変更した場合、同じ変更内でPassportを更新します。

session-endでは構造差分だけでなく、区域、Passport、Guided Tour、Task Lensへの影響を確認します。

## コマンド

Windowsではプロジェクト直下のopen-project-structure-map.cmdをダブルクリックします。

    python scripts/project-structure.py validate
    python scripts/project-structure.py diff
    python scripts/project-structure.py generate
    python scripts/project-structure.py serve --open-browser

初回承認:

    python scripts/project-structure.py verify --verified-by "User"

承認済み変更の基準線更新:

    python scripts/project-structure.py refresh --by "User"

## 固定出力

| Output | Meaning |
|---|---|
| DIRECTORY_MAP_PROVISIONAL | 初回構築と意味情報の確認中 |
| DIRECTORY_MAP_VERIFIED | 承認済み構造と一致 |
| DIRECTORY_MAP_DRIFT_DETECTED | 承認後の構造差分あり |
| DIRECTORY_MAP_INVALID | JSON、snapshot、意味情報の形式が不正 |
| DIRECTORY_MAP_CHECK_FAILED | Python、権限、読み取りなどで検査不能 |

## セキュリティ

- 127.0.0.1だけで待ち受ける
- 起動ごとに一時tokenを生成する
- APIはtokenなしアクセスを拒否する
- リポジトリ全体を静的配信しない
- ソースコード内容を読まない、保存しない、配信しない
- symlink先を走査しない
- 上位パスへ出る定義を拒否する
- Content Security Policyを付ける
- 画面からJSONや基準線を書き換えない

## Python

Python 3.10以降を推奨します。外部Pythonパッケージは使用しません。

Pythonがない場合はDIRECTORY_MAP_CHECK_FAILEDとして扱います。ランチャーもツールを自動インストールしません。
