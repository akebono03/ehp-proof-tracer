# Phase 176 R3R36 — 新規コード全文

本 Phase では既存コードの import、クラス、関数を変更していない。以下は、新規ファイルの全文である。

## `source.py`

```python
"""Isolated, source-dependent right-Hopf formula for a composite beta.

The existing single-element Toda Proposition 2.2 path remains unchanged.
No desired Hopf value, group structure, or reference is registered as GIVEN.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType


COMPOSITE_FORMULA_RULE_NAME = "specialize cited Toda Proposition 2.2 for a composite right factor"
COMPOSITE_SUBSTITUTION_RULE_NAME = "substitute proved Hopf image into composite right formula"


def composite_right_formula_parts(goal: object) -> tuple[object, Composition] | None:
    """Recognize H(alpha o E beta) = H(alpha) o E beta for typed composite beta.

    `Suspension(Composition(...))` has no endpoints in the legacy Expression
    class, so determine its sphere dimensions from the typed, *unsuspended*
    composite, rather than interpreting absent endpoints as a valid match.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)):
        return None
    product = goal.lhs.expression
    alpha = product.left
    right = product.right
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, Composition)):
        return None
    beta = right.expression
    alpha_endpoints = expression_endpoints(alpha)
    beta_endpoints = expression_endpoints(beta)
    if (alpha_endpoints is None or beta_endpoints is None
            or alpha_endpoints[0] != beta_endpoints[1] + 1):
        return None
    expected_rhs = Composition(MapApplication(EHP_H_MAP, alpha), right)
    return (alpha, beta) if goal.rhs == expected_rhs else None


def composite_right_formula_rule(goal: Relation) -> InferenceRule:
    """Require the independently screened universal source for specialization."""
    if composite_right_formula_parts(goal) is None:
        raise ValueError("not a typed composite-right Toda Proposition 2.2 formula")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == TodaProp22RightFormula()
            and composite_right_formula_parts(goal) is not None
        )

    return InferenceRule(
        name=COMPOSITE_FORMULA_RULE_NAME,
        description=(
            "Specialize the independently cited universal right-Hopf formula "
            "when its suspended right factor is a typed composite."
        ),
        premise_patterns=(PremisePattern(
            statement_type=TodaProp22RightFormula,
            statement_pattern=TodaProp22RightFormula(),
            proof_rule=ProofRule.GIVEN,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def composite_hopf_substitution_inputs(
    goal: object,
) -> tuple[Relation, Relation] | None:
    """Return the cited formula and independent H(alpha)=delta obligations.

    The value delta is checked against the canonical degree of the EHP H map:
    an element S^q -> S^n has H-value S^q -> S^(2n-1). The right-hand
    composite must retain the suspended beta verbatim.
    """
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
    delta = goal.rhs.left
    if (not isinstance(alpha, (HomotopyElement, Composition))
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, Composition)
            or goal.rhs.right != right):
        return None
    alpha_endpoints = expression_endpoints(alpha)
    delta_endpoints = expression_endpoints(delta)
    beta_endpoints = expression_endpoints(right.expression)
    if (alpha_endpoints is None or delta_endpoints is None
            or beta_endpoints is None):
        return None
    if alpha_endpoints[0] != beta_endpoints[1] + 1:
        return None
    if delta_endpoints != (alpha_endpoints[0], 2 * alpha_endpoints[1] - 1):
        return None
    formula = Relation(
        lhs=goal.lhs,
        rhs=Composition(MapApplication(EHP_H_MAP, alpha), right),
        relation_type=RelationType.EQUALITY,
    )
    if composite_right_formula_parts(formula) != (alpha, right.expression):
        return None
    hopf_value = Relation(
        lhs=MapApplication(EHP_H_MAP, alpha),
        rhs=delta,
        relation_type=RelationType.EQUALITY,
    )
    return formula, hopf_value


def composite_hopf_substitution_rule(goal: Relation) -> InferenceRule:
    """A proof of both subgoals is mandatory; candidate generation proves none."""
    inputs = composite_hopf_substitution_inputs(goal)
    if inputs is None:
        raise ValueError("not a typed composite-right Hopf substitution goal")
    formula, hopf_value = inputs

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == formula
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[1].conclusion == hopf_value
            and composite_hopf_substitution_inputs(goal) == inputs
        )

    return InferenceRule(
        name=COMPOSITE_SUBSTITUTION_RULE_NAME,
        description=(
            "Substitute an independently proved H(alpha)=delta into a proved "
            "specialization H(alpha o E beta)=H(alpha) o E beta."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                statement_pattern=formula,
                proof_rule=ProofRule.INFERENCE,
            ),
            PremisePattern(
                statement_type=Relation,
                statement_pattern=hopf_value,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_composite_right_hopf(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer conservative backward candidates only with one screened source."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    if composite_right_formula_parts(goal) is not None:
        return (GoalExpansion(
            composite_right_formula_rule(goal),
            (TodaProp22RightFormula(),),
        ),)
    inputs = composite_hopf_substitution_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(composite_hopf_substitution_rule(goal), inputs),)
```

## `audit.py`

```python
"""R3R36 source-first, read-only audit of composite-right Hopf expansions."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = "phase176_r3r36_composite_right_hopf_isolated"
ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "phase171_r2h_prop22_cited_hopf/source.py": (
        "class TodaProp22RightFormula:",
        "def _formula_parts(",
    ),
    "phase176_r3r30_generic_hopf_substitution_isolated/source.py": (
        "def generic_hopf_substitution_inputs(",
    ),
    "phase176_r3r34_composite_suspension_isolated/source.py": (
        "def composite_suspension_equality_input(",
    ),
    "phase165_r52_r9_shared_math.py": (
        "options.extend(expand_composite_suspension_equality(goal))",
    ),
}


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ("git", *args), cwd=ROOT, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    )
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + completed.stderr.strip())
    return completed.stdout.strip()


def preflight() -> dict:
    if str(Path(run_git("rev-parse", "--show-toplevel")).resolve()).casefold() != str(ROOT.resolve()).casefold():
        raise RuntimeError("WRONG_REPOSITORY")
    if run_git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    for relative, signatures in SOURCES.items():
        file = ROOT / relative
        if not file.is_file():
            raise RuntimeError("DEPENDENCY_MISSING: " + relative)
        source = file.read_text(encoding="utf-8-sig")
        if not all(signature in source for signature in signatures):
            raise RuntimeError("DEPENDENCY_SIGNATURE_CHANGED: " + relative)
    return {"head": run_git("rev-parse", "HEAD"), "dependency_guards": len(SOURCES)}


def probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
    from phase176_r3r36_composite_right_hopf_isolated.source import (
        COMPOSITE_FORMULA_RULE_NAME,
        COMPOSITE_SUBSTITUTION_RULE_NAME,
        composite_right_formula_parts,
        composite_hopf_substitution_inputs,
        expand_cited_composite_right_hopf,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match, find_inference_match,
    )
    from unified_statement_registry import AssertionOrigin

    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    right = Suspension(Composition(eta5, eta6))
    composite = Composition(nu, right)
    formula = Relation(
        MapApplication(EHP_H_MAP, composite),
        Composition(MapApplication(EHP_H_MAP, nu), right),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        formula.lhs, Composition(eta5, right), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu), eta5, RelationType.EQUALITY)
    if composite_right_formula_parts(formula) != (nu, right.expression):
        raise RuntimeError("COMPOSITE_FORMULA_NOT_RECOGNIZED")
    if composite_hopf_substitution_inputs(substituted) != (formula, hopf):
        raise RuntimeError("COMPOSITE_SUBSTITUTION_NOT_RECOGNIZED")

    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    source_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    available = tuple(step.conclusion for step in source_steps)
    formula_candidates = expand_cited_composite_right_hopf(formula, available)
    substitution_candidates = expand_cited_composite_right_hopf(substituted, available)
    if (len(formula_candidates) != 1
            or formula_candidates[0].rule.name != COMPOSITE_FORMULA_RULE_NAME
            or len(substitution_candidates) != 1
            or substitution_candidates[0].rule.name != COMPOSITE_SUBSTITUTION_RULE_NAME
            or substitution_candidates[0].subgoals != (formula, hopf)):
        raise RuntimeError("ISOLATED_CANDIDATE_CONTRACT_FAILURE")

    universal = next((step for step in source_steps
                      if step.conclusion == TodaProp22RightFormula()), None)
    hopf_source = next((step for step in source_steps
                        if step.conclusion == hopf), None)
    formula_step = None
    substituted_step = None
    if universal is not None:
        match = find_inference_match(formula_candidates[0].rule, (universal,))
        if match is not None:
            formula_step = apply_inference_match(match)
    if formula_step is not None and hopf_source is not None:
        match = find_inference_match(
            substitution_candidates[0].rule,
            (formula_step, hopf_source),
        )
        if match is not None:
            substituted_step = apply_inference_match(match)

    existing_provider = shared_expansion_provider(screened, proof_target=roots[0])
    return {
        "gate": "PASS_R3R36_ISOLATED_CANDIDATES_AUDITED_NOT_PUBLIC",
        "root": repr(roots[0]),
        "screened_prop22_count": available.count(TodaProp22RightFormula()),
        "screened_hopf_nu_prime_count": available.count(hopf),
        "composite_formula_candidates": len(formula_candidates),
        "composite_substitution_candidates": len(substitution_candidates),
        "composite_substitution_subgoals": len(substitution_candidates[0].subgoals),
        "formula_local_replay_from_screened_given": (
            formula_step is not None and formula_step.conclusion == formula
        ),
        "substitution_local_replay_from_screened_given": (
            substituted_step is not None
            and substituted_step.conclusion == substituted
            and substituted_step.rule is ProofRule.INFERENCE
        ),
        "existing_formula_candidate_names": [
            item.rule.name for item in existing_provider(formula)
        ],
        "existing_substituted_candidate_names": [
            item.rule.name for item in existing_provider(substituted)
        ],
        "shared_provider_modified_by_r3r36": False,
        "shared_dfs_source_order_gate_verified": False,
        "transport_to_eta_cube_proved": False,
        "hopf_image_goal_proved": False,
        "root_group_proved": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def execute(dry_run: bool) -> int:
    report: dict = {"gate": "FAIL_R3R36", "full_pytest": "NOT_RUN"}
    try:
        report.update(preflight())
        if dry_run:
            report["gate"] = "PASS_R3R36_DRYRUN"
        else:
            report.update(probe())
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    file = report_path()
    file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    for key, value in report.items():
        print("PHASE176_R3R36_" + key.upper() + "=" + str(value))
    print("REPORT=" + str(file))
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_source.py`

```python
"""Focused R3R36 contracts. Synthetic ProofSteps are not source certificates."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, expand_cited_prop22_right_formula,
)
from phase176_r3r36_composite_right_hopf_isolated.source import (
    COMPOSITE_FORMULA_RULE_NAME,
    COMPOSITE_SUBSTITUTION_RULE_NAME,
    composite_hopf_substitution_inputs,
    composite_hopf_substitution_rule,
    composite_right_formula_parts,
    expand_cited_composite_right_hopf,
)
from proof import (
    ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_match,
)


def elements():
    nu_prime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    eta5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    eta6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    eta7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    return nu_prime, eta5, eta6, eta7


def typed_goals():
    nu_prime, eta5, eta6, eta7 = elements()
    suspended_composite = Suspension(Composition(eta5, eta6))
    lhs = MapApplication(EHP_H_MAP, Composition(nu_prime, suspended_composite))
    formula = Relation(
        lhs, Composition(MapApplication(EHP_H_MAP, nu_prime), suspended_composite),
        RelationType.EQUALITY,
    )
    substituted = Relation(
        lhs, Composition(eta5, suspended_composite), RelationType.EQUALITY,
    )
    hopf = Relation(MapApplication(EHP_H_MAP, nu_prime), eta5, RelationType.EQUALITY)
    return formula, substituted, hopf


def test_composite_formula_is_cited_and_keeps_its_right_factor():
    formula, substituted, hopf = typed_goals()
    nu_prime, eta5, eta6, eta7 = elements()
    assert composite_right_formula_parts(formula) == (nu_prime, Composition(eta5, eta6))
    assert expand_cited_composite_right_hopf(formula, ()) == ()
    assert expand_cited_composite_right_hopf(
        formula, (TodaProp22RightFormula(), TodaProp22RightFormula()),
    ) == ()
    choices = expand_cited_composite_right_hopf(formula, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].rule.name == COMPOSITE_FORMULA_RULE_NAME
    assert choices[0].subgoals == (TodaProp22RightFormula(),)


def test_composite_substitution_has_two_independent_proof_goals():
    formula, substituted, hopf = typed_goals()
    assert composite_hopf_substitution_inputs(substituted) == (formula, hopf)
    choices = expand_cited_composite_right_hopf(substituted, (TodaProp22RightFormula(),))
    assert len(choices) == 1
    assert choices[0].rule.name == COMPOSITE_SUBSTITUTION_RULE_NAME
    assert choices[0].subgoals == (formula, hopf)
    assert expand_cited_composite_right_hopf(substituted, ()) == ()


def test_inference_replay_requires_proved_formula_and_hopf_value():
    formula, substituted, hopf = typed_goals()
    formal_rule = expand_cited_composite_right_hopf(
        formula, (TodaProp22RightFormula(),),
    )[0].rule
    simulated_source = ProofStep(TodaProp22RightFormula(), (), ProofRule.GIVEN)
    formal_match = find_inference_match(formal_rule, (simulated_source,))
    assert formal_match is not None
    formal_step = apply_inference_match(formal_match)
    assert formal_step.conclusion == formula
    assert formal_step.rule is ProofRule.INFERENCE
    substitute_rule = composite_hopf_substitution_rule(substituted)
    simulated_hopf = ProofStep(hopf, (), ProofRule.GIVEN)
    match = find_inference_match(substitute_rule, (formal_step, simulated_hopf))
    assert match is not None
    result = apply_inference_match(match)
    assert result.conclusion == substituted
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (formal_step, simulated_hopf)
    assert find_inference_match(
        substitute_rule,
        (ProofStep(formula, (), ProofRule.GIVEN), simulated_hopf),
    ) is None
    assert find_inference_match(
        substitute_rule,
        (formal_step, ProofStep(replace(hopf, rhs=elements()[2]), (), ProofRule.GIVEN)),
    ) is None


def test_composite_right_wrong_types_and_rhs_fail_closed():
    formula, substituted, hopf = typed_goals()
    nu_prime, eta5, eta6, eta7 = elements()
    wrong_alpha = replace(nu_prime, source=30)
    malformed = Relation(
        MapApplication(EHP_H_MAP, Composition(
            wrong_alpha, Suspension(Composition(eta5, eta6)),
        )),
        Composition(MapApplication(EHP_H_MAP, wrong_alpha),
                    Suspension(Composition(eta5, eta6))),
        RelationType.EQUALITY,
    )
    assert composite_right_formula_parts(malformed) is None
    wrong_rhs = replace(formula, rhs=Composition(eta5, formula.rhs.right))
    assert composite_right_formula_parts(wrong_rhs) is None
    bad_hopf_value = replace(substituted, rhs=Composition(eta6, substituted.rhs.right))
    assert composite_hopf_substitution_inputs(bad_hopf_value) is None
    wrong_suspended_right = replace(substituted, rhs=Composition(eta5, Suspension(Composition(eta6, eta7))))
    assert composite_hopf_substitution_inputs(wrong_suspended_right) is None
    assert expand_cited_composite_right_hopf(bad_hopf_value, (TodaProp22RightFormula(),)) == ()
    with pytest.raises(ValueError):
        composite_hopf_substitution_rule(bad_hopf_value)


def test_old_single_right_factor_remains_old_provider_responsibility():
    nu_prime, eta5, eta6, eta7 = elements()
    formula = Relation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, Suspension(eta5))),
        Composition(MapApplication(EHP_H_MAP, nu_prime), Suspension(eta5)),
        RelationType.EQUALITY,
    )
    assert expand_cited_composite_right_hopf(formula, (TodaProp22RightFormula(),)) == ()
    assert len(expand_cited_prop22_right_formula(formula, (TodaProp22RightFormula(),))) == 1


def test_general_composite_left_and_composite_right_are_well_typed():
    nu_prime, eta5, eta6, eta7 = elements()
    alpha = Composition(nu_prime, eta6)
    beta = Composition(eta6, eta7)
    right = Suspension(beta)
    delta = HomotopyElement("δ", 5, 7, 5)
    substituted = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, right)),
        Composition(delta, right), RelationType.EQUALITY,
    )
    inputs = composite_hopf_substitution_inputs(substituted)
    assert inputs is not None
    assert inputs[1] == Relation(MapApplication(EHP_H_MAP, alpha), delta,
                                 RelationType.EQUALITY)


def test_provider_rejects_non_tuple_available():
    formula, substituted, hopf = typed_goals()
    with pytest.raises(TypeError):
        expand_cited_composite_right_hopf(formula, [TodaProp22RightFormula()])
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $auditArgs = @()
    if ($DryRun) { $auditArgs += '--dry-run' }
    & python -B -m phase176_r3r36_composite_right_hopf_isolated.audit @auditArgs
    if ($LASTEXITCODE -ne 0) { throw 'R3R36 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R36 isolated pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'Proposition 2.2 existing pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r30_generic_hopf_substitution_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R30 existing pytest failed' }
        & python -B -m pytest -q -p no:cacheprovider phase176_r3r34_composite_suspension_isolated/tests/test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R34 existing pytest failed' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git diff --check failed' }
        Write-Host 'PHASE176_R3R36_GATE=PASS_R3R36_ISOLATED_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R36_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```
