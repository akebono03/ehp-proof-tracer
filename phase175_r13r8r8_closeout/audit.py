"""Read-only Phase 175 R13R8R8 closeout audit of three public proofs."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from phase175_r4r12r13r8r6_binding_contract.audit import (
    TARGETS,
    inspect_live_target,
)

BASELINE_HEAD = "b5a0b13884f6f0af527034d8c8bcd47b90c7cc97"
SOURCE_BLOBS = {
    "phase168_r3_37c_reference_projection.py": "a4140294f53c62972c35dd67fbfdfa1430232cae",
    "phase168_r3_5_model_renderer.py": "f77616cf4ccc734954754e6e5d3a8d8b550dfef1",
}
EXPECTED = {(5, 4): (24, 8), (6, 5): (23, 7), (7, 5): (8, 3)}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("REPOSITORY_ROOT_MISMATCH")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    head = git(root, "rev-parse", "HEAD")
    if head != BASELINE_HEAD:
        raise RuntimeError("HEAD_CHANGED_REVERIFY_BASELINE: " + head)
    checked = []
    for path, expected_blob in SOURCE_BLOBS.items():
        actual = git(root, "hash-object", "--", path)
        committed = git(root, "rev-parse", "HEAD:" + path)
        staged = git(root, "rev-parse", ":" + path)
        if actual != expected_blob or staged != expected_blob or committed != expected_blob:
            raise RuntimeError("SOURCE_BLOB_MISMATCH: " + path)
        raw = (root / path).read_bytes()
        crlf = raw.count(b"\r\n")
        lf = raw.count(b"\n") - crlf
        if crlf or b"\r" in raw.replace(b"\r\n", b""):
            raise RuntimeError("EOL_MIXED_OR_CRLF: " + path)
        checked.append({"path": path, "blob": actual, "lf": lf, "crlf": crlf})
    if git(root, "diff", "--check"):
        raise RuntimeError("GIT_DIFF_CHECK_OUTPUT")
    print("PHASE175_R13R8R8_HEAD=" + head)
    for item in checked:
        print("PHASE175_R13R8R8_SOURCE_BLOB=PASS " + str(item["path"]))
    return {"head": head, "checked_sources": checked}


def public_closeout() -> list[dict[str, object]]:
    from web_group_proof import build_standard_web_group_proof_view

    rows = []
    for n, k in TARGETS:
        inspected = inspect_live_target(n, k)
        expected_steps, expected_refs = EXPECTED[(n, k)]
        if (inspected["step_count"], inspected["citation_count"]) != (expected_steps, expected_refs):
            raise RuntimeError(f"COUNT_REGRESSION_{n}_{k}")
        if inspected["registered_fixed_body_gaps"]:
            raise RuntimeError(f"REGISTERED_BODY_GAP_{n}_{k}")
        if (n, k) == (5, 4) and not inspected["r3_r7"]["pass"]:
            raise RuntimeError("R3_R7_PROOF_NARRATIVE_REGRESSION")
        view = build_standard_web_group_proof_view(n, k, mode="narrative")
        if view.key != "generic-complete-proof":
            raise RuntimeError(f"WEB_PROVENANCE_REGRESSION_{n}_{k}: {view.key}")
        rendered = "\n".join(
            str(getattr(line, "prefix", "") or "") + " " +
            str(getattr(line, "statement_latex", "") or "")
            for line in getattr(view, "rendered_lines", ())
        )
        if (n, k) == (5, 4) and ("[R3]より" not in rendered or "[R7]より" not in rendered):
            raise RuntimeError("R3_R7_WEB_PREFIX_REGRESSION")
        print(f"PHASE175_R13R8R8_TARGET={n}:{k} STEPS={expected_steps} CITATIONS={expected_refs} GAPS=0 WEB=PASS")
        rows.append({"n": n, "k": k, "steps": expected_steps, "citations": expected_refs,
                     "fixed_body_gaps": 0, "web_key": view.key})
    return rows


def run(root: Path, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175_R13R8R8", "dry_run": dry_run, "read_only": True,
        "new_given": 0, "new_mathematical_rules": 0,
        "full_pytest": False, "gate": "FAIL_R13R8R8",
    }
    try:
        report["sources"] = source_guard(root)
        if not dry_run:
            report["targets"] = public_closeout()
        report["gate"] = ("PASS_R13R8R8_DRYRUN_SOURCE_GUARD" if dry_run
                          else "PASS_R13R8R8_PUBLIC_CLOSEOUT")
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
    out = Path(tempfile.gettempdir()) / "EHP_Phase175_R13R8R8_closeout.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE175_R13R8R8_GATE=" + str(report["gate"]))
    print("PHASE175_R13R8R8_REPORT=" + str(out))
    if "error" in report:
        print("PHASE175_R13R8R8_ERROR=" + str(report["error"]))
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
