# Project Structure Map Implementation Plan

## 目的

新規プロジェクトの全ディレクトリと全ファイルを機械的に把握し、責務、変更差分、未分類項目をローカル画面で確認できる機能を導入する。

## 背景

従来の `docs/DIRECTORY_MAP.md` は人手更新のため、構造変更とのずれを継続検出できなかった。Understand Anythingの「全体像を視覚的に把握する」という発想を採り入れるが、コード解析グラフではなく、このリポジトリの運用目的に合わせた構造・責務管理に限定する。

## Requirement Alignment

- [x] ユーザーの元要望を確認した
- [x] AI側の理解を要約した
- [x] 不明点、曖昧な点、懸念点を洗い出した
- [x] AIが置いた仮定を明示した
- [x] 必要なユーザー確認を行った
- [x] 未回答の重要な不明点が残っていない

確認メモ:

- Pythonは推奨実装とする。
- 全ファイルを表示し、1〜2秒間隔で自動更新する。
- ファイル内容は読み取らず、パスと種別だけを扱う。
- 役割は明示、継承、規約、未分類を区別し、AIが推測で確定しない。

## 対象範囲

### 変更するもの

- Python標準ライブラリだけで動く構造検証CLI
- JSON正本、path-only snapshot、生成Markdown
- localhost専用のツリービューア
- 初期化、session-start、session-end、CIへの構造ゲート統合
- starter、テンプレート、例、説明文書、テスト

### 変更しないもの

- ソースコードの意味解析
- 外部AI API、ベクトルDB、依存パッケージ
- 既存プロジェクト向け移行フロー
- リモート公開される構造ビューア

## Directory Context

Project Structure Gate result:

- 導入前の手動 `DIRECTORY_MAP` を置き換える機能自体の実装であるため、既存文書とstarter全体を対象にした。

Related directories:

- `scripts/`, `starter/`, `workflows/`, `templates/`, `docs/`, `examples/`, `.github/`

Responsibilities:

- 実行機能、配布物、運用手順、説明、CIを同期させる。

Boundaries not to cross:

- ファイル内容をsnapshotまたはHTTPレスポンスへ含めない。
- localhost以外へbindしない。

Files to inspect before implementation:

- README、初期化/session workflows、AGENTS template、既存DIRECTORY_MAP、docs check

Directory Map update candidate:

- manual MarkdownをJSON正本と生成Markdownへ移行する。

## Workflow Mode

- Strict

Mode selection reason:

- 構造管理のアーキテクチャ変更、ローカルHTTPサーバー、CI、配布starter全体へ影響するため。

Mode change during work:

- なし

## 実装方針

1. JSON、snapshot、固定出力の契約を定義する。
2. scan、validate、diff、generate、refresh、verify、serveを実装する。
3. 全ファイルツリーと詳細パネルを実装する。
4. 初期化、各セッション、CI、文書へ統合する。
5. OS別、HTTPセキュリティ、生成物、UIを検証する。

## 影響範囲

- 新規プロジェクトの初回構造設計、通常タスク開始判定、終了時の構造更新、CI。

## リスク

- 正本と生成物の二重編集、未分類項目の見落とし、symlink経由の範囲外走査、HTTP経由の情報漏えい。

## Security and Privacy

- 127.0.0.1限定、ランダムtoken、固定assetだけを配信し、ファイル内容を読まない設計とする。

## Rollback / Recovery

- 新規追加ファイルと構造ゲート統合差分を取り除けば、従来の手動DIRECTORY_MAP運用へ戻せる。

## 検証方法

```text
bash scripts/check-docs.sh
python scripts/test-project-structure.py
bash scripts/test-initialization-checker.sh
pwsh -File scripts/test-initialization-checker.ps1
powershell -File scripts/test-initialization-checker.ps1
node --check scripts/project-structure-viewer/app.js
git diff --check
desktop/mobile screenshot inspection
```

## 完了条件

- 要件を自動テストと手動UI確認で証明できる。
- root、starter、examples、workflows、CIに矛盾がない。
- 未分類または構造driftを通常タスク開始前に止められる。
