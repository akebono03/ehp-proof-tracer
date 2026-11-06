"""R3-R7-R11: source-first read-only recheck of hand-built family expressions.

R7/R10 diagnostic target symbols were typed as ASCII 'nu'/'eta', whereas
registered family symbols are 'ν'/'η'. These are NOT silently identified.
The audit reconstructs a second candidate from screened registered metadata,
and compares proposal frontiers without creating a proof step or a GIVEN.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r10_cited_family_gap_audit.audit import (
    source_blob_matches,
    verify_toda_transcription,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R11"
BASE_HEAD = "23979feec6685446a48d392fce3f2f1a55e85fe8"
REVIEWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r10_cited_family_gap_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase174_r3_r7_r10_cited_family_gap_audit/audit.py": "42b44e11051df819419a8a7d4f3f3bd8e080622d",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=True,
    )
    return result.stdout.strip()


def reviewed_head_lineage(
    local: str, remote: str, successor_commits: tuple[str, ...],
    changed_paths: tuple[str, ...],
) -> str:
    """Only the reviewed base and one R10-only successor are acceptable."""
    if local != remote or len(local) != 40:
        raise RuntimeError("Local and remote develop HEAD must match")
    if local == BASE_HEAD and not successor_commits and not changed_paths:
        return "REVIEWED_BASE"
    if (len(successor_commits) == 1
            and successor_commits[0] == local
            and local != BASE_HEAD
            and bool(changed_paths)
            and all(path.startswith(REVIEWED_SUCCESSOR_PREFIX)
                    for path in changed_paths)):
        return "REVIEWED_ONE_R10_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed HEAD lineage or non-R10 source change")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be a direct child of repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = remote_line.split()[0] if remote_line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes require review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes require review")
    if local == BASE_HEAD:
        commits: tuple[str, ...] = ()
        changed: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, capture_output=True, check=True,
        )
        commits = tuple(git("rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root).splitlines())
        changed = tuple(git("diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root).splitlines())
    lineage = reviewed_head_lineage(local, remote, commits, changed)
    for relative, expected in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not source_blob_matches(path.read_bytes(), expected):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "source_blobs_checked": len(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r10" / "cited_family_gap.json"


def validate_r10_evidence(report: dict[str, Any]) -> dict[str, Any]:
    """R10 live evidence is a measurement, never proof authorization."""
    if (report.get("phase") != "174-R3-R7-R10"
            or report.get("gate") != "PASS_READ_ONLY_CITED_FAMILY_OBLIGATIONS"):
        raise RuntimeError("Certified R10 live audit is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R10 trust contract changed")
    live = report.get("live") or {}
    expected = {
        "public_original_left_image_frontier": 0,
        "public_canonical_nu_image_frontier": 1,
        "public_right_factor_image_frontier": 1,
        "public_right_associated_image_frontier": 1,
    }
    for key, count in expected.items():
        if (live.get(key) or {}).get("proposal_count") != count:
            raise RuntimeError("R10 observed proposal count changed: " + key)
    if (live.get("source_matches_canonical") is not True
            or live.get("target_matches_canonical") is not False
            or live.get("screened_nu_family_given_count") != 1
            or live.get("isolated_cited_family_candidate_count") != 1
            or live.get("nu_family_definition_position_verified") is not True
            or live.get("public_provider_unchanged") is not True
            or live.get("new_verified_steps") != 0
            or live.get("toda_general_annihilator_directly_admitted") is not False):
        raise RuntimeError("R10 symbol gap or provenance changed")
    return {
        "gate": report["gate"],
        "original_target_noncanonical": True,
        "canonical_nu_proposals": 1,
        "new_verified_steps": 0,
    }


def strict_family_comparison(observed: object, canonical: object) -> dict[str, Any]:
    """Compare full metadata; never equate by the display name alone."""
    attrs = ("name", "dimension", "source", "target", "generator")
    return {
        "exactly_equal": observed == canonical,
        "different_attributes": [name for name in attrs
                                 if getattr(observed, name, None) != getattr(canonical, name, None)],
        "can_use_as_proof_of_equality": False,
    }


def inspect_live_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families, registered_family_of,
    )
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from proof import ProofRule, Relation, RelationType

    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target_zero)

    prior = exact_prior_database_result(5, 5)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != TodaPrimaryGroup(10, 5)
            or getattr(prior.rhs, "order", None) != 2):
        raise RuntimeError("Registered preceding group presentation changed")
    registered = read_registered_stable_families()
    nu = tuple(f for f in registered if f.family_id == 4)
    eta = tuple(f for f in registered if f.family_id == 2)
    if (len(nu) != 1 or len(eta) != 1
            or nu[0].symbol_family != "ν" or nu[0].stem != 3
            or eta[0].symbol_family != "η" or eta[0].stem != 1):
        raise RuntimeError("Registered ν / η family metadata changed")

    def member(family: object, n: int) -> HomotopyElement:
        result = HomotopyElement(
            family.name_at(n), dimension=n,
            source=n + family.stem, target=n,
            generator=GeneratorSymbol(family.symbol_family, n),
        )
        if registered_family_of(result) != family:
            raise RuntimeError("Canonical family member did not match ID registry")
        return result

    nu5, nu6 = member(nu[0], 5), member(nu[0], 6)
    eta8, eta9, eta10 = member(eta[0], 8), member(eta[0], 9), member(eta[0], 10)
    source_generator = prior.rhs.generator
    canonical_source = Composition(nu5, Composition(eta8, eta9))
    if source_generator != canonical_source:
        raise RuntimeError("Database generator is not the expected typed composition")

    # These are the old R7/R10 hand-built *diagnostic* expressions, NOT aliases
    # that the proof search may assume equivalent to registered members.
    ascii_nu6 = HomotopyElement(
        "nu_6", dimension=6, source=9, target=6,
        generator=GeneratorSymbol("nu", 6),
    )
    ascii_eta9 = HomotopyElement(
        "eta_9", dimension=9, source=10, target=9,
        generator=GeneratorSymbol("eta", 9),
    )
    ascii_eta10 = HomotopyElement(
        "eta_10", dimension=10, source=11, target=10,
        generator=GeneratorSymbol("eta", 10),
    )
    comparison = strict_family_comparison(ascii_nu6, nu6)
    if (comparison["exactly_equal"]
            or registered_family_of(ascii_nu6) is not None
            or registered_family_of(ascii_eta9) is not None):
        raise RuntimeError("The old diagnostic symbols changed identity")

    suspension = TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6))
    original_image = GeneratorImage(
        suspension, source_generator,
        Composition(ascii_nu6, Composition(ascii_eta9, ascii_eta10)),
    )
    canonical_image = GeneratorImage(
        suspension, source_generator,
        Composition(nu6, Composition(eta9, eta10)),
    )
    canonical_children = component_image_obligations(canonical_image)
    if (canonical_children is None or len(canonical_children) != 2
            or canonical_children[0].source_generator != nu5
            or canonical_children[0].target_generator != nu6
            or canonical_children[1].source_generator != Composition(eta8, eta9)
            or canonical_children[1].target_generator != Composition(eta9, eta10)):
        raise RuntimeError("Registered family composite does not decompose as expected")
    isolated = expand_composite_generator_image(canonical_image)
    if len(isolated) != 1 or isolated[0].subgoals != canonical_children:
        raise RuntimeError("Previously existing composite rule no longer applies")
    canonical_left_zero = Relation(
        Composition(nu6, eta9), Zero(), RelationType.EQUALITY,
    )
    diagnostic_left_zero = Relation(
        Composition(ascii_nu6, ascii_eta9), Zero(), RelationType.EQUALITY,
    )
    if any(is_exact_given(goal, admitted) for goal in (
        target_zero, ImageZeroStatement(suspension), original_image,
        canonical_image, canonical_children[0], canonical_children[1],
        canonical_left_zero, diagnostic_left_zero,
    )):
        raise RuntimeError("Source conclusion or intermediate goal was adopted as GIVEN")

    def proposal(goal: object) -> dict[str, Any]:
        info = summarize_proposals(provider, goal, admitted)
        return {"proposal_count": info["proposal_count"], "goal_type": type(goal).__name__}

    left_zero_options = tuple(provider(canonical_left_zero))
    return {
        "registered_family_ids": [eta[0].family_id, nu[0].family_id],
        "original_diagnostic_nu": repr(ascii_nu6),
        "registered_nu": repr(nu6),
        "nu_mismatch": comparison,
        "diagnostic_symbols_are_not_verified_aliases": True,
        "canonical_source_from_explicit_database_goal": True,
        "canonical_full_composite_candidate_count": len(isolated),
        "canonical_children": [repr(x)[:1500] for x in canonical_children],
        "public_diagnostic_full_image": proposal(original_image),
        "public_canonical_full_image": proposal(canonical_image),
        "public_canonical_nu_image": proposal(canonical_children[0]),
        "public_canonical_eta_square_image": proposal(canonical_children[1]),
        "public_diagnostic_left_zero": proposal(diagnostic_left_zero),
        "public_canonical_left_zero": proposal(canonical_left_zero),
        "canonical_left_rule_names": [str(getattr(x.rule, "name", "")) for x in left_zero_options],
        "transcription_not_promoted_to_proof": True,
        "new_verified_steps": 0,
        "public_provider_unchanged": True,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r11" / "canonical_fixture_audit.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_transcription(root)
    path = prior_report_path()
    if not path.is_file():
        raise RuntimeError("Certified R10 full audit JSON is required")
    previous = validate_r10_evidence(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_live_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_CANONICAL_FIXTURE_AUDIT",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": previous,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_CANONICAL_FIXTURE_GAP",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R11_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=" + report["git_state"]["source_guard"])
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "R10_ORIGINAL_TARGET_CANONICAL=False")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "DIAGNOSTIC_SYMBOLS_NOT_PROVEN_ALIASES=True")
        print(prefix + "EXISTING_CANONICAL_COMPOSITE_RULE=" + str(
            live["canonical_full_composite_candidate_count"]
        ))
        for label, key in (
            ("ORIGINAL_FULL_IMAGE", "public_diagnostic_full_image"),
            ("CANONICAL_FULL_IMAGE", "public_canonical_full_image"),
            ("CANONICAL_NU_IMAGE", "public_canonical_nu_image"),
            ("CANONICAL_ETA_SQUARE_IMAGE", "public_canonical_eta_square_image"),
            ("CANONICAL_LEFT_ZERO", "public_canonical_left_zero"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
        print(prefix + "CANONICAL_LEFT_ZERO_RULES=" + ",".join(live["canonical_left_rule_names"]))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
