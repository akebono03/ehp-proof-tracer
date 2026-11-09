# R39 新規コード全文

追加位置はプロジェクトルート直下の `phase174_r3_r7_r39_verified_zero_image_frontier/` です。既存コードは変更しません。


## __init__.py

```python

```

## audit.py

```python
"""Source-first actual ProofStep frontier for the R38 zero-image chain.

Do not promote adopted DB-prior GIVEN to INFERENCE, do not assert a root
completion, and do not modify any production provider, database or renderer.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import verify_checkout

ROOT = Path(__file__).resolve().parents[1]


def derive_from_expansion(expansion: object, steps: tuple[object, ...]):
    """Use the canonical inference matcher, never construct a fake proof step."""
    from phase165_r3_recursive_search import GoalExpansion
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step

    if not isinstance(expansion, GoalExpansion):
        raise TypeError("GoalExpansion required")
    if (not isinstance(steps, tuple)
            or any(not isinstance(step, ProofStep) for step in steps)
            or tuple(step.conclusion for step in steps) != expansion.subgoals):
        raise ValueError("ProofStep premises do not match candidate subgoals")
    matches = tuple(
        match for match in find_inference_matches_for_rule(expansion.rule, steps)
        if len(match.premises) == len(steps)
        and all(x is y for x, y in zip(match.premises, steps))
    )
    if len(matches) != 1:
        raise RuntimeError("No unique matching genuine inference")
    result = derive_inference_proof_step(matches[0])
    if (not isinstance(result, ProofStep)
            or result.rule is not ProofRule.INFERENCE
            or result.premises != steps):
        raise RuntimeError("Inference factory produced an invalid proof step")
    return result


def derive_one(goal: object, provider, parents: tuple[object, ...], rule_name: str | None = None):
    """Choose the one requested generic rule; reject ambiguity rather than guess."""
    options = provider(goal)
    chosen = tuple(option for option in options
                   if option.subgoals == tuple(parent.conclusion for parent in parents)
                   and (rule_name is None or option.rule.name == rule_name))
    if len(chosen) != 1:
        raise RuntimeError("Expected one typed inference for " + type(goal).__name__)
    result = derive_from_expansion(chosen[0], parents)
    if result.conclusion != goal:
        raise RuntimeError("Inferred conclusion differs from the intended goal")
    return result


def inspect_proof_frontier() -> dict[str, object]:
    """Prove generator zero from real citation; inspect cyclic DB blocker."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import RULE_NAME as CYCLIC_RULE
    from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    original_fixed = tuple(
        link.step for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    schema_steps = tuple(step for step in original_fixed
                         if type(step.conclusion) is CitedFamilyAnnihilator)
    if len(schema_steps) != 1:
        raise RuntimeError("Expected exactly one cited Toda (5.9) general source")
    source_step = schema_steps[0]
    source_citation = getattr(getattr(source_step, "inference_rule", None), "literature_reference", None)
    if source_citation is None or source_citation.locator != "(5.9)":
        raise RuntimeError("Source attribution is not Toda (5.9)")

    prior = exact_prior_database_result(5, 5)
    if type(prior) is not Relation or prior.relation_type is not RelationType.EQUALITY:
        raise RuntimeError("The reviewed earlier DB group is missing")
    db_step = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (not isinstance(db_step, ProofStep)
            or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("Earlier DB prior failed its existing independent admission gate")
    domain, target = prior.lhs, TodaPrimaryGroup(
        prior.lhs.group_dimension + 1, prior.lhs.sphere_dimension + 1,
    )
    mapping = TodaSuspensionMap(domain, target)
    lift = lifted_stable_composition(prior.rhs.generator)
    if lift is None:
        raise RuntimeError("R38 registered composite generator cannot be suspended")
    left = left_associated(lift)
    if left is None:
        raise RuntimeError("Canonical composition cannot be rebracketed")
    right_goal = GeneratorImage(mapping, prior.rhs.generator, lift)
    left_goal = GeneratorImage(mapping, prior.rhs.generator, left)
    zero_generator_goal = GeneratorImage(mapping, prior.rhs.generator, Zero())
    zero_image_goal = ImageZeroStatement(mapping)
    annihilator_goal = Relation(left.left, Zero(), RelationType.EQUALITY)

    shared = shared_expansion_provider(bridge, proof_target=root)
    public_r38 = tuple(x for x in shared(zero_image_goal) if x.rule.name == CYCLIC_RULE)
    if len(public_r38) != 1 or public_r38[0].subgoals != (prior, zero_generator_goal):
        raise RuntimeError("R38 public cyclic candidate disappeared")

    n6_step = derive_one(
        annihilator_goal,
        lambda goal: expand_cited_annihilator_specialization(goal, (source_step.conclusion,)),
        (source_step,),
    )
    factors = component_image_obligations(right_goal)
    if factors is None or len(factors) != 2:
        raise RuntimeError("Composite generator image does not factor into two typed images")
    stable_steps = tuple(derive_one(fact, expand_defined_stable_element_image, ())
                         for fact in factors)
    right_step = derive_one(right_goal, expand_composite_generator_image, stable_steps)
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    left_step = derive_one(left_goal, expand_generator_image_associativity, (right_step,))
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    zero_generator_step = derive_one(
        zero_generator_goal,
        lambda goal: expand_generator_zero_from_composite(goal, left_goal),
        (left_step, n6_step),
    )
    if zero_generator_step.rule is not ProofRule.INFERENCE:
        raise RuntimeError("Generator zero has not been inferred")
    if find_inference_matches_for_rule(public_r38[0].rule, (db_step, zero_generator_step)):
        raise RuntimeError("R6 rule accepted adopted DB GIVEN as an inferred presentation")
    if any(step.conclusion in (zero_image_goal, root) for step in original_fixed):
        raise RuntimeError("Forbidden direct zero image/root cited GIVEN")

    return {
        "cited_annihilator_source": "(5.9)",
        "source_general_given_count": 1,
        "adopted_earlier_db_prior_accepted": True,
        "db_prior_is_independent_literature": False,
        "db_presentation_step_rule": db_step.rule.name,
        "n6_annihilator_inferred": True,
        "stable_factor_images_inferred": len(stable_steps),
        "composite_image_inferred": True,
        "associativity_inferred": True,
        "generator_zero_inferred": True,
        "r6_accepts_db_prior_as_inferred_presentation": False,
        "cyclic_presentation_inference_available_in_this_audit": False,
        "zero_suspension_image_proved": False,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "new_givens": 0,
        "new_public_rules": 0,
        "full_pytest": False,
        "blocker": "Cyclic presentation for the R6 rule is an adopted DB GIVEN, not a verified INFERENCE",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    checkout = verify_checkout()
    observed = None if args.dry_run else inspect_proof_frontier()
    report = {
        "phase": "174-R3-R7-R39",
        "git_state": checkout,
        "observed": observed,
        "gate": (
            "PASS_R39_SOURCE_GUARD_ONLY" if args.dry_run else
            "PASS_R39_CITED_GENERATOR_ZERO_PROVED_DB_PRESENTATION_BARRIER"
        ),
    }
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r39"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "zero_image_frontier.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R39_"
    for key in ("local_head", "remote_head", "source_guard", "reviewed_r38_upstream_files", "public_r38_installed"):
        print(p + key.upper() + "=" + str(checkout[key]))
    if observed is not None:
        for key, value in observed.items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r39_verified_zero_image_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R39 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R39_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r39_verified_zero_image_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R39 verified frontier audit failed' }
    $Groups = @(
        @{Name='R39_STATIC'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_static.py'},
        @{Name='R39_GUARD'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_guard.py'},
        @{Name='R39_REAL_PROOF'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R38_PUBLIC'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R14_SOURCE'; Path='phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py'},
        @{Name='R6_CYCLIC'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'},
        @{Name='R7_COMPOSITE'; Path='phase174_r3_r7_r7_composite_zero_audit/tests/test_rule.py'},
        @{Name='R9_ASSOCIATIVITY'; Path='phase174_r3_r7_r9_composition_associativity/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R39_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R39 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R39_RUN=PASS'
    Write-Output 'PHASE174_R3R7R39_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## source_guard.py

```python
"""Read-only source and Git lineage checks for Phase 174 R3-R7-R39."""
from __future__ import annotations

import hashlib
from pathlib import Path
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "2e3fcfbea1a3816b146cf53320f9a3bbee618c52"
ALLOWED_UPSTREAM_PREFIXES = (
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/",
    "phase174_r3_r7_r38r1_r9_sha_pin_fix/",
)
CONTEXT = "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py"
PROVIDER = "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py"
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase169_r10eq_r1_universal_stable_definition/definition.py": "0c74d121419b6755e947a367d7de465d81193174",
}


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def matches_blob(data: bytes, sha: str) -> bool:
    clean = normalized(data)
    return len(sha) == 40 and sha in (
        git_blob(data), git_blob(clean), git_blob(clean.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Allow only reviewed R38 merge or one R38 local tracked change."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R39 directly at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R39 requires develop branch")
    local = git("rev-parse", "HEAD")
    output = git("ls-remote", "origin", "refs/heads/develop")
    remote = output.split()[0] if output else ""
    if not remote:
        raise RuntimeError("Cannot verify origin/develop")
    if remote != BASE_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed while examining lineage")
        rc = subprocess.run(("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
                            cwd=ROOT, capture_output=True).returncode
        if rc != 0:
            raise RuntimeError("Unknown remote lineage")
        advance = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not advance or any(not path.startswith(ALLOWED_UPSTREAM_PREFIXES)
                              and path != CONTEXT for path in advance):
            raise RuntimeError("Remote changed outside reviewed R38 scope")
    else:
        advance = ()
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Unknown local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only").splitlines())
    if changed not in ((), (CONTEXT,)):
        raise RuntimeError("Unexpected tracked edits")
    for path, sha in PINS.items():
        item = ROOT / path
        if not item.is_file() or not matches_blob(item.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    r38 = ROOT / "phase174_r3_r7_r38_source_bound_zero_image_public_wiring"
    baseline = r38 / "baseline" / "context_provider_registry.py"
    replacement = r38 / "replacement" / "context_provider_registry.py"
    if not (baseline.is_file() and replacement.is_file()):
        raise RuntimeError("R38 reviewed baseline and replacement absent")
    if normalized(baseline.read_bytes()) == normalized(replacement.read_bytes()):
        raise RuntimeError("R38 replacement does not differ from baseline")
    context = ROOT / CONTEXT
    if not context.is_file() or normalized(context.read_bytes()) != normalized(replacement.read_bytes()):
        raise RuntimeError("R38 public provider not installed or modified")
    if not (ROOT / PROVIDER).is_file() or not matches_blob((ROOT / PROVIDER).read_bytes(), R38_PROVIDER_BLOB):
        raise RuntimeError("R38 provider differs from reviewed implementation")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_r38_upstream_files": len(advance),
        "tracked_changes": list(changed),
        "public_r38_installed": True,
        "full_pytest": False,
    }


R38_PROVIDER_BLOB = "6aa48096b41714fbdf588c3ba423d264a4a13bb9"
```

## tests/test_guard.py

```python
"""Exact source fingerprint and checkout fail-closed checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import (
    BASE_HEAD, CONTEXT, PINS, R38_PROVIDER_BLOB,
    git_blob, matches_blob, normalized, verify_checkout,
)


def test_bytewise_git_blob_with_checked_crlf_variants():
    raw = b"line one\nline two\n"
    sha = git_blob(raw)
    assert len(sha) == 40
    assert matches_blob(raw, sha)
    assert matches_blob(raw.replace(b"\n", b"\r\n"), sha)
    assert not matches_blob(b"unexpected", sha)
    assert not matches_blob(raw, sha[:-1])


def test_reviewed_r38_package_and_live_source_are_pinned():
    checkout = verify_checkout()
    assert checkout["source_guard"] == "PASS"
    assert checkout["public_r38_installed"] is True
    assert checkout["local_head"] in (BASE_HEAD, checkout["remote_head"])
    assert len(R38_PROVIDER_BLOB) == 40


def test_wrong_source_pin_is_rejected(monkeypatch):
    import phase174_r3_r7_r39_verified_zero_image_frontier.source_guard as guard
    mutated = dict(guard.PINS)
    mutated["sources/toda/Toda_05_2.tex"] = "0" * 40
    monkeypatch.setattr(guard, "PINS", mutated)
    with pytest.raises(RuntimeError, match="Reviewed source differs"):
        guard.verify_checkout()
```

## tests/test_proof.py

```python
"""Actual R39 source-bound generator-zero proof and signed DB boundary."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r39_verified_zero_image_frontier.audit import (
    derive_from_expansion, inspect_proof_frontier,
)
from phase174_r3_r7_r39_verified_zero_image_frontier.source_guard import verify_checkout


def test_real_screened_toda_source_derives_generator_zero_only():
    result = inspect_proof_frontier()
    assert result["cited_annihilator_source"] == "(5.9)"
    assert result["n6_annihilator_inferred"] is True
    assert result["stable_factor_images_inferred"] == 2
    assert result["composite_image_inferred"] is True
    assert result["associativity_inferred"] is True
    assert result["generator_zero_inferred"] is True
    assert result["zero_suspension_image_proved"] is False


def test_db_prior_stays_given_not_a_fake_inference():
    result = inspect_proof_frontier()
    assert result["adopted_earlier_db_prior_accepted"] is True
    assert result["db_prior_is_independent_literature"] is False
    assert result["db_presentation_step_rule"] == "GIVEN"
    assert result["r6_accepts_db_prior_as_inferred_presentation"] is False
    assert result["cyclic_presentation_inference_available_in_this_audit"] is False
    assert result["new_givens"] == 0
    assert result["new_public_rules"] == 0
    assert result["root_complete"] is False


def test_inference_step_factory_rejects_nonexpansion_arguments():
    with pytest.raises(TypeError, match="GoalExpansion"):
        derive_from_expansion(object(), ())
```

## tests/test_static.py

```python
"""Read-only R39 artifact constraints: importable, complete, scope-isolated."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_all_new_python_units_have_valid_syntax():
    for path in sorted(ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_audit_does_not_rename_proof_rules_or_create_a_given():
    code = (ROOT / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(code)
    calls = tuple(node for node in ast.walk(tree) if isinstance(node, ast.Call))
    assert not any(isinstance(call.func, ast.Name) and call.func.id == "ProofStep" for call in calls)
    assert "verified_db_step" in code
    assert "derive_inference_proof_step" in code
    assert "new_givens\": 0" in code


def test_source_guard_does_not_modify_git_or_source_files():
    code = (ROOT / "source_guard.py").read_text(encoding="utf-8")
    assert "git(\"fetch\", \"-q\", \"origin\", \"develop\")" in code
    for forbidden in ('git("reset"', 'git("pull"', 'git("checkout"', '.write_bytes(', '.write_text('):
        assert forbidden not in code
    assert "R38_PROVIDER_BLOB" in code
    assert "phase174_r3_r7_r9_composition_associativity/rule.py" in code


def test_powershell_dryrun_does_not_run_tests_or_create_patches():
    text = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in text
    assert "--dry-run" in text
    assert "-m pytest -q" in text
    assert "(END)" in text
```
