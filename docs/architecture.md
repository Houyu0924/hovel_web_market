# HOVEL Repository Architecture

## Single Source of Truth

GitHubをHOVEL編集部の正式な管理基盤とする。

## 管理対象

- 記事案件: `jobs/`
- 記事候補: `ideas/backlog.csv`
- キーワード: `keywords/`
- 商品情報: `products/`
- 下書き: `content/drafts/`
- 公開原稿: `content/published/`
- AIプロンプト: `prompts/`
- KPI: `data/`
- 運用ルール: `docs/`

## 原則

1. 1記事につき1案件ファイルを作る
2. 工程状態は案件ファイルとバックログの両方で一致させる
3. AIの判断根拠を成果物に残す
4. 公開情報と実機検証を区別する
5. 公開後はPVだけでなくCTR、収益、更新必要性を記録する
