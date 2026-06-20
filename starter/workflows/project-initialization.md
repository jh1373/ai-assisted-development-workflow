# Project Initialization Workflow

新規プロジェクトで通常タスクを始める前に、一度だけ実行する初期設定ワークフローです。

目的は、最初からすべてを確定することではありません。
確定事項、仮説、不明点、後で決めることを区別し、最初のタスクを安全に始められる基準線を作ることです。

## 重要な原則

- 初期設定状態をAIの解釈で判定しない
- `scripts/check-initialization.sh` または `scripts/check-initialization.ps1` の固定出力を使う
- ユーザーと壁打ちする前に、AIがプロダクト要件を確定しない
- `Hypothesis` を `Confirmed` として扱わない
- `Unknown` をAIが勝手に補完しない
- すべてが確定していなくても、最初の検証タスクを安全に始められれば `ready` にできる
- `ready` への変更は、ユーザーの明示承認後だけ行う

## 状態

`.ai-workflow/project-state.conf` の `initialization_status` は次のいずれかです。

| Status | Meaning |
|---|---|
| `not_started` | 初期設定をまだ始めていない |
| `in_progress` | 壁打ち、文書作成、レビューの途中 |
| `ready` | ユーザー承認済みで、通常タスクを開始できる |
| `revisit_required` | 大きな方針変更があり、初期設定の一部を見直す必要がある |

`complete` は使いません。プロダクト方針は将来変わるため、ここで表すのは完全性ではなく開始可能性です。

## 手順

### 1. 状態を機械的に確認する

通常は `workflows/session-start.md` のStep 0で得た結果を、このセッションの判定結果として使います。
同じセッションで状態を変更していない限り、判定スクリプトを重ねて実行しません。

Project Initializationを直接開始し、このセッションでまだ判定していない場合だけ、現在の環境に合うスクリプトを1つ実行します。

Bash:

```bash
bash scripts/check-initialization.sh
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-initialization.ps1
```

出力が `INITIALIZATION_NOT_STARTED` の場合だけ、新しい初期設定を開始します。
`INITIALIZATION_IN_PROGRESS` の場合は、既存の文書を読み、前回の続きから再開します。
`INITIALIZATION_INVALID` または `INITIALIZATION_CHECK_FAILED` の場合は、未設定と推測せず、不整合をユーザーへ報告します。

### 2. 状態を `in_progress` にする

初期設定を開始することをユーザーへ伝えた後、状態ファイルを次へ変更します。

```text
schema_version=1
initialization_status=in_progress
user_approved=false
```

### 3. プロダクト構想を壁打ちする

一度に大量の質問を投げず、次の順番で少しずつ確認します。

1. 何を作ってみたいか
2. 誰のどんな問題を解決したいか
3. どんな価値を提供したいか
4. 中核となる利用場面は何か
5. 収益化を考えているか
6. 最初に何を確かめたいか
7. 今回は何を作らないか
8. 技術、期間、公開範囲、データ、安全性の制約は何か

ユーザーの回答ごとにAI側の理解を短く要約し、認識が違う場合は次へ進む前に修正します。

### 4. 情報の確度を分類する

`templates/project-brief.md` を `docs/PROJECT_BRIEF.md` として記入します。

各重要事項を次のいずれかに分類します。

| Classification | Meaning |
|---|---|
| `Confirmed` | ユーザーが現在の方針として決定した |
| `Hypothesis` | 検証前の仮説 |
| `Unknown` | まだ分からない |
| `Deferred` | 今は決めず、後のフェーズで決める |

ターゲットや収益化が未確定でも構いません。
未確定であることと、次にどう検証するかを明示します。

### 5. 初期経路を選ぶ

#### Discovery Track

プロダクト像、対象ユーザー、提供価値、収益化などに重要な仮説が残る場合に使います。
ROADMAPの最初を、調査、試作品、ユーザー確認などの検証フェーズにします。

#### Build-ready Track

対象ユーザー、中核価値、MVP、主要制約が十分に整理され、実装対象を安全に決められる場合に使います。

どちらを選んでも、仮説と不明点は隠しません。

### 6. 開発方針を決める

プロダクト要件を確認した後で、必要な範囲だけ決めます。

- 技術スタック
- 実行環境
- データ保存
- 認証や権限
- 外部サービス
- テストとビルド
- デプロイ先
- セキュリティとプライバシー
- ログ、監視、運用

Discovery Trackでは、変更しやすく戻しやすい暫定方針を優先し、未確定の本番設計を固定しません。

### 7. ROADMAPを作る

`docs/ROADMAP.md` に、プロジェクト全体のフェーズを書きます。

各フェーズに次を含めます。

- 目的
- 得たい成果または学び
- 主要タスク候補
- 完了条件
- 前提となる仮説
- 見直し条件

Discovery Trackでは、最初のフェーズを仮説検証にします。

### 8. AGENTS.mdを正式化する

初期状態の `AGENTS.md` は安全規則として使います。
プロダクト要件と開発方針が整理できた後、次をプロジェクト固有の内容へ更新します。

- プロジェクトの目的
- 技術スタック
- 実行、テスト、ビルドコマンド
- ディレクトリルール
- 変更してはいけない境界
- 依存追加ルール
- セキュリティルール
- AIがユーザーへ確認する条件
- 完了条件
- 公開、デプロイ、運用ルール

仮説を恒久的なルールとして固定しません。

### 9. PROJECT_STATUSを初期化する

最初の状態として次を記録します。

- 現在のフェーズ
- 初期設定で完了したこと
- 最初の候補タスク
- 未確定事項と注意点
- まだ実行していない検証

初期設定状態の正式な判定元はPROJECT_STATUSではなく、状態ファイルです。

### 10. DIRECTORY_MAPを作る

コード作成前は `Map Status: Provisional` とします。
予定している主要ディレクトリ、責務、境界だけを書きます。

プロジェクトの初期構築後、実際のファイル構成と照合して `Map Status: Verified` へ変更します。

### 11. 初期設定レビューを行う

`templates/initialization-review.md` を `docs/INITIALIZATION_REVIEW.md` として記入します。

AIは未確認項目を成功扱いせず、残る仮説、不明点、最初の検証タスクをユーザーへ提示します。

### 12. ユーザー承認を得る

ユーザーに次を確認します。

- 現時点のプロダクト理解で開始してよいか
- 仮説と不明点の扱いが正しいか
- ROADMAPの最初のフェーズが適切か
- AGENTS.mdのルールが適切か
- 最初のタスク候補が適切か

承認がない場合、`ready` に変更しません。

### 13. 状態を `ready` にする

ユーザーの明示承認後、次へ変更します。

```text
schema_version=1
initialization_status=ready
user_approved=true
```

判定スクリプトを再実行し、`INITIALIZATION_READY` を確認します。

### 14. 最初のタスクへ進む

通常タスクへ自動で進まず、最初の候補タスクと範囲を提示します。
ユーザーが開始を指示した後、`workflows/session-start.md` を実行します。

## `revisit_required` に戻す条件

次の変更が、現在のPROJECT_BRIEF、ROADMAP、AGENTS.mdの前提を大きく変える場合に使います。

- 対象ユーザーや解決する問題の変更
- 中核価値や収益モデルの大幅変更
- MVPの全面的な変更
- アーキテクチャや実行環境の全面変更
- データ、認証、公開範囲の重大な変更

見直しが必要になった時点で、状態を次へ変更します。

```text
schema_version=1
initialization_status=revisit_required
user_approved=false
```

小さな仕様変更では初期設定全体をやり直しません。
影響する文書だけを見直し、ユーザー承認後に再び `ready` にします。
