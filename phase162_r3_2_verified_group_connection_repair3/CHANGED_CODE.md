# R3-2 repair3 — 変更箇所と全文

- `phase162_web_narrative_integration.py`: `toda_rules` の追加 import および `_build_phase162_existing_group_connection()` のみを変更。インストーラが AST で関数全体を置換する。その他の関数と既存公開APIは維持。
- `tests/test_phase162_r3_2_verified_group_connection.py`: テストの `root` 探索を修正し、生成元一致テストを追加。
- `run_phase162_r3_2_repair3.ps1`: 実行対象パスの修正。
- `apply_phase162_r3_2_repair3.py`: 新規。直前コードとの整合性を検証して部分的に置換。

## 変更後の import 全文

```python
"""Phase 162 R5: add a separately validated map-isomorphism proof to web narrative."""

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement


from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase162_r2_existing_proof_connection import (
    reconstruct_phase162_r2_from_existing_proofs,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import Relation, RelationType, apply_inference_match, find_inference_match
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
)
```

## `_build_phase162_existing_group_connection` 全文

```python
def _build_phase162_existing_group_connection():
    """Build the group-root proof from independently derived existing evidence."""
    phase50 = build_phase50_representative_result()
    phase56 = build_phase56_representative_result()
    pi4_3_steps = phase50["final_group_steps"]
    toda52_steps = phase56["composition_isomorphism_steps"]
    if len(pi4_3_steps) != 1 or len(toda52_steps) != 1:
        raise ValueError("Expected one independently derived source premise of each kind")
    transport = toda_52_pi4_2_finite_cyclic_transport_inference_rule()
    match = find_inference_match(transport, (pi4_3_steps[0], toda52_steps[0]))
    if match is None:
        raise ValueError("Could not derive pi_4^2 from the existing Toda (5.2) evidence")
    source_step = apply_inference_match(match)
    if source_step.rule is not ProofRule.INFERENCE:
        raise ValueError("Source group must be derived")

    pi4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    if source_step.conclusion.lhs != pi4_2 or not isinstance(source_step.conclusion.rhs, FiniteCyclicGroup):
        raise ValueError("Existing source proof does not establish expected cyclic group")
    eta_definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    source_generator = source_step.conclusion.rhs.generator
    bridge_rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    bridge_match = find_inference_match(bridge_rule, eta_definitions)
    if bridge_match is None:
        raise ValueError("Existing eta-family definitions do not derive the image")
    bridge_step = apply_inference_match(bridge_match)
    from expression import Composition, Suspension
    if (
        not isinstance(bridge_step.conclusion, Relation)
        or bridge_step.conclusion.relation_type is not RelationType.EQUALITY
        or bridge_step.conclusion.lhs != Suspension(expression=source_generator)
        or not isinstance(bridge_step.conclusion.rhs, Composition)
        or bridge_step.conclusion.rhs.left.generator.family != "η"
        or bridge_step.conclusion.rhs.left.generator.index != 3
        or bridge_step.conclusion.rhs.right.generator.family != "η"
        or bridge_step.conclusion.rhs.right.generator.index != 4
    ):
        raise ValueError("Eta-family bridge does not match the source and target generators")
    goal = Relation(
        lhs=pi5_3,
        rhs=FiniteCyclicGroup(
            order=source_step.conclusion.rhs.order,
            generator=bridge_step.conclusion.rhs,
        ),
        relation_type=RelationType.EQUALITY,
    )
    suspension_map = TodaSuspensionMap(source_group=pi4_2, target_group=pi5_3)
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf_eta5) + exactness
    roots = {}
    seen = set()

    def collect(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            roots[identity] = step
        for premise in step.premises:
            collect(premise)

    for step in (source_step,) + eta_definitions + ehp_leaves:
        collect(step)
    return reconstruct_phase162_r2_from_existing_proofs(
        goal=goal,
        suspension_map=suspension_map,
        source_structure_steps=(source_step,),
        eta_definition_steps=eta_definitions,
        ehp_leaf_steps=ehp_leaves,
        trusted_given_roots=tuple(roots.values()),
    )
```

## 変更後テスト関数全文と import

```python
from pathlib import Path


def test_r3_2_only_lower_panel_label_is_changed():
    root = Path(__file__).resolve().parents[2]
    text = (root / "web_group_proof.py").read_text(encoding="utf-8-sig")
    assert "## 群構造の検証済み証明" in text
    assert "build_phase162_web_validated_isomorphism_markdown" in text
```

```python
from expression import Composition, Suspension
from proof import ProofRule, Relation, RelationType
from phase162_web_narrative_integration import _build_phase162_existing_group_connection


def test_r3_2_generator_is_derived_from_eta_bridge():
    connection = _build_phase162_existing_group_connection()
    source = connection.source_structure_step.conclusion.rhs.generator
    image = connection.generator_image_step.conclusion
    target = connection.reconstruction.goal.rhs.generator
    assert isinstance(image, Relation)
    assert image.relation_type is RelationType.EQUALITY
    assert image.lhs == Suspension(expression=source)
    assert isinstance(target, Composition)
    assert image.rhs == target
    assert connection.generator_image_step.rule is ProofRule.INFERENCE
```

## 完了条件と次段階

既存のR2/R3テストと今回のWeb接続focusedテストが通ること。R3-3で文献Referenceと既証明の群構造の帰属を整理する。全体テストはPhase末尾まで保留。
