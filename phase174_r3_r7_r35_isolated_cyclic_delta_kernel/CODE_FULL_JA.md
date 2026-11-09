# R35 全コード（新規ファイル・関数・テスト全文）

変更対象の既存ファイルはありません。以下をパッケージの各新規位置に配置します。import を含めコード内の省略はありません。

## __init__.py

```python
"""Phase 174 R3-R7-R35 isolated generic Delta kernel inference."""

```

## rule.py

```python
"""Generic free-to-finite cyclic Delta kernel inference, requiring three proofs.

This module does not register a source, create a GIVEN, or attach a provider.
A proposed GoalExpansion is not a certified ProofStep.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "free-to-finite cyclic Delta generator kernel from three verified premises"


def expression_coordinates(value: object) -> tuple[int, int] | None:
    """Read actual domain/codomain of a typed element or composition, not a label."""
    if type(value) is HomotopyElement:
        if (type(value.source) is int and type(value.target) is int
                and value.source >= value.target >= 2):
            return value.source, value.target
        return None
    if type(value) in (Suspension, IteratedSuspension):
        source = value.source
        target = value.target
        if (type(source) is int and type(target) is int
                and source >= target >= 2):
            return source, target
        return None
    if type(value) is Composition:
        left = expression_coordinates(value.left)
        right = expression_coordinates(value.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    return None


def conditional_inputs(
    goal: object,
    domain: object,
    codomain: object,
    signed_image: object,
) -> tuple[Relation, Relation, TodaDeltaImageUpToSignStatement] | None:
    """Require matching typed groups, generator and image; do not certify inputs."""
    if type(goal) is not KernelMultipleStatement:
        return None
    delta = goal.map
    if (type(delta) is not TodaDeltaMap
            or not valid_ehp_lower_delta(delta)
            or goal.domain != delta.source_group):
        return None
    if (type(domain) is not Relation
            or domain.relation_type is not RelationType.EQUALITY
            or domain.lhs != delta.source_group
            or type(domain.rhs) is not FreeCyclicGroup
            or domain.rhs.generator != goal.source_generator
            or expression_coordinates(domain.rhs.generator) != (
                delta.source_group.group_dimension,
                delta.source_group.sphere_dimension,
            )):
        return None
    if (type(codomain) is not Relation
            or codomain.relation_type is not RelationType.EQUALITY
            or codomain.lhs != delta.target_group
            or type(codomain.rhs) is not FiniteCyclicGroup
            or type(codomain.rhs.order) is not int
            or codomain.rhs.order < 1
            or codomain.rhs.order != goal.multiple
            or expression_coordinates(codomain.rhs.generator) != (
                delta.target_group.group_dimension,
                delta.target_group.sphere_dimension,
            )):
        return None
    if (type(signed_image) is not TodaDeltaImageUpToSignStatement
            or signed_image.map != delta
            or signed_image.element != domain.rhs.generator
            or signed_image.positive_value != codomain.rhs.generator):
        return None
    return domain, codomain, signed_image


def cyclic_delta_kernel_rule(
    goal: KernelMultipleStatement,
    domain: Relation,
    codomain: Relation,
    signed_image: TodaDeltaImageUpToSignStatement,
) -> InferenceRule:
    """Build a proof rule only for three structurally verified antecedents."""
    if conditional_inputs(goal, domain, codomain, signed_image) is None:
        raise ValueError("Three cyclic Delta kernel antecedents are incompatible")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[2].rule is ProofRule.GIVEN
            and conditional_inputs(
                goal, premises[0].conclusion,
                premises[1].conclusion, premises[2].conclusion,
            ) == (domain, codomain, signed_image)
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "A map Z{g} to Z/m{h}, sending g to +/-h, has kernel <m*g>. "
            "Requires an independently inferred source presentation and "
            "two separately cited target/image facts."
        ),
        premise_patterns=(
            PremisePattern(statement_type=Relation, statement_pattern=domain),
            PremisePattern(statement_type=Relation, statement_pattern=codomain),
            PremisePattern(
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=signed_image,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cyclic_delta_kernel(
    goal: object,
    available_statements: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose a proof only when two distinct earlier typed source facts exist."""
    if not isinstance(available_statements, tuple):
        raise TypeError("available_statements must be a tuple")
    if type(goal) is not KernelMultipleStatement:
        return ()
    delta = goal.map
    if (type(delta) is not TodaDeltaMap
            or not valid_ehp_lower_delta(delta)
            or goal.domain != delta.source_group):
        return ()
    signed = tuple(
        item for item in available_statements
        if type(item) is TodaDeltaImageUpToSignStatement
        and item.map == delta
        and item.element == goal.source_generator
    )
    if len(signed) != 1:
        return ()
    target = tuple(
        item for item in available_statements
        if type(item) is Relation
        and item.relation_type is RelationType.EQUALITY
        and item.lhs == delta.target_group
        and type(item.rhs) is FiniteCyclicGroup
        and item.rhs.order == goal.multiple
        and item.rhs.generator == signed[0].positive_value
    )
    if len(target) != 1:
        return ()
    domain = Relation(
        delta.source_group,
        FreeCyclicGroup(goal.source_generator),
        RelationType.EQUALITY,
    )
    if conditional_inputs(goal, domain, target[0], signed[0]) is None:
        return ()
    return (
        GoalExpansion(
            rule=cyclic_delta_kernel_rule(goal, domain, target[0], signed[0]),
            subgoals=(domain, target[0], signed[0]),
        ),
    )

```

## audit.py

```python
"""R35: read-only source-first audit of the isolated cyclic Delta kernel rule."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "89fcf47a22dbb212fe635381fa5af3095d5c1527"
REVIEWED_HEAD = "4200211563834028ed6c4e2eeb01004646b92ba9"
R34_TRACKED = "phase165_r52_r9_shared_math.py"
PINS = {
    "phase165_r52_r9_shared_math.py": "6b965aa49db2ad8707c75dcc953d3c78cdd3e458",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py": "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py": "6d32a6b7768245770bc14524b866fd2e8ef50db6",
    "phase165_r57_r20_general_specialization.py": "e09603bee51d776cd4326a95930fc9c41f272a1b",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py": "c2357859b00ed0b446bac7a060a6d0c134fc7de5",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def same_reviewed_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        blob_sha(candidate) == sha for candidate in (
            data, normalized, normalized.replace(b"\n", b"\r\n"),
        )
    )


def verify_checkout() -> dict[str, object]:
    """Do not reset the user's R34 uncommitted/merged handoff."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R35 directly into the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R35 requires develop")
    local = git("rev-parse", "HEAD")
    remote_output = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_output.split()[0] if remote_output else ""
    if remote != REVIEWED_HEAD or local not in (BASE_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed GitHub/local HEAD; re-audit before R35")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged edits require review")
    changed = git("diff", "--name-only").splitlines()
    if changed and (local != BASE_HEAD or changed != [R34_TRACKED]):
        raise RuntimeError("Unexpected tracked edits; no reset performed")
    for path, sha in PINS.items():
        file = ROOT / path
        if not file.is_file() or not same_reviewed_blob(file.read_bytes(), sha):
            raise RuntimeError("Reviewed code/source differs: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r34_mode": "UNMERGED_REVIEWED" if local == BASE_HEAD else "MERGED_REVIEWED",
        "tracked_edits_preserved": changed,
        "reviewed_pin_count": len(PINS),
    }


def inspect_isolated_frontier() -> dict[str, object]:
    """Observe the real screened citations, general diagonal and isolated rule."""
    from homotopy_groups import (
        FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r57_r20_general_specialization import (
        expand_cited_general_specialization,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
        RULE_NAME, expand_cyclic_delta_kernel,
    )
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    target_root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=target_root,
    )
    steps = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    delta = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    image = tuple(
        s.conclusion for s in steps
        if type(s.conclusion) is TodaDeltaImageUpToSignStatement
        and s.conclusion.map == delta
    )
    target = tuple(
        s.conclusion for s in steps
        if type(s.conclusion) is Relation
        and s.conclusion.relation_type is RelationType.EQUALITY
        and s.conclusion.lhs == delta.target_group
    )
    if len(image) != 1 or len(target) != 1:
        raise RuntimeError("R34 earlier two cited source steps not available")
    goal = KernelMultipleStatement(delta, delta.source_group, image[0].element, 2)
    proposals = expand_cyclic_delta_kernel(goal, tuple(s.conclusion for s in steps))
    if len(proposals) != 1 or proposals[0].rule.name != RULE_NAME:
        raise RuntimeError("R35 isolated kernel rule failed to recognize actual R34 source")
    source_goal = Relation(
        delta.source_group, FreeCyclicGroup(image[0].element), RelationType.EQUALITY,
    )
    if proposals[0].subgoals != (source_goal, target[0], image[0]):
        raise RuntimeError("R35 did not preserve exact R34 generator/source identity")
    general_diagonal = expand_cited_general_specialization(
        source_goal, tuple(s.conclusion for s in steps),
    )
    return {
        "screened_cited_codomain": 1,
        "screened_cited_signed_image": 1,
        "composite_generator_preserved": True,
        "isolated_kernel_expansions": len(proposals),
        "diagonal_generic_specialization_proposals": len(general_diagonal),
        "diagonal_proof_certified_by_audit": False,
        "kernel_proof_certified_by_audit": False,
        "shared_provider_connected_in_r35": False,
        "new_givens": 0,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_general_rules_installed_in_public_provider": 0,
        "root_complete": False,
        "full_pytest": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    frontier = None if dry_run else inspect_isolated_frontier()
    return {
        "phase": "174-R3-R7-R35",
        "git_state": state,
        "frontier": frontier,
        "gate": (
            "PASS_R35_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R35_ISOLATED_COMPOSITE_KERNEL_RULE_AUDITED_PUBLIC_WIRING_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r35"
    )
    folder.mkdir(parents=True, exist_ok=True)
    file = folder / ("preflight.json" if args.dry_run else "isolated_kernel_audit.json")
    file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R35_"
    for key in ("local_head", "remote_head", "source_guard", "r34_mode", "reviewed_pin_count"):
        print(prefix + key.upper() + "=" + str(result["git_state"][key]))
    if result["frontier"] is not None:
        for key, val in result["frontier"].items():
            print(prefix + key.upper() + "=" + str(val))
    print(prefix + "REPORT=" + str(file))
    print(prefix + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_rule.py

```python
"""Focused isolated proof-contract tests; fabricated steps are fixtures only."""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    RULE_NAME, conditional_inputs, cyclic_delta_kernel_rule,
    expand_cyclic_delta_kernel, expression_coordinates,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule, apply_inference_match,
)
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture(q: int = 9, n: int = 5):
    domain = TodaPrimaryGroup(q + 2, 2 * n + 1)
    target = TodaPrimaryGroup(q, n)
    delta = TodaDeltaMap(domain, target)
    iota = HomotopyElement(
        "iota", 2 * n + 1, q + 2, 2 * n + 1,
        GeneratorSymbol("ι", 2 * n + 1),
    )
    nu = HomotopyElement("a", n, q - 1, n, GeneratorSymbol("a", n))
    eta = HomotopyElement("b", q - 1, q, q - 1, GeneratorSymbol("b", q - 1))
    composite = Composition(nu, eta)
    src = Relation(domain, FreeCyclicGroup(iota), RelationType.EQUALITY)
    dst = Relation(target, FiniteCyclicGroup(2, composite), RelationType.EQUALITY)
    image = TodaDeltaImageUpToSignStatement(delta, iota, composite)
    goal = KernelMultipleStatement(delta, domain, iota, 2)
    return goal, src, dst, image


@pytest.mark.parametrize("q,n", [(9, 5), (11, 6), (13, 7), (17, 9)])
def test_general_ehp_windows_support_composition(q, n):
    goal, source, target, image = fixture(q, n)
    assert expression_coordinates(target.rhs.generator) == (q, n)
    assert conditional_inputs(goal, source, target, image) == (source, target, image)
    proposals = expand_cyclic_delta_kernel(goal, (target, image))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (source, target, image)
    assert proposals[0].rule.name == RULE_NAME


def test_real_verified_premise_types_produce_inference_only():
    goal, source, target, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, source, target, image)
    parent = InferenceRule(name="test-only source diagonal inference")
    facts = (
        ProofStep(source, (), ProofRule.INFERENCE, inference_rule=parent),
        ProofStep(target, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    matches = find_inference_matches_for_rule(rule, facts)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == facts


def test_missing_any_one_of_three_premises_rejects_proof():
    goal, src, dst, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, src, dst, image)
    facts = (
        ProofStep(src, (), ProofRule.INFERENCE),
        ProofStep(dst, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    for index in range(3):
        assert not find_inference_matches_for_rule(
            rule, tuple(f for i, f in enumerate(facts) if i != index)
        )


def test_unproved_diagonal_given_not_mistaken_for_inference():
    goal, src, dst, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, src, dst, image)
    facts = (
        ProofStep(src, (), ProofRule.GIVEN),
        ProofStep(dst, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    assert not find_inference_matches_for_rule(rule, facts)


def test_wrong_signed_witness_rejected():
    goal, src, dst, image = fixture()
    altered = TodaDeltaImageUpToSignStatement(image.map, image.element, src.rhs.generator)
    assert conditional_inputs(goal, src, dst, altered) is None
    assert expand_cyclic_delta_kernel(goal, (dst, altered)) == ()


def test_wrong_order_rejected():
    goal, src, dst, image = fixture()
    altered = Relation(dst.lhs, FiniteCyclicGroup(4, dst.rhs.generator), RelationType.EQUALITY)
    assert conditional_inputs(goal, src, altered, image) is None
    assert expand_cyclic_delta_kernel(goal, (altered, image)) == ()


def test_wrong_composition_rejected():
    goal, src, dst, image = fixture()
    a = HomotopyElement("a", 5, 7, 5)
    b = HomotopyElement("b", 8, 9, 8)
    broken = Composition(a, b)
    assert expression_coordinates(broken) is None
    wrong = Relation(dst.lhs, FiniteCyclicGroup(2, broken), RelationType.EQUALITY)
    wrong_image = TodaDeltaImageUpToSignStatement(image.map, image.element, broken)
    assert conditional_inputs(goal, src, wrong, wrong_image) is None


def test_ambiguous_source_witnesses_rejected():
    goal, src, dst, image = fixture()
    assert expand_cyclic_delta_kernel(goal, (dst, image, image)) == ()
    assert expand_cyclic_delta_kernel(goal, (dst, dst, image)) == ()


def test_unrelated_goal_does_not_expand():
    assert expand_cyclic_delta_kernel("pi12_7", ()) == ()


def test_no_source_facts_no_proposal():
    goal, src, dst, image = fixture()
    assert expand_cyclic_delta_kernel(goal, ()) == ()
    assert expand_cyclic_delta_kernel(goal, (dst,)) == ()
    assert expand_cyclic_delta_kernel(goal, (image,)) == ()

```

## tests/test_audit.py

```python
"""R35 integration observations, without modifying the shared provider."""
from __future__ import annotations

from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit import (
    inspect_isolated_frontier, verify_checkout,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    checked_prior_statements,
)
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    expand_cyclic_delta_kernel,
)
from phase165_r12_r2_quotient_rules import KernelMultipleStatement


def test_source_guard_keeps_reviewed_r34():
    assert verify_checkout()["source_guard"] == "PASS"


def test_real_r34_composition_is_not_replaced_with_synthetic_generator():
    codomain, image = checked_prior_statements()
    goal = KernelMultipleStatement(image.map, image.map.source_group, image.element, 2)
    proposals = expand_cyclic_delta_kernel(goal, (codomain, image))
    assert len(proposals) == 1
    assert proposals[0].subgoals[1:] == (codomain, image)


def test_real_shared_screen_preserves_unproved_frontier():
    result = inspect_isolated_frontier()
    assert result["screened_cited_codomain"] == 1
    assert result["screened_cited_signed_image"] == 1
    assert result["isolated_kernel_expansions"] == 1
    assert result["composite_generator_preserved"] is True
    assert result["kernel_proof_certified_by_audit"] is False
    assert result["shared_provider_connected_in_r35"] is False
    assert result["root_complete"] is False

```

## tests/test_static_contract.py

```python
"""Source-only structural tests independent of the deployed application."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parsed_module(name: str) -> ast.Module:
    return ast.parse((ROOT / name).read_text(encoding="utf-8"))


def test_no_direct_proofstep_creation_in_inference_rule():
    tree = parsed_module("rule.py")
    names = {node.func.id for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert "ProofStep" not in names
    assert "KernelMultipleStatement" not in names


def test_single_generic_rule_without_dimension_literals():
    tree = parsed_module("rule.py")
    functions = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert functions == {
        "expression_coordinates", "conditional_inputs", "cyclic_delta_kernel_rule",
        "expand_cyclic_delta_kernel",
    }
    source = (ROOT / "rule.py").read_text(encoding="utf-8")
    assert "π_12" not in source
    assert "pi12" not in source


def test_audit_never_claims_public_proof():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"kernel_proof_certified_by_audit": False' in source
    assert '"shared_provider_connected_in_r35": False' in source
    assert '"root_complete": False' in source


def test_full_runner_exists():
    text = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in text
    assert "R35_RULE" in text
    assert "FULL_PYTEST=False" in text

```

## run.ps1 全文

```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    if ($DryRun) {
        python -B -m phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R35 Source Guard / DryRun failed' }
        Write-Output 'PHASE174_R3R7R35_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r35_isolated_cyclic_delta_kernel.audit
    if ($LASTEXITCODE -ne 0) { throw 'R35 Source Guard / audit failed' }
    $Groups = @(
        @{Name='R35_STATIC'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_static_contract.py'},
        @{Name='R35_RULE'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'},
        @{Name='R35_AUDIT'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_audit.py'},
        @{Name='R34_PRIOR_SOURCE'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py'},
        @{Name='R34_PUBLIC'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py'},
        @{Name='R32_KERNEL_CONTRACT'; Path='phase174_r3_r7_r32_lower_delta_kernel_audit/tests/test_kernel_contract.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R35_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R35 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R35_RUN=PASS'
    Write-Output 'PHASE174_R3R7R35_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```
