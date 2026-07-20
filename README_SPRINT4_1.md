# HOVEL Sprint 4.1 — OpenAI API Integration

既存Workflow Engineへ、任意でOpenAI Responses APIを接続します。

## 安全設計

- 既定値ではAI接続は無効です
- APIキーは環境変数からのみ読み込みます
- API障害時は既存の決定論的出力へフォールバックできます
- 自動公開は行いません
- 最終状態は引き続き `human-review` です
- 未確認の価格、研究、引用、商品体験を捏造しない指示を共通適用します

## セットアップ

```bash
python3 -m pip install -r requirements-ai.txt
export OPENAI_API_KEY="YOUR_KEY"
export HOVEL_AI_ENABLED=true
export OPENAI_MODEL=gpt-5
```

API失敗時にも処理を継続する既定設定:

```bash
export HOVEL_AI_FALLBACK_ENABLED=true
```

API失敗時にWorkflowを停止する厳格設定:

```bash
export HOVEL_AI_FALLBACK_ENABLED=false
```

## 実行

```bash
python3 run.py --topic "仕事中に眠すぎる"
```

各ステージの実行ログには次が記録されます。

- `provider`: `openai` / `deterministic` / `deterministic-fallback`
- `model`
- `response_id`
- `ai_error`

## テスト

APIキーを使わずにテストできます。

```bash
python3 -m unittest discover -s tests
python3 scripts/validate_sprint2.py
```

## 既知の制約

- Sprint 4.1ではWeb検索を実行しません
- AI出力に引用元を自動付与しません
- API利用料金の集計は未実装です
- 構造化JSON出力は後続Sprintで追加します
