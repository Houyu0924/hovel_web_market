# HOVEL X半自動投稿フロー

## 目的
GitHub上の記事Markdownを起点に、X投稿案の生成・レビュー・承認・予約投稿を半自動化する。

## ディレクトリ

```text
social/x/
├── README.md
├── prompts/
│   └── generate-x-posts.md
├── schema/
│   └── x-post.schema.json
├── drafts/
├── approved/
└── published/
```

## 運用フロー
1. 記事Markdownを選ぶ
2. `prompts/generate-x-posts.md` を使い5投稿を生成
3. `drafts/` にJSONで保存
4. 人手で確認し、`status` を `approved` に変更
5. `approved/` に移動
6. Make / n8n / GitHub Actionsから予約投稿
7. 投稿後は `published/` に移動

## 投稿タイプ
- announcement: 記事公開告知
- conclusion: 記事の結論
- evidence: 根拠・データ
- action: 今日からできる行動
- repost: 数日後の再投稿

## レビュー基準
- 原則140文字以内
- 誇張・煽り・根拠のない断定をしない
- 記事内容と矛盾しない
- URL付き投稿は1記事につき1〜2本
- 1投稿1メッセージ
- 読者が実行できる具体性を入れる
- 医療・健康情報は診断表現を避ける

## 状態管理
- draft
- approved
- scheduled
- published
- rejected

## 次工程
1. テスト記事1本から5投稿を生成
2. `drafts/` に保存
3. X APIまたは予約投稿ツールの接続方法を決定
4. GitHub Secretsに認証情報を登録
