# Phase 170 R3-R9 変更コード全文

## 対象ファイル・関数

- `phase168_r2_toda52_transport.py`: `_toda52_cited_generator_equality`（`_toda52_group_presentation_matches` の直前に追加）、`_toda52_group_presentation_matches`、`_toda52_ordered_db_rule`、`expand_toda52_finite_cyclic_goal`。
- `phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py`: import 全部および `connect_explicit_literature_components`。
- 新規 `phase170_r3_r9_toda712_cited_rewrite/source712.py`: モジュール全体、関数 `_verified_adopted_source`、`verified_toda712_generator_equality`、`register_cited_toda712_generator_equality`。
- 新規テスト `tests/test_toda712_rewrite.py`。

置き換え用の本体ファイルは ZIP の `replacement/` に、追加モジュールと全テストも ZIP に収録している。

## phase168_r2_toda52_transport.py

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


def _toda52_cited_generator_equality(
    left: object, right: object, equality: object,
) -> bool:
    """One typed equality, cited as an independent proof premise.

    No name matching, CSV equivalence or inferred relation authorizes this.
    The relation must equate well-typed representatives of the same group.
    """
    if (not isinstance(equality, Relation)
            or equality.relation_type is not RelationType.EQUALITY):
        return False
    typed_left = _typed_source_and_target(left)
    if (typed_left is None or typed_left != _typed_source_and_target(right)
            or typed_left != _typed_source_and_target(equality.lhs)
            or typed_left != _typed_source_and_target(equality.rhs)):
        return False
    return ((left == equality.lhs and right == equality.rhs)
            or (left == equality.rhs and right == equality.lhs))


def _toda52_group_presentation_matches(
    source: object, target: object, *, equality: object | None = None,
) -> bool:
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
        if (equality is not None
                and _toda52_cited_generator_equality(original.generator, right, equality)):
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


def _toda52_ordered_db_rule(
    expected: object, source: object, *, equality: object | None = None,
) -> InferenceRule:
    """A verified earlier DB statement and cited (5.2), plus a cited equality if needed."""
    if not _toda52_group_presentation_matches(source, expected, equality=equality):
        raise ValueError("unmatched eta_2 image of earlier group generators")
    if (equality is not None
            and (not isinstance(equality, Relation)
                 or equality.relation_type is not RelationType.EQUALITY)):
        raise ValueError("rewrite premise is not a typed equality")

    def guard(premises, bindings):
        expected_count = 3 if equality is not None else 2
        if len(premises) != expected_count:
            return False
        first, second = (item.conclusion for item in premises[:2])
        if first != source or not _toda52_theorem_is_exact(second):
            return False
        if equality is not None and premises[2].conclusion != equality:
            return False
        return _toda52_group_presentation_matches(source, expected, equality=equality)

    patterns = (
        PremisePattern(statement_type=type(source), statement_pattern=source),
        PremisePattern(statement_type=Toda52UniversalStatement),
    )
    if equality is not None:
        patterns += (PremisePattern(statement_type=Relation, statement_pattern=equality),)
    return InferenceRule(
        name="Toda (5.2) transport from an admitted earlier typed group",
        description="Specialize (5.2) with an admitted group and any required cited equality.",
        premise_patterns=patterns,
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
    if source is None:
        return ()
    if _toda52_group_presentation_matches(source, goal):
        return tuple(GoalExpansion(
            _toda52_ordered_db_rule(goal, source), (source, theorem),
        ) for theorem in theorem_candidates)
    # Require a separately screened, individually cited equality. A DB
    # relation table or an uncited generator-name alias is not an axiom.
    cited_equalities = tuple(item for item in available
                             if isinstance(item, Relation)
                             and item.relation_type is RelationType.EQUALITY
                             and _toda52_group_presentation_matches(
                                 source, goal, equality=item))
    if len(cited_equalities) != 1:
        return ()
    equality = cited_equalities[0]
    return tuple(GoalExpansion(
        _toda52_ordered_db_rule(goal, source, equality=equality),
        (source, theorem, equality),
    ) for theorem in theorem_candidates)

```

## phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py

```python
"""Restore Proposition 5.1 boundaries while registering checked typed literature.

The Proposition 5.8 pi_7^3 component is adopted only after checking its
printed source and the structural generator. No proof is imported.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase163_r4_r11_literature_registration import register_prop56_literature_statements
from phase163_r4_r12_literature_registration import register_prop51_prop53_literature_statements
from phase165_r6_explicit_literature_inputs import prop51_prop53_inputs, prop56_inputs
from phase170_r3_r6_prop58_source import register_source_checked_prop58_pi73
from phase170_r3_r9_toda712_cited_rewrite.source712 import register_cited_toda712_generator_equality
from unified_statement_registry import UnifiedStatementRegistry


def connect_explicit_literature_components(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Register checked literature while preserving existing Proposition 5.1."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    first = register_prop51_prop53_literature_statements(base, prop51_prop53_inputs())
    second = register_prop56_literature_statements(first.snapshot, prop56_inputs())
    registered = register_cited_toda712_generator_equality(
        register_source_checked_prop58_pi73(second.snapshot)
    )
    if registered.proof_links != base.proof_links:
        raise ValueError("literature registration unexpectedly changed proof links")

    original = {
        assertion.assertion_id: assertion
        for assertion in base.registry._assertions.values()
        if assertion.assertion_id.startswith("boundary:Proposition 5.1:")
    }
    original_records = {
        record.assertion_id: record
        for record in base.records
        if record.assertion_id in original
    }
    registry = UnifiedStatementRegistry()
    for reference in registered.registry._references.values():
        registry.add_reference(reference)
    for assertion in registered.registry._assertions.values():
        registry.add_assertion(original.get(assertion.assertion_id, assertion))
    records = tuple(
        original_records.get(record.assertion_id, record)
        for record in registered.records
    )
    result = RegistryBridgeResult(registry, records, base.proof_links)
    for assertion_id, assertion in original.items():
        if result.registry.assertion(assertion_id) != assertion:
            raise ValueError("existing Proposition 5.1 assertion changed")
    return result

```

## phase170_r3_r9_toda712_cited_rewrite/source712.py

```python
"""Source-checked adoption of exactly one Toda (7.12) generator equality.

Chapter VII, (7.12) is a cited GIVEN. A separate, replayable inference
uses it with the admitted prior DB group and Toda (5.2). This module neither
certifies a proof nor claims that the original printed edition was checked.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha1
import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase166_r3aj_structured_generator import structured_generator_from_ids
from proof import Relation, RelationType
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_VI = ROOT / "sources" / "toda" / "Toda_06_2.tex"
CHAPTER_VII = ROOT / "sources" / "toda" / "Toda_07_2.tex"
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"
GENERATORS = ROOT / "data" / "HyoujiGen.csv"
CHAPTER_VI_BLOB = "76934583cff01c8ea83f768e26947eb9b556653b"
CHAPTER_VII_BLOB = "b5b366f2d2b72d7b419192fa74ab848eff098686"
CLAUSE = r"\(\varepsilon_3\circ\nu_{11} = \nu'\circ\ov{\nu}_6,"
LOCATOR_MARKER = r"\textbf{(7.12).}"
REF_ID = "adopted:toda7:eq7.12:generator_equality"
ASSERT_ID = "adopted:toda7:eq7.12:epsilon3_nu11_equal_nuprime_barnu6"


def _verified_adopted_source(path: Path, required_blob: str) -> str:
    """Match the reviewed Git blob, accepting local CRLF checkout conversion."""
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    def blob_digest(data: bytes) -> str:
        return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()
    if not any(blob_digest(value) == required_blob for value in (raw, normalized)):
        raise ValueError("unreviewed adopted Toda source: " + path.name)
    return normalized.decode("utf-8-sig")


def verified_toda712_generator_equality() -> tuple[Relation, int]:
    """Validate the unique printed (7.12) clause and typed registered IDs."""
    vi = _verified_adopted_source(CHAPTER_VI, CHAPTER_VI_BLOB)
    vii = _verified_adopted_source(CHAPTER_VII, CHAPTER_VII_BLOB)
    if vii.count(CLAUSE) != 1:
        raise ValueError("reviewed Toda (7.12) equality missing or ambiguous")
    clause_offset = vii.index(CLAUSE)
    marker_offset = vii.rfind(LOCATOR_MARKER, 0, clause_offset)
    if (marker_offset < 0 or clause_offset - marker_offset > 160
            or vii.count(LOCATOR_MARKER, marker_offset, clause_offset) != 1):
        raise ValueError("Toda (7.12) occurrence is outside its reviewed locator")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    if (manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or manifest.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise ValueError("unreviewed adopted Chapter V reference order")
    positions = tuple(row.get("publication_position") for row in manifest.get("assertions", ())
                      if row.get("chapter") == 5
                      and type(row.get("publication_position")) is int)
    if not positions or max(positions) != 10800:
        raise ValueError("Chapter V source-order boundary changed")
    # Relative to the frozen adopted transcription; never a claim about
    # absolute positions in Toda's original printed edition.
    adopted_position = max(positions) + vi.count("\n") + 1 + vii.count("\n", 0, clause_offset) + 1
    left = structured_generator_from_ids(
        ids=(10, 4), start_dimension=3, generator_csv=GENERATORS,
    )
    right = structured_generator_from_ids(
        ids=(3, 11), start_dimension=3, generator_csv=GENERATORS,
    )
    if left is None or right is None or left == right:
        raise ValueError("HyoujiGen typed generator correspondence invalid")
    from phase168_r2_toda52_transport import _typed_source_and_target
    if (_typed_source_and_target(left) != (14, 3)
            or _typed_source_and_target(right) != (14, 3)):
        raise ValueError("Toda (7.12) source and target dimensions disagree")
    return Relation(lhs=left, rhs=right, relation_type=RelationType.EQUALITY), adopted_position


def register_cited_toda712_generator_equality(base: RegistryBridgeResult) -> RegistryBridgeResult:
    """Register an exact fixed equality; never add a fabricated proof link.

    The ordinary source-first screen constructs the authorized GIVEN from
    this independently positioned assertion. Trust verification checks it.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    equality, position = verified_toda712_generator_equality()
    registry = UnifiedStatementRegistry()
    for reference in base.registry._references.values():
        registry.add_reference(reference)
    registry.add_reference(LiteratureEntry(
        reference_id=REF_ID, kind=ReferenceKind.EQUATION,
        locator="(7.12)",
        source_id="sources/toda/Toda_07_2.tex (adopted transcription, original edition unverified)",
        publication_position=position,
    ))
    for assertion in base.registry._assertions.values():
        registry.add_assertion(assertion)
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERT_ID, reference_id=REF_ID,
        kind=AssertionKind.STATEMENT, content=equality,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("typed generator equality in pi_14^3",),
    ))
    return RegistryBridgeResult(registry, base.records, base.proof_links)

```

## tests/test_toda712_rewrite.py

```python
"""Focused source, typed equality, provenance, negative and Web tests."""
from dataclasses import replace
from types import SimpleNamespace

import pytest

from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase168_r2_toda52_transport import (
    _toda52_cited_generator_equality, _toda52_group_presentation_matches,
    expand_toda52_finite_cyclic_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase170_r3_r9_toda712_cited_rewrite.source712 import (
    ASSERT_ID, REF_ID, verified_toda712_generator_equality,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def _goal_and_source():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=12)
    assert len(goals) == 1
    source = exact_prior_database_result(3, 11)
    assert source is not None
    return bridge, goals[0], source


def test_r3r9_cited_source_and_registered_typed_equality():
    relation, position = verified_toda712_generator_equality()
    bridge, goal, source = _goal_and_source()
    records = [a for a in bridge.registry._assertions.values() if a.assertion_id.endswith(ASSERT_ID)]
    assert len(records) == 1
    assertion = records[0]
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert assertion.content == relation
    ref = bridge.registry.reference(assertion.reference_id)
    assert ref.locator == "(7.12)" and ref.publication_position == position
    assert not _toda52_group_presentation_matches(source, goal)
    assert _toda52_group_presentation_matches(source, goal, equality=relation)


def test_r3r9_requires_citation_as_third_subgoal():
    equality, _ = verified_toda712_generator_equality()
    _, goal, source = _goal_and_source()
    theorem = Toda52UniversalStatement()
    assert expand_toda52_finite_cyclic_goal(goal, (theorem,)) == ()
    options = expand_toda52_finite_cyclic_goal(goal, (theorem, equality))
    assert len(options) == 1
    expansion = options[0]
    assert expansion.subgoals == (source, theorem, equality)
    assert expansion.rule.match_guard(tuple(SimpleNamespace(conclusion=x) for x in expansion.subgoals), {})
    assert not expansion.rule.match_guard((SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem)), {})
    reversed_relation = Relation(equality.rhs, equality.lhs, RelationType.EQUALITY)
    assert _toda52_cited_generator_equality(equality.lhs, equality.rhs, reversed_relation)


def test_r3r9_forgeries_and_wrong_relation_are_rejected():
    equality, _ = verified_toda712_generator_equality()
    _, goal, source = _goal_and_source()
    theorem = Toda52UniversalStatement()
    bad = Relation(equality.lhs, equality.lhs, RelationType.EQUALITY)
    assert not _toda52_group_presentation_matches(source, goal, equality=bad)
    assert expand_toda52_finite_cyclic_goal(goal, (theorem, bad)) == ()
    options = expand_toda52_finite_cyclic_goal(goal, (theorem, equality))
    guard = options[0].rule.match_guard
    assert not guard((SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem), SimpleNamespace(conclusion=bad)), {})
    assert not guard((SimpleNamespace(conclusion=goal), SimpleNamespace(conclusion=theorem), SimpleNamespace(conclusion=equality)), {})


def test_r3r9_prior_db_group_and_source_are_not_a_completed_proof():
    equality, _ = verified_toda712_generator_equality()
    _, goal, _ = _goal_and_source()
    # An equality by itself is insufficient: (5.2) must be in the screened context.
    assert expand_toda52_finite_cyclic_goal(goal, (equality,)) == ()


def test_r3r9_actual_pi14_search_and_web_trust_boundary():
    from phase165_r52_partial_proof import ProofSearchStatus
    from web_group_proof import build_standard_web_group_proof_view
    result = search_group_from_registered_goal(n=2, k=12)
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(result.proven_steps) >= 4
    assert any(step.rule is ProofRule.GIVEN and step.inference_rule is not None
               and step.inference_rule.literature_reference is not None
               and step.inference_rule.literature_reference.locator == "(7.12)"
               for step in result.proven_steps)
    view = build_standard_web_group_proof_view(
        n=2, k=12, max_depth=2, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof" and view.partial_result is False
    assert view.steps and view.rendered_lines

```

## tests/test_offline_contract.py

```python
"""Guarded patch and source-registration checks independent of production imports."""
from __future__ import annotations

import ast
from hashlib import sha1
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
ROUTER = HERE / 'replacement/phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py'
TRANSPORT = HERE / 'replacement/phase168_r2_toda52_transport.py'
SOURCE = HERE / 'source712.py'


def _functions(path: Path) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in ast.parse(path.read_text(encoding='utf-8')).body
            if isinstance(node, ast.FunctionDef)}


def test_reviewed_transport_is_a_complete_module():
    names = _functions(TRANSPORT)
    assert {'_toda52_group_presentation_matches',
            '_toda52_cited_generator_equality',
            '_toda52_ordered_db_rule',
            'expand_toda52_finite_cyclic_goal'} <= names.keys()
    assert not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                   and n.value.value is Ellipsis
                   for n in ast.walk(ast.parse(TRANSPORT.read_text(encoding='utf-8'))))


def test_router_existing_source_still_preserved():
    full = ROUTER.read_text(encoding='utf-8')
    assert 'register_source_checked_prop58_pi73' in full
    assert 'register_cited_toda712_generator_equality' in full
    assert len(_functions(ROUTER)) == 1


def test_reviewed_toda_reference_is_not_manufactured_from_csv():
    full = SOURCE.read_text(encoding='utf-8')
    assert 'CHAPTER_VII_BLOB' in full
    assert 'CLAUSE' in full and '(7.12)' in full
    assert 'ids=(10, 4)' in full and 'ids=(3, 11)' in full
    assert 'base.proof_links' in full
    assert 'ProofStep(' not in full


def test_runner_is_conservative_and_reversible():
    runner = (HERE / 'runner.py').read_text(encoding='utf-8')
    assert 'REVIEWED_BASE_HEAD' in runner
    assert 'git(root, "diff", "--cached", "--name-only")' in runner
    assert 'restored' in runner.lower()
    assert 'focused_pytest' in runner and 'active_web' in runner
    assert 'full_pytest": False' in runner
    assert 'if dry_run:' in runner


def test_source_file_and_runner_compiles():
    for name in ('runner.py', 'source712.py', 'verify.py'):
        compile((HERE / name).read_bytes(), name, 'exec')

```

## tests/test_offline_rewrite.py

```python
"""Offline AST checks of R3-R9 typed rewrite; no repository install required."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import sys
from types import ModuleType

import pytest

SOURCE = Path(__file__).resolve().parents[1] / 'replacement' / 'phase168_r2_toda52_transport.py'


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
class Group:
    group_dimension: int
    sphere_dimension: int


class Zero:
    pass


class Suspension:
    pass


class IteratedSuspension:
    pass


@dataclass(frozen=True)
class Finite:
    order: int
    generator: object


@dataclass(frozen=True)
class DirectSum:
    summands: tuple


class RelationType(Enum):
    EQUALITY = 'equality'


@dataclass(frozen=True)
class Relation:
    lhs: object
    rhs: object
    relation_type: RelationType = RelationType.EQUALITY


def _load(monkeypatch):
    expr = ModuleType('expression')
    expr.Composition = Composition
    expr.HomotopyElement = Element
    expr.GeneratorSymbol = Symbol
    expr.Sum = Sum
    expr.Multiple = Multiple
    expr.Suspension = Suspension
    expr.IteratedSuspension = IteratedSuspension
    groups = ModuleType('homotopy_groups')
    groups.FiniteCyclicGroup = Finite
    groups.FreeCyclicGroup = Finite
    groups.TodaPrimaryGroupZeroStatement = Zero
    groups.DirectSumGroup = DirectSum
    other = ModuleType('phase168_r2_8_3_generator_identity.identity')
    other.same_registered_group_presentation = lambda _a, _b: False
    for n, o in [('expression', expr),('homotopy_groups',groups),
                 ('phase168_r2_8_3_generator_identity.identity',other)]:
        monkeypatch.setitem(sys.modules,n,o)
    code=ast.parse(SOURCE.read_text(encoding='utf-8'))
    wanted={'_typed_source_and_target','_eta2_inverse_image',
            '_toda52_cited_generator_equality','_toda52_group_presentation_matches'}
    methods=[x for x in code.body if isinstance(x,ast.FunctionDef) and x.name in wanted]
    assert {x.name for x in methods}==wanted
    globs={'Composition':Composition,'HomotopyElement':Element,
           'GeneratorSymbol':Symbol,'FiniteCyclicGroup':Finite,
           'TodaPrimaryGroup':Group,'Relation':Relation,
           'RelationType':RelationType}
    exec(compile(ast.fix_missing_locations(ast.Module(body=methods,type_ignores=[])),
                 str(SOURCE),'exec'),globs)
    return globs


def _setup():
    eta = Element('eta2',2,3,2,Symbol('η',2))
    mu = Element('muprime',3,14,3,Symbol('muprime'))
    eps = Element('eps',3,11,3,Symbol('eps'))
    nu11 = Element('nu11',11,14,11,Symbol('nu',11))
    nuprime = Element('nuprime',3,6,3,Symbol('nuprime'))
    barnu = Element('barnu6',6,14,6,Symbol('barnu',6))
    nueps = Element('nueps',3,14,3,Symbol('nueps'))
    lhs = Composition(eps,nu11)
    rhs = Composition(nuprime,barnu)
    source=Relation(Group(14,3), DirectSum((Finite(4,mu),Finite(2,lhs),Finite(2,nueps))))
    target=Relation(Group(14,2), DirectSum((Finite(4,Composition(eta,mu)),
               Finite(2,Composition(eta,rhs)),Finite(2,Composition(eta,nueps)))))
    eq=Relation(lhs,rhs)
    return source,target,eq


def test_requires_cited_typed_equality(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    matches=api['_toda52_group_presentation_matches']
    assert not matches(source,target)
    assert matches(source,target,equality=eq)


def test_reverse_equality_but_not_a_fake_one(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    matches=api['_toda52_group_presentation_matches']
    assert matches(source,target,equality=Relation(eq.rhs,eq.lhs))
    assert not matches(source,target,equality=Relation(eq.lhs,eq.lhs))
    assert not matches(source,target,equality=Relation(eq.lhs,eq.rhs,relation_type='non-equality'))


def test_wrong_dimensions_rejected(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    wrong=Relation(eq.lhs,Element('bad',3,15,3,Symbol('bad')))
    assert not api['_toda52_group_presentation_matches'](source,target,equality=wrong)


def test_wrong_cyclic_order_rejected(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    different=Relation(target.lhs,DirectSum((target.rhs.summands[0],
                     Finite(4,target.rhs.summands[1].generator),
                     target.rhs.summands[2])))
    assert not api['_toda52_group_presentation_matches'](source,different,equality=eq)


def test_no_equality_required_for_directly_matching_existing_component(monkeypatch):
    api=_load(monkeypatch)
    source,target,eq=_setup()
    target_same=Relation(target.lhs,DirectSum((
        target.rhs.summands[0],
        Finite(2,Composition(target.rhs.summands[0].generator.left,eq.lhs)),
        target.rhs.summands[2])))
    assert api['_toda52_group_presentation_matches'](source,target_same)

```

## runner.py

```python
"""Guarded 3-file patch, focused tests, active Web check, rollback on failure."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
import os
from pathlib import Path
import subprocess
import sys

REVIEWED_BASE_HEAD = "fdf60522b6d477209e9d8d67720a63f9863e419c"
REVIEWED_BLOBS = {
    "phase168_r2_toda52_transport.py": "3bf9dfa2080e330e7030f0f0a7762f3fb1fa8fff",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py": "84dfa0c6fe54e9d51b6b11279ee0001d6231ef8a",
    "sources/toda/Toda_06_2.tex": "76934583cff01c8ea83f768e26947eb9b556653b",
    "sources/toda/Toda_07_2.tex": "b5b366f2d2b72d7b419192fa74ab848eff098686",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
}
TARGETS = (
    "phase168_r2_toda52_transport.py",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py",
)
NEW_MODULE = "phase170_r3_r9_toda712_cited_rewrite"


def git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def preflight(root: Path) -> dict:
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_BASE_HEAD:
        raise RuntimeError(f"unreviewed branch or HEAD: {branch} {head}")
    if git(root, "diff", "--name-only") or git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("tracked worktree or staged changes present")
    for path, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", f"HEAD:{path}") != blob or not (root/path).is_file():
            raise RuntimeError("reviewed file missing or changed: " + path)
    for target in TARGETS:
        raw = (root / target).read_bytes()
        normalized = raw.replace(b"\r\n", b"\n")
        def blobhash(data):
            return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()
        if blobhash(raw) != REVIEWED_BLOBS[target] and blobhash(normalized) != REVIEWED_BLOBS[target]:
            raise RuntimeError("worktree target differs from reviewed Git blob: " + target)
    return {"head": head, "branch": branch, "targets": list(TARGETS)}


def execute(root: Path, output: Path, name: str, command: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    run = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                         errors="replace", check=False)
    (output / f"{name}.log").write_text(run.stdout, encoding="utf-8")
    print(run.stdout, flush=True)
    print(f"PHASE170_R3R9_{name.upper()}_EXIT={run.returncode}", flush=True)
    return run.returncode


def run(root: Path, *, dry_run: bool) -> int:
    package = Path(__file__).resolve().parent
    output = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "EHPProofTracerRecovery" / (
        "phase170_r3_r9_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    )
    output.mkdir(parents=True, exist_ok=False)
    print("PHASE170_R3R9_MODE=CITED_GENERATOR_EQUALITY", flush=True)
    print(f"PHASE170_R3R9_OUTPUT={output}", flush=True)
    report = {"phase": "170 R3-R9", "mode": "DRY_RUN" if dry_run else "GUARDED_PATCH", "full_pytest": False}
    saved: dict[str, bytes] = {}
    modified: list[str] = []
    passed = False
    try:
        report["preflight"] = preflight(root)
        for target in TARGETS:
            original = (root / target).read_bytes()
            replacement = (package / "replacement" / target).read_bytes()
            compile(replacement, target, "exec")
            saved[target] = original
            (output / (Path(target).name + ".before")).write_bytes(original)
            if replacement == original or replacement.replace(b"\r\n",b"\n") == original.replace(b"\r\n",b"\n"):
                raise RuntimeError("replacement is unchanged: " + target)
        compile((package / "source712.py").read_bytes(), "source712.py", "exec")
        if dry_run:
            print("PHASE170_R3R9_DRY_RUN=PASS", flush=True)
            report["result"] = "DRY_RUN_PASS"
            passed = True
            return 0
        for target in TARGETS:
            dest = root / target
            dest.write_bytes((package / "replacement" / target).read_bytes())
            modified.append(target)
        focused = [
            package / "tests/test_toda712_rewrite.py",
            root / "phase170_r3_r7_toda52_ordered_db_transport/tests/test_ordered_db_toda52.py",
            root / "phase170_r3_r5_toda52_cyclic_generalization/tests/test_phase170_r3_r5_toda52_cyclic.py",
            root / "phase170_r3_r6_prop58_pi73_source/tests/test_phase170_r3_r6_source.py",
            root / "phase169_r10e4_ordered_db_prior/tests/test_r10e4_ordered_db_prior.py",
            root / "phase168_r2_toda52_transport/tests/test_phase168_r2_toda52_transport.py",
        ]
        if not all(path.is_file() for path in focused):
            raise RuntimeError("missing related focused test")
        ret = execute(root, output, "focused_pytest", [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", *(str(path) for path in focused),
        ])
        if ret:
            raise RuntimeError("focused pytest failed")
        ret = execute(root, output, "active_web", [
            sys.executable, "-B", str(package / "verify.py"),
        ])
        if ret:
            raise RuntimeError("active Web verification failed")
        passed = True
        report["result"] = "PATCHED_AND_WEB_VERIFIED"
        print("PHASE170_R3R9_RESULT=PATCHED_AND_WEB_VERIFIED", flush=True)
        print("PHASE170_R3R9_FULL_PYTEST=False", flush=True)
        return 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ROLLED_BACK"
        report["error"] = repr(exc)
        print(f"PHASE170_R3R9_REFUSED={type(exc).__name__}: {exc}", flush=True)
        return 2
    finally:
        if not passed:
            for target in modified:
                (root / target).write_bytes(saved[target])
                print("PHASE170_R3R9_RESTORED=" + target, flush=True)
        report_path = output / "result.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PHASE170_R3R9_REPORT=" + str(report_path), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

```

## verify.py

```python
"""Active Web verification of the previously missing pi_14^2 proof."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view


def main() -> int:
    for k in (5, 6, 8, 10, 11, 12, 14):
        result = search_group_from_registered_goal(n=2, k=k)
        status = getattr(result.status, "value", str(result.status))
        print(f"PHASE170_R3R9_k={k}_SEARCH_STATUS={status}", flush=True)
        print(f"PHASE170_R3R9_k={k}_OPEN_GOALS={len(result.open_goals)}", flush=True)
        print(f"PHASE170_R3R9_k={k}_PROVEN_STEPS={len(result.proven_steps)}", flush=True)
        if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
                or not result.proven_steps):
            print(f"PHASE170_R3R9_k={k}_DIAGNOSTICS={result.diagnostics!r}", flush=True)
            return 4
        view = build_standard_web_group_proof_view(
            n=2, k=k, max_depth=2, mode="narrative", citation_source="model",
        )
        print(f"PHASE170_R3R9_k={k}_WEB_KEY={view.key}", flush=True)
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.steps or not view.rendered_lines):
            return 5
        print(f"PHASE170_R3R9_k={k}=COMPLETE_AND_WEB_VERIFIED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
$Env:PYTHONPATH = $Root
$ArgsList = @('-B', (Join-Path $PSScriptRoot 'runner.py'), '--root', $Root)
if ($DryRun) { $ArgsList += '--dry-run' }
& python @ArgsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

```
