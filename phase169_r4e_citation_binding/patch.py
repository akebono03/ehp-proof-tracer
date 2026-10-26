"""Apply only the reviewed R4E reference/body binding changes.

Both production files must have their Git-reviewed baseline blobs and a clean
working tree. A future commit is acceptable only while those files are unchanged.
No mathematical rule, model, search, or web endpoint is patched.
"""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"

REFERENCE = "phase168_r3_37c_reference_projection.py"
RENDERER = "phase168_r3_5_model_renderer.py"
EXPECTED_BLOBS = {
    REFERENCE: "ee39f50c00117ac120ab74e391491d79fbd65c25",
    RENDERER: "324900b180b60e14ce7d310912e4833b1ff89c31",
}


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True,
    ).stdout


def checked_replacement(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"R4E baseline mismatch in {label}: expected 1 anchor, got {count}")
    return source.replace(old, new, 1)


def updated_reference(source: str) -> str:
    source = checked_replacement(
        source,
        "    from phase165_r52_r27_r5_literature import Toda52UniversalStatement\n",
        "    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement\n",
        "Reference function imports",
    )
    source = checked_replacement(
        source,
        '            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):\n'
        '                sentence = r"$\\pi_i^n=0\\quad(i<n)$."\n',
        '            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):\n'
        '                sentence = r"$\\pi_i^n=0\\quad(i<n)$."\n'
        '            elif (type(statement) is TodaProp44UniversalStatement\n'
        '                  and statement == TodaProp44UniversalStatement()):\n'
        '                sentence = (\n'
        '                    r"$\\alpha\\in\\pi_{2n-1}^{n}$, "\n'
        '                    r"$H(\\alpha)=\\pm\\iota_{2n-1}$ とすると, "\n'
        '                    r"$E:\\pi_{i-1}^{n-1}\\to\\pi_i^{n}$ は単射."\n'
        '                )\n',
        "Reference Proposition 4.4 content",
    )
    return source


def updated_renderer(source: str) -> str:
    source = checked_replacement(
        source,
        '            if sentence.endswith("である."):\n',
        '            # Cite the actual Proposition 4.4 GIVEN ancestor of a\n'
        '            # proved injective map; no rule-name or locator guessing.\n'
        '            from phase165_r14_r6_generic_iso import MapInjective\n'
        '            from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n'
        '            if step.rule is ProofRule.INFERENCE and isinstance(statement, MapInjective):\n'
        '                prop44_numbers = cited_general_ancestor_numbers(\n'
        '                    step, TodaProp44UniversalStatement\n'
        '                )\n'
        '                if prop44_numbers:\n'
        '                    prop44_tags = ", ".join(f"[R{number}]" for number in prop44_numbers)\n'
        '                    if prop44_tags not in sentence:\n'
        '                        sentence = f"{prop44_tags}より, " + sentence\n'
        '            if sentence.endswith("である."):\n',
        "Renderer injective map ancestry citation",
    )
    source = checked_replacement(
        source,
        '            if isinstance(step.conclusion, TodaProp42ExactnessStatement):\n'
        '                statement_latex = statement_latex.replace(r" \\text{ is exact}", "")\n'
        '                lines.append(f"{prefix}${statement_latex}$ は完全.")\n',
        '            if isinstance(step.conclusion, TodaProp42ExactnessStatement):\n'
        '                # An individual certified EHP window is sourced by the\n'
        '                # actual universal Proposition 4.2 GIVEN proof ancestor.\n'
        '                if not tags:\n'
        '                    source_numbers = cited_general_ancestor_numbers(\n'
        '                        step, TodaProp42GeneralExactnessStatement\n'
        '                    )\n'
        '                    if source_numbers:\n'
        '                        prefix = ", ".join(\n'
        '                            f"[R{number}]" for number in source_numbers\n'
        '                        ) + "より, "\n'
        '                statement_latex = statement_latex.replace(r" \\text{ is exact}", "")\n'
        '                lines.append(f"{prefix}${statement_latex}$ は完全.")\n',
        "Renderer EHP window ancestry citation",
    )
    return source


TRANSFORMS = {REFERENCE: updated_reference, RENDERER: updated_renderer}


def _validate_file(path: str, head_bytes: bytes, work_bytes: bytes) -> str:
    # The Git object identity is attached to the file contents, not to HEAD.
    digest = hashlib.sha1(
        f"blob {len(head_bytes)}\0".encode("ascii") + head_bytes
    ).hexdigest()
    if digest != EXPECTED_BLOBS[path]:
        raise RuntimeError(
            f"R4E unreviewed {path} Git blob {digest}; production was not patched"
        )
    if work_bytes.replace(b"\r\n", b"\n") != head_bytes.replace(b"\r\n", b"\n"):
        raise RuntimeError(f"R4E {path} has uncommitted changes; production was not patched")
    if b"\r\n" in work_bytes and b"\n" in work_bytes.replace(b"\r\n", b""):
        raise RuntimeError(f"R4E {path} has mixed newlines")
    text = work_bytes.decode("utf-8")
    if text.startswith("\ufeff"):
        raise RuntimeError(f"R4E unexpected UTF-8 BOM in {path}")
    return text


def construct_sources() -> dict[str, tuple[bytes, bytes]]:
    if not (ROOT / "web_group_proof.py").is_file():
        raise RuntimeError("R4E must run from the repository root")
    if git_bytes("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("R4E requires the develop branch")
    changes = {}
    for path in (REFERENCE, RENDERER):
        head_bytes = git_bytes("show", f"HEAD:{path}")
        work_bytes = (ROOT / path).read_bytes()
        src = _validate_file(path, head_bytes, work_bytes)
        src_unix = src.replace("\r\n", "\n")
        dst_unix = TRANSFORMS[path](src_unix)
        original_ast = ast.parse(src_unix)
        final_ast = ast.parse(dst_unix)
        # Exactly the named function is allowed to differ.
        if len(original_ast.body) != len(final_ast.body):
            raise RuntimeError(f"R4E module outline changed in {path}")
        for old, new in zip(original_ast.body, final_ast.body):
            if ast.dump(old, include_attributes=False) == ast.dump(new, include_attributes=False):
                continue
            wanted = ("project_reference_bodies" if path == REFERENCE
                      else "render_model_backed_narrative_markdown")
            if not (isinstance(old, ast.FunctionDef)
                    and isinstance(new, ast.FunctionDef)
                    and old.name == new.name == wanted):
                raise RuntimeError(f"R4E unexpected change outside {wanted} in {path}")
        dst = dst_unix.replace("\n", "\r\n") if "\r\n" in src else dst_unix
        updated = dst.encode("utf-8")
        if updated == work_bytes:
            raise RuntimeError(f"R4E {path} is already patched")
        changes[path] = (work_bytes, updated)
    return changes


def main() -> None:
    changes = construct_sources()
    OUTPUT.mkdir(exist_ok=True)
    # Prepare and validate both changed files before touching production.
    for path, (old, new) in changes.items():
        (OUTPUT / (path + ".FULL")).write_bytes(new)
        (OUTPUT / (path + ".before")).write_bytes(old)
        # Entire replacement function, keeping the original absolute module source.
        tree = ast.parse(new.decode("utf-8"))
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        lines = new.decode("utf-8").splitlines(keepends=True)
        full = "".join(lines[fn.lineno - 1:fn.end_lineno])
        (OUTPUT / (fn.name + "_FULL.py")).write_text(full + "\n", encoding="utf-8")
    written = []
    try:
        for path, (_, new) in changes.items():
            (ROOT / path).write_bytes(new)
            written.append(path)
    except BaseException:
        for path in written:
            (ROOT / path).write_bytes(changes[path][0])
        raise
    for path in changes:
        print("R4E_PATCHED=" + str(ROOT / path))
        print("R4E_BACKUP=" + str(OUTPUT / (path + ".before")))
        print("R4E_FULL_FUNCTION=" + str(OUTPUT / (("project_reference_bodies" if path == REFERENCE else "render_model_backed_narrative_markdown") + "_FULL.py")))
        print("R4E_FULL_FILE=" + str(OUTPUT / (path + ".FULL")))


if __name__ == "__main__":
    main()
