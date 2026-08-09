# HOVEL Top5 レバレッジ型WEBマーケ事業分析 v1

Date: 2026-08-09
Status: Strategy draft for 20 -> 5 -> 1 selection

## Purpose
利益1,000万円を狙うにあたり、Top20から残した5案を「なぜ有望か」だけでなく、**なぜ他社・他人がやらないのか / やっても勝てないのか**まで含めて評価する。

評価軸:
1. レバレッジ: 顧客増加に人時が比例しないか
2. Recurring: 月額/年額化しやすいか
3. Data moat: 利用とともにデータ資産が蓄積するか
4. 30日課金可能性: 9月から有料検証できるか
5. 初期資金: 少額でMVPを出せるか
6. 競争優位形成: 日本市場やVertical特化で守りを作れるか
7. Distribution: 顧客獲得チャネルを現実的に持てるか

---

# 結論

現時点の順位:

1. **企業Trigger Intelligence / Trigger-to-Action SaaS**
2. **競合変化→意思決定 Competitive Action Intelligence**
3. **AI検索ブランド露出・Citation Intelligence**
4. **営業会話→マーケ改善 Voice-of-Customer Intelligence**
5. **Win/Loss Intelligence**

ただし、単純な「Trigger API」「Web変更通知」「AI検索順位計測」は既に競合が強い。

HOVELが狙うべき共通方向は:

> **Signalを集めるだけでなく、Signal → 意味 → 優先順位 → 次のActionまでを日本の中小B2B向けに自動化する。**

データ収集単体はCommodityになりやすい。意思決定ワークフローまで持つことでRetentionとARPUを作る。

---

# 1. 企業Trigger Intelligence / Trigger-to-Action SaaS

## Customer Problem
B2B営業・マーケ担当者は、以下の「今売りやすい瞬間」を日々見落としている。

- 新サービス開始
- 法人プラン開始
- 価格変更
- 資金調達
- 採用急増
- 新拠点
- 経営者交代
- LP/メッセージ変更
- 新しい業務課題を示すPR

既存リストを一律に営業するより、Triggerがある企業へ接触する方が文脈を作りやすい。

## Existing proof overseas
Common RoomはWeb訪問、求人、GitHub、役職変更、プロダクト利用など多数のBuying Signalを統合し、誰に・いつ・なぜ接触するかに利用している。
TrigifyもSocial SignalやListeningを月額課金している。

Sources:
- https://www.commonroom.io/product/signals/
- https://www.commonroom.io/solutions/abm/
- https://www.trigify.io/pricing

## Why others do not do it
### 1. Trigger収集自体は簡単だが、False Positive除去が難しい
PRが出た = 購買意欲ではない。
「新サービス開始」の中でも、外部マーケ支援ニーズがある企業とない企業を判別する必要がある。

### 2. 日本語の公開情報が分散している
PR TIMES、企業ニュース、求人、IR、サービスLP、採用ページ、SNSなどデータ形式が統一されていない。

### 3. Signalだけ渡しても営業は動かない
「○○社が採用開始」という通知だけでは弱い。
必要なのは:
- なぜ今狙うか
- どのProblem仮説か
- 誰に連絡するか
- 何と言うか
まで。

### 4. スクレイピング/データ運用が地味で重い
URL変更、Bot対策、重複、誤検知、レート制限、DOM変更への保守が必要。
アイデアより運用力が参入障壁になる。

### 5. 海外大手はEnterprise寄り
Common Room等は高機能だが、日本の小規模B2BチームにはToo Muchになりやすい。

## HOVEL angle
**Trigger DetectionではなくTrigger-to-Action。**

Output例:
- Trigger: 法人向けプラン開始
- Why now: 新しいICPを探索している可能性
- Problem hypothesis: Message / ICP
- Recommended buyer: 代表 / 事業責任者 / マーケ責任者
- Outreach angle: 「法人向け開始後、どの顧客像が最も反応しているか…」
- Priority score: 87/100

## 7-day MVP
- 対象Verticalを1つに限定: B2B SaaS or 法人研修
- 100社登録
- PR TIMES + 公式ニュース + 料金/LP更新を毎日チェック
- AIでTrigger分類
- 重要Trigger 10件/日をGoogle Sheet/メールで出力
- 各TriggerにProblem仮説とOutreach hookを生成

**ソフトウェアを先に作らず、内部自動化 + 配信で検証する。**

## 30-day paid test
商品:
「営業Triggerリスト 毎週20社 + 接触理由付き」

仮価格:
- Beta: ¥9,800/月
- Standard hypothesis: ¥29,800〜¥49,800/月

KPI:
- Alert useful rate > 40%
- Trigger企業への返信率 vs 非Trigger企業
- Weekly active usage
- 2ヶ月目継続意向

## Moat path
1. 日本企業Trigger履歴DB
2. Trigger → 返信/商談/受注のOutcome data
3. 業界別「どのTriggerが何を売る時に効くか」モデル
4. CRM連携
5. API / Partner distribution

## Risk
SignalデータだけではClay/Common Room/既存営業DBに吸収される。
**Action qualityと日本Vertical特化がないなら不採用。**

---

# 2. Competitive Action Intelligence

## Customer Problem
競合の価格・商品・Positioning変更には重要情報があるが、人は定期確認しない。

Visualpingは既にページ変更監視を大規模に提供し、競合のpricing/product/homepage等を代表用途としている。

Sources:
- https://visualping.io/competitive-monitoring
- https://visualping.io/blog/monitor-competitor-websites

## Why others do not do it
### 1. DetectionはCommodity
Web差分監視はVisualping、Distill等で簡単にできる。
単なる「変わりました」通知に高い価格は付かない。

### 2. Noise問題
Cookie文言、日付、ブログ、footer等、意味のない変更が大量に出る。

### 3. 意味の解釈が会社ごとに違う
競合が価格を10%下げたとしても、自社が追随すべきかはポジショニング・顧客層で変わる。

### 4. ROI測定が難しい
競合変更を早く知ったことが売上にどれだけ寄与したか追跡しにくい。

## HOVEL angle
**Change DetectionではなくAction Intelligence。**

例:
Competitor pricing changed
→ 旧価格/新価格比較
→ 意図推定
→ 自社顧客へのリスク
→ Sales battlecard変更案
→ LP/価格/営業トークの具体的Next Action

## 7-day MVP
B2B SaaS 20社の:
- pricing
- homepage
- product
- case study
を監視。

変更時に「何が変わった / なぜ重要 / 何をすべき」を生成。

## 30-day paid test
5競合 monitoring: ¥9,800〜¥19,800/月
10〜20競合 + weekly decision digest: ¥49,800/月 仮説

## Moat path
- 競合変更履歴DB
- 業界別価格/positioning時系列
- 過去変更後の市場反応とのリンク

## Risk
Visualping自身がAI分析・Battlecard自動化まで拡張している。
Generic horizontalでは勝ちにくい。
**日本の特定Verticalの価格/Positioning databaseまで作れないなら不採用。**

---

# 3. AI Search Brand / Citation Intelligence

## Customer Problem
ChatGPT、Gemini、Perplexity等で商品探索が起きるようになり、ブランド側は:
- 自社が推薦されるか
- 競合より何位か
- 何を根拠に回答されるか
- 誤情報がないか
を把握したい。

Peec AI等がAI Search visibilityを日次で追跡している。

Source:
- https://peec.ai/pricing

## Why others do not do it
### 1. 市場は既に急速に混雑
参入障壁が低く、LLMにPromptを投げて記録するだけのMVPはコピーされやすい。

### 2. Measurementが不安定
回答はモデル、時刻、アカウント、地域、Prompt wordingで変化する。
「順位」をGoogle SEOのように扱うと誤解を生む。

### 3. Actionabilityが弱くなりやすい
「露出が低い」は分かっても何を変えれば改善するか因果が不明。

### 4. Platform dependency
OpenAI/Google/Perplexity側の仕様変更、API価格、検索統合変更に大きく依存。

### 5. 顧客教育が必要
まだAI検索由来のCVや売上を正確に計測できない企業も多い。

## HOVEL angle
Generic rank trackerではなく、**Japanese B2B AI Buyer Journey Intelligence**。

例:
「法人AI研修 おすすめ」だけではなく、購買担当者の100質問を固定し:
- Mention share
- Citation sources
- Competitor appearance
- Missing evidence
- Recommended content/PR actions
を返す。

## 7-day MVP
1 Vertical × 20 brands × 100 purchase prompts。
ChatGPT/Gemini/Perplexity等でBrand/Citation matrixを作る。

## 30-day paid test
AI visibility audit ¥30,000 one-off → monitoring ¥9,800〜¥29,800/月。

## Moat path
- 日本語B2B purchase prompt library
- Citation source DB
- Prompt → conversion proxy data
- Vertical benchmark

## Risk
競争スピードが非常に速い。
**単独本命より、他のデータ商品に組み込むFeature候補。**

---

# 4. Sales Conversation → Marketing Intelligence

## Customer Problem
営業通話には:
- 顧客の言葉
- objection
- price resistance
- alternatives
- value proposition反応
が大量に含まれるが、マーケチームはほとんど活用できていない。

Gongは会話データをVoice of Customerとして活用しており、Octave等はGong transcriptからpain point / objection / value propositionを自動抽出している。

Sources:
- https://www.gong.io/
- https://collective.gong.io/integrations/octave

## Why others do not do it
### 1. データアクセスが最大障壁
顧客の商談録音・transcriptを取得するにはCRM/Gong/Zoom/Meet等とのintegrationが必要。

### 2. Privacy / security
企業の機密情報・個人情報・顧客情報を扱うため、セキュリティ審査が重い。

### 3. Garbage in, garbage out
録音品質、営業担当の話し方、metadata不足で分析品質が大きく変わる。

### 4. Gong等のIncumbentが強い
Conversation Intelligence自体では既存大手と正面衝突する。

### 5. InsightをMarketing actionに変換する設計が難しい
単なる要約では価値が弱い。

## HOVEL angle
録音システムを作らない。
**既存Transcriptを受け取り、マーケ改善だけに特化するLayer。**

Output:
- customer wording
- objections
- segment差
- lost language
- recommended LP copy
- FAQ
- proof needed
- offer/package ideas

## 7-day MVP
顧客がexportした10〜30 transcriptsをアップロード。
No integrationで開始。

## 30-day paid test
Monthly 50 calls analysis: ¥30,000〜¥100,000/month hypothesis.

## Moat path
- Conversation → marketing action taxonomy
- Industry vocabulary
- Before/after LP outcome data

## Risk
初期導入のSecurity frictionが大きく、中小企業では録音データ自体が存在しない場合もある。

---

# 5. Win/Loss Intelligence

## Customer Problem
営業は失注理由をCRMに書くが、買い手本人の理由と一致しないことが多い。
ClozdはWin/Loss interview + AI + ongoing platformを組み合わせている。

Clozdは継続型Win/Loss programの方がProject型よりROI評価が高いと訴求している。

Sources:
- https://www.clozd.com/about-us
- https://www.clozd.com/solutions/win-loss-analysis-software
- https://www.clozd.com/state-of-win-loss

## Why others do not do it
### 1. Buyer interview recruitingが難しい
失注した相手は返信するインセンティブが低い。

### 2. 人間のTrustが必要
AIフォームだけでは本音が取れないケースがある。

### 3. Sample size問題
小規模B2Bでは月間失注数が少なく、統計的傾向が出るまで時間がかかる。

### 4. 単発コンサル化しやすい
インタビューを人間が実施すると人的稼働モデルへ戻る。

### 5. ROIまで時間がかかる
Insight→営業改善→新商談→受注という時間差がある。

## HOVEL angle
High-touch interview companyではなく:
- Closed Won/Lost data
- sales notes
- email
- optionally AI interview
から自動でDecision driversを継続抽出。

## 7-day MVP
CSV/CRM exportをUploadし、20〜100 dealsを分析。
本人Interviewなしでも何が取れるか検証。

## 30-day paid test
Monthly Win/Loss dashboard ¥30,000〜¥100,000。

## Moat path
- Lost reason ontology
- industry benchmarks
- seller reason vs buyer reason gap data

## Risk
本当のBuyer voiceを取らないと差別化が弱く、取ると人的コストが増える。
本命より将来的Feature候補。

---

# Why "nobody is doing it" is usually the wrong question

実際には、良い市場にはほぼ必ず誰かいる。

狙うべき問いは:

> **「なぜ既存企業が日本のこの顧客層、このWorkflow、この価格帯を十分に取れていないのか？」**

競合がいない理由は多くの場合OpportunityではなくWarningになる。

代表的Warning:
1. 顧客が痛みを感じていない
2. Budget ownerがいない
3. Data accessが取れない
4. ROIが証明できない
5. Churnが高い
6. Sales costがLTVを超える
7. API / platform dependencyが強すぎる
8. Human operationsをなくせない

よって「競合ゼロ」は加点しない。
**海外で有料需要が証明済み、しかし日本SMBに未最適化**を狙う。

---

# Comparative Score (仮説 / 5点満点)

| Business | Leverage | 30-day validation | Data moat | Recurring | Distribution | Defensibility | Total /30 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Trigger-to-Action | 5 | 5 | 5 | 5 | 4 | 4 | **28** |
| Competitive Action Intel | 5 | 5 | 4 | 5 | 4 | 3 | **26** |
| AI Search Intelligence | 5 | 5 | 3 | 5 | 4 | 2 | **24** |
| Conversation→Marketing | 5 | 3 | 5 | 5 | 3 | 4 | **25** |
| Win/Loss Intelligence | 4 | 3 | 5 | 5 | 3 | 4 | **24** |

Scoreは仮説。Paid validationで更新する。

---

# Recommended Direction

## First hypothesis to test
**Japanese B2B Trigger-to-Action Intelligence**

Do not build "another sales list".
Do not build generic "company news API".

Value proposition:

> **「今営業すべき会社と、その理由と、刺さる切り口が毎週届く。」**

Initial niche:
- B2B SaaS vendors / marketing agencies / sales agencies selling ¥100k+/month products
- Their target accounts: Japanese SMB / growth companies

### Why this first
1. Public dataだけでMVP可能 → 顧客データintegration不要
2. 自社でもDogfood可能
3. HOVELの既存Trigger research資産を再利用可能
4. 月額化しやすい
5. 企業数が増えても配信コストは比例しにくい
6. Outcome dataが蓄積すればMoatになる
7. API、CRM integration、White-labelへ拡張できる

---

# Kill criteria

30日テストで以下なら停止:
- 20人ヒアリングして「現在の営業リストで十分」が70%以上
- Trigger付きLeadでも返信率差が出ない
- Useful alert rate < 25%
- 月¥10,000すら払う意思がほぼない
- 1顧客あたりの手動調査が週60分以上必要

続行条件:
- 3社以上が有料Beta
- 2社以上が翌月継続意向
- Trigger outreach返信率が通常リストの2倍以上
- 重要Triggerの70%以上を自動処理可能

---

# August decision

8月中は開発を本格化しない。

1. 1 Verticalを決める
2. 100社のTriggerを1週間収集
3. AIでTrigger→Actionを生成
4. 10人のB2B営業/経営者に見せる
5. 「どのAlertなら毎月払うか」を確認
6. Landing Page + paid beta pre-orderを出す

**Paid signalが出るまでSaaS本開発しない。**

# Source notes
- Common Room signals: https://www.commonroom.io/product/signals/
- Common Room ABM: https://www.commonroom.io/solutions/abm/
- Trigify pricing: https://www.trigify.io/pricing
- Visualping competitor monitoring: https://visualping.io/competitive-monitoring
- Visualping competitor monitoring guide: https://visualping.io/blog/monitor-competitor-websites
- Peec AI pricing: https://peec.ai/pricing
- Gong: https://www.gong.io/
- Gong/Octave: https://collective.gong.io/integrations/octave
- Clozd about: https://www.clozd.com/about-us
- Clozd platform: https://www.clozd.com/solutions/win-loss-analysis-software
- Clozd state of win-loss: https://www.clozd.com/state-of-win-loss
