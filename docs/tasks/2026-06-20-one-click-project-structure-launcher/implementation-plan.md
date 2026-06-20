# One-click Project Structure Launcher Implementation Plan

## 目的

Windows利用者がコマンドを入力せず、プロジェクト直下のファイルをダブルクリックするだけでProject Structure Mapを起動できるようにする。

## Requirement Alignment

- [x] Windows向けのワンクリック起動を実装する
- [x] `.cmd`からlocalhostサーバーと既定ブラウザを起動する
- [x] Pythonを自動インストールせず、不足時は理由を表示する
- [x] starter、文書、生成DIRECTORY_MAP、テストを同期する
- [x] 検証後にコミットしてmainへpushする

## 対象範囲

### 変更するもの

- Project Structure CLIのブラウザ自動起動オプション
- starterのWindowsランチャー
- starter構造定義、生成文書、利用手順、テスト

### 変更しないもの

- localhostの公開範囲、token、read-only設計
- macOS/Linux向けデスクトップショートカット
- Pythonの自動インストール

## Directory Context

Project Structure Gate result:

- `DIRECTORY_MAP_PROVISIONAL`。starterの初回構築前状態として許容する。

Related directories:

- `scripts/`, `starter/`, `docs/`, `workflows/`

Boundaries not to cross:

- `127.0.0.1`以外へbindしない。
- tokenなしURLをブラウザへ渡さない。
- 起動失敗を隠してウィンドウを閉じない。

## Workflow Mode

- Standard

Mode selection reason:

- 新しい利用経路とCLIオプションを追加するが、認証、データ、本番環境、外部依存は変更しないため。

## 実装方針

1. Pythonへ`--open-browser`を追加する。
2. `.cmd`はPython検出、バージョン確認、CLI起動だけを担当する。
3. starter構造定義と生成文書へランチャーを追加する。
4. 単体テストと実際の`.cmd`起動で検証する。

## Security and Privacy

- Python標準の既定ブラウザ起動だけを使用する。URLは従来どおり一時token付きlocalhost URLとする。

## 検証方法

```text
bash scripts/check-docs.sh
python scripts/test-project-structure.py
bash/pwsh/Windows PowerShell initialization tests
starter/open-project-structure-map.cmd smoke test
git diff --check
```

## 完了条件

- `.cmd`のダブルクリック相当の実行で、viewerが起動しHTTP 200を返す。
- ブラウザ自動起動失敗時もサーバーは停止せず、手動URLを案内する。
- starterの未分類項目が0件である。
