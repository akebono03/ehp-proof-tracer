# Phase 174 R3-R7-R47 監査計画

## 監査対象と出典

- GitHub `akebono03/ehp-proof-tracer`、`develop`、監査時 HEAD `fe4f07940cdb5557397dc9e610b65b7eeaff0116`。
- R44 の `$E\pi_{10}^{5}=0$` の零像証明と、R46 の Toda Proposition 4.2 による EHP 完全性特殊化を連結する。
- DB prior `$\pi_{10}^{5}$` の巡回表示は **独立した文献の定理ではない**。出典付き Toda (5.9) から生成元の像が零と導く。
- `TodaProp42GeneralExactnessStatement` は出典付き `GIVEN`、各具体的な完全性は `INFERENCE`。
- 調査する標準探索の経路：根の群零 Goal → 上側 Δ 全射 → Hopf 単射 → `ImageZeroStatement` → Hopf 側の E-H 完全性 → 下側 `im H = ker Δ`。
- 下側の `KernelMultipleStatement` は意図的に未接続とし、次の監査対象として明示する。

## 変更一覧

- 新規 `phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/source_guard.py`：`verify_checkout()`。
- 新規 `phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/audit.py`：`inspect_integrated_hopf_frontier()`、`main()`。
- 新規 `phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/run.ps1`。
- 新規 `phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_guard.py`、`test_frontier.py`、`test_static.py`。
- 既存のクラス、関数、import、数学的推論規則、探索エンジンは一切変更しない。

## 完了条件

1. Source Guard と DryRun が PASS。
2. 同一の `search_registered_partial_proof()` 内で零像・Hopf 単射・下側の像＝核の各 ProofStep を観測し、出典祖先を検査。
3. 下側の核の整数倍表示が未解決であることを、その型付き Goal のまま記録。
4. 限定 pytest が PASS。全体 pytest は Phase 終了時のみ。
5. `$\pi_{12}^{7}=0$` の完成や Web HTTP 検証を宣言しない。

## 次工程との境界

R47 は既存の候補を接続して観察する段階。R48 以降では、未解決の `KernelMultipleStatement` と Prop. 2.7 の特殊化を、出典に依存する一般規則だけで検証する。専用 Narrative や新しい結論 `GIVEN` は追加しない。
