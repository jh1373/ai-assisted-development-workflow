# AI-assisted Development Workflow

> [!IMPORTANT]
> **このリポジトリは、新規プロジェクト専用です。**
> 既存プロジェクトへの導入には現在対応していません。
> `starter/` を既存プロジェクトへ直接コピーすると、README、AGENTS.md、`.github/`、`docs/` などの同名ファイルを上書きする可能性があります。

AI駆動開発で、実装速度だけを上げるのではなく、品質、判断理由、検証結果、責任範囲を失わずにプロダクトを作るための実践ガイドです。

このリポジトリは、AIにコード作成を丸投げするためのプロンプト集でも、Markdownテンプレート集でもありません。
Codex、Claude Code、Google Antigravity、GitHub Copilot などのAI開発支援ツールを使うときに、何をAIに任せ、何を人間が判断し、どの証拠を残せば品質を保てるかを整理するためのものです。

## 何を解決するか

AI駆動開発では、実装は速くなります。
一方で、次の問題も速く発生します。

- 何を作るべきかが曖昧なまま、AIがそれらしい実装を始める
- ユーザーとAIの認識がズレたまま、プロダクトが作られていく
- チャットが長くなり、前提や判断理由が埋もれる
- Gitには差分が残るが、なぜその実装にしたかは残らない
- AIが不要なリファクタリングや範囲外の変更を混ぜる
- テスト、ビルド、手動確認が曖昧なまま完了扱いになる
- 別のチャットや別の作業者が再開したとき、前回までの開発状況を把握できない
- 認証、権限、課金、個人情報などの高リスク変更をAI任せにしてしまう

このガイドの目的は、AIを使わないことではありません。
AIで実装速度を上げながら、人間が品質と公開判断に責任を持てる状態を作ることです。

## 基本思想

このワークフローは、次の考え方を中心にしています。

- チャットは作業場であり、信頼できる記録ではない
- Gitは「何を変えたか」を残すが、「なぜ変えたか」は別に残す
- 認識合わせが終わるまで、実装に進まない
- 実装前に目的、対象範囲、完了条件、検証方法を固定する
- AIの出力は成果物ではなく、レビュー対象の提案として扱う
- 完了とは、実装済みではなく、検証済みで再開可能な状態を指す
- 不確実性、失敗、見送った選択肢を隠さない
- 作業の重さは、リスクの大きさに合わせる

詳しくは [docs/principles.md](docs/principles.md) を参照してください。
この構成にしている理由は [docs/design-rationale.md](docs/design-rationale.md) にまとめています。

## 実践フロー

このワークフローは、新規プロジェクトで一度だけ行う初期設定と、初期設定後に1タスクずつ実行する通常フローを分けて扱います。

### 初回のみ: Project Initialization

```text
starter/を配置する
→ 初期設定状態をnot_startedとして確認する
→ ユーザーとAIがプロダクト構想を壁打ちする
→ 確定事項、仮説、不明点、後で決めることを分ける
→ PROJECT_BRIEFを作る
→ DiscoveryまたはBuild-readyの経路を選ぶ
→ ROADMAPを作る
→ AGENTS.mdをプロジェクト向けに正式化する
→ PROJECT_STATUSとJSON正本のDirectory Mapを初期化する
→ Project Structure Mapで予定構成を機械確認する
→ 初期設定レビューを行う
→ ユーザーが開始を承認する
→ 機械判定がINITIALIZATION_READYになったことを確認する
```

初期設定の目的は、すべてを最初から確定することではありません。
「なんとなく作ってみたい」という段階でも、仮説と不明点を明示し、最初の検証タスクを安全に始められれば準備完了にできます。

詳しくは [workflows/project-initialization.md](workflows/project-initialization.md) を参照してください。

### 初期設定後: Task Workflow

```text
session-startのStep 0でINITIALIZATION_READYを確認する
→ Project Structure Gateで構造の鮮度を機械確認する
→ 現在の開発状況を把握する
→ ROADMAPとPROJECT_STATUSから今回のタスクを選ぶ
→ DIRECTORY_MAPで今回読むべき範囲を絞る
→ AIがタスク内容とリスクを見てWorkflow Modeを判定する
→ implementation planで今回の実行計画を作る
→ AIと実装する
→ テストと手動確認を行う
→ 完了前レビューを行う
→ devlogとGitに記録する
→ 必要ならPRでレビューする
```

ROADMAPは初期設定で作るプロジェクト全体の地図です。
`implementation-plan.md` は、今回取り組む1タスクの実行計画です。

1つのタスクを、1つの開発セッションとして扱います。

```text
ユーザーの要望を受け取る
→ session-startのStep 0でINITIALIZATION_READYを確認する
→ 現在の開発状況を把握する
→ AI側の理解を要約する
→ 不明点、曖昧な点、懸念点を洗い出す
→ 必要ならユーザーに確認する
→ 合意できた範囲だけをタスク化する
→ DIRECTORY_MAPで関連範囲を絞る
→ Workflow Modeを判定する
→ 実装計画を作る
→ AIと実装する
→ テストと手動確認を行う
→ 完了前レビューを行う
→ devlogとGitに記録する
→ 必要ならPRでレビューする
```

実際の進め方は [docs/practical-guide.md](docs/practical-guide.md) にまとめています。
要件認識合わせの原則は [docs/requirement-alignment.md](docs/requirement-alignment.md) を参照してください。

## まず使う方法

新規プロジェクト用の空フォルダ、または `.git` だけが入った空リポジトリを用意し、導入スクリプトで `starter/` の中身をプロジェクトルートへ展開します。
このリポジトリ自体は開発運用のテンプレートです。
通常は、プロダクト用リポジトリを別に用意し、そこへ `starter/` を導入します。

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create-new-project.ps1 C:\path\to\my-new-project
```

Bash:

```bash
bash scripts/create-new-project.sh /path/to/my-new-project
```

導入スクリプトは、既存ファイルがある場所には展開しません。
既存プロジェクトへ誤って上書きする事故を防ぐため、導入先に `.git` 以外のファイルやフォルダがある場合は停止します。

展開すると、初期設定状態を持つ `.ai-workflow/`、AIが最初に読む `AGENTS.md`、プロダクト仮説を整理する `docs/PROJECT_BRIEF.md`、現在地を残す `docs/PROJECT_STATUS.md`、初期設定と通常タスクのワークフロー、作業用テンプレートが配置されます。
`.ai-workflow/directory-map.json` を構造と意味情報の正本とし、`docs/DIRECTORY_MAP.md` を自動生成します。
localhostのプロジェクト案内図では、プロジェクトの主な役割、処理の流れ、作業場所の案内、ファイルごとの役割を先に表示し、必要な場合だけ全ファイル一覧へ移動できます。

詳しくは [starter/README.md](starter/README.md) を参照してください。

プロジェクト案内図はPython 3.10以降を推奨し、外部Pythonパッケージなしで動作します。

新規プロジェクトへ`starter/`の中身を導入した後は、プロジェクト直下の`open-project-structure-map.cmd`をダブルクリックすると、サーバーと既定ブラウザが自動で起動します。
このリポジトリ上で試す場合は、`starter/open-project-structure-map.cmd`をダブルクリックしてください。

```bash
python scripts/project-structure.py validate
python scripts/project-structure.py serve --open-browser
```

localhost画面は`127.0.0.1`だけで起動し、全パス、役割の根拠、構造差分を閲覧専用で表示します。ファイル内容は読み取りません。

## 新規プロジェクトで必要な基本構成

初期設定と通常タスクを正しく分けるため、次を基本構成として扱います。

```text
.ai-workflow/project-state.conf
.ai-workflow/directory-map.json
.ai-workflow/directory-map.ignore
AGENTS.md
docs/PROJECT_BRIEF.md
docs/INITIALIZATION_REVIEW.md
docs/ROADMAP.md
docs/PROJECT_STATUS.md
docs/DIRECTORY_MAP.md
docs/README.md
docs/pull-request-template.md
docs/tasks/
workflows/project-initialization.md
workflows/session-start.md
workflows/session-end.md
scripts/check-initialization.sh
scripts/check-initialization.ps1
scripts/check-directory-map.sh
scripts/check-directory-map.ps1
scripts/project-structure.py
templates/project-brief.md
templates/initialization-review.md
templates/requirement-alignment.md
templates/implementation-plan.md
templates/completion-review.md
templates/devlog.md
```

- `.ai-workflow/project-state.conf`: 初期設定状態を機械判定する唯一の状態ファイル
- `.ai-workflow/directory-map.json`: 主な役割、ファイルの役割説明、処理の流れ、作業場所の案内、重要な場所、変更時の注意事項を保存する正本
- `.ai-workflow/directory-snapshot.json`: Verified時点の全パス構造を保存する生成基準線
- `PROJECT_BRIEF.md`: 確定事項、仮説、不明点、後で決めることを整理する
- `INITIALIZATION_REVIEW.md`: ユーザー承認を含む初期設定レビュー
- `ROADMAP.md`: プロジェクト全体のフェーズ、成果、見直し条件を残す
- `PROJECT_STATUS.md`: 次のセッションで最初に読む現在地メモ
- `DIRECTORY_MAP.md`: JSON正本から生成するプロジェクト案内図と構成の要約
- `docs/README.md`: docsの読み方、目的別の参照先、主要ファイルの意味と役割の一覧
- `pull-request-template.md`: PRテンプレートの目的、各項目の意味、初心者向けの記入例
- `docs/tasks/`: 1タスクごとの認識合わせ、計画、完了レビューを残す場所
- `requirement-alignment.md`: 実装前にユーザーとAIの認識を揃える確認メモ
- `implementation-plan.md`: 実装前に目的、範囲、検証方法を固定する計画
- `devlog.md`: 作業後に判断理由、検証結果、未完了事項を残す記録

Devlogの粒度は [examples/devlog/standard-task-devlog.md](examples/devlog/standard-task-devlog.md) を見本にしてください。
構造検証とlocalhost画面は [Project Structure Map](docs/project-structure-map.md) を参照してください。
docsの読み方と主要ファイルの意味は [docs/README.md](docs/README.md) を参照してください。

PRテンプレート、ADR、Strict modeの追加成果物は、プロジェクトのリスクと運用に応じて使います。
PRテンプレートの考え方と書き方は [docs/pull-request-template.md](docs/pull-request-template.md) を参照してください。

## 品質を守る関門

AI駆動開発では、速く作れるぶん、間違った変更も速く混ざります。
そのため、作業ごとに品質ゲートを決めます。

例:

- project initialization gate: 初期設定状態、仮説、不明点、ユーザー承認が確認できるか
- requirement alignment gate: ユーザーとAIの認識が揃っているか
- scope gate: 何をやるか、何をやらないかが明確か
- test gate: テスト、ビルド、手動確認を実行したか
- diff gate: 予定外の変更が混ざっていないか
- security gate: 秘密情報、個人情報、権限変更がないか
- recovery gate: 問題が出たときに戻せるか
- review gate: 人間が最終判断すべき変更ではないか

詳しくは [docs/quality-gates.md](docs/quality-gates.md) を参照してください。

## 運用モード

作業の重さに応じて、タスクごとに3段階で使います。
デフォルトは **Standard** です。
AIは今回のタスク内容とリスクを見て、低リスクなら理由を明示してMinimalに下げ、高リスクなら必ずStrictに上げます。
導入時にユーザーがモードを固定する必要はありません。

| モード | 向いている用途 | 目的 |
|---|---|---|
| Minimal | 小さく、戻しやすく、低リスクな作業 | 目的、検証、判断理由だけ残す |
| Standard | 通常の機能追加、バグ修正、UI改善 | 開始、計画、完了レビュー、devlogを回す |
| Strict | 認証、権限、課金、個人情報、本番、公開、設計変更 | リスク、承認、復旧方法まで証拠を残す |

詳しくは [docs/workflow-modes.md](docs/workflow-modes.md) と [docs/strict-mode.md](docs/strict-mode.md) を参照してください。

## 個人開発とチーム開発

個人開発では、現在地、判断理由、検証結果を残すことが主な目的です。
チーム開発では、それに加えて責任範囲、PRレビュー、CI、承認、ロールバックまで必要になります。

チームで使う場合は、最低限次を決めます。

- AIに任せてよい作業と、人間が必ず判断する作業
- PRで必ず書く検証結果
- Strict modeが必要な変更
- 誰がレビューし、誰がマージ判断するか
- 失敗時にどう戻すか

詳しくは [docs/team-development.md](docs/team-development.md) を参照してください。

## リポジトリ構成

```text
.
├── README.md
├── starter/
│   ├── .ai-workflow/
│   ├── AGENTS.md
│   ├── docs/
│   ├── templates/
│   ├── workflows/
│   └── .github/
├── docs/
│   ├── new-project-setup-guide.md
│   ├── adr-guidelines.md
│   ├── ai-human-boundary.md
│   ├── anti-patterns.md
│   ├── design-rationale.md
│   ├── definition-of-done.md
│   ├── README.md
│   ├── practical-guide.md
│   ├── principles.md
│   ├── pull-request-template.md
│   ├── quality-gates.md
│   ├── requirement-alignment.md
│   ├── review-checklist.md
│   ├── security.md
│   ├── strict-mode.md
│   ├── task-records.md
│   ├── team-development.md
│   └── workflow-modes.md
├── workflows/
│   ├── project-initialization.md
│   ├── session-start.md
│   └── session-end.md
├── templates/
│   ├── AGENTS.md
│   ├── adr.md
│   ├── completion-review.md
│   ├── devlog.md
│   ├── implementation-plan.md
│   ├── initialization-review.md
│   ├── project-brief.md
│   ├── project-status.md
│   ├── requirement-alignment.md
│   ├── directory-map.md
│   ├── roadmap.md
│   ├── rollback-plan.md
│   ├── security-review.md
│   └── task-brief.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── scripts/
│   ├── check-docs.sh
│   ├── create-new-project.sh
│   ├── create-new-project.ps1
│   ├── check-initialization.sh
│   ├── check-initialization.ps1
│   ├── test-initialization-checker.sh
│   └── test-initialization-checker.ps1
└── examples/
    ├── project-initialization/
    ├── devlog/
    └── react-app/
```

## 使うべき場面

- AI支援開発でチャットが長くなりすぎる
- 後から「なぜこの実装にしたのか」が分からなくなる
- Gitの差分だけでは判断理由が足りない
- 別チャットや別AIツールで作業を再開したい
- AIエージェントに守らせる開発ルールを明文化したい
- PRやIssueに検証結果と判断理由を接続したい
- 個人開発でもチーム開発に近い品質管理をしたい

## 使わない方がよい場面

- 数分で終わる単純な修正
- 一度きりの実験コード
- Gitやドキュメントで管理する必要がない作業
- ログを残すことで秘密情報が漏れる危険が高い作業

小さい作業に重い手順を強制する必要はありません。
重要なのは、作業のリスクに見合った証拠を残すことです。

## 導入方法

新規プロジェクトへ導入する場合は、まずこのリポジトリ直下で導入スクリプトを実行してください。
詳しい手順は [docs/new-project-setup-guide.md](docs/new-project-setup-guide.md) と [starter/README.md](starter/README.md) を参照してください。
運用の考え方を理解したい場合は、[docs/new-project-setup-guide.md](docs/new-project-setup-guide.md) から始めてください。

導入後の基本的な流れ:

1. `scripts/create-new-project.ps1` または `scripts/create-new-project.sh` で `starter/` を新規プロジェクトへ展開する
2. 初期設定チェッカーで `INITIALIZATION_NOT_STARTED` を確認する
3. `workflows/project-initialization.md` に沿ってユーザーとAIが壁打ちする
4. `docs/PROJECT_BRIEF.md` に確定事項、仮説、不明点、Deferredを記録する
5. DiscoveryまたはBuild-readyのROADMAPを作る
6. `AGENTS.md` をプロジェクト向けに正式化する
7. `PROJECT_STATUS.md` と `.ai-workflow/directory-map.json` を初期化し、`DIRECTORY_MAP.md` を生成する
8. `INITIALIZATION_REVIEW.md` を使って初期設定をレビューする
9. ユーザー承認後だけ状態を `ready` にする
10. チェッカーで `INITIALIZATION_READY` を確認する
11. ユーザーが最初のタスク開始を指示した後、`session-start.md` へ進む

最初に読む順番:

1. [docs/README.md](docs/README.md)
2. [docs/design-rationale.md](docs/design-rationale.md)
3. [docs/principles.md](docs/principles.md)
4. [docs/new-project-setup-guide.md](docs/new-project-setup-guide.md)
5. [workflows/project-initialization.md](workflows/project-initialization.md)
6. [docs/requirement-alignment.md](docs/requirement-alignment.md)
7. [docs/task-records.md](docs/task-records.md)
8. [docs/practical-guide.md](docs/practical-guide.md)
9. [docs/workflow-modes.md](docs/workflow-modes.md)
10. [docs/quality-gates.md](docs/quality-gates.md)
11. [docs/adr-guidelines.md](docs/adr-guidelines.md)

AIと人間の役割分担は [docs/ai-human-boundary.md](docs/ai-human-boundary.md) にまとめています。
よくある失敗パターンは [docs/anti-patterns.md](docs/anti-patterns.md) にまとめています。

## セキュリティとプライバシー

devlogやプロジェクト文書には、秘密情報、認証情報、個人情報、管理画面URL、社内固有情報を含めないでください。

詳しくは [docs/security.md](docs/security.md) を参照してください。

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
