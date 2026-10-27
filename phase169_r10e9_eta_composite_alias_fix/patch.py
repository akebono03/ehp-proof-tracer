"""R10E9: strictly guarded one-function normalization of typed eta aliases.

No changes to the mathematics, proof rules, cited facts or source registries.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r12_r21_eta_generator_chain.py"
OUTPUT = HERE / "output"
EXPECTED_BLOB = "dfd5eb7eb85ef5635aa68ad0b50de49a48aaf59c"

OLD_FUNCTION = '''def _eta_pair(goal: GeneratorSuspension):
    if not isinstance(goal, GeneratorSuspension) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    n = getattr(getattr(goal.target_generator, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        return None
    older = toda_eta_family_definition_statement(n - 1)
    newer = toda_eta_family_definition_statement(n)
    if (goal.map != TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
            or goal.source_generator != older.element
            or goal.target_generator != newer.element):
        return None
    return older, newer'''

NEW_FUNCTION = '''def _eta_pair(goal: GeneratorSuspension):
    """Match only recognized typed eta spellings to cited family instances.

    The DB uses Unicode subscript names and Toda's existing eta path may use
    underscore names.  The already existing alias checker verifies family,
    index, source, target, dimension and one of the two accepted spellings.
    No new proof source, suspension axiom, or equality is introduced.
    """
    if not isinstance(goal, GeneratorSuspension) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    n = getattr(getattr(goal.target_generator, "generator", None), "index", None)
    if type(n) is not int or n < 3:
        return None
    older = toda_eta_family_definition_statement(n - 1)
    newer = toda_eta_family_definition_statement(n)
    from phase165_r12_r28_presentation_connection import _matching_eta_name
    if (goal.map != TodaSuspensionMap(TodaPrimaryGroup(n, n - 1), TodaPrimaryGroup(n + 1, n))
            or not _matching_eta_name(goal.source_generator, older.element)
            or not _matching_eta_name(goal.target_generator, newer.element)):
        return None
    return older, newer'''


def _style_and_content(data: bytes) -> tuple[str, str]:
    """Reject mixed/newline-ambiguous source and preserve the exact style."""
    if not data or b"\r\n" not in data:
        if b"\r" in data:
            raise RuntimeError("R10E9 unsupported CR-only source")
        return data.decode("utf-8"), "LF"
    if b"\n" in data.replace(b"\r\n", b"") or b"\r" in data.replace(b"\r\n", b""):
        raise RuntimeError("R10E9 mixed newlines refused")
    return data.replace(b"\r\n", b"\n").decode("utf-8"), "CRLF"


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _single_function(text: str, name: str) -> str:
    module = ast.parse(text)
    nodes = [item for item in module.body if isinstance(item, ast.FunctionDef) and item.name == name]
    if len(nodes) != 1:
        raise RuntimeError("R10E9 expected exactly one " + name)
    return ast.get_source_segment(text, nodes[0]) or ""


def transform(text: str) -> str:
    """Replace the complete reviewed function, rejecting duplicates and drift."""
    if _single_function(text, "_eta_pair") != OLD_FUNCTION:
        raise RuntimeError("R10E9 eta function changed or already patched")
    if text.count(OLD_FUNCTION) != 1:
        raise RuntimeError("R10E9 eta function ambiguous")
    updated = text.replace(OLD_FUNCTION, NEW_FUNCTION, 1)
    ast.parse(updated)
    if _single_function(updated, "_eta_pair") != NEW_FUNCTION:
        raise RuntimeError("R10E9 eta function postcondition failed")
    return updated


def main() -> None:
    data = TARGET.read_bytes()
    source, style = _style_and_content(data)
    if _git_blob(source.encode("utf-8")) != EXPECTED_BLOB:
        raise RuntimeError("R10E9 working eta source differs from reviewed GitHub blob")
    updated = transform(source)
    new_bytes = updated.encode("utf-8")
    if style == "CRLF":
        new_bytes = new_bytes.replace(b"\n", b"\r\n")
    OUTPUT.mkdir(exist_ok=True)
    # Preserve previous output files for rollback by run.ps1.
    TARGET.write_bytes(new_bytes)
    (OUTPUT / "_eta_pair_FULL.py").write_text(NEW_FUNCTION + "\n", encoding="utf-8")
    (OUTPUT / "phase165_r12_r21_eta_generator_chain.py.FULL").write_text(updated, encoding="utf-8")
    print("R10E9_PATCHED=" + str(TARGET))
    print("R10E9_NEWLINE=" + style)
    print("R10E9_FULL_FUNCTION=" + str(OUTPUT / "_eta_pair_FULL.py"))
    print("R10E9_FULL_FILE=" + str(OUTPUT / "phase165_r12_r21_eta_generator_chain.py.FULL"))


if __name__ == "__main__":
    main()
