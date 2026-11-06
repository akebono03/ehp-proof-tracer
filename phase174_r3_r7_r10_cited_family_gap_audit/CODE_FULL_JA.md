# Phase 174 R3-R7-R10 — 追加コード全文

対象: `phase174_r3_r7_r10_cited_family_gap_audit/` をリポジトリルートに新規追加。既存クラス・関数・import・テストの変更はありません。
各 Python ファイルでは以下の表示が import を含む**ファイル全文**です。既存関数を抜粋・省略していません。
GitHub develop HEAD: `23979feec6685446a48d392fce3f2f1a55e85fe8`。
今回の限定 pytest: 新規監査テスト 20 件 PASS（独立実行）。Windows の全限定 pytest と live 監査は未確認です。

## `audit.py`

```python
"""Phase 174 R3-R7-R10: source-first audit of typed nu-family image obligations.

No production rule, public provider, assertion, GIVEN, or proof tree is added.
This diagnostic distinguishes source metadata from a verified proof step.
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
PHASE = "174-R3-R7-R10"
REVIEWED_HEAD = "23979feec6685446a48d392fce3f2f1a55e85fe8"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase174_r3_r7_r9_composition_associativity/audit.py": "5cfc1d0ad543e4006bfe3d3992ece047213511ef",
    "phase174_r3_r7_r8_composite_image_gap/audit.py": "87e8558e63c014e4e9ae9d16576e594752f2bf66",
    "phase163_r4_r94_output/manifest.json": "8f6fc9bdcb28e7eb038d2a01cedcbbbcc2bc2457",
}
TODA_59 = {
    "general_annihilator": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "generator_suspension": r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0",
    "zero_image_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data,
    ).hexdigest()


def source_blob_matches(data: bytes, expected_sha: str) -> bool:
    if len(expected_sha) != 40 or any(c not in "0123456789abcdef" for c in expected_sha):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(value) == expected_sha for value in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_pair(local: str, remote: str) -> bool:
    return local == remote == REVIEWED_HEAD


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("R10 package must be directly inside the repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = remote_line.split()[0] if remote_line else ""
    if not reviewed_head_pair(local, remote):
        raise RuntimeError("Unreviewed develop HEAD or local/remote mismatch")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Unreviewed staged changes")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Unreviewed tracked changes")
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not source_blob_matches(path.read_bytes(), expected):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_source_paths": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_transcription(root: Path = ROOT) -> dict[str, Any]:
    src = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = src.index(r"\begin{proposition}\label{prop:5.9}")
    end = src.index(r"\qed", start)
    proof_text = src[start:end]
    positions = {key: proof_text.find(clause) for key, clause in TODA_59.items()}
    if (any(n < 0 for n in positions.values())
            or list(positions.values()) != sorted(positions.values())):
        raise RuntimeError("Toda Proposition 5.9 transcription changed")
    return {
        "source": "Toda_05_2.tex: Proposition 5.9 proof; equation (5.9)",
        "clause_offsets": positions,
        "original_printed_edition_independently_verified": False,
        "transcription_is_not_a_proof_step": True,
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r9" / "composition_associativity.json"


def validate_r9_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R9"
            or report.get("gate") != "PASS_ISOLATED_ASSOCIATIVITY_CHILDREN_PENDING"):
        raise RuntimeError("R9 completed audit report is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("production_files_changed") is not False
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R9 proof trust boundary changed")
    live = report.get("live") or {}
    expected = {
        "isolated_rebracket_candidate_count": 1,
        "old_composite_candidate_count": 0,
        "right_associated_composite_candidate_count": 1,
    }
    for key, count in expected.items():
        if live.get(key) != count:
            raise RuntimeError("R9 isolated option count changed: " + key)
    for key, count in (
        ("public_right_associated_image_frontier", 1),
        ("public_left_associated_image_frontier", 0),
    ):
        if (live.get(key) or {}).get("proposal_count") != count:
            raise RuntimeError("R9 public candidate count changed: " + key)
    if (live.get("left_factor_root_rule") != "equality symmetry"
            or live.get("left_factor_symmetry_is_not_proof") is not True
            or live.get("public_provider_unchanged") is not True
            or live.get("new_verified_steps") != 0):
        raise RuntimeError("R9 symmetry or evidence boundary changed")
    return {
        "r9_gate": report["gate"],
        "left_image_public_options": 0,
        "right_image_public_options": 1,
        "left_zero_is_symmetry_only": True,
    }


def summarize_expression(value: object) -> dict[str, Any]:
    generator = getattr(value, "generator", None)
    return {
        "type": type(value).__name__,
        "name": getattr(value, "name", None),
        "dimension": getattr(value, "dimension", None),
        "source": getattr(value, "source", None),
        "target": getattr(value, "target", None),
        "symbol_family": getattr(generator, "family", None),
        "symbol_index": getattr(generator, "index", None),
        "repr": repr(value)[:1000],
    }


def inspect_live_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import component_image_obligations
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families, registered_stable_family_pair,
    )
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, expand_cited_stable_family, verified_source_positions,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        generator_image_associativity_inputs,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and screened.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    provider = shared_expansion_provider(screened, proof_target=target)

    prior = exact_prior_database_result(5, 5)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(10, 5)):
        raise RuntimeError("Typed prior group goal has changed")
    e = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    image_zero = ImageZeroStatement(e)
    r6 = cyclic_generator_zero_image_inputs(image_zero, prior)
    if r6 is None:
        raise RuntimeError("R6 typed generator goal is unavailable")
    original_generator_zero = r6[1]
    nu6 = HomotopyElement(
        "nu_6", dimension=6, source=9, target=6,
        generator=GeneratorSymbol("nu", 6),
    )
    eta9 = HomotopyElement(
        "eta_9", dimension=9, source=10, target=9,
        generator=GeneratorSymbol("eta", 9),
    )
    eta10 = HomotopyElement(
        "eta_10", dimension=10, source=11, target=10,
        generator=GeneratorSymbol("eta", 10),
    )
    original_left_composition = Composition(Composition(nu6, eta9), eta10)
    original_image = GeneratorImage(e, original_generator_zero.source_generator, original_left_composition)
    r9 = generator_image_associativity_inputs(original_image)
    if r9 is None or len(r9) != 1:
        raise RuntimeError("R9 right-associated image structure changed")
    right_image = r9[0]
    children = component_image_obligations(right_image)
    if children is None or len(children) != 2:
        raise RuntimeError("Existing composite rule no longer decomposes the right-associated goal")
    left_image, right_factor_image = children
    if left_image.source_generator != original_generator_zero.source_generator.left:
        raise RuntimeError("Left factor no longer agrees with registered generator")

    families = read_registered_stable_families()
    nu = tuple(f for f in families if f.family_id == 4)
    if len(nu) != 1 or nu[0].symbol_family != "ν" or nu[0].stem != 3:
        raise RuntimeError("Reviewed nu-family database identity differs")
    nu_family = nu[0]
    canonical_source = HomotopyElement(
        nu_family.name_at(5), 5, source=8, target=5,
        generator=GeneratorSymbol(nu_family.symbol_family, 5),
    )
    canonical_target = HomotopyElement(
        nu_family.name_at(6), 6, source=9, target=6,
        generator=GeneratorSymbol(nu_family.symbol_family, 6),
    )
    canonical_image = GeneratorImage(
        left_image.map, canonical_source, canonical_target,
    )
    family_pair = registered_stable_family_pair(
        canonical_image.source_generator, canonical_image.target_generator,
    )
    if family_pair is None or family_pair.family_id != nu_family.family_id:
        raise RuntimeError("Cited nu-family canonical pair did not match")
    family_sources = tuple(
        assertion for assertion in admitted
        if isinstance(assertion, CitedStableFamilyDefinition)
        and assertion.family_id == nu_family.family_id
    )
    screened_family = expand_cited_stable_family(canonical_image, admitted)
    reviewed_positions = dict(verified_source_positions())

    original_left_factor_zero = Relation(
        Composition(nu6, eta9), Zero(), RelationType.EQUALITY,
    )
    if any(is_exact_given(goal, admitted) for goal in (
        target, image_zero, original_generator_zero, original_image,
        right_image, left_image, canonical_image, original_left_factor_zero,
    )):
        raise RuntimeError("Target or uncited intermediate claim was admitted as GIVEN")

    return {
        "source_screening": "independent_source_screened",
        "registered_source_generator": summarize_expression(left_image.source_generator),
        "original_target_generator": summarize_expression(left_image.target_generator),
        "canonical_source_generator": summarize_expression(canonical_source),
        "canonical_target_generator": summarize_expression(canonical_target),
        "source_matches_canonical": left_image.source_generator == canonical_source,
        "target_matches_canonical": left_image.target_generator == canonical_target,
        "nu_family_id": nu_family.family_id,
        "nu_family_definition_position_verified": nu_family.family_id in reviewed_positions,
        "screened_nu_family_given_count": len(family_sources),
        "isolated_cited_family_candidate_count": len(screened_family),
        "public_original_left_image_frontier": summarize_proposals(provider, left_image, admitted),
        "public_canonical_nu_image_frontier": summarize_proposals(provider, canonical_image, admitted),
        "public_right_factor_image_frontier": summarize_proposals(provider, right_factor_image, admitted),
        "public_right_associated_image_frontier": summarize_proposals(provider, right_image, admitted),
        "left_factor_zero_fact_is_only_symmetry": True,
        "toda_general_annihilator_directly_admitted": False,
        "all_candidates_are_unproved_until_reconstructed": True,
        "public_provider_unchanged": True,
        "new_verified_steps": 0,
    }


def output_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return root / "EHPProofTracerAudit" / "phase174_r3_r7_r10" / "cited_family_gap.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_transcription(root)
    path = prior_report_path()
    if not path.is_file():
        raise RuntimeError("Certified R9 JSON report is required")
    prior = validate_r9_report(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_live_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_CITED_FAMILY_GAP",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_CITED_FAMILY_OBLIGATIONS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R10_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "R9_PUBLIC_LEFT_IMAGE_PROPOSALS=0")
    if report["live"] is not None:
        live = report["live"]
        for label, key in (
            ("PUBLIC_ORIGINAL_LEFT_IMAGE", "public_original_left_image_frontier"),
            ("PUBLIC_CANONICAL_NU_IMAGE", "public_canonical_nu_image_frontier"),
            ("PUBLIC_RIGHT_FACTOR_IMAGE", "public_right_factor_image_frontier"),
            ("PUBLIC_RIGHT_ASSOCIATED_IMAGE", "public_right_associated_image_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
        print(prefix + "ORIGINAL_SOURCE_CANONICAL=" + str(live["source_matches_canonical"]))
        print(prefix + "ORIGINAL_TARGET_CANONICAL=" + str(live["target_matches_canonical"]))
        print(prefix + "CITED_NU_DEFINITION_GIVENS=" + str(live["screened_nu_family_given_count"]))
        print(prefix + "ISOLATED_CITED_FAMILY_PROPOSALS=" + str(live["isolated_cited_family_candidate_count"]))
        print(prefix + "LEFT_FACTOR_SOURCE_LINK=UNPROVEN")
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `__init__.py`

```python
"""Read-only Phase 174 R3-R7-R10 source-first audit."""
```

## `tests/test_audit.py`

```python
"""R10 source-first lineage, evidence and no-proof-promotion contracts."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r10_cited_family_gap_audit.audit import (
    REVIEWED_HEAD,
    SOURCE_BLOBS,
    TODA_59,
    git_blob_sha,
    reviewed_head_pair,
    source_blob_matches,
    summarize_expression,
    validate_r9_report,
    verify_toda_transcription,
)


def sample_r9() -> dict:
    return {
        "phase": "174-R3-R7-R9",
        "gate": "PASS_ISOLATED_ASSOCIATIVITY_CHILDREN_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_rebracket_candidate_count": 1,
            "old_composite_candidate_count": 0,
            "right_associated_composite_candidate_count": 1,
            "public_right_associated_image_frontier": {"proposal_count": 1},
            "public_left_associated_image_frontier": {"proposal_count": 0},
            "left_factor_root_rule": "equality symmetry",
            "left_factor_symmetry_is_not_proof": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
        },
    }


def test_previous_r9_report_is_only_evidence_not_proof() -> None:
    data = validate_r9_report(sample_r9())
    assert data["left_image_public_options"] == 0
    assert data["right_image_public_options"] == 1
    assert data["left_zero_is_symmetry_only"] is True


@pytest.mark.parametrize("field,bad", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_production_inference_rules", 1),
    ("production_files_changed", True),
    ("public_provider_changed", True),
    ("completion_claimed", True),
))
def test_r9_rejects_modified_gate_or_trust_contract(field: str, bad: object) -> None:
    report = sample_r9()
    report[field] = bad
    with pytest.raises(RuntimeError):
        validate_r9_report(report)


@pytest.mark.parametrize("key,bad", (
    ("isolated_rebracket_candidate_count", 0),
    ("old_composite_candidate_count", 1),
    ("right_associated_composite_candidate_count", 0),
    ("left_factor_root_rule", "Toda source GIVEN"),
    ("left_factor_symmetry_is_not_proof", False),
    ("new_verified_steps", 1),
))
def test_r9_rejects_fabricated_completions(key: str, bad: object) -> None:
    report = sample_r9()
    report["live"][key] = bad
    with pytest.raises(RuntimeError):
        validate_r9_report(report)


def test_r9_rejects_wrong_public_goal_counts() -> None:
    report = sample_r9()
    report["live"]["public_left_associated_image_frontier"]["proposal_count"] = 1
    with pytest.raises(RuntimeError, match="public candidate count"):
        validate_r9_report(report)


def test_source_sha_requires_all_40_characters_and_content_match() -> None:
    source = b"line one\nline two\n"
    sha = git_blob_sha(source)
    assert source_blob_matches(source, sha)
    assert source_blob_matches(b"line one\r\nline two\r\n", sha)
    assert not source_blob_matches(source, sha[:-1])
    assert not source_blob_matches(source + b"changed", sha)
    assert all(len(value) == 40 for value in SOURCE_BLOBS.values())
    assert len(SOURCE_BLOBS) == 14


def test_head_must_equal_one_reviewed_develop_commit() -> None:
    assert reviewed_head_pair(REVIEWED_HEAD, REVIEWED_HEAD)
    assert not reviewed_head_pair(REVIEWED_HEAD, "f" * 40)
    assert not reviewed_head_pair("f" * 40, "f" * 40)


def test_source_claims_are_distinct_not_target_proof() -> None:
    assert "nu_n" in TODA_59["general_annihilator"]
    assert "nu_5" in TODA_59["generator_suspension"]
    assert TODA_59["zero_image_conclusion"] != TODA_59["general_annihilator"]


def test_toda_excerpt_requires_three_ordered_lines(tmp_path: Path) -> None:
    source = tmp_path / "sources" / "toda"
    source.mkdir(parents=True)
    (source / "Toda_05_2.tex").write_text(
        "prefix\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_59["general_annihilator"] + "\n"
        + TODA_59["generator_suspension"] + "\n"
        + TODA_59["zero_image_conclusion"] + "\n\\qed\n",
        encoding="utf-8",
    )
    result = verify_toda_transcription(tmp_path)
    assert result["transcription_is_not_a_proof_step"] is True
    (source / "Toda_05_2.tex").write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_59["zero_image_conclusion"] + "\n"
        + TODA_59["general_annihilator"] + "\n"
        + TODA_59["generator_suspension"] + "\n\\qed\n",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="transcription changed"):
        verify_toda_transcription(tmp_path)


def test_expression_descriptor_checks_full_generator_metadata() -> None:
    element = SimpleNamespace(
        name="ν₆", dimension=6, source=9, target=6,
        generator=SimpleNamespace(family="ν", index=6),
    )
    descriptor = summarize_expression(element)
    assert descriptor["name"] == "ν₆"
    assert descriptor["symbol_family"] == "ν"
    assert descriptor["symbol_index"] == 6


def test_source_only_audit_has_no_public_registration() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "validate_r9_report", "inspect_live_frontier"} <= functions
    assert not {"install", "patch", "register_given", "mutate_production"} & functions
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PriorPythonPath = $env:PYTHONPATH
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Independent pytest processes prevent identical test_audit.py module names
    # from colliding. Prepend mode keeps older file-vs-directory imports working.
    $Groups = @(
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
                throw "Missing focused test file: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R10_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R10_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R10 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R10_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r10_cited_family_gap_audit.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r10_cited_family_gap_audit.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R10 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PriorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    Pop-Location
}
```

## `README.md`

```markdown
# Phase 174 R3-R7-R10 — Cited Family Image Gap Audit

A read-only source-first audit of the two factor `GeneratorImage` obligations created by an already existing composition suspension rule. The audit checks the registered nu-family identity, canonical family naming and citation availability independently. It does not create mathematical evidence, attach a source as a direct goal GIVEN, register a production inference rule, or change the public provider.

## Usage

Unpack `R10.zip` directly into the root of the `akebono03/ehp-proof-tracer` develop checkout. It requires the completed R9 JSON audit record under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r9/composition_associativity.json`.

Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r10_cited_family_gap_audit\run.ps1 -DryRun`, then run without `-DryRun`. The script uses focused, separate pytest processes and intentionally does **not** execute the full test suite.

A successful full audit writes `cited_family_gap.json` under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r10/`. The reported proposal counts are **unverified backward candidates**, not completed proof trees.

GitHub develop HEAD is pinned to `23979feec6685446a48d392fce3f2f1a55e85fe8` and the reviewed source blob hashes. Any unexpected tracked change or HEAD mismatch fails closed.
```

## `AUDIT_PLAN_JA.md`

```markdown
# Phase 174 R3-R7-R10 監査計画

## 変更対象・追加位置

新規 `phase174_r3_r7_r10_cited_family_gap_audit/` のみ。

- `audit.py`：GitHub HEAD・ソース SHA と R9 JSON の検査、ν-family の正規型と既存 `GeneratorImage` の候補を検査する関数をファイル内に新規追加。
- `tests/test_audit.py`：監査契約テストを新規追加。既存テストの修正なし。
- `run.ps1`：同名 `test_audit.py` の import 衝突を避け、Phase 別に限定 pytest を実行。
- `README.md`：英語の実行説明。

既存本体・Proof Tree・Narrative・Web・共通5文書は変更しない。全体 pytest は実行しない。

## 数学的な対象

Toda Proposition 5.9 の採用転写では、ν_6 と η_9 の合成が零である一般関係を参照している。一方、R9 で得られた右結合の `GeneratorImage` が要求する左因子像には公開候補が0件である。出典、型付き系列定義、既存の候補、完成した ProofStep を混同しない。

R10 は左因子の `nu_6` と、引用済み ν-family の正規表示 `ν₆` を、表示名・GeneratorSymbol.family・次数・定義域と値域ごとに比較する。正規形に置き換えた検査対象について、`expand_cited_stable_family` と公開候補を別々に観測する。

これは元の Goal を勝手に正規形に置換する変更ではない。元の Goal の未解決状態を維持し、新たな GIVEN や未出典の具体的関係式を導入しない。

## 完了条件

1. 新規・関連限定 pytest と SHA Source Guard が PASS。
2. R9 の実行済み JSON の候補数・未完了契約を検証。
3. 引用済み ν-family 定義の存在、正規形と元の因子像との一致／不一致、候補数を JSON に記録。
4. 出典を使う場合も一般関係からの推論を必要とすることを明示。目標 `π₁₂⁷=0` の完成は宣言しない。

次段階 R11 は R10 の実測結果を確認してから、既存の正規化規則の再利用か、一般的な出典特殊化を最小限追加するか判断する。
```

## 実装後の変更一覧・完了条件・Phase 境界

- 変更: 上記新規ディレクトリのファイルのみ。本番の探索・GIVEN・Narrative・Web には変更なし。
- 実行する pytest: `run.ps1` の R10・R9〜R3・MATH_REGRESSION・FAMILY_REGRESSION の分割限定実行。全体テストは実行しない。
- 完了条件: SOURCE_GUARD=PASS、前工程 R9 JSON が PASS、ν-series の canonical pair・原表現の候補が記録され、監査 JSON が生成されること。
- 次 R11: R10 で実測された候補／識別子不一致／引用有無に基づき必要最小限の規則接続を判断する。結果の直接 GIVEN 登録なし。
