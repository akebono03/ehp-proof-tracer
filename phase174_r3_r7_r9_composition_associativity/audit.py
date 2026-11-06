"""R3-R7-R9: source-first audit of composition parenthesis mismatch.

No proof is created, and the public expansion provider is not modified.
The Toda annihilator is source text, not an authenticated proof premise.
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
PHASE = "174-R3-R7-R9"
REVIEWED_HEAD = "15785b921c15a19810b2b067715832ee20c61280"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r8_composite_image_gap/audit.py": "87e8558e63c014e4e9ae9d16576e594752f2bf66",
}
TODA_CLAUSES = {
    "general_annihilator": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "generator_suspension": r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0",
    "zero_image_conclusion": r"E\pi_{10}^5=0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepted_source_blob(data: bytes, expected_sha: str) -> bool:
    if len(expected_sha) != 40 or any(x not in "0123456789abcdef" for x in expected_sha):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(candidate) == expected_sha for candidate in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Expected repository root with this package as direct child")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if local != remote or local != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD: review current GitHub and tests")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    for relative, sha in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not accepted_source_blob(path.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_files": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    body = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = body.index(r"\begin{proposition}\label{prop:5.9}")
    end = body.index(r"\qed", start)
    section = body[start:end]
    positions = {name: section.find(text) for name, text in TODA_CLAUSES.items()}
    if any(offset < 0 for offset in positions.values()):
        raise RuntimeError("Toda Proposition 5.9 adopted transcription differs")
    if not (positions["general_annihilator"] < positions["generator_suspension"]
            < positions["zero_image_conclusion"]):
        raise RuntimeError("Toda source premise/conclusion sequence changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "reference": "Toda (5.9) in Proposition 5.9 proof",
        "positions": positions,
        "printed_edition_verified": False,
        "annihilator_specialization_is_unproved": True,
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r8" / "composite_image_gap.json"


def validate_r8_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R8"
            or report.get("gate") != "PASS_READ_ONLY_COMPOSITE_IMAGE_GAP_DIAGNOSIS"):
        raise RuntimeError("Certified R8 read-only audit is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R8 source and proof trust contract changed")
    live = report.get("live") or {}
    for key, expected in (
        ("public_composite_image_frontier", 0),
        ("public_left_factor_zero_frontier", 1),
        ("public_generator_zero_frontier", 0),
    ):
        if (live.get(key) or {}).get("proposal_count") != expected:
            raise RuntimeError("R8 observed frontier changed: " + key)
    if (live.get("existing_composite_image_rule_candidate_count") != 0
            or live.get("left_factor_rule_name") != "equality symmetry"
            or live.get("source_generator_type") != "Composition"
            or live.get("public_provider_unchanged") is not True
            or live.get("source_claim_promoted_to_given") is not False):
        raise RuntimeError("R8 structural gap or proof contract changed")
    return {
        "r8_gate": report["gate"],
        "previous_composite_options": 0,
        "previous_left_factor_rule_is_symmetry_only": True,
        "prior_completion_claimed": False,
    }


def inspect_rebracketing_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        composite_zero_generator_inputs,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        expand_generator_image_associativity, generator_image_associativity_inputs,
        right_associated_composition,
    )
    from phase174_r3_r7_source_first_audit.audit import is_exact_given, summarize_proposals
    from proof import ProofRule, Relation, RelationType

    zero_target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=zero_target)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=zero_target)
    prior = exact_prior_database_result(5, 5)
    if (not isinstance(prior, Relation) or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(10, 5)):
        raise RuntimeError("Prior finite cyclic presentation changed")
    e = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    image_zero = ImageZeroStatement(e)
    r6 = cyclic_generator_zero_image_inputs(image_zero, prior)
    if r6 is None:
        raise RuntimeError("R6 generator child not available")
    original_generator_zero = r6[1]
    nu6 = HomotopyElement("nu_6", dimension=6, source=9, target=6,
                          generator=GeneratorSymbol("nu", 6))
    eta9 = HomotopyElement("eta_9", dimension=9, source=10, target=9,
                           generator=GeneratorSymbol("eta", 9))
    eta10 = HomotopyElement("eta_10", dimension=10, source=11, target=10,
                            generator=GeneratorSymbol("eta", 10))
    left = Composition(Composition(nu6, eta9), eta10)
    original_image = GeneratorImage(e, original_generator_zero.source_generator, left)
    r7 = composite_zero_generator_inputs(original_generator_zero, original_image)
    if r7 is None or r7[0] != original_image or r7[1] != Relation(
        Composition(nu6, eta9), Zero(), RelationType.EQUALITY,
    ):
        raise RuntimeError("R7 composite/annihilator obligations changed")
    r9 = generator_image_associativity_inputs(original_image)
    proposals = expand_generator_image_associativity(original_image)
    if r9 is None or len(proposals) != 1 or proposals[0].subgoals != r9:
        raise RuntimeError("Generic rebracketing failed to offer one unproved Goal")
    right_image = r9[0]
    if right_image.target_generator != right_associated_composition(left):
        raise RuntimeError("Rebracketed target does not preserve composition factors")
    old_options = expand_composite_generator_image(original_image)
    new_options = expand_composite_generator_image(right_image)
    original_children = component_image_obligations(original_image)
    new_children = component_image_obligations(right_image)
    if old_options or original_children is not None:
        raise RuntimeError("R8 original unbracketed gap unexpectedly disappeared")
    if new_options and (len(new_options) != 1 or new_options[0].subgoals != new_children):
        raise RuntimeError("Existing right-associated rule changed")
    if any(is_exact_given(item, admitted) for item in (
        zero_target, image_zero, original_generator_zero, original_image,
        right_image, r7[1],
    )):
        raise RuntimeError("Source-screened goal was improperly admitted as GIVEN")
    left_proposals = tuple(provider(r7[1]))
    if len(left_proposals) != 1 or getattr(left_proposals[0].rule, "name", None) != "equality symmetry":
        raise RuntimeError("R8 left factor is no longer symmetry-only")
    return {
        "source_screening": "independent_source_screened",
        "source_generator_shape": repr(original_generator_zero.source_generator)[:1500],
        "left_associated_image": repr(left)[:1500],
        "right_associated_image": repr(right_image.target_generator)[:1500],
        "isolated_rebracket_candidate_count": len(proposals),
        "old_composite_candidate_count": len(old_options),
        "right_associated_composite_candidate_count": len(new_options),
        "right_associated_component_goals": (
            [{"type": type(c).__name__, "repr": repr(c)[:1500]} for c in new_children]
            if new_children is not None else []
        ),
        "source_generator_is_not_evidence": True,
        "public_right_associated_image_frontier": summarize_proposals(
            provider, right_image, admitted,
        ),
        "public_left_associated_image_frontier": summarize_proposals(
            provider, original_image, admitted,
        ),
        "left_factor_root_rule": getattr(left_proposals[0].rule, "name", None),
        "left_factor_symmetry_is_not_proof": True,
        "new_verified_steps": 0,
        "public_provider_unchanged": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r9" / "composition_associativity.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_source(root)
    previous = previous_report_path()
    if not previous.is_file():
        raise RuntimeError("Certified R8 report is required")
    prior = validate_r8_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_rebracketing_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_TYPED_ASSOCIATIVITY_AUDIT",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "public_provider_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_ASSOCIATIVITY_CHILDREN_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = report_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R9_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "SOURCE_ANNIHILATOR=VERIFIED_TRANSCRIPTION_NOT_GIVEN")
    if report["live"] is not None:
        live = report["live"]
        for label, key in (
            ("ISOLATED_REBRACKET", "isolated_rebracket_candidate_count"),
            ("ORIGINAL_COMPOSITE_RULE", "old_composite_candidate_count"),
            ("REASSOCIATED_COMPOSITE_RULE", "right_associated_composite_candidate_count"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]))
        for label, key in (
            ("PUBLIC_RIGHT_IMAGE", "public_right_associated_image_frontier"),
            ("PUBLIC_LEFT_IMAGE", "public_left_associated_image_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
        print(prefix + "LEFT_FACTOR_RULE=" + live["left_factor_root_rule"])
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
