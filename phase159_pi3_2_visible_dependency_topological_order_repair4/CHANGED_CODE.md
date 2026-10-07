# Phase 159 pi3_2 visible dependency topological ordering repair4

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - 変更関数:
    `order_toda_group_proof_narrative_visible_step_dependencies()`
- `tests/test_phase159_pi3_2_visible_dependency_topological_order.py`
  - テストファイル全文を更新
- `audit_phase159_pi3_2_stable_dependency_order.py`
  - 新規監査スクリプト

## import

production code の import 変更はありません。

## 修正内容

repair2 / repair3 で追加した newly-ready consumer 優先を撤回し、
repair1 型の stable topological order に戻す。

- `presentation.edges` の direct dependency edge のみ利用
- premise と consumer が同じ Argument local body を共有する場合のみ採用
- ready node が複数なら元 paragraph index を tie-break に使用
- cycle / ambiguous mapping は既存 markdown を維持
- edge のない statement 間の意味的優先順位は推測しない

## 変更関数全文

`apply_phase159_pi3_2_visible_dependency_topological_order_repair4.py`
内の `NEW_FUNCTION` が置換後の関数全文。

コード内の `...` による省略はありません。

## テスト

`tests/test_phase159_pi3_2_visible_dependency_topological_order.py`
を全文置換。

確認する依存順:

- `pi_2^1 = 0 < H 単射`
- `E 同型 < E 単射 < Delta=0 < H 全射`
- `H 単射 < H 同型`
- `H 全射 < H 同型`
- `pi_3^3 < eta_2 definition`
- `H 同型 < eta_2 definition < final result`
- `Delta=0` に「完全性より」
- direct edge のない `pi_3^3` と `E 同型` は元順序を保持

proof body 抽出は `partition("## 証明")` を使用。

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

- stable dependency-order audit が全 PASS
- focused pytest が全 PASS
- public pi_3^2 Narrative が repair1 の安全な順序へ戻る
- eta_2 definition / final result が H isomorphism より前へ移動しない
- Delta=0 が H surjective より前
- QED が最後

## 次 Phase との境界

`pi_2^1=0` の直後に `H 単射` を必ず置く branch-continuity は
post-render visible-step ordering では実装しない。

再検討する場合は upstream の
`order_toda_group_proof_narrative_arguments()` または Argument renderer
を監査する。

proof graph の edge 追加、statement type 固定順位、
multi-Argument renderer の再設計は今回行わない。
