"""Read-only R13R5 audit of the typed Delta-injectivity candidate frontier."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import traceback

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    _linear_coordinates,
    delta_injective_inputs,
    DELTA_RULE_NAME,
)
from phase175_r4r12r13r3_public_delta_e_bridge.provider import (
    delta_free_coordinate_proposals,
    screened_toda58_available,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import Relation, RelationType

PACKAGE = "phase175_r4r12r13r5_delta_guard_audit"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R13R5_GIT_FAILURE: " + process.stderr.strip())
    return process.stdout.strip()


def inspect_delta_guard() -> dict[str, object]:
    """Separate citation, group structure, generator identity, and provider wiring."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    signed = canonical_toda58()
    goal = MapInjective(signed.map)
    source = Relation(signed.map.source_group, FreeCyclicGroup(signed.element), RelationType.EQUALITY)
    target = exact_prior_database_result(4, 3)
    proof_target = exact_prior_database_result(5, 4)
    if proof_target is None:
        raise RuntimeError("R13R5_TARGET_PRIOR_RECORD_MISSING")
    bridge = build_shared_typed_bridge()
    cited = screened_toda58_available(bridge)
    direct = delta_free_coordinate_proposals(goal, cited58=cited)
    shared = tuple(shared_expansion_provider(bridge, proof_target=proof_target)(goal))
    selected = tuple(candidate for candidate in shared if candidate.rule.name == DELTA_RULE_NAME)
    structure: dict[str, object] = {
        "target_prior_exists": target is not None,
        "target_is_relation": isinstance(target, Relation),
        "target_is_equality": isinstance(target, Relation) and target.relation_type is RelationType.EQUALITY,
        "target_lhs_matches_delta": isinstance(target, Relation) and target.lhs == signed.map.target_group,
        "target_rhs_is_direct_sum": isinstance(target, Relation) and isinstance(target.rhs, DirectSumGroup),
        "target_repr": repr(target),
        "source_repr": repr(source),
        "delta_image_repr": repr(signed),
    }
    if isinstance(target, Relation) and isinstance(target.rhs, DirectSumGroup):
        parts = target.rhs.summands
        free = tuple(p for p in parts if isinstance(p, FreeCyclicGroup))
        finite = tuple(p for p in parts if isinstance(p, FiniteCyclicGroup))
        structure.update({
            "summand_count": len(parts),
            "summand_types": [type(p).__name__ for p in parts],
            "free_summand_count": len(free),
            "finite_summand_count": len(finite),
            "summand_generator_reprs": [repr(getattr(p, "generator", None)) for p in parts],
        })
        if len(free) == 1 and len(finite) == 1:
            expression = signed.positive_value
            structure.update({
                "source_free_coordinate_expression_repr": repr(expression.left.expression),
                "source_torsion_coordinate_expression_repr": repr(expression.right.expression),
                "free_generator_exact_match": free[0].generator == expression.left.expression,
                "torsion_generator_exact_match": finite[0].generator == expression.right.expression,
                "linear_coordinates": _linear_coordinates(
                    expression, free[0].generator, finite[0].generator,
                ),
                "torsion_order": finite[0].order,
            })
    accepted = delta_injective_inputs(goal, source, target, signed)
    structure["delta_guard_accepts"] = accepted is not None
    return {
        "toda58_citation_screened": cited,
        "direct_provider_candidate_count": len(direct),
        "shared_provider_candidate_count": len(selected),
        "shared_other_candidate_names": [c.rule.name for c in shared if c.rule.name != DELTA_RULE_NAME][:15],
        "guard": structure,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "public_code_modified": False,
        "recursive_proof_executed": False,
        "proof_complete": False,
    }


def run(root: Path, *, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175-R4R12R13R5", "dry_run": dry_run,
        "gate": "FAIL_R13R5", "full_pytest_executed": False,
        "new_given": 0, "new_mathematical_rules": 0,
        "target_proof_complete": False,
    }
    try:
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("R13R5_WRONG_ROOT")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("R13R5_WRONG_BRANCH")
        report["head"] = git(root, "rev-parse", "HEAD")
        report["diagnostics"] = inspect_delta_guard()
        report["gate"] = "PASS_R13R5_READ_ONLY_DELTA_GUARD_AUDIT_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    path = output / ("dry_run_report.json" if dry_run else "report.json")
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R5_GATE=" + str(report["gate"]))
    print("PHASE175_R13R5_HEAD=" + str(report.get("head", "UNVERIFIED")))
    diagnostics = report.get("diagnostics", {})
    if diagnostics:
        print("PHASE175_R13R5_CITED58=" + str(diagnostics["toda58_citation_screened"]))
        print("PHASE175_R13R5_DIRECT_DELTA_CANDIDATES=" + str(diagnostics["direct_provider_candidate_count"]))
        print("PHASE175_R13R5_SHARED_DELTA_CANDIDATES=" + str(diagnostics["shared_provider_candidate_count"]))
        guard = diagnostics["guard"]
        for key in ("target_is_relation", "target_lhs_matches_delta", "target_rhs_is_direct_sum", "free_generator_exact_match", "torsion_generator_exact_match", "linear_coordinates", "delta_guard_accepts"):
            print("PHASE175_R13R5_" + key.upper() + "=" + str(guard.get(key, "NOT_APPLICABLE")))
    print("PHASE175_R13R5_NEW_GIVEN=0")
    print("PHASE175_R13R5_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R5_REPORT=" + str(path))
    if "error" in report:
        print("PHASE175_R13R5_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args(argv)
    return run(arguments.root.resolve(), dry_run=arguments.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
