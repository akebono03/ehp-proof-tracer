"""Phase 175 R4R10: source-first cited (5.8) + Prop 2.5 public wiring.

Only the full shared bridge/provider functions are changed. No direct pi_9^5
conclusion is registered. A real proof replay is limited to the source-backed
Delta-composition statement, not the target homotopy group.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r4r10_cited_58_prop25_public import installer
from phase175_r4r10_cited_58_prop25_public.source import (
    EQUATION_REFERENCE_ID,
    PROPOSITION_REFERENCE_ID,
    build_cited_58_prop25_sources,
    canonical_toda58,
    source_positions,
)

PACKAGE = "phase175_r4r10_cited_58_prop25_public"
PRIOR_PACKAGE = "phase175_r4r8_signed_delta_kernel_frontier"
PRIOR_GATE = "PASS_R4R8_SIGNED_DELTA_KERNEL_FRONTIER_RECORDED_NOT_PUBLIC"
DRY_GATE = "PASS_R4R10_CITED_58_PROP25_DRYRUN"
FINAL_GATE = "PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING"
BASE_HEAD = "51f9907ac3116c78778d75864775d30d095efa5c"
R4R8_HEAD = "5c263cc69dc409842d3a13cb3fc65c2347df0bef"
REVIEWED_BLOBS = {
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "phase175_r4r7_prop25_typed_composition/rule.py": "e957752baf93f75352d106e53205730af9a02b4d",
    "phase165_r12_r20_eta_definition.py": "9d7058607c102c47265a192735180cac36321910",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(root: Path, *args: str, allowed_failure: bool = False) -> tuple[int, str]:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode and not allowed_failure:
        raise RuntimeError("R4R10_GIT_FAILED: " + " ".join(args) + " " + process.stderr.strip())
    return process.returncode, process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R10_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R10_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    if git(root, "merge-base", "--is-ancestor", BASE_HEAD, head, allowed_failure=True)[0]:
        raise RuntimeError("R4R10_UNREVIEWED_HEAD_ANCESTRY")
    paths = git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines()
    if any(not (path.startswith("phase175_r4r8_signed_delta_kernel_frontier/")
                or path.startswith("phase175_r4r9_general_cyclic_kernel_isolated/")
                or path == ".pytest_cache/v/cache/nodeids") for path in paths):
        raise RuntimeError("R4R10_UNREVIEWED_COMMITTED_PATHS: " + repr(paths))
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path)[1] != expected:
            raise RuntimeError("R4R10_SOURCE_BLOB_DRIFT: " + path)
    target, before, after, _ = installer.plan(root)
    tracked = set(git(root, "diff", "--name-only")[1].splitlines())
    tracked.update(git(root, "diff", "--cached", "--name-only")[1].splitlines())
    if any(path not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for path in tracked):
        raise RuntimeError("R4R10_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(tracked)))
    if installer.TARGET.as_posix() in tracked and before != after:
        raise RuntimeError("R4R10_PRODUCTION_DIRTY_NOT_INSTALLED")
    return {
        "head": head,
        "reviewed_base_head": BASE_HEAD,
        "reviewed_r4r8_head": R4R8_HEAD,
        "intervening_paths": sorted(paths),
        "source_blob_pins_checked": len(REVIEWED_BLOBS),
        "production_patch_already_applied": before == after,
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R10_R4R8_REPORT_INVALID")
    expected = {
        "phase": "175-R4R8",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(k) != v for k, v in expected.items()):
        raise RuntimeError("R4R10_R4R8_REPORT_SCOPE_INVALID")
    groups = report.get("groups")
    obligations = report.get("unresolved_obligations")
    if (not isinstance(groups, dict)
            or groups.get("prior_presentations_identified") != 2
            or groups.get("group_presentations_do_not_certify_E_actions") is not True
            or not isinstance(obligations, list)
            or len(obligations) != 6):
        raise RuntimeError("R4R10_R4R8_REPORT_EVIDENCE_INVALID")
    return {
        "prior_gate": PRIOR_GATE,
        "prior_unresolved_obligations": len(obligations),
        "prior_math_proofs_not_adopted": True,
    }


def find_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        found = explicit.expanduser().resolve()
        if not found.is_file():
            raise RuntimeError("R4R10_R4R8_REPORT_NOT_FOUND: " + str(found))
        return found
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    failed = []
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            failed.append(str(candidate) + " => " + str(exc))
    raise RuntimeError(
        "R4R10_SUCCESSFUL_R4R8_REPORT_MISSING: " + str(folder)
        + ("; " + " | ".join(failed[:3]) if failed else "")
    )


def sample_delta_eta9():
    """Construct only a typed *query*, not a verified result or proof."""
    from expression import Composition, GeneratorSymbol, HomotopyElement
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from toda_rules import TodaDeltaImageUpToSignStatement
    signed = canonical_toda58()
    beta = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = HomotopyElement("η₉", 9, 10, 9, GeneratorSymbol("η", index=9))
    return TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(signed.positive_value, beta),
    )


def replay_cited_prop25() -> dict[str, object]:
    """Replay only the separately cited source route with typed ProofSteps."""
    from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
    from phase165_r12_r20_eta_definition import build_cited_eta_family_definition
    from phase175_r4r10_cited_58_prop25_public.provider import (
        build_cited_58_prop25_provider,
    )
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    source = build_cited_58_prop25_sources()
    eta = build_cited_eta_family_definition(
        Path(__file__).resolve().parents[1] / "sources" / "toda" / "Toda_05_2.tex",
    )
    registry = UnifiedStatementRegistry()
    for bridge in (source, eta):
        for ref in bridge.registry._references.values():
            registry.add_reference(ref)
        for assertion in bridge.registry._assertions.values():
            registry.add_assertion(assertion)
    combined = RegistryBridgeResult(
        registry, (), source.proof_links + eta.proof_links,
    )
    expand = build_cited_58_prop25_provider(combined)
    goal = sample_delta_eta9()
    proposals = expand(goal)
    if len(proposals) != 1 or len(proposals[0].subgoals) != 3:
        raise RuntimeError("R4R10_CITED_PROP25_NOT_EXPOSED")
    prop, signed, identity = proposals[0].subgoals
    source_givens = {type(link.step.conclusion): link.step
                     for link in combined.proof_links if link.step is not None}
    from phase175_r4r10_cited_58_prop25_public.source import CitedToda58SignedDelta, CitedTodaProp25
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    def inferred(subgoal: object, premise):
        opts = expand(subgoal)
        if len(opts) != 1:
            raise RuntimeError("R4R10_PARENTS_NOT_EXPOSED: " + repr(subgoal))
        matches = find_inference_matches_for_rule(opts[0].rule, (premise,))
        if len(matches) != 1:
            raise RuntimeError("R4R10_PARENTS_NOT_MATCHED")
        return apply_inference_match(matches[0])
    signed_step = inferred(signed, source_givens[CitedToda58SignedDelta])
    identity_step = inferred(identity, source_givens[TodaEtaFamilyGeneralDefinition])
    matches = find_inference_matches_for_rule(
        proposals[0].rule,
        (source_givens[CitedTodaProp25], signed_step, identity_step),
    )
    if len(matches) != 1:
        raise RuntimeError("R4R10_PROP25_NOT_MATCHED")
    final = apply_inference_match(matches[0])
    if (final.rule is not ProofRule.INFERENCE or final.conclusion != goal
            or len(final.premises) != 3
            or signed_step.rule is not ProofRule.INFERENCE
            or identity_step.rule is not ProofRule.INFERENCE):
        raise RuntimeError("R4R10_REPLAY_NOT_VERIFIED")
    return {
        "conclusion_is_signed": True,
        "proposition_2_5_citation_present": True,
        "equation_5_8_citation_present": True,
        "eta_family_citation_present": True,
        "signed_parent_inferred": True,
        "composition_identity_parent_inferred": True,
        "root_group_conclusion_inferred": False,
        "full_search_performed": False,
    }


def inspect_public_connection() -> dict[str, object]:
    """Verify all three real backward routes in the default shared registry."""
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase175_r4r10_cited_58_prop25_public.provider import (
        CITED_PROP25_RULE, ETA_IDENTITY_RULE, SOURCE58_RULE,
        screened_cited_facts,
    )
    from phase175_r4r10_cited_58_prop25_public.source import (
        CitedToda58SignedDelta, CitedTodaProp25,
    )
    bridge = build_shared_typed_bridge()
    facts = screened_cited_facts(bridge)
    if (sum(type(x) is CitedToda58SignedDelta for x in facts) != 1
            or sum(type(x) is CitedTodaProp25 for x in facts) != 1
            or facts.count(TodaEtaFamilyGeneralDefinition()) != 1):
        raise RuntimeError("R4R10_PUBLIC_CITED_SOURCES_NOT_SCREENED")
    expand = shared_expansion_provider(bridge)
    proposals = expand(sample_delta_eta9())
    selected = tuple(option for option in proposals
                     if option.rule.name == CITED_PROP25_RULE
                     and len(option.subgoals) == 3)
    if len(selected) != 1:
        raise RuntimeError("R4R10_PUBLIC_PROP25_EXPANSION_NOT_CONNECTED")
    _, signed, identity = selected[0].subgoals
    if (not any(item.rule.name == SOURCE58_RULE for item in expand(signed))
            or not any(item.rule.name == ETA_IDENTITY_RULE for item in expand(identity))):
        raise RuntimeError("R4R10_PUBLIC_PARENT_EXPANSIONS_NOT_CONNECTED")
    return {
        "source_5_8_screened": True,
        "proposition_2_5_screened": True,
        "eta_definition_screened": True,
        "public_prop25_candidate_found": True,
        "public_signed_parent_candidate_found": True,
        "public_identity_parent_candidate_found": True,
        "public_root_pi95_proof_complete": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = report_folder()
    report: dict[str, object] = {
        "phase": "175-R4R10",
        "dry_run": dry_run,
        "gate": "FAIL_R4R10_CITED_58_PROP25_SHARED",
        "new_given": 2,
        "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        prior = find_prior(prior_file)
        report["prior_report"] = str(prior)
        report["prior"] = validate_prior(json.loads(prior.read_text(encoding="utf-8")))
        report["source_positions"] = source_positions(root)
        cited = build_cited_58_prop25_sources(root)
        if len(cited.proof_links) != 2:
            raise RuntimeError("R4R10_SOURCE_REGISTRY_COUNT_CHANGED")
        report["source_refs"] = [EQUATION_REFERENCE_ID, PROPOSITION_REFERENCE_ID]
        report["delta_composition_replay"] = replay_cited_prop25()
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = (None if dry_run else inspect_public_connection())
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
        report["traceback"] = traceback.format_exc()[-6000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R10 — Toda (5.8) / Prop 2.5 を共有探索へ接続\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "Toda (5.8) は出典付きの符号付き前提として利用します。\n\n"
        + "Prop 2.5 は R4R7 の型付き一般条件を使用します。\n\n"
        + "π₉⁵ の完成証明や符号の確定は本 Phase に含みません。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R10_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R10_NEW_CITED_GIVEN=2")
    print("PHASE175_R4R10_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R10_SIGN_PRESERVED=YES")
    print("PHASE175_R4R10_PUBLIC_PROPOSITION25=" + (
        "CONNECTED" if report.get("public", {}).get("public_prop25_candidate_found") else "NOT_CHECKED"
    ) if isinstance(report.get("public"), dict) else "PHASE175_R4R10_PUBLIC_PROPOSITION25=NOT_CHECKED")
    print("PHASE175_R4R10_PI95=NOT_COMPLETE")
    print("PHASE175_R4R10_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R10_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R10_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R10_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r8-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r8_report)


if __name__ == "__main__":
    sys.exit(main())
