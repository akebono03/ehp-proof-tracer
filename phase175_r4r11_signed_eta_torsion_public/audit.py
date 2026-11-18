"""Phase 175 R4R11: source-first signed Delta / proved eta order-two normalization.

The phase adds one general inference, not a new mathematical source/GIVEN.
A group query for pi_9^5 is not claimed complete by this phase.
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

from phase175_r4r11_signed_eta_torsion_public import installer

PACKAGE = "phase175_r4r11_signed_eta_torsion_public"
PRIOR_PACKAGE = "phase175_r4r10_cited_58_prop25_public"
PRIOR_GATE = "PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING"
DRY_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_DRYRUN"
FINAL_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING"
BASE_HEAD = "5c263cc69dc409842d3a13cb3fc65c2347df0bef"
REVIEWED_R4R10_HEAD = "abf619040d52aa9fd61c5bca60db81e28912e24d"
PINNED_WORKING_BLOBS = {
    "phase175_r4r10_cited_58_prop25_public/source.py": "b5162bdaac25e4578973816290207379734229f6",
    "phase175_r4r10_cited_58_prop25_public/provider.py": "be1d726fe98c0258685674ea41099aab1103f318",
    "phase175_r4r10_cited_58_prop25_public/audit.py": "4a60304020bfde1d28639eff9deb72c0e00d6b57",
    "phase175_r4r7_prop25_typed_composition/rule.py": "e957752baf93f75352d106e53205730af9a02b4d",
    "phase175_r4r5_eta7_annihilator_isolated/rule.py": "13fcf56001d2b03283acf2b921d639a01f4d89c3",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        encoding="utf-8", errors="replace", text=True, check=False,
    )
    if result.returncode and not allow_failure:
        raise RuntimeError("R4R11_GIT_FAILED: " + " ".join(args) + ": " + result.stderr)
    return result.returncode, result.stdout.strip()


def reviewed_eol_blob_matches(content: bytes, expected_blob: str) -> bool:
    """Match a pinned Git blob under LF or CRLF working-tree conventions.

    Git may store a text file with CRLF (notably expression.py and Toda TeX)
    while a checkout uses LF, or vice versa. Compare *complete bytes* of both
    line-ending encodings; never waive the pinned SHA-1 or change source text.
    """
    normalized = content.replace(b"\r\n", b"\n")
    candidates = (
        content,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
    return any(installer.git_blob_sha(data) == expected_blob for data in candidates)


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R11_WRONG_REPO_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R11_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    if head not in (BASE_HEAD, REVIEWED_R4R10_HEAD):
        raise RuntimeError("R4R11_UNREVIEWED_HEAD: " + head)
    if head == REVIEWED_R4R10_HEAD:
        code, _ = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head,
                      allow_failure=True)
        if code != 0:
            raise RuntimeError("R4R11_REVIEWED_LINEAGE_NOT_ANCESTOR")
        changed = git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines()
        if any(not (name == installer.TARGET.as_posix()
                    or name.startswith(PRIOR_PACKAGE + "/")) for name in changed):
            raise RuntimeError("R4R11_UNREVIEWED_INTERVENING_COMMIT")
    dirty = sorted(set(
        git(root, "diff", "--name-only")[1].splitlines()
        + git(root, "diff", "--cached", "--name-only")[1].splitlines()
    ))
    if any(item not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for item in dirty):
        raise RuntimeError("R4R11_UNREVIEWED_TRACKED_CHANGE: " + repr(dirty))
    # plan() fail-closes against arbitrary edits to shared production source,
    # and verifies the whole-function, idempotent patch, not merely a marker.
    plan_path, before, after, _ = installer.plan(root)
    if plan_path != root / installer.TARGET:
        raise RuntimeError("R4R11_WRONG_TARGET_PATH")
    for path, expected in PINNED_WORKING_BLOBS.items():
        file = root / path
        if not file.is_file():
            raise RuntimeError("R4R11_SOURCE_MISSING: " + path)
        if not reviewed_eol_blob_matches(file.read_bytes(), expected):
            raise RuntimeError("R4R11_SOURCE_DRIFT: " + path)
    return {
        "head": head,
        "reviewed_base_head": BASE_HEAD,
        "reviewed_successor_head": REVIEWED_R4R10_HEAD,
        "pinned_blobs": len(PINNED_WORKING_BLOBS),
        "production_patch_required": before != after,
        "production_after_blob": installer.git_blob_sha(after.replace(b"\r\n", b"\n")),
        "dirty_tracked_paths": dirty,
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R11_R4R10_REPORT_INVALID")
    expected = {
        "phase": "175-R4R10",
        "dry_run": False,
        "gate": PRIOR_GATE,
        "new_given": 2,
        "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R11_R4R10_GATE_OR_SCOPE_CHANGED")
    pre = report.get("preflight")
    replay = report.get("delta_composition_replay")
    public = report.get("public")
    installed = report.get("install")
    if (not isinstance(pre, dict) or pre.get("head") != BASE_HEAD
            or not isinstance(replay, dict)
            or not isinstance(public, dict)
            or not isinstance(installed, dict)
            or any(replay.get(key) is not True for key in (
                "conclusion_is_signed", "proposition_2_5_citation_present",
                "equation_5_8_citation_present", "eta_family_citation_present",
                "signed_parent_inferred", "composition_identity_parent_inferred",
            ))
            or replay.get("root_group_conclusion_inferred") is not False
            or public.get("public_prop25_candidate_found") is not True
            or public.get("public_signed_parent_candidate_found") is not True
            or public.get("public_identity_parent_candidate_found") is not True
            or public.get("public_root_pi95_proof_complete") is not False
            or installed.get("production_path") != installer.TARGET.as_posix()
            or installed.get("two_full_functions_exported") is not True
            or not isinstance(installed.get("after_git_blob"), str)
            or len(installed["after_git_blob"]) != 40):
        raise RuntimeError("R4R11_R4R10_EVIDENCE_INVALID")
    return {
        "successful_prior": True,
        "prior_head": pre["head"],
        "source_5_8_and_prop25_shared": True,
        "pi95_not_yet_complete": True,
    }


def find_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        result = explicit.expanduser().resolve()
        if not result.is_file():
            raise RuntimeError("R4R11_PRIOR_REPORT_MISSING: " + str(result))
        return result
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    rejected = []
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(path.read_text(encoding="utf-8")))
            return path
        except (OSError, ValueError, UnicodeError, RuntimeError) as exc:
            rejected.append(str(path) + ": " + str(exc))
    raise RuntimeError("R4R11_SUCCESSFUL_R4R10_REPORT_NOT_FOUND: " + str(folder)
                       + "; " + " | ".join(rejected[:3]))


def exact_delta_eta9_goal():
    from expression import Composition, MapApplication
    from map_facts import EHP_DELTA_MAP
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from proof import Relation
    signed = sample_delta_eta9()
    source = canonical_toda58()
    return Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(source.positive_value.right.expression,
                    signed.positive_value.right),
    )


def replay_general_rule() -> dict[str, object]:
    """Replay the three mandatory premises; no theorem-specific proof leaf."""
    from expression import Multiple, Zero
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r11_signed_eta_torsion_public.rule import signed_eta_two_torsion_rule
    from proof import (InferenceRule, ProofRule, ProofStep, Relation,
                       apply_inference_match, find_inference_matches_for_rule)
    goal = exact_delta_eta9_goal()
    signed = sample_delta_eta9()
    beta = signed.positive_value.right
    two_beta_zero = Relation(Multiple(2, beta), Zero())
    definition = TodaEtaFamilyGeneralDefinition()
    rule = signed_eta_two_torsion_rule(goal, signed, two_beta_zero, definition)
    parents = (
        ProofStep(signed, (), ProofRule.INFERENCE,
                  inference_rule=InferenceRule("synthetic signed premise")),
        ProofStep(two_beta_zero, (), ProofRule.INFERENCE,
                  inference_rule=InferenceRule("synthetic order-two premise")),
        ProofStep(definition, (), ProofRule.GIVEN,
                  inference_rule=InferenceRule("synthetic citation premise")),
    )
    # The synthetic fixtures are NOT substituted for real source certificates.
    matches = find_inference_matches_for_rule(rule, parents)
    if len(matches) != 1:
        raise RuntimeError("R4R11_ISOLATED_PROOF_REPLAY_FAILED")
    result = apply_inference_match(matches[0])
    if (result.rule is not ProofRule.INFERENCE
            or result.conclusion != goal
            or result.premises != parents):
        raise RuntimeError("R4R11_DERIVED_RESULT_INVALID")
    if find_inference_matches_for_rule(rule, parents[:2]):
        raise RuntimeError("R4R11_MISSING_CITATION_ACCEPTED")
    return {
        "synthetic_rule_contract_passed": True,
        "real_signed_parent_not_substituted": True,
        "real_order_zero_parent_not_substituted": True,
        "new_group_proof_created": False,
    }


def inspect_shared_connection() -> dict[str, object]:
    """Verify real DB-prior eta7 identity and all shared backward candidate routes.

    DB's generator may use a different Unicode name than a literature
    display label. Never silently equate HomotopyElement names: reconstruct
    the Prop 2.5 instance with the exact, admitted prior generator object.
    """
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
    from map_facts import EHP_DELTA_MAP
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r10_cited_58_prop25_public.provider import CITED_PROP25_RULE
    from phase175_r4r11_signed_eta_torsion_public.rule import RULE_NAME
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME as ORDER_RULE_NAME
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from proof import Relation
    from toda_rules import TodaDeltaImageUpToSignStatement

    bridge = build_shared_typed_bridge()
    root = exact_prior_database_result(5, 4)
    eta_prior = exact_prior_database_result(7, 1)
    if (not isinstance(root, Relation)
            or not isinstance(eta_prior, Relation)
            or eta_prior.lhs != TodaPrimaryGroup(8, 7)
            or not isinstance(eta_prior.rhs, FiniteCyclicGroup)
            or eta_prior.rhs.order != 2):
        raise RuntimeError("R4R11_TYPED_ROOT_OR_ETA7_DB_CONTEXT_NOT_FOUND")
    beta = eta_prior.rhs.generator
    if (not isinstance(beta, HomotopyElement)
            or beta.source != 8 or beta.target != 7 or beta.dimension != 7
            or beta.generator != GeneratorSymbol("η", index=7)):
        raise RuntimeError("R4R11_UNREVIEWED_ETA7_PRIOR_GENERATOR")
    source = canonical_toda58()
    gamma = sample_delta_eta9().element
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(source.positive_value, beta),
    )
    exact = Relation(
        MapApplication(EHP_DELTA_MAP, gamma),
        Composition(source.positive_value.right.expression, beta),
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    delta_options = tuple(item for item in provider(signed)
                          if item.rule.name == CITED_PROP25_RULE)
    if len(delta_options) != 1:
        raise RuntimeError("R4R11_R4R10_SIGNED_ROUTE_NOT_FOUND")
    exact_options = tuple(item for item in provider(exact)
                          if item.rule.name == RULE_NAME)
    if len(exact_options) != 1 or len(exact_options[0].subgoals) != 3:
        raise RuntimeError("R4R11_SHARED_NORMALIZATION_NOT_FOUND")
    child_signed, order, definition = exact_options[0].subgoals
    if (child_signed != signed
            or definition != TodaEtaFamilyGeneralDefinition()
            or child_signed.positive_value != signed.positive_value
            or source.positive_value.right.coefficient != -1):
        raise RuntimeError("R4R11_PUBLIC_PREMISES_CHANGED")
    order_options = tuple(item for item in provider(order)
                          if item.rule.name == ORDER_RULE_NAME)
    if not order_options or any(option.subgoals != (eta_prior,) for option in order_options):
        raise RuntimeError("R4R11_PUBLIC_ORDER_TWO_ROUTE_NOT_FOUND")
    return {
        "r4r10_signed_delta_route_present": True,
        "r4r11_exact_delta_route_present": True,
        "prior_eta7_order_two_route_present": True,
        "exact_database_generator_identity_reused": True,
        "three_proof_obligations_preserved": True,
        "group_conclusion_completed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = report_folder()
    report: dict[str, object] = {
        "phase": "175-R4R11", "dry_run": dry_run,
        "gate": "FAIL_R4R11_SIGNED_ETA_TORSION",
        "new_given": 0, "new_mathematical_rules": 1,
        "pi95_proof_complete": False, "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        prior = find_prior(prior_file)
        report["prior_report"] = str(prior)
        report["prior"] = validate_prior(json.loads(prior.read_text(encoding="utf-8")))
        report["isolated_replay"] = replay_general_rule()
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = None if dry_run else inspect_shared_connection()
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R11 — 2-torsion 符号正規化\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "(5.8) と Proposition 2.5 は R4R10 で出典登録済み。"
        + "一般規則は未証明の符号を勝手に選ばず、証明済み位数2の前提を必要とする。\n\n"
        + "π₉⁵ の完成証明は本段階で主張しない。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R11_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R11_NEW_GIVEN=0")
    print("PHASE175_R4R11_NEW_MATHEMATICAL_RULES=1")
    print("PHASE175_R4R11_SHARED_RULE=" + (
        "CONNECTED" if isinstance(report.get("public"), dict)
        and report["public"].get("r4r11_exact_delta_route_present") else "NOT_CHECKED"
    ))
    print("PHASE175_R4R11_PI95=NOT_COMPLETE")
    print("PHASE175_R4R11_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R11_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R11_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R11_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r10-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r10_report)


if __name__ == "__main__":
    sys.exit(main())
