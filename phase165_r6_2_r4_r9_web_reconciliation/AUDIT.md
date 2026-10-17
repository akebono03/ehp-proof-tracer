# R4-R9 監査

対象は $\pi_4^3$。命題台帳に基づく目標選択、利用順序付き探索、利用順序なし共通探索、PartialProofResult、NarrativeModel、公開 Web 入口を分けて観測します。

## 変更対象

新規 `audit.py` の `capture_result`, `safe_stage`, `run`, `render_md`, `main` とテスト、新規 `run.ps1`。本番ファイル・既存クラス・関数は変更しません。

## 完了条件

各経路の成功・失敗、ProofStep の件数、未解決 Goal、診断が JSON と Markdown に保存されること。公開証明完成の判定は観測結果に従います。

## 次段階との境界

今回の監査結果が明らかにした接続差だけを次段階で修復し、旧群別 Adapter は復活させません。全体 pytest は Phase 165 最終時にのみ実施します。
