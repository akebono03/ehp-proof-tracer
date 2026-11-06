"""R17: reviewed source and public typed pending map-goal display audit.

No map surjectivity or isomorphism is assumed. Audit distinguishes a cyclic
MapIsomorphism candidate from an independent certified proof.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, TARGET, blob_sha, expected_patched_bytes,
    matches_git_blob, normalize_and_style,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R17"
PRE_R16_HEAD = "e7bcd34a526b3f885a8e3be81c4aac362d8834c7"
REVIEWED_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
R16_PREFIX = "phase174_r3_r7_r16_public_ehp_zero_root/"
SHARED_MATH = "phase165_r52_r9_shared_math.py"
R15_SHARED_BLOB = "7f81769776278b46a220fb90771970a9dd7c73c2"
R16_SHARED_BLOB = "d42bb7420cf58f4dd466511d6498c66d9917b29c"
PINS = {
    "phase168_r3_27_typed_statement_projection.py": "26ce3632fe1b32bab7e822e8f701409b26f4f04a",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r16_public_ehp_zero_root/audit.py": "68e7611ede13f17a3358ee0754f5e296686ae042",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
    ).stdout


def reviewed_lineage(local: str, remote: str, committed: tuple[str, ...],
                     modified: tuple[str, ...], patched: bool) -> str:
    """Accept precisely the R16 working-tree handoff or merged state."""
    if remote != REVIEWED_HEAD or local not in (PRE_R16_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed local/remote develop HEAD; no automatic overwrite")
    if not committed or SHARED_MATH not in committed or not any(
        x.startswith(R16_PREFIX) for x in committed
    ) or any(x != SHARED_MATH and not x.startswith(R16_PREFIX) for x in committed):
        raise RuntimeError("Remote R16 lineage contains unexpected paths")
    target = TARGET.as_posix()
    initial = (SHARED_MATH,) if local == PRE_R16_HEAD else ()
    expected = tuple(sorted(initial + ((target,) if patched else ())))
    if tuple(sorted(modified)) != expected:
        raise RuntimeError("Unexpected local tracked changes: " + repr(modified))
    return ("LOCAL_R16_PATCH_UNCOMMITTED" if local == PRE_R16_HEAD
            else "R16_MERGED_CLEAN")


def verify_git_and_sources(*, patched: bool, root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R17 directly below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    local = git("rev-parse", "HEAD", root=root)
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged modifications require independent review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R16_HEAD, REVIEWED_HEAD, root=root)
    commits = git("rev-list", "--reverse", PRE_R16_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines()
    if len(commits) != 1:
        raise RuntimeError("Expected one reviewed R16 merge commit")
    diff_paths = tuple(git("diff", "--name-only", PRE_R16_HEAD, REVIEWED_HEAD, root=root).splitlines())
    lineage = reviewed_lineage(local, remote, diff_paths, changed, patched)
    for name, sha in PINS.items():
        file = root / name
        if not file.is_file() or not matches_git_blob(file.read_bytes(), sha):
            raise RuntimeError("R17 source pin changed: " + name)

    tracked_formatter = git_bytes("show", "HEAD:" + TARGET.as_posix(), root=root)
    if not matches_git_blob(tracked_formatter, EXPECTED_BLOB):
        raise RuntimeError("GitHub common formatter changed since review")
    target = root / TARGET
    source, _ = normalize_and_style(target.read_bytes())
    old, _ = normalize_and_style(tracked_formatter)
    expected = (normalize_and_style(expected_patched_bytes(tracked_formatter))[0]
                if patched else old)
    if source != expected:
        raise RuntimeError("Unreviewed local common formatter; abort")
    head_math = git_bytes("show", "HEAD:" + SHARED_MATH, root=root)
    expected_head = R15_SHARED_BLOB if local == PRE_R16_HEAD else R16_SHARED_BLOB
    if not matches_git_blob(head_math, expected_head):
        raise RuntimeError("R16 Git math baseline mismatch")
    if not matches_git_blob((root / SHARED_MATH).read_bytes(), R16_SHARED_BLOB):
        raise RuntimeError("Applied R16 shared math patch missing or altered")
    return {
        "local_head": local, "remote_head": remote,
        "lineage": lineage, "source_guard": "PASS",
        "pinned_paths": len(PINS) + 2, "modified_paths": changed,
        "r16_math_preserved": True,
    }


def previous_report_path() -> Path:
    home = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return home / "EHPProofTracerAudit" / "phase174_r3_r7_r16" / "public_ehp_root_audit.json"


def validate_r16_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R16"
            or report.get("gate") != "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN"
            or report.get("new_group_given") != 0
            or report.get("new_mathematical_inference_rules") != 0
            or report.get("full_pytest_run") is not False
            or report.get("root_proof_completed_claimed") is not False):
        raise RuntimeError("Prior R16 source-first result is not certified")
    live = report.get("live") or {}
    # R16 report structure is independently audited again in live R17, below.
    return {"gate": report["gate"], "root_was_not_completed": True}


def inspect_public_map_display() -> dict[str, Any]:
    """Compare real goal proof search, public math text, and cyclic iso branch."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import (
        MapInjective, MapIsomorphism, MapSurjective, expand_generic_iso_goal,
    )
    from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs, RULE_NAME
    from proof import ProofRule
    from web_group_proof_common import _group_proof_statement_latex

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    components = ehp_zero_inputs(goal)
    if components is None or len(components) != 4:
        raise RuntimeError("Typed EHP root obligations changed")
    surj = components[0]
    assert isinstance(surj, MapSurjective)
    rendered, fallback = _group_proof_statement_latex(surj)
    expected = r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}"
    if rendered != expected or fallback is not None:
        raise RuntimeError("Generic typed Delta-surjectivity math is not rendered")
    iso = MapIsomorphism(surj.map)
    iso_latex, iso_fallback = _group_proof_statement_latex(iso)
    inj_latex, inj_fallback = _group_proof_statement_latex(MapInjective(surj.map))
    if (iso_latex != r"\Delta: \pi_{13}^{13} \xrightarrow{\cong} \pi_{11}^{6}"
            or iso_fallback is not None
            or inj_latex != r"\Delta: \pi_{13}^{13} \hookrightarrow \pi_{11}^{6}"
            or inj_fallback is not None):
        raise RuntimeError("General typed map-property LaTeX is inconsistent")

    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root_options = tuple(provider(goal))
    surj_options = tuple(provider(surj))
    iso_options = tuple(provider(iso))
    generic_iso = tuple(expand_generic_iso_goal(iso))
    if (len(root_options) != 1 or root_options[0].rule.name != RULE_NAME
            or root_options[0].subgoals != components or surj_options):
        raise RuntimeError("R16 root or unresolved Delta-surjectivity baseline changed")
    cyclic_iso = bool(generic_iso) and surj in generic_iso[0].subgoals
    if not cyclic_iso:
        raise RuntimeError("Generic isomorphism proof dependency was unexpectedly changed")
    if any(link.step is not None and link.step.conclusion in (goal, surj, iso)
           and link.step.rule is ProofRule.GIVEN for link in screened.proof_links):
        raise RuntimeError("Target, Delta surjectivity, or Delta isomorphism was a direct GIVEN")

    result = search_group_from_registered_goal(n=7, k=5, bridge=bridge, goal=goal)
    if (result.status is ProofSearchStatus.COMPLETE or result.conclusion is not None
            or any(step.conclusion == goal for step in result.proven_steps)
            or not any(open_goal == surj for open_goal in result.open_goals)):
        raise RuntimeError("Unexpected claim of completed target proof or lost Delta goal")
    markdown = render_partial_proof_markdown(result)
    if ("$" + expected + "$" not in markdown
            or "MapSurjective（数式表示未対応）" in markdown):
        raise RuntimeError("Public common partial renderer did not display Delta math")
    return {
        "public_root_candidates": len(root_options),
        "public_delta_surjectivity_candidates": len(surj_options),
        "public_delta_isomorphism_candidates": len(iso_options),
        "generic_isomorphism_depends_on_surjectivity": cyclic_iso,
        "direct_given_for_goal_or_delta": False,
        "delta_latex": rendered,
        "search_status": result.status.value,
        "open_goal_types": [type(item).__name__ for item in result.open_goals],
        "proven_steps": len(result.proven_steps),
        "math_rule_changes": 0,
        "new_proof_steps": 0,
        "completion_claimed": False,
    }


def report_path(*, dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    name = "typed_map_preflight.json" if dry_run else "typed_map_public_audit.json"
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / name


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(patched=not dry_run, root=root)
    prior = previous_report_path()
    if not prior.is_file():
        raise RuntimeError("R16 public audit evidence not found: " + str(prior))
    previous = validate_r16_report(json.loads(prior.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_public_map_display()
    return {
        "phase": PHASE, "git_state": state, "previous": previous,
        "mode": "PREFLIGHT" if dry_run else "TYPED_PUBLIC_MAP_GOAL_DISPLAY",
        "live": live,
        "new_group_given": 0, "new_math_rules": 0,
        "production_math_modified": False,
        "full_pytest_run": False, "completion_claimed": False,
        "gate": ("PASS_PREFLIGHT" if dry_run else
                 "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = report_path(dry_run=args.dry_run)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R17_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["lineage"])
    print(prefix + "SOURCE_GUARD=PASS")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ROOT_PROPOSALS=" + str(live["public_root_candidates"]))
        print(prefix + "DELTA_SURJECTIVITY_PROPOSALS=" + str(live["public_delta_surjectivity_candidates"]))
        print(prefix + "ISOMORPHISM_PROPOSALS=" + str(live["public_delta_isomorphism_candidates"]))
        print(prefix + "ISOMORPHISM_CYCLE_GUARD=" + str(live["generic_isomorphism_depends_on_surjectivity"]))
        print(prefix + "PUBLIC_DELTA_LATEX=" + live["delta_latex"])
        print(prefix + "SEARCH_STATUS=" + live["search_status"])
        print(prefix + "SEARCH_PROVEN_STEPS=" + str(live["proven_steps"]))
        print(prefix + "OPEN_GOALS=" + str(len(live["open_goal_types"])))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
