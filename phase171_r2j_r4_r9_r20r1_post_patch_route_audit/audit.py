"""Phase 171 R20R1: locate the true competing right-end group proof paths.

This read-only audit never supplies an already inferred proof to another goal,
never changes the canonical resolver, and does not edit the R20 patch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from phase171_r2j_r4_r9_r20_eta_route_precedence import install as r20_install
from phase171_r2j_r4_r9_r20r1_post_patch_route_audit.classification import classify_routes

PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output" / "audit.json"
R19_REPORT = PACKAGE.parent / "phase171_r2j_r4_r9_r19_right_end_diagnostic" / "output" / "audit.json"


def preflight() -> dict[str, str]:
    """Accept only the reviewed committed original plus exact local R20 patch."""
    ready = r20_install.preflight()
    committed = r20_install.git_read("show", "HEAD:phase165_r52_r9_shared_math.py")
    local = r20_install.TARGET.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    original = committed.decode("utf-8-sig").replace("\r\n", "\n")
    if local != r20_install.patch_text(original):
        raise RuntimeError("R20R1 requires the exact installed R20 patch")
    if not R19_REPORT.is_file():
        raise RuntimeError("R19 report is missing")
    record = json.loads(R19_REPORT.read_text(encoding="utf-8-sig"))
    if record.get("phase") != "171-R2J-R4-R9-R19":
        raise RuntimeError("R19 report phase mismatch")
    if record.get("classification") != "RIGHT_GROUP_AMBIGUOUS_DERIVATIONS":
        raise RuntimeError("R19 ambiguity baseline mismatch")
    return {
        "branch": ready["branch"],
        "head": ready["head"],
        "original_blob": r20_install.blob_sha(committed),
        "r19_sha256": hashlib.sha256(R19_REPORT.read_bytes()).hexdigest(),
    }


def probe_one_route(
    goal: object,
    provider: object,
    option: object,
    bridge: object,
    citing: str,
    original_root: object,
) -> dict[str, Any]:
    """Restrict only the queried goal to one original provider proposal.

    All descendant goals are resolved by the actual shared provider.  No
    ProofStep or source is ever constructed or inserted by this wrapper.
    """
    from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import probe_premise

    def one_root_expansion(current: object) -> tuple:
        if type(current) is type(goal) and current == goal:
            return (option,)
        return provider(current)

    observed, step = probe_premise(
        goal, one_root_expansion, bridge, citing, original_root,
    )
    if step is not None and (step.conclusion != goal or step.inference_rule is None):
        raise RuntimeError("route returned an untrusted proof conclusion")
    return {
        "status": observed["status"],
        "error": observed.get("error"),
        "proved_rule": getattr(getattr(step, "inference_rule", None), "name", None),
        "source_ids": observed.get("source_ids"),
    }


def inspect_context(
    name: str,
    bridge: object,
    goal: object,
    citing: str,
    original_root: object,
) -> dict[str, Any]:
    """Trace each distinct root expansion without changing child providers."""
    from phase165_r52_r9_shared_math import shared_expansion_provider
    from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import probe_premise

    provider = shared_expansion_provider(bridge, proof_target=original_root)
    options = provider(goal)
    if not isinstance(options, tuple):
        raise RuntimeError("shared provider returned a non-tuple")
    direct, _ = probe_premise(goal, provider, bridge, citing, original_root)
    independent = []
    for index, option in enumerate(options, start=1):
        row = probe_one_route(goal, provider, option, bridge, citing, original_root)
        independent.append({
            "index": index,
            "rule": str(getattr(option.rule, "name", "")),
            "subgoals": [repr(item) for item in option.subgoals],
            **row,
        })
    return {
        "name": name,
        "right_goal": repr(goal),
        "direct_status": direct["status"],
        "direct_error": direct.get("error"),
        "provider_route_count": len(options),
        "routes": independent,
        "classification": classify_routes(
            direct["status"], tuple(row["status"] for row in independent),
        ),
    }


def inspect() -> dict[str, Any]:
    """Use both prior R18 source context and actual public-search context."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
    from phase171_r2j_r4_r9_r18_cardinality_premise_audit.audit import cardinality_route
    from homotopy_groups import TodaPrimaryGroup

    screened, root, citing = _screened_context()
    observed_contexts: list[object] = []
    public = search_group_from_registered_goal(
        n=3, k=3, bridge=build_shared_typed_bridge(), goal=root,
        context_sink=observed_contexts.append,
    )
    if len(observed_contexts) != 1:
        raise RuntimeError("expected the actual public-screened source context")
    provider = shared_expansion_provider(screened, proof_target=root)
    cardinality = FiniteGroupCardinality(TodaPrimaryGroup(6, 3), 4)
    right = cardinality_route(provider, cardinality).subgoals[2]
    contexts = {
        name: inspect_context(name, bridge, right, citing, root)
        for name, bridge in (("screened", screened), ("public", observed_contexts[0]))
    }
    return {
        "phase": "171-R2J-R4-R9-R20R1",
        "mode": "READ_ONLY_INDIVIDUAL_RIGHT_DERIVATION_AUDIT",
        "public_root_status": public.status.value,
        "contexts": contexts,
        "new_given": 0,
        "existing_source_changes": 0,
        "r20_patch_modified": False,
        "proof_tree_imported": False,
        "trust_boundary_modified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ready = preflight()
    print("PHASE171_R20R1_BRANCH=" + ready["branch"], flush=True)
    print("PHASE171_R20R1_HEAD=" + ready["head"], flush=True)
    print("PHASE171_R20R1_R20_PATCH=VERIFIED", flush=True)
    if args.dry_run:
        print("PHASE171_R20R1_RESULT=PASS_DRY_RUN", flush=True)
        return
    before = r20_install.git_read("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    if r20_install.git_read("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked source was changed during read-only audit")
    report.update({
        "git_head": ready["head"],
        "r19_sha256": ready["r19_sha256"],
        "tracked_status_unchanged": True,
    })
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R1_PUBLIC_ROOT=" + report["public_root_status"], flush=True)
    for name, row in report["contexts"].items():
        abbreviated = [{
            "index": item["index"], "rule": item["rule"],
            "status": item["status"], "error": item["error"],
        } for item in row["routes"]]
        print("PHASE171_R20R1_" + name.upper() + "_RIGHT_ERROR=" + str(row["direct_error"]), flush=True)
        print("PHASE171_R20R1_" + name.upper() + "_ROUTE_OUTCOMES=" + json.dumps(abbreviated, ensure_ascii=False), flush=True)
        print("PHASE171_R20R1_" + name.upper() + "_CLASSIFICATION=" + row["classification"], flush=True)
    print("PHASE171_R20R1_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R1_SOURCE_CHANGES=0", flush=True)
    print("PHASE171_R20R1_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R20R1_REPORT=" + str(OUTPUT), flush=True)
    print("PHASE171_R20R1_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
