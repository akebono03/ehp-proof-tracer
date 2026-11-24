# Phase 176 R3R34 追加コード全文

既存ファイルの編集・import 変更なし。リポジトリ直下に新規ディレクトリを配置する。

## `source.py` 全文

```python
"""A verified composite suspension image implies an element equality.

Isolated, general bridge: neither a special eta fact nor a GIVEN is created.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, Suspension
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


def composite_suspension_equality_input(goal: object) -> GeneratorImage | None:
    """Require typed composite factors and the same degree-one E-image."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Suspension)
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)):
        return None
    source = goal.lhs.expression
    target = goal.rhs
    if not all(isinstance(factor, HomotopyElement) for factor in
               (source.left, source.right, target.left, target.right)):
        return None
    endpoints_source = expression_endpoints(source)
    endpoints_target = expression_endpoints(target)
    if (endpoints_source is None or endpoints_target is None
            or endpoints_target !=
            (endpoints_source[0] + 1, endpoints_source[1] + 1)):
        return None
    if (not isinstance(endpoints_source[0], int)
            or not isinstance(endpoints_source[1], int)
            or endpoints_source[1] < 2):
        return None
    degree, sphere = endpoints_source
    return GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(degree, sphere),
            TodaPrimaryGroup(degree + 1, sphere + 1),
        ),
        source,
        target,
    )


def composite_suspension_equality_rule(goal: Relation) -> InferenceRule:
    """Keep the composite image as an independently proved premise."""
    required = composite_suspension_equality_input(goal)
    if required is None:
        raise ValueError("not a well-typed composite suspension equality")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required
            and composite_suspension_equality_input(goal) == required
        )

    return InferenceRule(
        name="proved composite suspension image yields typed element equality",
        description=(
            "An independently proved E-image of a typed composite "
            "identifies its suspension with the same target composite."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=GeneratorImage,
            statement_pattern=required,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_composite_suspension_equality(goal: object) -> tuple[GoalExpansion, ...]:
    """Return an open backward obligation, never a verified proof step."""
    required = composite_suspension_equality_input(goal)
    if required is None:
        return ()
    return (GoalExpansion(composite_suspension_equality_rule(goal), (required,)),)

```

## `audit.py` 全文

```python
"""Read-only R3R34 dependency and frontier report."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "phase176_r3r34_composite_suspension_isolated"


def preflight() -> dict:
    command = subprocess.run(("git", "branch", "--show-current"), cwd=ROOT,
                             capture_output=True, text=True)
    if command.returncode or command.stdout.strip() != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    paths = (
        "phase171_r2h_prop22_cited_hopf/source.py",
        "phase165_r12_r21_eta_generator_chain.py",
        "phase176_r3r30_generic_hopf_substitution_isolated/source.py",
        "phase165_r52_r9_shared_math.py",
    )
    for path in paths:
        if not (ROOT / path).is_file():
            raise RuntimeError("MISSING_DEPENDENCY: " + path)
    return {"develop": True, "required_sources": list(paths)}


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
    from proof import Relation, RelationType
    from phase176_r3r34_composite_suspension_isolated.source import (
        expand_composite_suspension_equality,
    )
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    e5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    e6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    e7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    goal = Relation(Suspension(Composition(e5, e6)), Composition(e6, e7), RelationType.EQUALITY)
    branch = expand_composite_suspension_equality(goal)
    if len(branch) != 1:
        raise RuntimeError("ISOLATED_BRANCH_NOT_FOUND")
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(screened, proof_target=roots[0])
    image = branch[0].subgoals[0]
    return {
        "isolated_rule": branch[0].rule.name,
        "isolated_subgoals": len(branch[0].subgoals),
        "existing_image_candidate_rules": [x.rule.name for x in provider(image)],
        "existing_equality_candidate_rules": [x.rule.name for x in provider(goal)],
        "shared_provider_modified": False,
        "proof_completed": False,
        "root_group_proved": False,
    }


def run(dry_run: bool) -> int:
    report = {"gate": "FAIL_R3R34", "full_pytest": "NOT_RUN", "new_given": 0,
              "production_modified": False}
    try:
        report["preflight"] = preflight()
        if dry_run:
            report["gate"] = "PASS_R3R34_DRYRUN"
        else:
            report["frontier"] = probe()
            report["gate"] = "PASS_R3R34_ISOLATED_BRIDGE_NOT_CONNECTED"
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / "report.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R34_GATE=" + report["gate"])
    for key, value in report.get("frontier", {}).items():
        print("PHASE176_R3R34_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R34_ERROR=" + report["error"])
    print("REPORT=" + str(output))
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## `tests/test_source.py` 全文

```python
from expression import Composition, GeneratorSymbol, HomotopyElement, Suspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase176_r3r34_composite_suspension_isolated.source import (
    composite_suspension_equality_input,
    expand_composite_suspension_equality,
)
from proof import ProofRule, Relation, RelationType, ProofStep


def elements():
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    return eta5, eta6, eta7


def goal():
    a, b, c = elements()
    # Source endpoints (7,5); target endpoints (8,6).
    return Relation(Suspension(Composition(a, b)),
                    Composition(b, c), RelationType.EQUALITY)


def test_composite_image_is_independent_subgoal():
    candidate = composite_suspension_equality_input(goal())
    assert isinstance(candidate, GeneratorImage)
    assert candidate.source_generator == goal().lhs.expression
    assert candidate.target_generator == goal().rhs
    options = expand_composite_suspension_equality(goal())
    assert len(options) == 1
    assert options[0].subgoals == (candidate,)


def test_rejects_mismatched_target():
    a, b, c = elements()
    wrong = Relation(Suspension(Composition(a, b)),
                     Composition(a, c), RelationType.EQUALITY)
    assert expand_composite_suspension_equality(wrong) == ()


def test_rejects_reversed_equality():
    original = goal()
    reversed_goal = Relation(original.rhs, original.lhs, RelationType.EQUALITY)
    assert expand_composite_suspension_equality(reversed_goal) == ()


def test_requires_inferred_proof_not_given():
    option = expand_composite_suspension_equality(goal())[0]
    premise = option.subgoals[0]
    guard = option.rule.match_guard
    assert guard((ProofStep(conclusion=premise, premises=(), rule=ProofRule.GIVEN),), {}) is False
    assert guard((ProofStep(conclusion=premise, premises=(), rule=ProofRule.INFERENCE),), {}) is True

```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $audit = Join-Path $PSScriptRoot 'audit.py'
    $auditArgs = @($audit)
    if ($DryRun) { $auditArgs += '--dry-run' }
    & python @auditArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R34 audit failed' }
    if (-not $DryRun) {
        $focused = Join-Path (Join-Path $PSScriptRoot 'tests') 'test_source.py'
        & python -m pytest -q -p no:cacheprovider $focused
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 isolated pytest failed' }
        & python -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 existing Hopf pytest failed' }
    }
} finally {
    Pop-Location
}

```

