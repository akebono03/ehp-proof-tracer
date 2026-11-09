# R52R2 コード全文（置換可能な完全単位）

## 変更一覧と追加位置

- `phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py`: `inspect_public_kernel_source_bound_probe()` 内の `citing_id` 取得を修正。以下はファイル全文（import も省略なし）。
- `phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py`: 末尾に新規テストを追加。以下はファイル全文（import も省略なし）。
- 新規 `phase174_r3_r7_r52r2_registry_assertion_id_fix/patch.py`: ファイル全文。
- 新規 `phase174_r3_r7_r52r2_registry_assertion_id_fix/tests/test_patch.py`: ファイル全文。
- 新規 `run.ps1`: スクリプト全文。

## 修正後 R52 audit.py

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
    citing_id = next(iter(original_bridge.registry._assertions.values())).assertion_id
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


## 修正後 R52 tests/test_static.py

```python
"""R52 does not install a source, mathematics, or display override."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r52_sources_parse_and_have_no_ellipsis() -> None:
    for path in (PACKAGE / "audit.py", PACKAGE / "source_guard.py", PACKAGE / "probe.py", *sorted((PACKAGE / "tests").glob("test_*.py"))):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                       and node.value.value is Ellipsis for node in ast.walk(tree))


def test_production_is_unchanged_and_probe_is_not_goal_specific() -> None:
    code = (PACKAGE / "probe.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in code
    assert "n=7" not in code and "k=5" not in code
    assert "SourceBoundGoal(conclusion=domain, source=source)" in code
    assert "return tuple(bound) + original" in code
    assert "find_inference_matches_for_rule(option.rule, (step,))" in code


def test_runner_stops_on_failures_and_has_no_global_pytest() -> None:
    code = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in code
    assert "--import-mode=importlib" in code
    assert "FULL_PYTEST=False" in code
    assert "git reset" not in code and "git clean" not in code
    assert "install.py" not in code

def test_citing_id_comes_from_registry_assertion_value_not_dict_key() -> None:
    """Dict iteration yields a string key; only the assertion value has assertion_id."""
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    audit = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "inspect_public_kernel_source_bound_probe"
    )
    statements = (
        node for node in ast.walk(audit)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "citing_id"
                for target in node.targets)
    )
    assignments = tuple(statements)
    assert len(assignments) == 1
    expression = ast.unparse(assignments[0].value)
    assert expression == (
        "next(iter(original_bridge.registry._assertions.values())).assertion_id"
    )

    class Assertion:
        def __init__(self, assertion_id: str) -> None:
            self.assertion_id = assertion_id

    values = {"source:key": Assertion("source:assertion")}.values()
    assert next(iter(values)).assertion_id == "source:assertion"
```


## R52R2 patch.py

```python
"""R52R2: repair only the registry assertion-id lookup in the R52 audit.

Read-only production: no mathematical rule, provider, Web route or other
application module is changed. Only the R52 audit and static test are replaced.
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
    TARGET_PREFIX + "tests/test_static.py",
)
EXPECTED_HASHES = {'phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py': ('5c2899abda9d4e38352d0aec7e5d91c065d8fab8fb3839e7240ad76183f6d6fe', '40ebfdd1452655f17613bf1927d21151966a0f098287846d1587e952c62442e8'), 'phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py': ('1547a6ab7bf78475d0bd9756bdb6d3b146a8e03324fdb5bc3fea94260c094559', '13976270d406920c26e8fe7dfc27ba2d29144d0c2f5d16dcbd19d8bf9d655b86')}


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def reviewed_paths(relative: str) -> tuple[Path, Path]:
    if relative not in TARGETS or not relative.startswith(TARGET_PREFIX):
        raise ValueError("Unreviewed R52R2 replacement target")
    suffix = relative[len(TARGET_PREFIX):]
    return PACKAGE / "baseline" / suffix, PACKAGE / "replacement" / suffix


def pending_replacements(root: Path = ROOT) -> tuple[tuple[Path, Path, str], ...]:
    decisions: list[tuple[Path, Path, str]] = []
    for relative in TARGETS:
        before, after = reviewed_paths(relative)
        destination = root / relative
        if not all(path.is_file() for path in (before, after, destination)):
            raise RuntimeError("R52R2 target or bundled source missing: " + relative)
        old_hash, new_hash = EXPECTED_HASHES[relative]
        if normalized_sha256(before.read_bytes()) != old_hash:
            raise RuntimeError("R52R2 bundled baseline tampered: " + relative)
        if normalized_sha256(after.read_bytes()) != new_hash:
            raise RuntimeError("R52R2 bundled replacement tampered: " + relative)
        present = normalized_sha256(destination.read_bytes())
        if present not in (old_hash, new_hash):
            raise RuntimeError("Unreviewed R52 working file: " + relative)
        decisions.append((
            destination, after, "ALREADY_REPAIRED" if present == new_hash else "REPLACE",
        ))
    return tuple(decisions)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import verify_checkout
    state = verify_checkout()
    decisions = pending_replacements()
    if not args.dry_run:
        for target, replacement, mode in decisions:
            if mode == "REPLACE":
                target.write_bytes(replacement.read_bytes())
        if any(mode != "ALREADY_REPAIRED" for _, _, mode in pending_replacements()):
            raise RuntimeError("R52R2 replacement verification failed")
    p = "PHASE174_R3R7R52R2_"
    for key in ("source_guard", "local_head", "remote_head"):
        print(p + key.upper() + "=" + str(state[key]))
    for target, _, mode in decisions:
        print(p + "TARGET=" + target.relative_to(ROOT).as_posix() + ":" + mode)
    print(p + "TARGET_FILES=" + str(len(decisions)))
    print(p + "PRODUCTION_FILES_CHANGED=0")
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_MATHEMATICAL_RULES=0")
    print(p + "FULL_PYTEST=False")
    print(p + "GATE=" + (
        "PASS_R52R2_ASSERTION_ID_DRYRUN" if args.dry_run else
        "PASS_R52R2_ASSERTION_ID_PATCH_APPLIED"
    ))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```


## R52R2 tests/test_patch.py

```python
"""R52R2 regression tests: dictionary keys must not be treated as assertion values."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r52r2_registry_assertion_id_fix.patch import (
    EXPECTED_HASHES, PACKAGE, TARGETS, normalized_sha256,
    pending_replacements, reviewed_paths,
)


def test_reviewed_targets_are_audit_and_static_test_only() -> None:
    assert TARGETS == (
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py",
        "phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py",
    )
    assert len(EXPECTED_HASHES) == 2
    for relative in TARGETS:
        baseline, replacement = reviewed_paths(relative)
        assert normalized_sha256(baseline.read_bytes()) == EXPECTED_HASHES[relative][0]
        assert normalized_sha256(replacement.read_bytes()) == EXPECTED_HASHES[relative][1]


def test_registry_lookup_uses_assertion_values_and_is_python310_compatible() -> None:
    source = (PACKAGE / "replacement/audit.py").read_text(encoding="utf-8")
    ast.parse(source, feature_version=(3, 10))
    assert (
        "next(iter(original_bridge.registry._assertions.values())).assertion_id"
        in source
    )
    assert (
        "next(iter(original_bridge.registry._assertions)).assertion_id"
        not in source
    )
    class Assertion:
        def __init__(self, assertion_id: str) -> None:
            self.assertion_id = assertion_id
    items = {"string-key": Assertion("linked-assertion")}
    assert next(iter(items.values())).assertion_id == "linked-assertion"


def test_guard_rejects_unreviewed_file(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, _ = reviewed_paths(relative)
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(before.read_bytes())
    statuses = pending_replacements(tmp_path)
    assert all(mode == "REPLACE" for _, _, mode in statuses)
    first, _, _ = statuses[0]
    first.write_text("# tampered", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unreviewed R52 working file"):
        pending_replacements(tmp_path)


def test_patch_idempotence(tmp_path: Path) -> None:
    for relative in TARGETS:
        before, after = reviewed_paths(relative)
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(before.read_bytes())
        assert normalized_sha256(target.read_bytes()) == normalized_sha256(before.read_bytes())
        target.write_bytes(after.read_bytes())
    results = pending_replacements(tmp_path)
    assert all(mode == "ALREADY_REPAIRED" for _, _, mode in results)


def test_regression_is_a_full_test_function_in_the_r52_static_module() -> None:
    source = (PACKAGE / "replacement/tests/test_static.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert any(
        isinstance(node, ast.FunctionDef)
        and node.name == "test_citing_id_comes_from_registry_assertion_value_not_dict_key"
        for node in tree.body
    )
    assert all(node.value is not Ellipsis for node in ast.walk(tree) if isinstance(node, ast.Constant))
```


## R52R2 run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r52r2_registry_assertion_id_fix.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 source preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R52R2_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r52r2_registry_assertion_id_fix.patch
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 guarded repair failed' }
    powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r52_public_kernel_source_bound_probe\run.ps1'
    if ($LASTEXITCODE -ne 0) { throw 'R52 probe audit or focused regression failed' }
    Write-Output 'PHASE174_R3R7R52R2_TEST_GROUP=R52R2_PATCH'
    python -B -m pytest -q --import-mode=importlib -p no:cacheprovider '.\phase174_r3_r7_r52r2_registry_assertion_id_fix\tests\test_patch.py'
    if ($LASTEXITCODE -ne 0) { throw 'R52R2 patch focused pytest failed' }
    Write-Output 'PHASE174_R3R7R52R2_RUN=PASS'
    Write-Output 'PHASE174_R3R7R52R2_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```


## R52R2 __init__.py

```python
"""R52R2 guarded registry assertion ID audit repair."""
```
