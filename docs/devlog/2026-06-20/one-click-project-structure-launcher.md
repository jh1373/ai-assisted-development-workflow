# Project Structure Mapワンクリック起動

## 作業テーマ

Windows利用者がコマンドを入力せず、`.cmd`のダブルクリックだけで構造ビューアを開けるようにした。

## 関連するタスク記録

```text
docs/tasks/2026-06-20-one-click-project-structure-launcher/
```

## なぜやったか

従来はtoken付きURLを得るためにPowerShellでPythonコマンドを実行し、そのURLをブラウザへ貼り付ける必要があった。エンジニア初心者が日常的に使うには操作が多く、可視化機能があっても利用されなくなる可能性があった。

## 判断したこと

### Workflow Mode

- Selected mode: Standard
- Reason: CLIと利用経路の追加であり、認証、データ、本番環境を変更しないため

### Directory Map

- Impact: updated
- Checker result: DIRECTORY_MAP_PROVISIONAL
- Reason: starterルートへ新しいランチャーを追加したため
- Updated JSON / snapshot / generated Markdown: JSONと生成Markdownを更新。Provisionalのためsnapshotは作成しない

### 採用した方針

- token生成とブラウザ起動はPython側で行う。
- `.cmd`はPython検出とCLI呼び出しだけに限定する。
- ブラウザ起動に失敗してもlocalhostサーバーは継続する。

### 見送った選択肢

- `.cmd`側で標準出力からtoken URLを解析する方法
- PowerShell専用ランチャー
- Pythonの自動インストール

### 理由

- token解析を`.cmd`へ持たせると引用符や非同期起動が複雑になる。Python標準の`webbrowser`を使う方が責務が明確で、Windows以外からのCLI利用にも再利用できる。

## ADR

- 既存CLIの小規模な拡張であり、独立した長期アーキテクチャ判断ではないため不要。

## 検証

```text
自動テスト、三種類の初期化テスト、文書検査、構文検査に成功。
.cmdを実際に起動し、Pythonプロセスが127.0.0.1:4173で待ち受け、token URLがHTTP 200を返すことを確認。
```

## 未完了・注意点

- 既定ブラウザ未登録時は、コンソールに表示されたURLを手動で開く。

## Definition of Done確認

- ダブルクリック相当の実行、エラー経路、starter同期、文書、テストを確認済み。

## 次にやること

- コミット、push後にGitHub Actionsの結果を確認する。
