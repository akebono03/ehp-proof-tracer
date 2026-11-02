"""Read-only audit of typed Toda (5.6) generator-image correspondence.

A structural generator-image match is NOT a ProofStep and NOT a mathematical
proof. The evaluator never registers a GIVEN, manufactures a rule, or changes
public search. It records the exact next proof obligations.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any

from phase173_r4_r3_premise_frontier_audit.audit import (
    REVIEWED_BLOBS as R4_R3_REVIEWED_BLOBS,
    abstract_signature,
    git,
)

REVIEWED_HEAD = "cd93bac8a2e4c08742f7eabc0ba97fda294d20b6"
REVIEWED_BLOBS = {
    **R4_R3_REVIEWED_BLOBS,
    "phase173_r4_r3_premise_frontier_audit/audit.py": "404cf99395fb6d7010f552ef872ac5b4ff7e3502",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "relation_rules.py": "0da057f35b7ebd51b31c247e04bc4b15b1dcff9e",
}
TARGET_DIMENSIONS = (7, 8, 9, 10)
SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def preflight(root: Path, *, remote: bool) -> dict:
    """Refuse unreviewed changes without modifying repository files."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not the repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError(f"unreviewed branch/HEAD: {branch} {head}; expected develop {REVIEWED_HEAD}")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked changes require review")
    for path, blob in REVIEWED_BLOBS.items():
        if not (root / path).is_file() or git(root, "rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("reviewed source blob mismatch: " + path)
    if remote:
        line = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not line or line.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("remote develop differs from reviewed HEAD")
    return {"branch": branch, "head": head, "source_guard": "PASS", "remote_checked": remote}


def _typed_endpoints(value: object) -> tuple[int, int] | None:
    """Return (source, target) for checked compositions and suspensions."""
    from expression import Composition, HomotopyElement, IteratedSuspension

    if isinstance(value, HomotopyElement):
        source, target = value.source, value.target
        if all(type(v) is int for v in (source, target)) and source >= target >= 2:
            return (source, target)
        return None
    if isinstance(value, IteratedSuspension):
        exponent = value.exponent
        if type(exponent) is not int or exponent < 0:
            return None
        inner = _typed_endpoints(value.expression)
        return ((inner[0] + exponent, inner[1] + exponent)
                if inner is not None else None)
    if isinstance(value, Composition):
        left = _typed_endpoints(value.left)
        right = _typed_endpoints(value.right)
        if left is None or right is None or right[1] != left[0]:
            return None
        return (right[0], left[1])
    return None


def _suspend_verified_shape(value: object) -> object | None:
    """Compute the expected *shape* of E(value), never a proved equation.

    Only the exact ν' and typed eta family used by the current four inputs
    are recognized. The operation encodes what suspension functoriality would
    have to prove; it does not discharge that proof obligation.
    """
    from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension

    endpoints = _typed_endpoints(value)
    if endpoints is None:
        return None
    if isinstance(value, Composition):
        left = _suspend_verified_shape(value.left)
        right = _suspend_verified_shape(value.right)
        if left is None or right is None:
            return None
        proposed = Composition(left=left, right=right)
        expected = (endpoints[0] + 1, endpoints[1] + 1)
        return proposed if _typed_endpoints(proposed) == expected else None
    if not isinstance(value, HomotopyElement):
        return None
    symbol = value.generator
    if not isinstance(symbol, GeneratorSymbol):
        return None
    if (value.dimension == 3 and endpoints == (6, 3)
            and (symbol.family == "\\nu'"
                 or (symbol.family == "ν" and symbol.decoration == "′"))):
        return IteratedSuspension(expression=value, exponent=1)
    if (symbol.family == "η" and type(symbol.index) is int
            and symbol.index >= 2 and value.dimension == symbol.index
            and endpoints == (symbol.index + 1, symbol.index)):
        next_index = symbol.index + 1
        return HomotopyElement(
            name="η" + str(next_index).translate(SUBSCRIPT_DIGITS),
            dimension=next_index, source=next_index + 1,
            target=next_index,
            generator=GeneratorSymbol(family="η", index=next_index),
        )
    return None


def _group_components(value: object) -> tuple[object, ...] | None:
    """Extract only a typed cyclic direct sum (or a typed zero group)."""
    from homotopy_groups import (
        DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from proof import Relation, RelationType

    if isinstance(value, TodaPrimaryGroupZeroStatement):
        return ()
    if not isinstance(value, Relation) or value.relation_type is not RelationType.EQUALITY:
        return None
    rhs = value.rhs
    components = rhs.summands if isinstance(rhs, DirectSumGroup) else (rhs,)
    if not components or not all(isinstance(c, (FiniteCyclicGroup, FreeCyclicGroup))
                                 for c in components):
        return None
    return components


def _nu4_composed_image(value: object) -> object | None:
    """Compute the expected symbolic ν4∘γ with checked source and target."""
    from expression import Composition
    from phase173_r4_r1_lemma54_source_bridge.source import canonical_hopf_relation

    nu4 = canonical_hopf_relation().lhs.expression
    gamma_endpoints = _typed_endpoints(value)
    if gamma_endpoints is None or gamma_endpoints[1] != 7:
        return None
    result = Composition(left=nu4, right=value)
    return result if _typed_endpoints(result) == (gamma_endpoints[0], 4) else None


def _map_components(first: object, second: object) -> tuple[object, ...] | None:
    """Build symbolic source images without classifying them as proved."""
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup

    left_components = _group_components(first)
    right_components = _group_components(second)
    if left_components is None or right_components is None:
        return None
    result: list[object] = []
    for component in left_components:
        image = _suspend_verified_shape(component.generator)
        if image is None:
            return None
        result.append(FiniteCyclicGroup(component.order, image)
                      if isinstance(component, FiniteCyclicGroup)
                      else FreeCyclicGroup(image))
    for component in right_components:
        image = _nu4_composed_image(component.generator)
        if image is None:
            return None
        result.append(FiniteCyclicGroup(component.order, image)
                      if isinstance(component, FiniteCyclicGroup)
                      else FreeCyclicGroup(image))
    return tuple(result)


def _exact_multiset_match(expected: tuple[object, ...] | None,
                          actual: tuple[object, ...] | None) -> bool:
    """Match generator expressions and orders, not just abstract group types."""
    if expected is None or actual is None or len(expected) != len(actual):
        return False
    remaining = list(actual)
    for item in expected:
        index = next((j for j, other in enumerate(remaining)
                      if type(other) is type(item) and other == item), None)
        if index is None:
            return False
        remaining.pop(index)
    return not remaining


def _citation_state(bridge: object, goal: object, chapter: str) -> dict:
    """Check publication eligibility; never insert the proposed citation into search."""
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase173_r4_r1_lemma54_source_bridge.source import add_verified_lemma54_source

    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        return {"citing_id": None, "lemma54_eligible": False,
                "reason": "missing_exact_publication_position"}
    try:
        add_verified_lemma54_source(
            bridge, citing_assertion_id=citing_id, chapter=chapter,
        )
    except (ValueError, TypeError, KeyError) as exc:
        return {"citing_id": citing_id, "lemma54_eligible": False,
                "reason": type(exc).__name__ + ": " + str(exc)[:360]}
    return {"citing_id": citing_id, "lemma54_eligible": True,
            "reason": "source_and_order_checked_without_registration"}


def inspect_live(root: Path) -> dict:
    """Inspect i=7 regression and the i=8,9,10 symbolic image frontier."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result,
    )
    from relation_rules import suspension_composition_functoriality_inference_rule

    bridge = build_shared_typed_bridge()
    chapter = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    rule = suspension_composition_functoriality_inference_rule()
    rows: list[dict] = []
    for i in TARGET_DIMENSIONS:
        target = exact_prior_database_result(4, i - 4)
        first = exact_prior_database_result(3, i - 4)
        second = exact_prior_database_result(7, i - 7)
        row: dict[str, Any] = {"i": i, "group": f"pi_{i}^4",
                               "first": f"pi_{i-1}^3", "second": f"pi_{i}^7",
                               "target_db": target is not None,
                               "first_db": first is not None,
                               "second_db": second is not None,
                               "functoriality_rule_name": rule.name,
                               "generator_images_proved": False,
                               "result_is_complete_proof": False}
        if target is None or first is None or second is None:
            row["status"] = "MISSING_TYPED_DATABASE_GOAL"
            rows.append(row)
            continue
        abstract_target = abstract_signature(target)
        abstract_inputs = (abstract_signature(first), abstract_signature(second))
        row["abstract_compatible"] = (
            abstract_target is not None
            and all(item is not None for item in abstract_inputs)
            and tuple(sorted(abstract_inputs[0] + abstract_inputs[1]))
            == tuple(sorted(abstract_target))
        )
        row["first_admitted_db_prior"] = admitted_db_step(
            first, proof_target=target,
        ) is not None
        row["second_admitted_db_prior"] = admitted_db_step(
            second, proof_target=target,
        ) is not None
        if i == 7:
            row["status"] = "PROTECTED_EXISTING_PI74_ROUTE"
            row["existing_pi74_unchanged"] = True
            rows.append(row)
            continue
        generated = _map_components(first, second)
        actual = _group_components(target)
        matched = _exact_multiset_match(generated, actual)
        row["symbolic_generator_match"] = matched
        row["expected_components"] = [str(c) for c in generated] if generated is not None else []
        row["registered_components"] = [str(c) for c in actual] if actual is not None else []
        row["citation"] = _citation_state(bridge, target, chapter)
        row["status"] = (
            "SYNTACTIC_MATCH_UNPROVED" if matched
            else "MISSING_GENERATOR_NORMALIZATION_OR_SOURCE"
        )
        rows.append(row)
    return {"scope": "n4 i=7..10", "rows": rows,
            "no_inference_steps_generated": True,
            "no_source_promoted_to_given": True}


def write_report(output: Path, report: dict) -> None:
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = ["# Phase 173 R4-R4 — 型付き生成元像の監査", "",
             "構造的な生成元像の一致は証明完了を意味しない。", "",
             "| 群 | 抽象構造 | 生成元像 | DB先行結果（2群） | 引用の位置 | 判定 |",
             "|---|---|---|---|---|---|"]
    for row in report.get("observation", {}).get("rows", []):
        citation = row.get("citation", {})
        lines.append(
            f"| {row['group']} | {row.get('abstract_compatible', 'N/A')} | "
            f"{row.get('symbolic_generator_match', '既存経路')} | "
            f"{row.get('first_admitted_db_prior')}, {row.get('second_admitted_db_prior')} | "
            f"{citation.get('lemma54_eligible', '未検査')} | {row['status']} |"
        )
    lines += ["", "具体的な生成元式・未証明の前提は audit.json を参照。", ""]
    (output / "audit.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path, *, dry_run: bool, remote: bool) -> int:
    base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
    output = base / ("phase173_r4_r4_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    output.mkdir(parents=True, exist_ok=False)
    report: dict = {"phase": "173 R4-R4", "mode": "AUDIT_ONLY",
                    "reviewed_head": REVIEWED_HEAD, "dry_run": dry_run,
                    "production_modified": False, "full_pytest": False,
                    "result": "NOT_STARTED", "output": str(output)}
    result_code = 2
    before = None
    print("PHASE173_R4_R4_OUTPUT=" + str(output), flush=True)
    try:
        before = preflight(root, remote=remote)
        report["preflight"] = before
        if dry_run:
            report["result"] = "DRY_RUN_PASS"
        else:
            report["observation"] = inspect_live(root)
            for row in report["observation"]["rows"]:
                print(f"PHASE173_R4_R4_{row['group']} "
                      f"STATUS={row['status']} "
                      f"ABSTRACT={row.get('abstract_compatible')} "
                      f"GENERATOR_MATCH={row.get('symbolic_generator_match')} "
                      f"LEMMA54={row.get('citation', {}).get('lemma54_eligible')}",
                      flush=True)
            if len(report["observation"]["rows"]) != len(TARGET_DIMENSIONS):
                raise RuntimeError("missing source groups in typed audit")
            report["result"] = "OBSERVATION_COMPLETE"
        result_code = 0
    except Exception as exc:
        report["result"] = "REFUSED_OR_ERROR"
        report["error"] = f"{type(exc).__name__}: {exc}"
        print("PHASE173_R4_R4_ERROR=" + report["error"], flush=True)
    finally:
        if before is not None:
            try:
                after = preflight(root, remote=False)
                report["tracked_unchanged"] = (
                    {key: value for key, value in before.items() if key != "remote_checked"}
                    == {key: value for key, value in after.items() if key != "remote_checked"}
                )
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)[:800]
            if report["tracked_unchanged"] is False:
                report["result"] = "TRACKED_STATE_CHANGED"
                result_code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(output, report)
        print("PHASE173_R4_R4_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE173_R4_R4_RESULT=" + report["result"], flush=True)
        print("PHASE173_R4_R4_REPORT=" + str(output / "audit.json"), flush=True)
    return result_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), dry_run=args.dry_run,
               remote=not args.skip_remote_check)


if __name__ == "__main__":
    raise SystemExit(main())
