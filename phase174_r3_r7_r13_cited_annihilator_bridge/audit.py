"""Phase 174 R3-R7-R13: read-only source registration and local proof-chain audit.

Unlike R12, the independently cited *general* Toda (5.9) law is put into an
isolated typed registry. Its n=6 instance is inferred, never made a GIVEN.
The public shared registry, search providers, and target-group proof are untouched.
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

from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
    ASSERTION_ID, REF_ID, build_isolated_toda59_annihilator_bridge,
    join_isolated_source_bridge, reviewed_toda59_source_position,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R13"
REVIEWED_HEAD = "9a8a3e953fe7d3bc7d8d989188aef15525b3a414"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase163_r4_r94_output/manifest.json": "8f6fc9bdcb28e7eb038d2a01cedcbbbcc2bc2457",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "unified_statement_registry.py": "be220ca9f95f20ef243ec295457912cd5ea99d0b",
    "phase163_r4_registry_bridge.py": "aa76059a51cb1f22d966dc9467b3e35919f51eae",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r12_toda59_annihilator_source/audit.py": "db27bcf483c1e7a05b85648eeb5bdb1c0a254ea0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(value: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(value)).encode("ascii") + b"\0" + value).hexdigest()


def matches_source_blob(value: bytes, expected: str) -> bool:
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    normalized = value.replace(b"\r\n", b"\n")
    return any(git_blob_sha(v) == expected for v in (
        value, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be a direct child of repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if local != remote or local != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD, or local/remote mismatch")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes must be reviewed")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes must be reviewed")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not matches_source_blob(file.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_paths": list(SOURCE_BLOBS),
        "untracked": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r12" / "toda59_annihilator.json"


def validate_r12_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R12"
            or report.get("gate") != "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"):
        raise RuntimeError("Completed R12 source-first audit is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False
            or report.get("full_pytest_run") is not False):
        raise RuntimeError("R12 proof trust boundary changed")
    live = report.get("live") or {}
    expected = {
        "independent_source_candidate_count": 1,
        "production_source_given_count": 0,
        "production_cited_specialization_count": 0,
        "new_verified_steps": 0,
    }
    for key, value in expected.items():
        if live.get(key) != value:
            raise RuntimeError("R12 previous evidence changed: " + key)
    if ((live.get("production_left_zero_proposals") or {}).get("proposal_count") != 1
            or live.get("production_left_zero_rule_names") != ["equality symmetry"]
            or live.get("source_as_proof_leaf_created") is not False
            or live.get("public_provider_unchanged") is not True):
        raise RuntimeError("R12 equality-symmetry-only boundary changed")
    return {"gate": report["gate"], "public_source_count": 0}


def inspect_isolated_registration_and_proof() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        canonical_annihilator_instance, cited_annihilator_specialization_rule,
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator,
    )
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule
    from unified_statement_registry import AssertionOrigin

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    public = build_shared_typed_bridge()
    public_screened = screen_independent_sources_for_derived_goal(public, goal=target)
    public_source_steps = tuple(
        link.step for link in public_screened.proof_links
        if isinstance(link.step, ProofStep)
        and isinstance(link.step.conclusion, CitedFamilyAnnihilator)
    )
    if public_source_steps:
        raise RuntimeError("Source already registered publicly: R13 assumptions changed")

    cited = build_isolated_toda59_annihilator_bridge()
    combined = join_isolated_source_bridge(public, cited)
    screened = screen_independent_sources_for_derived_goal(combined, goal=target)
    fixed_links = tuple(
        link for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, CitedFamilyAnnihilator)
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and screened.registry.assertion(link.assertion_id).content == link.step.conclusion
        and screened.registry.reference(
            screened.registry.assertion(link.assertion_id).reference_id
        ).publication_position == reviewed_toda59_source_position()
    )
    if len(fixed_links) != 1 or fixed_links[0].assertion_id != ASSERTION_ID:
        raise RuntimeError("Exactly one independently screened cited general law is required")
    cited_step = fixed_links[0].step
    schema = cited_step.conclusion
    instance = canonical_annihilator_instance(schema, 6)
    if instance is None:
        raise RuntimeError("Typed n=6 annihilator instance unavailable")
    if cited_step.conclusion == instance or cited_step.conclusion == target:
        raise RuntimeError("Source schema may not be a concrete target result")

    proposals = expand_cited_annihilator_specialization(instance, (schema,))
    if len(proposals) != 1 or proposals[0].subgoals != (schema,):
        raise RuntimeError("R12 cited specialization goal has changed")
    rule = cited_annihilator_specialization_rule(instance, schema)
    matches = find_inference_matches_for_rule(rule, (cited_step,))
    if len(matches) != 1:
        raise RuntimeError("Cited premise failed typed inference matching")
    inferred = derive_inference_proof_step(matches[0])
    if (inferred.rule is not ProofRule.INFERENCE
            or inferred.conclusion != instance
            or inferred.premises != (cited_step,)
            or inferred.inference_rule is not rule):
        raise RuntimeError("Provenance or inference ancestry was lost")

    original_provider = shared_expansion_provider(public_screened, proof_target=target)
    public_options = tuple(original_provider(instance))
    public_names = [getattr(x.rule, "name", "") for x in public_options]
    if public_names != ["equality symmetry"]:
        raise RuntimeError("Public equality symmetry frontier unexpectedly changed")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if isinstance(link.step, ProofStep) and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )

    def isolated_annihilator_provider(goal):
        return expand_cited_annihilator_specialization(goal, available)

    isolated_provider = shared_expansion_provider(
        screened, extra_providers=(isolated_annihilator_provider,), proof_target=target,
    )
    combined_options = tuple(isolated_provider(instance))
    names = [getattr(x.rule, "name", "") for x in combined_options]
    if (names.count(rule.name) != 1
            or len(combined_options) < len(public_options) + 1):
        raise RuntimeError("Isolated general source not exposed as a distinct typed GoalExpansion")
    return {
        "isolated_general_source_screened_count": len(fixed_links),
        "isolated_general_source_reference": REF_ID,
        "isolated_general_source_position": reviewed_toda59_source_position(),
        "printed_edition_independently_verified": False,
        "isolated_n6_inference_count": len(matches),
        "isolated_n6_inference_rule": inferred.inference_rule.name,
        "isolated_n6_inference_has_cited_parent": inferred.premises == (cited_step,),
        "isolated_source_type": type(schema).__name__,
        "isolated_n6_conclusion_type": type(instance).__name__,
        "public_general_source_given_count": len(public_source_steps),
        "public_n6_goal_proposal_count": len(public_options),
        "public_n6_goal_proposal_rule_names": public_names,
        "isolated_n6_goal_proposal_count": len(combined_options),
        "isolated_n6_goal_proposal_rule_names": names,
        "production_files_changed": False,
        "public_provider_unchanged": True,
        "root_proof_completed": False,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r13" / "cited_annihilator_bridge.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    manifest_position = reviewed_toda59_source_position(root / "phase163_r4_r94_output" / "manifest.json")
    if manifest_position <= 0:
        raise RuntimeError("Source order must be positive")
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        verify_toda59_annihilator_text,
    )
    source = verify_toda59_annihilator_text(root / "sources/toda/Toda_05_2.tex")
    path = previous_report_path()
    if not path.is_file():
        raise RuntimeError("Certified R12 JSON report is required")
    previous = validate_r12_report(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_isolated_registration_and_proof()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_REGISTRY_INFERENCE",
        "git_state": git_state,
        "source_review": source,
        "source_order_position": manifest_position,
        "prior_evidence": previous,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_production_source_given": 0,
        "new_isolated_general_source_given": 0 if dry_run else 1,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_CITED_SOURCE_INFERENCE_PUBLIC_UNCHANGED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R13_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "TODA59_SOURCE_ORDER_POSITION=" + str(report["source_order_position"]))
    if report["live"] is not None:
        live = report["live"]
        for name, key in (
            ("ISOLATED_CITED_SOURCE_GIVENS", "isolated_general_source_screened_count"),
            ("ISOLATED_N6_INFERENCE_MATCHES", "isolated_n6_inference_count"),
            ("PUBLIC_SOURCE_GIVENS", "public_general_source_given_count"),
            ("PUBLIC_LEFT_ZERO_PROPOSALS", "public_n6_goal_proposal_count"),
            ("ISOLATED_LEFT_ZERO_PROPOSALS", "isolated_n6_goal_proposal_count"),
        ):
            print(prefix + name + "=" + str(live[key]))
        print(prefix + "ISOLATED_N6_INFERENCE_HAS_CITED_PARENT=" + str(
            live["isolated_n6_inference_has_cited_parent"]
        ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "NEW_PRODUCTION_SOURCE_GIVEN=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
