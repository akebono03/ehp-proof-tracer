"""Reversible R2E installation with source and focused-test compatibility repair.

Only the reviewed shared bridge function and one stale test assertion are changed.
No Git checkout/reset, implicit proof link, or renderer changes are performed.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXISTING_TEST = ROOT / "test_phase165_r52_r9_shared_math.py"
NEW_MODULE = ROOT / "phase171_r2e_toda53_double_reference.py"
PAYLOAD = PACKAGE / "phase171_r2e_toda53_double_reference.py"
FULL_FUNCTION = PACKAGE / "build_shared_typed_bridge_FULL.py"
FULL_TEST = PACKAGE / "test_phase165_r52_r9_shared_math_FULL.py"
EXPECTED_BLOB = "0ff831522b59f88ff3ed3892f35e5e048be850e1"
EXPECTED_TEST_BLOB = "c6dcfb3cda9c9115fb802f4a1b2141e0502506bd"
BASELINE = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_DIRECTORIES = (
    "phase171_r1_n3_registered_audit/",
    "phase171_r1c_k3_registered_audit/",
    "phase171_r1d_k3_three_gap_diagnostics/",
    "phase171_r2a_prop56_alignment_audit/",
    "phase171_r2b_prop56_source_dependency_audit/",
    "phase171_r2c_pi63_source_frontier_audit/",
    "phase171_r2d_pi63_root_expansion_audit/",
    "phase171_r2e_toda53_double_source/",
)
ANCHOR = "        sources = sources + (build_cited_reviewed_definitions(),)"
ADDITION = "\n".join((
    "        from phase171_r2e_toda53_double_reference import (",
    "            build_adopted_toda53_double_reference,",
    "        )",
    "        sources = sources + (build_adopted_toda53_double_reference(production),)",
))
POSITION_OLD = "\n".join((
    "    from phase166_r3p_position_binding import place_r3p_reference_positions",
    "    return place_r3p_reference_positions(ordered)",
))
POSITION_NEW = "\n".join((
    "    if default_sources:",
    "        from phase166_r3p_position_binding import place_r3p_reference_positions",
    "        return place_r3p_reference_positions(ordered)",
    "    return ordered",
))
TEST_OLD = "\n".join((
    '    assert "証明対象" in body',
    '    assert "使用する結果" in body',
    '    assert "証明" in body',
))
TEST_NEW = "\n".join((
    '    assert "使用する結果" in body',
    '    assert "証明" in body',
    '    assert r"\\pi_{3}^{2}" in body',
    '    assert r"\\mathbb{Z}\\{\\eta_{2}\\}" in body',
))
TEST_PROOF_OLD = 'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n    from hopf_facts import ETA_2\n    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))\n    result = search_shared_group_goal(\n        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,\n    )\n    assert result.status is ProofSearchStatus.COMPLETE\n    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))\n    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)\n'
TEST_PROOF_NEW = 'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n    from hopf_facts import ETA_2\n    bridge = build_shared_typed_bridge()\n    result = search_shared_group_goal(\n        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,\n    )\n    assert result.status is ProofSearchStatus.COMPLETE\n    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))\n    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)\n'
BACKUP = (
    Path(os.environ.get("LOCALAPPDATA") or str(Path.home()))
    / "EHPProofTracerRecovery" / "phase171_r2e_toda53_double_source_backup"
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def verify_checkout() -> None:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    git("merge-base", "--is-ancestor", BASELINE, "HEAD")
    git("merge-base", "--is-ancestor", "origin/develop", "HEAD")
    changed = tuple(
        path for path in git("diff", "--name-only", "-z", BASELINE, "HEAD").split("\0")
        if path
    )
    if any(
        not any(path.startswith(directory) for directory in REVIEWED_DIRECTORIES)
        for path in changed
    ):
        raise RuntimeError("committed production changes outside reviewed audit directories")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked worktree changes exist before R2E installation")
    if git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py") != EXPECTED_BLOB:
        raise RuntimeError("reviewed source blob changed")
    if git("rev-parse", "HEAD:test_phase165_r52_r9_shared_math.py") != EXPECTED_TEST_BLOB:
        raise RuntimeError("reviewed focused test blob changed")
    for path in (PAYLOAD, FULL_FUNCTION, FULL_TEST, TARGET, EXISTING_TEST):
        if not path.is_file():
            raise RuntimeError("missing reviewed R2E file: " + str(path))
    if NEW_MODULE.exists():
        raise RuntimeError("source module path exists before installation")


def _replace_once(original: str, old: str, new: str, label: str) -> str:
    if original.count(old) != 1:
        raise RuntimeError(label + " anchor not unique")
    return original.replace(old, new, 1)


def proposed_source(original: bytes) -> bytes:
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    updated = _replace_once(normalized, ANCHOR, ANCHOR + "\n" + ADDITION, "source")
    updated = _replace_once(updated, POSITION_OLD, POSITION_NEW, "position")
    start = updated.index("def build_shared_typed_bridge(")
    end = updated.index("def shared_expansion_provider(", start)
    actual_function = updated[start:end].rstrip("\n")
    expected_function = FULL_FUNCTION.read_text(encoding="utf-8").rstrip("\n")
    if actual_function != expected_function:
        raise RuntimeError("full replacement function differs from reviewed payload")
    return updated.replace("\n", newline).encode("utf-8")


def proposed_test(original: bytes) -> bytes:
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    updated = _replace_once(normalized, TEST_OLD, TEST_NEW, "narrative test")
    updated = _replace_once(updated, TEST_PROOF_OLD, TEST_PROOF_NEW, "pi32 proof test")
    start = updated.index("def test_r9_pi32_regenerated_by_shared_mathematical_expansion()")
    end = updated.index("def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved()", start)
    if updated[start:end].strip() != TEST_PROOF_NEW.strip():
        raise RuntimeError("pi32 proof function differs from reviewed payload")
    return updated.replace("\n", newline).encode("utf-8")


def apply(*, dry_run: bool = False) -> None:
    verify_checkout()
    original_source = TARGET.read_bytes()
    original_test = EXISTING_TEST.read_bytes()
    updated_source = proposed_source(original_source)
    updated_test = proposed_test(original_test)
    module_payload = PAYLOAD.read_bytes()
    if (not module_payload or updated_source == original_source
            or updated_test == original_test):
        raise RuntimeError("no validated changes to install")
    if dry_run:
        print("PHASE171_R2E_PREFLIGHT=PASS")
        print("PHASE171_R2E_DRY_RUN=PASS")
        return
    BACKUP.mkdir(parents=True, exist_ok=True)
    state_path = BACKUP / "state.json"
    source_before = BACKUP / "phase165_r52_r9_shared_math.py.before"
    test_before = BACKUP / "test_phase165_r52_r9_shared_math.py.before"
    if any(path.exists() for path in (state_path, source_before, test_before)):
        raise RuntimeError("existing R2E backup state; manual review required")
    state = {
        "original_source_sha256": sha256(original_source).hexdigest(),
        "updated_source_sha256": sha256(updated_source).hexdigest(),
        "original_test_sha256": sha256(original_test).hexdigest(),
        "updated_test_sha256": sha256(updated_test).hexdigest(),
        "new_module_sha256": sha256(module_payload).hexdigest(),
    }
    source_before.write_bytes(original_source)
    test_before.write_bytes(original_test)
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        NEW_MODULE.write_bytes(module_payload)
        TARGET.write_bytes(updated_source)
        EXISTING_TEST.write_bytes(updated_test)
    except Exception:
        TARGET.write_bytes(original_source)
        EXISTING_TEST.write_bytes(original_test)
        if NEW_MODULE.is_file() and NEW_MODULE.read_bytes() == module_payload:
            NEW_MODULE.unlink()
        for path in (state_path, source_before, test_before):
            path.unlink(missing_ok=True)
        raise
    print("PHASE171_R2E_PATCHED=phase165_r52_r9_shared_math.py")
    print("PHASE171_R2E_TEST_PATCHED=test_phase165_r52_r9_shared_math.py")
    print("PHASE171_R2E_NEW=phase171_r2e_toda53_double_reference.py")
    print("PHASE171_R2E_BACKUP=" + str(BACKUP))


def restore() -> None:
    state_path = BACKUP / "state.json"
    source_before = BACKUP / "phase165_r52_r9_shared_math.py.before"
    test_before = BACKUP / "test_phase165_r52_r9_shared_math.py.before"
    if any(not path.is_file() for path in (state_path, source_before, test_before)):
        raise RuntimeError("R2E restore state missing")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    original_source = source_before.read_bytes()
    original_test = test_before.read_bytes()
    for contents, name in (
        (original_source, "original_source_sha256"),
        (original_test, "original_test_sha256"),
    ):
        if sha256(contents).hexdigest() != state[name]:
            raise RuntimeError("backup content changed: " + name)
    for path, name in (
        (TARGET, "updated_source_sha256"),
        (EXISTING_TEST, "updated_test_sha256"),
        (NEW_MODULE, "new_module_sha256"),
    ):
        if not path.is_file() or sha256(path.read_bytes()).hexdigest() != state[name]:
            raise RuntimeError("patched file modified: refusing to overwrite " + str(path))
    TARGET.write_bytes(original_source)
    EXISTING_TEST.write_bytes(original_test)
    NEW_MODULE.unlink()
    for path in (state_path, source_before, test_before):
        path.unlink()
    print("PHASE171_R2E_RESTORED=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "install", "restore"))
    args = parser.parse_args()
    try:
        if args.mode == "restore":
            restore()
        else:
            apply(dry_run=(args.mode == "check"))
        return 0
    except Exception as exc:
        print(f"PHASE171_R2E_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        print(traceback.format_exc()[-2200:], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
