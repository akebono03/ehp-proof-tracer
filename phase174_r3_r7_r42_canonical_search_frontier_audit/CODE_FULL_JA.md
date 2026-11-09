# R42 追加ファイル・関数の全文

既存クラス・関数・import は変更しません。以下のファイルをリポジトリ直下の新規 `phase174_r3_r7_r42_canonical_search_frontier_audit/` に配置してください。

## `__init__.py`（新規）

```python
"""Read-only canonical scoped search frontier audit, Phase 174 R3-R7-R42."""

```

## `source_guard.py`（新規）

```python
"""Read-only GitHub R41 handoff and source integrity gate for R42."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRE_R41_HEAD = "92edf5d5c5025243e70e06e57baa9220668cc7b6"
REVIEWED_R41_HEAD = "f604062833ff4dc2756daa96235814983f98fbf2"
SHARED = "phase165_r52_r9_shared_math.py"
R41_PREFIX = "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/"
PINS = {
    SHARED: "8bb72fe9b3fe22c1917c51971b12338d62be9e9b",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and sha in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Accept only the reviewed R41 merge or its exact uncommitted patch."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Unpack R42 directly into the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R42 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_R41_HEAD:
        raise RuntimeError("Unreviewed remote HEAD; R42 refuses an unknown source")
    local = git("rev-parse", "HEAD")
    if local not in (PRE_R41_HEAD, REVIEWED_R41_HEAD):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    changed = tuple(git("diff", "--name-only").splitlines())
    expected = (SHARED,) if local == PRE_R41_HEAD else ()
    if changed != expected:
        raise RuntimeError("Unexpected tracked edits: " + repr(changed))
    if local == PRE_R41_HEAD:
        git("fetch", "-q", "origin", "develop")
    if git("rev-parse", REVIEWED_R41_HEAD) != REVIEWED_R41_HEAD:
        raise RuntimeError("Reviewed R41 merge is not locally available")
    if subprocess.run(
        ("git", "merge-base", "--is-ancestor", PRE_R41_HEAD, REVIEWED_R41_HEAD),
        cwd=ROOT, capture_output=True,
    ).returncode != 0:
        raise RuntimeError("Unreviewed R41 history")
    upstream = tuple(git("diff", "--name-only", PRE_R41_HEAD, REVIEWED_R41_HEAD).splitlines())
    if (len(upstream) != 16
            or SHARED not in upstream
            or any(p != SHARED and not p.startswith(R41_PREFIX) for p in upstream)):
        raise RuntimeError("R41 merge includes unexpected paths")
    for path, sha in PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob(file.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "local_head": local,
        "remote_head": REVIEWED_R41_HEAD,
        "source_guard": "PASS",
        "handoff_mode": "UNMERGED_R41_PATCH" if local == PRE_R41_HEAD else "MERGED_R41_CLEAN",
        "reviewed_merge_paths": len(upstream),
        "reviewed_source_pins": len(PINS),
        "production_files_changed": 0,
        "full_pytest": False,
    }

```

## `audit.py`（新規）

```python
"""Trace genuine R41 candidates versus the still-open EHP root in canonical search.

This is a read-only scoped search probe, NOT an HTTP request or a source proof.
Never substitute R40's manually reconstructed result for a canonical result.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import verify_checkout


def inspect_search_frontier() -> dict[str, object]:
    """Explain exactly which typed public branch is absent, without adding rules."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as EHP_ZERO_RULE, ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, expand_upper_delta_surjectivity,
        upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        RULE_NAME as ZERO_IMAGE_RULE,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        screened_general_law,
    )
    from proof import ProofRule, ProofStep

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    sources = screened_general_law(bridge)
    if len(sources) != 1:
        raise RuntimeError("Required cited general source is missing")
    citing_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == sources[0]
    )
    if len(citing_ids) != 1:
        raise RuntimeError("Missing unique cited registry link for Toda (5.9)")
    public = shared_expansion_provider(bridge, proof_target=root)
    zero_inputs = ehp_zero_inputs(root)
    if zero_inputs is None:
        raise RuntimeError("Invalid general EHP zero root contract")
    upper = zero_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None:
        raise RuntimeError("Upper EHP Delta general rule no longer applies")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None:
        raise RuntimeError("Hopf injectivity has invalid typed subgoals")
    zero_image = hopf_inputs[0]
    root_candidates = tuple(x for x in public(root) if x.rule.name == EHP_ZERO_RULE)
    public_upper = tuple(x for x in public(upper) if x.rule.name == UPPER_RULE)
    public_hopf = tuple(x for x in public(hopf) if x.rule.name == HOPF_RULE)
    public_zero_image = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    isolated_upper = expand_upper_delta_surjectivity(upper)
    if (len(root_candidates) != 1
            or root_candidates[0].subgoals != zero_inputs
            or len(isolated_upper) != 1
            or isolated_upper[0].subgoals != upper_inputs
            or public_upper
            or len(public_zero_image) != 1):
        raise RuntimeError("Observed EHP/R37/R41 provider frontier changed")
    presentation, generator_zero = public_zero_image[0].subgoals
    db = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if (not isinstance(db, ProofStep)
            or not verified_db_step(db, proof_target=root, bridge=bridge)
            or db.rule is not ProofRule.GIVEN):
        raise RuntimeError("Earlier DB prior admission contract changed")
    # The canonical recursive search currently admits a DB prior using its
    # top-level `goal`, which for a direct ImageZero probe is not a group.
    # This is checked as a boundary and is NOT papered over by a fake step.
    if admitted_db_step(presentation, proof_target=zero_image, bridge=bridge) is not None:
        raise RuntimeError("The direct zero-image DB admission scope changed")

    def scoped_root(candidate):
        if candidate == root:
            return root_candidates
        if candidate == upper:
            return public_upper
        return ()

    partial = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_ids[0],
        expansion_provider=scoped_root,
        lookup_mode="typed_reference",
    )
    if (partial.status is not ProofSearchStatus.SEARCH_FAILED
            or partial.proven_steps or partial.conclusion is not None
            or not any(x == upper for x in partial.open_goals)
            or not any(x == root for x in partial.open_goals)):
        raise RuntimeError("Scoped canonical search no longer has expected open upper Delta")

    def scoped_zero(candidate):
        return public_zero_image if candidate == zero_image else ()

    zero_probe = search_registered_partial_proof(
        n=7, k=5, goal=zero_image, bridge=bridge,
        citing_assertion_id=citing_ids[0],
        expansion_provider=scoped_zero,
        lookup_mode="typed_reference",
    )
    if (zero_probe.status is not ProofSearchStatus.SEARCH_FAILED
            or zero_probe.proven_steps or zero_probe.conclusion is not None):
        raise RuntimeError("Direct typed-zero probe unexpectedly bypassed its DB boundary")
    return {
        "screened_toda59_sources": len(sources),
        "public_root_ehp_candidates": len(root_candidates),
        "public_upper_delta_r37_candidates": len(public_upper),
        "isolated_upper_delta_r37_candidates": len(isolated_upper),
        "public_hopf_r5_candidates": len(public_hopf),
        "public_zero_image_r41_candidates": len(public_zero_image),
        "zero_image_typed_subgoals": len(public_zero_image[0].subgoals),
        "adopted_db_prior_verified_for_group_root": True,
        "direct_zero_image_goal_admits_db_prior": False,
        "canonical_root_scoped_search_status": partial.status.value,
        "canonical_root_scoped_verified_steps": len(partial.proven_steps),
        "canonical_root_scoped_open_upper_delta": True,
        "canonical_zero_image_scoped_status": zero_probe.status.value,
        "canonical_zero_image_scoped_verified_steps": len(zero_probe.proven_steps),
        "scoped_probe_not_full_web_search": True,
        "new_given_statements": 0,
        "new_math_rules": 0,
        "production_files_changed": 0,
        "upper_delta_surjectivity_proved": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observed = None if args.dry_run else inspect_search_frontier()
    gate = (
        "PASS_R42_REVIEWED_R41_SOURCE_PREFLIGHT" if args.dry_run else
        "PASS_R42_CANONICAL_SCOPED_SEARCH_UPPER_DELTA_PROVIDER_AND_DB_SCOPE_PENDING"
    )
    report = {"phase": "174-R3-R7-R42", "git_state": state,
              "observed": observed, "gate": gate}
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r42"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "canonical_frontier.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R42_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `run.ps1`（新規）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r42_canonical_search_frontier_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R42 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R42_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r42_canonical_search_frontier_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R42 canonical scoped-search audit failed' }
    $Groups = @(
        @{Name='R42_STATIC'; Path='phase174_r3_r7_r42_canonical_search_frontier_audit/tests/test_static.py'},
        @{Name='R42_GUARD'; Path='phase174_r3_r7_r42_canonical_search_frontier_audit/tests/test_guard.py'},
        @{Name='R42_CANONICAL_FRONTIER'; Path='phase174_r3_r7_r42_canonical_search_frontier_audit/tests/test_frontier.py'},
        @{Name='R41_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R40_RULE_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'},
        @{Name='R37_UPPER_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R42_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R42 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R42_RUN=PASS'
    Write-Output 'PHASE174_R3R7R42_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```

## `tests/test_static.py`（新規）

```python
"""R42 is purely observational and does not modify the public proof engine."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_python_sources_parse_without_ellipsis():
    for name in ("audit.py", "source_guard.py"):
        parsed = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(parsed)
        )


def test_no_implementation_installer_or_provider_override():
    assert not (ROOT / "install.py").exists()
    assert not (ROOT / "provider.py").exists()
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert "search_registered_partial_proof(" in source
    assert "scoped_probe_not_full_web_search" in source


def test_r42_audit_keeps_proof_completion_false():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"root_complete": False' in source
    assert '"web_http_checked": False' in source
    assert '"new_given_statements": 0' in source


def test_powershell_supports_dryrun_and_focused_tests():
    script = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "--dry-run" in script
    assert "pytest -q --import-mode=importlib" in script
    assert "FULL_PYTEST=False" in script

```

## `tests/test_guard.py`（新規）

```python
"""R42 Git hash guard does not make unknown edits look reviewed."""
from __future__ import annotations

from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import (
    PINS, PRE_R41_HEAD, REVIEWED_R41_HEAD, git_blob, matches_blob,
)


def test_hashes_and_reviewed_heads_are_pinned():
    assert len(PRE_R41_HEAD) == 40
    assert len(REVIEWED_R41_HEAD) == 40
    assert len(PINS) >= 8
    assert all(len(sha) == 40 for sha in PINS.values())


def test_git_blob_matches_actual_byte_length():
    assert git_blob(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    assert matches_blob(b"alpha\r\nbeta\r\n", git_blob(b"alpha\nbeta\n"))


def test_git_blob_refuses_corrupt_or_short_sha():
    correct = git_blob(b"alpha\nbeta\n")
    assert not matches_blob(b"alpha\nbetx\n", correct)
    assert not matches_blob(b"alpha\nbeta\n", correct[:-1])

```

## `tests/test_frontier.py`（新規）

```python
"""Real scoped canonical-search results, with both missing public bridges explicit."""
from __future__ import annotations

from phase174_r3_r7_r42_canonical_search_frontier_audit.audit import inspect_search_frontier
from phase174_r3_r7_r42_canonical_search_frontier_audit.source_guard import verify_checkout


def test_r42_source_guard_accepts_only_reviewed_r41_handoff():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["reviewed_merge_paths"] == 16
    assert state["production_files_changed"] == 0


def test_public_zero_image_candidate_exists_but_upper_delta_wiring_is_absent():
    result = inspect_search_frontier()
    assert result["screened_toda59_sources"] == 1
    assert result["public_root_ehp_candidates"] == 1
    assert result["public_zero_image_r41_candidates"] == 1
    assert result["isolated_upper_delta_r37_candidates"] == 1
    assert result["public_upper_delta_r37_candidates"] == 0


def test_real_canonical_scoped_search_fails_closed_without_forged_proof():
    result = inspect_search_frontier()
    assert result["adopted_db_prior_verified_for_group_root"] is True
    assert result["direct_zero_image_goal_admits_db_prior"] is False
    assert result["canonical_root_scoped_search_status"] == "search_failed"
    assert result["canonical_root_scoped_verified_steps"] == 0
    assert result["canonical_root_scoped_open_upper_delta"] is True
    assert result["canonical_zero_image_scoped_status"] == "search_failed"
    assert result["scoped_probe_not_full_web_search"] is True
    assert result["new_given_statements"] == 0
    assert result["root_complete"] is False

```

