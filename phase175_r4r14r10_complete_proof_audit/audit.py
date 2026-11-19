"""Read-only audit of the canonical (n,k)=(6,4) completed EHP proof.

No GIVEN, inference rule, shared provider, or renderer is changed here.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import traceback

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapSurjective
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, verified_db_step
from phase175_r4r14r9_literature_zero_image.rule import (
    RULE_NAME as LITERATURE_RULE_NAME,
    verified_literature_zero_image_inputs,
)
from phase175_r4r14r6_surjective_zero_codomain.rule import RULE_NAME as ROOT_RULE_NAME
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


ROOT = Path(__file__).resolve().parents[1]
REPORT_NAME = "EHP_Phase175_R4R14R10_complete_proof_audit.json"


def git(*args: str) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True,
        encoding="utf-8", errors="replace", text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + ": " + result.stderr.strip())
    return result.stdout.strip()


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    head = git("rev-parse", "HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    required = (
        "phase175_r4r14r9_literature_zero_image/rule.py",
        "phase175_r4r14r9_literature_zero_image/provider.py",
        "phase165_r52_r9_shared_math.py",
    )
    if any(not (ROOT / filename).is_file() for filename in required):
        raise RuntimeError("R4R14R9_MISSING")
    shared = (ROOT / required[-1]).read_text(encoding="utf-8-sig")
    if "build_literature_zero_image_provider" not in shared:
        raise RuntimeError("LITERATURE_PROVIDER_NOT_CONNECTED")
    if "expand_surjective_zero_codomain" not in shared:
        raise RuntimeError("ROOT_SURJECTIVE_ZERO_RULE_NOT_CONNECTED")
    return {
        "head": head,
        "tracked_changes": git("diff", "--name-only").splitlines(),
        "staged_changes": [],
        "historical_source_guard": "FOUR_KNOWN_FAILURES_NOT_RECLASSIFIED",
    }


def walk_proof(root_step: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse actual parent ProofSteps; reject cycles and non-step parents."""
    found: list[ProofStep] = []
    active: set[int] = set()
    seen: set[int] = set()

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise RuntimeError("NON_PROOFSTEP_PARENT")
        identity = id(step)
        if identity in active:
            raise RuntimeError("CYCLIC_PROOF_TREE")
        if identity in seen:
            return
        active.add(identity)
        for parent in step.premises:
            visit(parent)
        active.remove(identity)
        seen.add(identity)
        found.append(step)

    visit(root_step)
    return tuple(found)


def audit_live_proof() -> dict[str, object]:
    """Re-run production search and inspect its accepted, linked proof tree."""
    contexts: list[object] = []
    result = search_group_from_registered_goal(n=6, k=4, context_sink=contexts.append)
    status = getattr(result.status, "value", str(result.status))
    root_statement = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    if (status != "complete" or result.conclusion != root_statement
            or result.open_goals or len(contexts) != 1):
        raise RuntimeError("ROOT_SEARCH_NOT_COMPLETE_OR_CONTEXT_MISSING: " + status)
    bridge = contexts[0]
    roots = tuple(step for step in result.proven_steps if step.conclusion == root_statement)
    if len(roots) != 1:
        raise RuntimeError("ROOT_STEP_NOT_UNIQUE")
    root = roots[0]
    if (root.rule is not ProofRule.INFERENCE
            or getattr(root.inference_rule, "name", None) != ROOT_RULE_NAME
            or len(root.premises) != 2):
        raise RuntimeError("ROOT_INFERENCE_NOT_SURJECTIVE_ZERO_CODOMAIN")

    source = TodaPrimaryGroup(9, 5)
    mapping = TodaSuspensionMap(source, root_statement.group)
    expected_root_parents = (MapSurjective(mapping), ImageZeroStatement(mapping))
    if tuple(parent.conclusion for parent in root.premises) != expected_root_parents:
        raise RuntimeError("ROOT_PARENTS_NOT_EXACT_TYPED_MAP_PROPERTIES")
    if any(parent.rule is not ProofRule.INFERENCE for parent in root.premises):
        raise RuntimeError("ROOT_PARENT_NOT_INFERRED")

    zero_image = root.premises[1]
    presentation = exact_prior_database_result(5, 4)
    if presentation is None:
        raise RuntimeError("TYPED_PRIOR_PRESENTATION_MISSING")
    generator_zero = GeneratorImage(mapping, presentation.rhs.generator, Zero())
    if (getattr(zero_image.inference_rule, "name", None) != LITERATURE_RULE_NAME
            or len(zero_image.premises) != 2
            or tuple(parent.conclusion for parent in zero_image.premises)
            != (presentation, generator_zero)):
        raise RuntimeError("ZERO_IMAGE_NOT_LINKED_LITERATURE_RULE")
    literature_step, generator_step = zero_image.premises
    if (literature_step.rule is not ProofRule.GIVEN
            or generator_step.rule is not ProofRule.INFERENCE):
        raise RuntimeError("LITERATURE_OR_GENERATOR_PROVENANCE_INCORRECT")
    verified = verified_literature_zero_image_inputs(
        zero_image.conclusion, presentation, proof_target=root_statement, bridge=bridge,
    )
    if verified is None or verified[0] != (presentation, generator_zero) or verified[1] != literature_step:
        raise RuntimeError("LITERATURE_STEP_NOT_EXACT_LINKED_WITNESS")

    linked = tuple(link for link in bridge.proof_links if link.step == literature_step)
    if len(linked) != 1:
        raise RuntimeError("LITERATURE_LINK_NOT_UNIQUE")
    assertion = bridge.registry.assertion(linked[0].assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or reference.locator != "Proposition 5.8"):
        raise RuntimeError("PROPOSITION_58_CITATION_NOT_MATCHED")
    if verified_db_step(literature_step, proof_target=root_statement, bridge=bridge):
        raise RuntimeError("LITERATURE_STEP_MISTAKEN_FOR_DB_ADOPTION")

    tree = walk_proof(root)
    given = tuple(step for step in tree if step.rule is ProofRule.GIVEN)
    if any(step.conclusion == root_statement for step in given):
        raise RuntimeError("DIRECT_ROOT_GIVEN")
    # All leaves must originate from a genuinely linked, screened fixed statement.
    for step in given:
        if step.premises:
            raise RuntimeError("GIVEN_WITH_PARENTS")
        candidates = tuple(link for link in bridge.proof_links if link.step == step)
        if not candidates:
            raise RuntimeError("UNLINKED_GIVEN_IN_COMPLETED_TREE: " + repr(step.conclusion))
        if not any(
            bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
            and bridge.registry.assertion(link.assertion_id).content == step.conclusion
            for link in candidates
        ):
            raise RuntimeError("GIVEN_NOT_FIXED_SOURCE")
    cited_locators = sorted(set(
        bridge.registry.reference(bridge.registry.assertion(link.assertion_id).reference_id).locator
        for step in given for link in bridge.proof_links if link.step == step
    ))
    required_locators = ("Proposition 5.8", "(5.9)")
    if not all(locator in cited_locators for locator in required_locators):
        raise RuntimeError("EXPECTED_REFERENCES_NOT_IN_PROOF_TREE")

    return {
        "search_status": status,
        "root_conclusion": str(root_statement),
        "proven_steps": len(result.proven_steps),
        "tree_steps": len(tree),
        "open_goals": [],
        "root_rule": ROOT_RULE_NAME,
        "root_parent_rules": [getattr(step.inference_rule, "name", None) for step in root.premises],
        "zero_image_rule": LITERATURE_RULE_NAME,
        "zero_image_parent_rules": [getattr(step.rule, "name", str(step.rule)) for step in zero_image.premises],
        "literature_reference": reference.locator,
        "literature_fixed_origin": True,
        "literature_step_is_verified_db": False,
        "given_leaves": len(given),
        "given_leaf_locators": cited_locators,
        "public_references": list(result.references),
        "new_given": 0,
        "production_files_changed_by_audit": False,
        "full_pytest": False,
    }


def run(dry_run: bool) -> int:
    report: dict[str, object] = {"phase": "175_R4R14R10", "gate": "FAIL", "dry_run": dry_run}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["proof"] = audit_live_proof()
        report["gate"] = "PASS_READ_ONLY_DRYRUN" if dry_run else "PASS_COMPLETED_PROOF_TREE_AUDIT"
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
        report["traceback"] = traceback.format_exc()[-7000:]
    target = Path(os.environ.get("TEMP", tempfile.gettempdir())) / REPORT_NAME
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("R4R14R10_GATE=" + str(report["gate"]))
    print("R4R14R10_REPORT=" + str(target))
    if "error" in report:
        print("R4R14R10_ERROR=" + str(report["error"]))
        return 1
    if "proof" in report:
        proof = report["proof"]
        print("R4R14R10_SEARCH_STATUS=" + proof["search_status"])
        print("R4R14R10_OPEN_GOALS=" + str(len(proof["open_goals"])))
        print("R4R14R10_TREE_STEPS=" + str(proof["tree_steps"]))
        print("R4R14R10_REFERENCE_LOCATORS=" + repr(proof["given_leaf_locators"]))
        print("R4R14R10_NEW_GIVEN=0")
        print("R4R14R10_HISTORICAL_GUARD=KNOWN_FAILURES_RETAINED")
    print("(END)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
