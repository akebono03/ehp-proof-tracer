"""Source-first (5.11) citation and public-provider wiring audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import traceback

from . import installer

PACKAGE = "phase175_r4r12r10r1_cited_511_public"
REVIEWED_HEAD = "3ec001a59044aeb056ec7190c43c6066eaf5abae"
REVIEWED_R9_HEAD = "bf0d7be3081c61f2feec075a3c82c2004c29bbf2"
REVIEWED_R9_COMMITTED_PATHS = frozenset({
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r12r8_delta_generator_source_audit/AUDIT_PLAN_JA.md",
    "phase175_r4r12r8_delta_generator_source_audit/CODE_FULL_JA.md",
    "phase175_r4r12r8_delta_generator_source_audit/README.md",
    "phase175_r4r12r8_delta_generator_source_audit/__init__.py",
    "phase175_r4r12r8_delta_generator_source_audit/audit.py",
    "phase175_r4r12r8_delta_generator_source_audit/output/audit_report.json",
    "phase175_r4r12r8_delta_generator_source_audit/output/preflight.json",
    "phase175_r4r12r8_delta_generator_source_audit/run.ps1",
    "phase175_r4r12r8_delta_generator_source_audit/tests/test_audit.py",
    "phase175_r4r12r9_delta_generator_image_bridge/AUDIT_PLAN_JA.md",
    "phase175_r4r12r9_delta_generator_image_bridge/CODE_FULL_JA.md",
    "phase175_r4r12r9_delta_generator_image_bridge/README.md",
    "phase175_r4r12r9_delta_generator_image_bridge/__init__.py",
    "phase175_r4r12r9_delta_generator_image_bridge/audit.py",
    "phase175_r4r12r9_delta_generator_image_bridge/installer.py",
    "phase175_r4r12r9_delta_generator_image_bridge/output/SHARED_PROVIDER_FULL_AFTER.py",
    "phase175_r4r12r9_delta_generator_image_bridge/output/audit_report.json",
    "phase175_r4r12r9_delta_generator_image_bridge/output/preflight.json",
    "phase175_r4r12r9_delta_generator_image_bridge/rule.py",
    "phase175_r4r12r9_delta_generator_image_bridge/run.ps1",
    "phase175_r4r12r9_delta_generator_image_bridge/tests/test_lineage.py",
    "phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py",
})


# R4R12R10R1R5: reviewed 2026-11-18 commit of audit/test packages.
# This commit does not change the tracked production module blob.
REVIEWED_R10_HEAD = "12d2116bc23e96c879d97b043dbc104b31030091"
REVIEWED_R10_COMMITTED_PATHS = frozenset({
    ".pytest_cache/v/cache/nodeids",
    "phase175_r4r12r10r1_cited_511_public/AUDIT_PLAN_JA.md",
    "phase175_r4r12r10r1_cited_511_public/CODE_FULL_JA.md",
    "phase175_r4r12r10r1_cited_511_public/README.md",
    "phase175_r4r12r10r1_cited_511_public/__init__.py",
    "phase175_r4r12r10r1_cited_511_public/audit.py",
    "phase175_r4r12r10r1_cited_511_public/installer.py",
    "phase175_r4r12r10r1_cited_511_public/output/preflight.json",
    "phase175_r4r12r10r1_cited_511_public/provider.py",
    "phase175_r4r12r10r1_cited_511_public/run.ps1",
    "phase175_r4r12r10r1_cited_511_public/source.py",
    "phase175_r4r12r10r1_cited_511_public/tests/test_cited_511.py",
    "phase175_r4r12r10r1_cited_511_public/tests/test_lineage.py",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/AUDIT_PLAN_JA.md",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/CODE_FULL_JA.md",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/README.md",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/__init__.py",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/audit.py",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/output/audit_report.json",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/output/preflight.json",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/run.ps1",
    "phase175_r4r12r10r1r3_orientation_type_diagnostic/tests/test_audit.py",
})


# R4R12R10R1R6: explicit review of the existing R10/R3 package overlay.
# No other tracked code, theorem source, or mathematical rule may be modified.
REVIEWED_R10_LOCAL_OVERLAY = frozenset({
    "phase175_r4r12r10r1_cited_511_public/AUDIT_PLAN_JA.md",
    "phase175_r4r12r10r1_cited_511_public/CODE_FULL_JA.md",
    "phase175_r4r12r10r1_cited_511_public/README.md",
    "phase175_r4r12r10r1_cited_511_public/audit.py",
    "phase175_r4r12r10r1_cited_511_public/provider.py",
    "phase175_r4r12r10r1_cited_511_public/tests/test_cited_511.py",
    "phase175_r4r12r10r1_cited_511_public/tests/test_lineage.py",
    "phase175_r4r12r10r1_cited_511_public/output/preflight.json",
})


def validate_reviewed_local_changes(dirty: set[str]) -> list[str]:
    """Reject any tracked source change outside the exact reviewed R10 overlay.

    The output/preflight.json exception is only for a prior failed audit
    report. Source and installer modules are deliberately not in this list.
    The production target is guarded separately by installer.plan().
    """
    allowed = REVIEWED_R10_LOCAL_OVERLAY | {
        str(installer.TARGET), ".pytest_cache/v/cache/nodeids",
    }
    unexpected = dirty - allowed
    if unexpected:
        raise RuntimeError(
            "R10R1_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(unexpected))
        )
    return sorted(dirty)


def validate_reviewed_lineage(head: str, committed_paths: frozenset[str],
                              ancestor_check: bool, commit_count: int) -> str:
    """Accept exactly three reviewed commits with exact cumulative diffs."""
    if head == REVIEWED_HEAD:
        if committed_paths or commit_count != 0:
            raise RuntimeError("R10R1_UNREVIEWED_OLD_HEAD_DIFF")
        return "R9_LOCAL_PATCH_BEFORE_COMMIT"
    if head == REVIEWED_R9_HEAD:
        if (not ancestor_check or commit_count != 1
                or committed_paths != REVIEWED_R9_COMMITTED_PATHS):
            raise RuntimeError("R10R1_UNREVIEWED_R9_COMMIT_DIFF")
        return "R9_REVIEWED_COMMITTED"
    if head == REVIEWED_R10_HEAD:
        expected = REVIEWED_R9_COMMITTED_PATHS | REVIEWED_R10_COMMITTED_PATHS
        if not ancestor_check or commit_count != 2 or committed_paths != expected:
            raise RuntimeError("R10R1_UNREVIEWED_R10_COMMIT_DIFF")
        return "R10_R3_REVIEWED_COMMITTED"
    raise RuntimeError("R10R1_UNREVIEWED_HEAD: " + head)


def verify_git(root: Path) -> dict[str, object]:
    if Path(installer.git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R10R1_WRONG_ROOT")
    if installer.git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R10R1_WRONG_BRANCH")
    head = installer.git(root, "rev-parse", "HEAD")
    from subprocess import run
    # Require Git to verify the exact reviewed ancestor and one-commit diff.
    ancestor = run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head],
        cwd=root, capture_output=True, check=False,
    ).returncode == 0
    count = int(installer.git(root, "rev-list", "--count", REVIEWED_HEAD + ".." + head))
    paths = frozenset(installer.git(
        root, "diff", "--name-only", REVIEWED_HEAD, head,
    ).splitlines())
    lineage = validate_reviewed_lineage(head, paths, ancestor, count)
    dirty = set(installer.git(root, "diff", "--name-only").splitlines())
    dirty.update(installer.git(root, "diff", "--cached", "--name-only").splitlines())
    reviewed_dirty = validate_reviewed_local_changes(dirty)
    return {"head": head, "dirty": reviewed_dirty, "lineage": lineage}


def inspect(root: Path, *, dry_run: bool) -> dict[str, object]:
    from .provider import expand_cited_511, same_registered_cited_511, RULE_NAME
    from .source import CitedToda511, canonical_511, verify_cited_511
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result

    git = verify_git(root)
    position = verify_cited_511(root)
    root_goal = exact_prior_database_result(5, 4)
    cyclic = CyclicStructureStatement(root_goal.lhs, root_goal.rhs.generator, 2)
    options = expand_public_two_summand_quotient(cyclic, proof_target=root_goal)
    if len(options) != 2:
        raise RuntimeError("R10R1_QUOTIENT_ROUTE_DRIFT")
    delta_goal = options[1].subgoals[2]
    if (not isinstance(delta_goal, GeneratorImage)
            or not same_registered_cited_511(delta_image_equality(delta_goal))):
        raise RuntimeError("R10R1_ORIENTATION1_TYPED_MISMATCH")
    actual_goal = delta_image_equality(delta_goal)
    isolated = expand_cited_511(actual_goal, (CitedToda511(canonical_511()),))
    if len(isolated) != 1 or isolated[0].subgoals != (CitedToda511(canonical_511()),):
        raise RuntimeError("R10R1_CITED_INFERENCE_MISSING")
    output = root / PACKAGE / "output"
    changed = installer.install(root, dry_run=dry_run, output=output)
    public = None
    if not dry_run:
        bridge = build_shared_typed_bridge()
        shared = shared_expansion_provider(bridge, proof_target=root_goal)
        relation_candidates = tuple(shared(actual_goal))
        selected = [x for x in relation_candidates if x.rule.name == RULE_NAME]
        image_candidates = tuple(shared(delta_goal))
        if len(selected) != 1:
            raise RuntimeError("R10R1_CITED_511_NOT_PUBLIC")
        if not any(x.rule.name == "proved typed Delta equality implies generator image"
                   and x.subgoals == (actual_goal,) for x in image_candidates):
            raise RuntimeError("R10R1_R9_IMAGE_BRIDGE_NOT_PUBLIC")
        public = {"cited_relation_candidates": len(selected),
                  "generator_image_candidates": len(image_candidates),
                  "cited_subgoal": repr(selected[0].subgoals[0]),
                  "typed_notation_match": True,
                  "orientation1_relation": repr(actual_goal)}
    return {"phase": PACKAGE, "git": git, "source_position": position,
            "installation": changed, "public": public, "new_group_result_given": 0,
            "cited_equation_given": 1, "new_mathematical_rules": 0,
            "full_pytest_executed": False, "group_complete": False,
            "recursive_proof_search_executed": False,
            "gate": "PASS_R4R12R10R1_CITED_511_CONNECTED_PROOF_PENDING"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    output = root / PACKAGE / "output" / ("preflight.json" if args.dry_run else "audit_report.json")
    try:
        result = inspect(root, dry_run=args.dry_run)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1_GATE=" + result["gate"])
        print("PHASE175_R4R12R10R1_GROUP_COMPLETE=False")
        print("PHASE175_R4R12R10R1_REPORT=" + str(output))
        return 0
    except Exception as error:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"gate": "FAIL_R4R12R10R1", "error": str(error),
                                     "traceback": traceback.format_exc()}, ensure_ascii=False,
                                     indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1_GATE=FAIL_R4R12R10R1")
        print("PHASE175_R4R12R10R1_ERROR=" + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
