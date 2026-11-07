"""R18 source-first review of a noncircular Delta-surjectivity branch.

The common public search remains unchanged. An isolated GoalExpansion
records obligations, not a proof or a root completion.
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
PHASE = "174-R3-R7-R18"
PRE_R17_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
REVIEWED_HEAD = "4d59298949c14dc02d8bfb6ec28da4624ed980da"
R18_MERGED_HEAD = "7ecd12f28b5943b105ac6a953be69b44eae4a26e"
R18_AUDIT_PATH = "phase174_r3_r7_r18_delta_image_surjectivity/audit.py"
HANDOFF_TRACKED = (
    "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
    "web_group_proof_common.py",
)
PINS = {
    "phase165_r52_r9_shared_math.py": "d42bb7420cf58f4dd466511d6498c66d9917b29c",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "map_facts.py": "86fbf404783e15d344595bf54df5a9a8bafc35fc",
    "phase164_r8_proofstep_factory.py": "d314def19ab4e3e77f57af0ca9da18d7837efdda",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r57_r19_delta_image_backward.py": "c5b3447258f41e15219ead8daeeb17cbb5605b6d",
    "toda_delta_image_rules.py": "f0ccdc2d3b8545986caaaba51a213c86cc08b781",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py": "0a9a3732688509fe4b75d35e26854f18bcdc9aa9",
    "web_group_proof_common.py": "cb52a4dc2b4c24594f2acf2d76dc6c68ec0947ab",
    "phase174_r3_r7_r17r2_windows_git_path_guard_fix/patch.py": "652d76bec07271471fcb568f67e3f2826c4b96d3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data,
    ).hexdigest()


def matches_git_blob(data: bytes, expected: str) -> bool:
    """Support uniform Windows CRLF checkout; reject partial/mixed EOLs."""
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    remainder = data.replace(b"\r\n", b"")
    if b"\r" in remainder or (b"\r\n" in data and b"\n" in remainder):
        return False
    normalized = data.replace(b"\r\n", b"\n")
    return any(git_blob_sha(x) == expected for x in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def matches_reviewed_checkout(data: bytes, expected: str, git_stored: bytes) -> bool:
    """Accept only the pinned Git blob or exact uniform EOL checkout variants.

    Git may store mixed LF/CRLF in a reviewed file. A clean checkout can
    preserve those exact bytes or convert all line endings consistently.
    No character other than CR or LF may differ from the pinned Git object.
    """
    if git_blob_sha(git_stored) != expected:
        return False
    normalized = git_stored.replace(b"\r\n", b"\n")
    return data in (
        git_stored,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )

def checked_lineage(local: str, remote: str, changes: tuple[str, ...],
                    committed: tuple[str, ...]) -> str:
    """Require an exactly reviewed R17 history and R18 handoff, if merged."""
    allowed_committed = set(HANDOFF_TRACKED)
    if (not set(HANDOFF_TRACKED).issubset(set(committed))
            or any(path not in allowed_committed and not path.startswith(
                ("phase174_r3_r7_r17_typed_map_open_goal/",
                 "phase174_r3_r7_r17r1_historical_test_contract/",
                 "phase174_r3_r7_r17r2_windows_git_path_guard_fix/"),
            ) for path in committed)):
        raise RuntimeError("Remote R17 merge lineage has unexpected files")
    if remote == REVIEWED_HEAD:
        if local == REVIEWED_HEAD and changes == ():
            return "R17_MERGED_CLEAN"
        if local == PRE_R17_HEAD and tuple(sorted(changes)) == HANDOFF_TRACKED:
            return "R17_PATCHES_UNCOMMITTED_MATCH_MERGED_REMOTE"
        raise RuntimeError("Unreviewed R17 worktree state: " + repr(changes))
    if remote != R18_MERGED_HEAD:
        raise RuntimeError("Unreviewed remote develop HEAD; no checkout/reset")
    if local == REVIEWED_HEAD and changes == ():
        return "R18_MERGED_REMOTE_R17_LOCAL_CLEAN"
    if local == R18_MERGED_HEAD and changes == ():
        return "R18_MERGED_CLEAN"
    if local == R18_MERGED_HEAD and changes == (R18_AUDIT_PATH,):
        return "R18_MERGED_REVIEWED_GUARD_FIX"
    raise RuntimeError("Unreviewed R18 worktree changes: " + repr(changes))



def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    repo = Path(git("rev-parse", "--show-toplevel", root=root)).resolve()
    if repo != root.resolve():
        raise RuntimeError("Extract the R18 folder directly under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R18 requires develop branch")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require separate audit")
    changes = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R17_HEAD, REVIEWED_HEAD, root=root)
    commits = tuple(git("rev-list", PRE_R17_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines())
    if len(commits) != 1:
        raise RuntimeError("Expected one reviewed R17 merge commit")
    changed_in_review = tuple(git(
        "diff", "--name-only", PRE_R17_HEAD, REVIEWED_HEAD, root=root,
    ).splitlines())
    lineage = checked_lineage(local, remote, changes, changed_in_review)
    if remote == R18_MERGED_HEAD:
        git_bytes("merge-base", "--is-ancestor", REVIEWED_HEAD, R18_MERGED_HEAD, root=root)
        r18_commits = git("rev-list", REVIEWED_HEAD + ".." + R18_MERGED_HEAD, root=root).splitlines()
        r18_paths = git("diff", "--name-only", REVIEWED_HEAD, R18_MERGED_HEAD, root=root).splitlines()
        if (len(r18_commits) != 1 or not r18_paths
                or any(not p.startswith("phase174_r3_r7_r18_delta_image_surjectivity/")
                       for p in r18_paths)):
            raise RuntimeError("Unreviewed R18 merge lineage")
    for relative, blob in PINS.items():
        file = root / relative
        git_stored = git_bytes("show", "HEAD:" + relative, root=root)
        if (not file.is_file()
                or not matches_reviewed_checkout(file.read_bytes(), blob, git_stored)):
            raise RuntimeError("R18 Source Guard mismatch: " + relative)
    for relative in HANDOFF_TRACKED:
        reviewed = git_bytes("show", REVIEWED_HEAD + ":" + relative, root=root)
        if git_blob_sha(reviewed) != PINS[relative]:
            raise RuntimeError("Reviewed GitHub R17 target mismatch: " + relative)
    return {
        "local_head": local, "remote_head": remote,
        "lineage": lineage, "source_guard": "PASS",
        "pinned_files": len(PINS), "tracked_changes": list(changes),
    }



def validate_prior_r17() -> dict[str, Any]:
    """Validate prior evidence or recheck the live public proof boundary.

    Local audit JSON is per-Windows-profile state, not a mathematical axiom.
    Absence triggers fresh R17 public-search verification, never fabricated
    evidence or a silent transfer of another account's audit report.
    Present but invalid evidence is rejected instead of being bypassed.
    Git source pins and the corrected historical-test source are checked
    separately by verify_git_and_sources() before this function is called.
    """
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit"
    required = (
        ("phase174_r3_r7_r17/typed_map_public_audit.json",
         "174-R3-R7-R17", "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
        ("phase174_r3_r7_r17r1/historical_contract_audit.json",
         "174-R3-R7-R17R1", "PASS_HISTORICAL_TEST_CONTRACT_CORRECTED_R17_PUBLIC_UNCHANGED"),
    )
    results: dict[str, Any] = {}
    missing: list[tuple[str, str]] = []
    for relative, phase, gate in required:
        path = base / relative
        if not path.is_file():
            missing.append((relative, phase))
            continue
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if (obj.get("phase") != phase or obj.get("gate") != gate
                or obj.get("new_group_given") != 0
                or obj.get("full_pytest_run") is not False):
            raise RuntimeError("Prior R17 evidence inconsistent: " + relative)
        results[phase] = gate

    if missing:
        from phase174_r3_r7_r17_typed_map_open_goal.audit import (
            inspect_public_map_display,
        )
        live = inspect_public_map_display()
        expected_delta = r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}"
        if (live.get("public_root_candidates") != 1
                or live.get("public_delta_surjectivity_candidates") != 0
                or live.get("generic_isomorphism_depends_on_surjectivity") is not True
                or live.get("direct_given_for_goal_or_delta") is not False
                or live.get("delta_latex") != expected_delta
                or live.get("search_status") != "search_failed"
                or live.get("proven_steps") != 0
                or live.get("completion_claimed") is not False):
            raise RuntimeError("Live R17 proof boundary cannot replace missing local evidence")
        for relative, phase in missing:
            if phase == "174-R3-R7-R17":
                results[phase] = "LIVE_PUBLIC_BOUNDARY_REVALIDATED_NO_LOCAL_REPORT"
            else:
                results[phase] = "CORRECTED_TEST_SOURCE_PINNED_NO_LOCAL_REPORT"
        results["recovery"] = {
            "mode": "LIVE_REVALIDATED_NO_SYNTHETIC_REPORT",
            "missing_local_reports": [relative for relative, _ in missing],
            "public_root_candidates": live["public_root_candidates"],
            "delta_surjectivity_candidates": live["public_delta_surjectivity_candidates"],
            "verified_steps": live["proven_steps"],
            "corrected_historical_test_pinned_by_source_guard": True,
        }
    return results


def inspect_live_frontier() -> dict[str, Any]:
    """Compare isolated inference and public source-screened proof frontier."""
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, admitted_db_step,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r18_delta_image_surjectivity.rule import (
        RULE_NAME, delta_surjectivity_image_inputs,
        expand_delta_surjectivity_from_full_free_cyclic_image,
    )
    from proof import ProofRule, ProofStep, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    children = ehp_zero_inputs(target)
    if children is None or len(children) != 4:
        raise RuntimeError("R16 EHP root prerequisites changed")
    delta = children[0]
    if not isinstance(delta, MapSurjective):
        raise RuntimeError("Root does not require typed Delta surjectivity")
    codomain = delta.map.target_group
    n = codomain.sphere_dimension
    k = codomain.group_dimension - n
    prior = exact_prior_database_result(n, k)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != codomain
            or not isinstance(prior.rhs, FreeCyclicGroup)):
        raise RuntimeError("Expected concrete earlier free-cyclic codomain goal unavailable")
    required = delta_surjectivity_image_inputs(delta, prior)
    isolated = expand_delta_surjectivity_from_full_free_cyclic_image(delta, prior)
    if required is None or len(isolated) != 1 or isolated[0].subgoals != required:
        raise RuntimeError("General image/codomain Delta candidate not valid")

    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    provider = shared_expansion_provider(screened, proof_target=target)
    root_candidates = tuple(provider(target))
    public_delta = tuple(provider(delta))
    group_candidates = tuple(provider(prior))
    image_candidates = tuple(provider(required[1]))
    signed = tuple(
        link.step for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, TodaDeltaImageUpToSignStatement)
        and link.step.conclusion.map == delta.map
        and link.step.conclusion.positive_value == prior.rhs.generator
    )
    if len(root_candidates) != 1 or public_delta:
        raise RuntimeError("R17 public root/Delta frontier baseline changed")
    if (any(link.step is not None and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion in (target, delta, required[1])
            for link in screened.proof_links)):
        raise RuntimeError("Unapproved direct GIVEN for target or Delta")
    db_prior = admitted_db_step(prior, proof_target=target, bridge=screened)
    result = search_group_from_registered_goal(n=7, k=5, bridge=bridge, goal=target)
    if result.conclusion is not None or any(step.conclusion == target for step in result.proven_steps):
        raise RuntimeError("Unverified completion of pi12^7 was detected")
    return {
        "source_screening": "independent_source_screened",
        "public_root_proposals": len(root_candidates),
        "public_delta_surjectivity_proposals": len(public_delta),
        "isolated_delta_surjectivity_proposals": len(isolated),
        "isolated_rule_name": RULE_NAME,
        "codomain_n": n, "codomain_k": k,
        "codomain_relation_is_goal_not_proof": True,
        "codomain_prior_db_admissible": db_prior is not None,
        "image_zero_or_free_cyclic_is_not_given": True,
        "public_codomain_presentation_proposals": len(group_candidates),
        "public_delta_free_cyclic_image_proposals": len(image_candidates),
        "matching_cited_signed_delta_witness_count": len(signed),
        "generic_isomorphism_cycle_shortcut_used": False,
        "search_status": result.status.value,
        "search_open_goals": len(result.open_goals),
        "search_verified_steps": len(result.proven_steps),
        "new_proof_steps_created": 0,
        "new_group_given": 0,
        "completion_claimed": False,
        "production_provider_changed": False,
    }


def report_path(dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    directory = base / "EHPProofTracerAudit" / "phase174_r3_r7_r18"
    return directory / ("delta_image_preflight.json" if dry_run else "delta_image_frontier.json")


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    previous = validate_prior_r17()
    live = None if dry_run else inspect_live_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY",
        "git_state": state, "prior_evidence": previous, "live": live,
        "new_group_given": 0, "new_math_rules_in_production": 0,
        "new_isolated_inference_rules": 1,
        "production_files_modified": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": ("PASS_PREFLIGHT" if dry_run else
                 "PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    output = report_path(args.dry_run)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R18_"
    state = report["git_state"]
    print(prefix + "LOCAL_HEAD=" + state["local_head"])
    print(prefix + "REMOTE_HEAD=" + state["remote_head"])
    print(prefix + "LINEAGE=" + state["lineage"])
    print(prefix + "SOURCE_GUARD=PASS")
    live = report["live"]
    if live is not None:
        for key in (
            "public_root_proposals", "public_delta_surjectivity_proposals",
            "isolated_delta_surjectivity_proposals",
            "public_codomain_presentation_proposals",
            "public_delta_free_cyclic_image_proposals",
            "matching_cited_signed_delta_witness_count",
            "codomain_prior_db_admissible", "search_verified_steps",
        ):
            print(prefix + key.upper() + "=" + str(live[key]))
        print(prefix + "SEARCH_STATUS=" + live["search_status"])
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
