# Session End Workflow

開発セッションの終了時に、作業内容、判断理由、検証結果を残すための手順です。

## 目的

- Gitに差分を残すだけでなく、判断理由を残す
- 次のセッションで迷わず再開できるようにする
- 失敗した試行や見送った選択肢を消さずに残す
- 完了前に漏れや未検証を確認する
- DIRECTORY_MAPの更新要否を確認する

## 手順

### 1. 完了前レビューを行う

`templates/completion-review.md` を使い、今回の作業が計画通りに終わっているか確認します。
完了前レビューは、タスク記録フォルダに保存します。

保存先の例:

```text
docs/tasks/YYYY-MM-DD-HHMM-task-name/completion-review.md
```

見ること:

- ユーザーの元要望と最終成果物が合っているか
- 完了したこと
- 未完了のこと
- 計画から変わったこと
- 意図していない変更
- 検証結果
- 次のセッションへの引き継ぎ

完了判断は `docs/ai-workflow/definition-of-done.md` を基準にします。
コードを書いたことではなく、検証され、次回再開できる状態になったことを確認します。

### 2. 計画とのズレを確認する

最初に作った計画と、実際の作業結果を比較します。

確認すること:

- 計画したタスクは完了したか
- 途中で方針変更があったか
- 予定外の変更が混ざっていないか
- やらないと決めた範囲に触れていないか

### 3. テストとビルドを確認する

プロジェクトに応じて、必要な検証を行います。

例:

```bash
npm test
npm run build
git diff --check
```

成功した場合は、devlogに実行したコマンドと結果を要約します。
失敗が残る場合は、隠さず未完了事項として記録します。

### 4. devlogを書く

`templates/devlog.md` を使い、作業ログを作成します。

タスクを実行した場合は、必ずdevlogを残します。
小さい修正では短くて構いませんが、判断理由、検証結果、未完了事項の3つは省略しません。

保存先の例:

```text
docs/devlog/YYYY-MM-DD/HHMM-task-name.md
```

devlogで重視するのは、作業量ではなく判断理由です。

書くこと:

- なぜこの作業をしたか
- 何を変更したか
- どの選択肢を見送ったか
- どんな問題があったか
- 何を検証したか
- 何が未完了か
- 次に何をするべきか

長期的に残すべき設計判断がある場合は、devlogだけでなくADRを作成します。
ただし、AIはADRを勝手に確定しません。
ADR候補を検知した場合は、[docs/ai-workflow/adr-guidelines.md](../docs/ai-workflow/adr-guidelines.md) に沿ってユーザーに確認します。
ADRのテンプレートは `templates/adr.md` です。

devlogには、関連するタスク記録フォルダとADRの有無を記録します。

### 5. Directory Mapの更新要否を確認する

`docs/DIRECTORY_MAP.md` は生成文書なので直接編集しません。
次を実行し、承認済み基準線との差分を確認します。

```bash
python scripts/project-structure.py validate
python scripts/project-structure.py diff
```

`DIRECTORY_MAP_VERIFIED`なら構造更新は不要です。
`DIRECTORY_MAP_DRIFT_DETECTED`なら、追加、削除、移動、役割、境界への影響を確認します。

更新が必要な例:

- 新しい主要ディレクトリを追加した
- 既存ディレクトリの責務を変えた
- ファイル配置ルールを変えた
- タスク別の参照先が変わった
- 次回のAIが迷いそうな構成変更をした

更新不要な例:

- 既存ディレクトリ内の小さなUI変更
- 文言修正
- テスト追加のみ
- README更新のみ
- ディレクトリ責務に影響しない小さな修正

構造変更を受け入れる場合は、先に `.ai-workflow/directory-map.json` の役割と境界を更新します。
未分類、登録パス欠落、走査警告を解消した後、基準線とMarkdownを更新します。

```bash
python scripts/project-structure.py refresh --by "User or reviewer"
```

Provisionalから最初のVerifiedへ移す場合は、ユーザーが全体構造と役割を確認した後に実行します。

```bash
python scripts/project-structure.py verify --verified-by "User"
```

更新要否、差分、実行結果、理由はcompletion reviewまたはdevlogに残します。

例:

```text
Directory Map impact: none
Reason: 既存ディレクトリ内のUI表示変更のみで、責務や構成に変更なし。
```

```text
Directory Map impact: updated
Reason: `src/features/search/` を追加し、JSON正本へ検索機能の責務と参照先を明記してsnapshotを更新した。
```

### 6. プロジェクト状態を更新する

必要に応じて、次のようなファイルを更新します。

- `docs/PROJECT_STATUS.md`
- `docs/ROADMAP.md`
- `.ai-workflow/directory-map.json`
- `.ai-workflow/directory-snapshot.json`
- `docs/DIRECTORY_MAP.md`（生成）
- `docs/ARCHITECTURE.md` がある場合
- `docs/README.md`

ただし、単純な修正まで毎回すべて更新する必要はありません。
次回の再開に必要な情報だけを更新します。

### 7. Gitに記録する

差分を確認し、必要なファイルだけをコミットします。

```bash
git status --short
git diff --check
git add [files]
git commit -m "[message]"
```

コミットメッセージは短く、devlogで理由を補足します。

## 終了時の確認テンプレート

```text
完了したこと:
- ...

検証:
- ...

未完了:
- ...

更新したドキュメント:
- ...

Directory Map impact:
- ...

タスク記録:
- ...

Devlog:
- ...

ADR:
- ...

コミット:
- ...
```

## 書かないもの

devlogや公開ドキュメントには、次の情報を含めません。

- APIキー
- パスワード
- トークン
- 秘密鍵
- 管理画面URL
- 個人情報
- 社内固有の機密情報
- 長すぎるコマンド出力
- チャット全文
- 未確認の成功表現
- AIの回答を根拠にしただけの完了判断
