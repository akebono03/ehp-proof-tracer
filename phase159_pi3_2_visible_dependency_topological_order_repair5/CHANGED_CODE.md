# Phase 159 pi3_2 visible dependency topological ordering repair5

## 変更対象

1. `toda_group_proof_narrative_contribution_renderer.py`
   - `order_toda_group_proof_narrative_visible_step_dependencies()`
   - repair2 適用直前 backup、すなわち repair1 成功状態から関数全体を復元する。

2. `tests/test_phase159_pi3_2_visible_dependency_topological_order.py`
   - ファイル全文を置換する。
   - repair2 / repair3 の branch-continuity expectation は削除する。

3. `run_phase159_pi3_2_visible_dependency_topological_order_repair5.ps1`
   - Python / pytest が non-zero exit の場合、その場で終了する。

## import

production code の import 変更はありません。

## 復元する関数

復元元:

`phase159_pi3_2_visible_dependency_topological_order_repair2_backup/toda_group_proof_narrative_contribution_renderer.py`

この backup は repair2 適用直前に作成されており、repair1 が 12 passed した時点の production code を保持している。

apply script は top-level function の開始位置を

`def order_toda_group_proof_narrative_visible_step_dependencies(`

で検出し、次の top-level `def` までを関数全体として復元する。

repair4 のような固定された後続関数名による境界検出は使用しない。

## テスト契約

確認する依存順:

- `$pi_2^1=0$` より後に `H` 単射
- `E` 同型 -> `E` 単射 -> `Delta=0` -> `H` 全射
- `H` 単射 -> `H` 同型
- `H` 全射 -> `H` 同型
- `$pi_3^3$` -> `eta_2` 定義
- `H` 同型 -> `eta_2` 定義 -> 最終結果
- `Delta=0` に「完全性より」が付く

要求しないもの:

- `$pi_2^1=0$` の直後に `H` 単射を置くこと
- edge のない root statement 間に新しい意味的順位を付けること

## 実行する pytest

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

全体テストは実行しない。

## 完了条件

- apply が成功する。
- stable dependency-order audit が全 PASS。
- focused pytest が全 PASS。
- `Delta=0` が `H` 全射より前。
- `H` 同型が `eta_2` 定義より前。
- `eta_2` 定義が最終結果より前。
- `□` が最後。

## 次 Phase との境界

branch-continuity は今回実装しない。

再検討時は post-render paragraph reorder ではなく、
`order_toda_group_proof_narrative_arguments()` と
Argument renderer の upstream ordering を先に監査する。

proof graph の edge 追加、statement type 固定順位、
multi-Argument renderer の再設計は行わない。
