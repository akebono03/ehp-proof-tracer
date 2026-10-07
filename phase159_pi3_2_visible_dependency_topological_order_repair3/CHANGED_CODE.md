# Phase 159 pi3_2 visible dependency topological ordering repair3

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - 変更関数:
    `order_toda_group_proof_narrative_visible_step_dependencies()`
- `tests/test_phase159_pi3_2_visible_dependency_topological_order.py`
  - テストファイル全文を更新
- `audit_phase159_pi3_2_argument_local_order.py`
  - 新規監査スクリプト

## import

production code の import 変更はありません。

既存 import:
- `order_toda_group_proof_narrative_arguments`
- `extract_toda_group_proof_narrative_argument_local_body_blocks`
- `extract_toda_group_proof_narrative_argument_conclusion_step`

を再利用する。

## 修正理由

repair2 は全 visible statement の paragraph slots を global に再利用したため、
別 Argument に属する eta_2 definition / final result まで前方へ移動した。

repair3 は visible ProofStep を、実際の Argument 表示順に従って
「最初に表示責任を持つ Argument」に一度だけ割り当てる。

並べ替えは各 Argument の owned paragraph slots 内だけで行う。

## 変更関数全文

`apply_phase159_pi3_2_visible_dependency_topological_order_repair3.py`
内の `NEW_FUNCTION` が置換後の関数全文。

コード内の省略はない。

## ordering contract

各 Argument 内で:

1. `presentation.edges` の direct dependency edge のみ利用。
2. owned visible steps だけで DAG を構成。
3. topological validity を維持。
4. 直前の step により newly-ready になった consumer を優先。
5. newly-ready が複数なら元表示順を tie-break に利用。
6. cycle の場合はその Argument を変更しない。
7. 別 Argument の paragraph slot へ statement を移動しない。

## focused pytest

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

## 完了条件

public proof body 内で:

- `pi_2^1=0 < H 単射 < pi_3^3`
- `E 同型 < E 単射 < Delta=0 < H 全射`
- `H 単射 < H 同型`
- `H 全射 < H 同型`
- `H 同型 < eta_2 definition < final result`

を満たす。

Reference section の同一 statement を `str.index()` が拾わないよう、
テストは `## 証明` より後の proof body だけを評価する。

## 次 Phase との境界

- proof graph に edge を追加しない。
- statement type 優先順位を追加しない。
- Argument model を変更しない。
- multi-Argument renderer を再設計しない。
- 全体テストは Phase 159 最終段階まで実行しない。
