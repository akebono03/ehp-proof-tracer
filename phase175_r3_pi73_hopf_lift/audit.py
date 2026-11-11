"""Phase 175 R3: source-first, isolated pi_7^3 Hopf cyclic-lift search.

No production files, existing rules, source leaves, or web output are modified.
An independent root inference remains unproved until the canonical search
reconstructs every required premise from earlier screened sources.
"""
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

from phase175_r2_k4_frontier_audit.audit import preflight as r2_preflight

PACKAGE = "phase175_r3_pi73_hopf_lift"
WORKER_MARKER = "__PHASE175_R3_PI73_WORKER__="
R2_PACKAGE = "phase175_r2_k4_frontier_audit"
EXTRA_PINS = {
    "phase171_r2i_eta_hopf_bridge/source.py": "4a15d33964f0c87edfe3e7f8337c720c04d17e91",
    "phase171_r2j_r2_cyclic_hopf_surjective/source.py": "ebe53bc49872bd12b8c6eb0649e853726d7d45fe",
    "phase168_r2_8_4_generic_specialization/specialization.py": "9c5c986cd17b11d484442dbb81653d277c0e1ae1",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r12_r24_web_search_connection.py": "71d0c6c365a46e833a2bfe304c771d2e010178ca",
}


def git(root: Path, *arguments: str) -> str:
    """Read only Git; do not modify the checkout or its index."""
    process = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R3_GIT_FAILED: " + " ".join(arguments))
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    """Reuse R2's tested guard and pin the R3 proof-search dependencies."""
    checked = r2_preflight(root)
    for relative, expected in EXTRA_PINS.items():
        if not (root / relative).is_file():
            raise RuntimeError("R3_SOURCE_MISSING: " + relative)
        if git(root, "rev-parse", "HEAD:" + relative) != expected:
            raise RuntimeError("R3_SOURCE_PIN_MISMATCH: " + relative)
    return {**checked, "r3_extra_pins": dict(EXTRA_PINS)}


def validate_r2(report: dict[str, object]) -> None:
    """Require actual completed R2 screening; a DryRun cannot authorize R3."""
    if (not isinstance(report, dict)
            or report.get("phase") != "175-R2"
            or report.get("mode") != "READ_ONLY_FRONTIER_AUDIT"
            or report.get("dry_run") is not False
            or report.get("result") != "PASS_R2_SOURCE_FRONTIER_RECORDED"
            or report.get("tracked_unchanged") is not True
            or report.get("production_changes") != []
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("full_pytest_executed") is not False):
        raise RuntimeError("R3_R2_EVIDENCE_REJECTED")
    worker = report.get("source_worker")
    data = worker.get("data") if isinstance(worker, dict) else None
    source73 = data.get("pi_7_3") if isinstance(data, dict) else None
    root_status = report.get("r1_root_status")
    if (not isinstance(worker, dict)
            or worker.get("status") != "PASS_SOURCE_INVENTORY"
            or not isinstance(source73, dict)
            or source73.get("printed_prop58_checked") is not True
            or source73.get("typed_relation_matches_db") is not True
            or source73.get("source_is_independent_complete_proof") is not False
            or not isinstance(root_status, list)
            or len(root_status) != 3
            or root_status[0].get("group") != "pi_7^3"
            or root_status[0].get("status") != "search_failed"
            or root_status[0].get("proven_steps") != 0):
        raise RuntimeError("R3_R2_PI73_SOURCE_OR_GAP_CHANGED")
    before = report.get("preflight")
    if not isinstance(before, dict) or before.get("branch") != "develop":
        raise RuntimeError("R3_R2_SOURCE_CONTEXT_MISSING")


def select_r2_report(explicit: Path | None) -> Path:
    """Choose the latest valid normal R2 audit; never use guessed evidence."""
    if explicit is not None:
        if not explicit.is_file():
            raise RuntimeError("R3_R2_REPORT_NOT_FOUND")
        return explicit.resolve()
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / R2_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_r2(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (RuntimeError, ValueError, OSError, UnicodeError, json.JSONDecodeError):
            continue
    raise RuntimeError("R3_NO_VALID_R2_EVIDENCE")


def verify_lineage(root: Path, report: dict[str, object], checked: dict[str, object]) -> dict[str, object]:
    """Allow only new R2 audit files between the R2 result and this HEAD."""
    old = report["preflight"].get("head")
    new = checked.get("head")
    if (type(old) is not str or type(new) is not str
            or re.fullmatch(r"[0-9a-f]{40}", old) is None
            or re.fullmatch(r"[0-9a-f]{40}", new) is None):
        raise RuntimeError("R3_UNVERIFIED_GIT_HEAD")
    if old == new:
        return {"mode": "SAME_HEAD", "audit_only_paths": []}
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", old, new],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("R3_R2_HEAD_NOT_ANCESTOR")
    changes = git(root, "diff", "--name-status", "--no-renames", old, new)
    rows = [line.split("\t", 1) for line in changes.splitlines()]
    if (not rows or any(
            len(row) != 2 or row[0] != "A"
            or not row[1].startswith(R2_PACKAGE + "/")
            for row in rows)):
        raise RuntimeError("R3_R2_LINEAGE_NOT_AUDIT_ONLY")
    return {"mode": "AUDIT_ONLY_DESCENDANT", "audit_only_paths": [row[1] for row in rows]}


def inspect_pi73() -> dict[str, object]:
    """Attempt isolated canonical proof reconstruction using no synthetic facts."""
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r3_pi73_hopf_lift.rule import RULE_NAME, expand_cited_hopf_lift, hopf_lift_inputs
    from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
    from phase171_r2j_r2_cyclic_hopf_surjective.source import _same_generator
    from phase168_r2_8_4_generic_specialization.specialization import (
        specialize_registered_higher_stem,
    )
    from phase170_r3_r6_prop58_source import _source_checked_pi73_relation
    from proof import ProofRule, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    bridge = build_shared_typed_bridge()
    target = exact_prior_database_result(3, 4)
    if (not isinstance(target, Relation)
            or target.lhs != TodaPrimaryGroup(7, 3)
            or target.relation_type is not RelationType.EQUALITY
            or not isinstance(target.rhs, FiniteCyclicGroup)
            or target.rhs.order != 2
            or _source_checked_pi73_relation(bridge) != target):
        raise RuntimeError("R3_TYPED_PI73_GOAL_CHANGED")
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if not isinstance(citing, str) or not citing:
        raise RuntimeError("R3_PI73_CITING_ASSERTION_MISSING")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    )
    if target in available:
        raise RuntimeError("R3_TARGET_CLAIM_ADMITTED_AS_GIVEN")
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    chains = eligible_eta_hopf_chains(available)
    exact_chain_names = sum(
        chain.conclusion.lhs.expression == cyclic.generator for chain in chains
    )
    id_checked_chains = tuple(
        chain for chain in chains
        if _same_generator(
            cyclic.generator, chain.conclusion.lhs.expression, cyclic.order,
        )
    )
    # The EHP Hopf codomain is S^(2*n-1); inspect only preceding schemas.
    codomain_schemata = tuple(
        specialized for statement in available if isinstance(statement, Relation)
        for specialized in (specialize_registered_higher_stem(
            statement, 2 * cyclic.group.sphere_dimension - 1,
        ),)
        if specialized is not None
        and specialized.lhs == TodaPrimaryGroup(
            cyclic.group.group_dimension, 2 * cyclic.group.sphere_dimension - 1,
        )
        and isinstance(specialized.rhs, FiniteCyclicGroup)
        and specialized.rhs.order == cyclic.order
    )
    source_pair_matches = sum(
        hopf_lift_inputs(cyclic, schema, chain.conclusion) is not None
        for chain in id_checked_chains for schema in codomain_schemata
    )
    isolated = expand_cited_hopf_lift(cyclic, available)
    if len(isolated) > 1:
        raise RuntimeError("R3_AMBIGUOUS_CITED_HOPF_CHAINS")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    baseline_root_routes = ordinary(cyclic)

    def provider(goal: object):
        if goal == cyclic and isolated:
            return isolated + tuple(option for option in ordinary(goal)
                                    if option.rule.name != RULE_NAME)
        return ordinary(goal)

    result = search_registered_partial_proof(
        n=3, k=4, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference_publication",
    )
    observed_status = result.status.value
    complete = result.status is ProofSearchStatus.COMPLETE and result.conclusion == target
    trust_verified = False
    trust_error = None
    if complete:
        try:
            verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing,
            )
            trust_verified = True
        except Exception as exc:
            trust_error = type(exc).__name__ + ": " + str(exc)
    actual_steps = list(result.proven_steps)
    matches = [
        step for step in actual_steps
        if step.rule is ProofRule.INFERENCE
        and step.conclusion == cyclic
        and getattr(getattr(step, "inference_rule", None), "name", None) == RULE_NAME
    ]
    if matches and any(len(step.premises) != 3 for step in matches):
        raise RuntimeError("R3_HOPF_LIFT_INVALID_PREMISE_COUNT")
    forbidden = [
        repr(step.conclusion) for step in actual_steps
        if step.rule is ProofRule.GIVEN and step.conclusion == target
    ]
    if forbidden:
        raise RuntimeError("R3_TARGET_CONCLUSION_HAS_GIVEN_LEAF")
    candidate_inputs = [repr(item) for item in isolated[0].subgoals] if isolated else []
    zero_image_route_counts = []
    if isolated:
        injectivity_goal = isolated[0].subgoals[0]
        if not isinstance(injectivity_goal, MapInjective):
            raise RuntimeError("R3_HOPF_INJECTIVITY_NOT_TYPED")
        zero_image_route_counts = [
            {"rule": option.rule.name, "subgoals": [repr(x) for x in option.subgoals]}
            for option in ordinary(injectivity_goal)[:15]
        ]
    return {
        "registered_goal": repr(target),
        "screened_fixed_leaves_count": len(available),
        "target_direct_given_excluded": target not in available,
        "hopf_lift_candidate_count": len(isolated),
        "cited_hopf_chain_count": len(chains),
        "exact_generator_spelling_matches": exact_chain_names,
        "registered_generator_identity_matches": len(id_checked_chains),
        "earlier_codomain_schema_count": len(codomain_schemata),
        "source_pair_matches": source_pair_matches,
        "hopf_lift_premises": candidate_inputs,
        "injectivity_routes": zero_image_route_counts,
        "prior_cyclic_routes": len(baseline_root_routes),
        "isolated_search_status": observed_status,
        "isolated_proven_step_count": len(actual_steps),
        "isolated_open_goals": [repr(item)[:1400] for item in result.open_goals[:30]],
        "isolated_diagnostics": [str(x)[:1200] for x in result.diagnostics[:15]],
        "isolated_root_complete": complete,
        "isolated_trust_verified": trust_verified,
        "isolated_trust_error": trust_error,
        "certified_hopf_lift_steps": len(matches),
        "new_given": 0,
        "new_production_rules": 0,
        "public_search_modified": False,
        "public_web_complete_claimed": False,
    }


def worker() -> int:
    """Separate potentially expensive source-first proof attempt from report IO."""
    try:
        payload = {"status": "INSPECTED", "data": inspect_pi73()}
    except Exception as exc:
        payload = {
            "status": "WORKER_ERROR", "error": type(exc).__name__ + ": " + str(exc),
            "traceback": traceback.format_exc()[-7000:],
        }
    print(WORKER_MARKER + json.dumps(payload, ensure_ascii=False), flush=True)
    return 0


def launch_worker(root: Path, seconds: int, folder: Path) -> dict[str, object]:
    """Bound runtime and save all worker diagnostics outside the checkout."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        proc = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker", "--root", str(root)],
            cwd=root, env=env, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        output = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
        (folder / "worker.log").write_text(output, encoding="utf-8")
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(proc.stdout + "\nSTDERR:\n" + proc.stderr, encoding="utf-8")
    markers = [line[len(WORKER_MARKER):] for line in proc.stdout.splitlines()
               if line.startswith(WORKER_MARKER)]
    if proc.returncode or len(markers) != 1:
        return {"status": "INVALID_WORKER", "exit_code": proc.returncode,
                "markers": len(markers)}
    try:
        payload = json.loads(markers[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_JSON"}
    return payload if isinstance(payload, dict) else {"status": "INVALID_PAYLOAD"}


def write_report(folder: Path, report: dict[str, object]) -> None:
    """Write complete immutable JSON and a compact Japanese mathematical summary."""
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    if "worker" not in report or report["worker"].get("status") != "INSPECTED":
        return
    observed = report["worker"]["data"]
    lines = [
        "# Phase 175 R3 — $\\pi_7^3$ の Hopf 生成元逆像監査", "",
        "Toda Proposition 5.8 の $\\pi_7^3$ 自体を GIVEN にしない。", "",
        "$$H:\\pi_7^3\\to\\pi_7^5,\\quad H(\\nu'\\eta_6)=\\eta_5^2,$$", "",
        "$$\\pi_7^5=\\mathbb Z/2\\{\\eta_5^2\\}$$", "",
        "$H$ 単射と上記2つの独立した INFERENCE から", "",
        "$$\\pi_7^3=\\mathbb Z/2\\{\\nu'\\eta_6\\}$$", "",
        "を一般推論として提案する。", "",
        f"- Screened source GIVEN count: {observed['screened_fixed_leaves_count']}",
        f"- Hopf-lift proposal count: {observed['hopf_lift_candidate_count']}",
        f"- Cited Hopf chains: {observed['cited_hopf_chain_count']}",
        f"- Exact generator spelling matches: {observed['exact_generator_spelling_matches']}",
        f"- HyoujiGen ID matches: {observed['registered_generator_identity_matches']}",
        f"- Earlier cyclic codomain schemas: {observed['earlier_codomain_schema_count']}",
        f"- Complete source-pair matches: {observed['source_pair_matches']}",
        f"- Isolated proof search: `{observed['isolated_search_status']}`",
        f"- Certified Hopf-lift roots: {observed['certified_hopf_lift_steps']}",
        f"- Isolated Trust Boundary: {observed['isolated_trust_verified']}",
        "- Public provider: unchanged", "- Full pytest: not run", "",
        "## 実際の Open Goals", "",
    ]
    lines += ["- `" + item.replace("`", "'") + "`" for item in observed["isolated_open_goals"]]
    if not observed["isolated_open_goals"]:
        lines.append("- なし")
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, r2_path: Path | None, timeout_seconds: int) -> int:
    """Require R2 evidence, then attempt the actual isolated Hopf route."""
    local = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = local / "EHPProofTracerAudit" / PACKAGE / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3", "mode": "ISOLATED_PI73_HOPF_LIFT",
        "dry_run": dry_run, "production_changes": [],
        "new_given": 0, "public_provider_changed": False,
        "full_pytest_executed": False, "result": "NOT_STARTED",
    }
    checked = None
    code = 2
    print("PHASE175_R3_OUTPUT=" + str(folder), flush=True)
    try:
        checked = preflight(root)
        report["preflight"] = checked
        r2_report_path = select_r2_report(r2_path)
        previous = json.loads(r2_report_path.read_text(encoding="utf-8"))
        validate_r2(previous)
        lineage = verify_lineage(root, previous, checked)
        report["r2_report"] = str(r2_report_path)
        report["lineage"] = lineage
        print("PHASE175_R3_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3_R2_EVIDENCE=PASS", flush=True)
        print("PHASE175_R3_R2_LINEAGE=" + lineage["mode"], flush=True)
        if dry_run:
            report["result"] = "PASS_R3_READ_ONLY_DRYRUN"
            code = 0
        else:
            result = launch_worker(root, timeout_seconds, folder)
            report["worker"] = result
            if result.get("status") != "INSPECTED":
                raise RuntimeError("R3_HOPF_WORKER_NOT_VERIFIED: " + str(result))
            data = result["data"]
            if data["target_direct_given_excluded"] is not True:
                raise RuntimeError("R3_FORBIDDEN_TARGET_GIVEN")
            print("PHASE175_R3_HOPF_LIFT_CANDIDATES=" + str(data["hopf_lift_candidate_count"]), flush=True)
            print("PHASE175_R3R1_CITED_HOPF_CHAINS=" + str(data["cited_hopf_chain_count"]), flush=True)
            print("PHASE175_R3R1_EXACT_GENERATOR_MATCHES=" + str(data["exact_generator_spelling_matches"]), flush=True)
            print("PHASE175_R3R1_REGISTERED_ID_MATCHES=" + str(data["registered_generator_identity_matches"]), flush=True)
            print("PHASE175_R3R1_CODOMAIN_SCHEMAS=" + str(data["earlier_codomain_schema_count"]), flush=True)
            print("PHASE175_R3R1_SOURCE_PAIR_MATCHES=" + str(data["source_pair_matches"]), flush=True)
            print("PHASE175_R3_SEARCH_STATUS=" + data["isolated_search_status"], flush=True)
            print("PHASE175_R3_ISOLATED_COMPLETE=" + str(data["isolated_root_complete"]), flush=True)
            print("PHASE175_R3_ISOLATED_TRUST=" + str(data["isolated_trust_verified"]), flush=True)
            print("PHASE175_R3_PUBLIC_PROVIDER_MODIFIED=False", flush=True)
            if (data["isolated_root_complete"]
                    and data["isolated_trust_verified"]
                    and data["certified_hopf_lift_steps"] == 1):
                report["result"] = "PASS_R3_PI73_ISOLATED_VERIFIED"
            else:
                report["result"] = "PASS_R3_PI73_HOPF_FRONTIER_RECORDED"
            code = 0
    except Exception as exc:
        report["result"] = "R3_REFUSED_OR_WORKER_ERROR"
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
        print("PHASE175_R3_ERROR=" + report["error"], flush=True)
        code = 2
    finally:
        if checked is not None:
            try:
                report["tracked_unchanged"] = preflight(root) == checked
            except Exception as exc:
                report["tracked_unchanged"] = False
                report["postflight_error"] = str(exc)
            if report["tracked_unchanged"] is not True:
                report["result"] = "R3_TRACKED_STATE_CHANGED"
                code = 2
        else:
            report["tracked_unchanged"] = None
        write_report(folder, report)
        print("PHASE175_R3_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3_TRACKED_UNCHANGED=" + str(report["tracked_unchanged"]), flush=True)
        print("PHASE175_R3_GATE=" + report["result"], flush=True)
        print("(END)", flush=True)
    return code


def main() -> int:
    """Command-line entrypoint for dry-run, live audit, and isolated worker."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--r2-report", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("positive timeout required")
    if args.worker:
        return worker()
    return run(args.root.resolve(), args.dry_run, args.r2_report, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
