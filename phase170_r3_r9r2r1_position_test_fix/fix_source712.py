"""Fix only the reviewed Toda (7.12) source clause in the R3-R9 package.

Fail closed if either the checked TeX or the local R3-R9 module differs from
what this narrowly scoped repair expects. Do not change a published citation,
a proof, a transport rule, or the existing source-verification function.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import sys


CHAPTER_VII = Path("sources/toda/Toda_07_2.tex")
R9_SOURCE = Path("phase170_r3_r9_toda712_cited_rewrite/source712.py")
EXPECTED_CLAUSE = (
    r"\varepsilon_3\circ\nu_{11} = \nu'\circ\ov{\nu}_6,\qquad"
    "\n"
    r"\varepsilon'\circ\eta_{13} = \nu'\circ\varepsilon_6 ."
)
EQUATION_BEGIN = r"\begin{equation}"
EQUATION_END = r"\end{equation}"
COMMENTED_LOCATOR = r"% \textbf{(7.12).}"
CLAUSE_ASSIGNMENT = (
    "CLAUSE = (\n"
    "    r\"\\varepsilon_3\\circ\\nu_{11} = \\nu'\\circ\\ov{\\nu}_6,\\qquad\"\n"
    "    \"\\n\"\n"
    "    r\"\\varepsilon'\\circ\\eta_{13} = \\nu'\\circ\\varepsilon_6 .\"\n"
    ")"
)


def normalized_utf8(path: Path) -> str:
    """Decode the actual file; normalize only line endings for comparison."""
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def verify_reviewed_toda712(text: str) -> int:
    """Check the unique printed clause inside the cited, labeled equation."""
    if text.count(EXPECTED_CLAUSE) != 1:
        raise ValueError("Toda (7.12) literal is absent or ambiguous")
    if text.count(COMMENTED_LOCATOR) != 1:
        raise ValueError("Toda (7.12) source locator is absent or ambiguous")
    clause_at = text.index(EXPECTED_CLAUSE)
    locator_at = text.index(COMMENTED_LOCATOR)
    begin_at = text.rfind(EQUATION_BEGIN, 0, locator_at)
    end_at = text.find(EQUATION_END, locator_at)
    if begin_at < 0 or end_at < 0:
        raise ValueError("Toda (7.12) is not inside an equation environment")
    if not (begin_at < locator_at < clause_at < end_at):
        raise ValueError("Toda (7.12) clause is not in its labeled equation")
    if text.find(EQUATION_END, begin_at, locator_at) >= 0:
        raise ValueError("Toda (7.12) locator is outside its equation")
    if text.find(EQUATION_BEGIN, locator_at, clause_at) >= 0:
        raise ValueError("Toda (7.12) clause belongs to a different equation")
    body = text[locator_at:clause_at]
    if body.strip() != COMMENTED_LOCATOR + "\\":
        raise ValueError("Toda (7.12) equation preamble differs from reviewed source")
    return clause_at


def clause_assignment_span(source: str) -> tuple[int, int, object]:
    """Locate exactly one module-level CLAUSE assignment with Python's AST."""
    tree = ast.parse(source)
    matching = []
    for item in tree.body:
        if isinstance(item, ast.Assign):
            names = [target.id for target in item.targets if isinstance(target, ast.Name)]
            if "CLAUSE" in names:
                matching.append(item)
        elif isinstance(item, ast.AnnAssign):
            if isinstance(item.target, ast.Name) and item.target.id == "CLAUSE":
                matching.append(item)
    if len(matching) != 1:
        raise ValueError("R3-R9 module must contain exactly one top-level CLAUSE assignment")
    assignment = matching[0]
    try:
        old_clause = ast.literal_eval(assignment.value)
    except (ValueError, TypeError, SyntaxError, MemoryError) as exc:
        raise ValueError("R3-R9 CLAUSE is not a static string literal") from exc
    if not isinstance(old_clause, str):
        raise ValueError("R3-R9 CLAUSE is not a string")
    if "verified_toda712_generator_equality" not in {
        item.name for item in tree.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }:
        raise ValueError("R3-R9 source verifier is missing")
    return assignment.lineno, assignment.end_lineno, old_clause


def build_minimal_replacement(source: str) -> tuple[str, str]:
    """Replace CLAUSE and nothing else, preserving all pre-existing functions."""
    begin, end, old_clause = clause_assignment_span(source)
    # Require that the existing source guard is still present, including in
    # the idempotent case. Never weaken or circumvent source verification.
    if source.count("vii.count(CLAUSE) != 1") != 1:
        raise ValueError("R3-R9 source verifier guard is not in its reviewed form")
    if old_clause == EXPECTED_CLAUSE:
        return source, "ALREADY_ALIGNED"
    if not ("(7.12)" in old_clause or
            (r"\varepsilon" in old_clause and r"\nu" in old_clause)):
        raise ValueError("R3-R9 CLAUSE does not appear to describe Toda (7.12)")
    lines = source.splitlines(keepends=True)
    replacement = CLAUSE_ASSIGNMENT + "\n"
    proposed = "".join(lines[:begin - 1]) + replacement + "".join(lines[end:])
    ast.parse(proposed)
    if proposed.count("vii.count(CLAUSE) != 1") != 1:
        raise ValueError("source verifier was changed")
    start_new, end_new, clause_new = clause_assignment_span(proposed)
    if clause_new != EXPECTED_CLAUSE or start_new != begin:
        raise ValueError("constructed CLAUSE failed the exact-string audit")
    # The R3-R9 verifier function's implementation must be byte-identical.
    old_tree = ast.parse(source)
    new_tree = ast.parse(proposed)
    def function_bodies(tree: ast.Module) -> dict[str, str]:
        return {
            item.name: ast.dump(item, include_attributes=False)
            for item in tree.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
    if function_bodies(old_tree) != function_bodies(new_tree):
        raise ValueError("a function other than CLAUSE would have changed")
    return proposed, "PATCH_REQUIRED"


def run_audit(root: Path, apply: bool = False) -> dict[str, object]:
    """Verify source + local R3-R9 package; optionally update its CLAUSE."""
    original_tex = normalized_utf8(root / CHAPTER_VII)
    at = verify_reviewed_toda712(original_tex)
    module_path = root / R9_SOURCE
    module_original_bytes = module_path.read_bytes()
    utf8_text = module_original_bytes.decode("utf-8-sig")
    original_newline = "\r\n" if b"\r\n" in module_original_bytes else "\n"
    module_text = utf8_text.replace("\r\n", "\n").replace("\r", "\n")
    updated_text, status = build_minimal_replacement(module_text)
    if apply and status == "PATCH_REQUIRED":
        # The caller backs up the original module before invoking --apply.
        updated_bytes = updated_text.replace("\n", original_newline).encode("utf-8")
        if module_original_bytes.startswith(b"\xef\xbb\xbf"):
            updated_bytes = b"\xef\xbb\xbf" + updated_bytes
        module_path.write_bytes(updated_bytes)
        status = "PATCHED"
    return {
        "status": status,
        "chapter_vii": str(CHAPTER_VII),
        "r9_source": str(R9_SOURCE),
        "clause_offset": at,
        "source_verifier_unchanged": True,
        "checked_clause": EXPECTED_CLAUSE,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(run_audit(args.repo.resolve(), args.apply), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, SyntaxError, UnicodeError) as exc:
        print("PHASE170_R3R9R2_REFUSED=" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
