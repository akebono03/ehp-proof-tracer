# Phase 174 R3-R7-R14R1 — 修正コード全文

## 変更一覧・追加位置

- `phase174_r3_r7_r14_public_annihilator_connection/audit.py`：`checked_source_blob` を関数全体で置換。他の関数・import変更なし。
- `phase174_r3_r7_r14_public_annihilator_connection/tests/test_audit.py`：`test_original_crlf_git_blob_pin_is_accepted_without_weakening_guard` と `test_source_guard_rejects_bare_cr_mixed_endings_and_invalid_sha` をファイル末尾に新規追加。import変更なし。
- `run.ps1` は変更なしで同梱。

以下の2つの Python ファイルは **import から末尾まで全文** を収録する。元の R14 Patch・数学的規則・公開経路接続の設計は変更しない。

## audit.py 全文

```python
"""Read-only source-first gate for the Toda (5.9) public bridge connection.

One audited general source, one typed specialization. No target-group GIVEN,
no dedicated narrative and no root completion claim are manufactured.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r14_public_annihilator_connection.patch import (
    EXPECTED_BLOB, TARGET, expected_patched_bytes, git_blob_sha,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R14"
BASE_HEAD = "9a8a3e953fe7d3bc7d8d989188aef15525b3a414"
R13_PREFIX = "phase174_r3_r7_r13_cited_annihilator_bridge/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase163_r4_r94_output/manifest.json": "8f6fc9bdcb28e7eb038d2a01cedcbbbcc2bc2457",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "unified_statement_registry.py": "be220ca9f95f20ef243ec295457912cd5ea99d0b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase174_r3_r7_r13_cited_annihilator_bridge/audit.py": "2470c4946cb646f7955514cf573b2906271f4e5a",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def checked_source_blob(value: bytes, expected: str) -> bool:
    """Accept pinned Git blobs with LF/CRLF checkout conversions only.

    The reviewed Toda TeX blob itself uses CRLF: hashing LF alone would
    reject its original bytes.  This check retains the original pinned SHA,
    rejects bare CR and mixed line endings, and never accepts edited content.
    """
    if len(expected) != 40 or any(c not in "0123456789abcdef" for c in expected):
        return False
    without_crlf = value.replace(b"\r\n", b"")
    if b"\r" in without_crlf:
        return False
    if b"\r\n" in value and b"\n" in without_crlf:
        return False
    normalized = value.replace(b"\r\n", b"\n")
    candidates = (
        value,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
    return any(git_blob_sha(candidate) == expected for candidate in candidates)


def reviewed_head_lineage(
    local: str,
    remote: str,
    successors: tuple[str, ...],
    changed: tuple[str, ...],
) -> str:
    if len(local) != 40 or local != remote:
        raise RuntimeError("Local/remote develop HEAD differs")
    if local == BASE_HEAD and not successors and not changed:
        return "REVIEWED_BASE"
    if (len(successors) == 1 and successors == (local,)
            and changed and all(path.startswith(R13_PREFIX) for path in changed)):
        return "REVIEWED_ONE_R13_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or non-R13 intervening commits")


def verify_git_and_sources(*, patched: bool, root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be directly under repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    changed_worktree = tuple(git("diff", "--name-only", cwd=root).splitlines())
    if patched and changed_worktree != (str(TARGET),):
        raise RuntimeError("Unexpected tracked modifications after patch")
    if not patched and changed_worktree:
        raise RuntimeError("Unexpected tracked modifications before patch")
    if local == BASE_HEAD:
        commits: tuple[str, ...] = ()
        changed_commit: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        commits = tuple(git("rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root).splitlines())
        changed_commit = tuple(git("diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root).splitlines())
    lineage = reviewed_head_lineage(local, remote, commits, changed_commit)
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not checked_source_blob(path.read_bytes(), expected):
            raise RuntimeError("Pinned source differs: " + relative)
    # Check exact output of the audited transform against the HEAD file. This
    # does not accept arbitrary edits merely because the Python AST still parses.
    original = subprocess.run(
        ("git", "show", "HEAD:" + str(TARGET).replace("\\", "/")),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if not checked_source_blob(original, EXPECTED_BLOB):
        raise RuntimeError("Reviewed public shared math source changed")
    actual = (root / TARGET).read_bytes()
    if patched:
        predicted = expected_patched_bytes(original)
        # Git may checkout CRLF; select worktree line style, never modify text.
        if b"\r\n" in actual and b"\r\n" not in predicted:
            predicted = predicted.replace(b"\n", b"\r\n")
        if actual != predicted:
            raise RuntimeError("Tracked shared math patch is not the exact reviewed transform")
    else:
        if not checked_source_blob(actual, EXPECTED_BLOB):
            raise RuntimeError("Tracked shared math source changed before patch")
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "tracked_changed": list(changed_worktree),
        "public_patch_applied": patched,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r13" / "cited_annihilator_bridge.json"


def validate_r13_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R13"
            or report.get("gate") != "PASS_ISOLATED_CITED_SOURCE_INFERENCE_PUBLIC_UNCHANGED"
            or report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("new_production_source_given") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False
            or report.get("full_pytest_run") is not False
            or report.get("source_order_position") != 9300):
        raise RuntimeError("Verified R13 complete audit is required")
    live = report.get("live") or {}
    expected = {
        "isolated_general_source_screened_count": 1,
        "isolated_n6_inference_count": 1,
        "public_general_source_given_count": 0,
        "public_n6_goal_proposal_count": 1,
        "isolated_n6_goal_proposal_count": 2,
    }
    for key, count in expected.items():
        if live.get(key) != count:
            raise RuntimeError("R13 observed count changed: " + key)
    if (live.get("isolated_n6_inference_has_cited_parent") is not True
            or live.get("public_n6_goal_proposal_rule_names") != ["equality symmetry"]
            or live.get("public_provider_unchanged") is not True
            or live.get("production_files_changed") is not False
            or live.get("root_proof_completed") is not False):
        raise RuntimeError("R13 proof ancestry or non-production contract changed")
    return {"gate": report["gate"], "isolated_ancestor_cited": True}


def inspect_public_source_and_proof() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        canonical_annihilator_instance, cited_annihilator_specialization_rule,
        RULE_NAME,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator,
    )
    from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
        reviewed_toda59_source_position,
    )
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule
    from unified_statement_registry import AssertionOrigin

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    fixed = []
    for link in screened.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or not isinstance(step.conclusion, CitedFamilyAnnihilator)):
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (step.rule is not ProofRule.GIVEN or step.premises
                or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion
                or reference.locator != "(5.9)"
                or reference.publication_position != reviewed_toda59_source_position()
                or step.inference_rule is None
                or step.inference_rule.literature_reference is None
                or step.inference_rule.literature_reference.locator != "(5.9)"):
            raise RuntimeError("Incorrect cited general source entered public bridge")
        fixed.append(step)
    if len(fixed) != 1:
        raise RuntimeError("Expected exactly one source-first screened general GIVEN")
    schema = fixed[0].conclusion
    instance = canonical_annihilator_instance(schema, 6)
    if instance is None or instance == goal:
        raise RuntimeError("Typed n=6 instance missing or equals target")
    provider = shared_expansion_provider(screened, proof_target=goal)
    options = tuple(provider(instance))
    cited = tuple(option for option in options if option.rule.name == RULE_NAME)
    if len(cited) != 1 or cited[0].subgoals != (schema,):
        raise RuntimeError("Public provider lacks source-bound n=6 inference")
    rule = cited_annihilator_specialization_rule(instance, schema)
    matches = find_inference_matches_for_rule(rule, (fixed[0],))
    if len(matches) != 1:
        raise RuntimeError("Verified source parent does not satisfy rule")
    inferred = derive_inference_proof_step(matches[0])
    if (inferred.rule is not ProofRule.INFERENCE
            or inferred.conclusion != instance
            or inferred.premises != (fixed[0],)):
        raise RuntimeError("Public n=6 inference lost cited parent")
    if any(link.step is not None and link.step.conclusion == goal
           and link.step.rule is ProofRule.GIVEN for link in screened.proof_links):
        raise RuntimeError("Target-group GIVEN shortcut detected")
    return {
        "public_general_source_givens": len(fixed),
        "public_n6_specialization_proposals": len(cited),
        "public_n6_all_proposals": len(options),
        "public_n6_cited_parent": True,
        "public_derived_n6_rule": inferred.inference_rule.name,
        "new_group_given": 0,
        "goal_complete_claimed": False,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r14" / "public_annihilator_connection.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(patched=not dry_run, root=root)
    prior_path = previous_report_path()
    if not prior_path.is_file():
        raise RuntimeError("Completed R13 audit report missing")
    prior = validate_r13_report(json.loads(prior_path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_public_source_and_proof()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "PUBLIC_SOURCE_FIRST_CONNECT",
        "git_state": git_state,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_direct_concrete_relation_given": 0,
        "new_general_source_given": 0 if dry_run else 1,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_PUBLIC_CITED_GENERAL_SOURCE_N6_INFERENCE_ROOT_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    out = output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R14_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "PUBLIC_SOURCE_GIVENS=" + str(live["public_general_source_givens"]))
        print(prefix + "PUBLIC_N6_SPECIALIZATION_PROPOSALS=" + str(live["public_n6_specialization_proposals"]))
        print(prefix + "PUBLIC_N6_ALL_PROPOSALS=" + str(live["public_n6_all_proposals"]))
        print(prefix + "PUBLIC_N6_HAS_CITED_PARENT=" + str(live["public_n6_cited_parent"]))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_DIRECT_CONCRETE_RELATION_GIVEN=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(out))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_audit.py 全文

```python
"""R13 evidence, source-lineage and source-first trust boundary tests."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r14_public_annihilator_connection.audit import (
    BASE_HEAD, R13_PREFIX, SOURCE_BLOBS, checked_source_blob,
    reviewed_head_lineage, validate_r13_report,
)


def sample_r13() -> dict:
    return {
        "phase": "174-R3-R7-R13",
        "gate": "PASS_ISOLATED_CITED_SOURCE_INFERENCE_PUBLIC_UNCHANGED",
        "source_order_position": 9300,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_production_source_given": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "live": {
            "isolated_general_source_screened_count": 1,
            "isolated_n6_inference_count": 1,
            "public_general_source_given_count": 0,
            "public_n6_goal_proposal_count": 1,
            "isolated_n6_goal_proposal_count": 2,
            "isolated_n6_inference_has_cited_parent": True,
            "public_n6_goal_proposal_rule_names": ["equality symmetry"],
            "public_provider_unchanged": True,
            "production_files_changed": False,
            "root_proof_completed": False,
        },
    }


def test_completed_r13_evidence_is_accepted_not_promoted_to_target_proof() -> None:
    prior = validate_r13_report(sample_r13())
    assert prior["isolated_ancestor_cited"] is True


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("new_production_source_given", 1),
    ("public_provider_changed", True),
    ("completion_claimed", True),
    ("full_pytest_run", True),
    ("source_order_position", 9400),
))
def test_r13_top_level_contract_fails_closed(field: str, value: object) -> None:
    report = sample_r13()
    report[field] = value
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


@pytest.mark.parametrize("field,value", (
    ("isolated_general_source_screened_count", 0),
    ("isolated_n6_inference_count", 0),
    ("public_general_source_given_count", 1),
    ("public_n6_goal_proposal_count", 2),
    ("isolated_n6_goal_proposal_count", 1),
    ("isolated_n6_inference_has_cited_parent", False),
    ("public_provider_unchanged", False),
    ("production_files_changed", True),
    ("root_proof_completed", True),
))
def test_r13_proof_evidence_cannot_be_overstated(field: str, value: object) -> None:
    report = deepcopy(sample_r13())
    report["live"][field] = value
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


def test_r13_symmetry_only_root_is_required() -> None:
    report = sample_r13()
    report["live"]["public_n6_goal_proposal_rule_names"] = ["cited source"]
    with pytest.raises(RuntimeError):
        validate_r13_report(report)


def test_strict_reviewed_head_or_one_r13_successor_only() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    successor = "f" * 40
    assert reviewed_head_lineage(
        successor, successor, (successor,), (R13_PREFIX + "registry.py",)
    ) == "REVIEWED_ONE_R13_ONLY_SUCCESSOR"
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, successor, (successor,), ("proof.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, successor, (successor, successor), (R13_PREFIX + "audit.py",))
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(successor, BASE_HEAD, (), ())


def test_fixed_pins_reject_truncated_sha_and_changed_content() -> None:
    example = b"abc\n"
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha
    sha = git_blob_sha(example)
    assert checked_source_blob(example, sha)
    assert checked_source_blob(b"abc\r\n", sha)
    assert not checked_source_blob(example, sha[:-1])
    assert not checked_source_blob(example + b"x", sha)
    assert all(len(v) == 40 for v in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 11


def test_original_crlf_git_blob_pin_is_accepted_without_weakening_guard() -> None:
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha

    original_crlf = b"Toda source\r\nSecond line\r\n"
    reviewed_crlf_sha = git_blob_sha(original_crlf)
    assert checked_source_blob(original_crlf, reviewed_crlf_sha)
    assert checked_source_blob(b"Toda source\nSecond line\n", reviewed_crlf_sha)
    assert not checked_source_blob(b"Toda source CHANGED\r\nSecond line\r\n", reviewed_crlf_sha)


def test_source_guard_rejects_bare_cr_mixed_endings_and_invalid_sha() -> None:
    from phase174_r3_r7_r14_public_annihilator_connection.patch import git_blob_sha

    reviewed = b"a\r\nb\r\n"
    sha = git_blob_sha(reviewed)
    assert not checked_source_blob(b"a\rb\r", sha)
    assert not checked_source_blob(b"a\r\nb\n", sha)
    assert not checked_source_blob(reviewed, sha[:-1])
    assert not checked_source_blob(reviewed, "f" * 40)
    assert SOURCE_BLOBS["sources/toda/Toda_05_2.tex"] == "579661138928499ba04a51327f686d9b971b5314"

```

## run.ps1 全文（変更なし）

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$BackupPath = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r14\phase165_r52_r9_shared_math.original.py'
$TargetPath = Join-Path $RepoRoot 'phase165_r52_r9_shared_math.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Preflight must run before modifying a single tracked source file.
    & python -B -m phase174_r3_r7_r14_public_annihilator_connection.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R14 source-first preflight failed: $LASTEXITCODE" }
    & python -B -m phase174_r3_r7_r14_public_annihilator_connection.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R14 guarded patch dry-run failed: $LASTEXITCODE" }

    # Each group runs in a separate process to avoid test_rule.py basename collisions.
    $Groups = @(
        @{ Name = 'R14'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_patch.py',
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_audit.py'
        ) },
        @{ Name = 'R13'; Paths = @(
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_registry.py',
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_audit.py'
        ) },
        @{ Name = 'R12'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_source.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_audit.py'
        ) },
        @{ Name = 'R11'; Paths = @(
            '.\phase174_r3_r7_r11_canonical_fixture_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R10'; Paths = @(
            '.\phase174_r3_r7_r10_cited_family_gap_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) },
        @{ Name = 'FAMILY_REGRESSION'; Paths = @(
            '.\phase169_r10d2_general_family_definition\tests\test_r10d2_general_family.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing focused test: $TestPath"
            }
        }
    }
    Write-Output 'PHASE174_R3R7R14_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R14_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "R14 $($Group.Name) focused pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R14_FOCUSED_PYTEST=PASS'
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R14_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r14_public_annihilator_connection.patch
        if ($LASTEXITCODE -ne 0) { throw "R14 guarded apply failed: $LASTEXITCODE" }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw "R14 public integration pytest failed: $LASTEXITCODE" }
        & python -B -m phase174_r3_r7_r14_public_annihilator_connection.audit
        if ($LASTEXITCODE -ne 0) { throw "R14 public source-first audit failed: $LASTEXITCODE" }
    }
    Write-Output '(END)'
}
catch {
    $TrackedAfterError = @(git diff --name-only)
    if ($PatchAttempted -and (Test-Path -LiteralPath $BackupPath) -and
        ($TrackedAfterError -contains 'phase165_r52_r9_shared_math.py')) {
        Copy-Item -LiteralPath $BackupPath -Destination $TargetPath -Force
        Write-Output 'PHASE174_R3R7R14_ROLLBACK=ORIGINAL_SOURCE_RESTORED'
    }
    throw
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}

```

## 完了条件

限定 pytest と Source Guard と DryRun・本監査の全 PASS。本監査の結果なしで完了宣言しない。
