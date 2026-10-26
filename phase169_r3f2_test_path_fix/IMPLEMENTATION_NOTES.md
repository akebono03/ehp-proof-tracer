# Phase 169 R3F2 — テストファイル指定の訂正

## 原因

R3F1 の ZIP には `tests/test_phase169_r3f_ehp_terminal_subgoals.py` が存在した。一方 `run.ps1` は存在しない `tests/test_phase169_r3f1_committed_ehp_baseline_fix.py` を指定したため、pytest が収集前に終了した。自動復元により本番2ファイルは元の状態へ戻った。

## 今回の変更対象

1. `run.ps1`：存在するテストファイルを参照。パッケージ内5ファイルと関連テスト4ファイルを、適用より前に `Test-Path` で検査。監査モジュール名と表示ラベルを R3F2 に更新。
2. `apply.py`：表示するフェーズ名だけを R3F2 に変更。ガード条件、Git blob 検証、変更箇所、復元処理は R3F1 と同一。
3. `README.md` と本書：修正内容に合わせて更新。
4. 本番に適用する `shared_expansion_provider()` と新規 `expand_registered_ehp_terminal_goal()` は R3F1 とバイト単位で同一。
5. 新規テスト8件のコード全文 `tests/test_phase169_r3f_ehp_terminal_subgoals.py` と `audit.py` も R3F1 と同一。

## 本番の変更箇所とコード全文

- `phase165_r52_r9_shared_math.py` — `shared_expansion_provider()` 全文：`full_functions/shared_expansion_provider.py`。
- `phase165_r14_r5_ehp_connection.py` — `audit_ehp_connection()` の直前へ新規 `expand_registered_ehp_terminal_goal()`：`full_functions/expand_registered_ehp_terminal_goal.py`。
- import 節の追加・変更なし。変更後のモジュール全文は `output/` に出力。
- 既存テストは変更しない。対象の限定 pytest は `run.ps1` に全文指定。

## 完了条件と次段階の境界

- 限定 pytest 成功、実探索監査成功、終端2 Goal にそれぞれ1件の候補を生成。
- `INFERENCE` の要件を保持し、`GIVEN` を捏造せず、$\pi_5^3$ は `partial` のまま。
- R3G で $H(\nu\prime)=\eta_5$ と Proposition 5.1 複合命題の証明可能性を調べる。
- Phase 169 完了まで全体 pytest は実行しない。
