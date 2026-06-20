# New Project Adoption Guide

新規プロジェクトへこのワークフローを導入し、最初の通常タスクを安全に開始できる状態にするための手順です。

## 目的

- 導入直後の初期設定と、初期設定後の通常タスクを分離する
- AIに初期設定状態を推測させない
- ユーザーとAIが壁打ちしてプロダクトの基準線を作る
- 確定事項、仮説、不明点、後で決めることを区別する
- すべてが未確定でも、最初の検証タスクを安全に始められるようにする
- ユーザー承認なしに通常実装へ進まない

## 初期設定と通常タスク

このワークフローには2つの入口があります。

```text
初回のみ: workflows/project-initialization.md
初期設定後の毎回: workflows/session-start.md
```

Project Initializationは、最初から完璧なプロダクト計画を作る工程ではありません。
通常タスクを始めるために必要な前提と、不確実性の扱いを合意する工程です。

## Step 1: 新規プロジェクトを用意する

プロダクト用の新しいGitリポジトリを用意します。
このワークフロー用リポジトリの中でプロダクトを実装するのではなく、プロダクト側へ `starter/` を配置します。

Bash:

```bash
cp -R starter/. /path/to/new-project/
```

PowerShell:

```powershell
Copy-Item -Path .\starter\* -Destination C:\path\to\new-project -Recurse -Force
Copy-Item -Path .\starter\.github -Destination C:\path\to\new-project -Recurse -Force
Copy-Item -Path .\starter\.ai-workflow -Destination C:\path\to\new-project -Recurse -Force
```

PowerShellでは、隠しディレクトリの `.github/` と `.ai-workflow/` を明示的にコピーします。

## Step 2: 初期状態を機械的に確認する

Bash:

```bash
bash scripts/check-initialization.sh
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-initialization.ps1
```

導入直後は次を返します。

```text
INITIALIZATION_NOT_STARTED
```

AIはMarkdownの内容から初期設定状態を推測しません。

## Step 3: Project Initializationを開始する

`workflows/project-initialization.md` を読み、状態を次へ変更します。

```text
schema_version=1
initialization_status=in_progress
user_approved=false
```

この状態のまま途中でセッションを終了しても構いません。
次回は `INITIALIZATION_IN_PROGRESS` を受け取り、既存の初期設定文書から続けます。

## Step 4: プロダクト構想を壁打ちする

AIは一度にすべてを聞かず、次を少しずつ確認します。

1. どのようなものを作ってみたいか
2. 誰のどのような問題を解決したいか
3. どのような価値を提供したいか
4. 中核となる利用場面は何か
5. 収益化をどの程度考えているか
6. 最初に何を確かめたいか
7. 今回は何を作らないか
8. 技術、公開、データ、安全性の制約は何か

質問ごとにAI側の理解を提示し、認識が違う場合は修正してから次へ進みます。

## Step 5: PROJECT_BRIEFを作る

`templates/project-brief.md` を使い、`docs/PROJECT_BRIEF.md` を記入します。

重要事項を次へ分類します。

| Classification | Meaning |
|---|---|
| Confirmed | ユーザーが現在の方針として決めた |
| Hypothesis | 検証前の仮説 |
| Unknown | まだ分からない |
| Deferred | 今は決めず、後で決める |

ターゲットや収益化が不明でも、初期設定を失敗扱いにはしません。
AIが勝手に埋めず、検証方法または見直し時期を記録します。

## Step 6: 初期経路を選ぶ

### Discovery

対象ユーザー、中核価値、収益化、MVPなどに重要な仮説が残る場合に使います。
ROADMAPの最初を調査、試作品、ユーザー確認などの検証フェーズにします。

### Build-ready

対象ユーザー、中核価値、MVP、主要制約が十分に整理され、実装対象を安全に決められる場合に使います。

経路はプロジェクトの格付けではなく、現在の不確実性に合わせるためのものです。

## Step 7: 開発方針を決める

プロダクト要件を確認した後で、必要な範囲の技術方針を決めます。

- 実行環境と技術スタック
- データ保存
- 認証や権限
- 外部サービス
- テストとビルド
- デプロイ
- セキュリティとプライバシー
- ログ、監視、運用

Discoveryでは、仮説検証に不要な本番設計を固定しません。

## Step 8: ROADMAPを作る

`docs/ROADMAP.md` に各フェーズの目的、成果または学び、主要タスク候補、完了条件、前提仮説、見直し条件を書きます。

Discoveryの例:

```text
Phase 1: アイデア検証
Phase 2: MVP定義
Phase 3: MVP開発
Phase 4: 公開準備
```

ROADMAPはプロジェクト全体の地図です。
1タスクの実装手順は `implementation-plan.md` に分けます。

## Step 9: AGENTS.mdを正式化する

初期状態のAGENTS.mdは、安全規則と初期設定ルーティングを提供します。
PROJECT_BRIEFと開発方針が整理できた後、次をプロジェクト固有の内容へ更新します。

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

Hypothesisを恒久ルールとして固定しません。

## Step 10: PROJECT_STATUSを初期化する

`docs/PROJECT_STATUS.md` に次を記録します。

- 現在のフェーズ
- 初期設定で完了したこと
- 最初の候補タスク
- 未確定事項と注意点
- 検証状態

初期設定状態の正式な判定元はPROJECT_STATUSではなく、`.ai-workflow/project-state.conf` です。

## Step 11: DIRECTORY_MAPを作る

コードがまだない場合は、次を記録します。

```text
Map Status: Provisional
```

予定している主要ディレクトリ、責務、境界を書きます。
初期構築後に実際の構成と照合し、`Map Status: Verified` へ変更します。

## Step 12: Initialization Reviewを行う

`templates/initialization-review.md` を使い、`docs/INITIALIZATION_REVIEW.md` を記入します。

確認すること:

- 確定事項と仮説が分かれているか
- AIが不明点を補完していないか
- 最初のタスクを妨げる不明点が残っていないか
- ROADMAPが現在の成熟段階に合っているか
- AGENTS.mdが確定事項に基づいているか
- 最初のタスクが1つの目的に絞られているか

## Step 13: ユーザー承認を得る

AIは次をユーザーへ提示します。

- PROJECT_BRIEFの要点
- ConfirmedとHypothesis
- 残るUnknownとDeferred
- ROADMAPの最初のフェーズ
- AGENTS.mdの主要ルール
- 最初のタスク候補

ユーザーの明示承認前に `ready` にしてはいけません。

## Step 14: READYを確認する

承認後、状態を次へ変更します。

```text
schema_version=1
initialization_status=ready
user_approved=true
```

チェッカーを再実行し、次を確認します。

```text
INITIALIZATION_READY
```

`ready`は、すべての事業・製品判断が完了した意味ではありません。
現在の仮説と不明点を明示したうえで、最初のタスクを安全に始められる意味です。

READY判定では、状態ファイルだけでなく、プロジェクト固有AGENTS、確認済みの初期経路、名前付きPhase 1、記入済みDirectory Map、承認者・承認日・確認要約も検査します。
これらの判定対象に初期値またはプレースホルダーが残る場合は `INITIALIZATION_INVALID` です。

## Step 15: 最初のタスクを開始する

AIは初期設定後に自動で実装を始めません。
最初のタスク候補、対象範囲、対象外、期待する証拠を提示します。

ユーザーが開始を指示した後、`workflows/session-start.md` へ進みます。

通常タスクの進め方は [practical-guide.md](practical-guide.md) を参照してください。

## 状態不整合の扱い

### INITIALIZATION_INVALID

初期設定を最初からやり直しません。
状態ファイル、必須文書、承認記録のどこが矛盾しているかを報告します。

### INITIALIZATION_CHECK_FAILED

初期設定済みかどうかを推測しません。
スクリプト、権限、実行環境の問題を先に確認します。

### INITIALIZATION_REVISIT_REQUIRED

対象ユーザー、中核価値、MVP、アーキテクチャ、データ、公開範囲などの大きな変更時に使います。
状態を `revisit_required`、承認を `false` に戻します。
影響する文書だけを見直し、ユーザーの再承認後に `ready` へ戻します。
