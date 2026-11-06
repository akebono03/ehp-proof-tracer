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
