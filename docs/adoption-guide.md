# Adoption Guide

既存プロジェクトにこのワークフローを導入するための手順です。

## 目的

このガイドは、テンプレートをただ置くだけではなく、実際に開発で使える状態にすることを目的にしています。

## Step 1: ワークフローの前提を確認する

導入時にMinimal、Standard、Strictのどれかを固定する必要はありません。
Workflow Modeは、タスクを実行するときにAIが作業内容とリスクを見て自動判定します。

デフォルトはStandardです。
AIは、低リスクなら理由を明示してMinimalに下げ、高リスクなら必ずStrictに上げます。
迷った場合はStandardを使います。
Strictの可能性がある場合は、実装前にユーザーへ確認します。

モード選択は、導入設定ではなくタスク実行時のリスク判定です。
MinimalまたはStrictに変更する場合は、implementation plan、completion review、devlog、PRに理由を残します。

導入前に [design-rationale.md](design-rationale.md)、[principles.md](principles.md)、[requirement-alignment.md](requirement-alignment.md)、[practical-guide.md](practical-guide.md) を読み、なぜこの運用を入れるのか、1タスクをどう進めるのかを先に共有します。
テンプレートだけを置いても、判断理由を残す文化がなければ効果は限定的です。

## Step 2: ファイルを配置する

既存プロジェクトに丸ごと導入する場合は、このリポジトリの `starter/` の中身を、導入先プロジェクトのルートにコピーします。
このリポジトリ自体は開発運用のテンプレートであり、通常はこのリポジトリの中でプロダクト本体を開発しません。
プロダクト用のリポジトリを別に用意し、そこへ `starter/` を導入します。

コピー後の構成は次の形です。

```text
AGENTS.md
docs/
  PROJECT_STATUS.md
  ROADMAP.md
  DIRECTORY_MAP.md
  ai-workflow/
  tasks/
  devlog/
  adr/
workflows/
  session-start.md
  session-end.md
templates/
  adr.md
  requirement-alignment.md
  implementation-plan.md
  completion-review.md
  devlog.md
  directory-map.md
  security-review.md
  rollback-plan.md
.github/
  pull_request_template.md
  ISSUE_TEMPLATE/
```

最初から全ファイルを使う必要はありません。
ただし、AIが最初に読むルール、現在地、要件認識合わせ、実装計画、完了レビュー、devlogはセットで置いた方が運用が崩れにくくなります。
大規模化するプロジェクトでは、`docs/DIRECTORY_MAP.md` も早めに整備します。
コード全体を読ませるのではなく、主要ディレクトリと責務から今回読むべき範囲を絞るためです。

AIエージェントを使うプロジェクトでは、ルートの `AGENTS.md` をプロジェクト用に編集します。
`AGENTS.md` には「曖昧な点がある場合は実装前に確認する」「認識合わせが終わるまで実装しない」など、必ず守らせたいルールを書きます。

`.github/` は隠しディレクトリのため、コピー時に漏れないようにします。

Bash:

```bash
cp -R starter/. /path/to/project/
```

PowerShell:

```powershell
Copy-Item -Path .\starter\* -Destination C:\path\to\project -Recurse -Force
Copy-Item -Path .\starter\.github -Destination C:\path\to\project -Recurse -Force
```

## Step 3: 作りたいものを整理する

導入直後は、いきなり実装に入らず、まずプロジェクト全体の目的を整理します。

確認すること:

- 何を作りたいか
- 誰のために作るか
- どの問題を解決するか
- 最初に必要な最小機能は何か
- 制約、前提、使わない技術、扱わない範囲は何か
- 成功条件は何か

必要に応じてAIと壁打ちし、目的、制約、成功条件を明確にします。
この段階では細かな実装計画ではなく、プロジェクト全体の方向性を決めます。

## Step 4: ROADMAPを書く

`docs/ROADMAP.md` は、プロジェクト全体の地図です。
大きな作業はフェーズに分けます。

例:

```text
Phase 1: 最小機能
Phase 2: 主要機能
Phase 3: 品質改善
Phase 4: 公開準備
```

ロードマップは細かすぎる必要はありません。
次に何をするべきかが分かる粒度で十分です。

重要なのは、ROADMAPを実装計画と混同しないことです。
ROADMAPは全体計画であり、`implementation-plan.md` は今回取り組む1タスクの実行計画です。

## Step 5: PROJECT_STATUSを書く

`docs/PROJECT_STATUS.md` は、次のセッションで最初に読む現在地メモです。

最低限、次を書きます。

- 今のフェーズ
- 完了済み
- 進行中
- 次にやる候補タスク
- 注意点
- 最後に確認したテストやビルド

## Step 6: DIRECTORY_MAPを書く

`docs/DIRECTORY_MAP.md` は、主要ディレクトリと責務を説明する地図です。
コード全文を読むための一覧ではありません。
AIが実装前に今回のタスクで確認すべき範囲を絞れるようにするためのものです。

最初は詳細な図である必要はありません。
主要ディレクトリ、責務、タスク別の参照先、触ってはいけない境界だけで十分です。

確認すること:

- 主要ディレクトリは何か
- 各ディレクトリの責務は何か
- UI、API、domain、types、utilsなどの境界はどこか
- タスク種別ごとに最初に見る場所はどこか
- 触ってはいけない境界は何か

## Step 7: 最初のセッションを始める

`workflows/session-start.md` を使い、現在地を復元します。

確認すること:

- Git状態
- PROJECT_STATUS
- ROADMAP
- DIRECTORY_MAP
- 最新devlog
- テストやビルドの状態
- ROADMAP上の次の候補タスク

session-startは、ただファイルを読む手順ではありません。
ROADMAPとPROJECT_STATUSから今回取り組むタスクを確認し、そのタスクに入る前に細かな実装計画を作れる状態にするための手順です。

## Step 8: 今回のタスクを決める

ROADMAPとPROJECT_STATUSをもとに、今回のセッションで扱うタスクを1つに絞ります。

確認すること:

- 今回どのROADMAP項目に取り組むか
- そのタスクの目的は何か
- どこまでを今回やるか
- 何を今回やらないか
- 完了条件は何か

タスクが大きすぎる場合は、実装前にさらに小さく分けます。
1セッションで複数の大きな目的を混ぜないことが重要です。

## Step 9: 要件認識合わせを行う

ユーザーの要望が短い場合や、意図、範囲、完了条件に曖昧さがある場合は、`templates/requirement-alignment.md` を使います。
記録はテンプレート本体ではなく、`docs/tasks/YYYY-MM-DD-HHMM-task-name/requirement-alignment.md` に保存します。

確認すること:

- ユーザーの元要望
- AI側の理解
- 実装対象と対象外
- 不明点、曖昧な点、懸念点
- AIが置いた仮定
- ユーザー確認結果

未回答の重要な不明点がある場合は、実装に進みません。

## Step 10: Directory Contextを確認する

今回のタスクが決まったら、`docs/DIRECTORY_MAP.md` を使って確認範囲を絞ります。
コード全体を読むのではなく、今回読むべきディレクトリ、責務、触ってはいけない境界を先に確認します。

確認すること:

- 今回のタスクはどのディレクトリに関係するか
- そのディレクトリの責務は何か
- 関連して読むべきディレクトリはどこか
- 触ってはいけない境界はどこか
- DIRECTORY_MAPと実際の構成にズレがないか

確認結果は、implementation planのDirectory Contextに記録します。
DIRECTORY_MAPと実際の構成にズレがある場合は、Directory Map更新候補として記録します。

## Step 11: Workflow ModeをAIが判定する

今回のタスクが決まったら、AIがWorkflow Modeを判定します。
ユーザーが導入時にモードを手動で選ぶ必要はありません。

判定ルール:

- デフォルトはStandard
- 小さく、戻しやすく、低リスクで、挙動、データ、セキュリティ、本番設定に影響しない場合だけMinimalに下げる
- 認証、権限、課金、個人情報、データ移行、本番設定、外部依存、公開リリース、アーキテクチャ変更を含む場合はStrictに上げる
- Strictの可能性があるが判断できない場合は、実装前にユーザーへ確認する

判定結果と理由は、implementation planに記録します。
作業中にリスクが変わった場合は、completion review、devlog、PRにも変更理由を残します。

## Step 12: 実装計画を作る

`templates/implementation-plan.md` を使います。
記録は `docs/tasks/YYYY-MM-DD-HHMM-task-name/implementation-plan.md` に保存します。

計画には、次の観点を必ず入れます。

- 目的
- 背景
- 変更するもの
- 変更しないもの
- Directory Context
- 実装手順
- 影響範囲
- リスク
- Workflow Modeと判定理由
- 検証方法
- 完了条件

完了条件を書くときは、[definition-of-done.md](definition-of-done.md) を基準にします。

実装計画はROADMAPの代わりではありません。
ROADMAPで決めた全体方針の中から、今回の1タスクをどう実行するかを具体化するものです。

## Step 13: 完了前レビューを行う

`templates/completion-review.md` を使い、作業漏れを確認します。
記録は `docs/tasks/YYYY-MM-DD-HHMM-task-name/completion-review.md` に保存します。

ここで見るのは、コードが書けたかだけではありません。

- 計画した作業が終わっているか
- 余計な変更が混ざっていないか
- テストやビルドが通っているか
- ドキュメント更新が必要か
- 次回に残すべき注意点があるか

重要な設計判断が発生した場合は、`templates/adr.md` を使って `docs/adr/` に記録します。
devlogは作業判断、ADRは長期的な設計判断を残すために分けます。
ADR候補の判断基準は [adr-guidelines.md](adr-guidelines.md) を参照してください。

Strict modeでは、必要に応じて `templates/security-review.md` と `templates/rollback-plan.md` も作成します。

## Step 14: devlogを書く

`templates/devlog.md` を使い、判断理由を残します。

devlogは作業日報ではありません。
後から判断を追うための記録です。

タスク記録の保存先とdevlogの関係は [task-records.md](task-records.md) を参照してください。

## Step 15: Gitに記録する

最後に差分を確認し、必要なファイルだけをコミットします。

```bash
git status --short
git diff --check
git add [files]
git commit -m "[short message]"
```

コミットメッセージは短くて構いません。
理由はdevlogに残します。

## Step 16: PRとCIに接続する

GitHubを使う場合は、`.github/pull_request_template.md` と `.github/ISSUE_TEMPLATE/` を導入します。

これにより、PR上で次を確認しやすくなります。

- workflow mode
- mode selection reason
- 関連する計画、レビュー、devlog、ADR
- 予定外の変更
- 検証結果
- セキュリティとプライバシー
- Strict modeの追加ゲート

CIを使う場合は、導入先プロジェクトの技術スタックに合わせて、文書構造、未解決プレースホルダー、秘密情報らしき文字列、ローカルリンクを確認するチェックを追加します。
このワークフローの導入自体に、専用のインストールスクリプトは必須ではありません。

品質ゲートの考え方は [quality-gates.md](quality-gates.md) を参照してください。
チームで導入する場合は [team-development.md](team-development.md) を先に読み、誰がレビューし、誰が最終判断するかを決めてから運用します。

## 導入時の注意

- 既存プロジェクトのルールを上書きしない
- テンプレートはプロジェクトに合わせて削る
- 秘密情報をdevlogに書かない
- すべての作業で重い手順を強制しない
- Workflow Modeは導入時に固定せず、タスクごとにAIが判定する
- Minimalに下げる場合とStrictに上げる場合は理由を残す
- PRやCIを入れても、人間のレビュー責任はなくならない
- Strict modeはチェック欄を埋めることではなく、リスクを証拠付きで扱うこと
