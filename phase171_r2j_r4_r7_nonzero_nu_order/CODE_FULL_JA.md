# Phase 171 R2J-R4-R7 — 変更コード全文と実行手順

## GitHub 監査と変更境界

GitHub `akebono03/ehp-proof-tracer` の `develop` について、実行ログ HEAD `19fe298c` から1コミット進んだ現行コードを確認した。R4-R3、R4-R5、R4-R6、R2J-R3、推論照合器 `proof.py` および関連テストを確認した。新しいディレクトリだけを追加し、本番コード・既存テスト・既存文書を変更しない。

## 変更対象

- `phase171_r2j_r4_r7_nonzero_nu_order/source.py`: `NonZeroGroupElement`、`FiniteElementOrder`、`nonzero_cyclic_generator_image()`、`injected_generator_nonzero_rule()`、`nonzero_double_from_equality()`、`inferred_nonzero_double_rule()`、`order_four_from_nonzero_double()`、`inferred_order_four_rule()` を新規追加。
- `phase171_r2j_r4_r7_nonzero_nu_order/audit.py`: `_git()`、`_infer()`、`build_nonzero_nu_order_proof()`、`main()` を新規追加。
- `phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py`: テスト関数12件を新規追加。
- `run.ps1` と `README.md`、`監査仕様.md`、`__init__.py`、`tests/__init__.py` を新規追加。

追加位置はリポジトリ直下の新規ディレクトリ。既存コードの import や関数は変更しない。全てのコードを省略せず記載する。

## 新規 source.py — クラスと関数をファイル全文で追加

```python
"""Generic typed inference of an injected nonzero generator and order four.

A finite cyclic generator is nonzero for order >= 2. Injectivity transports
its nonzeroness. Equality transfers nonzeroness to a double, and a group
of cardinality four with a nonzero double has an element of order four.

These constructors propose typed conclusions only. They do not create GIVEN
leaves or promote a database goal into a theorem.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase165_r14_r6_generic_iso import MapInjective
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


@dataclass(frozen=True)
class NonZeroGroupElement:
    group: TodaPrimaryGroup
    element: object


@dataclass(frozen=True)
class FiniteElementOrder:
    group: TodaPrimaryGroup
    element: object
    order: int


def nonzero_cyclic_generator_image(
    source_group: object, injective: object, image: object,
) -> NonZeroGroupElement | None:
    """Infer E(x) != 0 for a proved finite-cyclic generator x and injective E.

    Typed HyoujiGen identity bridges prior citations with missing endpoint
    annotations, but never confers proof status without the source relation.
    """
    if (
        not isinstance(source_group, Relation)
        or source_group.relation_type is not RelationType.EQUALITY
        or not isinstance(source_group.lhs, TodaPrimaryGroup)
        or not isinstance(source_group.rhs, FiniteCyclicGroup)
        or type(source_group.rhs.order) is not int
        or source_group.rhs.order < 2
        or not isinstance(injective, MapInjective)
        or not isinstance(injective.map, TodaSuspensionMap)
        or injective.map.source_group != source_group.lhs
        or not isinstance(image, MapApplication)
        or image.map != EHP_E_MAP
    ):
        return None
    source, target = _endpoints(image.expression), injective.map.target_group
    if (
        source != (
            source_group.lhs.group_dimension,
            source_group.lhs.sphere_dimension,
        )
        or target != TodaPrimaryGroup(
            source_group.lhs.group_dimension + 1,
            source_group.lhs.sphere_dimension + 1,
        )
    ):
        return None
    exact_generator = source_group.rhs.generator == image.expression
    registered_identity = same_registered_group_presentation(
        source_group.rhs,
        FiniteCyclicGroup(source_group.rhs.order, image.expression),
    )
    if not exact_generator and not registered_identity:
        return None
    return NonZeroGroupElement(target, image)


def injected_generator_nonzero_rule(
    goal: NonZeroGroupElement,
    source_group: Relation,
    injective: MapInjective,
) -> InferenceRule:
    if nonzero_cyclic_generator_image(source_group, injective, goal.element) != goal:
        raise ValueError("source generator, injection and nonzero image do not match")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and premises[0].conclusion == source_group
            and premises[1].conclusion == injective
            and nonzero_cyclic_generator_image(
                premises[0].conclusion, premises[1].conclusion, goal.element,
            ) == goal
        )

    return InferenceRule(
        name="injective map preserves nonzero finite-cyclic generator",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def nonzero_double_from_equality(
    equality: object, nonzero_image: object,
) -> NonZeroGroupElement | None:
    """Use exact typed equality 2*x=E(y), not display-name matching."""
    if (
        not isinstance(equality, Relation)
        or equality.relation_type is not RelationType.EQUALITY
        or not isinstance(equality.lhs, Multiple)
        or type(equality.lhs.coefficient) is not int
        or equality.lhs.coefficient != 2
        or not isinstance(equality.rhs, MapApplication)
        or equality.rhs.map != EHP_E_MAP
        or not isinstance(nonzero_image, NonZeroGroupElement)
        or nonzero_image.element != equality.rhs
        or not isinstance(nonzero_image.group, TodaPrimaryGroup)
        or _endpoints(equality.lhs.expression) != (
            nonzero_image.group.group_dimension,
            nonzero_image.group.sphere_dimension,
        )
    ):
        return None
    return NonZeroGroupElement(nonzero_image.group, equality.lhs)


def inferred_nonzero_double_rule(
    goal: NonZeroGroupElement,
    equality: Relation,
    nonzero_image: NonZeroGroupElement,
) -> InferenceRule:
    if nonzero_double_from_equality(equality, nonzero_image) != goal:
        raise ValueError("nonzero double does not follow from typed equality")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and premises[0].conclusion == equality
            and premises[1].conclusion == nonzero_image
            and nonzero_double_from_equality(
                premises[0].conclusion, premises[1].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="typed equality transfers nonzeroness to double",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation,
                           relation_type=RelationType.EQUALITY),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=NonZeroGroupElement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def order_four_from_nonzero_double(
    cardinality: object, nonzero_double: object,
) -> FiniteElementOrder | None:
    """Lagrange: order(x) divides four; 2*x != 0 forces order(x)=4."""
    if (
        not isinstance(cardinality, FiniteGroupCardinality)
        or cardinality.order != 4
        or type(cardinality.order) is not int
        or not isinstance(cardinality.group, TodaPrimaryGroup)
        or not isinstance(nonzero_double, NonZeroGroupElement)
        or nonzero_double.group != cardinality.group
        or not isinstance(nonzero_double.element, Multiple)
        or type(nonzero_double.element.coefficient) is not int
        or nonzero_double.element.coefficient != 2
        or _endpoints(nonzero_double.element.expression) != (
            cardinality.group.group_dimension,
            cardinality.group.sphere_dimension,
        )
    ):
        return None
    return FiniteElementOrder(
        cardinality.group, nonzero_double.element.expression, 4,
    )


def inferred_order_four_rule(
    goal: FiniteElementOrder,
    cardinality: FiniteGroupCardinality,
    nonzero_double: NonZeroGroupElement,
) -> InferenceRule:
    if order_four_from_nonzero_double(cardinality, nonzero_double) != goal:
        raise ValueError("order four cannot be concluded without a nonzero double")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and premises[0].conclusion == cardinality
            and premises[1].conclusion == nonzero_double
            and order_four_from_nonzero_double(
                premises[0].conclusion, premises[1].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite order-four group and nonzero double imply order-four element",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=FiniteGroupCardinality),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=NonZeroGroupElement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )
```

## 新規 audit.py — 関数をファイル全文で追加

```python
"""Read-only Phase 171 R2J-R4-R7 replay: 2 nu' != 0, then order(nu')=4.

Use the R4-R3 typed double relation, R2J-R3 injectivity, a unique earlier
pi_5^2 group source and the R4-R6 cardinality. No middle-group structure
is given or inferred here; its cyclic presentation is reserved for R4-R8.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from expression import MapApplication
from homotopy_groups import TodaPrimaryGroup
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r3_double_image_bridge.audit import build_double_image_proof
from phase171_r2j_r4_r5_short_exact_sequence.audit import _screened_leaf_ids
from phase171_r2j_r4_r6_middle_cardinality.audit import build_middle_cardinality_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    FiniteElementOrder,
    NonZeroGroupElement,
    inferred_nonzero_double_rule,
    inferred_order_four_rule,
    injected_generator_nonzero_rule,
    nonzero_cyclic_generator_image,
    nonzero_double_from_equality,
    order_four_from_nonzero_double,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("R4-R7 permits read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def _infer(rule, parents: tuple[ProofStep, ...], goal: object) -> ProofStep:
    """Require one ordered, real matcher result and a genuine ProofStep root."""
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, parents)
        if len(match.premises) == len(parents)
        and all(a is b for a, b in zip(match.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique genuine typed inference match")
    root = derive_inference_proof_step(matches[0])
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != goal
        or len(root.premises) != len(parents)
        or any(a is not b for a, b in zip(root.premises, parents))
    ):
        raise RuntimeError("derived inference step failed the parent contract")
    return root


def build_nonzero_nu_order_proof() -> tuple[ProofStep, ProofStep, tuple[ProofStep, ...], dict]:
    """Replay all earlier proof trees, then derive double nonzero and order four."""
    screened, pi63_goal, citing = _screened_context()
    cardinality_root, _, cardinality_report = build_middle_cardinality_proof()
    double_root, _, double_report = build_double_image_proof()
    if (
        cardinality_root.rule is not ProofRule.INFERENCE
        or cardinality_root.conclusion.group != TodaPrimaryGroup(6, 3)
        or cardinality_root.conclusion.order != 4
        or double_root.rule is not ProofRule.INFERENCE
        or not isinstance(double_root.conclusion, Relation)
        or cardinality_report["new_given_added"] != 0
        or double_report["new_given_added"] != 0
    ):
        raise RuntimeError("R4-R3/R4-R6 inferred antecedents are unavailable")

    # Reuse exact ProofSteps from the successful R4-R6 tree; do not recreate
    # the source as a GIVEN or reconstruct the injectivity result from labels.
    prior_group = cardinality_root.premises[0]
    short_exact = cardinality_root.premises[1]
    if (
        prior_group.rule is not ProofRule.GIVEN
        or len(short_exact.premises) != 3
        or short_exact.rule is not ProofRule.INFERENCE
    ):
        raise RuntimeError("prior group or short exact proof ancestry malformed")
    e_injective = short_exact.premises[0]
    if (
        e_injective.rule is not ProofRule.INFERENCE
        or not isinstance(e_injective.conclusion, MapInjective)
    ):
        raise RuntimeError("missing proved E injection from short exact proof")
    typed_equality = double_root.conclusion
    image = typed_equality.rhs
    if not isinstance(image, MapApplication) or image.map != EHP_E_MAP:
        raise RuntimeError("R4-R3 double equality has no typed E-image")

    generator_nonzero = nonzero_cyclic_generator_image(
        prior_group.conclusion, e_injective.conclusion, image,
    )
    if generator_nonzero is None:
        raise RuntimeError("prior generator does not match injected triple eta")
    image_rule = injected_generator_nonzero_rule(
        generator_nonzero, prior_group.conclusion, e_injective.conclusion,
    )
    image_root = _infer(image_rule, (prior_group, e_injective), generator_nonzero)

    doubled_nonzero = nonzero_double_from_equality(
        typed_equality, generator_nonzero,
    )
    if doubled_nonzero is None:
        raise RuntimeError("derived double equality is not compatible with nonzero E-image")
    double_nonzero_rule = inferred_nonzero_double_rule(
        doubled_nonzero, typed_equality, generator_nonzero,
    )
    double_nonzero_root = _infer(
        double_nonzero_rule, (double_root, image_root), doubled_nonzero,
    )

    order_goal = order_four_from_nonzero_double(
        cardinality_root.conclusion, doubled_nonzero,
    )
    if (
        order_goal is None
        or not isinstance(order_goal, FiniteElementOrder)
        or order_goal.group != TodaPrimaryGroup(6, 3)
        or order_goal.element != typed_equality.lhs.expression
        or order_goal.order != 4
    ):
        raise RuntimeError("nonzero doubled element and group order do not prove order four")
    order_rule = inferred_order_four_rule(
        order_goal, cardinality_root.conclusion, doubled_nonzero,
    )
    order_root = _infer(
        order_rule, (cardinality_root, double_nonzero_root), order_goal,
    )
    nodes = proof_ancestry(order_root)
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    ids = _screened_leaf_ids(screened, citing, leaves)
    if (
        double_nonzero_root.rule is not ProofRule.INFERENCE
        or double_nonzero_root.conclusion != NonZeroGroupElement(
            TodaPrimaryGroup(6, 3), typed_equality.lhs,
        )
        or not ids
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
        or any(node.rule is ProofRule.GIVEN and node.conclusion in (
            order_goal, doubled_nonzero, generator_nonzero,
        ) for node in nodes)
    ):
        raise RuntimeError("a group result or forged nonzero/order-four fact entered ancestry")
    report = {
        "phase": "171-R2J-R4-R7",
        "mode": "READ_ONLY_TYPED_NONZERO_AND_ELEMENT_ORDER_REPLAY",
        "status": "INFERRED",
        "prior_source": repr(prior_group.conclusion),
        "e_injective": repr(e_injective.conclusion),
        "double_relation": repr(typed_equality),
        "cardinality": repr(cardinality_root.conclusion),
        "nonzero_image": repr(image_root.conclusion),
        "nonzero_double": repr(double_nonzero_root.conclusion),
        "element_order": repr(order_root.conclusion),
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": len(leaves),
        "verified_source_ids": list(dict.fromkeys(ids)),
        "new_given_added": 0,
        "nu_prime_double_nonzero_proven": True,
        "nu_prime_order_four_proven": True,
        "pi63_cyclic_presentation_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return double_nonzero_root, order_root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4-R7 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    for relative in (
        "phase171_r2j_r4_r3_double_image_bridge/audit.py",
        "phase171_r2j_r4_r6_middle_cardinality/audit.py",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing earlier proof module: " + relative)
    print("PHASE171_R2J_R4_R7_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R7_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R7_RESULT=PASS_DRY_RUN", flush=True)
        return
    nonzero, order, nodes, report = build_nonzero_nu_order_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source changed during read-only proof replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R7_DOUBLE_NONZERO=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R7_NU_PRIME_ORDER_FOUR=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R7_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R7_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R7_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R7_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R7_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R7_RUN=PASS", flush=True)
    print("PHASE171_R2J_R4_R7_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## 新規 tests/test_audit.py — import と全テスト関数

```python
"""Focused type, provenance, negative and end-to-end proof tests for R4-R7."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.audit import (
    _git,
    build_nonzero_nu_order_proof,
)
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    FiniteElementOrder,
    NonZeroGroupElement,
    inferred_nonzero_double_rule,
    inferred_order_four_rule,
    injected_generator_nonzero_rule,
    nonzero_cyclic_generator_image,
    nonzero_double_from_equality,
    order_four_from_nonzero_double,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _eta(n: int, *, typed: bool = True) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n,
        source=n + 1 if typed else None,
        target=n if typed else None,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int, *, typed: bool = True) -> Composition:
    return Composition(
        _eta(n, typed=typed),
        Composition(_eta(n + 1, typed=typed), _eta(n + 2, typed=typed)),
    )


def _fixture():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    source = Relation(a, FiniteCyclicGroup(2, _triple(2)), RelationType.EQUALITY)
    injective = MapInjective(TodaSuspensionMap(a, b))
    image = MapApplication(EHP_E_MAP, _triple(2))
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    equality = Relation(Multiple(2, nu), image, RelationType.EQUALITY)
    finite = FiniteGroupCardinality(b, 4)
    return source, injective, equality, finite


def test_injective_nonzero_from_a_real_finite_cyclic_generator():
    source, injective, equality, _ = _fixture()
    value = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert value == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.rhs)
    rule = injected_generator_nonzero_rule(value, source, injective)
    parents = (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(injective, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    root = derive_inference_proof_step(matches[0])
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == value
    assert root.premises == parents


def test_prior_untyped_eta_composition_is_matched_by_registered_identity():
    source, injective, equality, _ = _fixture()
    untyped = replace(source, rhs=FiniteCyclicGroup(2, _triple(2, typed=False)))
    assert source.rhs.generator != untyped.rhs.generator
    assert nonzero_cyclic_generator_image(
        untyped, injective, equality.rhs,
    ) == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.rhs)


def test_wrong_generator_map_and_cyclic_order_are_rejected():
    source, injective, equality, _ = _fixture()
    wrong_gen = replace(source, rhs=FiniteCyclicGroup(2, _triple(3)))
    wrong_e = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert nonzero_cyclic_generator_image(wrong_gen, injective, equality.rhs) is None
    assert nonzero_cyclic_generator_image(source, wrong_e, equality.rhs) is None
    assert nonzero_cyclic_generator_image(
        replace(source, rhs=FiniteCyclicGroup(1, source.rhs.generator)),
        injective, equality.rhs,
    ) is None
    assert nonzero_cyclic_generator_image(
        replace(source, rhs=FiniteCyclicGroup(True, source.rhs.generator)),
        injective, equality.rhs,
    ) is None


def test_nonzero_image_rule_rejects_fabricated_given_injectivity():
    source, injective, equality, _ = _fixture()
    goal = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert goal is not None
    rule = injected_generator_nonzero_rule(goal, source, injective)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(source, (), ProofRule.GIVEN),
        ProofStep(injective, (), ProofRule.GIVEN),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(source, (), ProofRule.RELATION),
        ProofStep(injective, (), ProofRule.INFERENCE),
    )) == ()


def test_typed_equality_transfers_nonzero_to_exact_double():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    value = nonzero_double_from_equality(equality, nonzero)
    assert value == NonZeroGroupElement(TodaPrimaryGroup(6, 3), equality.lhs)
    rule = inferred_nonzero_double_rule(value, equality, nonzero)
    parents = (
        ProofStep(equality, (), ProofRule.INFERENCE),
        ProofStep(nonzero, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    root = derive_inference_proof_step(matches[0])
    assert root.conclusion == value
    assert root.premises == parents


def test_wrong_double_coefficient_equality_and_group_fail_closed():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    for bad in (0, 1, 3, True):
        altered = replace(equality, lhs=Multiple(bad, equality.lhs.expression))
        assert nonzero_double_from_equality(altered, nonzero) is None
    assert nonzero_double_from_equality(
        replace(equality, rhs=MapApplication(EHP_E_MAP, _triple(3))),
        nonzero,
    ) is None
    assert nonzero_double_from_equality(
        equality,
        replace(nonzero, group=TodaPrimaryGroup(6, 4)),
    ) is None


def test_nonzero_double_must_have_inferred_equality_and_image():
    source, injective, equality, _ = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    assert nonzero is not None
    value = nonzero_double_from_equality(equality, nonzero)
    assert value is not None
    rule = inferred_nonzero_double_rule(value, equality, nonzero)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(equality, (), ProofRule.GIVEN),
        ProofStep(nonzero, (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(equality, (), ProofRule.INFERENCE),
        ProofStep(nonzero, (), ProofRule.GIVEN),
    )) == ()


def test_order_four_uses_cardinality_and_nonzero_double():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    goal = order_four_from_nonzero_double(finite, doubled)
    assert goal == FiniteElementOrder(TodaPrimaryGroup(6, 3), equality.lhs.expression, 4)
    rule = inferred_order_four_rule(goal, finite, doubled)
    parents = (
        ProofStep(finite, (), ProofRule.INFERENCE),
        ProofStep(doubled, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, (parents[1], parents[0]))
    assert len(matches) == 1
    assert matches[0].premises == parents
    assert derive_inference_proof_step(matches[0]).conclusion == goal


def test_cardinality_and_nonzero_double_must_match():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    assert order_four_from_nonzero_double(
        replace(finite, order=2), doubled,
    ) is None
    assert order_four_from_nonzero_double(
        replace(finite, order=True), doubled,
    ) is None
    assert order_four_from_nonzero_double(
        finite, replace(doubled, group=TodaPrimaryGroup(7, 3)),
    ) is None
    assert order_four_from_nonzero_double(
        finite, replace(doubled, element=Multiple(3, equality.lhs.expression)),
    ) is None


def test_order_four_rule_requires_two_inferences():
    source, injective, equality, finite = _fixture()
    nonzero = nonzero_cyclic_generator_image(source, injective, equality.rhs)
    doubled = nonzero_double_from_equality(equality, nonzero)
    assert doubled is not None
    goal = order_four_from_nonzero_double(finite, doubled)
    assert goal is not None
    rule = inferred_order_four_rule(goal, finite, doubled)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(finite, (), ProofRule.GIVEN),
        ProofStep(doubled, (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(finite, (), ProofRule.INFERENCE),
        ProofStep(doubled, (), ProofRule.GIVEN),
    )) == ()


def test_git_guard_rejects_write_operations():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_proof_replay_is_source_bound_and_not_a_cyclic_group_claim():
    double_nonzero_root, order_root, nodes, report = build_nonzero_nu_order_proof()
    assert double_nonzero_root.rule is ProofRule.INFERENCE
    assert order_root.rule is ProofRule.INFERENCE
    assert order_root.conclusion.order == 4
    assert report["status"] == "INFERRED"
    assert report["nu_prime_double_nonzero_proven"] is True
    assert report["nu_prime_order_four_proven"] is True
    assert report["pi63_cyclic_presentation_proven"] is False
    assert report["new_given_added"] == 0
    assert len(report["verified_source_ids"]) >= 3
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) >= 3
```

## 新規 run.ps1 — 解凍後の実行コード

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r7_nonzero_nu_order.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R4_R7_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py `
        phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py `
        phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R4_R7_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r7_nonzero_nu_order.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R7 nonzero/order proof replay failed' }
    Write-Output 'PHASE171_R2J_R4_R7_RESULT=PASS_AUDIT_ONLY'
}
finally {
    Pop-Location
}
```

## 新規 README.md — 英語全文

```markdown
# EHP Proof Tracer — Phase 171 R2J-R4-R7

This independent, read-only audit reconstructs two typed inferences:

1. $2\nu'\neq0$ in $\pi_6^3$ from the already proved $2\nu'=E(\eta_2^3)$, the injectivity of $E:\pi_5^2\to\pi_6^3$, and the earlier cited $\pi_5^2\cong\mathbb Z/2\{\eta_2^3\}$.
2. $\nu'$ has order exactly four using the R4-R6 inferred cardinality $|\pi_6^3|=4$ and the inferred nonzero double.

The rules are structural and work with typed group endpoints and matched generator identity, not printed expressions. The earlier cited group is an existing screened `GIVEN` leaf and is never recreated or promoted from database metadata. The R4-R3 relation, E-injectivity, and R4-R6 cardinality remain independently inferred proof subtrees.

## Scope

The package adds only `phase171_r2j_r4_r7_nonzero_nu_order/`: `source.py`, `audit.py`, focused tests, launcher, and full source records. It does not modify production Providers, prior phase packages, the tracked documentation, or the Git index. It does not assert a completed cyclic presentation of $\pi_6^3$; that final step belongs to R4-R8.

## Windows PowerShell

From the repository root, extract the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1"
git status -sb
git diff --stat
```

The runner checks the `develop` branch, runs 31 focused tests (12 new, 10 R4-R6 and 9 R4-R3), then reconstructs the actual proof trees. It leaves the entire test suite for Phase 171 closeout. Real-repository test and replay success must be verified on the local worktree.

## Success criteria

The audit must report `PHASE171_R2J_R4_R7_DOUBLE_NONZERO=INFERRED`, `PHASE171_R2J_R4_R7_NU_PRIME_ORDER_FOUR=INFERRED`, `PHASE171_R2J_R4_R7_NEW_GIVEN=0`, and `PHASE171_R2J_R4_R7_PI63_PROVEN=False`. Every `GIVEN` ancestor must uniquely match an earlier publication-screened fixed assertion; a completed middle-group presentation must not enter the proof.
```

## 新規 監査仕様.md — 日本語全文

```markdown
# Phase 171 R2J-R4-R7 — $2\nu'\neq0$ と位数4の型付き証明

## 対象・前提

GitHub `akebono03/ehp-proof-tracer` の `develop` の現行 R4-R3、R4-R5、R4-R6、R2J-R3 と関連テストを確認する。R4-R6 の実行ログは限定 pytest 19 PASS、`MIDDLE_CARDINALITY=INFERRED`、`CARDINALITY=4`、`NEW_GIVEN=0` である。最新 `develop` はログ HEAD `19fe298c` から R4-R6 の監査ファイルを含む1コミット先にある。

## 数学的推論

1. 先行出典付き群構造 $\pi_5^2\cong\mathbb Z/2\{\eta_2^3\}$ から生成元 $\eta_2^3\neq0$。
2. R2J-R3 で実際に推論済みの $E:\pi_5^2\to\pi_6^3$ の単射性を用い、$E(\eta_2^3)\neq0$。
3. R4-R3 の実際の推論済み $2\nu'=E(\eta_2^3)$ を用い、$2\nu'\neq0$。
4. R4-R6 の実際の推論済み $|\pi_6^3|=4$ と Lagrange の定理から $\nu'$ の位数は4を割る。$2\nu'\neq0$ より位数1・2ではないので、$\operatorname{ord}(\nu')=4$。

## 変更対象・追加位置

既存の本番ファイル、テスト、ドキュメントは変更しない。次の新規ディレクトリをリポジトリ直下に追加する。

- `phase171_r2j_r4_r7_nonzero_nu_order/source.py`: 新規 `NonZeroGroupElement`、`FiniteElementOrder` クラス、新規 `nonzero_cyclic_generator_image()`、`injected_generator_nonzero_rule()`、`nonzero_double_from_equality()`、`inferred_nonzero_double_rule()`、`order_four_from_nonzero_double()`、`inferred_order_four_rule()`。一般規則だけを置く。
- `phase171_r2j_r4_r7_nonzero_nu_order/audit.py`: 新規 `_git()`、`_infer()`、`build_nonzero_nu_order_proof()`、`main()`。既存の証明木を再構成して接続する。
- `phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py`: 12件の新規テスト、型・不正 `GIVEN`・前提並べ替え・実データ再構成を検査。
- `run.ps1`、`README.md`、`CODE_FULL_JA.md`、この文書、空の `__init__.py` を新規追加。

## Trust Boundary（証明の信頼境界）

- 先行する Proposition 5.6 の $\pi_5^2$ 群結果は、新規 `GIVEN` を作らず、R4-R6 の実際の出典付き葉を再利用する。
- $E$ の単射性、$2\nu'=E(\eta_2^3)$、群位数4は、必ず実際の `INFERENCE` の祖先から受け取る。
- 登録済み生成元の同一性は、`HyoujiGen.csv` による構造的照合、または完全な型一致に限る。表示上の名前の一致のみでは認定しない。
- 新しい命題を `GIVEN` として登録しない。出典を欠く要素の非零性、群の位数、$\pi_6^3$ の完成結果を仮定しない。
- すべての祖先 `GIVEN` は、現行引用境界より前の一意な `FIXED_STATEMENT` と照合する。
- R4-R7 は $\operatorname{ord}(\nu')=4$ まで。$\pi_6^3\cong\mathbb Z/4\{\nu'\}$ の最終的な群構造 `Relation` の作成は R4-R8 に残す。

## テスト・完了条件

`python -B -m pytest -q -p no:cacheprovider phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py` を実行する。合計31件を予定する。全体 pytest は Phase 171 完了時のみ実行する。

`DOUBLE_NONZERO=INFERRED`、`NU_PRIME_ORDER_FOUR=INFERRED`、`NEW_GIVEN=0`、`PI63_PROVEN=False`、`RUN=PASS` を実環境で確認するまでは完了扱いにしない。Git 追跡ファイルが実行前後で変化しないことを確認する。
```

## 新規 __init__.py

```python
"""Phase 171 R2J-R4-R7: source-bound nonzero double and order-four proof."""
```

## 新規 tests/__init__.py

```python
"""Focused R2J-R4-R7 checks."""
```

## 実行（Windows PowerShell）

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R7_NONZERO_ORDER.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r7_nonzero_nu_order\run.ps1"
git status -sb
git diff --stat
```

## 完了条件と次段階

限定 pytest 31件 PASS、`DOUBLE_NONZERO=INFERRED`、`NU_PRIME_ORDER_FOUR=INFERRED`、`NEW_GIVEN=0`、`PI63_PROVEN=False` と Git 追跡ファイルに変更がないこと。次の R4-R8 で位数4の元から群の巡回表示を型付き結論として構築する。全体 pytest は Phase 171 の最終段階まで実行しない。
