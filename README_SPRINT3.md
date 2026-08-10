# HOVEL Sprint 3 — Knowledge & Intelligence Layer

Sprint 2へ次の機能を追加します。

- Knowledge Base全文検索
- 既存記事インデックス
- 類似記事・カニバリゼーション候補
- 内部リンク候補
- バージョン管理可能なPrompt Engine
- Workflow Engine統合
- unittestとスモークテスト

## 導入

```bash
python3 install_sprint3.py /path/to/hovel_web_market
cd /path/to/hovel_web_market
python3 scripts/validate_sprint3.py
```

## 実行

```bash
python3 run.py --topic "仕事中に眠すぎる"
```

`tasks/<task-id>/intelligence.json` が追加されます。

## 設計上の制約

- 外部AI APIはまだ呼び出しません
- Web検索はまだ行いません
- 類似度は軽量な語彙集合ベースです
- 自動公開は禁止です
- 最終状態は `human-review` です

これらはSprint 4で外部AI・検索・CIへ接続する前提の安全なローカル基盤です。
