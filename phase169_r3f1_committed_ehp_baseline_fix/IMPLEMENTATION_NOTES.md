# Phase 169 R3F1 — 既存コミットへの基準修正

## 原因と検証済みの GitHub 状態

- 直前の R3F は最初の適用ガードで `R3F_APPLY_EXIT_CODE=6` となり、本番コードは変更していない。
- 誤った旧基準：`phase165_r52_r9_shared_math.py` の `36a4c355758ee55ba4d39606a8e0f281bb43efff`。
- 現行の HEAD `2e0b466ee6a91f891ca6b101794b1bd6bca0b970` における正しい Git blob：`ff78d5e2a64cc74e77ef22c2e562485af15c204f`。
- `phase165_r14_r5_ehp_connection.py` は Git blob `e76a0a772a709aff94b31583c4e80291b2537f36` のまま。
- 今回は Git のコミット済み R3E1 を元に、R3F の**同一**変更を実施する。古い未適用版を再適用せず、外部の旧 ZIP への依存は持たせない。

## 変更対象と全コードの所在

1. `phase165_r14_r5_ehp_connection.py`：既存の `audit_ehp_connection()` の直前に新規 `expand_registered_ehp_terminal_goal()` を追加。局所 import は関数全文に含む。モジュール import 節は変更なし。
2. `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` を関数全体で置換。既存 API、既存 import 節は変更なし。R3E1 の `expand_registered_ehp_goal` は必ず維持する。
3. 新規 `tests/test_phase169_r3f_ehp_terminal_subgoals.py`：既存 R3F の8テストをそのまま収録し、関連する既存テストだけ実行。
4. `apply.py` と `run.ps1`：コミット済み版の検証と限定テスト・監査・復元を実施する。

本番ファイルの置換後の全文は `output/phase165_r52_r9_shared_math.py.full.py` と `output/phase165_r14_r5_ehp_connection.py.full.py` に出力される。新規・変更関数の全文は ZIP の `full_functions/` に収録する。

## 数学上の未完了範囲

- `TodaDeltaInjectiveStatement` の証明には Proposition 5.1 の複合命題が `INFERENCE` として証明される必要がある。
- `TodaHopfInvariantSurjectiveStatement` はさらに $H(\nu')=\eta_5$ を `INFERENCE` として必要とする。
- この R3F1 は候補を出すだけで、ProofStep、GIVEN、引用の許可を捏造しない。
- $\pi_5^3$ は推論が完了するまで `partial` のまま。次工程 R3G に終端の証明可能性の確認を残す。

## pytest と完了条件

`run.ps1` は新規8テストと既存の EHP・推論・文献終端テストのみ実施する。実文献順で screen 済みのコンテキストを監査し、終端2件に各1個の候補ができたこと、INFERENCE 前提が変更されないこと、$\pi_4^2$ が `complete`、$\pi_5^3$ が未完成であることを条件にする。全体 pytest は Phase 169 終了時だけ実施する。
