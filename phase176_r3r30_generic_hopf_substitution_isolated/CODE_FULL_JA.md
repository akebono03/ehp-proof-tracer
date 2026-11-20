# R3R30 新規ファイル全文

## source.py

```python
"""General, type-checked substitution into cited Toda Proposition 2.2.

This module creates no GIVEN and does not assert any particular Hopf image.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, _formula_parts,
)
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import (
    InferenceRule, PremisePattern, ProofRule, Relation, RelationType,
)


def generic_hopf_substitution_inputs(
    goal: object,
) -> tuple[Relation, Relation] | None:
    """Derive the two *independent* proof obligations for H(α∘Eβ)=δ∘Eβ."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.rhs, Composition)):
        return None
    product = goal.lhs.expression
    alpha = product.left
    right = product.right
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, HomotopyElement)
            or goal.rhs.right != right):
        return None
    delta = goal.rhs.left
    endpoints = expression_endpoints(delta)
    beta_endpoints = expression_endpoints(right.expression)
    if endpoints is None or beta_endpoints is None:
        return None
    suspended = (beta_endpoints[0] + 1, beta_endpoints[1] + 1)
    if endpoints[0] != suspended[1]:
        return None
    formula = Relation(
        goal.lhs, Composition(MapApplication(EHP_H_MAP, alpha), right),
        RelationType.EQUALITY,
    )
    if _formula_parts(formula) != (alpha, right.expression):
        return None
    hopf_value = Relation(
        MapApplication(EHP_H_MAP, alpha), delta, RelationType.EQUALITY,
    )
    return formula, hopf_value


def generic_hopf_substitution_rule(goal: Relation) -> InferenceRule:
    """Keep both required premises checked by ordinary verified proof search."""
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed right-Hopf substitution goal")
    formula, hopf_value = inputs

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == formula
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].conclusion == hopf_value
            and generic_hopf_substitution_inputs(goal) == inputs
        )

    return InferenceRule(
        name="substitute independently proved Hopf value into cited right formula",
        description=(
            "From a proved instance H(alpha o E beta)=H(alpha) o E beta "
            "and an independently proved H(alpha)=delta, conclude "
            "H(alpha o E beta)=delta o E beta."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                statement_pattern=formula,
            ),
            PremisePattern(
                statement_type=Relation,
                statement_pattern=hopf_value,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_generic_hopf_substitution(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Never treat a desired Hopf value as an available GIVEN."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    inputs = generic_hopf_substitution_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(generic_hopf_substitution_rule(goal), inputs),)
```

## audit.py

```python
"""R3R30 isolated audit; no production files are modified."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r30_generic_hopf_substitution_isolated.source import (
    generic_hopf_substitution_inputs, expand_generic_hopf_substitution,
)
from proof import Relation, RelationType

ROOT = Path(__file__).resolve().parent.parent


def inspect(dry_run: bool) -> dict:
    result = subprocess.run(
        ["git", "branch", "--show-current"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode or result.stdout.strip() != "develop":
        raise RuntimeError("expected develop checkout")
    if dry_run:
        return {"gate": "PASS_R3R30_DRYRUN", "full_pytest": "NOT_RUN"}
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    alpha = Composition(nu, eta6)
    right = Suspension(eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(Composition(eta5, eta6), right),
        RelationType.EQUALITY,
    )
    proposals = expand_generic_hopf_substitution(goal, (TodaProp22RightFormula(),))
    return {
        "gate": "PASS_R3R30_ISOLATED_GENERAL_SUBSTITUTION",
        "candidate_count": len(proposals),
        "subgoal_count": len(proposals[0].subgoals) if proposals else 0,
        "subgoals": [repr(x) for x in proposals[0].subgoals] if proposals else [],
        "no_direct_hopf_value_given": True,
        "public_provider_modified": False,
        "new_given": 0,
        "root_proof_complete_claimed": False,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        result = inspect(args.dry_run)
    except Exception as exc:
        result = {"gate": "FAIL_R3R30", "error": str(exc), "full_pytest": "NOT_RUN"}
    location = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
                / "EHPProofTracerAudit"
                / "phase176_r3r30_generic_hopf_substitution_isolated")
    location.mkdir(parents=True, exist_ok=True)
    path = location / "report.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    for key, value in result.items():
        print("PHASE176_R3R30_" + key.upper() + "=" + str(value))
    print("PHASE176_R3R30_REPORT=" + str(path))
    print("(END)")
    return 0 if result["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_source.py

```python
"""R3R30 focused contracts: independent proof obligations, no forged facts."""
from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r30_generic_hopf_substitution_isolated.source import (
    expand_generic_hopf_substitution, generic_hopf_substitution_inputs,
    generic_hopf_substitution_rule,
)
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule, apply_inference_match,
)


def elements():
    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    return nu, eta5, eta6


def goal_and_inputs():
    nu, eta5, eta6 = elements()
    alpha = Composition(nu, eta6)
    right = Suspension(eta6)
    delta = Composition(eta5, eta6)
    goal = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(delta, right),
        RelationType.EQUALITY,
    )
    inputs = generic_hopf_substitution_inputs(goal)
    assert inputs is not None
    return goal, inputs


def test_two_independent_subgoals_for_composite_left() -> None:
    goal, inputs = goal_and_inputs()
    choices = expand_generic_hopf_substitution(goal, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].subgoals == inputs
    assert inputs[0].lhs == goal.lhs
    assert inputs[1].lhs.expression == goal.lhs.expression.left


def test_proved_formula_and_hopf_value_close_by_inference() -> None:
    goal, (formula, hopf_value) = goal_and_inputs()
    rule = generic_hopf_substitution_rule(goal)
    premises = (ProofStep(formula, (), ProofRule.INFERENCE),
                ProofStep(hopf_value, (), ProofRule.INFERENCE))
    matches = find_inference_matches_for_rule(rule, premises)
    assert len(matches) == 1
    result = apply_inference_match(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == premises


def test_wrong_hopf_value_or_unproved_formula_rejected() -> None:
    goal, (formula, hopf_value) = goal_and_inputs()
    rule = generic_hopf_substitution_rule(goal)
    cited = ProofStep(formula, (), ProofRule.INFERENCE)
    wrong = ProofStep(replace(hopf_value, rhs=elements()[1]), (), ProofRule.INFERENCE)
    assert not find_inference_matches_for_rule(rule, (cited, wrong))
    direct_formula = ProofStep(formula, (), ProofRule.GIVEN)
    genuine_hopf = ProofStep(hopf_value, (), ProofRule.INFERENCE)
    assert not find_inference_matches_for_rule(rule, (direct_formula, genuine_hopf))


def test_cited_general_formula_required() -> None:
    goal, _ = goal_and_inputs()
    assert expand_generic_hopf_substitution(goal, ()) == ()
    assert expand_generic_hopf_substitution(
        goal, (TodaProp22RightFormula(), TodaProp22RightFormula()),
    ) == ()


def test_type_and_rhs_fail_closed() -> None:
    goal, _ = goal_and_inputs()
    assert generic_hopf_substitution_inputs(replace(goal, rhs=goal.rhs.left)) is None
    assert generic_hopf_substitution_inputs(
        replace(goal, rhs=Composition(goal.rhs.left, elements()[1]))
    ) is None
    with pytest.raises(ValueError):
        generic_hopf_substitution_rule(replace(goal, rhs=goal.rhs.left))
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
Push-Location (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
try {
    if ($DryRun) {
        python -B -m phase176_r3r30_generic_hopf_substitution_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw "R3R30 DryRun failed" }
    } else {
        python -B -m phase176_r3r30_generic_hopf_substitution_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw "R3R30 audit failed" }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r30_generic_hopf_substitution_isolated\tests `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw "R3R30 focused tests failed" }
        Write-Host "PHASE176_R3R30_GATE=PASS_R3R30_FOCUSED_TESTS"
        Write-Host "PHASE176_R3R30_FULL_PYTEST=NOT_RUN"
        Write-Host "(END)"
    }
} finally {
    Pop-Location
}
```
