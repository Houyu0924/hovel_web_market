# HOVEL Sprint 2 Complete

外部ライブラリ不要、Python 3.9対応のWorkflow Engineです。

## 導入
```bash
python3 install_sprint2.py /path/to/hovel_web_market
cd /path/to/hovel_web_market
python3 scripts/validate_sprint2.py
```

## 実行
```bash
python3 run.py --topic "会社員向け耳栓比較"
```

## 再開
```bash
python3 run.py --resume "<task-id>"
```

このMVPはWeb検索、商品価格取得、論文検索、外部AI API呼び出しを行いません。最終状態は必ず `human-review` です。
