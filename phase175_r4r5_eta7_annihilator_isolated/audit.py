"""Phase 175 R4R5R2: derive m*g=0 from finite-cyclic summands.

Reuse explicit ordered DB priors for both pi_8^7 and pi_8^4; never replay
prior proofs. Direct-sum and single-summand inferences remain isolated;
production and source registries are not modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4_pi95_audit.audit import git, preflight
from phase175_r4r4_pi95_premise_frontier.audit import verify_code_and_source_pins
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    expand_finite_cyclic_order_zero,
    order_zero_premise, typed_endpoints,
)

PACKAGE = "phase175_r4r5_eta7_annihilator_isolated"
PRIOR_PACKAGE = "phase175_r4r4_pi95_premise_frontier"
PRIOR_GATE = "PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC"
EXPECTED_PRIOR_HEAD = "43140c00d311e4bbcc20688eb9e50a5d0050a787"
PINNED_R4R4_BLOB = "0a9fbbd1c3262dfc46ec8f6e8a819eb5876742fc"
DRY_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_DRYRUN"
FINAL_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC"
EXTRA_SOURCE_PINS = {
    # Existing ordered DB prior API and the concrete parsers it calls.
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "repository.py": "b648a360e98e3c3143d8f3c7489d8ade46b9ecb0",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    # Structural types and ordinary inference replay.
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase175_r4r4_pi95_premise_frontier/audit.py": PINNED_R4R4_BLOB,
}


def latest_prior_report(explicit: Path | None = None) -> Path:
    """Use only a successful non-DryRun R4R4 report, never invented evidence."""
    if explicit is not None:
        found = explicit.resolve()
        if not found.is_file():
            raise RuntimeError("R4R5_R4R4_REPORT_MISSING: " + str(found))
        return found
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for found in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            record = json.loads(found.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError):
            continue
        if isinstance(record, dict) and record.get("gate") == PRIOR_GATE:
            return found
    raise RuntimeError("R4R5_SUCCESSFUL_R4R4_REPORT_NOT_FOUND")


def validate_prior_report(record: object) -> dict[str, object]:
    """Check provenance and scope; a prior audit is never a proof certificate."""
    if not isinstance(record, dict):
        raise RuntimeError("R4R5_PRIOR_NOT_OBJECT")
    expected = {
        "phase": "175-R4R4",
        "mode": "SOURCE_FIRST_PREMISE_FRONTIER_AUDIT",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "public_proof_complete": False,
        "full_pytest_executed": False,
        "premise_count": 6,
        "verified_parent_steps_replayed_here": 0,
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R5_PRIOR_GATE_OR_SCOPE_INVALID")
    preflight_data = record.get("preflight")
    if (not isinstance(preflight_data, dict)
            or preflight_data.get("head") != EXPECTED_PRIOR_HEAD
            or preflight_data.get("pinned_source_count") != 18):
        raise RuntimeError("R4R5_PRIOR_HEAD_OR_SOURCE_INVALID")
    rows = record.get("premises")
    if (not isinstance(rows, list) or len(rows) != 6
            or [row.get("index") for row in rows if isinstance(row, dict)]
            != [1, 2, 3, 4, 5, 6]
            or any(row.get("verified_parent_step_in_r4r4") is not False
                   for row in rows if isinstance(row, dict))):
        raise RuntimeError("R4R5_PRIOR_PREMISE_FRONTIER_INVALID")
    return {"prior_head": preflight_data["head"], "premises": len(rows),
            "prior_audit_is_not_a_proof": True}


def validate_prior_lineage(root: Path, old_head: str, current_head: str) -> list[str]:
    """Allow the verified R4R4 package commit, no unrelated tracked changes."""
    if old_head != EXPECTED_PRIOR_HEAD:
        raise RuntimeError("R4R5_UNREVIEWED_PRIOR_HEAD")
    _, observed_head = git(root, "rev-parse", "HEAD")
    if observed_head != current_head:
        raise RuntimeError("R4R5_HEAD_CHANGED")
    status, _ = git(root, "merge-base", "--is-ancestor", old_head, current_head,
                    allow_failure=True)
    if status != 0:
        raise RuntimeError("R4R5_PRIOR_HEAD_NOT_ANCESTOR")
    _, names = git(root, "diff", "--name-only", old_head, current_head)
    changed = sorted(set(name.strip() for name in names.splitlines() if name.strip()))
    extra = [name for name in changed if not name.startswith(PRIOR_PACKAGE + "/")]
    if extra:
        raise RuntimeError("R4R5_UNREVIEWED_LINEAGE_CHANGES: " + repr(extra))
    return changed


def verify_source_pins(root: Path) -> dict[str, str]:
    """Pin committed DB-prior implementation, source data and inference code."""
    for name, expected in EXTRA_SOURCE_PINS.items():
        if not (root / name).is_file():
            raise RuntimeError("R4R5_SOURCE_MISSING: " + name)
        _, actual = git(root, "rev-parse", "HEAD:" + name)
        if actual != expected:
            raise RuntimeError("R4R5_SOURCE_PIN_DRIFT: " + name)
    verify_code_and_source_pins(root)
    return dict(EXTRA_SOURCE_PINS)


def eta7_prior_and_isolated_zero() -> dict[str, object]:
    """Reuse the verified, ordered DB prior; DO NOT reconstruct its proof tree.

    The target group is read only as a typed goal for the existing prior-order
    gate. Neither group row is asserted as a new literature statement. The
    ordinary m*g=0 inference is replayed against a checked DB-prior ProofStep.
    """
    from expression import GeneratorSymbol, HomotopyElement, Multiple, Zero
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, precedes_db_goal,
        verified_db_step,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    source_relation = exact_prior_database_result(7, 1)
    if (not isinstance(source_relation, Relation)
            or source_relation.relation_type is not RelationType.EQUALITY
            or source_relation.lhs != TodaPrimaryGroup(8, 7)
            or not isinstance(source_relation.rhs, FiniteCyclicGroup)
            or type(source_relation.rhs.order) is not int
            or source_relation.rhs.order != 2):
        raise RuntimeError("R4R5_PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID")
    generator = source_relation.rhs.generator
    if (not isinstance(generator, HomotopyElement)
            or generator.source != 8
            or generator.target != 7
            or generator.dimension != 7
            or not isinstance(generator.generator, GeneratorSymbol)
            or generator.generator.family != "η"
            or generator.generator.index != 7):
        raise RuntimeError("R4R5_PI87_DB_GENERATOR_UNVERIFIED")

    # The target is a GOAL only, not an assumed/proved result.
    target_relation = exact_prior_database_result(5, 4)
    if (not isinstance(target_relation, Relation)
            or target_relation.relation_type is not RelationType.EQUALITY
            or target_relation.lhs != TodaPrimaryGroup(9, 5)):
        raise RuntimeError("R4R5_PI95_DB_TARGET_GOAL_MISSING")
    if not precedes_db_goal(7, 1, 5, 4):
        raise RuntimeError("R4R5_PRIOR_ORDER_DISALLOWED")

    adopted_step = admitted_db_step(
        source_relation, proof_target=target_relation,
    )
    if (adopted_step is None
            or adopted_step.rule is not ProofRule.GIVEN
            or adopted_step.premises
            or adopted_step.conclusion != source_relation
            or not verified_db_step(adopted_step, proof_target=target_relation)):
        raise RuntimeError("R4R5_PI87_DB_PRIOR_AUTHENTICATION_FAILED")

    goal = Relation(Multiple(2, generator), Zero(), RelationType.EQUALITY)
    if order_zero_premise(goal) != source_relation:
        raise RuntimeError("R4R5_ORDER_ZERO_SOURCE_GOAL_NOT_IDENTICAL")
    options = expand_finite_cyclic_order_zero(goal)
    if len(options) != 1 or options[0].subgoals != (source_relation,):
        raise RuntimeError("R4R5_ORDER_ZERO_RULE_EXPANSION_FAILED")
    matches = find_inference_matches_for_rule(options[0].rule, (adopted_step,))
    if len(matches) != 1:
        raise RuntimeError("R4R5_ORDER_ZERO_RULE_MATCH_FAILED")
    step = apply_inference_match(matches[0])
    if (step.rule is not ProofRule.INFERENCE or step.conclusion != goal
            or step.premises != (adopted_step,)):
        raise RuntimeError("R4R5_ORDER_ZERO_PROOF_STEP_INVALID")

    return {
        "prior_group": "pi_8^7",
        "prior_status": "ADOPTED_DATABASE_PRIOR",
        "prior_rechecked_against_explicit_csv": True,
        "prior_order_checked_against_pi95": True,
        "prior_proof_search_executed": False,
        "prior_proof_tree_reconstructed": False,
        "source_goal": repr(source_relation),
        "target_is_unproved_goal": True,
        "derived_statement": repr(goal),
        "derived_rule": step.inference_rule.name,
        "derived_rule_proof_step": True,
        "derived_step_has_authenticated_db_premise": step.premises[0] is adopted_step,
        "adopted_db_prior_step_count": 1,
        "new_literature_given": 0,
        "registered_in_public": False,
    }


def direct_sum_prior_and_isolated_zero() -> dict[str, object]:
    """Use the earlier pi_8^4 *direct sum* without replaying its proof.

    Each component generator is independently tested against the same rule.
    Its DB prior is authenticated once using the existing strict order gate.
    This is an isolated rule application, NOT a public proof-tree insertion.
    """
    from expression import Multiple, Zero
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, precedes_db_goal,
        verified_db_step,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    source_relation = exact_prior_database_result(4, 4)
    target_relation = exact_prior_database_result(5, 4)
    if (not isinstance(source_relation, Relation)
            or source_relation.relation_type is not RelationType.EQUALITY
            or source_relation.lhs != TodaPrimaryGroup(8, 4)
            or not isinstance(source_relation.rhs, DirectSumGroup)
            or len(source_relation.rhs.summands) != 2
            or not all(isinstance(s, FiniteCyclicGroup)
                       and type(s.order) is int and s.order == 2
                       for s in source_relation.rhs.summands)):
        raise RuntimeError("R4R5_PI84_DIRECT_SUM_DB_PRIOR_MISSING")
    if (not isinstance(target_relation, Relation)
            or target_relation.relation_type is not RelationType.EQUALITY
            or target_relation.lhs != TodaPrimaryGroup(9, 5)
            or not precedes_db_goal(4, 4, 5, 4)):
        raise RuntimeError("R4R5_PI84_PRIOR_ORDER_OR_TARGET_INVALID")

    prior_step = admitted_db_step(source_relation, proof_target=target_relation)
    if (prior_step is None or prior_step.rule is not ProofRule.GIVEN
            or prior_step.premises
            or prior_step.conclusion != source_relation
            or not verified_db_step(prior_step, proof_target=target_relation)):
        raise RuntimeError("R4R5_PI84_DB_PRIOR_AUTHENTICATION_FAILED")

    derivations: list[dict[str, object]] = []
    for summand in source_relation.rhs.summands:
        if typed_endpoints(summand.generator) != (8, 4):
            raise RuntimeError("R4R5_PI84_GENERATOR_ENDPOINTS_INVALID")
        goal = Relation(
            Multiple(summand.order, summand.generator), Zero(),
            RelationType.EQUALITY,
        )
        if order_zero_premise(goal, source_relation) != source_relation:
            raise RuntimeError("R4R5_DIRECT_SUM_MEMBERSHIP_NOT_VERIFIED")
        proposals = expand_finite_cyclic_order_zero(goal, (source_relation,))
        if len(proposals) != 1 or proposals[0].subgoals != (source_relation,):
            raise RuntimeError("R4R5_DIRECT_SUM_RULE_EXPANSION_FAILED")
        matches = find_inference_matches_for_rule(proposals[0].rule, (prior_step,))
        if len(matches) != 1:
            raise RuntimeError("R4R5_DIRECT_SUM_RULE_MATCH_FAILED")
        result = apply_inference_match(matches[0])
        if (result.rule is not ProofRule.INFERENCE
                or result.conclusion != goal
                or result.premises != (prior_step,)):
            raise RuntimeError("R4R5_DIRECT_SUM_PROOF_STEP_INVALID")
        derivations.append({
            "generator": repr(summand.generator),
            "order": summand.order,
            "zero_relation": repr(result.conclusion),
            "inference_rule": result.inference_rule.name,
            "authenticated_prior_parent": result.premises[0] is prior_step,
        })

    if len(derivations) != 2 or len({item["generator"] for item in derivations}) != 2:
        raise RuntimeError("R4R5_PI84_TWO_DISTINCT_SUMMANDS_NOT_ESTABLISHED")
    return {
        "prior_group": "pi_8^4",
        "prior_status": "ADOPTED_DATABASE_PRIOR",
        "prior_rechecked_against_explicit_csv": True,
        "prior_order_checked_against_pi95": True,
        "prior_proof_search_executed": False,
        "prior_proof_tree_reconstructed": False,
        "summands_verified_in_isolation": 2,
        "inferred_zero_steps": len(derivations),
        "summand_derivations": derivations,
        "new_literature_given": 0,
        "registered_in_public": False,
    }


def output_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    dest = base / "EHPProofTracerAudit" / PACKAGE / stamp
    dest.mkdir(parents=True, exist_ok=False)
    return dest


def run(root: Path, dry_run: bool, prior_path: Path | None = None) -> int:
    output = output_folder()
    data: dict[str, object] = {
        "phase": "175-R4R5R2", "revision": "R2",
        "mode": "ISOLATED_ORDERED_DB_PRIOR_FINITE_DIRECT_SUM_ORDER_TO_ZERO",
        "dry_run": dry_run, "gate": "FAIL_R4R5_ETA7_ORDER_ZERO",
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 1,
        "rule_connected_to_public": False, "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    try:
        pre = preflight(root)
        data["preflight"] = pre
        prior_file = latest_prior_report(prior_path)
        data["prior_report_path"] = str(prior_file)
        old = validate_prior_report(json.loads(prior_file.read_text(encoding="utf-8")))
        data["prior_report_evidence"] = old
        data["lineage_paths"] = validate_prior_lineage(root, old["prior_head"], pre["head"])
        data["extra_source_pins"] = verify_source_pins(root)
        data["proposition25_status"] = "CITED_BUT_NOT_CONNECTED_BY_R4R5"
        data["toda58_status"] = "CITED_BUT_NOT_CONNECTED_BY_R4R5"
        if not dry_run:
            data["eta7"] = eta7_prior_and_isolated_zero()
            data["direct_sum"] = direct_sum_prior_and_isolated_zero()
        else:
            data["eta7"] = {"status": "NOT_READ_IN_DRYRUN", "prior_proof_search_executed": False}
            data["direct_sum"] = {"status": "NOT_READ_IN_DRYRUN", "prior_proof_search_executed": False}
        data["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        data["error"] = f"{type(exc).__name__}: {exc}"
        data["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R4R5R2 — 巡回直和成分の位数から零関係の推論監査", "",
        "Gate: `" + str(data["gate"]) + "`", "",
        "π₈⁷・π₈⁴ の認証済み先行 DB 結果から、各有限巡回成分の位数倍が0となる規則を隔離適用。",
        "先行群の完成証明の再探索は行わない。",
        "Proposition 2.5 と (5.8) の接続は次段階、π₉⁵ の公開証明は未完成。", "",
        "η₇ の実証: `" + str(data.get("eta7", {})) + "`", "",
        "直和成分の実証: `" + str(data.get("direct_sum", {})) + "`", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("PHASE175_R4R5_HEAD=" + str(data.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R5_PINNED_R4_SOURCES=" + str(data.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4R5_ADDITIONAL_SOURCE_PINS=" + str(len(data.get("extra_source_pins", {}))))
    print("PHASE175_R4R5_NEW_GIVEN=0")
    print("PHASE175_R4R5_NEW_GENERAL_RULES=1")
    print("PHASE175_R4R5_PUBLIC_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R5_FULL_PYTEST=NOT_RUN")
    eta = data.get("eta7", {})
    print("PHASE175_R4R5_PI87_PRIOR=" + str(eta.get("prior_status", eta.get("status", "UNVERIFIED"))))
    print("PHASE175_R4R5_PI87_PROOF_SEARCH_EXECUTED=" + str(eta.get("prior_proof_search_executed", False)))
    print("PHASE175_R4R5_2ETA7_ZERO_STEP=" + str(eta.get("derived_rule_proof_step", False)))
    direct_sum = data.get("direct_sum", {})
    print("PHASE175_R4R5_DIRECT_SUM_ZERO_STEPS=" + str(direct_sum.get("inferred_zero_steps", 0)))
    print("PHASE175_R4R5R2_DIRECT_SUM_ZERO_STEPS=" + str(direct_sum.get("inferred_zero_steps", 0)))
    print("PHASE175_R4R5_PI84_PROOF_SEARCH_EXECUTED=" + str(direct_sum.get("prior_proof_search_executed", False)))
    print("PHASE175_R4R5_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R5_GATE=" + str(data["gate"]))
    print("PHASE175_R4R5R2_GATE=" + str(data["gate"]))
    if "error" in data:
        print("PHASE175_R4R5_ERROR=" + data["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r4-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run, args.r4r4_report)


if __name__ == "__main__":
    sys.exit(main())
