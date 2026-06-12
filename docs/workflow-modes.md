# Workflow Modes

このワークフローは、すべてのプロジェクトに同じ重さで適用するものではありません。
作業の重要度や規模に応じて、3つのモードを使い分けます。

## Mode Selection Rule

デフォルトは **Standard mode** です。

ユーザーが明示しない限り、AIはまずStandard modeとして扱います。
そのうえで、作業内容とリスクを見て、理由を明示してMinimalまたはStrictに切り替えます。

### Minimalに下げてよい条件

AIは、次をすべて満たす場合だけMinimal modeに下げてもよいです。

- 作業が小さい
- 変更を戻しやすい
- ユーザー影響が低い
- プロダクトの挙動を変えない、または影響が非常に限定的である
- データ、認証、権限、課金、個人情報、本番設定に触れない
- 公開範囲、リリース、外部依存、アーキテクチャに影響しない

Minimalに下げる場合、AIは理由を明示します。

例:

```text
この作業はREADMEの誤字修正のみで、挙動、データ、セキュリティ、本番設定に影響しないためMinimal modeで進めます。
```

### Strictに上げる条件

次を含む場合、AIは必ずStrict modeに上げます。

- 認証
- 権限
- 課金、決済、サブスクリプション
- 個人情報、顧客情報
- DB変更、データ移行、データ削除
- 本番設定、インフラ、デプロイ
- 外部API、外部サービス、依存ライブラリ追加
- 公開リリース
- アーキテクチャ変更
- 取り消しにくい変更

Strictに上げる場合、AIは理由を明示します。

例:

```text
この作業は認証と権限に関わるため、Strict modeで進めます。
```

### 判断に迷う場合

判断に迷う場合はStandard modeを使います。

ただし、Strict modeが必要な可能性がある場合は、実装前に止まり、ユーザーに確認します。

## Minimal

小さく始めるための最小構成です。

### 向いている用途

- 学習用プロジェクト
- 小さな個人開発
- 数時間から数日の作業
- まずログを残す習慣を作りたい場合

### 使うファイル

- `docs/PROJECT_STATUS.md`
- `templates/implementation-plan.md`
- `templates/devlog.md`

### 守ること

- Requirement Alignment Firstは必ず守る
- Minimalに下げた理由を記録する
- 実装前に目的と完了条件を書く
- 終了時に判断理由を1つ以上残す
- テストや手動確認の結果を書く

## Standard

継続的な個人開発や、面接で見せるポートフォリオに向いています。

### 向いている用途

- 1週間以上続く個人開発
- 複数フェーズに分かれる開発
- AI支援開発の進め方を外部に説明したい場合
- 途中で別チャットに切り替える開発

### 使うファイル

- Minimal の全ファイル
- `workflows/session-start.md`
- `workflows/session-end.md`
- `templates/completion-review.md`
- `templates/roadmap.md`

### 守ること

- Requirement Alignment Firstは必ず守る
- 1タスク1セッションを基本にする
- 作業開始時に現在地を復元する
- 完了前レビューを通す
- 重要判断はdevlogに残す

## Strict

公開前、複数人開発、重要な設計変更に使う厳格なモードです。

### 向いている用途

- 本番公開前
- 認証、権限、課金、個人情報を扱う変更
- 大きなアーキテクチャ変更
- 複数人での開発
- 長期運用するプロジェクト
- データ移行や本番設定を変更する作業
- 外部依存やライブラリを追加する作業

### 使うファイル

- Standard の全ファイル
- `docs/review-checklist.md`
- `docs/security.md`
- `docs/definition-of-done.md`
- `docs/strict-mode.md`
- プロジェクト固有の `docs/ARCHITECTURE.md`
- プロジェクト固有の `docs/README.md`
- 必要に応じて `docs/adr/`

### 守ること

- Requirement Alignment Firstは必ず守る
- Strictに上げた理由を記録する
- 変更対象と変更しない対象を明確にする
- セキュリティとプライバシーを確認する
- テスト、ビルド、手動確認を記録する
- 見送った選択肢と理由を残す
- 未完了事項を隠さない
- ロールバックまたは復旧方法を記録する
- 最終判断者を明確にする

各モードでどの品質ゲートを最低限通すかは [quality-gates.md](quality-gates.md) を参照してください。

## モード選択の目安

| 状況 | 推奨モード |
|---|---|
| 30分以内の軽微な修正 | Minimalに下げてもよい |
| 新機能を1つ追加する | Standard |
| 不具合の原因調査 | Standard |
| 認証や権限を変更する | Strict |
| 課金、個人情報、データ移行を扱う | Strict |
| 依存ライブラリを追加する | Standard、影響が大きければStrict |
| 公開前チェック | Strict |
| READMEだけの小修正 | Minimal |

## 作業中のモード変更

作業中に当初の見立てと違うリスクが見つかった場合、AIはモードを変更します。

- Minimalで始めたが、挙動変更が必要になった場合はStandardに上げる
- Standardで始めたが、認証、権限、個人情報、本番設定などに触れると分かった場合はStrictに上げる
- Strict条件に該当する可能性があるが判断できない場合は、実装を止めてユーザーに確認する

モードを変更した場合、implementation plan、completion review、devlog、PRに理由を残します。
