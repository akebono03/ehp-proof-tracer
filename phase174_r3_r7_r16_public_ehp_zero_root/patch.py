"""Guarded one-function Phase 174 R3-R7-R16 public EHP root connection.

The existing generic zero-group inference is only proposed. This patch does not
register any GIVEN, discharge premises, or change any proof renderer.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase165_r52_r9_shared_math.py")
BASE_BLOB = "7f81769776278b46a220fb90771970a9dd7c73c2"
PACKAGE = ROOT / "phase174_r3_r7_r16_public_ehp_zero_root"
BACKUP_DIR = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r16"
BACKUP = BACKUP_DIR / "phase165_r52_r9_shared_math.original.py"

OLD = (
    "        options = []\n"
    "        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation\n"
)
NEW = (
    "        options = []\n"
    "        from phase174_r3_r7_r3_ehp_zero_rule.rule import (\n"
    "            expand_ehp_zero_from_delta_surjectivity,\n"
    "        )\n"
    "        options.extend(expand_ehp_zero_from_delta_surjectivity(goal))\n"
    "        from phase166_r3q_hopf_image_relation import expand_hopf_image_relation\n"
)


def blob_sha(value: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(value)).encode("ascii") + b"\0" + value).hexdigest()


def normalize_and_style(value: bytes) -> tuple[str, bytes]:
    """Preserve uniform checkout EOL; reject BOM, bare-CR, mixed EOL."""
    if value.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in tracked production source")
    rest = value.replace(b"\r\n", b"")
    if b"\r" in rest or (b"\r\n" in value and b"\n" in rest):
        raise RuntimeError("Mixed or malformed tracked production line endings")
    eol = b"\r\n" if b"\r\n" in value else b"\n"
    return value.replace(b"\r\n", b"\n").decode("utf-8"), eol


def transform_source(source: str) -> str:
    """Replace one exact anchor inside the already reviewed shared provider."""
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("R16 requires one unmodified shared-provider anchor")
    before = ast.parse(source)
    before_function = next((x for x in before.body
                            if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider"), None)
    if before_function is None or not any(isinstance(x, ast.FunctionDef) and x.name == "expand"
                                           for x in ast.walk(before_function)):
        raise RuntimeError("Expected shared expand function not found")
    result = source.replace(OLD, NEW, 1)
    after = ast.parse(result)
    before_names = [x.name for x in before.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]
    after_names = [x.name for x in after.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]
    if before_names != after_names:
        raise RuntimeError("Unexpected public API change")
    compile(result, str(TARGET), "exec")
    return result


def patched_bytes(original: bytes) -> bytes:
    source, style = normalize_and_style(original)
    if blob_sha(source.encode("utf-8")) != BASE_BLOB and blob_sha(original) != BASE_BLOB:
        raise RuntimeError("Pinned R15 production source differs")
    return transform_source(source).encode("utf-8").replace(b"\n", style)


def expected_from_head(root: Path = ROOT) -> tuple[bytes, bytes]:
    """Read the tracked source only; never trust an unreviewed working tree."""
    import subprocess
    result = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=root, check=True, capture_output=True,
    )
    original = result.stdout
    patched = patched_bytes(original)
    local = (root / TARGET).read_bytes()
    local_normalized, local_eol = normalize_and_style(local)
    head_normalized, _ = normalize_and_style(original)
    if local_normalized != head_normalized:
        raise RuntimeError("Local tracked file differs from reviewed HEAD")
    return local, transform_source(local_normalized).encode("utf-8").replace(b"\n", local_eol)


def export_complete_function(source: str, path: Path) -> None:
    """Emit the entire replacement function, never a short line-level diff."""
    tree = ast.parse(source)
    names = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "shared_expansion_provider"]
    if len(names) != 1:
        raise RuntimeError("Expected one shared_expansion_provider")
    node = names[0]
    lines = source.splitlines()
    body = "\n".join(lines[node.lineno - 1:node.end_lineno])
    path.write_text(
        "# R16 変更後の関数全文\n\n"
        "変更対象: `phase165_r52_r9_shared_math.py` → "
        "`shared_expansion_provider`（内部の `expand` を含む）。\n\n"
        "import はファイル先頭で変更なし。\n\n"
        "```python\n" + body + "\n```\n",
        encoding="utf-8",
    )


def guarded_apply(*, dry_run: bool, root: Path = ROOT) -> dict[str, str]:
    original, expected = expected_from_head(root)
    output_source, _ = normalize_and_style(expected)
    output = root / "phase174_r3_r7_r16_public_ehp_zero_root" / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(output_source, output)
    info = {
        "before_sha": blob_sha(normalize_and_style(original)[0].encode("utf-8")),
        "after_sha": blob_sha(output_source.encode("utf-8")),
        "full_function_file": str(output),
    }
    if dry_run:
        return info
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != original:
        raise RuntimeError("A conflicting prior R16 backup exists; manual review needed")
    BACKUP.write_bytes(original)
    path = root / TARGET
    path.write_bytes(expected)
    if path.read_bytes() != expected:
        path.write_bytes(original)
        raise RuntimeError("R16 write verification failed")
    info["backup"] = str(BACKUP)
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    info = guarded_apply(dry_run=args.dry_run)
    for key, value in info.items():
        print("PHASE174_R3R7R16_PATCH_" + key.upper() + "=" + value)
    print("PHASE174_R3R7R16_PATCH_GATE=" + ("PASS_PREFLIGHT" if args.dry_run else "PASS_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
