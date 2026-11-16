# Phase 175 R3R7 — 変更したコード・テストの全文

新規コード／テストのみ。既存ファイルに対する置換はない。新規ファイルは下記の相対パスへ追加する。省略記号によるコードの省略はない。

## `phase175_r3r7_lemma54_membership/__init__.py`

```python
"""Phase 175 R3R7: isolated cited Lemma 5.4 even-factor membership audit."""
```

## `phase175_r3r7_lemma54_membership/audit.py`

```python
"""Phase 175 R3R7: read-only isolated source-to-EHP proof-search audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r6_lemma57_general import audit as r3r6
from phase175_r3r7_lemma54_membership.source import verify_lemma54_before_lemma57

PACKAGE = "phase175_r3r7_lemma54_membership"
MARKER = "__PHASE175_R3R7_WORKER__="
ALLOWED_NEW_FILES = frozenset({
    PACKAGE + "/__init__.py",
    PACKAGE + "/source.py",
    PACKAGE + "/rule.py",
    PACKAGE + "/audit.py",
    PACKAGE + "/run.ps1",
    PACKAGE + "/README.md",
    PACKAGE + "/AUDIT_PLAN_JA.md",
    PACKAGE + "/CODE_FULL_JA.md",
    PACKAGE + "/TEST_RESULTS_JA.md",
    PACKAGE + "/tests/__init__.py",
    PACKAGE + "/tests/test_source.py",
    PACKAGE + "/tests/test_rule.py",
    PACKAGE + "/tests/test_audit.py",
})


def verify_lineage(root: Path, previous: dict, checked: dict) -> dict[str, object]:
    """Permit only explicitly named added audit files since the verified R2 run."""
    old = previous.get("preflight", {}).get("head")
    new = checked.get("head")
    if (not isinstance(old, str) or not isinstance(new, str)
            or re.fullmatch(r"[a-f0-9]{40}", old) is None
            or re.fullmatch(r"[a-f0-9]{40}", new) is None
            or r3r6._lineage_git(root, "rev-parse", "HEAD") != new):
        raise RuntimeError("R3R7_INVALID_VERIFIED_HEAD")
    if old == new:
        return {"mode": "SAME_HEAD", "audit_only_paths": [], "r3r7_added_paths": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old, new],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("R3R7_R2_HEAD_NOT_ANCESTOR")
    changes = r3r6._lineage_git(root, "diff", "--name-status", "--no-renames", old, new)
    paths: list[str] = []
    additions: list[str] = []
    for line in changes.splitlines():
        status, tab, path = line.partition("\t")
        if tab != "\t" or status != "A":
            raise RuntimeError("R3R7_NON_AUDIT_CHANGE_IN_LINEAGE")
        if (path.startswith(r3r6.R2_PACKAGE + "/")
                or path in r3r6.R3_LINEAGE_ALLOWED_ADDITIONS
                or path in r3r6.R3R5_ALLOWED_ADDITIONS
                or path in r3r6.R3R6_ALLOWED_ADDITIONS):
            paths.append(path)
        elif path in ALLOWED_NEW_FILES:
            paths.append(path)
            additions.append(path)
        else:
            raise RuntimeError("R3R7_UNKNOWN_LINEAGE_ADDITION: " + path)
    if not paths:
        raise RuntimeError("R3R7_EMPTY_DESCENDANT_DIFF")
    return {
        "mode": "AUDIT_ONLY_DESCENDANT",
        "audit_only_paths": paths,
        "r3r7_added_paths": additions,
    }


def scoped_preflight(root: Path) -> dict[str, object]:
    """Reuse the R3 Source Guard and R2 evidence; extend lineage for this ZIP."""
    from phase175_r3_pi73_hopf_lift import audit as r3

    if r3.R3_LINEAGE_ALLOWED_ADDITIONS != r3r6.R3_LINEAGE_ALLOWED_ADDITIONS:
        raise RuntimeError("R3R7_R3_SOURCE_GUARD_POLICY_CHANGED")
    checked = r3.preflight(root)
    report_file = r3.select_r2_report(None)
    previous = json.loads(report_file.read_text(encoding="utf-8"))
    r3.validate_r2(previous)
    lineage = verify_lineage(root, previous, checked)
    source = verify_lemma54_before_lemma57(root)
    return {
        "r3_source_guard": checked,
        "r2_lineage": lineage,
        "r2_report_path": str(report_file),
        "lemma54_lemma57_source": source,
    }


def latest_successful_r3r6() -> Path:
    """Require the actual preceding normal audit, never its DryRun or notes."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / "phase175_r3r6_lemma57_general"
    for path in sorted(directory.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            data = report.get("worker", {}).get("data", {})
            statuses = {item["name"]: item["status"] for item in data.get("observations", ())}
            if (report.get("phase") == "175-R3R6"
                    and report.get("dry_run") is False
                    and report.get("result") == "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED"
                    and report.get("tracked_unchanged") is True
                    and report.get("new_production_given") == 0
                    and data.get("source_general_given_count") == 1
                    and data.get("particular_nu_prime_given_count") == 0
                    and statuses == {
                        "double_suspension_membership": "UNRESOLVED",
                        "lemma57_zero_generator_image": "UNRESOLVED",
                    }):
                return path
        except (OSError, UnicodeError, KeyError, ValueError, TypeError):
            continue
    raise RuntimeError("R3R7_NO_VERIFIED_R3R6_NORMAL_AUDIT_REPORT")


def inspect_actual_search() -> dict[str, object]:
    """Reconstruct real ProofSteps without a saved result or direct target GIVEN."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase166_r3c_publication_order import precedes_citing_assertion
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase173_r4_r1_lemma54_source_bridge.source import (
        ADOPTED_ASSERTION_ID,
        TodaLemma54TypedSource,
    )
    from phase174_r3_r6_r2_prop44_lemma54.source import attach_earlier_verified_lemma54
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        expand_hopf_injective_from_zero_image,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        expand_zero_image_from_cyclic_generator,
    )
    from phase175_r3_pi73_hopf_lift.frontier import inspect_independent_obligation
    from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
    from phase175_r3r6_lemma57_general.rule import (
        expand_cited_lemma57_zero_generator,
        lemma57_criterion_inputs,
    )
    from phase175_r3r6_lemma57_general.source import (
        GENERAL_ASSERTION_ID,
        TodaLemma57GeneralCriterion,
        build_isolated_lemma57_source,
        merge_isolated_cited_source,
    )
    from phase175_r3r7_lemma54_membership.rule import (
        cited_lemma54_double_relation,
        expand_cited_lemma54_double,
        expand_even_factor_membership,
    )
    from proof import ProofRule, Relation
    from unified_statement_registry import AssertionOrigin

    root = Path(__file__).resolve().parents[1]
    original = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(target, Relation)
            or target.lhs != TodaPrimaryGroup(7, 3)
            or not isinstance(prior, Relation)
            or prior.lhs != TodaPrimaryGroup(6, 2)):
        raise RuntimeError("R3R7_GROUP_GOAL_OR_PI62_PRIOR_INVALID")
    citing = resolve_specialized_goal_citing_id(original, target)
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("R3R7_CITING_ASSERTION_NOT_REGISTERED")
    source_bound = attach_earlier_verified_lemma54(original, citing)
    screened = screen_shared_proof_context(
        source_bound, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    supplement = build_isolated_lemma57_source(root)
    merged = merge_isolated_cited_source(screened, supplement)
    for assertion_id in (ADOPTED_ASSERTION_ID, GENERAL_ASSERTION_ID):
        if assertion_id not in merged.registry._assertions:
            raise RuntimeError("R3R7_REQUIRED_EARLIER_SOURCE_NOT_ADOPTED: " + assertion_id)
        if not precedes_citing_assertion(merged, assertion_id, citing):
            raise RuntimeError("R3R7_CITED_SOURCE_AFTER_GOAL: " + assertion_id)
    available = tuple(
        link.step.conclusion for link in merged.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and merged.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1
            or target in available):
        raise RuntimeError("R3R7_INVALID_SOURCE_LEAVES_OR_TARGET_GIVEN")
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero_generator = GeneratorImage(e, prior.rhs.generator, Zero())
    lemma57_inputs = lemma57_criterion_inputs(zero_generator)
    if lemma57_inputs is None:
        raise RuntimeError("R3R7_TYPED_LEMMA57_TARGET_NOT_MATCHED")
    general, membership = lemma57_inputs
    equation = cited_lemma54_double_relation()
    extracted = expand_cited_lemma54_double(equation, available)
    factors = expand_even_factor_membership(membership, (equation,))
    zero_offers = expand_cited_lemma57_zero_generator(zero_generator, available)
    if (len(extracted) != 1 or len(factors) != 1 or len(zero_offers) != 1
            or extracted[0].subgoals != (TodaLemma54TypedSource(),)
            or factors[0].subgoals != (equation,)
            or zero_offers[0].subgoals != (general, membership)):
        raise RuntimeError("R3R7_TYPED_SOURCE_CHAIN_NOT_OFFERED")
    zero_image = ImageZeroStatement(e)
    bridge_options = expand_zero_image_from_cyclic_generator(zero_image, prior)
    if len(bridge_options) != 1 or bridge_options[0].subgoals != (prior, zero_generator):
        raise RuntimeError("R3R7_CYCLIC_ZERO_IMAGE_BRIDGE_MISSING")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    lift_offers = expand_cited_hopf_lift(cyclic, available)
    if len(lift_offers) != 1:
        raise RuntimeError("R3R7_CITED_HOPF_LIFT_NOT_UNIQUE")
    hopf_injective = lift_offers[0].subgoals[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf_injective)
    if (hopf_inputs is None or hopf_inputs[0] != zero_image
            or len(expand_hopf_injective_from_zero_image(hopf_injective)) != 1):
        raise RuntimeError("R3R7_EHP_EXACTNESS_RULE_UNAVAILABLE")
    ordinary = shared_expansion_provider(merged, proof_target=target)

    def provider(goal: object):
        if goal == equation:
            return extracted + ordinary(goal)
        if goal == membership:
            return factors + ordinary(goal)
        if goal == zero_generator:
            return zero_offers + ordinary(goal)
        if goal == zero_image:
            return bridge_options + ordinary(goal)
        if goal == hopf_injective:
            return expand_hopf_injective_from_zero_image(goal) + ordinary(goal)
        if goal == cyclic:
            return lift_offers + ordinary(goal)
        return ordinary(goal)

    goals = (
        ("lemma54_double_relation", equation),
        ("double_suspension_membership", membership),
        ("lemma57_zero_generator_image", zero_generator),
        ("zero_suspension_image", zero_image),
        ("hopf_injectivity", hopf_injective),
        ("pi73_cyclic_lift", cyclic),
    )
    inspected = [
        inspect_independent_obligation(name, goal, merged, citing, provider)
        for name, goal in goals
    ]
    return {
        "target": repr(target),
        "verified_lemma54_source": True,
        "verified_lemma57_source": True,
        "lemma54_precedes_lemma57": True,
        "new_specific_given": 0,
        "new_production_rules": 0,
        "public_provider_modified": False,
        "literal_equation": repr(equation),
        "membership_goal": repr(membership),
        "offered_source_extraction": len(extracted),
        "offered_generic_factor_rule": len(factors),
        "offered_lemma57_rule": len(zero_offers),
        "observations": inspected,
    }


def worker() -> int:
    """Run isolated canonical search; errors are reported as failed audits."""
    try:
        payload = {"status": "INSPECTED", "data": inspect_actual_search()}
    except Exception as exc:
        payload = {
            "status": "ERROR",
            "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-8000:],
        }
    print(MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def launch_worker(root: Path, seconds: int, folder: Path) -> dict[str, object]:
    """Constrain the expensive proof search in a separate Python process."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--root", str(root), "--worker"],
            cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=seconds, check=False, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8",
    )
    rows = [line[len(MARKER):] for line in completed.stdout.splitlines() if line.startswith(MARKER)]
    if completed.returncode or len(rows) != 1:
        return {"status": "INVALID_WORKER", "code": completed.returncode, "markers": len(rows)}
    try:
        result = json.loads(rows[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return result if isinstance(result, dict) else {"status": "INVALID_WORKER_PAYLOAD"}


def write_report(folder: Path, report: dict) -> None:
    """All outputs are outside the repository and UTF-8 encoded."""
    (folder / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    md = [
        "# Phase 175 R3R7 — Lemma 5.4 double suspension membership", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- No direct theorem GIVEN and no production or Web changes",
        "- Whole-repository pytest not executed", "",
        "## Verified proof-search obligations", "",
    ]
    data = report.get("worker", {}).get("data", {})
    if isinstance(data, dict):
        for item in data.get("observations", ()):
            md.append("- **" + item["name"] + "**: " + item["status"])
            md.append("  - offered routes: " + str(item["offered_routes"]))
            for unresolved in item.get("observed_unresolved", ())[:5]:
                md.append("  - Open Goal: `" + str(unresolved).replace("`", "'") + "`")
    if report.get("error"):
        md.extend(["", "## Failure", "", "`" + str(report["error"]) + "`"])
    (folder / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    """Preflight, fixed-source checks, isolated audit, and postflight guard."""
    root = Path(root).resolve()
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R7", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_specific_given": 0, "production_changes": [], "full_pytest": False,
    }
    preflight = None
    code = 2
    print("PHASE175_R3R7_OUTPUT=" + str(folder), flush=True)
    try:
        preflight = scoped_preflight(root)
        report["preflight"] = preflight
        report["r3r6_report"] = str(latest_successful_r3r6())
        print("PHASE175_R3R7_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R7_LEMMA54_BEFORE_LEMMA57=PASS", flush=True)
        print("PHASE175_R3R7_R3R6_EVIDENCE=PASS", flush=True)
        if dry_run:
            report["result"] = "PASS_R3R7_READ_ONLY_DRYRUN"
            code = 0
        else:
            inspected = launch_worker(root, timeout_seconds, folder)
            report["worker"] = inspected
            if inspected.get("status") != "INSPECTED":
                raise RuntimeError("R3R7_WORKER_FAILED: " + str(inspected))
            data = inspected.get("data")
            if (not isinstance(data, dict)
                    or data.get("verified_lemma54_source") is not True
                    or data.get("verified_lemma57_source") is not True
                    or data.get("new_specific_given") != 0
                    or data.get("new_production_rules") != 0
                    or data.get("public_provider_modified") is not False):
                raise RuntimeError("R3R7_TYPED_SOURCE_POLICY_FAILURE")
            statuses = {item["name"]: item["status"] for item in data["observations"]}
            expected = {
                "lemma54_double_relation", "double_suspension_membership",
                "lemma57_zero_generator_image", "zero_suspension_image",
                "hopf_injectivity", "pi73_cyclic_lift",
            }
            if set(statuses) != expected:
                raise RuntimeError("R3R7_TYPED_PROOF_OBLIGATIONS_MISSING")
            for name, status in statuses.items():
                print("PHASE175_R3R7_" + name.upper() + "=" + status, flush=True)
            if statuses["double_suspension_membership"] != "INFERRED":
                report["result"] = "R3R7_MEMBERSHIP_UNRESOLVED"
                code = 3
            elif statuses["pi73_cyclic_lift"] == "INFERRED":
                report["result"] = "PASS_R3R7_ISOLATED_PI73_CYCLIC_INFERRED"
                code = 0
            else:
                report["result"] = "PASS_R3R7_MEMBERSHIP_INFERRED_PI73_PENDING"
                code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
        report["result"] = "R3R7_REFUSED_OR_WORKER_ERROR"
        print("PHASE175_R3R7_ERROR=" + str(report["error"]), flush=True)
    finally:
        if preflight is not None:
            try:
                report["tracked_unchanged"] = scoped_preflight(root) == preflight
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3R7_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3R7_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R7_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3R7_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    if args.worker:
        return worker()
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## `phase175_r3r7_lemma54_membership/rule.py`

```python
"""Isolated source extraction and degree-generic even-factor membership.

The source extraction is the literal Lemma 5.4 identity, not a new theorem.
The independent mathematical implication works for any typed alpha in pi_i^3:
E^2(alpha) = 2 beta, beta in pi_(i+2)^5, implies the Lemma 5.7 hypothesis.
No result is made a GIVEN by these backward expansions.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import FiniteCyclicGroup
from phase165_r3_recursive_search import GoalExpansion
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase175_r3r6_lemma57_general.rule import TodaLemma57DoubleSuspensionMembership
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)

SOURCE_RULE_NAME = "Toda Lemma 5.4 verified double-suspension clause extraction"
FACTOR_RULE_NAME = "even double-suspension factor implies Lemma 5.7 membership"


def canonical_nu_prime() -> HomotopyElement:
    """Use the already source-registered (5.3) nu-prime representative."""
    return HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )


def cited_lemma54_double_relation() -> Relation:
    """Encode precisely 2 E nu_4 = E^2 nu-prime from Lemma 5.4."""
    nu4 = canonical_hopf_relation().lhs.expression
    nu_prime = canonical_nu_prime()
    return Relation(
        lhs=Multiple(2, IteratedSuspension(nu4, 1)),
        rhs=IteratedSuspension(nu_prime, 2),
        relation_type=RelationType.EQUALITY,
    )


def _same_typed_alpha_identity(left: object, right: object) -> bool:
    """Allow only an identical typed class or a uniquely registered generator ID.

    FiniteCyclicGroup here is an identity-matching wrapper; no group order is
    inferred or used as a theorem by this check.
    """
    if typed_element_span(left) != typed_element_span(right):
        return False
    if left == right:
        return True
    if typed_element_span(left) != (6, 3):
        return False
    return same_registered_group_presentation(
        FiniteCyclicGroup(4, left), FiniteCyclicGroup(4, right),
    )


def lemma54_double_rule(goal: Relation) -> InferenceRule:
    """Require an actual screened Lemma 5.4 GIVEN to extract the cited clause."""
    if goal != cited_lemma54_double_relation():
        raise ValueError("R3R7 Lemma 5.4 double relation does not match source")
    source = TodaLemma54TypedSource()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and cited_lemma54_double_relation() == goal
        )

    return InferenceRule(
        name=SOURCE_RULE_NAME,
        description=(
            "Extract only 2E(nu_4)=E^2(nu-prime) from the independently "
            "screened, full cited Lemma 5.4. No direct group GIVEN."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaLemma54TypedSource,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Lemma 5.4", locator="Lemma 5.4",
        ),
    )


def expand_cited_lemma54_double(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Do not offer an extracted relation without one exact screened source."""
    if (not isinstance(available, tuple)
            or goal != cited_lemma54_double_relation()
            or available.count(TodaLemma54TypedSource()) != 1):
        return ()
    return (GoalExpansion(lemma54_double_rule(goal), (TodaLemma54TypedSource(),)),)


def even_factorization_inputs(
    goal: object, relation: object,
) -> tuple[Relation] | None:
    """Check the general equation E^2(alpha)=2 beta, either direction.

    The formal source must have type pi_i^3 and beta must have type
    pi_(i+2)^5. Only a checked equality, not the assertion of beta's
    existence, supplies this evidence.
    """
    if not isinstance(goal, TodaLemma57DoubleSuspensionMembership):
        return None
    alpha = goal.alpha
    span = typed_element_span(alpha)
    if span is None or span[1] != 3 or span[0] < 3:
        return None
    i = span[0]
    if not isinstance(relation, Relation) or relation.relation_type is not RelationType.EQUALITY:
        return None
    for left, right in ((relation.lhs, relation.rhs), (relation.rhs, relation.lhs)):
        if not (isinstance(left, Multiple) and left.coefficient == 2
                and typed_element_span(left.expression) == (i + 2, 5)
                and isinstance(right, IteratedSuspension)
                and right.exponent == 2
                and _same_typed_alpha_identity(right.expression, alpha)):
            continue
        return (relation,)
    return None


def even_factor_membership_rule(
    goal: TodaLemma57DoubleSuspensionMembership, relation: Relation,
) -> InferenceRule:
    """Make a genuine INFERENCE from the earlier proved doubled equality."""
    required = even_factorization_inputs(goal, relation)
    if required is None:
        raise ValueError("R3R7 invalid double-suspension factorization")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and bool(premises[0].premises)
            and premises[0].conclusion == relation
            and even_factorization_inputs(goal, relation) == required
        )

    return InferenceRule(
        name=FACTOR_RULE_NAME,
        description=(
            "For alpha in pi_i(S^3), a proved equality E^2(alpha)=2 beta "
            "with beta in pi_(i+2)(S^5) gives E^2(alpha) in "
            "2 iota_5 o pi_(i+2)(S^5); the identity iota_5 acts trivially."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=Relation,
            relation_type=RelationType.EQUALITY,
            statement_pattern=relation,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_even_factor_membership(
    goal: object, candidate_relations: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """General backward rule: only concrete, typed factorization candidates."""
    if not isinstance(candidate_relations, tuple):
        return ()
    result: list[GoalExpansion] = []
    for relation in candidate_relations:
        if even_factorization_inputs(goal, relation) is None:
            continue
        if any(existing.subgoals == (relation,) for existing in result):
            continue
        result.append(GoalExpansion(
            even_factor_membership_rule(goal, relation), (relation,),
        ))
    return tuple(result)
```

## `phase175_r3r7_lemma54_membership/run.ps1`

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

$tests = @(
    'phase175_r3r7_lemma54_membership/tests',
    'phase175_r3r6_lemma57_general/tests/test_rule.py',
    'phase175_r3r6_lemma57_general/tests/test_source.py',
    'phase175_r3r5_pi73_lemma57_frontier/tests/test_frontier.py',
    'phase173_r4_r1_lemma54_source_bridge/tests/test_source.py'
)

Write-Output 'PHASE175_R3R7_FOCUSED_PYTEST_START'
& python -B -m pytest -q -p no:cacheprovider @tests
if ($LASTEXITCODE -ne 0) {
    Write-Error 'R3R7 focused pytest failed'
    exit 2
}
Write-Output 'PHASE175_R3R7_FOCUSED_PYTEST=PASS'

$argsList = @(
    '-B', '-m', 'phase175_r3r7_lemma54_membership.audit',
    '--root', $root, '--timeout-seconds', [string]$TimeoutSeconds
)
if ($DryRun) {
    $argsList += '--dry-run'
}
& python @argsList
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R7_EXIT_CODE=$code"
exit $code
```

## `phase175_r3r7_lemma54_membership/source.py`

```python
"""Read-only verification of Toda Lemma 5.4 before Lemma 5.7.

The adopted Chapter V transcription has a pinned reviewed Git blob. The
original printed edition has not been independently checked. No conclusion
about pi_7^3 or E(eta_2 nu-prime) is registered as a GIVEN here.
"""
from __future__ import annotations

import json
from pathlib import Path

from phase173_r4_r1_lemma54_source_bridge.source import (
    DOUBLE_TEXT,
    HOPF_TEXT,
    MEMBERSHIP_TEXT,
    SOURCE_ID as LEMMA54_SOURCE_ID,
    TodaLemma54TypedSource,
    validate_lemma54_text,
)
from phase175_r3r5_pi73_lemma57_frontier.source import verify_reviewed_toda_source
from phase175_r3r6_lemma57_general.source import verify_lemma57_manifest

MANIFEST = Path("phase163_r4_r94_output/manifest.json")
CHAPTER = Path("sources/toda/Toda_05_2.tex")
LEMMA54_SHA256 = "30f72eb36033b069ca814d409d87a4195569c28f50b31501bf3599999e185faa"
LEMMA54_POSITION = 8300
LEMMA57_POSITION = 9100
PROPOSITION58_POSITION = 9200


def verify_lemma54_before_lemma57(root: Path) -> dict[str, object]:
    """Verify the entire existing typed Lemma 5.4, source and citation order."""
    root = Path(root)
    source_evidence = verify_reviewed_toda_source(root)
    source = (root / CHAPTER).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    validate_lemma54_text(source)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8-sig"))
    if manifest.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST":
        raise ValueError("R3R7 unexpected source-manifest mode")
    assertions = manifest.get("assertions")
    if not isinstance(assertions, list):
        raise ValueError("R3R7 source assertions missing")
    expected = (
        ("toda:Lemma 5.4", LEMMA54_SOURCE_ID, LEMMA54_SHA256, LEMMA54_POSITION),
        ("toda:Lemma 5.7", "toda:tex:ch5:0015",
         "01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c",
         LEMMA57_POSITION),
        ("toda:Proposition 5.8", "toda:tex:ch5:0016",
         "4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124",
         PROPOSITION58_POSITION),
    )
    selected: dict[str, dict] = {}
    for reference_id, statement_id, sha256, position in expected:
        matches = [item for item in assertions if item.get("reference_id") == reference_id]
        if len(matches) != 1:
            raise ValueError("R3R7 missing or ambiguous literature reference: " + reference_id)
        row = matches[0]
        if (row.get("statement_id") != statement_id
                or row.get("source_sha256") != sha256
                or row.get("publication_position") != position
                or row.get("review_needed") is not False):
            raise ValueError("R3R7 unreviewed or reordered citation: " + reference_id)
        selected[reference_id] = row
    actual_lemma = selected["toda:Lemma 5.4"]["source_text"]
    validate_lemma54_text(actual_lemma)
    if any(term not in actual_lemma for term in (DOUBLE_TEXT, HOPF_TEXT, MEMBERSHIP_TEXT)):
        raise ValueError("R3R7 Lemma 5.4 double-suspension source clause absent")
    if actual_lemma not in source:
        raise ValueError("R3R7 manifest lemma is not a literal source passage")
    verify_lemma57_manifest(root)
    if not LEMMA54_POSITION < LEMMA57_POSITION < PROPOSITION58_POSITION:
        raise ValueError("R3R7 unexpected literature order")
    return {
        "source_blob": source_evidence["source_blob"],
        "lemma54_statement_id": LEMMA54_SOURCE_ID,
        "lemma54_source_sha256": LEMMA54_SHA256,
        "lemma54_position": LEMMA54_POSITION,
        "lemma57_position": LEMMA57_POSITION,
        "proposition58_position": PROPOSITION58_POSITION,
        "printed_edition_independently_checked": False,
        "new_specific_given": 0,
        "new_production_source": 0,
        "source_statement": repr(TodaLemma54TypedSource()),
    }
```

## `phase175_r3r7_lemma54_membership/tests/__init__.py`

```python
"""Focused, production-dependent R3R7 regression tests."""
```

## `phase175_r3r7_lemma54_membership/tests/test_audit.py`

```python
"""Audit guard regression tests on real temporary Git histories."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import pytest

from phase175_r3r7_lemma54_membership import audit


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def commit(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "-c", "user.name=EHP Audit Test",
        "-c", "user.email=test@example.invalid", "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "baseline.py").write_text("production = 'unchanged'\n", encoding="utf-8")
    start = commit(root, "reviewed source state")
    return root, start


@pytest.mark.parametrize("path", [
    "phase175_r3r6_lemma57_general/rule.py",
    "phase175_r3r7_lemma54_membership/rule.py",
    "phase175_r3r7_lemma54_membership/tests/test_rule.py",
])
def test_only_named_audit_additions_accepted(repo, path: str) -> None:
    root, start = repo
    file = root / path
    file.parent.mkdir(parents=True)
    file.write_text("isolated audit only\n", encoding="utf-8")
    end = commit(root, "add reviewed audit file")
    result = audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})
    assert result["audit_only_paths"] == [path]
    assert result["r3r7_added_paths"] == ([path] if path in audit.ALLOWED_NEW_FILES else [])


@pytest.mark.parametrize("path", [
    "src/core.py",
    "phase175_r3r7_lemma54_membership/unreviewed_rule.py",
    "phase175_r3r6_lemma57_general/secret.py",
])
def test_unknown_addition_rejected(repo, path: str) -> None:
    root, start = repo
    file = root / path
    file.parent.mkdir(parents=True)
    file.write_text("unexpected\n", encoding="utf-8")
    end = commit(root, "unreviewed new file")
    with pytest.raises(RuntimeError, match="R3R7_UNKNOWN_LINEAGE_ADDITION"):
        audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})


def test_modified_production_rejected(repo) -> None:
    root, start = repo
    (root / "baseline.py").write_text("production = 'changed'\n", encoding="utf-8")
    end = commit(root, "modify production")
    with pytest.raises(RuntimeError, match="R3R7_NON_AUDIT_CHANGE_IN_LINEAGE"):
        audit.verify_lineage(root, {"preflight": {"head": start}}, {"head": end})


def test_success_report_required_before_any_audit(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R3R7_NO_VERIFIED_R3R6"):
        audit.latest_successful_r3r6()
    parent = tmp_path / "EHPProofTracerAudit" / "phase175_r3r6_lemma57_general" / "20260101"
    parent.mkdir(parents=True)
    (parent / "report.json").write_text(json.dumps({
        "phase": "175-R3R6", "dry_run": False,
        "result": "PASS_R3R6_GENERAL_LEMMA57_FRONTIER_RECORDED",
        "tracked_unchanged": True, "new_production_given": 0,
        "worker": {"data": {
            "source_general_given_count": 1,
            "particular_nu_prime_given_count": 0,
            "observations": [
                {"name": "double_suspension_membership", "status": "UNRESOLVED"},
                {"name": "lemma57_zero_generator_image", "status": "UNRESOLVED"},
            ],
        }},
    }), encoding="utf-8")
    assert audit.latest_successful_r3r6() == parent / "report.json"
```

## `phase175_r3r7_lemma54_membership/tests/test_rule.py`

```python
"""Test the real typed backward rules, including the proof-parent boundary."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from proof import ProofRule, Relation, RelationType, find_inference_matches_for_rule
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase175_r3r6_lemma57_general.rule import TodaLemma57DoubleSuspensionMembership
from phase175_r3r7_lemma54_membership.rule import (
    FACTOR_RULE_NAME,
    SOURCE_RULE_NAME,
    canonical_nu_prime,
    cited_lemma54_double_relation,
    even_factorization_inputs,
    even_factor_membership_rule,
    expand_cited_lemma54_double,
    expand_even_factor_membership,
    lemma54_double_rule,
)


def test_source_double_relation_uses_true_sphere_degrees() -> None:
    from phase169_r10eq_r1_universal_stable_definition.definition import typed_element_span

    relation = cited_lemma54_double_relation()
    assert relation.relation_type is RelationType.EQUALITY
    assert relation.lhs.coefficient == 2
    assert relation.lhs.expression.exponent == 1
    assert typed_element_span(relation.lhs) == (8, 5)
    assert typed_element_span(relation.rhs) == (8, 5)
    assert relation.rhs.expression == canonical_nu_prime()


def test_source_extraction_requires_unique_cited_given() -> None:
    relation = cited_lemma54_double_relation()
    source = TodaLemma54TypedSource()
    assert expand_cited_lemma54_double(relation, ()) == ()
    assert expand_cited_lemma54_double(relation, (source, source)) == ()
    proposals = expand_cited_lemma54_double(relation, (source,))
    assert len(proposals) == 1
    assert proposals[0].rule.name == SOURCE_RULE_NAME
    assert proposals[0].subgoals == (source,)
    rule = lemma54_double_rule(relation)
    good = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=source)
    wrong = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=source)
    assert rule.match_guard((good,), {}) is True
    assert rule.match_guard((wrong,), {}) is False


def test_inferred_double_equality_yields_membership_without_new_given() -> None:
    relation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    assert even_factorization_inputs(goal, relation) == (relation,)
    options = expand_even_factor_membership(goal, (relation, relation))
    assert len(options) == 1
    assert options[0].subgoals == (relation,)
    assert options[0].rule.name == FACTOR_RULE_NAME
    rule = even_factor_membership_rule(goal, relation)
    given_source = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=TodaLemma54TypedSource())
    inferred_relation = SimpleNamespace(
        rule=ProofRule.INFERENCE, conclusion=relation, premises=(given_source,),
    )
    no_proof = SimpleNamespace(rule=ProofRule.INFERENCE, conclusion=relation, premises=())
    direct_given = SimpleNamespace(rule=ProofRule.GIVEN, conclusion=relation, premises=())
    assert rule.match_guard((inferred_relation,), {}) is True
    assert rule.match_guard((no_proof,), {}) is False
    assert rule.match_guard((direct_given,), {}) is False


def test_accepted_db_alias_uses_registered_identity_not_display_name() -> None:
    db_alias = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(r"\nu'"),
    )
    goal = TodaLemma57DoubleSuspensionMembership(db_alias)
    assert even_factorization_inputs(goal, cited_lemma54_double_relation()) is not None
    spoofed = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol("unregistered-nu-prime"),
    )
    assert even_factorization_inputs(
        TodaLemma57DoubleSuspensionMembership(spoofed),
        cited_lemma54_double_relation(),
    ) is None


def test_wrong_factor_degree_and_non_two_coefficients_rejected() -> None:
    relation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    wrong_factor = HomotopyElement(
        name="ν₄", dimension=4, source=7, target=4,
        generator=GeneratorSymbol("ν", index=4),
    )
    assert even_factorization_inputs(
        goal, replace(relation, lhs=Multiple(2, wrong_factor)),
    ) is None
    assert even_factorization_inputs(
        goal, replace(relation, lhs=Multiple(3, relation.lhs.expression)),
    ) is None
    assert even_factorization_inputs(
        goal, replace(relation, rhs=IteratedSuspension(canonical_nu_prime(), 1)),
    ) is None
    assert even_factorization_inputs(goal, replace(relation, relation_type=RelationType.ORDER)) is None


def test_general_rule_accepts_other_degree_compatible_elements() -> None:
    arbitrary = HomotopyElement(
        name="alpha", dimension=3, source=9, target=3,
        generator=GeneratorSymbol("arbitrary"),
    )
    beta = HomotopyElement(
        name="beta", dimension=5, source=11, target=5,
        generator=GeneratorSymbol("arbitrary_half"),
    )
    relation = Relation(
        IteratedSuspension(arbitrary, 2), Multiple(2, beta),
        RelationType.EQUALITY,
    )
    goal = TodaLemma57DoubleSuspensionMembership(arbitrary)
    assert even_factorization_inputs(goal, relation) == (relation,)
    assert len(expand_even_factor_membership(goal, (relation,))) == 1


def test_actual_inference_matching_refuses_missing_parent() -> None:
    from proof import InferenceRule, ProofStep

    equation = cited_lemma54_double_relation()
    goal = TodaLemma57DoubleSuspensionMembership(canonical_nu_prime())
    given = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    inferred = ProofStep(
        equation, (given,), ProofRule.INFERENCE,
        inference_rule=InferenceRule("test fixture, not a live proof"),
    )
    rule = even_factor_membership_rule(goal, equation)
    assert len(find_inference_matches_for_rule(rule, (inferred,))) == 1
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(
        rule, (ProofStep(equation, (), ProofRule.GIVEN),),
    ) == ()
```

## `phase175_r3r7_lemma54_membership/tests/test_source.py`

```python
"""Pin full Lemma 5.4 source and independent publication ordering."""
from __future__ import annotations

import json

import pytest

from phase173_r4_r1_lemma54_source_bridge.source import (
    DOUBLE_TEXT, HOPF_TEXT, MEMBERSHIP_TEXT,
)
from phase175_r3r7_lemma54_membership import source


def lemma_text() -> str:
    return (
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        + MEMBERSHIP_TEXT + "\n"
        + HOPF_TEXT + ",\\qquad " + DOUBLE_TEXT + ".\n"
        + "\\end{lemma}"
    )


def manifest() -> dict:
    return {
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "assertions": [
            {
                "reference_id": "toda:Lemma 5.4",
                "statement_id": source.LEMMA54_SOURCE_ID,
                "source_sha256": source.LEMMA54_SHA256,
                "publication_position": 8300,
                "review_needed": False,
                "source_text": lemma_text(),
            },
            {
                "reference_id": "toda:Lemma 5.7",
                "statement_id": "toda:tex:ch5:0015",
                "source_sha256": "01ccddfcde701ce0272d6e85226f1620b5c2c7907dc5cf19742fc70fd041c04c",
                "publication_position": 9100,
                "review_needed": False,
                "source_text": "source unit checked separately",
            },
            {
                "reference_id": "toda:Proposition 5.8",
                "statement_id": "toda:tex:ch5:0016",
                "source_sha256": "4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124",
                "publication_position": 9200,
                "review_needed": False,
                "source_text": "source unit checked separately",
            },
        ],
    }


def setup_source(monkeypatch, tmp_path, data: dict) -> None:
    monkeypatch.setattr(source, "verify_reviewed_toda_source", lambda root: {"source_blob": "verified"})
    monkeypatch.setattr(source, "verify_lemma57_manifest", lambda root: {"source": "verified"})
    manuscript = tmp_path / source.CHAPTER
    manuscript.parent.mkdir(parents=True, exist_ok=True)
    manuscript.write_text(lemma_text(), encoding="utf-8")
    report = tmp_path / source.MANIFEST
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def test_all_cited_source_clauses_and_order_required(monkeypatch, tmp_path) -> None:
    setup_source(monkeypatch, tmp_path, manifest())
    result = source.verify_lemma54_before_lemma57(tmp_path)
    assert result["lemma54_position"] == 8300
    assert result["lemma57_position"] == 9100
    assert result["new_specific_given"] == 0


@pytest.mark.parametrize("mutation", [
    "missing", "bad_sha", "bad_order", "needs_review", "missing_double", "duplicate",
])
def test_source_pin_fail_closed(monkeypatch, tmp_path, mutation: str) -> None:
    data = manifest()
    item = data["assertions"][0]
    if mutation == "missing":
        data["assertions"].pop(0)
    elif mutation == "bad_sha":
        item["source_sha256"] = "a" * 64
    elif mutation == "bad_order":
        item["publication_position"] = 9300
    elif mutation == "needs_review":
        item["review_needed"] = True
    elif mutation == "missing_double":
        item["source_text"] = item["source_text"].replace(DOUBLE_TEXT, "REMOVED")
    elif mutation == "duplicate":
        data["assertions"].append(dict(item))
    setup_source(monkeypatch, tmp_path, data)
    with pytest.raises((ValueError, RuntimeError)):
        source.verify_lemma54_before_lemma57(tmp_path)


def test_actual_checkout_sources_are_reviewed() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    evidence = source.verify_lemma54_before_lemma57(root)
    assert evidence["new_specific_given"] == 0
    assert evidence["source_blob"] == "579661138928499ba04a51327f686d9b971b5314"
```

