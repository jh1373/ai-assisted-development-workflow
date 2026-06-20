# localhost tokenログ対策 計画

## 目的

プロジェクト案内図の一時tokenがAPIのURLとHTTPログへ表示される問題を解消する。

## 変更方針

- 初回tokenはURLクエリではなくURLフラグメントでブラウザへ渡す
- API認証は専用HTTPヘッダーを使用する
- URLクエリによるAPI認証を拒否する
- HTTPログ内のtokenは防御的に伏せ字にする
- `.cmd`の自動ブラウザ起動時は、起動メッセージにも実tokenを表示しない
- tokenがログへ残らないことを自動テストする

## 完了条件

- APIリクエストURLにtokenが含まれない
- URLクエリのtokenではAPIへアクセスできない
- 正しいHTTPヘッダーではAPIへアクセスできる
- HTTPログに実際のtokenが出力されない
- `.cmd`起動時のターミナルに実tokenが表示されない
- rootとstarterが同期し、全テストが成功する
