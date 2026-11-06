"""Phase 174 R3-R7-R12: isolated Toda (5.9) source-schema preflight.

Reads the certified R11 report and checks typed public goal proposals.
There is no production integration, no generated proof leaf, and no group GIVEN.
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

from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    reviewed_toda59_annihilator_schema, verify_toda59_annihilator_text,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R12"
BASE_HEAD = "f260e157e69716a7021c02b49b6828359fba23d0"
REVIEWED_R11_HEAD = "162a72e42a7eadc16c62555de8239391bb5175cc"
ALLOWED_SUCCESSOR = "phase174_r3_r7_r11_canonical_fixture_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r11_canonical_fixture_audit/audit.py": "348f0c805de2bdda156cbc40543e88de0ec3c11e",
    "phase174_r3_r7_r11_canonical_fixture_audit/tests/test_audit.py": "5f3dba359af7bccacb2f004ff03e05bef7b12817",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def source_blob_matches(data: bytes, expected_sha: str) -> bool:
    if (len(expected_sha) != 40
            or any(c not in "0123456789abcdef" for c in expected_sha)):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(item) == expected_sha for item in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_lineage(
    local: str, remote: str, successors: tuple[str, ...],
    changed: tuple[str, ...],
) -> str:
    if local != remote or len(local) != 40:
        raise RuntimeError("Local/remote develop mismatch")
    if local == BASE_HEAD and not successors and not changed:
        return "REVIEWED_BASE"
    if (local == REVIEWED_R11_HEAD
            and successors == (REVIEWED_R11_HEAD,)
            and bool(changed)
            and all(path.startswith(ALLOWED_SUCCESSOR) for path in changed)):
        return "REVIEWED_R11_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or source changes")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("R12 package must be directly inside repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == BASE_HEAD:
        commits: tuple[str, ...] = ()
        changed: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        commits = tuple(git(
            "rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
        changed = tuple(git(
            "diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
    lineage = reviewed_head_lineage(local, remote, commits, changed)
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not source_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "checked_blob_count": len(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def prior_report_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return root / "EHPProofTracerAudit" / "phase174_r3_r7_r11" / "canonical_fixture_audit.json"


def validate_r11_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R11"
            or report.get("gate") != "PASS_READ_ONLY_CANONICAL_FIXTURE_GAP"):
        raise RuntimeError("Certified R11 full live audit report is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R11 proof trust contract changed")
    live = report.get("live") or {}
    if (live.get("canonical_full_composite_candidate_count") != 1
            or live.get("diagnostic_symbols_are_not_verified_aliases") is not True
            or live.get("canonical_source_from_explicit_database_goal") is not True
            or live.get("canonical_left_rule_names") != ["equality symmetry"]
            or live.get("transcription_not_promoted_to_proof") is not True
            or live.get("public_provider_unchanged") is not True
            or live.get("new_verified_steps") != 0):
        raise RuntimeError("R11 source or canonical-generator evidence changed")
    for key, expected in (
        ("public_canonical_full_image", 1),
        ("public_canonical_nu_image", 1),
        ("public_canonical_eta_square_image", 1),
        ("public_canonical_left_zero", 1),
    ):
        if (live.get(key) or {}).get("proposal_count") != expected:
            raise RuntimeError("R11 observed candidate count changed: " + key)
    return {"gate": report["gate"], "canonical_left_zero_only_symmetry": True}


def inspect_source_and_frontier() -> dict[str, Any]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        annihilator_specialization_inputs, canonical_annihilator_instance,
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    reviewed = reviewed_toda59_annihilator_schema()
    left = canonical_annihilator_instance(reviewed, 6)
    if (not isinstance(left, Relation)
            or left.relation_type is not RelationType.EQUALITY
            or not isinstance(left.lhs, Composition)
            or left.rhs != Zero()
            or left.lhs.left.generator.index != 6
            or left.lhs.right.generator.index != 9):
        raise RuntimeError("General source does not produce the correct typed n=6 instance")
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
    source_is_live = is_exact_given(reviewed, admitted)
    if source_is_live or is_exact_given(left, admitted) or is_exact_given(target, admitted):
        raise RuntimeError("Unreviewed annihilator or target assertion was admitted")
    isolated = expand_cited_annihilator_specialization(left, (reviewed,))
    without_source = expand_cited_annihilator_specialization(left, admitted)
    if (len(isolated) != 1 or isolated[0].subgoals != (reviewed,)
            or without_source or annihilator_specialization_inputs(left, ())):
        raise RuntimeError("Source-bound specialization did not preserve proof trust")
    public = summarize_proposals(provider, left, admitted)
    observed = tuple(provider(left))
    names = [str(getattr(option.rule, "name", "")) for option in observed]
    if public["proposal_count"] != 1 or names != ["equality symmetry"]:
        raise RuntimeError("R11 equality-symmetry-only gap changed")
    return {
        "source_screening": "adopted_toda_transcription_verified_but_not_admitted",
        "schema_type": type(reviewed).__name__,
        "schema_repr": repr(reviewed),
        "canonical_left_relation_repr": repr(left)[:1600],
        "independent_source_candidate_count": len(isolated),
        "production_source_given_count": int(source_is_live),
        "production_cited_specialization_count": len(without_source),
        "production_left_zero_proposals": public,
        "production_left_zero_rule_names": names,
        "source_as_proof_leaf_created": False,
        "new_verified_steps": 0,
        "public_provider_unchanged": True,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r12" / "toda59_annihilator.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    github = verify_git_and_sources(root)
    transcription = verify_toda59_annihilator_text(root / "sources/toda/Toda_05_2.tex")
    previous = prior_report_path()
    if not previous.is_file():
        raise RuntimeError("Certified R11 report is required")
    prior = validate_r11_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_source_and_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_CITED_ANNIHILATOR",
        "git_state": github,
        "source_review": transcription,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    out = output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R12_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "TODA59_GENERAL_ANNIHILATOR=VERIFIED_TRANSCRIPTION_NOT_GIVEN")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ISOLATED_SOURCE_SPECIALIZATION_PROPOSALS=" + str(
            live["independent_source_candidate_count"]
        ))
        print(prefix + "PUBLIC_SOURCE_GIVEN_COUNT=" + str(
            live["production_source_given_count"]
        ))
        print(prefix + "PUBLIC_CITED_SPECIALIZATION_PROPOSALS=" + str(
            live["production_cited_specialization_count"]
        ))
        print(prefix + "PUBLIC_LEFT_ZERO_PROPOSALS=" + str(
            live["production_left_zero_proposals"]["proposal_count"]
        ))
        print(prefix + "PUBLIC_LEFT_ZERO_RULES=" + ",".join(
            live["production_left_zero_rule_names"]
        ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(out))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
