# HOVEL Data Collector v0.1

## 目的

note・X・Amazonアソシエイト・Search Consoleの週次データを、APIを使わず5分程度でGitHubへ取り込む。

## 方針

現段階では完全自動化しない。各管理画面を人間が確認し、必要な数値だけを1つの入力ファイルへ記録する。変換スクリプトが各CSVと週次入力サマリーを生成する。

## 毎週の流れ

1. `data-collector/inbox/weekly-input.csv` を開く
2. note・X・Amazon・Search Consoleの管理画面から数値を入力
3. ローカルまたはGitHub Codespacesで次を実行

```bash
python scripts/process_weekly_metrics.py
```

4. 生成されたCSVを確認
5. GitHubへコミット
6. Analyst Agentが週次レビューを作成

## 入力対象

### note
- 週次PV
- スキ
- コメント
- 公開記事数

### X
- フォロワー
- インプレッション
- いいね
- リポスト
- 返信
- プロフィールアクセス
- URLクリック

### Amazonアソシエイト
- クリック
- 注文数
- 紹介料

### Search Console
- クリック
- 表示回数
- CTR
- 平均掲載順位

## 保存先

- `data/note/weekly_metrics.csv`
- `data/x/account_metrics.csv`
- `data/amazon/associate_metrics.csv`
- `data/search-console/weekly_metrics.csv`
- `data/weekly/raw/`

## 完了条件

- 必須指標に空欄がない
- 数値形式が正しい
- 前週と同じ週番号を重複登録しない
- 変換スクリプトがエラーなく終了する

## コスト

- GitHub: 0円
- Python: 0円
- API: 不使用
- 想定作業時間: 初回15分、定常5〜10分
