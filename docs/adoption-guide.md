# Adoption Guide

既存プロジェクトにこのワークフローを導入するための手順です。

## 目的

このガイドは、テンプレートをただ置くだけではなく、実際に開発で使える状態にすることを目的にしています。

## Step 1: 導入モードを選ぶ

最初からすべてを導入する必要はありません。

- 小さく始める: Minimal
- 継続開発で使う: Standard
- 公開前や複数人開発で使う: Strict

迷った場合は Standard から始めます。

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
  implementation-plan.md
  completion-review.md
  devlog.md
```

このリポジトリの `workflows/` と `templates/` から必要なファイルをコピーします。

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

## Step 6: 実装計画を作る

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

## Step 7: 完了前レビューを行う

`templates/completion-review.md` を使い、作業漏れを確認します。

ここで見るのは、コードが書けたかだけではありません。

- 計画した作業が終わっているか
- 余計な変更が混ざっていないか
- テストやビルドが通っているか
- ドキュメント更新が必要か
- 次回に残すべき注意点があるか

## Step 8: devlogを書く

`templates/devlog.md` を使い、判断理由を残します。

devlogは作業日報ではありません。  
後から判断を追うための記録です。

## Step 9: Gitに記録する

最後に差分を確認し、必要なファイルだけをコミットします。

```bash
git status --short
git diff --check
git add [files]
git commit -m "[short message]"
```

コミットメッセージは短くて構いません。  
理由はdevlogに残します。

## 導入時の注意

- 既存プロジェクトのルールを上書きしない
- テンプレートはプロジェクトに合わせて削る
- 秘密情報をdevlogに書かない
- すべての作業で重い手順を強制しない
- 小さな修正ではMinimal運用に落とす
