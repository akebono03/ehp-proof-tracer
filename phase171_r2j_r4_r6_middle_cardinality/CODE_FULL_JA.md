# Phase 171 R2J-R4-R6 — 変更コード全文

今回の変更は新規ファイルのみです。既存ファイルの import、クラス、関数、テストは変更しません。コード中の省略はありません。

## `source.py`

```python
"""Infer the finite cardinality of the middle group of a short exact sequence.

No fixed group result or proof leaf is created here.  This generic rule
requires independently supported finite cyclic end-group presentations.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r5_short_exact_sequence.source import EHPShortExactSequence
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


@dataclass(frozen=True)
class FiniteGroupCardinality:
    """Typed statement: the finite group has exactly ``order`` elements."""

    group: TodaPrimaryGroup
    order: int


def cardinality_from_short_exact(
    left: object, sequence: object, right: object,
) -> FiniteGroupCardinality | None:
    """Apply |B|=|A||C| only to correctly matched finite end groups.

    This function constructs a candidate conclusion.  It is not evidence;
    the inference rule additionally requires proof steps for all inputs.
    """
    if not isinstance(sequence, EHPShortExactSequence):
        return None
    if not all(
        isinstance(statement, Relation)
        and statement.relation_type is RelationType.EQUALITY
        and isinstance(statement.lhs, TodaPrimaryGroup)
        and isinstance(statement.rhs, FiniteCyclicGroup)
        and type(statement.rhs.order) is int
        and statement.rhs.order > 0
        for statement in (left, right)
    ):
        return None
    if left.lhs != sequence.source_group or right.lhs != sequence.target_group:
        return None
    if (
        sequence.injection.source_group != sequence.source_group
        or sequence.injection.target_group != sequence.middle_group
        or sequence.projection.source_group != sequence.middle_group
        or sequence.projection.target_group != sequence.target_group
    ):
        return None
    return FiniteGroupCardinality(
        group=sequence.middle_group,
        order=left.rhs.order * right.rhs.order,
    )


def finite_cardinality_from_short_exact_rule(
    goal: FiniteGroupCardinality,
) -> InferenceRule:
    """Require a short-exact INFERENCE and verified end-group statements."""
    if (
        not isinstance(goal, FiniteGroupCardinality)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or type(goal.order) is not int
        or goal.order <= 0
    ):
        raise ValueError("a positive typed finite-cardinality goal is required")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].rule is ProofRule.INFERENCE
            and premises[2].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and cardinality_from_short_exact(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite middle-group cardinality from short exact sequence",
        premise_patterns=(
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=EHPShortExactSequence,
            ),
            PremisePattern(statement_type=Relation, relation_type=RelationType.EQUALITY),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_finite_cardinality_from_short_exact(
    goal: object,
    left: object,
    sequence: object,
    right: object,
) -> tuple[GoalExpansion, ...]:
    """Return one backward proof obligation, never a fact from a database."""
    if (
        not isinstance(goal, FiniteGroupCardinality)
        or cardinality_from_short_exact(left, sequence, right) != goal
    ):
        return ()
    return (GoalExpansion(
        finite_cardinality_from_short_exact_rule(goal),
        (left, sequence, right),
    ),)
```

## `audit.py`

```python
"""R2J-R4-R6: replay cardinality of pi_6^3 from a proved short exact EHP sequence.

The pi_5^2 group is a uniquely screened earlier Proposition 5.6
component, not the pi_6^3 target.  The pi_6^5 group is an INFERENCE
already inside the genuine R4-R5 proof tree.  No group structure of
the middle term and no order-four generator is assumed or concluded.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r5_short_exact_sequence.audit import (
    _screened_leaf_ids,
    build_short_exact_proof,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    cardinality_from_short_exact,
    expand_finite_cardinality_from_short_exact,
    finite_cardinality_from_short_exact_rule,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
PRIOR_SUFFIX = "boundary:Proposition 5.6:pi5_2_group_relation"


def _git(*arguments: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in permitted:
        raise ValueError("only read-only Git operations are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def screened_prior_pi52(screened, citing: str):
    """Select exactly one earlier fixed GIVEN for pi_5^2, not a DB goal.

    Identifiers may carry a ``shared:N:`` registry prefix.  The
    literature position and typed contents must also agree.
    """
    matches = []
    for link in screened.proof_links:
        if not (
            link.assertion_id == PRIOR_SUFFIX
            or link.assertion_id.endswith(":" + PRIOR_SUFFIX)
        ):
            continue
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and isinstance(step.conclusion, Relation)
            and step.conclusion.relation_type is RelationType.EQUALITY
            and step.conclusion.lhs == TodaPrimaryGroup(5, 2)
            and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
            and type(step.conclusion.rhs.order) is int
            and step.conclusion.rhs.order > 0
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 5.6"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matches.append(link)
    if len(matches) != 1:
        raise RuntimeError("unique earlier, source-screened pi_5^2 component is required")
    return matches[0]


def proven_right_group_from_short_exact(root: ProofStep) -> ProofStep:
    """Reuse the genuine pi_6^5 inference within the R4-R5 H proof branch."""
    if root.rule is not ProofRule.INFERENCE or len(root.premises) != 3:
        raise RuntimeError("short-exact root has wrong inferred ancestry")
    hopf_root = root.premises[2]
    if hopf_root.rule is not ProofRule.INFERENCE or len(hopf_root.premises) != 2:
        raise RuntimeError("Hopf surjectivity proof branch is not complete")
    group_root = hopf_root.premises[0]
    if (
        group_root.rule is not ProofRule.INFERENCE
        or not isinstance(group_root.conclusion, Relation)
        or group_root.conclusion.relation_type is not RelationType.EQUALITY
        or group_root.conclusion.lhs != TodaPrimaryGroup(6, 5)
        or not isinstance(group_root.conclusion.rhs, FiniteCyclicGroup)
        or len(group_root.premises) != 1
        or group_root.premises[0].rule is not ProofRule.GIVEN
    ):
        raise RuntimeError("pi_6^5 group must be a proved source-specialized relation")
    return group_root


def build_middle_cardinality_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Attach an earlier pi_5^2 fact to the R4-R5 proof without new GIVENs."""
    screened, pi63_goal, citing = _screened_context()
    left = screened_prior_pi52(screened, citing)
    exact_root, _, _ = build_short_exact_proof()
    right = proven_right_group_from_short_exact(exact_root)
    goal = cardinality_from_short_exact(
        left.step.conclusion, exact_root.conclusion, right.conclusion,
    )
    if goal is None or goal.group != TodaPrimaryGroup(6, 3) or goal.order != 4:
        raise RuntimeError("finite end-group data do not yield pi_6^3 of order four")
    proposals = expand_finite_cardinality_from_short_exact(
        goal, left.step.conclusion, exact_root.conclusion, right.conclusion,
    )
    if len(proposals) != 1 or proposals[0].subgoals != (
        left.step.conclusion, exact_root.conclusion, right.conclusion,
    ):
        raise RuntimeError("finite cardinality backward obligation not unique")
    parents = (left.step, exact_root, right)
    rule = finite_cardinality_from_short_exact_rule(goal)
    matches = tuple(
        item for item in find_inference_matches_for_rule(rule, parents)
        if len(item.premises) == 3
        and all(a is b for a, b in zip(item.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique typed cardinality inference match")
    root = derive_inference_proof_step(matches[0])
    nodes = proof_ancestry(root)
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    ids = _screened_leaf_ids(screened, citing, leaves)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != goal
        or root.premises != parents
        or left.assertion_id not in ids
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
        or any(node.rule is ProofRule.GIVEN and node.conclusion == goal for node in nodes)
    ):
        raise RuntimeError("cardinality proof has a fabricated premise or target-group result")
    report = {
        "phase": "171-R2J-R4-R6",
        "mode": "READ_ONLY_TYPED_MIDDLE_CARDINALITY_REPLAY",
        "status": "INFERRED",
        "prior_pi52_assertion_id": left.assertion_id,
        "prior_pi52_relation": repr(left.step.conclusion),
        "pi65_derived_relation": repr(right.conclusion),
        "short_exact": repr(exact_root.conclusion),
        "conclusion": repr(root.conclusion),
        "cardinality": goal.order,
        "root_inference_rule": rule.name,
        "inferences": sum(node.rule is ProofRule.INFERENCE for node in nodes),
        "given_leaves": len(leaves),
        "verified_source_ids": list(dict.fromkeys(ids)),
        "new_given_added": 0,
        "nu_prime_order_four_proven": False,
        "pi63_group_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R4-R6 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (ROOT / "phase171_r2j_r4_r5_short_exact_sequence" / "audit.py").is_file():
        raise RuntimeError("R4-R5 must exist in the worktree")
    print("PHASE171_R2J_R4_R6_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R6_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R6_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, nodes, report = build_middle_cardinality_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R6_MIDDLE_CARDINALITY=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R6_CARDINALITY=" + str(report["cardinality"]), flush=True)
    print("PHASE171_R2J_R4_R6_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R6_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R6_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R6_NU_PRIME_ORDER_FOUR_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R6_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R6_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R6_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R6_RUN=PASS", flush=True)
    print("PHASE171_R2J_R4_R6_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused mathematical, matcher, source-boundary and replay checks for R4-R6."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r5_short_exact_sequence.source import short_exact_from_ehp
from phase171_r2j_r4_r6_middle_cardinality.audit import (
    _git,
    build_middle_cardinality_proof,
    screened_prior_pi52,
)
from phase171_r2j_r4_r6_middle_cardinality.source import (
    FiniteGroupCardinality,
    cardinality_from_short_exact,
    expand_finite_cardinality_from_short_exact,
    finite_cardinality_from_short_exact_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _fixture():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    element_a = HomotopyElement(
        name="a", dimension=2, source=5, target=2,
        generator=GeneratorSymbol(family="a", index=2),
    )
    element_c = HomotopyElement(
        name="c", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="c", index=5),
    )
    left = Relation(a, FiniteCyclicGroup(2, element_a), RelationType.EQUALITY)
    right = Relation(c, FiniteCyclicGroup(2, element_c), RelationType.EQUALITY)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    sequence = short_exact_from_ehp(
        MapInjective(TodaSuspensionMap(a, b)),
        exact,
        MapSurjective(TodaHopfInvariantMap(b, c)),
    )
    assert sequence is not None
    return left, sequence, right


def test_generic_cardinality_product_without_middle_group_presentation():
    left, sequence, right = _fixture()
    value = cardinality_from_short_exact(left, sequence, right)
    assert value == FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    assert value.group == sequence.middle_group
    assert len(expand_finite_cardinality_from_short_exact(value, left, sequence, right)) == 1


def test_mixed_source_and_inference_steps_produce_real_inference():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    steps = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(
        finite_cardinality_from_short_exact_rule(goal), steps,
    )
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == steps
    assert result.conclusion == goal


def test_permuted_available_premises_match_in_canonical_order():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    steps = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(
        finite_cardinality_from_short_exact_rule(goal),
        (steps[2], steps[0], steps[1]),
    )
    assert len(matches) == 1
    assert matches[0].premises == steps


def test_bad_end_group_coordinates_and_fake_cardinality_are_rejected():
    left, sequence, right = _fixture()
    wrong_left = replace(left, lhs=TodaPrimaryGroup(6, 2))
    wrong_right = replace(right, lhs=TodaPrimaryGroup(7, 5))
    assert cardinality_from_short_exact(wrong_left, sequence, right) is None
    assert cardinality_from_short_exact(left, sequence, wrong_right) is None
    goal = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 5)
    assert expand_finite_cardinality_from_short_exact(goal, left, sequence, right) == ()


def test_wrong_sequence_map_endpoints_are_rejected():
    left, sequence, right = _fixture()
    bad = replace(sequence, injection=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    assert cardinality_from_short_exact(left, bad, right) is None
    bad = replace(sequence, projection=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))
    assert cardinality_from_short_exact(left, bad, right) is None


def test_unproved_short_exact_or_forged_group_leaf_is_rejected():
    left, sequence, right = _fixture()
    goal = cardinality_from_short_exact(left, sequence, right)
    assert goal is not None
    rule = finite_cardinality_from_short_exact_rule(goal)
    valid = (
        ProofStep(left, (), ProofRule.GIVEN),
        ProofStep(sequence, (), ProofRule.INFERENCE),
        ProofStep(right, (), ProofRule.INFERENCE),
    )
    assert find_inference_matches_for_rule(rule, (
        valid[0], ProofStep(sequence, (), ProofRule.GIVEN), valid[2],
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        valid[0], valid[1], ProofStep(right, (), ProofRule.RELATION),
    )) == ()


def test_positive_integer_cardinality_and_cyclic_orders_required():
    left, sequence, right = _fixture()
    assert cardinality_from_short_exact(
        replace(left, rhs=FiniteCyclicGroup(True, left.rhs.generator)),
        sequence, right,
    ) is None
    assert cardinality_from_short_exact(
        left, sequence, replace(right, rhs=FiniteCyclicGroup(0, right.rhs.generator)),
    ) is None
    with pytest.raises(ValueError):
        finite_cardinality_from_short_exact_rule(FiniteGroupCardinality(
            TodaPrimaryGroup(6, 3), 0,
        ))
    assert expand_finite_cardinality_from_short_exact(object(), left, sequence, right) == ()


def test_real_prior_proposition56_source_is_unique_and_earlier():
    screened, goal, citing = _screened_context()
    link = screened_prior_pi52(screened, citing)
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.conclusion.lhs == TodaPrimaryGroup(5, 2)
    assert link.step.conclusion.rhs.order == 2
    assert precedes_citing_assertion(screened, link.assertion_id, citing)
    assert link.step.conclusion != goal


def test_read_only_git_guard_rejects_mutating_commands():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_replay_uses_prior_source_and_inferred_cyclic_codomain():
    root, nodes, report = build_middle_cardinality_proof()
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    assert root.premises[0].rule is ProofRule.GIVEN
    assert root.premises[1].rule is ProofRule.INFERENCE
    assert root.premises[2].rule is ProofRule.INFERENCE
    assert report["status"] == "INFERRED"
    assert report["cardinality"] == 4
    assert report["new_given_added"] == 0
    assert report["nu_prime_order_four_proven"] is False
    assert report["pi63_group_proven"] is False
    assert sum(node.rule is ProofRule.GIVEN for node in nodes) >= 3
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r6_middle_cardinality.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R4_R6_RESULT=PASS_DRY_RUN'
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py `
        phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R4_R6_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r6_middle_cardinality.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R4-R6 cardinality proof replay failed' }
    Write-Output 'PHASE171_R2J_R4_R6_RESULT=PASS_AUDIT_ONLY'
}
finally {
    Pop-Location
}
```

## `README.md`

```markdown
# Phase 171 R2J-R4-R6 — Finite Cardinality of the Middle Group

This read-only package derives the **cardinality**, not a cyclic presentation, of the EHP middle group from an already inferred short exact sequence and two finite cyclic end-group presentations.

For the Phase 171 instance, the prior source component of Toda Proposition 5.6 identifies `pi_5^2` as a group of order two; that component must be a unique citation-screened earlier `GIVEN`. The `pi_6^5` order-two presentation must be an `INFERENCE` already embedded in the Phase 171 R4-R5 proof tree, ultimately derived from Toda Proposition 5.1. The short exact sequence must itself be inferred from verified EHP exactness and map properties.

The generic rule yields `FiniteGroupCardinality(TodaPrimaryGroup(6,3),4)`. It does not establish the order of `nu-prime` or `pi_6^3 = Z/4{nu-prime}`. It introduces no new `GIVEN`, changes no production source, and does not treat a database target as an axiom. Earlier proof results are reused; their proofs are not required to be repeated in the body of a final narrative.

## Files

- `source.py`: complete generic typed cardinality statement, checked consequence, inference rule, and backward-goal expansion.
- `audit.py`: independent cited-source screening and actual proof-tree reconstruction.
- `tests/test_audit.py`: 10 focused tests, including negative cases and an active end-to-end replay.
- `run.ps1`: preflight, focused pytest, and actual read-only audit.
- `CODE_FULL_JA.md`: full new code and test bodies, including imports.
- `監査仕様.md`: Japanese audit specification.

## Windows PowerShell

From the repository root, extract the accompanying ZIP into `.` and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r6_middle_cardinality\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r6_middle_cardinality\run.ps1"
git status -sb
git diff --stat
```

The runner intentionally does not run the full test suite; reserve that for Phase 171 closeout. Existing files, staging, Git history, and production providers are unchanged.
```

## `監査仕様.md`

```markdown
# Phase 171 R2J-R4-R6 — 位数4の型付き推論監査

## 目的と範囲

R2J-R4-R5 で証明した短完全列

$$
0\longrightarrow\pi_5^2\xrightarrow{E}\pi_6^3\xrightarrow{H}\pi_6^5\longrightarrow0
$$

に両端の位数2の群構造を接続し、位数の積の公式から

$$
|\pi_6^3|=|\pi_5^2|\,|\pi_6^5|=2\cdot2=4
$$

を `INFERENCE` として生成する。これは巡回群の構造や $\nu'$ の位数4を示すものではない。

## 証拠の境界

- $\pi_5^2$ の群構造は Toda Proposition 5.6 に記録された、$\pi_6^3$ の引用対象より**先行する成分**であり、型・出典・順序を確認した `GIVEN` として採用する。証明の再探索は要求しない。
- $\pi_6^5$ の群構造は Toda Proposition 5.1 の一般規則を特殊化した `INFERENCE` を R4-R5 の証明木からそのまま再利用する。
- 短完全列は R4-R5 で導出した `INFERENCE` とする。
- 出典付き `GIVEN` 葉は既存の一意な登録 ID に対応し、引用境界より前に存在しなければならない。
- 群名や表示文字列だけでは前提の整合性を認めない。始域・終域・写像の対応、有限巡回群の位数を型付きで検証する。
- `pi_6^3` の DB Goal や Proposition 5.6 の目標成分を前提として採用しない。

## 変更ファイル・追加位置

新規ディレクトリ `phase171_r2j_r4_r6_middle_cardinality/` をリポジトリ直下に追加する。`source.py` に `FiniteGroupCardinality`、`cardinality_from_short_exact()`、`finite_cardinality_from_short_exact_rule()`、`expand_finite_cardinality_from_short_exact()` を新規追加する。`audit.py` に `_git()`、`screened_prior_pi52()`、`proven_right_group_from_short_exact()`、`build_middle_cardinality_proof()`、`main()` を新規追加する。`tests/test_audit.py` に `_fixture()` と10個のテスト関数を新規追加する。`run.ps1`、`README.md`、この監査仕様、`CODE_FULL_JA.md`、`__init__.py` 2ファイルを新規追加する。

既存ファイルを変更する必要はない。import 部分、クラス、関数、テストは `CODE_FULL_JA.md` で全文提示する。

## 実行する pytest

```powershell
python -B -m pytest -q -p no:cacheprovider `
  phase171_r2j_r4_r6_middle_cardinality/tests/test_audit.py `
  phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py
```

限定テストは新規10件と R4-R5 の関連9件の計19件。全体 pytest は Phase 171 終了時のみ。

## 完了条件

1. DryRun が PASS。
2. 限定 pytest が PASS。
3. `PHASE171_R2J_R4_R6_MIDDLE_CARDINALITY=INFERRED`、`PHASE171_R2J_R4_R6_CARDINALITY=4`。
4. `PHASE171_R2J_R4_R6_NEW_GIVEN=0`、`PHASE171_R2J_R4_R6_PI63_PROVEN=False`。
5. 既存追跡ファイルの状態が変わらない。

## 次 Phase との境界

次段階では、すでに導出した $2\nu'=E(\eta_2^3)$、$E$ の単射性、$\pi_5^2=\mathbb Z/2\{\eta_2^3\}$ を使い、$2\nu'\ne0$ すなわち $\nu'$ の位数4を推論する。今回の R4-R6 で先取りしない。
```
