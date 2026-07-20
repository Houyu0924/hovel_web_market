# HOVEL Affiliate Factory

HOVEL向けアフィリエイト記事の企画・制作・審査・公開管理を標準化する無料運用基盤です。

## 目的

- AIが調査、構成、執筆、審査の大部分を担当
- 運営者は事実確認、体験追記、リンク確認、公開判断に集中
- 未使用商品の体験談を捏造しない
- 記事数ではなく、検索流入・クリック・収益・更新性で評価

## 基本フロー

1. `ideas/backlog.csv` に記事候補を登録
2. `python scripts/create_job.py --keyword "..." --type comparison` を実行
3. `jobs/` に案件ファイルが生成される
4. AIプロンプトを順番に実行
5. `content/drafts/` に下書きを保存
6. Pull Requestで公開前レビュー
7. 公開後に `data/performance.csv` を更新

## ディレクトリ

- `config/` ブランド・審査基準
- `prompts/` AI担当別プロンプト
- `templates/` 記事・案件テンプレート
- `ideas/` 記事候補
- `jobs/` 制作案件
- `content/drafts/` 下書き
- `content/published/` 公開済み原稿
- `data/` KPI・商品情報
- `scripts/` 無料で動く補助スクリプト

## 最初の案件

`jobs/2026-07-20-eye-mask-comparison.md`

テーマは「会社員向けアイマスク比較」です。ただし既存記事と検索意図が重複する場合は、全面リライトではなく更新案件として扱ってください。
