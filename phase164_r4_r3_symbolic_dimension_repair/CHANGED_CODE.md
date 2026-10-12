# Phase 164 R4-R3 修正内容

## 変更対象

- `phase164_r4_r3_independent_semantic_audit.py` の `assess_typed_clauses` 関数（関数全体を置換）。
- `tests/test_phase164_r4_r3_independent_semantic_audit.py` の新規テスト2件（末尾に追加）。既存7テストは保持。
- PowerShell ランナーは既存 R4-R3 の局所テスト実行方式を保持。

## 原因と境界

`higher_eta_group_relation.lhs.sphere_dimension` は `ScalarSymbol("n")` である。Python の `>=3` は型エラーとなるため、`ScalarSum(n,1)`、位数2、生成元 `η_n` の記号構造を検査する。`n>=3` の全範囲の数学的真偽、原本照合、引用資格は未承認のまま。

## 変更後 import 部分（関数内 import を含む完全版）

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r2_semantic_structure import compare_structured_leaves
```

## 変更後の関数全体

```python
def assess_typed_clauses(crosswalk: dict, leaves: tuple[object, ...]) -> dict:
    """Verify concrete typed claims; decline unproved universal/general claims."""
    from expression import HomotopyElement, MapApplication, Multiple, ScalarSum, ScalarSymbol
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
    from map_facts import EHP_H_MAP
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp51FiniteDimensionalStatement

    if len(leaves) != 2 or any(getattr(s, "rule", None) is not ProofRule.INFERENCE for s in leaves):
        raise ValueError("expected two existing INFERENCE leaves")
    prior = compare_structured_leaves(crosswalk, leaves)
    if not (prior["prop51"]["all_four_components_structurally_present"]
            and prior["nu_prime_hopf"]["source_tokens_all_present"]):
        raise ValueError("R4-R2 structural audit not satisfied")
    prop_source = _source_row(crosswalk, "prop51_finite_dimensional")["source_text"]
    hopf_source = _source_row(crosswalk, "nu_prime_hopf")["source_text"]
    prop = leaves[0].conclusion
    hopf = leaves[1].conclusion
    if not isinstance(prop, TodaProp51FiniteDimensionalStatement):
        raise ValueError("unexpected Prop 5.1 conclusion type")

    g = prop.pi3_2_group_relation
    g_ok = (isinstance(g, Relation) and g.relation_type is RelationType.EQUALITY
            and _group(g.lhs, 3, 2) and isinstance(g.rhs, FreeCyclicGroup)
            and _element(g.rhs.generator, "η", 2, 3, 2)
            and all(token in prop_source for token in (r"\pi^{2}_{3}", r"\gen{\eta_2}", r"\mathbb Z")))

    h = prop.eta2_hopf_relation
    h_ok = (isinstance(h, Relation) and h.relation_type is RelationType.EQUALITY
            and isinstance(h.lhs, MapApplication) and h.lhs.map == EHP_H_MAP
            and _element(h.lhs.expression, "η", 2, 3, 2)
            and isinstance(h.rhs, HomotopyElement)
            and h.rhs.name == "ι_3"
            and h.rhs.dimension == 3
            and r"H(\eta_2)=\iota_3" in prop_source)

    delta = prop.delta_iota5_relation
    positive = getattr(delta, "positive_value", None)
    delta_ok = (isinstance(delta, TodaDeltaImageUpToSignStatement)
                and _group(getattr(delta.map, "source_group", None), 5, 5)
                and _group(getattr(delta.map, "target_group", None), 3, 2)
                and isinstance(delta.element, HomotopyElement)
                and delta.element.name == "ι_5"
                and isinstance(positive, Multiple)
                and positive.coefficient == 2
                and _element(positive.expression, "η", 2, 3, 2)
                and r"\Delta(\iota_5)=\pm 2\,\eta_2" in prop_source)

    # The production result is a symbolic n-family, not a concrete integer case.
    # Checking n >= 3 with Python would raise TypeError for ScalarSymbol.
    higher = prop.higher_eta_group_relation
    higher_symbolic = False
    if isinstance(higher, Relation) and higher.relation_type is RelationType.EQUALITY:
        lhs = higher.lhs
        rhs = higher.rhs
        n = getattr(lhs, "sphere_dimension", None)
        dimension = getattr(lhs, "group_dimension", None)
        generator = getattr(rhs, "generator", None)
        higher_symbolic = (
            isinstance(n, ScalarSymbol)
            and n.name == "n"
            and isinstance(dimension, ScalarSum)
            and dimension.left == n
            and dimension.right == 1
            and isinstance(rhs, FiniteCyclicGroup)
            and rhs.order == 2
            and isinstance(generator, HomotopyElement)
            and getattr(generator.generator, "family", None) == "η"
            and getattr(generator.generator, "index", None) == n
            and generator.dimension == n
            and r"\pi^{n}_{n+1}" in prop_source
            and r"(n\ge3)" in prop_source
        )

    relation_ok = (isinstance(hopf, Relation)
                   and hopf.relation_type is RelationType.EQUALITY
                   and isinstance(hopf.lhs, MapApplication)
                   and hopf.lhs.map == EHP_H_MAP
                   and isinstance(hopf.lhs.expression, HomotopyElement)
                   and hopf.lhs.expression.name == "ν′"
                   and (hopf.lhs.expression.source, hopf.lhs.expression.target) == (6, 3)
                   and _element(hopf.rhs, "η", 5, 6, 5)
                   and r"\nu'\in\pi_6^3" in hopf_source
                   and r"H(\nu')=\eta_5" in hopf_source)
    checks = {
        "pi3_2_free_cyclic_eta2": bool(g_ok),
        "eta2_hopf_iota3": bool(h_ok),
        "delta_iota5_up_to_sign_twice_eta2": bool(delta_ok),
        "higher_eta_symbolic_family_structure": bool(higher_symbolic),
        "nu_prime_hopf_eta5": bool(relation_ok),
    }
    if not all(checks.values()):
        raise ValueError("typed mathematical clause mismatch: " + ", ".join(k for k, v in checks.items() if not v))
    return {
        "phase": "164 R4-R3",
        "mode": "READ_ONLY_INDEPENDENT_TYPED_CLAUSE_AUDIT",
        "status": "TYPED_CLAUSE_CONSISTENCY_CONFIRMED_AUTHORIZATION_BLOCKED",
        "source_statement_ids": [EXPECTED_SOURCES[k][0] for k in EXPECTED_SOURCES],
        "typed_checks": checks,
        "typed_checks_passed": len(checks),
        "proposition_5_1_universal_range_verified": False,
        "proposition_5_1_stable_clause_covered": False,
        "equation_5_3_double_nu_clause_covered": False,
        "translated_source_clauses_structurally_consistent": True,
        "independent_original_edition_verified": False,
        "independent_mathematical_truth_verified": False,
        "publication_and_availability_verified": False,
        "typed_registry_binding_written": False,
        "citation_eligible": False,
        "proof_search_connected": False,
        "production_modified": False,
        "full_pytest_run": False,
    }

```

## 追加テスト全文・必要 import

```python
from dataclasses import replace
import pytest
from phase164_r4_r3_independent_semantic_audit import assess_typed_clauses

def test_symbolic_eta_family_kept_symbolic(inputs):
    from expression import ScalarSum, ScalarSymbol

    crosswalk, leaves = inputs
    relation = leaves[0].conclusion.higher_eta_group_relation
    n = relation.lhs.sphere_dimension
    assert isinstance(n, ScalarSymbol)
    assert n.name == "n"
    assert relation.lhs.group_dimension == ScalarSum(left=n, right=1)
    report = assess_typed_clauses(crosswalk, leaves)
    assert report["typed_checks"]["higher_eta_symbolic_family_structure"]
    assert not report["proposition_5_1_universal_range_verified"]


def test_corrupted_symbolic_eta_group_dimension_rejected(inputs):
    from expression import ScalarSum

    crosswalk, leaves = inputs
    statement = leaves[0].conclusion
    relation = statement.higher_eta_group_relation
    n = relation.lhs.sphere_dimension
    bad_group = replace(relation.lhs, group_dimension=ScalarSum(left=n, right=2))
    changed_relation = replace(relation, lhs=bad_group)
    changed_statement = replace(statement, higher_eta_group_relation=changed_relation)
    changed_step = replace(leaves[0], conclusion=changed_statement)
    with pytest.raises(ValueError, match="typed mathematical clause mismatch"):
        assess_typed_clauses(crosswalk, (changed_step, leaves[1]))
```

## 実行 pytest と完了条件

`python -B -m pytest -q tests/test_phase164_r4_r3_independent_semantic_audit.py tests/test_phase164_r4_r2_semantic_structure.py tests/test_phase164_r4_r1_source_crosswalk.py`

9件の R4-R3 テスト（既存7件＋追加2件）および先行監査テストの成功、監査 JSON 生成、引用資格 false を完了条件とする。全体 pytest は Phase 最後だけ。次の R4-R4 で独立出典根拠を扱う。
