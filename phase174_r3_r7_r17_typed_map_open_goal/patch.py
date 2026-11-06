"""Guarded R17 replacement of one common typed statement formatting function.

The proof search, mathematical rules, and shared Narrative model are untouched.
The target is source-checked and the entire replacement function is exported.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("web_group_proof_common.py")
EXPECTED_BLOB = "0126fd71c66257fc2f4f498a5357d44a67a55884"
PACKAGE = ROOT / "phase174_r3_r7_r17_typed_map_open_goal"
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
          / "EHPProofTracerAudit" / "phase174_r3_r7_r17"
          / "web_group_proof_common.original.py")
OUTPUT = PACKAGE / "MODIFIED_FUNCTION_FULL_JA.md"

OLD = (
    "  from proof import Relation, RelationType\n"
    "\n"
    "  if (\n"
    "    isinstance(statement, CyclicStructureStatement)\n"
)
NEW = (
    "  from proof import Relation, RelationType\n"
    "  from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaSuspensionMap\n"
    "  from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective\n"
    "  from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex\n"
    "\n"
    "  # A display projection of the typed map property, never a proof claim.\n"
    "  if isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism)):\n"
    "    mapping = statement.map\n"
    "    if isinstance(mapping, (TodaDeltaMap, TodaSuspensionMap, TodaHopfInvariantMap)):\n"
    "      source = group_tex(mapping.source_group)\n"
    "      target = group_tex(mapping.target_group)\n"
    "      symbol = map_symbol_tex(mapping)\n"
    "      if source is not None and target is not None and symbol is not None:\n"
    "        arrow = (\n"
    "          r'\\hookrightarrow' if isinstance(statement, MapInjective)\n"
    "          else r'\\twoheadrightarrow' if isinstance(statement, MapSurjective)\n"
    "          else r'\\xrightarrow{\\cong}'\n"
    "        )\n"
    "        return (f'{symbol}: {source} {arrow} {target}', None)\n"
    "\n"
    "  if (\n"
    "    isinstance(statement, CyclicStructureStatement)\n"
)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalize_and_style(data: bytes) -> tuple[str, bytes]:
    """Preserve uniform LF/CRLF; refuse BOM, mixed EOL or bare CR."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in common formatter")
    remainder = data.replace(b"\r\n", b"")
    if b"\r" in remainder or (b"\r\n" in data and b"\n" in remainder):
        raise RuntimeError("Malformed source line endings")
    return data.replace(b"\r\n", b"\n").decode("utf-8"), (b"\r\n" if b"\r\n" in data else b"\n")


def matches_git_blob(data: bytes, sha: str) -> bool:
    try:
        text, _ = normalize_and_style(data)
    except (UnicodeError, RuntimeError):
        return False
    normalized = text.encode("utf-8")
    return any(blob_sha(x) == sha for x in (data, normalized, normalized.replace(b"\n", b"\r\n")))


def transform_source(source: str) -> str:
    """Alter exactly one current common formatter without a special n/k branch."""
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("Expected one unpatched common map formatter anchor")
    before = ast.parse(source)
    functions = [n for n in before.body if isinstance(n, ast.FunctionDef)]
    if sum(n.name == "_group_proof_statement_latex" for n in functions) != 1:
        raise RuntimeError("Common typed formatter function missing or duplicated")
    replaced = source.replace(OLD, NEW, 1)
    after = ast.parse(replaced)
    before_public = [n.name for n in before.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    after_public = [n.name for n in after.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    if before_public != after_public:
        raise RuntimeError("Unexpected public class/function changes")
    compile(replaced, str(TARGET), "exec")
    return replaced


def expected_patched_bytes(original: bytes) -> bytes:
    source, eol = normalize_and_style(original)
    if not matches_git_blob(original, EXPECTED_BLOB):
        raise RuntimeError("Common formatter differs from pinned GitHub blob")
    return transform_source(source).encode("utf-8").replace(b"\n", eol)


def export_complete_function(source: str, destination: Path = OUTPUT) -> None:
    """Write the entire *actual* modified function extracted from the AST."""
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "_group_proof_statement_latex"]
    if len(nodes) != 1:
        raise RuntimeError("Expected one complete formatter function")
    lines = source.splitlines()
    fn = nodes[0]
    complete = "\n".join(lines[fn.lineno - 1:fn.end_lineno])
    destination.write_text(
        "# R17 変更後の関数全文\n\n"
        "変更対象: `web_group_proof_common.py` の `_group_proof_statement_latex`。\n\n"
        "この関数内の import ブロックも省略せず含みます。"
        "ファイル先頭の import は変更ありません。\n\n"
        "```python\n" + complete + "\n```\n",
        encoding="utf-8",
    )


def guarded_patch(*, dry_run: bool, root: Path = ROOT) -> dict[str, str]:
    """Never overwrite a nonmatching checkout; preserve backup on application."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("Missing common formatter")
    original = path.read_bytes()
    result = expected_patched_bytes(original)
    output_source, _ = normalize_and_style(result)
    export_complete_function(output_source, root / OUTPUT.relative_to(ROOT))
    summary = {
        "before_sha": blob_sha(normalize_and_style(original)[0].encode("utf-8")),
        "after_sha": blob_sha(output_source.encode("utf-8")),
        "full_function": str(root / OUTPUT.relative_to(ROOT)),
    }
    if dry_run:
        return summary
    backup = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / "web_group_proof_common.original.py"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Conflicting existing R17 source backup")
    backup.write_bytes(original)
    path.write_bytes(result)
    if path.read_bytes() != result:
        path.write_bytes(original)
        raise RuntimeError("R17 patched bytes failed verification")
    summary["backup"] = str(backup)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    summary = guarded_patch(dry_run=args.dry_run)
    for label, value in summary.items():
        print("PHASE174_R3R7R17_PATCH_" + label.upper() + "=" + value)
    print("PHASE174_R3R7R17_PATCH_GATE=" + ("PASS_PREFLIGHT" if args.dry_run else "PASS_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
