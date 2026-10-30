"""Read-only assessment of the remaining pi_6^3 extension obligations.

This module adds no GIVEN, proof rule, or completed group structure.
All source facts must be screened using the already positioned pi_6^3 target.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from expression import Composition, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaProp42ExactnessStatement
from homotopy_groups import TodaEHPExactnessWindow
from map_facts import EHP_E_MAP, EHP_H_MAP
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
DOUBLE_SUFFIX = "toda:adopted:eq5.3:nu_prime_double_relation"
HOPF_SUFFIX = "toda:adopted:eq5.3:nu_prime_hopf_relation"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("read-only Git command required")
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def _fixed_source_records(screened, citing, *, locator: str | None = None) -> list[dict]:
    """Inspect only earlier, publication-screened fixed GIVEN source facts."""
    found: list[dict] = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if locator is not None and reference.locator != locator:
            continue
        if not (
            step is not None
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            continue
        found.append({
            "assertion_id": link.assertion_id,
            "locator": reference.locator,
            "type": type(step.conclusion).__name__,
            "statement": repr(step.conclusion)[:1500],
            "publication_position": reference.publication_position,
        })
    return found


def _matching_screened_relation(screened, citing, suffix: str):
    """Find a unique relation identified by a screened source assertion ID."""
    matches = []
    for link in screened.proof_links:
        if not link.assertion_id.endswith(suffix) or link.step is None:
            continue
        assert_row = screened.registry.assertion(link.assertion_id)
        if (
            assert_row.origin is AssertionOrigin.FIXED_STATEMENT
            and link.step.rule is ProofRule.GIVEN
            and not link.step.premises
            and link.step.conclusion == assert_row.content
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matches.append(link.step.conclusion)
    return matches[0] if len(matches) == 1 else None


def _extension_window() -> TodaProp42ExactnessStatement:
    """Actual E-H window for pi_5^2 -> pi_6^3 -> pi_6^5."""
    return TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(5, 2),
        middle_term=TodaPrimaryGroup(6, 3),
        target_term=TodaPrimaryGroup(6, 5),
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))


def _generator_image_goal(source: Relation, double: Relation):
    """Propose an E-image only for correctly typed full generator composites.

    The existing recursive _endpoints validates nested composition; the
    legacy Composition.is_type_compatible accepts only elementary factors.
    This returns a goal, not evidence that the E-image equality holds.
    """
    if not (
        isinstance(source, Relation)
        and source.relation_type is RelationType.EQUALITY
        and source.lhs == TodaPrimaryGroup(5, 2)
        and isinstance(source.rhs, FiniteCyclicGroup)
        and source.rhs.order == 2
        and isinstance(double, Relation)
        and double.relation_type is RelationType.EQUALITY
        and isinstance(double.lhs, Multiple)
        and double.lhs.coefficient == 2
        and isinstance(double.rhs, Composition)
        and _endpoints(source.rhs.generator) == (5, 2)
        and _endpoints(double.lhs.expression) == (6, 3)
        and _endpoints(double.rhs) == (6, 3)
    ):
        return None
    return GeneratorImage(
        map=TodaSuspensionMap(
            TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
        ),
        source_generator=source.rhs.generator,
        target_generator=double.rhs,
    )


def _summarize_options(provider, goal) -> dict:
    if goal is None:
        return {"count": 0, "names": [], "subgoals": []}
    options = provider(goal)
    return {
        "count": len(options),
        "names": [str(option.rule.name) for option in options[:24]],
        "subgoals": [
            [repr(item)[:350] for item in option.subgoals]
            for option in options[:12]
        ],
    }


def inspect() -> dict:
    """Observe the actual project registry without claiming missing proofs are done."""
    screened, goal63, citing = _screened_context()
    double = _matching_screened_relation(screened, citing, DOUBLE_SUFFIX)
    hopf = _matching_screened_relation(screened, citing, HOPF_SUFFIX)
    group52_db = database_structured_group_goal_candidates(n=2, k=3)
    if len(group52_db) != 1:
        group52_db = ()
    group52_registered = registered_group_goal_candidates(screened, n=2, k=3)
    group65_registered = registered_group_goal_candidates(screened, n=5, k=1)
    target_relations = registered_group_goal_candidates(screened, n=3, k=3)
    provider = shared_expansion_provider(screened, proof_target=goal63)
    image_goal = _generator_image_goal(group52_db[0], double) if group52_db and double else None
    exact = _extension_window()
    source_inventory = {
        locator: _fixed_source_records(screened, citing, locator=locator)
        for locator in ("Proposition 4.2 (4.4)", "(5.2)", "Proposition 5.3", "(5.3)", "Proposition 5.1", "Proposition 5.6")
    }
    return {
        "phase": "171-R2J-R4-R1",
        "mode": "AUDIT_ONLY",
        "pi63_goal": repr(goal63),
        "pi63_citing_id": citing,
        "screened_source_inventory": source_inventory,
        "pi63_target_registered_count": len(target_relations),
        "pi52_db_candidates": [repr(value) for value in group52_db],
        "pi52_registered_candidates": [repr(value) for value in group52_registered],
        "pi65_registered_candidates": [repr(value) for value in group65_registered],
        "nu_prime_double_source_screened": double is not None,
        "nu_prime_double_statement": repr(double) if double else None,
        "nu_prime_hopf_source_screened": hopf is not None,
        "nu_prime_hopf_statement": repr(hopf) if hopf else None,
        "ehp_e_h_window_valid": prop42_exactness_indices(exact) is not None,
        "ehp_e_h_window": repr(exact),
        "suspended_pi52_generator_goal": repr(image_goal) if image_goal is not None else None,
        "suspended_pi52_generator_frontier": _summarize_options(provider, image_goal),
        "pi63_root_frontier": _summarize_options(provider, goal63),
        "open_proof_obligations": [
            "Prove the pi_5^2 group structure from earlier cited sources; never adopt Proposition 5.6 target as a premise",
            "Prove E(eta_2^3)=eta_3 eta_4 eta_5 as a typed generator image",
            "Prove H: pi_6^3 -> pi_6^5 surjective from cited H(nu')=eta_5 and the proved pi_6^5 generator",
            "Derive the short exact extension and order four without importing the target group fact",
            "Use the cited double relation and nonzero injected generator to prove nu-prime has order four",
            "Construct the final pi_6^3 cyclic presentation using actual inference ancestry",
        ],
        "pi63_proven": False,
        "given_added": 0,
        "production_changed": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("audit requires develop and does not change the branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    print("PHASE171_R2J_R4_R1_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R1_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R1_RESULT=PASS_DRY_RUN", flush=True)
        return
    from phase171_r2j_r3_ehp_exactness.audit import build_r2j_r3_proof
    from phase165_r14_r6_generic_iso import MapInjective
    delta_proof, injective_proof, ancestors, _ = build_r2j_r3_proof()
    if delta_proof.rule is not ProofRule.INFERENCE or injective_proof.rule is not ProofRule.INFERENCE:
        raise RuntimeError("R2J-R3 proof roots not inferred")
    if not isinstance(injective_proof.conclusion, MapInjective):
        raise RuntimeError("R2J-R3 injectivity root is ill-typed")
    report = inspect()
    report["r2j_r3_e_injective_inferred"] = True
    report["r2j_r3_delta_zero_inferred"] = True
    report["r2j_r3_ancestry_count"] = len(ancestors)
    report["git_head"] = head
    after = _git("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked worktree changed during R4-R1 audit")
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# Phase 171 R2J-R4-R1 — 拡大の未解決部分の監査", "",
        "- モード: AUDIT_ONLY", f"- HEAD: `{head}`",
        "- R2J-R3 の Delta=0・E 単射: 証明木再構成 PASS",
        "- R2J-R4 の完成証明: 未実施", "",
        "## 既存根拠", "",
    ]
    for key in ("nu_prime_double_source_screened", "nu_prime_hopf_source_screened", "ehp_e_h_window_valid"):
        summary.append(f"- {key}: `{report[key]}`")
    summary.extend(("", "## 残る証明義務", ""))
    summary.extend("- " + item for item in report["open_proof_obligations"])
    summary.extend(("", "原文・DB の記録を完成証明の GIVEN として追加しない。", ""))
    (OUTPUT / "audit.md").write_text("\n".join(summary), encoding="utf-8")
    print("PHASE171_R2J_R4_R1_R3_PROOF=PASS", flush=True)
    print("PHASE171_R2J_R4_R1_DOUBLE_SCREENED=" + str(report["nu_prime_double_source_screened"]), flush=True)
    print("PHASE171_R2J_R4_R1_HOPF_SCREENED=" + str(report["nu_prime_hopf_source_screened"]), flush=True)
    print("PHASE171_R2J_R4_R1_EHP_WINDOW_VALID=" + str(report["ehp_e_h_window_valid"]), flush=True)
    print("PHASE171_R2J_R4_R1_PI52_DB_CANDIDATES=" + str(len(report["pi52_db_candidates"])), flush=True)
    print("PHASE171_R2J_R4_R1_GENERATOR_IMAGE_OPTIONS=" + str(report["suspended_pi52_generator_frontier"]["count"]), flush=True)
    print("PHASE171_R2J_R4_R1_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R1_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R1_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R1_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
