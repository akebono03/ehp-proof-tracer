"""R33 read-only audit: independent source and public proof-leaf availability.

This package changes no production provider, no mathematical rule, and no
GIVEN. A cited text, a typed goal, and a verified ProofStep are distinct.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    classify_three_premises, inspect_prior_three_clauses,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "02f694b27a4239052bfa9d27a116fca6bbbff6b5"
SOURCE = "sources/toda/Toda_05_2.tex"
REVIEWED_SUCCESSOR_DIRS = (
    "phase174_r3_r7_r32_lower_delta_kernel_audit/",
    "phase174_r3_r7_r32r1_reviewed_head_handoff_fix/",
)
GIT_BLOB_PINS = {
    SOURCE: "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "742451ea67ede314f99246afbb470a5e8a7f008f",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r57_r19_delta_image_backward.py": "c5b3447258f41e15219ead8daeeb17cbb5605b6d",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase170_r3_r6_prop58_source.py": "f0223668e60bb9d18f10b0e8721dece79d7e705a",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py": "bc78a9732230ce4af021bbc9b218a4153d3af96e",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py": "12487ac30e214facd786f106e8e2934b635e60cf",
}
LOCAL_SHA256_PINS = {
    "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py":
        "ab6f81dbbb32c6fd46dfb85c639534f7eff15062e2cc42c58b32f44efc0bc191",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/audit.py":
        "c191d8a9c25007e1d42b4a7faa6898b1d118a3b60f021f2dbb5ec713f0aa7656",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py":
        "c4ff7d4eb1d24569fdb97c87eec9fa4689ff0bc7b224a3e29bbbda2439ca995a",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/run.ps1":
        "6e070729ce6c5ae809be0f564a87372df179ab49ce971f7a3af41efdd0044103",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob_pin(data: bytes, sha: str) -> bool:
    canonical = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        git_blob_sha(candidate) == sha
        for candidate in (data, canonical, canonical.replace(b"\n", b"\r\n"))
    )


def canonical_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Permit only an exact reviewed tree or successor adding R32 files only."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R33 must be extracted at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R33 requires develop")
    local = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if not remote:
        raise RuntimeError("Cannot verify current GitHub develop")
    reviewed_additions: tuple[str, ...] = ()
    if remote != BASE_HEAD:
        # Only inspect upstream history; this does not change the working tree.
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("GitHub HEAD changed while fetching")
        ancestor = subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
            cwd=ROOT, capture_output=True,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("New GitHub history is not a reviewed successor")
        reviewed_additions = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not reviewed_additions or any(
            not path.startswith(REVIEWED_SUCCESSOR_DIRS) for path in reviewed_additions
        ):
            raise RuntimeError("GitHub changed files outside the reviewed R32-only handoff")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Local HEAD differs from reviewed local/remote versions")
    if git("diff", "--name-only") or git("diff", "--cached", "--name-only"):
        raise RuntimeError("Unexpected tracked edits; preserve and review manually")
    for path, sha in GIT_BLOB_PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob_pin(file.read_bytes(), sha):
            raise RuntimeError("Reviewed production/source blob differs: " + path)
    for path, sha in LOCAL_SHA256_PINS.items():
        file = ROOT / path
        if not file.is_file() or canonical_sha256(file.read_bytes()) != sha:
            raise RuntimeError("Reviewed R31/R32 package differs: " + path)
    return {
        "local_head": local, "remote_head": remote,
        "reviewed_successor_r32_files": list(reviewed_additions),
        "checked_pinned_github_files": len(GIT_BLOB_PINS),
        "checked_pinned_handoff_files": len(LOCAL_SHA256_PINS),
        "source_guard": "PASS", "r30_r31_r32_preserved": True,
    }


def inspect_registered_frontier() -> dict[str, object]:
    """Read public screens and DB prior without inventing or attaching steps."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import (
        FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap,
        TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, precedes_db_goal,
    )
    from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import (
        conditional_kernel_premises, generator_has_group_coordinates,
    )
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement
    from unified_statement_registry import AssertionOrigin

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    domain = TodaPrimaryGroup(11, 11)
    target = TodaPrimaryGroup(9, 5)
    lower = TodaDeltaMap(domain, target)
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    leaves = tuple(link.step for link in screened.proof_links
                   if link.step is not None and link.step.rule is ProofRule.GIVEN)
    domain_leaves = tuple(step for step in leaves
                          if type(step.conclusion) is Relation
                          and step.conclusion.relation_type is RelationType.EQUALITY
                          and step.conclusion.lhs == domain
                          and type(step.conclusion.rhs) is FreeCyclicGroup)
    target_leaves = tuple(step for step in leaves
                          if type(step.conclusion) is Relation
                          and step.conclusion.relation_type is RelationType.EQUALITY
                          and step.conclusion.lhs == target
                          and type(step.conclusion.rhs) is FiniteCyclicGroup
                          and step.conclusion.rhs.order == 2)
    image_leaves = tuple(step for step in leaves
                         if type(step.conclusion) is TodaDeltaImageUpToSignStatement
                         and step.conclusion.map == lower)
    direct_kernel = tuple(step for step in leaves
                          if type(step.conclusion) is KernelMultipleStatement
                          and step.conclusion.map == lower)
    direct_root = tuple(step for step in leaves if step.conclusion == goal)
    if direct_kernel or direct_root:
        raise RuntimeError("A forbidden direct kernel/root source leaf was exposed")
    all_screened = classify_three_premises(
        domain=len(domain_leaves) == 1,
        codomain=len(target_leaves) == 1,
        image=len(image_leaves) == 1,
    )
    fixed_candidates = tuple(
        a for a in bridge.registry._assertions.values()
        if a.origin is AssertionOrigin.FIXED_STATEMENT
    )
    fixed_group_candidates = tuple(
        a for a in fixed_candidates if type(a.content) is Relation
        and a.content.relation_type is RelationType.EQUALITY
        and a.content.lhs in (domain, target)
    )
    fixed_lower_delta_candidates = tuple(
        a for a in fixed_candidates
        if type(a.content) is TodaDeltaImageUpToSignStatement
        and a.content.map == lower
    )
    db = exact_prior_database_result(5, 4)
    if db is None:
        raise RuntimeError("Previously verified pi_9^5 DB prior is absent")
    db_valid = (type(db) is Relation and db.relation_type is RelationType.EQUALITY
                and db.lhs == target and type(db.rhs) is FiniteCyclicGroup
                and db.rhs.order == 2 and precedes_db_goal(5, 4, 7, 5))
    if not db_valid:
        raise RuntimeError("DB prior has changed or is not strictly earlier")
    db_generator = db.rhs.generator
    # Avoid fake HomotopyElement substitutions: inspect the real typed object.
    accepts_db_generator = generator_has_group_coordinates(db_generator, target)
    generator = HomotopyElement(
        "iota_11", 11, 11, 11, GeneratorSymbol("iota", 11),
    )
    expected_kernel = KernelMultipleStatement(lower, domain, generator, 2)
    synthetic_target = Relation(
        target, FiniteCyclicGroup(2, HomotopyElement(
            "nu_5_eta_8", 9, 9, 5, GeneratorSymbol("nu_eta", 5),
        )), RelationType.EQUALITY,
    )
    synthetic_domain = Relation(
        domain, FreeCyclicGroup(generator), RelationType.EQUALITY,
    )
    synthetic_signed = TodaDeltaImageUpToSignStatement(
        lower, generator, synthetic_target.rhs.generator,
    )
    if conditional_kernel_premises(
        expected_kernel, synthetic_domain, synthetic_target, synthetic_signed,
    ) != (synthetic_domain, synthetic_target, synthetic_signed):
        raise RuntimeError("R32 isolated conditional lemma changed")
    # Never substitute the synthetic representation for an actual DB generator.
    db_pair_accepts_contract = conditional_kernel_premises(
        expected_kernel, synthetic_domain, db, TodaDeltaImageUpToSignStatement(
            lower, generator, db_generator,
        ),
    ) is not None
    return {
        "screened_domain_premises": len(domain_leaves),
        "screened_codomain_premises": len(target_leaves),
        "screened_generator_image_premises": len(image_leaves),
        "screened_completeness": all_screened,
        "registry_fixed_group_candidates": len(fixed_group_candidates),
        "registry_fixed_lower_delta_candidates": len(fixed_lower_delta_candidates),
        "strictly_earlier_db_prior_present": True,
        "db_prior_generator_type": type(db_generator).__name__,
        "r32_contract_accepts_db_generator": accepts_db_generator,
        "r32_contract_accepts_actual_db_relation": db_pair_accepts_contract,
        "db_prior_is_an_independent_literature_citation": False,
        "hypothetical_group_and_map_steps_not_certified": True,
        "kernel_direct_given_inserted": False,
        "root_direct_given_inserted": False,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    git_state = verify_checkout()
    source_text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    source_facts = inspect_prior_three_clauses(source_text)
    frontier = None if dry_run else inspect_registered_frontier()
    return {
        "phase": "174-R3-R7-R33",
        "git_state": git_state,
        "source_evidence": [vars(x) for x in source_facts],
        "frontier": frontier,
        "new_givens": 0, "new_inference_rules": 0,
        "production_files_changed": 0,
        "kernel_proved": False, "root_complete": False,
        "full_pytest": False,
        "gate": ("PASS_R33_SOURCE_PREFLIGHT_ONLY" if dry_run else
                 "PASS_R33_INDEPENDENT_THREE_PREMISE_FRONTIER_AUDITED_SOURCE_WIRING_PENDING"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    output_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r33"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / ("preflight.json" if args.dry_run else "source_frontier.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R33_"
    for key in ("local_head", "remote_head", "source_guard", "r30_r31_r32_preserved"):
        print(p + key.upper() + "=" + str(result["git_state"][key]))
    print(p + "THREE_PRINTED_SOURCES_PRECEDE_PROP59=True")
    if result["frontier"] is not None:
        for key, value in result["frontier"].items():
            if key == "screened_completeness":
                for subkey, subvalue in value.items():
                    if subkey != "premises":
                        print(p + "FRONTIER_" + subkey.upper() + "=" + str(subvalue))
            elif isinstance(value, (bool, int, str)):
                print(p + key.upper() + "=" + str(value))
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_INFERENCE_RULES=0")
    print(p + "KERNEL_PROVED=False")
    print(p + "ROOT_COMPLETE=False")
    print(p + "FULL_PYTEST=False")
    print(p + "REPORT=" + str(path))
    print(p + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
