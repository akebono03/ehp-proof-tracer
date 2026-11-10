# R51 追加コード全文

全て新規ファイル。既存の import・クラス・関数は変更しない。以下のコードは `run.ps1` を含めてそのまま配置できる単位である。

## `phase174_r3_r7_r51_public_route_gap_audit/__init__.py`

```python
"""R51: read-only audit of the canonical public group proof path."""

```

## `phase174_r3_r7_r51_public_route_gap_audit/source_guard.py`

```python
"""Pin the actual current develop commit and its reviewed source files.

This guard does not use the stale R50 source guard, whose HEAD limit predates
its merger. No tracked production edits are allowed in this audit.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "a77592da1c8ae5aa1d33969ef9674ce914bce341"
REVIEWED_BLOBS = {
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/audit.py": "033410427c965f73080d6a9c3ed42f93129b0950",
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/source_guard.py": "ceb31b6f567858aca861235df68304cafd53a3c2",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase165_r52_r3_web_adapter.py": "dda215780c0468cf421592aff86c79b1f5482eed",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase173_r4_r11_zero_public_connection/route.py": "e3230eed2dfa8dd3efc60cc0a03f787fa92bbeaa",
}


def git(*arguments: str) -> str:
    result = subprocess.run(("git",) + arguments, cwd=ROOT, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    canonical = data.replace(b"\r\n", b"\n")
    return any(git_blob(candidate) == expected for candidate in (
        data, canonical, canonical.replace(b"\n", b"\r\n"),
    ))


def verify_checkout() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R51 must be extracted into the checkout root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R51 requires develop")
    local = git("rev-parse", "HEAD")
    text = git("ls-remote", "origin", "refs/heads/develop")
    remote = text.split()[0] if text else ""
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit required")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("R51 requires no staged/modified tracked files")
    for relative, sha in REVIEWED_BLOBS.items():
        path = ROOT / relative
        if not path.is_file() or not matches_blob(path.read_bytes(), sha):
            raise RuntimeError("Reviewed file differs: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local,
        "remote_head": remote,
        "reviewed_files": len(REVIEWED_BLOBS),
        "production_files_changed": 0,
        "full_pytest": False,
    }

```

## `phase174_r3_r7_r51_public_route_gap_audit/audit.py`

```python
"""R51: compare the actual public group search and Web model with R50.

Read-only. Do not replace the public provider with R50's curated provider, or
make any group-specific Narrative. Inspect real source-linked candidate shapes
and the canonical public search's observed ProofStep list.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import verify_checkout


def inspect_public_route_gap() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r50_root_exactness_terminal_zero_frontier.audit import (
        inspect_integrated_root_frontier,
    )
    from proof import ProofRule, Relation
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))

    # This is the EXACT public group search entry, with its ordinary bridge
    # and context sink. No preselected R50 provider is passed to it.
    contexts = []
    original = build_shared_typed_bridge()
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=original, context_sink=contexts.append,
    )
    if len(contexts) != 1:
        raise RuntimeError("Public group search did not expose one screened context")
    screened = contexts[0]
    provider = shared_expansion_provider(screened, proof_target=goal)

    root_options = tuple(option for option in provider(goal)
                         if option.rule.name == ROOT_RULE)
    if len(root_options) != 1 or root_options[0].subgoals != ehp_zero_inputs(goal):
        raise RuntimeError("Public EHP root candidate differs from reviewed R50")
    upper = root_options[0].subgoals[0]
    upper_options = tuple(option for option in provider(upper)
                          if option.rule.name == UPPER_RULE)
    if len(upper_options) != 1 or upper_options[0].subgoals != upper_delta_surjectivity_inputs(upper):
        raise RuntimeError("Public upper Delta proof candidate differs from reviewed R50")
    kernel_goal = upper_options[0].subgoals[2]
    if not isinstance(kernel_goal, KernelMultipleStatement):
        raise RuntimeError("Upper Delta no longer demands a kernel multiple")
    kernel_options = tuple(option for option in provider(kernel_goal)
                           if option.rule.name == KERNEL_RULE)
    if len(kernel_options) != 1 or len(kernel_options[0].subgoals) != 3:
        raise RuntimeError("Public R35 cited three-premise kernel proposal missing")
    domain = kernel_options[0].subgoals[0]
    if not isinstance(domain, Relation):
        raise RuntimeError("Kernel domain is no longer a typed group Relation")
    direct_domain_steps = tuple(link.step for link in screened.proof_links
                                if link.step is not None
                                and link.step.rule is ProofRule.GIVEN
                                and link.step.conclusion == domain)
    from phase165_r52_r9_shared_math import shared_expansion_provider as build_provider
    domain_options = tuple(x for x in build_provider(screened, proof_target=goal)(domain)
                           if x.rule.name == "generic cited typed scalar specialization"
                           and len(x.subgoals) == 1)
    public_source_bound = tuple(option for option in kernel_options
                                if any(isinstance(x, SourceBoundGoal)
                                       for x in option.subgoals))

    # This is the public model-backed view (same entry called by Group query).
    # A complete view must pass the existing proof-tree trust boundary, which
    # we do not bypass, stub or replace.
    web_view = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    if web_view.n != n or web_view.k != k:
        raise RuntimeError("Public Web view target differs")
    web_complete = web_view.key == "generic-complete-proof" and not web_view.partial_result
    result_complete = result.status is ProofSearchStatus.COMPLETE
    if result_complete != web_complete:
        raise RuntimeError("Public search and Web model disagree on completion")
    if result_complete and result.conclusion != goal:
        raise RuntimeError("Completed public result differs from target")

    # Independent observation: R50's source-checked, scoped inference proof.
    # This is NOT installed in the public search and is not injected as steps.
    r50 = inspect_integrated_root_frontier()
    if (r50["canonical_status"] != "complete"
            or r50["canonical_root_verified_complete"] is not True
            or r50["canonical_root_four_independent_inference_parents"] is not True
            or r50["canonical_root_has_all_six_cited_facts"] is not True
            or r50["canonical_open_goal_types"] != {}):
        raise RuntimeError("R50 certified scoped root proof contract changed")

    original_types = dict(sorted(Counter(type(x).__name__ for x in result.open_goals).items()))
    proven_types = dict(sorted(Counter(type(x.conclusion).__name__
                                    for x in result.proven_steps).items()))
    same_scoped_public = result_complete and web_complete
    gap = not same_scoped_public
    # No mathematical rule is changed here. An inferred-domain requirement
    # may need a generic SourceBoundGoal in ordinary search, not the R50-only
    # goal-by-goal provider filtering. This is a diagnostic, NOT a proof.
    source_bound_missing = bool(direct_domain_steps and domain_options and
                                not public_source_bound)
    if gap and source_bound_missing:
        gate = "PASS_R51_PUBLIC_SOURCE_BOUND_KERNEL_GAP_IDENTIFIED"
    elif gap:
        gate = "PASS_R51_PUBLIC_SCOPED_SEARCH_GAP_RECORDED"
    else:
        gate = "PASS_R51_PUBLIC_ROOT_PROOF_PRESENT_HTTP_PENDING"
    return {
        "target": "pi_12^7 = 0",
        "r50_scoped_complete": True,
        "r50_scoped_verified_steps": r50["canonical_verified_steps"],
        "r50_scoped_root_has_six_cited_facts": True,
        "r50_proof_not_injected_into_public": True,
        "public_result_status": result.status.value,
        "public_result_verified_steps": len(result.proven_steps),
        "public_result_open_goal_types": original_types,
        "public_result_proven_goal_types": proven_types,
        "public_result_diagnostics": list(result.diagnostics),
        "public_root_proof_complete": result_complete,
        "public_root_inference_count": sum(
            step.conclusion == goal and step.rule is ProofRule.INFERENCE
            for step in result.proven_steps
        ),
        "public_screened_source_links": len(screened.proof_links),
        "public_root_ehp_candidates": len(root_options),
        "public_upper_delta_candidates": len(upper_options),
        "public_r35_kernel_candidates": len(kernel_options),
        "public_r35_kernel_requires_bare_relation": any(
            isinstance(x, Relation) for x in kernel_options[0].subgoals
        ),
        "public_r35_kernel_source_bound_candidates": len(public_source_bound),
        "public_kernel_domain_direct_givens": len(direct_domain_steps),
        "public_kernel_domain_cited_specializations": len(domain_options),
        "public_source_bound_kernel_gap_candidate": source_bound_missing,
        "public_web_key": web_view.key,
        "public_web_partial_result": web_view.partial_result,
        "public_web_rendered_lines": len(web_view.rendered_lines),
        "public_web_model_route_checked": True,
        "public_http_checked": False,
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
    audit = None if args.dry_run else inspect_public_route_gap()
    data = {
        "phase": "174-R3-R7-R51",
        "git_state": state,
        "observations": audit,
        "new_given": 0,
        "production_files_changed": 0,
        "full_pytest": False,
        "gate": "PASS_R51_PUBLIC_ROUTE_PREFLIGHT" if args.dry_run else audit["gate"],
    }
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = base / "EHPProofTracerAudit" / "phase174_r3_r7_r51"
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / ("preflight.json" if args.dry_run else "public_route_gap.json")
    dest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tag = "PHASE174_R3R7R51_"
    for key, value in state.items():
        print(tag + key.upper() + "=" + str(value))
    if audit is not None:
        for key, value in audit.items():
            print(tag + key.upper() + "=" + str(value))
    print(tag + "REPORT=" + str(dest))
    print(tag + "GATE=" + data["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `phase174_r3_r7_r51_public_route_gap_audit/tests/test_static.py`

```python
"""R51 remains a read-only public-route diagnosis."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r51_python_files_parse_without_ellipsis() -> None:
    for relative in ("audit.py", "source_guard.py", "tests/test_static.py",
                     "tests/test_guard.py", "tests/test_public.py"):
        tree = ast.parse((PACKAGE / relative).read_text(encoding="utf-8"))
        assert not any(isinstance(item, ast.Constant) and item.value is Ellipsis
                       for item in ast.walk(tree))


def test_r51_does_not_install_math_or_replace_renderer() -> None:
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "search_group_from_registered_goal(" in audit
    assert "build_standard_web_group_proof_view(" in audit
    assert "inspect_integrated_root_frontier()" in audit
    assert "ProofStep(" not in audit
    assert "write_text(" not in audit.split("def main()")[0]
    assert "FULL_PYTEST=False" in script
    assert "pytest -q" in script
    for illegal in ("git reset", "git clean", "install.py", "patch.py"):
        assert illegal not in script


def test_r51_public_provider_is_not_replaced_by_curated_r50_provider() -> None:
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "shared_expansion_provider(screened, proof_target=goal)" in audit
    assert "bridge=original, context_sink=contexts.append" in audit
    assert "source_bound_missing" in audit
    assert "R50" in audit

```

## `phase174_r3_r7_r51_public_route_gap_audit/tests/test_guard.py`

```python
"""R51 pins the merged R50 review and all public search entry points."""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.source_guard import (
    REVIEWED_BLOBS, REVIEWED_HEAD, git_blob, matches_blob, verify_checkout,
)


def test_source_guard_rejects_unreviewed_blob() -> None:
    assert len(REVIEWED_BLOBS) == 12
    assert len(REVIEWED_HEAD) == 40
    for digest in REVIEWED_BLOBS.values():
        assert len(digest) == 40
    assert matches_blob(b"small", git_blob(b"small"))
    assert not matches_blob(b"changed", git_blob(b"small"))


def test_source_guard_requires_reviewed_live_develop() -> None:
    result = verify_checkout()
    assert result["source_guard"] == "PASS"
    assert result["local_head"] == REVIEWED_HEAD
    assert result["remote_head"] == REVIEWED_HEAD
    assert result["production_files_changed"] == 0
    assert result["full_pytest"] is False

```

## `phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py`

```python
"""Compare actual public search and scoped R50 without installing a proof."""
from __future__ import annotations

from phase174_r3_r7_r51_public_route_gap_audit.audit import inspect_public_route_gap


def test_source_backed_scoped_root_is_complete_and_not_injected() -> None:
    report = inspect_public_route_gap()
    assert report["r50_scoped_complete"] is True
    assert report["r50_scoped_verified_steps"] == 28
    assert report["r50_scoped_root_has_six_cited_facts"] is True
    assert report["r50_proof_not_injected_into_public"] is True
    assert report["new_given"] == 0
    assert report["production_files_changed"] == 0


def test_public_search_and_web_model_have_same_completion_status() -> None:
    report = inspect_public_route_gap()
    if report["public_root_proof_complete"]:
        assert report["public_result_status"] == "complete"
        assert report["public_web_key"] == "generic-complete-proof"
        assert report["public_web_partial_result"] is False
    else:
        assert report["public_result_status"] in ("partial", "search_failed")
        assert report["public_web_key"] == "generic-partial-proof"
        assert report["public_web_partial_result"] is True
    assert report["public_web_model_route_checked"] is True
    assert report["public_http_checked"] is False


def test_public_kernel_candidate_must_be_present_without_forcing_completion() -> None:
    report = inspect_public_route_gap()
    assert report["public_root_ehp_candidates"] == 1
    assert report["public_upper_delta_candidates"] == 1
    assert report["public_r35_kernel_candidates"] == 1
    assert report["public_r35_kernel_requires_bare_relation"] is True
    assert report["public_r35_kernel_source_bound_candidates"] == 0
    assert report["public_kernel_domain_cited_specializations"] >= 1
    assert report["gate"].startswith("PASS_R51_")

```

## `phase174_r3_r7_r51_public_route_gap_audit/run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r51_public_route_gap_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R51 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R51_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r51_public_route_gap_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R51 public route audit failed' }
    $Groups = @(
        @{Name='R51_STATIC'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_static.py'; Mode='importlib'},
        @{Name='R51_GUARD'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_guard.py'; Mode='importlib'},
        @{Name='R51_PUBLIC'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'; Mode='importlib'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'; Mode='importlib'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R51_TEST_GROUP=' + $Group.Name)
        $Mode = $Group.Mode
        python -B -m pytest -q "--import-mode=$Mode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R51 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R51_RUN=PASS'
    Write-Output 'PHASE174_R3R7R51_PRODUCTION_FILES_CHANGED=0'
    Write-Output 'PHASE174_R3R7R51_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```
