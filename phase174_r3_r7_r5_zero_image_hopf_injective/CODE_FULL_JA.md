# Phase 174 R3-R7-R5R1 — 置換用コード全文

## 変更対象

1. `phase174_r3_r7_r5_zero_image_hopf_injective/audit.py` — `REVIEWED_R4_SUCCESSOR_HEAD` 定数追加、`reviewed_develop_head_pair` 新規関数（`verify_git_and_sources` の直前）、既存 `verify_git_and_sources` を変更。
2. `phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_audit.py` — import ブロック全文更新、テスト4関数追加（既存テストは維持）。
3. 新規 `phase174_r3_r7_r5_zero_image_hopf_injective/R5R1_GUARD_FIX_JA.md` — 検証記録。

`audit.py` とテストファイルの全体を以下に示します。import 部分を含み、省略はありません。`run.ps1` と `rule.py` は前回から変更せず、ZIP 内に全文を同梱しています。

## audit.py 全文

```python
"""Phase 174 R3-R7-R5: isolated generic image-zero/Hopf-injectivity audit.

No production module, group database, public provider or renderer is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R5"
REVIEWED_HEAD = "1f3a61d7d6cfc7854e56c4f5c372bf5c71e203df"
# Reviewed on 2026-11-06: exactly one successor commit added only
# phase174_r3_r7_r4_delta_surjectivity_audit/ package files. All nine
# pinned source blobs below are unchanged. No other successor is accepted.
REVIEWED_R4_SUCCESSOR_HEAD = "db9ef1cd1560744352bced43d3b4e1b95003edfb"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "map_property_rules.py": "4adeebc9dedb3daf210cd8755be811aca32f1e8b",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
TODA_CLAUSES = {
    "nonzero_group": r"\pi^{5}_{10}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8^2}",
    "suspension_of_generator_zero": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "zero_suspension_image": r"E\pi_{10}^5=0",
    "free_group_later_conclusion": r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(item) == expected for item in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_develop_head_pair(local: str, remote: str) -> bool:
    """Accept only identical, individually reviewed develop commits.

    The one reviewed successor to R5's original HEAD introduces the R4R1
    audit package only; pinned mathematical sources are checked separately.
    """
    return (
        local == remote
        and local in (REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD)
    )


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be directly under the repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if not reviewed_develop_head_pair(local, remote):
        raise RuntimeError("Unreviewed develop HEAD: source review is required")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    for path, expected in SOURCE_BLOBS.items():
        p = root / path
        if not p.is_file() or not accepted_source_blob(p.read_bytes(), expected):
            raise RuntimeError("Pinned source changed: " + path)
    return {
        "local_head": local,
        "remote_head": remote,
        "branch": "develop",
        "source_guard": "PASS",
        "reviewed_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    text = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = text.index(r"\begin{proposition}\label{prop:5.9}")
    end = text.index(r"\qed", start)
    section = text[start:end]
    offsets = {key: section.find(value) for key, value in TODA_CLAUSES.items()}
    if any(value < 0 for value in offsets.values()):
        raise RuntimeError("Toda Proposition 5.9 cited transcription changed")
    if not (offsets["nonzero_group"] < offsets["suspension_of_generator_zero"]
            < offsets["zero_suspension_image"]
            < offsets["free_group_later_conclusion"]):
        raise RuntimeError("Toda source premise/conclusion order changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "clauses": list(TODA_CLAUSES),
        "source_offsets": offsets,
        "printed_edition_independently_verified": False,
        "source_conclusion_is_not_given": True,
    }


def prior_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r4"
        / "delta_surjectivity_audit.json"
    )


def validate_r4_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R4"
            or report.get("gate") != "PASS_READ_ONLY_DELTA_SURJECTIVITY_GAP"):
        raise RuntimeError("R4 certified audit gate is absent")
    if (report.get("new_group_given") != 0
            or report.get("new_inference_rules") != 0
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R4 audit changed proof evidence or completion claims")
    source = report.get("source_review") or {}
    if source.get("pi10_5_nonzero_but_suspension_zero") is not True:
        raise RuntimeError("R4 source nonzero-group/zero-image distinction absent")
    live = report.get("live") or {}
    candidates = live.get("candidate_obligations") or {}
    expected = {
        "delta_surjectivity": 0,
        "eh_exactness": 1,
        "hd_exactness": 1,
        "hopf_injectivity": 1,
        "false_pi10_5_zero_shortcut": 0,
    }
    if any((candidates.get(name) or {}).get("proposal_count") != count
           for name, count in expected.items()):
        raise RuntimeError("R4 observed candidate frontier changed")
    neighbors = live.get("neighbor_groups") or {}
    for label in ("pi_10^5", "pi_9^5"):
        item = neighbors.get(label) or {}
        if (item.get("search_status") != "search_failed"
                or len(item.get("open_goals", [])) != 3):
            raise RuntimeError("R4 neighboring group search evidence changed")
    return {
        "gate": report["gate"],
        "observed_counts": expected,
        "neighbor_search_status": {
            label: neighbors[label]["search_status"]
            for label in ("pi_10^5", "pi_9^5")
        },
        "source_zero_map_is_not_proven_step": True,
    }


def inspect_screened_zero_image_frontier() -> dict[str, Any]:
    from homotopy_groups import (
        TodaHopfInvariantMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
        hopf_injectivity_from_zero_image_inputs,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(target_zero, admitted):
        raise RuntimeError("Forbidden direct zero-group GIVEN encountered")
    provider = shared_expansion_provider(screened, proof_target=target_zero)
    hopf_goal = MapInjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(11, 6), TodaPrimaryGroup(11, 11),
    ))
    inputs = hopf_injectivity_from_zero_image_inputs(hopf_goal)
    if inputs is None or not isinstance(inputs[0], ImageZeroStatement):
        raise RuntimeError("Generic image-zero antecedent is malformed")
    if is_exact_given(inputs[0], admitted):
        raise RuntimeError("Unscreened zero-image fact was inserted as GIVEN")
    options = expand_hopf_injective_from_zero_image(hopf_goal)
    if len(options) != 1 or options[0].subgoals != inputs:
        raise RuntimeError("Expected exactly one isolated generic alternative")
    old = expand_generic_ehp_hopf_goal(hopf_goal)
    if len(old) != 1:
        raise RuntimeError("Previous zero-group shortcut rule changed")
    return {
        "source_screening": "independent_source_screened",
        "screened_given_count": len(admitted),
        "isolated_hopf_injectivity_candidate_count": len(options),
        "isolated_subgoals": [
            {"type": type(x).__name__, "repr": repr(x)[:1000]} for x in inputs
        ],
        "production_hopf_injectivity_frontier": summarize_proposals(
            provider, hopf_goal, admitted,
        ),
        "production_zero_image_frontier": summarize_proposals(
            provider, inputs[0], admitted,
        ),
        "production_eh_exactness_frontier": summarize_proposals(
            provider, inputs[1], admitted,
        ),
        "old_zero_group_shortcut": [
            {"type": type(x).__name__, "repr": repr(x)[:1000]}
            for x in old[0].subgoals
        ],
        "isolated_candidate_is_not_proof": True,
        "new_verified_proof_steps": 0,
        "no_public_provider_wiring": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return (
        base / "EHPProofTracerAudit" / "phase174_r3_r7_r5"
        / "zero_image_hopf_injective.json"
    )


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_source(root)
    previous = prior_path()
    if not previous.is_file():
        raise RuntimeError("R3-R7-R4 certified audit JSON is required")
    prior = validate_r4_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_screened_zero_image_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_RULE",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_HOPF_INJECTIVITY_ZERO_IMAGE_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = report_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R5_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "R4_OBSERVED_DELTA_SURJECTIVITY_PROPOSALS=0")
    print(prefix + "SOURCE_PI105_NONZERO_BUT_E_IMAGE_ZERO=VERIFIED_TRANSCRIPTION")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_HOPF_INJECTIVITY_PROPOSALS=" + str(
            live["isolated_hopf_injectivity_candidate_count"]
        ))
        for name, key in (
            ("PRODUCTION_IMAGE_ZERO", "production_zero_image_frontier"),
            ("PRODUCTION_EH_EXACTNESS", "production_eh_exactness_frontier"),
            ("PRODUCTION_HOPF_INJECTIVITY", "production_hopf_injectivity_frontier"),
        ):
            print(prefix + name + "_PROPOSALS=" + str(
                live[key]["proposal_count"]
            ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_audit.py 全文

```python
"""Source and evidence contracts for the isolated zero-image audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r5_zero_image_hopf_injective.audit import (
    REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, SOURCE_BLOBS, TODA_CLAUSES,
    accepted_source_blob, blob_sha, reviewed_develop_head_pair,
    validate_r4_evidence, verify_git_and_sources,
)


def sample_r4() -> dict:
    return {
        "phase": "174-R3-R7-R4",
        "gate": "PASS_READ_ONLY_DELTA_SURJECTIVITY_GAP",
        "new_group_given": 0,
        "new_inference_rules": 0,
        "completion_claimed": False,
        "source_review": {"pi10_5_nonzero_but_suspension_zero": True},
        "live": {
            "candidate_obligations": {
                "delta_surjectivity": {"proposal_count": 0},
                "eh_exactness": {"proposal_count": 1},
                "hd_exactness": {"proposal_count": 1},
                "hopf_injectivity": {"proposal_count": 1},
                "false_pi10_5_zero_shortcut": {"proposal_count": 0},
            },
            "neighbor_groups": {
                "pi_10^5": {"search_status": "search_failed", "open_goals": [1, 2, 3]},
                "pi_9^5": {"search_status": "search_failed", "open_goals": [1, 2, 3]},
            },
        },
    }


def test_r4_certified_evidence_accepted_with_provenance_distinctions() -> None:
    checked = validate_r4_evidence(sample_r4())
    assert checked["observed_counts"]["delta_surjectivity"] == 0
    assert checked["source_zero_map_is_not_proven_step"]


def test_r4_dryrun_is_not_live_evidence() -> None:
    data = sample_r4()
    data["gate"] = "PASS_PREFLIGHT"
    with pytest.raises(RuntimeError, match="certified audit"):
        validate_r4_evidence(data)


def test_r4_new_given_and_completion_claim_fail_closed() -> None:
    data = sample_r4()
    data["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="changed proof evidence"):
        validate_r4_evidence(data)
    data = sample_r4()
    data["completion_claimed"] = True
    with pytest.raises(RuntimeError, match="changed proof evidence"):
        validate_r4_evidence(data)


@pytest.mark.parametrize("name,count", (
    ("delta_surjectivity", 1), ("eh_exactness", 0),
    ("false_pi10_5_zero_shortcut", 1),
))
def test_observed_prior_counts_must_not_be_fabricated(name: str, count: int) -> None:
    data = sample_r4()
    data["live"]["candidate_obligations"][name]["proposal_count"] = count
    with pytest.raises(RuntimeError, match="frontier changed"):
        validate_r4_evidence(data)


def test_neighbor_group_completion_cannot_be_assumed() -> None:
    data = sample_r4()
    data["live"]["neighbor_groups"]["pi_10^5"]["search_status"] = "complete"
    with pytest.raises(RuntimeError, match="neighboring group"):
        validate_r4_evidence(data)


def test_source_blob_accepts_crlf_but_rejects_different_content() -> None:
    a = b"source\nline\n"
    assert accepted_source_blob(a, blob_sha(a))
    assert accepted_source_blob(b"source\r\nline\r\n", blob_sha(a))
    assert not accepted_source_blob(b"source\nchanged\n", blob_sha(a))


def test_toda_source_separates_nonzero_group_and_zero_image() -> None:
    assert r"\mathbb Z_2" in TODA_CLAUSES["nonzero_group"]
    assert TODA_CLAUSES["zero_suspension_image"] == r"E\pi_{10}^5=0"
    assert len(SOURCE_BLOBS) == 9
    assert len(REVIEWED_HEAD) == 40


def test_source_audit_contains_no_install_or_direct_given() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    funcs = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_screened_zero_image_frontier" in funcs
    assert "verify_git_and_sources" in funcs
    assert "patch" not in funcs
    assert "install" not in funcs
    assert "create_given" not in funcs


@pytest.mark.parametrize("local,remote,accepted", (
    (REVIEWED_HEAD, REVIEWED_HEAD, True),
    (REVIEWED_R4_SUCCESSOR_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, True),
    (REVIEWED_HEAD, REVIEWED_R4_SUCCESSOR_HEAD, False),
    (REVIEWED_R4_SUCCESSOR_HEAD, REVIEWED_HEAD, False),
    ("0" * 40, "0" * 40, False),
    ("0" * 40, REVIEWED_R4_SUCCESSOR_HEAD, False),
))
def test_reviewed_develop_head_pair_only_allows_identical_audited_commits(
    local: str, remote: str, accepted: bool,
) -> None:
    assert reviewed_develop_head_pair(local, remote) is accepted


def test_reviewed_successor_is_exact_and_pinned_sources_stay_strict() -> None:
    assert REVIEWED_R4_SUCCESSOR_HEAD == "db9ef1cd1560744352bced43d3b4e1b95003edfb"
    assert len(SOURCE_BLOBS) == 9
    assert "sources/toda/Toda_05_2.tex" in SOURCE_BLOBS
    assert "phase165_r52_r9_shared_math.py" in SOURCE_BLOBS
    assert "map_property_rules.py" in SOURCE_BLOBS


def test_verify_git_and_sources_accepts_reviewed_successor_with_pinned_blobs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r5_zero_image_hopf_injective.audit as audit_module

    for relative_path in SOURCE_BLOBS:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"fixture reviewed source")

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        commands = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): REVIEWED_R4_SUCCESSOR_HEAD,
            ("ls-remote", "origin", "refs/heads/develop"):
                REVIEWED_R4_SUCCESSOR_HEAD + "\trefs/heads/develop",
            ("diff", "--cached", "--name-only"): "",
            ("diff", "--name-only"): "",
            ("status", "--porcelain=v1", "--untracked-files=normal"): "",
        }
        if args not in commands:
            raise AssertionError("Unexpected Git invocation: " + repr(args))
        return commands[args]

    monkeypatch.setattr(audit_module, "git", fake_git)
    monkeypatch.setattr(audit_module, "accepted_source_blob", lambda data, expected: data == b"fixture reviewed source")
    result = verify_git_and_sources(tmp_path)
    assert result["local_head"] == REVIEWED_R4_SUCCESSOR_HEAD
    assert result["remote_head"] == REVIEWED_R4_SUCCESSOR_HEAD
    assert result["source_guard"] == "PASS"
    assert len(result["reviewed_files"]) == 9


def test_verify_git_and_sources_rejects_modified_pinned_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    import phase174_r3_r7_r5_zero_image_hopf_injective.audit as audit_module

    for relative_path in SOURCE_BLOBS:
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"modified source")

    def fake_git(*args: str, cwd: Path = tmp_path) -> str:
        commands = {
            ("rev-parse", "--show-toplevel"): str(tmp_path),
            ("branch", "--show-current"): "develop",
            ("rev-parse", "HEAD"): REVIEWED_R4_SUCCESSOR_HEAD,
            ("ls-remote", "origin", "refs/heads/develop"):
                REVIEWED_R4_SUCCESSOR_HEAD + "\trefs/heads/develop",
            ("diff", "--cached", "--name-only"): "",
            ("diff", "--name-only"): "",
        }
        return commands[args]

    monkeypatch.setattr(audit_module, "git", fake_git)
    with pytest.raises(RuntimeError, match="Pinned source changed"):
        verify_git_and_sources(tmp_path)

```

## run.ps1 全文（変更なし）

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each group gets a separate Python process. Several previous Phase
    # packages contain test_audit.py or test_rule.py with the same basename.
    # Prepend mode is required for old module/directory naming collisions.
    $R5Tests = @(
        '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
        '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
    )
    $R4Tests = @(
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
        '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
    )
    $R3Tests = @(
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
        '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
    )
    $MathTests = @(
        '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
        '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
        '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
    )
    $Groups = @(
        @{ Name = 'R5'; Paths = $R5Tests },
        @{ Name = 'R4'; Paths = $R4Tests },
        @{ Name = 'R3'; Paths = $R3Tests },
        @{ Name = 'MATH_REGRESSION'; Paths = $MathTests }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Focused test file missing: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R5_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R5_PYTEST_GROUP=$($Group.Name)"
        $TestPaths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @TestPaths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R5 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R5_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r5_zero_image_hopf_injective.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r5_zero_image_hopf_injective.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R5 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}

```

## rule.py 全文（変更なし）

```python
"""Generic EHP: im(E)=0 and exactness at B imply ker(H)=0.

The mathematical inference is independent of any specific n, k or generator.
No source fact, ProofStep, GIVEN or production search registration is created.
The zero-image premise is intentionally left as a separate proof obligation.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact E-H window and zero suspension image imply Hopf injectivity"


def hopf_injectivity_from_zero_image_inputs(
    goal: object,
) -> tuple[ImageZeroStatement, TodaProp42ExactnessStatement] | None:
    """Derive a type-checked, dimensionally valid pair of independent goals."""
    if not isinstance(goal, MapInjective):
        return None
    hopf = goal.map
    if not isinstance(hopf, TodaHopfInvariantMap):
        return None
    middle = hopf.source_group
    target = hopf.target_group
    if not isinstance(middle, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q = middle.group_dimension
    sphere = middle.sphere_dimension
    if (type(q) is not int or type(sphere) is not int
            or sphere < 2 or q < sphere
            or target != TodaPrimaryGroup(q, 2 * sphere - 1)):
        return None
    preceding = TodaPrimaryGroup(q - 1, sphere - 1)
    e = TodaSuspensionMap(preceding, middle)
    exactness = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=preceding,
        middle_term=middle,
        target_term=target,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(exactness) != (sphere - 1, q, "e_h"):
        return None
    return ImageZeroStatement(e), exactness


def hopf_injective_from_zero_image_rule(goal: MapInjective) -> InferenceRule:
    """Construct a general rule requiring two independently proved premises."""
    required = hopf_injectivity_from_zero_image_inputs(goal)
    if required is None:
        raise ValueError("invalid typed EHP Hopf-injectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and hopf_injectivity_from_zero_image_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "By EHP exactness, im(E)=ker(H). If the suspension image "
            "is independently proved zero, then ker(H)=0, so H is "
            "injective. A zero preceding group is not required."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=ImageZeroStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaProp42ExactnessStatement,
                statement_pattern=required[1],
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_hopf_injective_from_zero_image(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Return one unproved backward branch; do not create proof leaves."""
    required = hopf_injectivity_from_zero_image_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=hopf_injective_from_zero_image_rule(goal),
        subgoals=required,
    ),)

```
