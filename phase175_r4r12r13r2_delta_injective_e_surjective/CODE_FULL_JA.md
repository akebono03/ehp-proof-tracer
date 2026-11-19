# R13R2 新規コード全文

新規 `rule.py`、`audit.py`、`tests/test_rule.py` はすべてパッケージ内に配置。既存ファイルは変更しない。

## rule.py（全文）

```python
"""Isolated, source-first general Delta injectivity and EHP E-surjectivity rules.

No new GIVEN, group fact, saved proof, or public provider is added here.
Every input remains an independently discharged backward proof goal.
"""
from __future__ import annotations

from expression import Multiple, Sum
from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement, TodaProp42ExactnessStatement


DELTA_RULE_NAME = "free cyclic source and nonzero free coordinate imply Delta injectivity"
E_RULE_NAME = "injective Delta and consecutive EHP exactness imply suspension surjectivity"


def _linear_coordinates(value: object, free: object, torsion: object) -> tuple[int, int] | None:
    """Accept only a literal linear combination of two listed summand generators."""
    if value == free:
        return 1, 0
    if value == torsion:
        return 0, 1
    if isinstance(value, Multiple) and type(value.coefficient) is int:
        pair = _linear_coordinates(value.expression, free, torsion)
        if pair is not None:
            return value.coefficient * pair[0], value.coefficient * pair[1]
    if isinstance(value, Sum):
        left = _linear_coordinates(value.left, free, torsion)
        right = _linear_coordinates(value.right, free, torsion)
        if left is not None and right is not None:
            return left[0] + right[0], left[1] + right[1]
    return None


def delta_injective_inputs(
    goal: object,
    source: object,
    target: object,
    image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Check a free-cyclic source and an explicitly nonzero free image coordinate.

    The signed image may be either sign: nonzero free coordinate is invariant.
    The torsion coordinate must refer to the other actual direct-sum generator.
    """
    if not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaDeltaMap):
        return None
    delta = goal.map
    if not all(isinstance(g, TodaPrimaryGroup) for g in (delta.source_group, delta.target_group)):
        return None
    if not isinstance(source, Relation) or not isinstance(target, Relation):
        return None
    if source.relation_type is not RelationType.EQUALITY or target.relation_type is not RelationType.EQUALITY:
        return None
    if source.lhs != delta.source_group or target.lhs != delta.target_group:
        return None
    if not isinstance(source.rhs, FreeCyclicGroup):
        return None
    if not isinstance(target.rhs, DirectSumGroup) or len(target.rhs.summands) != 2:
        return None
    free_parts = tuple(x for x in target.rhs.summands if isinstance(x, FreeCyclicGroup))
    finite_parts = tuple(x for x in target.rhs.summands if isinstance(x, FiniteCyclicGroup))
    if len(free_parts) != 1 or len(finite_parts) != 1 or finite_parts[0].order < 1:
        return None
    if not isinstance(image, TodaDeltaImageUpToSignStatement):
        return None
    if image.map != delta or image.element != source.rhs.generator:
        return None
    pair = _linear_coordinates(
        image.positive_value, free_parts[0].generator, finite_parts[0].generator,
    )
    if pair is None or pair[0] == 0:
        return None
    return source, target, image


def delta_injective_from_free_coordinate_rule(
    goal: MapInjective,
    required: tuple[Relation, Relation, TodaDeltaImageUpToSignStatement],
) -> InferenceRule:
    """ProofStep matcher; cannot infer a result merely from candidate subgoals."""
    if delta_injective_inputs(goal, *required) is None:
        raise ValueError("invalid free-coordinate Delta injectivity inputs")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and tuple(step.conclusion for step in premises) == required
            and delta_injective_inputs(goal, *required) == required
        )

    return InferenceRule(
        name=DELTA_RULE_NAME,
        description=(
            "A map Z -> Z + Z/m is injective when its generator has a "
            "nonzero integer coordinate in the free summand."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=required[0]),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY,
                           statement_pattern=required[1]),
            PremisePattern(statement_type=TodaDeltaImageUpToSignStatement,
                           statement_pattern=required[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_delta_injective_from_free_coordinate(
    goal: object, source: object, target: object, image: object,
) -> tuple[GoalExpansion, ...]:
    required = delta_injective_inputs(goal, source, target, image)
    if required is None:
        return ()
    return (GoalExpansion(delta_injective_from_free_coordinate_rule(goal, required), required),)


def e_surjective_inputs(
    goal: object,
) -> tuple[MapInjective, TodaProp42ExactnessStatement, TodaProp42ExactnessStatement] | None:
    """Build the only matching H-Delta and E-H windows for an E map."""
    if not isinstance(goal, MapSurjective) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    suspension = goal.map
    a, b = suspension.source_group, suspension.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(v) is not int for v in (
        a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension,
    )):
        return None
    if a.group_dimension + 1 != b.group_dimension or a.sphere_dimension + 1 != b.sphere_dimension:
        return None
    c = TodaPrimaryGroup(b.group_dimension, 2 * a.sphere_dimension + 1)
    d = TodaPrimaryGroup(b.group_dimension - 2, a.sphere_dimension)
    h_delta = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=b, middle_term=c, target_term=d,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    ))
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=a, middle_term=b, target_term=c,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(h_delta) is None or prop42_exactness_indices(e_h) is None:
        return None
    return MapInjective(TodaDeltaMap(c, d)), h_delta, e_h


def e_surjective_from_delta_injective_rule(goal: MapSurjective) -> InferenceRule:
    required = e_surjective_inputs(goal)
    if required is None:
        raise ValueError("invalid EHP suspension surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and e_surjective_inputs(goal) == required
        )

    return InferenceRule(
        name=E_RULE_NAME,
        description=(
            "Exact H-Delta gives im(H)=ker(Delta)=0; exact E-H then gives "
            "im(E)=ker(H)=the whole middle group."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_e_surjective_from_delta_injective(goal: object) -> tuple[GoalExpansion, ...]:
    required = e_surjective_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(e_surjective_from_delta_injective_rule(goal), required),)

```

## audit.py（全文）

```python
"""Isolated Phase 175 R13R2 arithmetic and source-boundary audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import e_surjective_inputs


def run(root: Path, dry_run: bool) -> int:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            text=True, capture_output=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R13R2 requires develop")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          text=True, capture_output=True, check=True).stdout.strip()
    signed = canonical_toda58()
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    required = e_surjective_inputs(goal)
    if required is None or required[0].map != signed.map:
        raise RuntimeError("Toda (5.8) Delta is not the EHP Delta target")
    report = {
        "phase": "175-R4R12R13R2", "dry_run": dry_run, "head": head,
        "gate": "PASS_R13R2_ISOLATED_RULES_NOT_PUBLIC_NOT_COMPLETE",
        "new_given": 0, "new_mathematical_rules": 2,
        "production_changes": [], "full_pytest_executed": False,
        "public_provider_connected": False, "target_proof_complete": False,
        "delta": repr(signed.map),
        "exactness": [repr(x) for x in required[1:]],
    }
    output = root / "phase175_r4r12r13r2_delta_injective_e_surjective" / "output"
    output.mkdir(exist_ok=True)
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("gate", "head", "new_given", "public_provider_connected", "target_proof_complete"):
        print("PHASE175_R13R2_" + key.upper() + "=" + str(report[key]))
    print("PHASE175_R13R2_REPORT=" + str(output / "report.json"))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_rule.py（全文）

```python
"""Focused tests of isolated R13R2 inference rules (no public installation)."""
from expression import Multiple, Sum
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    delta_injective_inputs, expand_delta_injective_from_free_coordinate,
    e_surjective_inputs, expand_e_surjective_from_delta_injective,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def _delta_fixture():
    signed = canonical_toda58()
    free = signed.positive_value.left.expression
    torsion = signed.positive_value.right.expression
    source = Relation(
        lhs=TodaPrimaryGroup(9, 9), rhs=FreeCyclicGroup(signed.element),
        relation_type=RelationType.EQUALITY,
    )
    target = Relation(
        lhs=TodaPrimaryGroup(7, 4),
        rhs=DirectSumGroup((FreeCyclicGroup(free), FiniteCyclicGroup(4, torsion))),
        relation_type=RelationType.EQUALITY,
    )
    return MapInjective(signed.map), source, target, signed


def test_toda58_nonzero_free_coordinate_has_conditional_branch():
    goal, source, target, signed = _delta_fixture()
    assert delta_injective_inputs(goal, source, target, signed) == (source, target, signed)
    expansions = expand_delta_injective_from_free_coordinate(goal, source, target, signed)
    assert len(expansions) == 1
    assert expansions[0].subgoals == (source, target, signed)


def test_zero_free_coordinate_is_rejected():
    goal, source, target, signed = _delta_fixture()
    torsion_only = TodaDeltaImageUpToSignStatement(
        map=signed.map, element=signed.element,
        positive_value=Multiple(-1, signed.positive_value.right.expression),
    )
    assert delta_injective_inputs(goal, source, target, torsion_only) is None


def test_unlisted_generator_is_rejected():
    goal, source, target, signed = _delta_fixture()
    wrong = Relation(
        lhs=target.lhs,
        rhs=DirectSumGroup((FreeCyclicGroup(signed.element),
                            FiniteCyclicGroup(4, signed.positive_value.right.expression))),
        relation_type=RelationType.EQUALITY,
    )
    assert delta_injective_inputs(goal, source, wrong, signed) is None


def test_matching_consecutive_exactness_windows():
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    required = e_surjective_inputs(goal)
    assert required is not None
    assert required[0] == MapInjective(TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)))
    assert len(expand_e_surjective_from_delta_injective(goal)) == 1
    assert expand_e_surjective_from_delta_injective(goal)[0].subgoals == required


def test_invalid_suspension_dimensions_are_rejected():
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 6)))
    assert e_surjective_inputs(goal) is None
    assert expand_e_surjective_from_delta_injective(goal) == ()

```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $argsAudit = @('-m', 'phase175_r4r12r13r2_delta_injective_e_surjective.audit', '--root', $root)
    if ($DryRun) { $argsAudit += '--dry-run' }
    python @argsAudit
    if ($LASTEXITCODE -ne 0) { throw 'R13R2 audit failed' }
    python -m pytest -q phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R13R2 focused tests failed' }
} finally { Pop-Location }

```

