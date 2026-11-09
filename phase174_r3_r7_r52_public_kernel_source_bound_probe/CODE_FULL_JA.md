# R52 新規コード全文

対象: 新規 `phase174_r3_r7_r52_public_kernel_source_bound_probe/` のみ。変更する既存クラス・既存関数・既存 import はありません。

以下は新規ファイル全文です。

## phase174_r3_r7_r52_public_kernel_source_bound_probe/source_guard.py

```python
"""R52: pin the reviewed develop commit and all material mathematical sources.

R51 is merged, so its own old HEAD guard is intentionally not invoked.
No production files are modified or allowed to differ from their reviewed blobs.
"""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import (
    ROOT,
    REVIEWED_BLOBS as R51_PROTECTED_BLOBS,
    git,
    matches_blob,
)

REVIEWED_HEAD = "0d0b6b31582ff3e505d14fdde5eaf5e9a0b343d7"
R51_HANDOFF_BLOBS = {
    "phase174_r3_r7_r51_public_route_gap_audit/audit.py": "9f48c852950be09f44ef2ffe653c54a5fc59a090",
    "phase174_r3_r7_r51_public_route_gap_audit/source_guard.py": "28a3d2ff73a26a7edd29de90946d9bdcc7ffb9fd",
    "phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py": "2e7ee99bbdfe0c6e0720e615d9a932c9d9ac54c7",
}


def verify_checkout() -> dict[str, object]:
    """Reject unreviewed committed or tracked changes and all stale citations."""
    if git("rev-parse", "--show-toplevel") != str(ROOT):
        from pathlib import Path
        if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
            raise RuntimeError("R52 requires the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R52 requires branch develop")
    local = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD: re-audit the R52 source pins")
    if git("diff", "--name-only") or git("diff", "--cached", "--name-only"):
        raise RuntimeError("R52 does not allow modified/staged tracked files")
    pins = {**R51_PROTECTED_BLOBS, **R51_HANDOFF_BLOBS}
    if len(pins) != len(R51_PROTECTED_BLOBS) + len(R51_HANDOFF_BLOBS):
        raise RuntimeError("R52 protected source paths overlap")
    for relative, sha in pins.items():
        path = ROOT / relative
        if not path.is_file() or not matches_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed source changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local,
        "remote_head": remote,
        "reviewed_files": len(pins),
        "production_files_changed": 0,
        "full_pytest": False,
    }

```

## phase174_r3_r7_r52_public_kernel_source_bound_probe/probe.py

```python
"""R52: non-installed, generic source-bound R35 kernel-domain provider probe.

Only the proof obligation is constrained. It does not construct a ProofStep,
create a GIVEN, change R35's inference rule, or specialize by group indices.
"""
from __future__ import annotations

from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

SPECIALIZATION_RULE = "generic cited typed scalar specialization"


def cited_inferred_domain_sources(
    domain: Relation,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> tuple[object, ...]:
    """Find only individually link-certified fixed sources that infer a domain.

    A plain earlier DB row and a proposition label are insufficient. The
    existing checked specialization rule must match the actual linked GIVEN.
    """
    if type(domain) is not Relation or not isinstance(bridge, RegistryBridgeResult):
        return ()
    valid: list[object] = []
    for option in provider(domain):
        if (type(option) is not GoalExpansion
                or option.rule.name != SPECIALIZATION_RULE
                or len(option.subgoals) != 1):
            continue
        source = option.subgoals[0]
        for link in bridge.proof_links:
            step = link.step
            if (not isinstance(step, ProofStep)
                    or step.rule is not ProofRule.GIVEN
                    or step.premises
                    or step.conclusion != source):
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or assertion.content != source
                    or type(reference.publication_position) is not int
                    or reference.publication_position < 1
                    or getattr(getattr(step.inference_rule, "literature_reference", None),
                               "locator", None) != reference.locator):
                continue
            if not find_inference_matches_for_rule(option.rule, (step,)):
                continue
            if not any(type(old) is type(source) and old == source for old in valid):
                valid.append(source)
    return tuple(valid)


def build_source_bound_kernel_probe(
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Prepend a cited inference obligation for every eligible R35 kernel.

    Keep all original options as fallback. The first actual successful proof
    is still selected by the ordinary recursive engine, not by this probe.
    """
    if not callable(provider) or not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("expected a shared provider and screened source bridge")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        original = provider(goal)
        if type(goal) is not KernelMultipleStatement:
            return original
        bound: list[GoalExpansion] = []
        for option in original:
            if (type(option) is not GoalExpansion
                    or option.rule.name != KERNEL_RULE
                    or len(option.subgoals) != 3
                    or type(option.subgoals[0]) is not Relation):
                continue
            domain = option.subgoals[0]
            for source in cited_inferred_domain_sources(domain, provider, bridge):
                proposal = GoalExpansion(
                    rule=option.rule,
                    subgoals=(SourceBoundGoal(conclusion=domain, source=source),)
                    + option.subgoals[1:],
                )
                if proposal not in bound:
                    bound.append(proposal)
        return tuple(bound) + original

    return expand

```

## phase174_r3_r7_r52_public_kernel_source_bound_probe/audit.py

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
    if probe(goal) != original(goal):
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

## phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_guard.py

```python
"""R52 pins actual GitHub R51 merge and reviewed mathematical file content."""
from __future__ import annotations

from phase174_r3_r7_r52_public_kernel_source_bound_probe.source_guard import (
    REVIEWED_HEAD, R51_HANDOFF_BLOBS, R51_PROTECTED_BLOBS, ROOT,
    verify_checkout,
)


def test_new_head_and_r51_handoff_are_reviewed() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert len(R51_HANDOFF_BLOBS) == 3
    assert len(R51_PROTECTED_BLOBS) == 12
    assert ROOT.is_absolute()


def test_source_guard_rejects_modified_production_and_verifies_head() -> None:
    result = verify_checkout()
    assert result["source_guard"] == "PASS"
    assert result["remote_head"] == REVIEWED_HEAD
    assert result["reviewed_files"] == 15
    assert result["production_files_changed"] == 0

```

## phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py

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
    assert after[-len(before):] == before
    assert wrapper(root) == provider(root)


def test_missing_screened_cited_proof_link_never_adds_source_bound() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    provider = shared_expansion_provider(screened, proof_target=root)
    no_links = RegistryBridgeResult(screened.registry, screened.records, ())
    wrapper = build_source_bound_kernel_probe(provider, no_links)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    assert wrapper(kernel) == provider(kernel)


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

## phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py

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

```

## phase174_r3_r7_r52_public_kernel_source_bound_probe/run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r52_public_kernel_source_bound_probe.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R52 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R52_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r52_public_kernel_source_bound_probe.audit
    if ($LASTEXITCODE -ne 0) { throw 'R52 probe audit failed' }
    $Groups = @(
        @{Name='R52_STATIC'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_static.py'},
        @{Name='R52_GUARD'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_guard.py'},
        @{Name='R52_PROBE'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'},
        @{Name='R51_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R52_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R52 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R52_RUN=PASS'
    Write-Output 'PHASE174_R3R7R52_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```
