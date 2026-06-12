# Adoption Guide

既存プロジェクトにこのワークフローを導入するための手順です。

## 目的

このガイドは、テンプレートをただ置くだけではなく、実際に開発で使える状態にすることを目的にしています。

## Step 1: 導入モードを選ぶ

最初からすべてを導入する必要はありません。

- 小さく始める: Minimal
- 継続開発で使う: Standard
- 公開前や複数人開発で使う: Strict

デフォルトはStandardです。
AIは、低リスクなら理由を明示してMinimalに下げ、高リスクなら必ずStrictに上げます。
迷った場合はStandardを使います。
Strictの可能性がある場合は、実装前にユーザーへ確認します。

導入前に [principles.md](principles.md)、[requirement-alignment.md](requirement-alignment.md)、[practical-guide.md](practical-guide.md) を読み、なぜこの運用を入れるのか、1タスクをどう進めるのかを先に共有します。
テンプレートだけを置いても、判断理由を残す文化がなければ効果は限定的です。

## Step 2: ファイルを配置する

Standard の場合、次の構成を推奨します。

```text
docs/
  PROJECT_STATUS.md
  ROADMAP.md
  devlog/
workflows/
  session-start.md
  session-end.md
templates/
  AGENTS.md
  adr.md
  requirement-alignment.md
  implementation-plan.md
  completion-review.md
  devlog.md
  security-review.md
  rollback-plan.md
.github/
  pull_request_template.md
  ISSUE_TEMPLATE/
```

このリポジトリの `workflows/` と `templates/` から必要なファイルをコピーします。

AIエージェントを使うプロジェクトでは、`templates/AGENTS.md` をプロジェクト用に編集し、リポジトリルートの `AGENTS.md` として配置します。

## Step 3: PROJECT_STATUSを書く

`docs/PROJECT_STATUS.md` は、次のセッションで最初に読む現在地メモです。

最低限、次を書きます。

- 今のフェーズ
- 完了済み
- 進行中
- 次にやること
- 注意点
- 最後に確認したテストやビルド

## Step 4: ROADMAPを書く

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

## Step 5: 最初のセッションを始める

`workflows/session-start.md` を使い、現在地を復元します。

確認すること:

- Git状態
- PROJECT_STATUS
- ROADMAP
- 最新devlog
- テストやビルドの状態

## Step 6: 要件認識合わせを行う

ユーザーの要望が短い場合や、意図、範囲、完了条件に曖昧さがある場合は、`templates/requirement-alignment.md` を使います。

確認すること:

- ユーザーの元要望
- AI側の理解
- 実装対象と対象外
- 不明点、曖昧な点、懸念点
- AIが置いた仮定
- ユーザー確認結果

未回答の重要な不明点がある場合は、実装に進みません。

## Step 7: 実装計画を作る

`templates/implementation-plan.md` を使います。

計画には、次の観点を必ず入れます。

- 目的
- 背景
- 変更するもの
- 変更しないもの
- 実装手順
- 影響範囲
- リスク
- 検証方法
- 完了条件

完了条件を書くときは、[definition-of-done.md](definition-of-done.md) を基準にします。

## Step 8: 完了前レビューを行う

`templates/completion-review.md` を使い、作業漏れを確認します。

ここで見るのは、コードが書けたかだけではありません。

- 計画した作業が終わっているか
- 余計な変更が混ざっていないか
- テストやビルドが通っているか
- ドキュメント更新が必要か
- 次回に残すべき注意点があるか

重要な設計判断が発生した場合は、`templates/adr.md` を使って `docs/adr/` に記録します。
devlogは作業判断、ADRは長期的な設計判断を残すために分けます。

Strict modeでは、必要に応じて `templates/security-review.md` と `templates/rollback-plan.md` も作成します。

## Step 9: devlogを書く

`templates/devlog.md` を使い、判断理由を残します。

devlogは作業日報ではありません。
後から判断を追うための記録です。

## Step 10: Gitに記録する

最後に差分を確認し、必要なファイルだけをコミットします。

```bash
git status --short
git diff --check
git add [files]
git commit -m "[short message]"
```

コミットメッセージは短くて構いません。
理由はdevlogに残します。

## Step 11: PRとCIに接続する

GitHubを使う場合は、`.github/pull_request_template.md` と `.github/workflows/docs-check.yml` を導入します。

これにより、PR上で次を確認しやすくなります。

- workflow mode
- mode selection reason
- 関連する計画、レビュー、devlog、ADR
- 予定外の変更
- 検証結果
- セキュリティとプライバシー
- Strict modeの追加ゲート

CIでは `scripts/check-docs.sh` により、最低限の文書構造、未解決プレースホルダー、秘密情報らしき文字列、ローカルリンクを確認します。

品質ゲートの考え方は [quality-gates.md](quality-gates.md) を参照してください。
チームで導入する場合は [team-development.md](team-development.md) を先に読み、誰がレビューし、誰が最終判断するかを決めてから運用します。

## 導入時の注意

- 既存プロジェクトのルールを上書きしない
- テンプレートはプロジェクトに合わせて削る
- 秘密情報をdevlogに書かない
- すべての作業で重い手順を強制しない
- 小さな修正ではMinimal運用に落とす
- Minimalに下げる場合とStrictに上げる場合は理由を残す
- PRやCIを入れても、人間のレビュー責任はなくならない
- Strict modeはチェック欄を埋めることではなく、リスクを証拠付きで扱うこと
