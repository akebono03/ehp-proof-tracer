"""Audit real Proposition 2.7 registry evidence without promoting source metadata.

This phase deliberately creates no GIVEN, new inference, or public provider.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r7_r26_prop27_source_premise_connection.bridge import (
    Prop27SourceEvidence,
    audited_prop27_source,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    Prop27TypedHopfDeltaStatement,
    typed_specialization,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = "19812c26777a254535ed36b7f892f6c16482b306"
ALLOWED_DIRS = (
    "phase174_r3_r7_r26_prop27_source_premise_connection/",
    "phase174_r3_r7_r27_certified_premise_registry_audit/",
)
ALLOWED_CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex",
    "proof.py",
    "homotopy_groups.py",
    "phase163_r4_registry_bridge.py",
    "unified_statement_registry.py",
    "phase165_r3_recursive_search.py",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
    "tests/test_phase50_prop27_theorem_semantics.py",
)


def git(*args: str, root: Path = ROOT) -> str:
    result = subprocess.run(("git",) + args, cwd=root, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.strip()


def classify_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    bad = tuple(p for p in paths if p != ALLOWED_CACHE
                and not any(p.startswith(prefix) for prefix in ALLOWED_DIRS))
    if bad:
        raise RuntimeError("Unreviewed paths: " + repr(bad))
    return paths


def matches_checkout(actual: bytes, committed: bytes) -> bool:
    normalized = committed.replace(b"\r\n", b"\n")
    return actual in (committed, normalized, normalized.replace(b"\n", b"\r\n"))


def inspect_checkout(root: Path = ROOT) -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R27 under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R27 requires develop")
    head = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if head != remote:
        raise RuntimeError("Local/remote develop mismatch; review manually")
    parent_check = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                                  cwd=root, capture_output=True)
    if parent_check.returncode:
        raise RuntimeError("Reviewed R25 commit not an ancestor")
    classify_paths(tuple(git("diff", "--name-only", BASE, head, root=root).splitlines()))
    tracked = tuple(sorted(set(git("diff", "--name-only", root=root).splitlines()) |
                           set(git("diff", "--cached", "--name-only", root=root).splitlines())))
    classify_paths(tracked)
    for path in PROTECTED:
        old = subprocess.run(("git", "show", BASE + ":" + path), cwd=root,
                             check=True, capture_output=True).stdout
        actual = (root / path).read_bytes()
        if not matches_checkout(actual, old):
            raise RuntimeError("Protected source changed: " + path)
    return {"local_head": head, "remote_head": remote,
            "protected_files": len(PROTECTED), "source_guard": "PASS"}


def inspect_registry(bridge: object, source: Prop27SourceEvidence) -> dict[str, object]:
    """Inspect actual links, never interpret archive metadata as ProofStep."""
    from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationStatus
    from proof import ProofRule, ProofStep
    from unified_statement_registry import AssertionOrigin

    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("Expected an actual RegistryBridgeResult")
    matching_references = tuple(ref for ref in bridge.registry._references.values()
                                if ref.locator == source.locator)
    matching_assertions = tuple(a for a in bridge.registry._assertions.values()
                                if a.reference_id in {r.reference_id for r in matching_references})
    linked_steps = tuple(link.step for link in bridge.proof_links
                         if link.assertion_id in {a.assertion_id for a in matching_assertions}
                         and link.step is not None)
    actual_candidates = tuple(step for step in linked_steps
                              if isinstance(step, ProofStep)
                              and isinstance(step.conclusion, Prop27SourceEvidence)
                              and step.conclusion == source)
    # A registry link, a label and a status string do NOT independently certify a step.
    # Fail closed if the registry now contains possible source steps requiring review.
    if actual_candidates:
        raise RuntimeError("Prop27 registry source steps require independent certification review")
    source_evidence_as_given = tuple(step for step in linked_steps
                                     if isinstance(step, ProofStep)
                                     and step.rule is ProofRule.GIVEN
                                     and isinstance(step.conclusion, (
                                         Prop27SourceEvidence,
                                         Prop27GeneralTheoremPremise,
                                         Prop27TypedHopfDeltaStatement,
                                     )))
    if source_evidence_as_given:
        raise RuntimeError("Direct Prop27 schema/instance GIVEN would bypass source gate")
    structured = sum(record.status is MigrationStatus.STRUCTURED for record in bridge.records
                     if record.assertion_id in {a.assertion_id for a in matching_assertions})
    return {
        "matching_literature_references": len(matching_references),
        "matching_assertions": len(matching_assertions),
        "structured_registry_records": structured,
        "linked_steps": len(linked_steps),
        "eligible_certified_source_step": False,
        "certification_from_metadata": False,
    }


def inspect_public_root() -> dict[str, object]:
    """Use the actual read-only R22 public frontier; do not invoke display changes."""
    from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import inspect_public_boundary
    current = inspect_public_boundary()
    if current["search_status"] != "search_failed" or current["verified_steps"] != 0:
        raise RuntimeError("Public frontier changed; independently review before connecting")
    return {"search_status": current["search_status"],
            "signed_delta_witnesses": current["signed_delta_witnesses"],
            "verified_steps": current["verified_steps"], "root_complete": False}


def report(dry_run: bool, root: Path = ROOT) -> dict[str, object]:
    state = inspect_checkout(root)
    evidence = audited_prop27_source(root)
    if typed_specialization(6).source_iota_dimension != 13:
        raise RuntimeError("Typed n=6 delta source changed")
    registry = None
    public = None
    if not dry_run:
        from phase163_r4_registry_bridge import build_registry_bridge
        registry = inspect_registry(build_registry_bridge(), evidence)
        public = inspect_public_root()
    return {"phase": "174-R3-R7-R27", "git": state,
            "source": {"locator": evidence.locator, "sha256": evidence.theorem_sha256},
            "registry": registry, "public": public,
            "new_given": 0, "new_production_rules": 0,
            "new_public_registration": False, "full_pytest": False,
            "root_complete": False,
            "gate": ("PASS_R27_SOURCE_PREFLIGHT_ONLY" if dry_run else
                     "PASS_R27_REGISTRY_BOUNDARY_AUDITED_CERTIFIED_STEP_PENDING")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    path = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) /
            "EHPProofTracerAudit" / "phase174_r3_r7_r27")
    path.mkdir(parents=True, exist_ok=True)
    dest = path / ("preflight.json" if args.dry_run else "registry_boundary.json")
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R27_"
    print(prefix + "HEAD=" + str(result["git"]["local_head"]))
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "SOURCE_SHA256=" + str(result["source"]["sha256"]))
    if result["registry"] is not None:
        for field, value in result["registry"].items():
            print(prefix + "REGISTRY_" + field.upper() + "=" + str(value))
        for field, value in result["public"].items():
            print(prefix + "PUBLIC_" + field.upper() + "=" + str(value))
    print(prefix + "NEW_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "PUBLIC_REGISTRATION=False")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "REPORT=" + str(dest))
    print(prefix + "GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
