"""R28 source-first preflight and isolated typed literature / inference audit."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, REFERENCE_ID, Prop27UniversalLiteratureStatement,
    register_universal_prop27, verified_universal_statement,
    derive_registered_general_premise,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    typed_specialization, prop27_typed_specialization_rule,
)
from proof import ProofRule, find_inference_match, apply_inference_match

ROOT = Path(__file__).resolve().parents[1]
BASE = "7203ed2ced9a4bb05274e2a4380241b328943c33"
ALLOWED = (
    "phase174_r3_r7_r27_certified_premise_registry_audit/",
    "phase174_r3_r7_r28_prop27_typed_literature_registration/",
)
CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex", "proof.py", "homotopy_groups.py",
    "unified_statement_registry.py", "phase163_r4_registry_bridge.py",
    "phase165_r3_recursive_search.py",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
    "phase174_r3_r7_r26_prop27_source_premise_connection/bridge.py",
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=True).stdout.strip()


def allowed_paths(paths: tuple[str, ...]) -> bool:
    bad = tuple(path for path in paths if path != CACHE
                and not any(path.startswith(prefix) for prefix in ALLOWED))
    if bad:
        raise RuntimeError("Unreviewed paths: " + repr(bad))
    return True


def source_guard() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Expected repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git("rev-parse", "HEAD")
    line = git("ls-remote", "origin", "refs/heads/develop")
    if not line or head != line.split()[0]:
        raise RuntimeError("Local/remote develop differ")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                              cwd=ROOT, capture_output=True)
    if ancestor.returncode:
        raise RuntimeError("R27 reviewed HEAD is not an ancestor")
    allowed_paths(tuple(git("diff", "--name-only", BASE, head).splitlines()))
    allowed_paths(tuple(git("diff", "--name-only").splitlines()))
    allowed_paths(tuple(git("diff", "--cached", "--name-only").splitlines()))
    for file in PROTECTED:
        baseline = subprocess.run(("git", "show", BASE + ":" + file),
                                  cwd=ROOT, capture_output=True, check=True).stdout
        working = (ROOT / file).read_bytes()
        normalized = baseline.replace(b"\r\n", b"\n")
        if working not in (baseline, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("Protected source changed: " + file)
    return head


def check_registration() -> dict[str, object]:
    bridge = register_universal_prop27(ROOT)
    assertion = bridge.registry.assertion(ASSERTION_ID)
    ref = bridge.registry.reference(REFERENCE_ID)
    general = derive_registered_general_premise(bridge)
    match = find_inference_match(prop27_typed_specialization_rule(6), (general,))
    if match is None:
        raise RuntimeError("Proposition 2.7 n=6 inference not available")
    instance = apply_inference_match(match)
    if (instance.rule is not ProofRule.INFERENCE
            or instance.premises != (general,)
            or instance.conclusion != typed_specialization(6)):
        raise RuntimeError("n=6 inference chain invalid")
    return {
        "universal_registered": isinstance(assertion.content, Prop27UniversalLiteratureStatement),
        "reference_locator": ref.locator,
        "source_sha256": assertion.content.source_sha256,
        "universal_given_count": 1,
        "n6_direct_given_count": 0,
        "general_inference": general.rule is ProofRule.INFERENCE,
        "n6_inference": instance.rule is ProofRule.INFERENCE,
        "parent_depth": 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head = source_guard()
    universal = verified_universal_statement(ROOT)
    print("PHASE174_R3R7R28_HEAD=" + head)
    print("PHASE174_R3R7R28_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R28_SOURCE_SHA256=" + universal.source_sha256)
    if not args.dry_run:
        for key, value in check_registration().items():
            print("PHASE174_R3R7R28_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R28_PUBLIC_REGISTRATION=False")
    print("PHASE174_R3R7R28_FULL_PYTEST=False")
    print("PHASE174_R3R7R28_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R28_GATE=" + (
        "PASS_R28_SOURCE_PREFLIGHT_ONLY" if args.dry_run else
        "PASS_R28_UNIVERSAL_REGISTERED_ISOLATED_INFERENCE_PUBLIC_PENDING"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
