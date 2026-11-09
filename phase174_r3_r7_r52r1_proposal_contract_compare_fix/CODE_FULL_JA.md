# R52R1 変更・新規コード全文
次のファイルに含まれるコードはすべて省略なしの置換可能な全文。`audit.py` の import も全文表示する。
## 変更対象の一覧
- `phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py`: `inspect_public_kernel_source_bound_probe` 全体。
- `phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py`: `proposal_contract` を最初のテストの直前に追加。その他の既存・新規テストを含むファイル全文。
- `phase174_r3_r7_r52r1_proposal_contract_compare_fix/`: 新規クラスなし、`patch.py` 関数群・`tests/test_patch.py` テスト関数群と `run.ps1`。

## R52 置換: audit.py（全文）
```python
"""R52: measure a generic SourceBoundGoal wrapper against the real public route.

No installation, direct mathematical assertions, Web overrides or fake proofs.
A candidate is not a proof: report the actual verified canonical DFS status.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout


def inspect_public_kernel_source_bound_probe() -> dict[str, object]:
    """Run a fresh ordinary DFS with only the cited kernel-domain preference."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.probe import (
        build_source_bound_kernel_probe,
    )
    from proof import ProofRule, ProofStep
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    original_bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    public_result = search_group_from_registered_goal(
        n=n, k=k, bridge=original_bridge, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("R52 cannot identify the actual screened public context")
    screened = contexts[0]
    original = shared_expansion_provider(screened, proof_target=goal)
    probe = build_source_bound_kernel_probe(original, screened)
    root_options = tuple(x for x in original(goal) if x.rule.name == ROOT_RULE)
    if len(root_options) != 1 or root_options[0].subgoals != ehp_zero_inputs(goal):
        raise RuntimeError("R52 public root expansion changed")
    upper_options = upper_delta_surjectivity_inputs(root_options[0].subgoals[0])
    if upper_options is None:
        raise RuntimeError("R52 upper Delta typed prerequisites changed")
    kernel_goal = upper_options[2]
    if type(kernel_goal) is not KernelMultipleStatement:
        raise RuntimeError("R52 expected a typed R35 kernel obligation")
    original_kernel = tuple(x for x in original(kernel_goal) if x.rule.name == KERNEL_RULE)
    augmented = tuple(x for x in probe(kernel_goal) if x.rule.name == KERNEL_RULE)
    bound = tuple(x for x in augmented if any(
        isinstance(s, SourceBoundGoal) for s in x.subgoals
    ))
    if len(original_kernel) != 1:
        raise RuntimeError("R52 expected exactly one public R35 kernel proposal")
    if any(x.rule.name != KERNEL_RULE for x in bound):
        raise RuntimeError("R52 changed a non-R35 inference")
    # Runtime-generated InferenceRule objects contain distinct match_guard
    # closures. Compare the stable proposal contract instead of function identity.
    def contract(option: object) -> tuple[object, ...]:
        rule = option.rule
        return (
            type(rule), rule.name, rule.description,
            rule.premise_patterns, rule.conclusion_pattern,
            rule.literature_reference, option.subgoals,
        )

    if tuple(contract(item) for item in probe(goal)) != tuple(
        contract(item) for item in original(goal)
    ):
        raise RuntimeError("R52 changed the public root expansion")
    citing_id = next(iter(original_bridge.registry._assertions)).assertion_id
    probed = search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=screened,
        citing_assertion_id=citing_id, expansion_provider=probe,
        lookup_mode="typed_reference",
    )
    root_steps = tuple(step for step in probed.proven_steps
                       if step.conclusion == goal and step.rule is ProofRule.INFERENCE)
    kernel_steps = tuple(step for step in probed.proven_steps
                         if step.conclusion == kernel_goal and step.rule is ProofRule.INFERENCE)
    domain_step_is_inferred = any(
        len(step.premises) == 3
        and step.premises[0].rule is ProofRule.INFERENCE
        and step.premises[1].rule is ProofRule.GIVEN
        and step.premises[2].rule is ProofRule.GIVEN
        for step in kernel_steps
    )
    root_has_four_inferred = any(
        len(step.premises) == 4
        and tuple(parent.conclusion for parent in step.premises) == root_options[0].subgoals
        and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
        for step in root_steps
    )
    expected_locators = {
        "(5.9)", "Proposition 4.2 (4.4)",
        "Proposition 5.8", "(5.10)",
        "Proposition 2.7", "(5.1)",
    }
    def ancestor_locators(step: ProofStep) -> set[str]:
        found: set[str] = set()
        visited: set[int] = set()
        def visit(current: ProofStep) -> None:
            if id(current) in visited:
                return
            visited.add(id(current))
            if current.rule is ProofRule.GIVEN:
                cite = getattr(getattr(current.inference_rule, "literature_reference", None),
                               "locator", None)
                if isinstance(cite, str):
                    found.add(cite)
            for parent in current.premises:
                visit(parent)
        visit(step)
        return found
    matching_citations = any(expected_locators.issubset(ancestor_locators(step))
                             for step in root_steps)
    actual_complete = probed.status is ProofSearchStatus.COMPLETE
    if actual_complete and (probed.conclusion != goal or not root_has_four_inferred
                            or not matching_citations or not domain_step_is_inferred):
        raise RuntimeError("R52 claims completion without the actual verified EHP root")
    if root_steps and not actual_complete:
        raise RuntimeError("R52 observed a root inference but returned partial status")
    web = build_standard_web_group_proof_view(
        n=n, k=k, mode="narrative", citation_source="model",
    )
    if (web.partial_result != (public_result.status is not ProofSearchStatus.COMPLETE)):
        raise RuntimeError("R52 public model and group search disagree")
    gate = (
        "PASS_R52_GENERIC_BOUND_PUBLIC_PROVIDER_PROBE_COMPLETE_NOT_INSTALLED"
        if actual_complete and bound else
        "PASS_R52_GENERIC_BOUND_ADDITIONAL_PUBLIC_GAP_IDENTIFIED"
    )
    return {
        "root": "pi_12^7 = 0",
        "public_status": public_result.status.value,
        "public_verified_steps": len(public_result.proven_steps),
        "public_web_key": web.key,
        "public_web_partial_result": web.partial_result,
        "public_web_http_checked": False,
        "public_provider_unchanged": True,
        "public_r35_unbound_candidates": len(original_kernel),
        "probe_r35_source_bound_candidates": len(bound),
        "probe_generic_rule_name": KERNEL_RULE,
        "probe_root_candidate_unchanged": True,
        "probe_status": probed.status.value,
        "probe_verified_steps": len(probed.proven_steps),
        "probe_open_goal_types": dict(sorted(Counter(type(x).__name__ for x in probed.open_goals).items())),
        "probe_proven_goal_types": dict(sorted(Counter(type(x.conclusion).__name__
                                                   for x in probed.proven_steps).items())),
        "probe_diagnostics": list(probed.diagnostics),
        "probe_kernel_inference_count": len(kernel_steps),
        "probe_kernel_domain_inferred": domain_step_is_inferred,
        "probe_root_inference_count": len(root_steps),
        "probe_root_four_inferred_parents": root_has_four_inferred,
        "probe_root_six_cited_ancestors": matching_citations,
        "probe_root_complete": actual_complete and root_has_four_inferred and matching_citations,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "full_pytest": False,
        "gate": gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observations = None if args.dry_run else inspect_public_kernel_source_bound_probe()
    gate = "PASS_R52_REVIEWED_R51_PREFLIGHT" if args.dry_run else observations["gate"]
    report = {
        "phase": "174-R3-R7-R52",
        "state": state,
        "observations": observations,
        "gate": gate,
    }
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r52"
    )
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / ("preflight.json" if args.dry_run else "public_kernel_bound_probe.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R52_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observations is not None:
        for key, value in observations.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## R52 置換: tests/test_probe.py（全文）
```python
"""R52 tests the generic proposal shape and real canonical proof boundaries."""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r3_recursive_search import SourceBoundGoal
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
from phase174_r3_r7_r52_public_kernel_source_bound_probe.audit import (
    inspect_public_kernel_source_bound_probe,
)
from phase174_r3_r7_r52_public_kernel_source_bound_probe.probe import (
    build_source_bound_kernel_probe,
)


def proposal_contract(option: object) -> tuple[object, ...]:
    """Compare a generated rule's public contract, not closure identity."""
    rule = option.rule
    return (
        type(rule), rule.name, rule.description,
        rule.premise_patterns, rule.conclusion_pattern,
        rule.literature_reference, option.subgoals,
    )


def test_generic_wrapper_adds_only_cited_r35_kernel_obligation() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    original = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(original, goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    wrapper = build_source_bound_kernel_probe(provider, screened)
    upper = ehp_zero_inputs(root)[0]
    kernel = upper_delta_surjectivity_inputs(upper)[2]
    before = provider(kernel)
    after = wrapper(kernel)
    bound = tuple(x for x in after if x.rule.name == KERNEL_RULE
                  and isinstance(x.subgoals[0], SourceBoundGoal))
    assert all(x.rule.name == KERNEL_RULE for x in bound)
    original_r35 = tuple(x for x in before if x.rule.name == KERNEL_RULE)
    assert len(original_r35) == 1
    assert all(x.subgoals[0].conclusion == original_r35[0].subgoals[0]
               for x in bound)
    assert tuple(proposal_contract(x) for x in after[-len(before):]) == tuple(
        proposal_contract(x) for x in before
    )
    assert tuple(proposal_contract(x) for x in wrapper(root)) == tuple(
        proposal_contract(x) for x in provider(root)
    )


def test_generated_rule_closure_identity_does_not_change_root_contract() -> None:
    """A provider may rebuild an equivalent inference guard on each call."""
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        expand_ehp_zero_from_delta_surjectivity,
    )

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    first = expand_ehp_zero_from_delta_surjectivity(goal)
    second = expand_ehp_zero_from_delta_surjectivity(goal)
    assert len(first) == len(second) == 1
    assert first[0].rule.match_guard is not second[0].rule.match_guard
    assert proposal_contract(first[0]) == proposal_contract(second[0])


def test_missing_screened_cited_proof_link_never_adds_source_bound() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    no_links = RegistryBridgeResult(screened.registry, screened.records, ())
    wrapper = build_source_bound_kernel_probe(provider, no_links)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    assert tuple(proposal_contract(x) for x in wrapper(kernel)) == tuple(
        proposal_contract(x) for x in provider(kernel)
    )


def test_probe_reports_actual_canonical_progress_and_does_not_claim_web() -> None:
    report = inspect_public_kernel_source_bound_probe()
    assert report["public_provider_unchanged"] is True
    assert report["public_web_http_checked"] is False
    assert type(report["probe_r35_source_bound_candidates"]) is int
    assert report["probe_r35_source_bound_candidates"] >= 0
    assert report["public_r35_unbound_candidates"] == 1
    assert report["probe_root_candidate_unchanged"] is True
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    if report["probe_status"] == "complete":
        assert report["probe_root_complete"] is True
        assert report["probe_root_inference_count"] == 1
        assert report["probe_root_four_inferred_parents"] is True
        assert report["probe_root_six_cited_ancestors"] is True
        assert report["probe_kernel_domain_inferred"] is True
    else:
        assert report["probe_root_inference_count"] == 0
        assert report["probe_root_complete"] is False
        assert report["probe_open_goal_types"]
```

## R52R1 新規: patch.py（全文）
```python
"""R52R1: guarded replacement of unstable generated-rule object comparisons.

Patches only R52's audit and focused tests. No production source, mathematical
rule, source registry, or common renderer is changed.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET_PREFIX = "phase174_r3_r7_r52_public_kernel_source_bound_probe/"
TARGETS = (
    TARGET_PREFIX + "audit.py",
    TARGET_PREFIX + "tests/test_probe.py",
)
EXPECTED_HASHES = {'phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py': ('aee32aed10be84fc7cd8e2f3541ed986c0f05ef73c79eb684c902bceeb854b65', '5c2899abda9d4e38352d0aec7e5d91c065d8fab8fb3839e7240ad76183f6d6fe'), 'phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py': ('f39b4fff0f54a0dc8d4eeda40d7b7598a3cbaaaa7ec46ffc96c09bd7b9a26e1b', '3d5c34cfac99501b8aa1f6531866cb512cf77a30c2185047b0842b7477bbc865')}


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def bundled_paths(relative: str) -> tuple[Path, Path]:
    if relative not in TARGETS or not relative.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R52R1 patch target")
    suffix = relative[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / suffix, PACKAGE / "replacement" / suffix


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    decisions: list[tuple[Path, Path, str]] = []
    for relative in TARGETS:
        baseline, replacement = bundled_paths(relative)
        destination = root / relative
        if not all(path.is_file() for path in (baseline, replacement, destination)):
            raise RuntimeError("Missing reviewed R52R1 file: " + relative)
        before, after = EXPECTED_HASHES[relative]
        if normalized_sha256(baseline.read_bytes()) != before:
            raise RuntimeError("Bundled baseline changed: " + relative)
        if normalized_sha256(replacement.read_bytes()) != after:
            raise RuntimeError("Bundled replacement changed: " + relative)
        current = normalized_sha256(destination.read_bytes())
        if current not in (before, after):
            raise RuntimeError("R52 source is not reviewed baseline/replacement: " + relative)
        decisions.append((destination, replacement, "ALREADY_REPAIRED" if current == after else "REPLACE"))
    return tuple(decisions)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout

    state = verify_checkout()
    pending = pending_replacements()
    if not args.dry_run:
        for destination, replacement, mode in pending:
            if mode == "REPLACE":
                destination.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("R52R1 replacement verification failed")
    prefix = "PHASE174_R3R7R52R1_"
    for key in ("source_guard", "local_head", "remote_head"):
        print(prefix + key.upper() + "=" + str(state[key]))
    for destination, _, mode in pending:
        print(prefix + "TARGET=" + destination.relative_to(ROOT).as_posix() + ":" + mode)
    print(prefix + "TARGET_FILES=" + str(len(TARGETS)))
    print(prefix + "PRODUCTION_FILES_CHANGED=0")
    print(prefix + "NEW_GIVENS=0")
    print(prefix + "NEW_MATHEMATICAL_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "GATE=" + ("PASS_R52R1_PROPOSAL_CONTRACT_DRYRUN" if args.dry_run else "PASS_R52R1_PROPOSAL_CONTRACT_PATCH_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## R52R1 新規: tests/test_patch.py（全文）
```python
"""R52R1: source-hash and stable-proposal-comparison regressions."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r52r1_proposal_contract_compare_fix.patch import (
    EXPECTED_HASHES,
    PACKAGE,
    TARGETS,
    bundled_paths,
    normalized_sha256,
    pending_replacements,
)


def test_patch_has_only_two_reviewed_r52_targets() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py",
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py",
    )
    for relative in TARGETS:
        baseline, replacement = bundled_paths(relative)
        expected_before, expected_after = EXPECTED_HASHES[relative]
        assert normalized_sha256(baseline.read_bytes()) == expected_before
        assert normalized_sha256(replacement.read_bytes()) == expected_after
        ast.parse(replacement.read_text(encoding="utf-8"))


def test_reviewed_patch_is_idempotent_and_rejects_unaudited_input(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, after = bundled_paths(relative)
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(before.read_bytes())
    first = pending_replacements(tmp_path)
    assert len(first) == 2
    assert all(mode == "REPLACE" for _, _, mode in first)
    for destination, replacement, _ in first:
        destination.write_bytes(replacement.read_bytes())
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in pending_replacements(tmp_path))
    (tmp_path / TARGETS[0]).write_text("unreviewed", encoding="utf-8")
    with pytest.raises(RuntimeError, match="not reviewed"):
        pending_replacements(tmp_path)


def test_audit_checks_stable_contract_not_regenerated_closure_identity() -> None:
    source = (PACKAGE / "replacement/audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "if probe(goal) != original(goal)" not in source
    assert "contract(item) for item in probe(goal)" in source
    assert "contract(item) for item in original(goal)" in source
    assert "rule.premise_patterns, rule.conclusion_pattern" in source
    assert "rule.literature_reference, option.subgoals" in source
    assert "ProofStep(" not in source
    assert not any(
        isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis for node in ast.walk(tree)
    )


def test_probe_regression_has_new_guard_comparison_fixture() -> None:
    source = (PACKAGE / "replacement/tests/test_probe.py").read_text(encoding="utf-8")
    assert "test_generated_rule_closure_identity_does_not_change_root_contract" in source
    assert "wrapper(root) == provider(root)" not in source
    assert "wrapper(kernel) == provider(kernel)" not in source
    assert "after[-len(before):] == before" not in source
    assert "proposal_contract(x) for x in wrapper(root)" in source
    assert "proposal_contract(x) for x in after[-len(before):]" in source
    assert "assert first[0].rule.match_guard is not second[0].rule.match_guard" in source
```

## R52R1 新規: run.ps1（全文）
```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r52r1_proposal_contract_compare_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R52R1 preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R52R1_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r52r1_proposal_contract_compare_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R52R1 guarded repair failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r52_public_kernel_source_bound_probe\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R52 probe audit or regression tests failed' }
    Write-Output 'PHASE174_R3R7R52R1_TEST_GROUP=R52R1_PATCH'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider '.\phase174_r3_r7_r52r1_proposal_contract_compare_fix\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R52R1 patch focused tests failed' }
    Write-Output 'PHASE174_R3R7R52R1_RUN=PASS'
    Write-Output 'PHASE174_R3R7R52R1_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## R52R1 新規: __init__.py（全文）
```python
"""R52R1 audited repair of generated proposal comparison."""
```
