# Pull Request Template

このドキュメントは、`.github/pull_request_template.md` の目的と使い方を説明します。

Pull Request Templateは、GitHubでPull Requestを作成するときに本文へ自動で入る確認シートです。
このワークフローでは、AIが作った変更をそのまま信用せず、変更範囲、検証結果、判断理由、残るリスクを人間が確認できる形に戻すために使います。

## Pull Requestとは

Pull Requestは、作業ブランチで行った変更をmainブランチへ取り込んでよいか確認する依頼です。

初心者向けに言うと、次のような流れです。

```text
作業用ブランチを作る
→ ファイルを変更する
→ テストや確認を行う
→ Pull Requestを作る
→ 変更内容、理由、検証結果、リスクを書く
→ レビューしてからmainへ取り込む
```

mainへ直接pushする場合、このテンプレートは自動では使われません。
直接pushする作業では、completion review、devlog、コミットメッセージ、実行した検証で同じ情報を残します。

## なぜAI駆動開発で必要か

AIを使うと実装は速くなります。
一方で、次の問題も速く混ざります。

- ユーザーの依頼とAIの理解が少しずれたまま実装される
- AIが「ついでに」範囲外の変更を入れる
- テストや手動確認を実行しないまま完了扱いになる
- 設計判断の理由がチャットの中に埋もれる
- ログ、スクリーンショット、設定ファイルに秘密情報や個人情報が混ざる
- 将来の作業者が、なぜその変更を入れたのか追えなくなる

Pull Request Templateは、これらをレビュー前に確認するための最低限の型です。
テンプレートを埋めること自体が目的ではありません。
レビューする人が、変更を取り込んでよいか判断できる状態を作ることが目的です。

## いつ使うか

GitHubでPull Requestを作る作業では使います。

特に次の変更では、Pull Requestを使う価値が高くなります。

- 複数ファイルにまたがる変更
- 初期設定、ワークフロー、品質ゲートの変更
- 認証、権限、課金、個人情報、本番設定、公開リリースに関わる変更
- 設計判断やADR候補がある変更
- 将来の利用者やチームメンバーが確認する必要がある変更

小さな文言修正など、mainへ直接pushする運用を選ぶ場合でも、テンプレートにある観点は確認します。

## 各項目の意味

### Summary

何を変えたか、なぜ変えたかを書きます。

悪い例:

```text
修正しました。
```

良い例:

```text
PRテンプレートの使い方が初心者に伝わりにくかったため、各項目の意味と記入例を説明するドキュメントを追加した。
```

### Workflow Mode

今回の作業をどの重さで進めたかを書きます。

- Minimal: 小さく、戻しやすく、低リスクな作業
- Standard: 通常の機能追加、バグ修正、UI改善
- Strict: 認証、権限、課金、個人情報、本番、公開、設計変更など高リスクな作業

Workflow Modeは導入時に固定するものではありません。
タスクごとに、変更内容とリスクを見て選びます。

### Related Artifacts

関連する作業記録へのリンクを書きます。

Related Artifactsに書くものは、実際の成果物置き場ではありません。
`docs/tasks/` は、認識合わせ、実装計画、完了レビューなどのタスク記録を残す場所です。
実際のコード、テスト、UI、設定ファイルは通常のプロジェクト構成の中に置きます。

例:

```text
Task records: docs/tasks/2026-06-23-pr-template-guide/
Implementation plan: docs/tasks/2026-06-23-pr-template-guide/implementation-plan.md
Completion review: docs/tasks/2026-06-23-pr-template-guide/completion-review.md
Devlog: docs/devlog/2026-06-23/pr-template-guide.md
```

### ADR Decision

ADRはArchitecture Decision Recordの略で、設計判断の記録です。

次のような判断がある場合は、ADR候補として扱います。

- 新しい技術スタックを採用する
- 認証方式や権限設計を変える
- データ構造やディレクトリ構成を大きく変える
- 将来の開発方針に影響する選択をする

すべての変更にADRは不要です。
不要な場合は、なぜ不要かをdevlogやPRに短く残します。

### Scope Check

今回やる範囲と、やらない範囲を確認します。

AI駆動開発では、AIが良かれと思って範囲外の変更を混ぜることがあります。
Scope Checkはそれを防ぐ欄です。

見るべきこと:

- ユーザーの依頼とAIの理解が一致しているか
- 今回の変更対象が明確か
- 関係ないファイルを変えていないか
- 予定外の変更がある場合、その理由を書いているか

### Verification

実行した確認を書きます。

書くべきものは、成功したコマンドだけではありません。
スキップした確認がある場合も、理由を書きます。

例:

```text
bash scripts/check-docs.sh: passed
python scripts/test-project-structure.py: passed
Manual browser check: skipped, documentation-only change
project structure checker: DIRECTORY_MAP_VERIFIED
```

「AIが大丈夫と言った」は検証ではありません。
実行したコマンド、手動確認、確認できなかった理由を残します。

### Security and Privacy

秘密情報、個人情報、認証情報が混ざっていないか確認します。

特に確認するもの:

- 認証トークン
- Cookie
- APIキー
- private key
- 顧客情報
- 個人情報
- ローカル環境のパスやスクリーンショット
- ログに含まれる機密情報

セキュリティやプライバシーに関係しない変更でも、「関係しない」と判断した理由を短く書きます。

### Strict Mode Gate

Strict modeのときだけ埋める欄です。

高リスクな変更では、少なくとも次を確認します。

- リスクレビューを書いたか
- 問題が起きたときの戻し方を書いたか
- 人間の承認が必要か
- リリースや本番環境への影響があるか

初心者向けに言うと、「失敗したときに戻せるか」「人間が最終判断すべきか」を見る欄です。

### Remaining Risk

まだ残っている不安点を書きます。

例:

```text
Windowsでは確認済み。macOSとLinuxでは未確認。
```

```text
自動テストは通過。スマートフォン実機での表示確認は未実施。
```

リスクを隠すと、次の作業者が同じ場所で失敗します。
残るリスクは、弱点ではなく、次に見るべき場所の案内です。

## 最小記入例

小さなドキュメント修正なら、次の粒度で十分です。

```text
Summary:
PRテンプレートの使い方を初心者向けに説明するドキュメントを追加した。

Workflow Mode:
Standard
Reason: ドキュメント追加だが、GitHub運用とstarter配布物に影響するため。

Related Artifacts:
なし。小規模な説明追加のため、PR本文とコミットで追跡する。

ADR Decision:
ADR not needed. 設計判断ではなく説明追加のため。

Verification:
bash scripts/check-docs.sh: passed
git diff --check: passed

Security and Privacy:
秘密情報、個人情報、認証情報の追加なし。

Remaining Risk:
なし。
```

## このテンプレートで守りたいこと

このテンプレートが守るのは、形式ではなく判断の品質です。

- 何を変えたか分かる
- なぜ変えたか分かる
- どこまでAIに任せたか分かる
- 何を人間が確認したか分かる
- どの検証を実行したか分かる
- 残るリスクが隠されていない

AI駆動開発では、速さだけでなく、後から確認できることが重要です。
Pull Request Templateは、その確認をGitHub上に残すための入口です。
