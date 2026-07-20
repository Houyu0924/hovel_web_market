# HOVEL 無料版AIマーケティング部

OpenAI APIや有料検索APIを使わず、ChatGPT Plus、GitHub、Python標準ライブラリ、GitHub Actionsで記事制作を管理します。

## 費用方針

- OpenAI API: 使用しない
- 外部の従量課金API: 使用しない
- GitHub Actions: 無料枠内で利用
- 自動公開: 行わない
- 最終公開判断: 運営者が行う

## 運用フロー

### 1. 記事案件を作る

```bash
python3 scripts/create_review_packet.py \
  --topic "会社員向け耳栓おすすめ比較" \
  --type comparison \
  --keyword "耳栓 おすすめ 会社員"
```

`jobs/YYYY-MM-DD-記事名/` に次のファイルが作られます。

- `brief.md`: ChatGPTへ渡す制作指示と人間用チェックリスト
- `job.json`: 案件メタデータ

### 2. ChatGPTで記事を制作する

ChatGPTに以下を指示します。

> GitHubの最新記事案件を開き、brief.mdとprompts、config、既存記事を確認して、市場調査から編集長審査まで実行してください。成果物を同じ案件フォルダへ保存し、記事原稿をcontent/draftsへ追加してPull Requestを作成してください。

ChatGPT Plusの契約範囲で作業するため、API従量課金は発生しません。

### 3. 自動品質検査

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_sprint2.py
python3 scripts/quality_gate.py --repo-root .
```

Pull Requestを作るとGitHub Actionsでも同じ検査が実行されます。

品質ゲートは次を検査します。

- front matterの必須項目
- 見出し構造
- 極端に短い本文
- 「必ず」「絶対」などの保証表現
- 医療的な治癒表現
- 未使用商品の体験談を疑う表現
- TODOや仮リンク
- 広告表記
- URLがある記事の出典セクション

機械検査を通過しても、事実の正しさや引用元の内容は人間が確認します。

## 運営者が担当する作業

1. 引用元を開いて確認する
2. 商品価格、仕様、リンクを確認する
3. 自分の体験が必要な箇所だけ追記する
4. note上の表示を確認する
5. Pull Requestを承認して公開する

## 制約

この仕組みだけでは、ChatGPTを無人で定時起動したり、Web調査を完全自動化したり、noteへ自動投稿したりはできません。それらには外部API、ブラウザ自動化、または別の実行基盤が必要です。

無料版では、ChatGPTとの会話を制作エンジン、GitHubを案件管理と監査ログ、GitHub Actionsを機械検査として使います。
