# R13R7 全コード（置換・追加可能な単位）

変更対象: `phase175_r4r12r13r2_delta_injective_e_surjective/rule.py` の import 全体と `_linear_coordinates` 関数。新規: `phase175_r4r12r13r7_typed_nu_prime_notation/notation.py`, `installer.py`, `audit.py`, `tests/test_r13r7_notation.py`, `run.ps1`。

## 変更後 rule.py 全文（現行 R13R2 に対する置換結果）

```python
"""Isolated, source-first general Delta injectivity and EHP E-surjectivity rules.

No new GIVEN, group fact, saved proof, or public provider is added here.
Every input remains an independently discharged backward proof goal.
"""
from __future__ import annotations

from expression import Multiple, Sum
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import (
    same_typed_generator_notation,
)
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
    if same_typed_generator_notation(value, free):
        return 1, 0
    if same_typed_generator_notation(value, torsion):
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

## notation.py 全文

```python
"""Strict notation-only equivalence for one-fold suspension of typed nu-prime.

This helper does not identify different mathematical generators or produce
ProofSteps. The Unicode-prime / ASCII-prime and LaTeX-family spellings are
alternate encodings of the same explicitly typed nu-prime symbol.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension


def _nu_prime_label(value: object) -> bool:
    """Recognize only documented encodings of the typed nu-prime symbol."""
    return isinstance(value, str) and value in ("ν′", "ν'", "\\nu'", "\\nu′")


def _nu_prime_element_alias(left: object, right: object) -> bool:
    """Refuse to collapse names unless every typed field is compatible."""
    if not isinstance(left, HomotopyElement) or not isinstance(right, HomotopyElement):
        return False
    if not (type(left.dimension) is int and type(right.dimension) is int):
        return False
    if (
        left.dimension != right.dimension
        or left.source != right.source
        or left.target != right.target
        or not all(type(x) is int for x in (left.source, left.target, right.source, right.target))
    ):
        return False
    if not (_nu_prime_label(left.name) and _nu_prime_label(right.name)):
        return False
    if not isinstance(left.generator, GeneratorSymbol) or not isinstance(right.generator, GeneratorSymbol):
        return False
    def symbol_is_nu_prime(g: GeneratorSymbol) -> bool:
        return (
            g.index is None
            and (
                (g.family == "ν" and g.decoration in ("′", "'"))
                or (g.family in ("\\nu'", "\\nu′", "ν′", "ν'") and g.decoration is None)
            )
        )
    return symbol_is_nu_prime(left.generator) and symbol_is_nu_prime(right.generator)


def same_typed_generator_notation(left: object, right: object) -> bool:
    """Check equality or strictly equivalent one-suspension nu-prime notation.

    Not a group identity theorem: only syntactically interchangeable encodings
    are recognized; arbitrary homotopy elements never compare equal this way.
    """
    if left == right:
        return True
    if isinstance(left, Suspension) and isinstance(right, IteratedSuspension):
        return type(right.exponent) is int and right.exponent == 1 and _nu_prime_element_alias(
            left.expression, right.expression
        )
    if isinstance(left, IteratedSuspension) and isinstance(right, Suspension):
        return type(left.exponent) is int and left.exponent == 1 and _nu_prime_element_alias(
            left.expression, right.expression
        )
    return False
```

## installer.py 全文

```python
"""Minimal anchored replacement of the R13R2 coordinate matcher only."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase175_r4r12r13r2_delta_injective_e_surjective/rule.py")
OLD_IMPORT = "from expression import Multiple, Sum\n"
NEW_IMPORT = (
    "from expression import Multiple, Sum\n"
    "from phase175_r4r12r13r7_typed_nu_prime_notation.notation import (\n"
    "    same_typed_generator_notation,\n"
    ")\n"
)
OLD_BODY = "    if value == free:\n        return 1, 0\n    if value == torsion:\n        return 0, 1\n"
NEW_BODY = (
    "    if same_typed_generator_notation(value, free):\n"
    "        return 1, 0\n"
    "    if same_typed_generator_notation(value, torsion):\n"
    "        return 0, 1\n"
)


def render(source: str) -> tuple[str, bool]:
    """Fail closed on source drift and partial application."""
    if source.count(NEW_IMPORT) == 1 and source.count(NEW_BODY) == 1:
        return source, False
    if NEW_IMPORT in source or NEW_BODY in source:
        raise RuntimeError("R13R7_PARTIAL_PATCH")
    if source.count(OLD_IMPORT) != 1 or source.count(OLD_BODY) != 1:
        raise RuntimeError("R13R7_SOURCE_DRIFT")
    result = source.replace(OLD_IMPORT, NEW_IMPORT, 1).replace(OLD_BODY, NEW_BODY, 1)
    return result, True


def plan(root: Path) -> tuple[Path, str, str, bool]:
    path = root / TARGET
    before = path.read_text(encoding="utf-8-sig")
    after, needed = render(before)
    return path, before, after, needed


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    import ast
    path, before, after, required = plan(root)
    ast.parse(after)
    output.mkdir(parents=True, exist_ok=True)
    (output / "rule_FULL.py").write_text(after, encoding="utf-8")
    if required and not dry_run:
        raw = path.read_bytes()
        if b"\r\n" in raw:
            path.write_bytes(after.replace("\n", "\r\n").encode("utf-8"))
        else:
            path.write_text(after, encoding="utf-8")
    return {"change_required": required, "installed": required and not dry_run,
            "target": str(TARGET), "full_replacement_file": str(output / "rule_FULL.py")}
```

## audit.py 全文

```python
"""Verify strict notation matching and real public Delta candidates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r7_typed_nu_prime_notation.installer import install
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation

PACKAGE = "phase175_r4r12r13r7_typed_nu_prime_notation"


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", check=False)
    if p.returncode != 0:
        raise RuntimeError("R13R7_GIT_FAILED " + repr(args) + ": " + p.stderr)
    return p.stdout.strip()


def inspect(*, proof_before_patch: bool) -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
        delta_free_coordinate_proposals, screened_toda58_available,
    )
    signed = canonical_toda58()
    relation = exact_prior_database_result(4, 3)
    if relation is None or not isinstance(relation.rhs, DirectSumGroup):
        raise RuntimeError("R13R7_DB_GROUP_MISSING")
    parts = [x for x in relation.rhs.summands if isinstance(x, FiniteCyclicGroup)]
    if len(parts) != 1:
        raise RuntimeError("R13R7_TORSION_PART_NOT_UNIQUE")
    cited = screened_toda58_available(build_shared_typed_bridge())
    goal = MapInjective(signed.map)
    count = len(delta_free_coordinate_proposals(goal, cited58=cited))
    return {
        "toda58_citation_screened": cited,
        "raw_torsion_equal": signed.positive_value.right.expression == parts[0].generator,
        "strict_notation_alias": same_typed_generator_notation(
            signed.positive_value.right.expression, parts[0].generator),
        "public_delta_candidates": count,
        "requires_positive_count_after_install": not proof_before_patch,
        "group_proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R13R7_ROOT_MISMATCH")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R13R7_BRANCH_MISMATCH")
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report = {"phase": "175-R4R12R13R7", "dry_run": dry_run,
              "head": git(root, "rev-parse", "HEAD"), "new_given": 0,
              "new_mathematical_rules": 0, "full_pytest": "NOT_RUN",
              "gate": "FAIL_R13R7"}
    try:
        report["patch"] = install(root, dry_run=dry_run, output=output)
        # DryRun intentionally examines the unpatched process without
        # ever claiming a public proof is available.
        report["frontier"] = inspect(proof_before_patch=dry_run)
        f = report["frontier"]
        if not f["toda58_citation_screened"] or not f["strict_notation_alias"]:
            raise RuntimeError("R13R7_SOURCE_OR_NOTATION_GUARD_FAILED")
        if not dry_run and f["public_delta_candidates"] != 1:
            raise RuntimeError("R13R7_DELTA_CANDIDATE_NOT_CONNECTED")
        report["gate"] = ("PASS_R13R7_DRYRUN_NOT_COMPLETE" if dry_run else
                          "PASS_R13R7_DELTA_CANDIDATE_CONNECTED_NOT_COMPLETE")
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R13R7_GATE=" + report["gate"])
    print("PHASE175_R13R7_HEAD=" + report["head"])
    for key, val in report.get("frontier", {}).items():
        print("PHASE175_R13R7_" + key.upper() + "=" + str(val))
    print("PHASE175_R13R7_NEW_GIVEN=0")
    print("PHASE175_R13R7_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R13R7_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R7_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R13R7_ERROR=" + report["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_r13r7_notation.py 全文

```python
"""Positive and negative notation guard tests, plus actual DB correspondence."""
from __future__ import annotations

from dataclasses import replace

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r7_typed_nu_prime_notation import installer
from phase175_r4r12r13r7_typed_nu_prime_notation.notation import same_typed_generator_notation


def observed_pair():
    signed = canonical_toda58()
    earlier = exact_prior_database_result(4, 3)
    assert isinstance(earlier.rhs, DirectSumGroup)
    part, = (x for x in earlier.rhs.summands if isinstance(x, FiniteCyclicGroup))
    return signed.positive_value.right.expression, part.generator


def test_actual_prior_and_source_are_same_strict_nu_prime_notation():
    left, right = observed_pair()
    assert left != right
    assert same_typed_generator_notation(left, right)
    assert same_typed_generator_notation(right, left)


def test_incompatible_dimensions_and_prime_or_family_rejected():
    left, right = observed_pair()
    assert not same_typed_generator_notation(left, replace(right, exponent=2))
    wrong_dim = replace(right.expression, source=right.expression.source + 1)
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_dim))
    wrong_family = replace(right.expression, generator=GeneratorSymbol("\\eta'"))
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_family))
    wrong_name = replace(right.expression, name="ν")
    assert not same_typed_generator_notation(left, replace(right, expression=wrong_name))


def test_other_elements_are_not_identified_by_similar_suspension():
    left, right = observed_pair()
    other = HomotopyElement("ν", 3, 6, 3, GeneratorSymbol("ν"))
    assert not same_typed_generator_notation(Suspension(other), IteratedSuspension(other, 1))
    assert same_typed_generator_notation(right, right)
    assert not same_typed_generator_notation(left, IteratedSuspension(right.expression, 0))


def test_installer_is_idempotent_and_rejects_partial_patch():
    path = installer.TARGET
    # Validate against the actual checked-in R13R2 implementation.
    source = open(path, encoding="utf-8-sig").read()
    updated, needed = installer.render(source)
    if needed:
        assert installer.NEW_IMPORT in updated and installer.NEW_BODY in updated
        assert installer.render(updated) == (updated, False)
    else:
        assert installer.NEW_IMPORT in source and installer.NEW_BODY in source
    import pytest
    with pytest.raises(RuntimeError, match="PARTIAL"):
        installer.render(installer.NEW_IMPORT + installer.OLD_BODY)
```

## run.ps1 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$arguments = @('-m', 'phase175_r4r12r13r7_typed_nu_prime_notation.audit', '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q --import-mode=importlib phase175_r4r12r13r7_typed_nu_prime_notation/tests/test_r13r7_notation.py phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py phase175_r4r12r13r3_public_delta_e_bridge/tests/test_provider.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
```

