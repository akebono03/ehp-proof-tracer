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
