"""R29 source-guarded canonical provider integration audit."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
    build_canonical_prop27_context, expand_cited_prop27_goal,
    search_canonical_prop27_instance,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parents[1]
BASE = "9dad1fb060f3bcc507626c980b767a0a52d2e923"
ALLOWED = (
    "phase174_r3_r7_r28_prop27_typed_literature_registration/",
    "phase174_r3_r7_r29_prop27_canonical_provider/",
)
CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex",
    "proof.py",
    "homotopy_groups.py",
    "unified_statement_registry.py",
    "phase163_r4_registry_bridge.py",
    "phase165_r3_recursive_search.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r6_2_unified_registry_r3_r3/provider_registry.py",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=True).stdout.strip()


def allow_paths(paths: tuple[str, ...]) -> bool:
    bad = tuple(path for path in paths
                if path != CACHE and not any(path.startswith(p) for p in ALLOWED))
    if bad:
        raise RuntimeError("Unreviewed committed/staged paths: " + repr(bad))
    return True


def source_guard() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("unexpected repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    head = git("rev-parse", "HEAD")
    line = git("ls-remote", "origin", "refs/heads/develop")
    if not line or head != line.split()[0]:
        raise RuntimeError("local and remote develop differ")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                              cwd=ROOT, capture_output=True)
    if ancestor.returncode:
        raise RuntimeError("R28 reviewed HEAD is not an ancestor")
    allow_paths(tuple(git("diff", "--name-only", BASE, head).splitlines()))
    allow_paths(tuple(git("diff", "--name-only").splitlines()))
    allow_paths(tuple(git("diff", "--cached", "--name-only").splitlines()))
    # R28 is not necessarily committed at BASE; verify its distributed bytes.
    r28 = ROOT / "phase174_r3_r7_r28_prop27_typed_literature_registration" / "registration.py"
    r28_data = r28.read_bytes()
    normalized_r28 = r28_data.replace(b"\r\n", b"\n")
    if hashlib.sha256(normalized_r28).hexdigest() != (
        "a117a00aee6dd6e54ecce578eff2cd1038f6b3a691e0b60592c7f5b5267ea17c"
    ):
        raise RuntimeError("R28 registration source differs from reviewed package")
    for file in PROTECTED:
        baseline = subprocess.run(("git", "show", BASE + ":" + file),
                                  cwd=ROOT, capture_output=True, check=True).stdout
        working = (ROOT / file).read_bytes()
        normalized = baseline.replace(b"\r\n", b"\n")
        if working not in (baseline, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("reviewed source changed: " + file)
    return head


def audit_canonical_search() -> dict[str, object]:
    bridge, providers = build_canonical_prop27_context(ROOT)
    if len(providers.entries()) != 1:
        raise RuntimeError("expected exactly one explicit provider")
    target = typed_specialization(6)
    candidates = expand_cited_prop27_goal(target)
    if len(candidates) != 1:
        raise RuntimeError("typed reverse search candidate missing")
    result = search_canonical_prop27_instance(ROOT, 6)
    if (result.conclusion != target or result.rule is not ProofRule.INFERENCE
            or len(result.premises) != 1
            or result.premises[0].rule is not ProofRule.INFERENCE
            or len(result.premises[0].premises) != 1
            or result.premises[0].premises[0].rule is not ProofRule.GIVEN
            or type(result.premises[0].premises[0].conclusion)
            is not Prop27UniversalLiteratureStatement):
        raise RuntimeError("canonical proof chain failed provenance verification")
    return {
        "shared_registry_reference_count": len(bridge.registry._references),
        "explicit_provider_count": len(providers.entries()),
        "n6_backward_candidates": len(candidates),
        "verified_n6_inference": True,
        "parent_depth": 2,
        "n6_direct_given_count": 0,
        "web_default_route_modified": False,
        "root_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head = source_guard()
    print("PHASE174_R3R7R29_HEAD=" + head)
    print("PHASE174_R3R7R29_SOURCE_GUARD=PASS")
    if not args.dry_run:
        for key, value in audit_canonical_search().items():
            print("PHASE174_R3R7R29_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R29_PUBLIC_WEB_REGISTRATION=False")
    print("PHASE174_R3R7R29_FULL_PYTEST=False")
    print("PHASE174_R3R7R29_GATE=" + (
        "PASS_R29_SOURCE_PREFLIGHT_ONLY" if args.dry_run
        else "PASS_R29_CANONICAL_PROVIDER_VERIFIED_WEB_WIRING_PENDING"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
