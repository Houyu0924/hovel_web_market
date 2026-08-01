# HOVEL Loop Engineering v0.1

HOVELのコンテンツ運営を、単発プロンプトではなく「目標・実行・検証・停止・学習」の循環として管理するための基盤です。

## 目的

読者の悩みを発見し、記事・X投稿・商品レビューとして実行し、反応データから次の投資先を決める。

```text
Trigger / Discovery
        ↓
Execution
        ↓
Verification
        ↓
Human Approval
        ↓
Publish / Distribute
        ↓
Measurement
        ↓
Decision / Memory
        └────────────→ Next Loop
```

## v0.1で実装する3ループ

1. 公開後改善ループ
2. X投稿改善ループ
3. 商品レビュー検証ループ

## 運用原則

- GitHubをSSOTとする
- AIは下書き・集計・候補生成まで自動化できる
- 健康表現、商品推奨、公開、購入は人間承認を必須とする
- AIの自己申告ではなく、ファイル・数値・チェック結果を完了証拠とする
- 同じ失敗を3回繰り返した場合は停止し、人間へエスカレーションする

## ディレクトリ

```text
loop-engineering/
├── README.md
├── config/
│   ├── goals.yml
│   ├── quality-gates.yml
│   └── stop-conditions.yml
├── schemas/
│   ├── article-metrics.schema.json
│   ├── x-post-experiment.schema.json
│   └── product-review.schema.json
├── data/
│   ├── content-metrics.csv
│   ├── x-experiments.csv
│   └── product-reviews.csv
├── prompts/
│   ├── weekly-review.md
│   ├── x-post-optimizer.md
│   └── product-review-evaluator.md
└── workflows/
    └── operating-procedure.md
```

## 初期KPI

- note月間PV: 127 → 250
- noteスキ率: 9 / 127 = 7.1%を維持または改善
- Amazonアソシエイト月間クリック: 2 → 10
- Xフォロワー: 17 → 30
- X投稿: 週14本
- 価値ある返信: 週35件
- 商品レビュー: 1件開始

## 完了条件

v0.1は、以下を満たした時点で稼働開始とみなします。

- KPIと停止条件が設定されている
- 3ループの入力フォーマットが存在する
- 毎週レビュー用プロンプトが存在する
- オールドスパイス検証データを記録できる
- 人間承認ポイントが明記されている
