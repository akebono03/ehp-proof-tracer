"""Safely patch only the reviewed nu-prime branch of _factor_identity."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = "phase168_r2_8_3_generator_identity/identity.py"
TARGET = ROOT / RELATIVE
EXPECTED_HEAD_BLOB = "b6e097848ff5dd93ab23eeb724250a21423222bb"

ORIGINAL_FUNCTION = '''def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = ((family == record["latex"] and index is None and decoration is None)
                         or (family == "ν" and index == base_n and decoration in ("′", "'")))
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None'''

REPLACEMENT_FUNCTION = r'''def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = (
                (family == record["latex"] and index is None and decoration is None)
                or (family == "ν" and index == base_n and decoration in ("′", "'"))
                or (
                    family == "ν"
                    and index is None
                    and decoration in ("′", "'")
                    and identifier == 3
                    and base_n == 3
                    and stem == 3
                    and record.get("kinds") == "1"
                    and record["latex"] == r"\nu'"
                    and record["display"] in ("ν'", "ν′")
                )
            )
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None'''


def _git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ("git",) + arguments, cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=check,
    )


def _source_function(text: str) -> str:
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "_factor_identity"]
    if len(functions) != 1:
        raise RuntimeError("_factor_identity must exist exactly once")
    node = functions[0]
    lines = text.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno]).rstrip("\r\n")


def proposed_bytes(source: bytes) -> tuple[str, bytes]:
    if source.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("unexpected UTF-8 BOM: refusing replacement")
    text = source.decode("utf-8")
    if "\r\n" in text and "\n" in text.replace("\r\n", ""):
        raise RuntimeError("mixed newlines: refusing replacement")
    existing = _source_function(text.replace("\r\n", "\n"))
    if existing == REPLACEMENT_FUNCTION:
        return "ALREADY_PATCHED", source
    if existing != ORIGINAL_FUNCTION:
        raise RuntimeError("_factor_identity differs from reviewed source")
    normalized = text.replace("\r\n", "\n")
    if normalized.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("reviewed function is not unique")
    new_text = normalized.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    if "\r\n" in text:
        new_text = new_text.replace("\n", "\r\n")
    ast.parse(new_text)
    return "NEEDS_PATCH", new_text.encode("utf-8")


def preflight() -> tuple[str, bytes, bytes]:
    branch = _git("branch", "--show-current").stdout.decode("utf-8").strip()
    if branch != "develop":
        raise RuntimeError("expected develop branch, got " + branch)
    original = TARGET.read_bytes()
    state, updated = proposed_bytes(original)
    if state == "NEEDS_PATCH":
        baseline = _git("rev-parse", "HEAD:" + RELATIVE).stdout.decode("ascii").strip()
        if baseline != EXPECTED_HEAD_BLOB:
            raise RuntimeError("unreviewed committed identity.py: " + baseline)
        if _git("diff", "--quiet", "HEAD", "--", RELATIVE, check=False).returncode != 0:
            raise RuntimeError("identity.py has local tracked changes; refusing overwrite")
    return state, original, updated


def _atomic_write(destination: Path, payload: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=".r2g_", dir=str(destination.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        state, original, updated = preflight()
        print("PHASE171_R2G_PREFLIGHT=" + state, flush=True)
        if args.action == "check":
            print("PHASE171_R2G_RESULT=PASS_CHECK", flush=True)
            return 0
        if state == "ALREADY_PATCHED":
            print("PHASE171_R2G_RESULT=PASS_ALREADY_PATCHED", flush=True)
            return 0
        base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        directory = base / ("phase171_r2g_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        directory.mkdir(parents=True, exist_ok=False)
        backup = directory / "identity.py.before"
        backup.write_bytes(original)
        (directory / "state.json").write_text(json.dumps({
            "target": RELATIVE,
            "original_sha256": hashlib.sha256(original).hexdigest(),
            "patched_sha256": hashlib.sha256(updated).hexdigest(),
            "reviewed_git_blob": EXPECTED_HEAD_BLOB,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        _atomic_write(TARGET, updated)
        print("PHASE171_R2G_BACKUP=" + str(directory), flush=True)
        print("PHASE171_R2G_PATCHED=" + RELATIVE, flush=True)
        print("PHASE171_R2G_RESULT=PASS_APPLY", flush=True)
        return 0
    except Exception as exc:
        print("PHASE171_R2G_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
