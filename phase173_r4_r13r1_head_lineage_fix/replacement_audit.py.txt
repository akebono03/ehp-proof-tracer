"""Read-only source, proof-tree, citation and Web audit for pi_7^4..pi_11^4.

The implementation makes no production edits, accepts no goals as proof
premises, and does not widen the supported range to pi_12^4.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    verified_db_step,
)
from phase173_r4_r10_general_toda56_core.core import checked_general_inputs
from phase173_r4_r12_common_narrative.projection import (
    GENERIC_ROOT,
    LEGACY_ROOT,
    SOURCE_FIRST_ROOT,
    _source_number,
    project_verified_toda56_narrative,
)
from phase173_r4_r12_common_narrative.install import git, preflight
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view

REVIEWED_HEAD = "a9b4617fbef603e4ced2252b7812d2dfa19fc606"
ADAPTER_PATH = "phase165_r52_r3_web_adapter.py"


def source_guard(root: Path) -> None:
    """Accept only the reviewed pre-commit or committed R4-R12 tree.

    R4-R12's original installer is valid for the pre-commit worktree but
    refuses the legitimate committed adapter blob. For the committed case,
    reproduce its byte-exact patch from the audited parent and verify its
    projector and predecessor proof route before accepting any narrative.
    """
    import subprocess
    from hashlib import sha256

    committed_head = "33f73f1dfb853875589b8fb70bda9853c75a8dae"
    committed_adapter_blob = "57b079d51d6d5810ab0be6884feae1ed117a386c"
    head = git(root, "rev-parse", "HEAD")
    if head not in (REVIEWED_HEAD, committed_head):
        raise RuntimeError(f"HEAD differs from both reviewed R4-R12 states: {head}")
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4-R13 must run from the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4-R13 requires develop")
    remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop").split()[0]
    if remote != head:
        raise RuntimeError("Local HEAD differs from GitHub develop")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    changed = tuple(git(root, "diff", "--name-only").splitlines())

    if head == REVIEWED_HEAD:
        target, actual, expected, installed = preflight(root)
        if target != root / ADAPTER_PATH or not installed or actual != expected:
            raise RuntimeError("R4-R12 uncommitted Web adapter differs from reviewed patch")
        if changed != (ADAPTER_PATH,):
            raise RuntimeError(f"Unexpected tracked worktree changes: {changed!r}")
    else:
        from phase173_r4_r12_common_narrative.install import (
            EXISTING_PROOF_TARGET,
            EXPECTED_PROJECTOR_SHA256,
            git_bytes,
            patched_source,
        )
        from phase173_r4_r11_zero_public_connection import install as earlier

        if changed:
            raise RuntimeError(f"Committed R4-R12 worktree has tracked changes: {changed!r}")
        if git(root, "rev-parse", "HEAD:" + ADAPTER_PATH) != committed_adapter_blob:
            raise RuntimeError("Committed R4-R12 Web adapter blob differs")
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head],
            cwd=root, check=False,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("R4-R12 HEAD lineage is not verified")
        source_before = git_bytes(root, "show", REVIEWED_HEAD + ":" + ADAPTER_PATH)
        fixture = (root / "phase173_r4_r12_common_narrative"
                   / "web_adapter_FULL.py.txt").read_text(encoding="utf-8")
        expected = patched_source(source_before, fixture)
        if (root / ADAPTER_PATH).read_bytes() != expected:
            raise RuntimeError("Committed R4-R12 Web adapter is not the reviewed patch")
        if git_bytes(root, "show", "HEAD:" + ADAPTER_PATH) != expected:
            raise RuntimeError("Committed Web adapter differs from reviewed source")
        projector = (root / "phase173_r4_r12_common_narrative" / "projection.py")
        if (not projector.is_file()
                or sha256(projector.read_bytes()).hexdigest()
                != EXPECTED_PROJECTOR_SHA256):
            raise RuntimeError("R4-R12 narrative projector differs from reviewed bytes")
        earlier_source = git_bytes(
            root, "show", earlier.BASE_HEAD + ":" + EXISTING_PROOF_TARGET,
        )
        earlier_fixture = (root / "phase173_r4_r11_zero_public_connection"
                           / "search_group_from_registered_goal_FULL.py.txt").read_text(
                               encoding="utf-8",
                           )
        expected_proof = earlier.patched_source(earlier_source, earlier_fixture)
        if (root / EXISTING_PROOF_TARGET).read_bytes() != expected_proof:
            raise RuntimeError("Existing R4-R11 zero-group proof route differs")

    print("PHASE173_R4_R13_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R13_HEAD=" + head, flush=True)


def inspect_dimension(dimension: int, *, with_web: bool = True) -> dict:
    """Audit first completed root and existing citation ownership, not just UI key."""
    if type(dimension) is not int or dimension not in (7, 8, 9, 10, 11):
        raise ValueError("R4-R13 concerns only five already-completed dimensions")
    bridge = build_shared_typed_bridge()
    contexts: list = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=bridge,
        context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise ValueError(f"pi_{dimension}^4 no longer has a completed screened proof")
    model = build_linked_proof_narrative_model(result, contexts[0])
    if model.root_index is None:
        raise ValueError("A complete proof lacks a narrative root")
    root = model.steps[model.root_index]
    name = getattr(getattr(root, "inference_rule", None), "name", None)
    expected_name = LEGACY_ROOT if dimension == 7 else (
        SOURCE_FIRST_ROOT if dimension in (8, 9, 10) else GENERIC_ROOT
    )
    if (root.rule is not ProofRule.INFERENCE
            or name != expected_name
            or root.conclusion != result.conclusion
            or root.inference_rule is None
            or len(root.premises) != 4
            or not root.inference_rule.match_guard(root.premises, {})):
        raise ValueError(f"Unexpected typed proof root for pi_{dimension}^4")
    base = render_model_backed_narrative_markdown(result, model)
    projected = project_verified_toda56_narrative(result, model, base)
    if ("使用する結果" not in projected
            or projected.count("\n証明\n") != 1
            or not projected.endswith("□\n")
            or "Proposition 4.4" not in projected):
        raise ValueError("Narrative sections are missing or malformed")
    if dimension > 7:
        theorem, left, right, hopf = root.premises
        first = exact_prior_database_result(3, dimension - 4)
        second = exact_prior_database_result(7, dimension - 7)
        if (left.conclusion != first or right.conclusion != second
                or not verified_db_step(left, proof_target=result.conclusion,
                                        bridge=contexts[0])
                or not verified_db_step(right, proof_target=result.conclusion,
                                        bridge=contexts[0])):
            raise ValueError("One or both adopted database priors lost certification")
        sources = (
            _source_number(model, theorem, locator="Proposition 4.4"),
            _source_number(model, left, db_prior=True),
            _source_number(model, right, db_prior=True),
            _source_number(model, hopf.premises[0], locator="Lemma 5.4"),
        )
        if (len(set(sources)) != 4
                or rf"\Phi_{{{dimension}}}:" not in projected
                or rf"i={dimension}" not in projected
                or rf"\pi_{{{dimension - 1}}}^3\oplus\pi_{{{dimension}}}^7"
                   not in projected):
            raise ValueError("Proposition 4.4 specialization or citations changed")
        if dimension == 11:
            if ("両側の先行群はいずれも零群" not in projected
                    or r"\pi_{11}^{4} = 0" not in projected
                    or r"\Phi_{11}(" in projected):
                raise ValueError("Zero group narrative falsely presents a generator image")
        elif "生成元の対応" not in projected:
            raise ValueError("Nonzero group narrative omitted map components")
    if with_web:
        view = build_standard_web_group_proof_view(
            n=4, k=dimension - 4,
            mode="narrative", citation_source="model",
        )
        math = tuple(segment.value for line in view.rendered_lines
                     for segment in line.segments
                     if segment.kind in ("inline_math", "display_math"))
        if (view.key != "generic-complete-proof" or view.partial_result
                or not view.rendered_lines
                or not any(r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in expr
                           for expr in math)
                or (dimension > 7 and not any(
                    rf"\Phi_{{{dimension}}}:" in expr for expr in math
                ))):
            raise ValueError("Web narrative does not reflect the certified model")
    citations = tuple({
        "number": citation.number,
        "locator": citation.reference.locator or citation.reference.label,
        "step_indices": list(citation.step_indices),
    } for citation in model.citations)
    row = {
        "group": f"pi_{dimension}^4",
        "dimension": dimension,
        "root_rule": name,
        "source_verified": True,
        "source_reference_count": len(citations),
        "source_references": citations,
        "open_goals": len(result.open_goals),
        "web_verified": with_web,
        "narrative_markdown": projected,
    }
    print(
        f"PHASE173_R4_R13_PI_{dimension}_4"
        f" ROOT_CERTIFIED=True REFERENCES={len(citations)}"
        f" OPEN=0 WEB_CHECKED={with_web}",
        flush=True,
    )
    return row


def inspect_unproven_epsilon() -> bool:
    """The general rule must refuse a merely compatible pi_12^4 DB goal."""
    goal = exact_prior_database_result(4, 8)
    result = goal is not None and checked_general_inputs(goal) is None
    print("PHASE173_R4_R13_PI_12_4_UNPROVEN_REJECTED=" + str(result), flush=True)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source_guard(root)
    if args.dry_run:
        print("PHASE173_R4_R13_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R13_RESULT=PASS_DRY_RUN", flush=True)
        return 0
    rows = [inspect_dimension(i) for i in (7, 8, 9, 10, 11)]
    rejected = inspect_unproven_epsilon()
    if not rejected or any(not row["source_verified"] or not row["web_verified"]
                           for row in rows):
        print("PHASE173_R4_R13_RESULT=FAIL", flush=True)
        return 2
    output = Path(__file__).with_name("verification_result.json")
    output.write_text(json.dumps({
        "phase": "173 R4-R13", "read_only": True,
        "reviewed_head": REVIEWED_HEAD,
        "groups": rows,
        "pi12_unproven_rejected": rejected,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R13_REPORT=" + str(output), flush=True)
    print("PHASE173_R4_R13_ALL_FIVE_SOURCE_AND_WEB=PASS", flush=True)
    print("PHASE173_R4_R13_RESULT=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
