# HOVEL Problem Template v0.1

## 目的

HOVELにおけるすべての活動を、顧客の悩み（Problem）から一貫して開始するための標準テンプレート。

HOVELの最小管理単位は、記事・動画・商品ではなく **Problem** とする。

---

## 基本フロー

```text
Problem
  ↓
HPS評価
  ↓
Research
  ↓
HOVEL Lab
  ↓
Asset化
  ↓
公開・提供
  ↓
顧客反応
  ↓
改善
  ↓
Problemへ還流
```

---

## Problem登録テンプレート

```yaml
problem_id: P-0001

problem:
  title: 昼食後に眠くなる
  summary: 午後の集中力低下や業務ミスにつながる

categories:
  - BODY
  - WORK

target:
  primary: 25〜35歳の男性会社員
  context:
    - デスクワーク中心
    - 昼食後も会議や判断業務がある

customer_impact:
  - 集中力が落ちる
  - 判断ミスが増える
  - 生産性が低下する
  - 残業につながる

root_cause_hypotheses:
  - 睡眠不足
  - 昼食量
  - 食事構成
  - 食後行動
  - カフェイン依存
  - 日中の活動不足

hps:
  customer_value: 0      # 0-10
  repeatability: 0       # 0-10
  expandability: 0       # 0-10
  hovel_fit: 0           # 0-5
  evidence: 0            # 0-5
  asset_value: 0         # 0-5
  market_size: 0         # 0-3
  urgency: 0             # 0-1
  profitability: 0       # 0-1
  total: 0               # 0-50
  rank: D                # A/B/C/D
  version: v0.1

research:
  status: not_started
  sources:
    - PubMed
    - 厚生労働省
    - 学会・公的機関
  key_findings: []
  uncertainties: []

hovel_lab:
  required: true
  status: not_started
  hypothesis: ""
  protocol: ""
  period: ""
  metrics: []
  result: ""
  limitations: []

assets:
  planned:
    - article
    - youtube_long
    - short_video
    - checklist
    - ai_prompt
    - comparison_table
  created: []

commercialization:
  affiliate_candidates: []
  digital_product_candidates: []
  service_candidates: []

kpi:
  primary: []
  secondary: []
  actuals: {}

status:
  current: intake
  available_values:
    - intake
    - scored
    - research
    - lab
    - production
    - published
    - measuring
    - improving
    - archived

review:
  next_review_date: ""
  decision_log: []
```

---

## ステータス運用

| ステータス | 定義 |
|---|---|
| intake | 悩みを登録した段階 |
| scored | HPS評価済み |
| research | 市場・エビデンス調査中 |
| lab | HOVEL Labで検証中 |
| production | 記事・動画・資料を制作中 |
| published | 公開・配布済み |
| measuring | KPI・顧客反応を計測中 |
| improving | 改善・再編集中 |
| archived | 現時点で休止・対象外 |

---

## 運用原則

1. 記事や動画を先に作らず、必ずProblemを先に登録する。
2. HPSは優先順位を補助するものであり、最終判断は投資審査で行う。
3. 再現性と拡散性を重点評価する。
4. ResearchとLabで確認できない性能や効果は断定しない。
5. 1つのProblemから複数のAssetを生成する。
6. 公開後の反応をProblemへ戻し、再採点・改善する。
7. テンプレートは運用結果に基づいてバージョン更新する。

---

## HOVELにおけるAssetの定義

Assetとは、Problemを解決する過程で生成され、再利用・改善・収益化できる知的または実務的資産を指す。

例：

- 記事
- YouTube動画
- ショート動画
- AIプロンプト
- GitHubドキュメント
- チェックシート
- Googleフォーム
- 実験データ
- 商品比較表
- メールテンプレート
- 調査ノート
- 意思決定ログ

---

## 次の実装候補

- Problemごとの個別ファイル命名規則
- Asset IDとProblem IDの関連付け
- HOVEL Lab実験テンプレート
- KPI記録フォーマット
- Problem一覧インデックス
- GitHub Issuesとの連携

---

Version: v0.1
Status: Beta
