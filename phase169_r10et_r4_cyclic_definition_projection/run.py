"""Apply exact, audited R4 code and run only focused tests; rollback on failure."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import traceback
from pathlib import Path

from phase169_r10et_r4_cyclic_definition_projection.patch import (
    EXPECTED_GIT_BLOBS, PROJECTOR, RENDERER,
    prepare, apply, restore, git_blob_sha1,
)

FOCUSED_TESTS = (
    "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_patch.py",
    "phase169_r10et_r4_cyclic_definition_projection/tests/test_r10et_r4_live.py",
    "phase169_r10a_verified_stable_chain_projection/tests/test_r10a_verified_stable_chain.py",
    "phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_stable_definition.py",
    "phase169_r10eq_r1_universal_stable_definition/tests/test_r10eq_live.py",
    "phase169_r10er_r1_mixed_definition_projection/tests/test_r10er_projection.py",
    "phase169_r10en_shared_citation_provenance/tests/test_r10en_core.py",
    "phase169_r10el_shared_generator_suppression/tests/test_r10el_live.py",
    "phase169_r10es_r1_typed_partial_power_display/tests/test_r10es_display.py",
    "phase169_r10et_r3_cyclic_definition_projection_audit/tests/test_shadow_policy.py",
)


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          text=True, encoding="utf-8", errors="replace",
                          capture_output=True).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cases", choices=("focus", "all"), default="all")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    print("R10ET_R4_MODE=IMPLEMENT_FOCUSED", flush=True)
    print("R10ET_R4_BRANCH=" + git(root, "branch", "--show-current"), flush=True)
    print("R10ET_R4_HEAD=" + git(root, "rev-parse", "HEAD"), flush=True)
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R10ET-R4 refuses branch other than develop")
    if git(root, "diff", "--name-status") or git(root, "diff", "--cached", "--name-status"):
        raise RuntimeError("R10ET-R4 refuses preexisting tracked changes")
    for path, blob in EXPECTED_GIT_BLOBS.items():
        observed = git_blob_sha1((root / path).read_bytes())
        if observed != blob:
            raise RuntimeError(f"R10ET-R4 refuses modified source {path}: {observed}")
    before = prepare(root, output)
    applied = False
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        apply(root, before)
        applied = True
        print("R10ET_R4_CHANGED=" + ",".join((PROJECTOR, RENDERER)), flush=True)
        for path in (PROJECTOR, RENDERER):
            print(f"R10ET_R4_FULL_FILE_{Path(path).stem.upper()}=" +
                  str(output / (Path(path).stem + ".FULL")), flush=True)
            print(f"R10ET_R4_FULL_FUNCTION_{Path(path).stem.upper()}=" +
                  str(output / (Path(path).stem + ".changed_function.FULL.py")), flush=True)
        print("R10ET_R4_FOCUSED_PYTEST_START", flush=True)
        cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
               *FOCUSED_TESTS]
        passed = subprocess.run(cmd, cwd=root, env=env).returncode
        print(f"R10ET_R4_FOCUSED_PYTEST_EXIT={passed}", flush=True)
        if passed:
            raise RuntimeError("focused pytest failed; production files restored")
        from phase169_r10et_r4_cyclic_definition_projection.audit import audit
        if not audit(root, output, cases=args.cases):
            raise RuntimeError("R10ET-R4 focused real-case audit failed")
        status = git(root, "diff", "--name-only")
        expected = {PROJECTOR, RENDERER}
        if set(status.splitlines()) != expected:
            raise RuntimeError(f"unexpected tracked change(s): {status}")
        if git(root, "diff", "--cached", "--name-only"):
            raise RuntimeError("unexpected staged change")
        for path in expected:
            if (root / path).read_bytes() != before[path][1]:
                raise RuntimeError(f"unexpected post-audit change to {path}")
        print("R10ET_R4_AUDIT=PASS", flush=True)
        print("R10ET_R4_TRACKED_CHANGED_ONLY_EXPECTED=True", flush=True)
        print("R10ET_R4_PROVIDER_UNCHANGED=True", flush=True)
        print("R10ET_R4_IMPLEMENTATION_COMPLETE=PASS", flush=True)
        return 0
    except Exception:
        print("R10ET_R4_ERROR=" + traceback.format_exc(), flush=True)
        if applied:
            restore(root, before)
            print("R10ET_R4_ROLLBACK=True", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
