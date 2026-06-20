# Directory Map Generated Document

`docs/DIRECTORY_MAP.md` は手動で記入するテンプレートではありません。

役割、境界、タスク別参照先の正本:

```text
.ai-workflow/directory-map.json
```

全パス構造のVerified基準線:

```text
.ai-workflow/directory-snapshot.json
```

Markdown生成:

```bash
python scripts/project-structure.py generate
```

初期設定ではJSONの`status`を`provisional`にし、予定している主要ディレクトリと責務だけを登録します。
初期構築後、実際の全ファイル、役割、境界をユーザーが確認してから次を実行します。

```bash
python scripts/project-structure.py verify --verified-by "User"
```

生成される文書には次が含まれます。

- ProvisionalまたはVerified
- 構造チェッカーの固定出力
- 現在と基準線の構造ハッシュ
- ファイル数、ディレクトリ数、未分類数
- 主要パスと責務
- タスク別の参照先
- 境界と禁止事項
- 構造差分件数

全ファイルツリーとライブ差分は次で確認します。

```bash
python scripts/project-structure.py serve
```

詳しい仕様は [Project Structure Map](../docs/project-structure-map.md) を参照してください。
