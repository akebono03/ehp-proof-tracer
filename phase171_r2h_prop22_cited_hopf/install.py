"""Guarded, idempotent R2H integration; no reset, checkout, or overwrite of edits."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
BASE_BLOB_SHA = "97bd75c575200ff799e10c5d1f646bc804136580"
ANCHOR_SOURCE = "        sources = sources + (build_adopted_toda53_double_reference(production),)"
INSERT_SOURCE = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            build_cited_prop22_right_reference,\n"
    "        )\n"
    "        sources = sources + (build_cited_prop22_right_reference(production),)"
)
ANCHOR_PROVIDER = "        options.extend(expand_hopf_image_relation(goal, tuple(available)))"
INSERT_PROVIDER = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            expand_cited_prop22_right_formula,\n"
    "        )\n"
    "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))"
)


def git(*arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("git inspection failed: " + process.stderr)
    return process.stdout.strip()


def git_blob(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n")
    return sha1(b"blob " + str(len(normalized)).encode() + b"\0" + normalized).hexdigest()


def patch_source(source: str) -> str:
    """Insert only the R2H source and expansion connections in existing functions."""
    eol = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    if (normalized.count(ANCHOR_SOURCE) != 1
            or normalized.count(ANCHOR_PROVIDER) != 1):
        raise ValueError("shared integration anchors changed or are ambiguous")
    for addition in (INSERT_SOURCE, INSERT_PROVIDER):
        if addition in normalized:
            raise ValueError("partial or duplicate R2H integration")
    normalized = normalized.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE)
    normalized = normalized.replace(ANCHOR_PROVIDER, ANCHOR_PROVIDER + "\n" + INSERT_PROVIDER)
    return normalized.replace("\n", eol)


def status() -> tuple[str, bytes, bytes]:
    """Allow only the reviewed HEAD file or its exact two-connection patch.

    The Git blob SHA covers original bytes.  CRLF versus LF conversion in a
    checkout must not be confused with an unreviewed source modification.
    """
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R2H must run on develop")
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    head_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    if head_blob != BASE_BLOB_SHA:
        raise RuntimeError("HEAD shared_math blob differs from reviewed baseline")
    baseline_process = subprocess.run(
        ["git", "show", "HEAD:phase165_r52_r9_shared_math.py"],
        cwd=ROOT, capture_output=True, check=True,
    )
    baseline_bytes = baseline_process.stdout
    if sha1(b"blob " + str(len(baseline_bytes)).encode() + b"\0" + baseline_bytes).hexdigest() != BASE_BLOB_SHA:
        raise RuntimeError("Git HEAD shared_math blob content is inconsistent")

    current = TARGET.read_bytes()
    baseline_text = baseline_bytes.decode("utf-8")
    current_text = current.decode("utf-8")
    normalize = lambda value: value.replace("\r\n", "\n")
    if normalize(current_text) == normalize(baseline_text):
        updated = patch_source(current_text).encode("utf-8")
        return "NEEDS_PATCH", current, updated
    expected = patch_source(baseline_text)
    if normalize(current_text) == normalize(expected):
        return "ALREADY_APPLIED", current, current
    raise RuntimeError("shared_math contains unreviewed changes; refusing to overwrite")


def full_functions(source: str) -> dict[str, str]:
    """Extract the full post-change functions, never truncated diffs."""
    import ast
    tree = ast.parse(source)
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in (
            "build_shared_typed_bridge", "shared_expansion_provider",
        ):
            result[node.name] = ast.get_source_segment(source, node)
    if set(result) != {"build_shared_typed_bridge", "shared_expansion_provider"}:
        raise ValueError("expected full shared functions missing")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "apply"))
    args = parser.parse_args()
    stage, before, after = status()
    print("PHASE171_R2H_PREFLIGHT=" + stage, flush=True)
    if args.mode == "check":
        print("PHASE171_R2H_RESULT=PASS_CHECK", flush=True)
        return 0
    if stage == "NEEDS_PATCH":
        dest_root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        dest = dest_root / ("phase171_r2h_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        dest.mkdir(parents=True, exist_ok=False)
        backup = dest / TARGET.name
        shutil.copy2(TARGET, backup)
        print("PHASE171_R2H_BACKUP=" + str(dest), flush=True)
        if TARGET.read_bytes() != before:
            raise RuntimeError("shared file changed during R2H preflight")
        TARGET.write_bytes(after)
        print("PHASE171_R2H_PATCHED=" + str(TARGET.relative_to(ROOT)), flush=True)
    checked = TARGET.read_text(encoding="utf-8")
    pieces = full_functions(checked)
    output = ROOT / "phase171_r2h_prop22_cited_hopf" / "output"
    output.mkdir(parents=True, exist_ok=True)
    for name, code in pieces.items():
        (output / (name + "_FULL.py")).write_text(code + "\n", encoding="utf-8")
    print("PHASE171_R2H_FUNCTIONS_FULL=" + str(output), flush=True)
    print("PHASE171_R2H_RESULT=PASS_APPLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
