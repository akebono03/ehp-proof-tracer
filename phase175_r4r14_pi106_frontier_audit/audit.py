"""Read-only Phase 175 R4R14 frontier audit for pi_10^6.

No proof step, citation, inference, or production code is installed here.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT_FILES = {
    "phase165_r52_r9_shared_math.py": "f5329594a8298af34cd05932bf4a7b6c59d6e4de",
    "phase165_r55_nk_only_goal.py": "e436879f578148fe5c30f5a34974bea3425108b2",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
}
TARGET = (6, 4)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("EXPECTED_DEVELOP")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_NOT_AUDITED")
    pinned = {}
    for path, sha in ROOT_FILES.items():
        target = root / path
        if not target.is_file():
            raise RuntimeError("MISSING_SOURCE: " + path)
        head_blob = git(root, "rev-parse", "HEAD:" + path)
        work_blob = git(root, "hash-object", path)
        if head_blob != sha or work_blob != sha:
            raise RuntimeError("SOURCE_BLOB_CHANGED: " + path + " head=" + head_blob + " work=" + work_blob)
        pinned[path] = sha
    return {"head": git(root, "rev-parse", "HEAD"), "branch": "develop", "source_blobs": pinned}


def inspect_live() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        canonical_annihilator_instance, expand_cited_annihilator_specialization, RULE_NAME,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from proof import ProofRule
    from web_group_proof import build_standard_web_group_proof_view

    n, k = TARGET
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    source_steps = [link.step for link in screened.proof_links
                    if link.step is not None and isinstance(link.step.conclusion, CitedFamilyAnnihilator)
                    and link.step.rule is ProofRule.GIVEN]
    if len(source_steps) != 1:
        raise RuntimeError("TODA59_SOURCE_COUNT_NOT_ONE: " + str(len(source_steps)))
    schema = source_steps[0].conclusion
    instance = canonical_annihilator_instance(schema, 6)
    if instance is None or instance == goal:
        raise RuntimeError("TODA59_N6_INSTANCE_NOT_TYPED")
    options = expand_cited_annihilator_specialization(instance, (schema,))
    if len(options) != 1 or options[0].subgoals != (schema,) or options[0].rule.name != RULE_NAME:
        raise RuntimeError("TODA59_N6_NOT_SOURCE_BACKED")
    provider = shared_expansion_provider(screened, proof_target=goal)
    public_options = [option for option in provider(instance) if option.rule.name == RULE_NAME]
    if len(public_options) != 1 or public_options[0].subgoals != (schema,):
        raise RuntimeError("TODA59_PUBLIC_PROVIDER_DISCONNECTED")
    required = ehp_zero_inputs(goal)
    if required is None:
        raise RuntimeError("EHP_EXACTNESS_ROUTE_NOT_TYPED")
    contexts = []
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge, context_sink=contexts.append)
    view = build_standard_web_group_proof_view(n, k, mode="narrative")
    web_key = view.key
    if result.status is ProofSearchStatus.COMPLETE:
        if web_key != "generic-complete-proof":
            raise RuntimeError("COMPLETE_SEARCH_WEB_DISAGREEMENT")
        state = "COMPLETE_ALREADY"
    else:
        if web_key != "generic-partial-proof":
            raise RuntimeError("PARTIAL_SEARCH_WEB_DISAGREEMENT")
        state = "PARTIAL_FRONTIER_CONFIRMED"
    return {
        "target": {"n": n, "k": k},
        "toda59_source_givens": len(source_steps),
        "toda59_n6_specialization": True,
        "public_specialization_options": len(public_options),
        "ehp_delta_route_premise_types": [type(x).__name__ for x in required],
        "ehp_delta_route_surjectivity_goal": str(required[0]),
        "search_status": result.status.name,
        "open_goals": [str(x) for x in result.open_goals],
        "web_key": web_key,
        "state": state,
        "new_given": 0,
        "new_rules": 0,
    }


def run(root: Path, dry_run: bool) -> int:
    report: dict[str, object] = {"phase": "175_R4R14", "mode": "AUDIT_ONLY", "full_pytest": False,
                                 "new_given": 0, "new_rules": 0, "gate": "FAIL_R4R14"}
    try:
        report["source_guard"] = source_guard(root)
        if dry_run:
            report["gate"] = "PASS_R4R14_DRYRUN_SOURCE_GUARD"
        else:
            report["live"] = inspect_live()
            report["gate"] = "PASS_R4R14_SOURCE_AND_EHP_FRONTIER_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14_pi106_frontier.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R4R14_GATE=" + str(report["gate"]))
    print("PHASE175_R4R14_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R4R14_ERROR=" + str(report["error"]))
        return 1
    if not dry_run:
        live = report["live"]
        print("PHASE175_R4R14_TODA59=REGISTERED_N6_TYPED_PUBLIC")
        print("PHASE175_R4R14_STATE=" + live["state"])
        print("PHASE175_R4R14_WEB=" + live["web_key"])
        print("PHASE175_R4R14_OPEN_GOALS=" + str(len(live["open_goals"])))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
