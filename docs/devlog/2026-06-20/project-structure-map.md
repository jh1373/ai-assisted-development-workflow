# Project Structure Map導入

## 作業テーマ

新規プロジェクトの構造、責務、境界、構造差分を機械検証し、localhostで可視化する機能を導入した。

## 関連するタスク記録

```text
docs/tasks/2026-06-20-project-structure-map/
```

## なぜやったか

手動の `docs/DIRECTORY_MAP.md` だけでは、ファイル追加やディレクトリ整理後のずれを検出できず、AIが古い構造理解で実装範囲を決める危険があった。Understand Anythingの「全体像を視覚化する」発想は採用しつつ、コード意味解析ではなく、このリポジトリの目的である責務、境界、タスク導線の管理へ最適化した。

## 変更したこと

- Python標準ライブラリだけで動くProject Structure CLIを追加した。
- JSON正本、path-only snapshot、生成Markdownを分離した。
- 全ファイルを表示するread-only localhostビューアを追加した。
- 初期化、session-start、session-end、AGENTS、CI、品質文書へ構造ゲートを統合した。
- starterと初期化例、React例を新方式へ揃えた。

## 判断したこと

### Workflow Mode

- Selected mode: Strict
- Reason: アーキテクチャ、HTTP、CI、配布物全体へ影響するため
- Mode changes during work: なし

### Directory Map

- Impact: updated
- Checker result: starterとexamplesはDIRECTORY_MAP_PROVISIONAL
- Reason: 初回構築前の配布物なので、利用者の構造承認前にVerifiedへしないため
- Updated JSON / snapshot / generated Markdown: JSONと生成Markdownを追加。snapshotは利用プロジェクトでverify時に生成する

### 採用した方針

- 構造判定はパスと種別だけに限定し、ソースコード内容を読まない。
- 役割は明示、明示pattern、規約、親継承、未分類を区別する。
- 役割が規約由来でも、親ディレクトリの境界と関連タスクは継承する。
- localhostは127.0.0.1へ限定し、APIはランダムtokenで保護する。
- Provisionalは最初の構築タスクだけ許容し、通常運用はVerifiedを要求する。

### 見送った選択肢

- Understand Anythingのコードや依存構成をコピーすること
- ソースコード解析、LLM、embedding、ベクトルDBを導入すること
- Markdownを正本のまま維持すること
- ファイル変更ごとにブラウザを自動再読み込みすること

### 理由

- この機能の目的はコード知識グラフではなく、構造ドリフトと責務境界の運用管理である。外部依存を増やさず、1〜2秒のpollingで十分な鮮度を得る方が導入時の再現性が高い。

## ADR

- アーキテクチャ判断ではあるが、ユーザー確認なしでADRを作成しない運用ルールに従い未作成。既存の `docs/design-rationale.md` とこのdevlogへ理由を残した。

## 発生した問題と対応

- in-app browserが実行環境のmetadata不足で起動できなかったため、既に導入済みのMicrosoft Edge headlessでread-only表示確認を行った。
- 390px指定のEdge headlessはWindows側の最小window幅で画像がcropされたため、CSSの650px以下media queryが適用される500px幅で狭幅レイアウトを確認した。
- 規約判定したファイルが親の禁止事項を失う欠陥を見つけ、役割判定と境界継承を分離した。
- 古いsession-startとReact例が手動Markdown更新を許していたため、JSON正本と生成手順へ統一した。

## 検証

```text
docs check, Markdown links, secret patterns: passed
Project Structure unit/integration tests: passed (Windows symlink permission test only skipped)
Bash, pwsh, Windows PowerShell initialization tests: passed
JavaScript, Bash, Python syntax checks: passed
starter and examples generated documents: current
HTTP token, CSP, fixed asset allowlist, traversal rejection, live update: passed
desktop and narrow-width UI: visually confirmed
```

## 未完了・注意点

- symlinkの動的作成テストは、権限を許可したWindowsまたはLinux CIでも実行すると追加証拠になる。
- `verify` は初期設定で人間が構造案を承認してから実行する。starterを事前にVerifiedへしてはいけない。

## Definition of Done確認

- 全要件をコード、テスト、文書、starter、examples、CIへ反映した。自動検証と実画面確認が成功し、既知の注意点を記録した。

## 次にやること

- ユーザーが差分を確認した後、必要ならコミットとpushを行う。
