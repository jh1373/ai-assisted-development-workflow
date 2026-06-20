# Session Start Workflow

新しい開発セッションを始めるときに、現在の開発状況を把握するための手順です。

## 目的

- チャット履歴に依存せず、ドキュメントから現在の開発状況を把握する
- ユーザーの要望とAI側の理解を揃えてから作業する
- 今回の作業範囲を明確にする
- 既存の変更や未完了事項を把握する
- 実装前にテストや既知の問題を確認する
- ROADMAPから今回取り組む候補タスクを確認する
- DIRECTORY_MAPから今回読むべき範囲を絞る
- タスクごとにWorkflow Modeを判定する
- 実装に入る前に、計画を作れる状態にする

## 手順

### 0. Initialization Gateを確認する

通常タスクを始める前に、現在の環境に合う判定スクリプトを1つ実行します。

```bash
bash scripts/check-initialization.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-initialization.ps1
```

AIは文書の雰囲気やファイル数から初期設定状態を推測しません。

- `INITIALIZATION_READY`: 次のGit確認へ進む
- `INITIALIZATION_NOT_STARTED`: `workflows/project-initialization.md` を開始し、通常タスクには進まない
- `INITIALIZATION_IN_PROGRESS`: 既存の初期設定文書を読み、続きから再開する
- `INITIALIZATION_REVISIT_REQUIRED`: 影響する前提だけを見直し、再承認まで通常タスクには進まない
- `INITIALIZATION_INVALID`: 設定不整合を報告し、初期設定を最初からやり直さない
- `INITIALIZATION_CHECK_FAILED`: 実行失敗を報告し、状態を推測しない

このゲートはMinimal、Standard、Strictの選択より前に通します。

### 1. Gitの状態を確認する

```bash
git status --short --branch
```

確認すること:

- 現在のブランチ
- 未コミットの変更
- 未追跡ファイル
- 前回作業の残りがないか

未コミットの変更がある場合は、今回の作業と関係があるかを先に確認します。

### 2. プロジェクトルールを読む

次のようなファイルがある場合は、最初に確認します。

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `CONTRIBUTING.md`
- `docs/principles.md`
- `docs/definition-of-done.md`

ここでは、プロジェクト固有のルール、禁止事項、実行環境、テスト方法を確認します。

### 3. 現在の開発状況を確認する

次のようなファイルを読み、現在の開発状況を把握します。

- `docs/PROJECT_STATUS.md`
- `docs/ROADMAP.md`
- `docs/DIRECTORY_MAP.md`
- `docs/ARCHITECTURE.md` がある場合
- 直近の `docs/devlog/`

確認すること:

- 今どのフェーズか
- 前回何を完了したか
- 次に何をする予定か
- 注意すべき未完了事項は何か
- 主要ディレクトリと責務は何か
- 設計上の前提は何か

`docs/ROADMAP.md` は全体の地図、`docs/PROJECT_STATUS.md` は現在地として扱います。
この時点では実装に入らず、次に取り組む候補タスクを整理します。
DIRECTORY_MAPはここでは全体把握として読み、タスク別の読み取り範囲は後のDirectory Contextで絞ります。

### 4. 健全性を確認する

プロジェクトに応じて、テストやビルドを実行します。

例:

```bash
npm test
npm run build
```

失敗している場合は、新しい実装に入る前に原因を確認します。

### 5. 今回の候補タスクを確認する

ROADMAPとPROJECT_STATUSから、今回取り組む候補タスクを確認します。

確認すること:

- ROADMAP上のどのフェーズ、どの項目に関係するか
- PROJECT_STATUSで次にやる候補として挙がっているか
- 前回devlogに未完了事項や注意点が残っていないか
- 今回のセッションで扱える大きさか
- 複数の目的が混ざっていないか

タスクが大きすぎる場合は、実装前に小さく分けます。
ROADMAPは全体計画であり、implementation planは今回の1タスクの実行計画です。

### 6. 要件認識合わせを確認する

実装前に、ユーザーの要望とAI側の理解が揃っているか確認します。

確認すること:

- ユーザーの元要望は何か
- AI側はどう理解したか
- 実装対象と対象外は明確か
- 完了条件は明確か
- 不明点、曖昧な点、懸念点は残っていないか
- AIが勝手に置いた仮定はないか

未回答の重要な不明点がある場合は、実装に進みません。
必要に応じて `templates/requirement-alignment.md` を使います。

### 7. 今回の作業範囲を宣言する

作業前に、今回のセッションで扱う範囲を短くまとめます。

例:

```text
今回の対象:
- フェーズ2の検索機能
- 対象ファイルは src/features/search/ 配下
- UIの大幅変更は行わない
- 完了条件は検索結果の表示とテスト通過
```

### 8. Directory Contextを確認する

`docs/DIRECTORY_MAP.md` を読み、今回のタスクで確認すべき範囲を絞ります。
目的はコード全体を読むことではありません。
主要ディレクトリ、責務、境界を先に確認し、必要なコードだけを読むことです。

確認すること:

- 今回のタスクはどのディレクトリに関係するか
- そのディレクトリの責務は何か
- 関連して読むべきディレクトリはどこか
- 触ってはいけない境界はどこか
- DIRECTORY_MAPと実際の構成に大きなズレがなさそうか

`docs/DIRECTORY_MAP.md` がない場合は、実装前に現在の主要ディレクトリと責務を短く整理します。
新しい主要ディレクトリや責務変更が必要になりそうな場合は、実装計画にDirectory Map更新候補として記録します。

### 9. Workflow Modeを判定する

デフォルトはStandardです。
Workflow Modeは導入時に固定せず、今回のタスク内容を見てAIが判定します。

- 小さく、戻しやすく、低リスクで、挙動、データ、セキュリティ、本番設定に影響しない場合だけMinimalに下げます。
- 認証、権限、課金、個人情報、データ移行、本番設定、外部依存、公開リリース、アーキテクチャ変更を含む場合はStrictに上げます。
- MinimalまたはStrictに変更する場合は理由を記録します。
- Strictの可能性があり判断できない場合は、実装前にユーザーへ確認します。

詳しくは [docs/workflow-modes.md](../docs/workflow-modes.md) を参照します。

### 10. 実装計画を作る

作業範囲を確認したら、`templates/implementation-plan.md` を使って実装計画を作ります。

計画なしに実装へ入らないことが重要です。
AI支援開発では実装速度が速いため、先に目的、対象範囲、検証方法を固定しておかないと、不要な変更が混ざりやすくなります。
判定したWorkflow Modeと理由も、この実装計画に記録します。
Directory Contextも、この実装計画に記録します。

実装計画や認識合わせはテンプレート本体に直接書き込まず、タスク記録として保存します。
保存先の例:

```text
docs/tasks/YYYY-MM-DD-HHMM-task-name/
  requirement-alignment.md
  implementation-plan.md
```

詳しくは [docs/task-records.md](../docs/task-records.md) を参照します。

認証、権限、課金、個人情報、データ移行、本番設定、依存追加、公開前作業を含む場合は、Strict modeとして扱います。
その場合は [docs/strict-mode.md](../docs/strict-mode.md) の確認項目を計画に含めます。

## 開始時の出力テンプレート

```text
現在の開発状況:
[プロジェクトの現在フェーズ]

前回まで:
[直近devlogやPROJECT_STATUSから分かる完了内容]

今回やること:
[今回の作業範囲]

注意点:
[未完了事項、リスク、触らない範囲]

確認したもの:
- initialization checker: INITIALIZATION_READY
- git status
- selected task from roadmap/project status
- directory map
- requirement alignment
- workflow mode
- project status
- roadmap
- latest devlog
- tests/build

次に作るもの:
- task records
- implementation plan

Directory Context:
- Related directories:
- Responsibilities:
- Boundaries not to cross:
- Files to inspect before planning:
```
