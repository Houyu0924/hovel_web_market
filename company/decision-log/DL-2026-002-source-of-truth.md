# DL-2026-002: 情報を一元管理する

- **Date:** 2026-07-20
- **Owner:** HOVEL CEO
- **Status:** Adopted

## Background
AIごとに情報が分散すると、重複調査、判断の不一致、更新漏れが発生する。

## Decision
GitHubをルール、SOP、プロンプト、テンプレート、記事の正本とする。頻繁に更新する数値データは将来的にGoogle Sheetsまたはデータベースへ移行できるが、スキーマと参照先はGitHubで管理する。

## Reason
変更履歴、レビュー、ロールバック、AIと人間の共同作業を一元化できるため。

## Impact
AIは既存のKnowledge Baseを先に参照し、不足情報のみ追加調査する。
