# Phase 170 R3-R7（改訂）— 置換用コード全文

## 変更対象

- `phase168_r2_toda52_transport.py`：関数 `expand_toda52_finite_cyclic_goal()` の置換。既存処理を `_expand_toda52_screened_cyclic_goal()` にそのまま移動。新規関数 `_eta2_inverse_image()`, `_toda52_group_presentation_matches()`, `_toda52_ordered_db_rule()` は旧経路の後に追加。
- トップレベル import：変更なし。新規ファイルは R3-R7 実行用フォルダの `runner.py`, `verify.py`, `run.ps1`, 限定テストのみ。
- 既存のテストファイルは変更しない。DB、Trust Boundary、Web Renderer も変更しない。

## 本体ファイル全文（import 含む）

```python
"""Backward transport along the cited Toda (5.2) eta_2 composition isomorphism.

Every proposed transport needs a separately screened source group proof and
Toda (5.2). Neither DB goals nor generator names are accepted as GIVEN facts.
The established i=4 proposal is retained unchanged.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from proof import InferenceRule, LiteratureReference, PremisePattern, Relation, RelationType


def _eta2_composition_parts(generator: object):
    if not isinstance(generator, Composition):
        return None
    left, right = generator.left, generator.right
    if not isinstance(left, HomotopyElement) or not isinstance(right, HomotopyElement):
        return None
    if (left.dimension != 2 or left.source != 3 or left.target != 2
            or left.generator != GeneratorSymbol(family="η", index=2)):
        return None
    if (right.dimension != 3 or right.source != 4 or right.target != 3
            or right.generator != GeneratorSymbol(family="η", index=3)):
        return None
    return right


def _toda52_rule(expected: Relation) -> InferenceRule:
    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        source, theorem = (step.conclusion for step in premises)
        if not isinstance(theorem, Toda52UniversalStatement):
            return False
        if (theorem.minimum_i != 3 or theorem.variable != "i"
                or theorem.map_formula != "alpha -> eta_2 o alpha"
                or theorem.source_group != "pi_i^3" or theorem.target_group != "pi_i^2"):
            return False
        if (not isinstance(source, Relation)
                or source.relation_type is not RelationType.EQUALITY
                or source.lhs != TodaPrimaryGroup(4, 3)
                or not isinstance(source.rhs, FiniteCyclicGroup)
                or source.rhs.order != 2):
            return False
        parts = _eta2_composition_parts(expected.rhs.generator)
        if parts is None:
            return False
        eta3 = source.rhs.generator
        return (isinstance(eta3, HomotopyElement)
                and eta3.dimension == parts.dimension
                and eta3.source == parts.source
                and eta3.target == parts.target
                and eta3.generator == parts.generator
                and expected.lhs == TodaPrimaryGroup(4, 2))

    def conclusion(premises):
        return expected

    return InferenceRule(
        name="Toda (5.2) finite-cyclic eta2 composition transport",
        description="Transport a proved cyclic structure along the cited (5.2) isomorphism at i=4.",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(statement_type=Toda52UniversalStatement),
        ),
        conclusion_builder=conclusion,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda (5.2)", locator="(5.2)",
        ),
    )


def _toda52_theorem_is_exact(item: object) -> bool:
    return (isinstance(item, Toda52UniversalStatement)
            and item.minimum_i == 3
            and item.map_formula == "alpha -> eta_2 o alpha"
            and item.source_group == "pi_i^3"
            and item.target_group == "pi_i^2"
            and item.variable == "i")


def _typed_source_and_target(expression: object) -> tuple[int, int] | None:
    """Check concrete composite types without guessing from printed names."""
    if isinstance(expression, HomotopyElement):
        if (type(expression.source) is int and type(expression.target) is int
                and expression.source > expression.target >= 2):
            return expression.source, expression.target
        return None
    if isinstance(expression, Composition):
        left = _typed_source_and_target(expression.left)
        right = _typed_source_and_target(expression.right)
        if left is None or right is None or right[1] != left[0]:
            return None
        return right[0], left[1]
    return None


def _eta2_right_generator(goal: Relation) -> object | None:
    """Return a typed map S^m -> S^3 whose eta_2 composition is the target."""
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        return None
    candidate = goal.rhs.generator
    if not isinstance(candidate, Composition):
        return None
    eta2 = candidate.left
    if (not isinstance(eta2, HomotopyElement)
            or type(eta2.dimension) is not int
            or eta2.dimension != 2 or eta2.source != 3 or eta2.target != 2
            or eta2.generator != GeneratorSymbol(family="η", index=2)):
        return None
    right = candidate.right
    if _typed_source_and_target(right) != (goal.lhs.group_dimension, 3):
        return None
    return right


def _toda52_general_rule(expected: Relation, source: Relation) -> InferenceRule:
    """Use only a screened, exact source and the cited universal theorem."""
    if (not isinstance(expected, Relation) or not isinstance(source, Relation)
            or expected.relation_type is not RelationType.EQUALITY
            or source.relation_type is not RelationType.EQUALITY
            or not isinstance(expected.rhs, FiniteCyclicGroup)
            or not isinstance(source.rhs, FiniteCyclicGroup)
            or expected.rhs.order != source.rhs.order
            or expected.lhs.sphere_dimension != 2
            or source.lhs != TodaPrimaryGroup(expected.lhs.group_dimension, 3)):
        raise ValueError("invalid (5.2) transport source or target")

    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        first, second = (step.conclusion for step in premises)
        if first != source or not _toda52_theorem_is_exact(second):
            return False
        right = _eta2_right_generator(expected)
        if right is None:
            return False
        from phase168_r2_8_3_generator_identity.identity import (
            same_registered_group_presentation,
        )
        typed_right = FiniteCyclicGroup(order=expected.rhs.order, generator=right)
        return (typed_right == source.rhs
                or same_registered_group_presentation(typed_right, source.rhs))

    return InferenceRule(
        name="Toda (5.2) typed finite-cyclic composition transport",
        description="Transport a separately proved cyclic group along the cited (5.2) isomorphism.",
        premise_patterns=(
            PremisePattern(statement_type=Relation, statement_pattern=source),
            PremisePattern(statement_type=Toda52UniversalStatement),
        ),
        conclusion_builder=lambda premises: expected,
        match_guard=guard,
        literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)"),
    )


def _expand_toda52_screened_cyclic_goal(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Screened (5.2) finite-cyclic transport at every well-typed m>=4.

    i=4 retains its original route. New m>=5 proposals require an exact,
    separately screened prior Relation for pi_m^3; a DB result is never a leaf.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and isinstance(goal.lhs, TodaPrimaryGroup)
            and type(goal.lhs.group_dimension) is int
            and goal.lhs.sphere_dimension == 2
            and goal.lhs.group_dimension >= 4
            and isinstance(goal.rhs, FiniteCyclicGroup)
            and type(goal.rhs.order) is int
            and goal.rhs.order >= 2):
        return ()
    accepted = tuple(item for item in available if _toda52_theorem_is_exact(item))
    if not accepted:
        return ()
    m = goal.lhs.group_dimension
    if m == 4:
        if goal.rhs.order != 2:
            return ()
        eta3 = _eta2_composition_parts(goal.rhs.generator)
        if eta3 is None:
            return ()
        source = Relation(
            lhs=TodaPrimaryGroup(4, 3),
            rhs=FiniteCyclicGroup(
                order=2,
                generator=HomotopyElement(
                    name="η_3", dimension=eta3.dimension,
                    source=eta3.source, target=eta3.target,
                    generator=eta3.generator,
                ),
            ),
            relation_type=RelationType.EQUALITY,
        )
        return tuple(GoalExpansion(_toda52_rule(goal), (source, item)) for item in accepted)

    right = _eta2_right_generator(goal)
    if right is None:
        return ()
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    target_source = TodaPrimaryGroup(m, 3)
    right_presentation = FiniteCyclicGroup(order=goal.rhs.order, generator=right)
    sources = []
    for item in available:
        if (not isinstance(item, Relation)
                or item.relation_type is not RelationType.EQUALITY
                or item.lhs != target_source
                or not isinstance(item.rhs, FiniteCyclicGroup)
                or item.rhs.order != goal.rhs.order):
            continue
        if (item.rhs != right_presentation
                and not same_registered_group_presentation(item.rhs, right_presentation)):
            continue
        if item not in sources:
            sources.append(item)
    return tuple(
        GoalExpansion(_toda52_general_rule(goal, source), (source, theorem))
        for source in sources
        for theorem in accepted
    )


def _eta2_inverse_image(generator: object, dimension: int) -> object | None:
    """Recognize a typed eta_2 image, including additive presentations.

    This is generator correspondence, not a group equality obtained from DB.
    """
    from expression import IteratedSuspension, Multiple, Sum, Suspension

    if isinstance(generator, Composition):
        eta, right = generator.left, generator.right
        if (not isinstance(eta, HomotopyElement)
                or eta.dimension != 2 or eta.source != 3 or eta.target != 2
                or eta.generator != GeneratorSymbol(family="η", index=2)):
            return None

        def endpoints(value: object) -> tuple[int, int] | None:
            if isinstance(value, (HomotopyElement, Suspension, IteratedSuspension)):
                source, target = value.source, value.target
                if type(source) is int and type(target) is int and source > target >= 2:
                    return source, target
                return None
            if isinstance(value, Composition):
                left, other = endpoints(value.left), endpoints(value.right)
                if left is None or other is None or left[0] != other[1]:
                    return None
                return other[0], left[1]
            return None

        return right if endpoints(right) == (dimension, 3) else None
    if isinstance(generator, Sum):
        left = _eta2_inverse_image(generator.left, dimension)
        right = _eta2_inverse_image(generator.right, dimension)
        if left is not None and right is not None:
            return Sum(left, right)
    if isinstance(generator, Multiple):
        if type(generator.coefficient) is int:
            right = _eta2_inverse_image(generator.expression, dimension)
            if right is not None:
                return Multiple(generator.coefficient, right)
    return None


def _toda52_group_presentation_matches(source: object, target: object) -> bool:
    """Check generator-wise eta_2 image for cyclic, direct-sum or zero groups."""
    from homotopy_groups import (
        DirectSumGroup, FreeCyclicGroup, TodaPrimaryGroupZeroStatement,
    )
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )

    def match_component(original: object, result: object, dimension: int) -> bool:
        if type(original) is not type(result):
            return False
        if not isinstance(original, (FiniteCyclicGroup, FreeCyclicGroup)):
            return False
        if isinstance(original, FiniteCyclicGroup) and original.order != result.order:
            return False
        right = _eta2_inverse_image(result.generator, dimension)
        if right is None:
            return False
        if original.generator == right:
            return True
        equivalent = (FiniteCyclicGroup(original.order, right)
                      if isinstance(original, FiniteCyclicGroup)
                      else FreeCyclicGroup(right))
        return same_registered_group_presentation(original, equivalent)

    if isinstance(source, TodaPrimaryGroupZeroStatement):
        return (isinstance(target, TodaPrimaryGroupZeroStatement)
                and target.group == TodaPrimaryGroup(source.group.group_dimension, 2)
                and source.group.sphere_dimension == 3)
    if not (isinstance(source, Relation) and isinstance(target, Relation)
            and source.relation_type is RelationType.EQUALITY
            and target.relation_type is RelationType.EQUALITY
            and isinstance(source.lhs, TodaPrimaryGroup)
            and isinstance(target.lhs, TodaPrimaryGroup)
            and source.lhs == TodaPrimaryGroup(target.lhs.group_dimension, 3)
            and target.lhs.sphere_dimension == 2):
        return False
    dimension = target.lhs.group_dimension
    if isinstance(source.rhs, (FiniteCyclicGroup, FreeCyclicGroup)):
        return match_component(source.rhs, target.rhs, dimension)
    if isinstance(source.rhs, DirectSumGroup) and isinstance(target.rhs, DirectSumGroup):
        remaining = list(source.rhs.summands)
        if len(remaining) != len(target.rhs.summands) or not remaining:
            return False
        for target_component in target.rhs.summands:
            matched = next((index for index, component in enumerate(remaining)
                            if match_component(component, target_component, dimension)), None)
            if matched is None:
                return False
            remaining.pop(matched)
        return not remaining
    return False


def _toda52_ordered_db_rule(expected: object, source: object) -> InferenceRule:
    """A verified earlier DB statement and cited (5.2) imply a typed image."""
    if not _toda52_group_presentation_matches(source, expected):
        raise ValueError("unmatched eta_2 image of earlier group generators")

    def guard(premises, bindings):
        if len(premises) != 2:
            return False
        first, second = (item.conclusion for item in premises)
        return (first == source
                and _toda52_theorem_is_exact(second)
                and _toda52_group_presentation_matches(source, expected))

    return InferenceRule(
        name="Toda (5.2) transport from an admitted earlier typed group",
        description="Specialize (5.2) with a separately admitted group premise.",
        premise_patterns=(
            PremisePattern(statement_type=type(source), statement_pattern=source),
            PremisePattern(statement_type=Toda52UniversalStatement),
        ),
        conclusion_pattern=expected,
        match_guard=guard,
        literature_reference=LiteratureReference(label="Toda (5.2)", locator="(5.2)"),
    )


def expand_toda52_finite_cyclic_goal(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Common Toda (5.2) route for n=2: cyclic, free, zero and direct sum.

    The public function name is retained for API compatibility. The existing
    vetted finite-cyclic route has priority. Every DB source becomes a subgoal:
    the ordinary proof engine must admit it via R10E4 strict (k,n) order,
    and the public trust boundary independently verifies it against sphere.csv.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    established = _expand_toda52_screened_cyclic_goal(goal, available)
    if established:
        return established
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, group_coordinates, precedes_db_goal,
    )
    target = group_coordinates(goal)
    if target is None:
        return ()
    n, k = target
    dimension = n + k
    if n != 2 or dimension < 6:
        return ()
    if not isinstance(goal, (Relation, TodaPrimaryGroupZeroStatement)):
        return ()
    if not (isinstance(goal, TodaPrimaryGroupZeroStatement)
            or (goal.relation_type is RelationType.EQUALITY
                and isinstance(goal.lhs, TodaPrimaryGroup))):
        return ()
    theorem_candidates = tuple(item for item in available if _toda52_theorem_is_exact(item))
    if not theorem_candidates:
        return ()
    source_n, source_k = 3, dimension - 3
    if not precedes_db_goal(source_n, source_k, n, k):
        return ()
    source = exact_prior_database_result(source_n, source_k)
    if source is None or not _toda52_group_presentation_matches(source, goal):
        return ()
    return tuple(GoalExpansion(
        _toda52_ordered_db_rule(goal, source), (source, theorem),
    ) for theorem in theorem_candidates)

```

## tests/test_ordered_db_toda52.py — 全文

```python
"""Focused real-repository checks for generalized Toda (5.2) and DB precedence."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, group_coordinates, precedes_db_goal,
)
from phase168_r2_toda52_transport import (
    _toda52_group_presentation_matches, expand_toda52_finite_cyclic_goal,
)
from proof import Relation, RelationType


def _db_goal(k: int) -> object:
    zeros = database_zero_group_goal_candidates(n=2, k=k)
    if zeros:
        assert len(zeros) == 1
        return zeros[0]
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=k)
    assert len(goals) == 1
    return goals[0]


@pytest.mark.parametrize("k", [4, 6, 7, 8, 9, 10, 14])
def test_r3r7_db_source_precedes_and_is_a_typed_eta2_presentation(k: int) -> None:
    target = _db_goal(k)
    dimension = k + 2
    source = exact_prior_database_result(3, dimension - 3)
    assert source is not None
    assert group_coordinates(source) == (3, k - 1)
    assert precedes_db_goal(3, k - 1, 2, k)
    assert _toda52_group_presentation_matches(source, target)
    assert admitted_db_step(source, proof_target=target) is not None


@pytest.mark.parametrize("k", [4, 6, 7, 8, 9, 10, 14])
def test_r3r7_inference_requests_db_source_and_cited_theorem(k: int) -> None:
    target = _db_goal(k)
    theorem = Toda52UniversalStatement()
    proposals = expand_toda52_finite_cyclic_goal(target, (theorem,))
    assert len(proposals) == 1
    source, citation = proposals[0].subgoals
    assert group_coordinates(source) == (3, k - 1)
    assert citation == theorem
    assert proposals[0].rule.match_guard(
        (SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem)),
        {},
    )
    assert expand_toda52_finite_cyclic_goal(target, ()) == ()
    assert not proposals[0].rule.match_guard(
        (SimpleNamespace(conclusion=target), SimpleNamespace(conclusion=theorem)),
        {},
    )


def test_r3r7_does_not_create_source_as_an_unproved_root() -> None:
    target = _db_goal(6)
    assert isinstance(target, Relation)
    assert target.lhs == TodaPrimaryGroup(8, 2)
    wrong = Relation(
        target.lhs,
        FiniteCyclicGroup(7, target.rhs.generator),
        RelationType.EQUALITY,
    )
    assert expand_toda52_finite_cyclic_goal(
        wrong, (Toda52UniversalStatement(),),
    ) == ()


def test_r3r7_zero_is_typed_without_generator_invention() -> None:
    target = _db_goal(7)
    assert isinstance(target, TodaPrimaryGroupZeroStatement)
    source = exact_prior_database_result(3, 6)
    assert isinstance(source, TodaPrimaryGroupZeroStatement)
    assert source.group == TodaPrimaryGroup(9, 3)
    assert _toda52_group_presentation_matches(source, target)

```

## tests/test_offline_contract.py — 全文

```python
"""Offline integrity checks; these require no network or project installation."""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parent
SOURCE = PACKAGE / "replacement" / "phase168_r2_toda52_transport.py"
ORIGINAL_SHA256 = "52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe"


def test_r3r7_complete_source_is_compilable_and_contains_all_functions() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    compile(text, str(SOURCE), "exec")
    tree = ast.parse(text)
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert functions.count("expand_toda52_finite_cyclic_goal") == 1
    for name in (
        "_expand_toda52_screened_cyclic_goal",
        "_eta2_inverse_image",
        "_toda52_group_presentation_matches",
        "_toda52_ordered_db_rule",
    ):
        assert functions.count(name) == 1


def test_r3r7_existing_math_is_not_rewritten() -> None:
    original = (PACKAGE / "baseline" / "phase168_r2_toda52_transport.py").read_bytes()
    assert sha256(original).hexdigest() == ORIGINAL_SHA256
    after = SOURCE.read_text(encoding="utf-8")
    before = original.decode("utf-8")
    assert after.startswith(before.replace(
        "def expand_toda52_finite_cyclic_goal(",
        "def _expand_toda52_screened_cyclic_goal(",
        1,
    ).rstrip())


def test_r3r7_script_is_complete_and_rollback_is_explicit() -> None:
    code = (PACKAGE / "runner.py").read_text(encoding="utf-8")
    tree = ast.parse(code)
    assert any(isinstance(node, ast.FunctionDef) and node.name == "run" for node in tree.body)
    assert "target.write_bytes(original)" in code
    assert "PHASE170_R3R7_ROLLBACK" in code
    assert "git(root, \"rev-parse\"" in code
    assert "FULL_PYTEST=False" in code


def test_r3r7_no_unrelated_production_replacement() -> None:
    replacements = list((PACKAGE / "replacement").rglob("*.py"))
    assert [file.name for file in replacements] == ["phase168_r2_toda52_transport.py"]


def test_r3r7_n2_degrees_require_earlier_db_and_original_theorem() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    assert "precedes_db_goal(source_n, source_k, n, k)" in text
    assert "exact_prior_database_result(source_n, source_k)" in text
    assert "_toda52_theorem_is_exact(item)" in text
    assert "dimension < 6" in text
    assert "source, theorem" in text

```

## tests/test_algorithm_isolated.py — 全文

```python
"""Exercise actual new matching functions with locally constructed typed examples."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys
from types import ModuleType

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "replacement" / "phase168_r2_toda52_transport.py"


@dataclass(frozen=True)
class Symbol:
    family: str
    index: int | None = None


@dataclass(frozen=True)
class Element:
    name: str
    dimension: int
    source: int
    target: int
    generator: Symbol


@dataclass(frozen=True)
class Composition:
    left: object
    right: object


@dataclass(frozen=True)
class Sum:
    left: object
    right: object


@dataclass(frozen=True)
class Multiple:
    coefficient: int
    expression: object


@dataclass(frozen=True)
class Suspension:
    expression: object

    @property
    def source(self):
        return self.expression.source + 1

    @property
    def target(self):
        return self.expression.target + 1


@dataclass(frozen=True)
class IteratedSuspension:
    expression: object
    exponent: int

    @property
    def source(self):
        return self.expression.source + self.exponent

    @property
    def target(self):
        return self.expression.target + self.exponent


@dataclass(frozen=True)
class Group:
    group_dimension: int
    sphere_dimension: int


@dataclass(frozen=True)
class Zero:
    group: Group


@dataclass(frozen=True)
class Finite:
    order: int
    generator: object


@dataclass(frozen=True)
class Free:
    generator: object


@dataclass(frozen=True)
class DirectSum:
    summands: tuple


class Equality(Enum):
    EQUALITY = "equality"


@dataclass(frozen=True)
class Relation:
    lhs: Group
    rhs: object
    relation_type: Equality = Equality.EQUALITY


def _load_matcher(monkeypatch):
    expr = ModuleType("expression")
    expr.Composition = Composition
    expr.HomotopyElement = Element
    expr.GeneratorSymbol = Symbol
    expr.Multiple = Multiple
    expr.Sum = Sum
    expr.Suspension = Suspension
    expr.IteratedSuspension = IteratedSuspension
    groups = ModuleType("homotopy_groups")
    groups.DirectSumGroup = DirectSum
    groups.FreeCyclicGroup = Free
    groups.FiniteCyclicGroup = Finite
    groups.TodaPrimaryGroupZeroStatement = Zero
    alias = ModuleType("phase168_r2_8_3_generator_identity.identity")
    alias.same_registered_group_presentation = lambda left, right: False
    monkeypatch.setitem(sys.modules, "expression", expr)
    monkeypatch.setitem(sys.modules, "homotopy_groups", groups)
    monkeypatch.setitem(sys.modules, "phase168_r2_8_3_generator_identity.identity", alias)
    full = ast.parse(SOURCE.read_text(encoding="utf-8"))
    methods = [n for n in full.body if isinstance(n, ast.FunctionDef) and n.name in (
        "_eta2_inverse_image", "_toda52_group_presentation_matches",
    )]
    result = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods, type_ignores=[])),
                 str(SOURCE), "exec"), {
        "Composition": Composition, "HomotopyElement": Element,
        "GeneratorSymbol": Symbol, "FiniteCyclicGroup": Finite,
        "TodaPrimaryGroup": Group, "Relation": Relation,
        "RelationType": Equality,
    }, result)
    # Function globals are separate from result due to exec globals/locals.
    globs = {
        "Composition": Composition, "HomotopyElement": Element,
        "GeneratorSymbol": Symbol, "FiniteCyclicGroup": Finite,
        "TodaPrimaryGroup": Group, "Relation": Relation,
        "RelationType": Equality,
    }
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods, type_ignores=[])),
                 str(SOURCE), "exec"), globs)
    return globs["_toda52_group_presentation_matches"]


def _eta2():
    return Element("η₂", 2, 3, 2, Symbol("η", 2))


def _element(name: str, m: int):
    return Element(name, 3, m, 3, Symbol(name))


def test_isolated_finite_cyclic_and_rejects_order_mismatch(monkeypatch):
    matches = _load_matcher(monkeypatch)
    source = _element("ν′", 6)
    left = Relation(Group(6, 3), Finite(4, source))
    target = Relation(Group(6, 2), Finite(4, Composition(_eta2(), source)))
    assert matches(left, target)
    assert not matches(left, Relation(Group(6, 2), Finite(2, Composition(_eta2(), source))))


def test_isolated_zero_and_rejects_wrong_degree(monkeypatch):
    matches = _load_matcher(monkeypatch)
    assert matches(Zero(Group(9, 3)), Zero(Group(9, 2)))
    assert not matches(Zero(Group(9, 3)), Zero(Group(10, 2)))


def test_isolated_direct_sum_permuted_and_additive_generators(monkeypatch):
    matches = _load_matcher(monkeypatch)
    a, b = _element("a", 12), _element("b", 12)
    source = Relation(Group(12, 3), DirectSum((Finite(2, a), Finite(4, b))))
    target = Relation(Group(12, 2), DirectSum((
        Finite(4, Composition(_eta2(), b)),
        Finite(2, Composition(_eta2(), a)),
    )))
    assert matches(source, target)
    added = Relation(Group(12, 3), Finite(2, Sum(a, b)))
    sum_image = Relation(Group(12, 2), Finite(2, Sum(
        Composition(_eta2(), a), Composition(_eta2(), b),
    )))
    assert matches(added, sum_image)


def test_isolated_free_cyclic_and_multiple(monkeypatch):
    matches = _load_matcher(monkeypatch)
    a = _element("a", 17)
    source = Relation(Group(17, 3), Free(Multiple(2, a)))
    target = Relation(Group(17, 2), Free(Multiple(2, Composition(_eta2(), a))))
    assert matches(source, target)

```

## runner.py — 全文

```python
"""Single-file guarded replacement with strict preflight and rollback."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

REVIEWED_HEAD = "84a9d8ad6110ed82b80bdeb7e9a0c5a361214de0"
REVIEWED_BLOB = "b3e104857e3a8129fb01df65ce3a38ff188ecd1f"
REVIEWED_SHA256 = "52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe"
TARGET = "phase168_r2_toda52_transport.py"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if process.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {process.stderr.strip()}")
    return process.stdout.strip()


def preflight(root: Path) -> dict:
    branch, head = git(root, "branch", "--show-current"), git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch} {head}")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("tracked worktree/index changes found; refusing to overwrite")
    if git(root, "rev-parse", f"HEAD:{TARGET}") != REVIEWED_BLOB:
        raise RuntimeError("reviewed source blob is different")
    target = root / TARGET
    if not target.is_file() or sha256(target.read_bytes()).hexdigest() != REVIEWED_SHA256:
        raise RuntimeError("on-disk source is not the reviewed Phase 170 R3-R5 implementation")
    for name in (
        "phase170_r3_r6_prop58_source.py",
        "phase169_r10e4_ordered_db_prior/db_prior.py",
        "phase168_r3_41p13_trust_boundary/verification.py",
    ):
        if not (root / name).is_file():
            raise RuntimeError(f"required reviewed dependency missing: {name}")
    return {"head": head, "branch": branch, "reviewed_blob": REVIEWED_BLOB}


def execute(root: Path, output: Path, name: str, command: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    process = subprocess.run(command, cwd=root, env=env, text=True,
                             encoding="utf-8", errors="replace",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (output / f"{name}.log").write_text(process.stdout, encoding="utf-8")
    print(process.stdout, flush=True)
    print(f"PHASE170_R3R7_{name.upper()}_EXIT={process.returncode}", flush=True)
    return process.returncode


def run(root: Path, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery" / (
        "phase170_r3_r7_db_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R7_MODE=GUARDED_TODA52_ORDERED_DB", flush=True)
    print(f"PHASE170_R3R7_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R7 revised", "mode": "DRY_RUN" if dry_run else "ONE_FILE_GUARDED_PATCH"}
    target = root / TARGET
    changed = False
    passed = False
    original = None
    try:
        report.update(preflight(root))
        original = target.read_bytes()
        replacement = (package / "replacement" / TARGET).read_bytes()
        compile(replacement, TARGET, "exec")
        (output / "phase168_r2_toda52_transport.py.before").write_bytes(original)
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
            print("PHASE170_R3R7_DRY_RUN=PASS", flush=True)
            passed = True
            return 0
        target.write_bytes(replacement)
        changed = True
        focused = [
            package / "tests" / "test_ordered_db_toda52.py",
            root / "phase168_r2_toda52_transport" / "tests" / "test_phase168_r2_toda52_transport.py",
            root / "phase170_r3_r5_toda52_cyclic_generalization" / "tests" / "test_phase170_r3_r5_toda52_cyclic.py",
            root / "phase169_r10e4_ordered_db_prior" / "tests" / "test_r10e4_ordered_db_prior.py",
            root / "phase170_r3_r6_prop58_pi73_source" / "tests" / "test_phase170_r3_r6_source.py",
        ]
        missing = [str(p) for p in focused if not p.is_file()]
        if missing:
            raise RuntimeError(f"focused test file missing: {missing!r}")
        status = execute(root, output, "focused_pytest", [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", *(str(path) for path in focused),
        ])
        if status:
            raise RuntimeError(f"focused pytest failed: {status}")
        status = execute(root, output, "active_web", [sys.executable, "-B", str(package / "verify.py")])
        if status:
            raise RuntimeError(f"active Web verification failed: {status}")
        report["result"] = "PATCHED_AND_WEB_VERIFIED"
        passed = True
        print("PHASE170_R3R7_RESULT=PATCHED_AND_WEB_VERIFIED", flush=True)
        print("PHASE170_R3R7_FULL_PYTEST=False", flush=True)
        return 0
    except Exception as error:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(error)
        print(f"PHASE170_R3R7_REFUSED={type(error).__name__}: {error}", flush=True)
        return 2
    finally:
        if changed and not passed and original is not None:
            target.write_bytes(original)
            print("PHASE170_R3R7_ROLLBACK=RESTORED_R3R6_STATE", flush=True)
        report_path = output / "result.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"PHASE170_R3R7_REPORT={report_path}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

```

## verify.py — 全文

```python
"""Check actual Web proof closure for every requested low-range n=2 structure."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


TARGETS = (3, 4, 5, 6, 7, 8, 9, 10, 14)


def check(k: int) -> bool:
    label = f"pi_{k + 2}^2"
    result = search_group_from_registered_goal(n=2, k=k)
    print(f"PHASE170_R3R7_{label}_STATUS={result.status}", flush=True)
    print(f"PHASE170_R3R7_{label}_PROVEN_STEPS={len(result.proven_steps)}", flush=True)
    print(f"PHASE170_R3R7_{label}_OPEN_GOALS={len(result.open_goals)}", flush=True)
    if result.status is not ProofSearchStatus.COMPLETE or not result.proven_steps or result.open_goals:
        print(f"PHASE170_R3R7_{label}_DIAGNOSTICS={result.diagnostics!r}", flush=True)
        return False
    view = build_standard_web_group_proof_view(
        n=2, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    okay = (
        view.key == "generic-complete-proof"
        and not view.partial_result
        and bool(view.steps)
        and bool(view.rendered_lines)
    )
    print(f"PHASE170_R3R7_{label}_WEB_KEY={view.key}", flush=True)
    print(f"PHASE170_R3R7_{label}_WEB_PARTIAL={view.partial_result}", flush=True)
    print(f"PHASE170_R3R7_{label}={'COMPLETE_AND_WEB_VERIFIED' if okay else 'WEB_FAILED'}", flush=True)
    return okay


def main() -> int:
    failures = tuple(k for k in TARGETS if not check(k))
    if failures:
        print(f"PHASE170_R3R7_UNFINISHED_K={failures!r}", flush=True)
        return 2
    print("PHASE170_R3R7_ALL_TARGETS_COMPLETE_AND_WEB_VERIFIED=True", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## run.ps1 — 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Env:PYTHONPATH = $Root
$ArgList = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root)
if ($DryRun) { $ArgList += '--dry-run' }
& python @ArgList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

```

## 実施する pytest

本実行では新規テスト・既存 R3-R5/R3-R6/R10E4 の限定 pytest のみ実施する。全体 pytest は Phase 170 の終わりに行う。

## 完了条件

対象群で `ProofSearchStatus.COMPLETE`、未解決 Goal が0、Web で `generic-complete-proof`、Trust Boundary 通過。失敗時は置換した本体1ファイルをバックアップから復元する。

## 次 Phase との境界

対応不能な高次生成元、DB の構造変換が不明瞭なものを勝手に証明済みとする処理や、Proposition 5.9 の個別登録は含まない。
