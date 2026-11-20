# Phase 176 R3R27R1 — 追加コード全文

すべて新規ファイル。既存 import の変更はない。

# source.py

```python
"""Source-verified isolated Toda (5.5) quadruple nu relation; no public wiring."""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    canonical_member,
)
from phase174_r3_r6_source_extension.source import ROOT, verify_extension_texts
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep, Relation, RelationType
from toda_rules import toda_eta_family_definition_statement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

REFERENCE_ID = "toda:(5.5):quadruple_nu"
ASSERTION_ID = "toda:176:r3r27r1:universal:quadruple_nu"
RULE_NAME = "specialize cited Toda (5.5) quadruple nu-family identity"


@dataclass(frozen=True)
class Toda55UniversalQuadrupleStatement:
    """Source fact: 4 nu_n = eta_n eta_(n+1) eta_(n+2), n>=5."""
    minimum_index: int = 5
    coefficient: int = 4
    family: str = "ν"


def build_cited_toda55_quadruple_source() -> RegistryBridgeResult:
    """Check the reviewed source bytes and the *second* (5.5) clause."""
    positions = dict(verify_extension_texts())
    text = (ROOT / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8-sig")
    anchor = r"\begin{equation}\label{eq:5.5}"
    if text.count(anchor) != 1:
        raise ValueError("Toda (5.5) anchor must be unique")
    body = text.split(anchor, 1)[1].split(r"\end{equation}", 1)[0]
    if (r"n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu'" not in body
            or r"4\nu_{n}=\eta_n^{3}" not in body
            or r"4\nu=\eta^{3}" not in body):
        raise ValueError("Toda (5.5) quadruple clause missing")
    definition = r"\eta^{3}_{n}:=\eta_{n}\circ\eta_{n+1}\circ\eta_{n+2}"
    if definition not in text[:text.index(anchor)]:
        raise ValueError("eta-cube definition is not cited before Toda (5.5)")
    statement = Toda55UniversalQuadrupleStatement()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.5)",
        source_id="sources/toda/Toda_05_2.tex (adopted transcription; original edition unverified)",
        publication_position=positions["(5.5)"],
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=statement,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("quadruple nu-family relation for n>=5 only",),
    ))
    step = ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited universal Toda (5.5) quadruple relation",
            literature_reference=LiteratureReference(label="Toda (5.5)", locator="(5.5)"),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord("phase176_r3r27r1", "(5.5):quadruple_nu",
                         ASSERTION_ID, MigrationStatus.STRUCTURED,
                         "source-blob-verified universal quadruple relation"),),
        (ProofStepLink(ASSERTION_ID, step=step),),
    )


def canonical_quadruple_goal(n: int) -> Relation | None:
    """A source-based schematic specialization; NEVER a proof certificate."""
    if type(n) is not int or n < 5:
        return None
    family = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(family, n)
    if member is None:
        return None
    eta_elements = tuple(toda_eta_family_definition_statement(j).element
                         for j in (n, n + 1, n + 2))
    if not all(isinstance(e, HomotopyElement) and e.generator == GeneratorSymbol("η", index=j)
               and e.source == j + 1 and e.target == j for j, e in zip((n, n+1, n+2), eta_elements)):
        return None
    eta_cube = Composition(eta_elements[0], Composition(eta_elements[1], eta_elements[2]))
    if eta_cube.left.source != eta_cube.right.left.target or not eta_cube.right.is_type_compatible():
        return None
    if eta_elements[2].source != member.element.source or eta_elements[0].target != member.element.target:
        return None
    return Relation(Multiple(4, member.element), eta_cube, RelationType.EQUALITY)


def quadruple_inputs(goal: object) -> tuple[StableFamilyMemberDefinition, Toda55UniversalQuadrupleStatement, TodaEtaFamilyGeneralDefinition] | None:
    if not isinstance(goal, Relation) or not isinstance(goal.lhs, Multiple):
        return None
    nu = goal.lhs.expression
    if not isinstance(nu, HomotopyElement) or type(nu.dimension) is not int:
        return None
    if canonical_quadruple_goal(nu.dimension) != goal:
        return None
    family = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(family, nu.dimension)
    if member is None:
        return None
    return member, Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition()


def cited_quadruple_rule(goal: Relation) -> InferenceRule:
    inputs = quadruple_inputs(goal)
    if inputs is None:
        raise ValueError("not a cited typed Toda (5.5) quadruple goal")

    def guard(premises, bindings):
        return (len(premises) == 3
                and premises[0].rule is ProofRule.INFERENCE
                and premises[1].rule is ProofRule.GIVEN
                and premises[2].rule is ProofRule.GIVEN
                and tuple(p.conclusion for p in premises) == inputs
                and quadruple_inputs(goal) == inputs)

    return InferenceRule(
        name=RULE_NAME,
        description="Specialize source-verified Toda (5.5) using separately proved ν-family member and cited η notation.",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=StableFamilyMemberDefinition, statement_pattern=inputs[0]),
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=Toda55UniversalQuadrupleStatement, statement_pattern=inputs[1]),
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=TodaEtaFamilyGeneralDefinition, statement_pattern=inputs[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
        literature_reference=LiteratureReference(label="Toda (5.5)", locator="(5.5)"),
    )


def expand_cited_quadruple(goal: object, available: tuple[object, ...]) -> tuple[GoalExpansion, ...]:
    """Return a backward proof *candidate* only when BOTH citations were screened."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    inputs = quadruple_inputs(goal)
    if inputs is None:
        return ()
    if (available.count(inputs[0].source) != 1
            or available.count(inputs[1]) != 1
            or available.count(inputs[2]) != 1):
        return ()
    return (GoalExpansion(cited_quadruple_rule(goal), inputs),)

```

# audit.py

```python
"""Isolated source-first probe, independent of public shared search wiring."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    build_cited_toda55_quadruple_source,
    canonical_quadruple_goal,
    expand_cited_quadruple,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r27r1_toda55_quadruple_isolated"


def checked_head() -> str:
    def git(*args: str) -> str:
        proc = subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
        if proc.returncode:
            raise RuntimeError("git error: " + proc.stderr)
        return proc.stdout.strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT:
        raise RuntimeError("WRONG_REPOSITORY")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    return git("rev-parse", "HEAD")


def capture() -> dict[str, object]:
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
    from proof import ProofRule
    bridge = build_cited_toda55_quadruple_source()
    citation = bridge.proof_links[0].step.conclusion
    assert citation == Toda55UniversalQuadrupleStatement()
    goal = canonical_quadruple_goal(5)
    if goal is None:
        raise RuntimeError("NU5_CANONICAL_GOAL_MISSING")
    family = CitedStableFamilyDefinition(4, 4, 3)
    available = (citation, family, TodaEtaFamilyGeneralDefinition())
    proposals = expand_cited_quadruple(goal, available)
    if len(proposals) != 1 or len(proposals[0].subgoals) != 3:
        raise RuntimeError("ISOLATED_CANDIDATE_MISSING")
    if any(isinstance(child, ProofRule) for child in proposals[0].subgoals):
        raise RuntimeError("UNEXPECTED_PROOF_OBJECT")
    return {
        "source_assertion_count": len(bridge.proof_links),
        "source_statement": repr(citation),
        "nu5_goal": repr(goal),
        "isolated_candidate_count": len(proposals),
        "candidate_rule": proposals[0].rule.name,
        "candidate_children": [repr(child) for child in proposals[0].subgoals],
        "public_provider_modified": False,
        "isolated_candidate_is_proof": False,
        "nu5_quadruple_proved": False,
        "root_pi83_proved": False,
        "new_direct_group_given": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    parent = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    path = parent / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path / "report.json"


def execute(dry_run: bool) -> int:
    result: dict[str, object] = {
        "phase": "176_R3R27R1", "gate": "FAIL_R3R27R1",
        "full_pytest": "NOT_RUN", "public_provider_modified": False,
    }
    try:
        result["head"] = checked_head()
        if dry_run:
            result["gate"] = "PASS_R3R27R1_DRYRUN"
        else:
            result["observed"] = capture()
            result["gate"] = "PASS_R3R27R1_CITED_QUADRUPLE_ISOLATED"
    except Exception as exc:
        result["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_path()
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R27R1_GATE=" + str(result["gate"]))
    print("PHASE176_R3R27R1_HEAD=" + str(result.get("head", "UNVERIFIED")))
    if "observed" in result:
        for key, value in result["observed"].items():
            print("PHASE176_R3R27R1_" + key.upper() + "=" + str(value))
    if "error" in result:
        print("PHASE176_R3R27R1_ERROR=" + str(result["error"]))
    print("PHASE176_R3R27R1_REPORT=" + str(path))
    print("PHASE176_R3R27R1_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(result["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

# tests/test_source.py

```python
"""Focused source and guarded inference contracts for the second Toda (5.5) clause."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, Multiple, Zero
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition, canonical_member,
)
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    Toda55UniversalQuadrupleStatement,
    build_cited_toda55_quadruple_source,
    canonical_quadruple_goal,
    cited_quadruple_rule,
    expand_cited_quadruple,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def available_sources():
    return (
        Toda55UniversalQuadrupleStatement(),
        CitedStableFamilyDefinition(4, 4, 3),
        TodaEtaFamilyGeneralDefinition(),
    )


def test_source_adopts_only_second_clause() -> None:
    bridge = build_cited_toda55_quadruple_source()
    assert len(bridge.proof_links) == 1
    step = bridge.proof_links[0].step
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == Toda55UniversalQuadrupleStatement()
    assertion = bridge.registry.assertion(bridge.proof_links[0].assertion_id)
    assert assertion.content == step.conclusion
    assert bridge.registry.reference(assertion.reference_id).publication_position == 8600


@pytest.mark.parametrize("n", (5, 6, 12))
def test_canonical_nu_quadruple_goal_is_typed(n: int) -> None:
    goal = canonical_quadruple_goal(n)
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert goal.lhs.coefficient == 4
    assert goal.lhs.expression.dimension == n
    assert isinstance(goal.rhs, Composition)
    assert tuple(x.generator.index for x in
                 (goal.rhs.left, goal.rhs.right.left, goal.rhs.right.right)) == (n, n + 1, n + 2)
    assert len(expand_cited_quadruple(goal, available_sources())) == 1


def test_unsupported_indices_and_sources_fail_closed() -> None:
    assert canonical_quadruple_goal(4) is None
    assert canonical_quadruple_goal(True) is None
    goal = canonical_quadruple_goal(5)
    assert expand_cited_quadruple(goal, ()) == ()
    assert expand_cited_quadruple(goal, available_sources()[:-1]) == ()
    assert expand_cited_quadruple(goal, available_sources() + (available_sources()[0],)) == ()
    assert expand_cited_quadruple(replace(goal, rhs=Zero()), available_sources()) == ()
    assert expand_cited_quadruple(Relation(Multiple(2, goal.lhs.expression), goal.rhs,
                                           RelationType.EQUALITY), available_sources()) == ()


def test_only_independently_inferred_family_member_can_close() -> None:
    goal = canonical_quadruple_goal(5)
    rule = cited_quadruple_rule(goal)
    family = CitedStableFamilyDefinition(4, 4, 3)
    member = canonical_member(family, 5)
    premise = ProofStep(member, (), ProofRule.INFERENCE,
                        inference_rule=InferenceRule(name="test independent family member"))
    cited = ProofStep(Toda55UniversalQuadrupleStatement(), (), ProofRule.GIVEN)
    eta = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, (premise, cited, eta))
    assert len(matches) == 1
    assert find_inference_matches_for_rule(rule, (
        ProofStep(member, (), ProofRule.GIVEN), cited, eta)) == ()
    assert find_inference_matches_for_rule(rule, (premise, cited)) == ()
    assert find_inference_matches_for_rule(rule, (premise, eta, cited)) == ()

```

# run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r27r1_toda55_quadruple_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1 DryRun failed' }
    } else {
        python -B -m phase176_r3r27r1_toda55_quadruple_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1 isolated audit failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests `
            .\phase174_r3_r6_source_extension\tests\test_source.py `
            .\phase171_r2e_toda53_double_source\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R27R1 focused tests failed' }
        Write-Host 'PHASE176_R3R27R1_GATE=PASS_R3R27R1_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R27R1_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}

```

