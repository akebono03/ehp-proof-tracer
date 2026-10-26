"""R4F: display the actual Hopf-fibration applicability of the cited Prop 4.4.

Strictly verify the R4E working copy and reviewed repository Git blob before
editing only render_model_backed_narrative_markdown.  Never add proof premises.
"""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "output"
RENDERER = "phase168_r3_5_model_renderer.py"
REVIEWED_BASE_BLOB = "324900b180b60e14ce7d310912e4833b1ff89c31"


def git_bytes(*args: str) -> bytes:
    return subprocess.run(("git", *args), cwd=ROOT, check=True,
                          capture_output=True).stdout


def git_blob_hash(content: bytes) -> str:
    return hashlib.sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()

def checked_replacement(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"R4E baseline mismatch in {label}: expected 1 anchor, got {count}")
    return source.replace(old, new, 1)

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

def reviewed_r4e_worktree() -> tuple[bytes, str]:
    """Approve only the exact R4E code based on reviewed Git baseline bytes."""
    if git_bytes("branch", "--show-current").decode().strip() != "develop":
        raise RuntimeError("R4F requires the develop branch")
    if not (ROOT / "web_group_proof.py").is_file():
        raise RuntimeError("R4F must be extracted into the repository root")
    reviewed = git_bytes("cat-file", "blob", REVIEWED_BASE_BLOB)
    if git_blob_hash(reviewed) != REVIEWED_BASE_BLOB:
        raise RuntimeError("R4F reviewed baseline object is not available")
    expected = updated_renderer(reviewed.decode("utf-8").replace("\r\n", "\n"))
    head = git_bytes("show", f"HEAD:{RENDERER}")
    old_blob = git_blob_hash(head)
    expected_crlf = expected.replace("\n", "\r\n").encode("utf-8")
    expected_lf = expected.encode("utf-8")
    allowed = {REVIEWED_BASE_BLOB, git_blob_hash(expected_crlf),
               git_blob_hash(expected_lf)}
    if old_blob not in allowed:
        raise RuntimeError("R4F Git HEAD renderer is not reviewed baseline or R4E")
    original = (ROOT / RENDERER).read_bytes()
    if original not in (expected_crlf, expected_lf):
        raise RuntimeError("R4F renderer does not exactly match reviewed R4E; no edit")
    if b"\r\n" in original and b"\n" in original.replace(b"\r\n", b""):
        raise RuntimeError("R4F mixed newlines")
    return original, expected


_INJECTION_ANCHOR = '                    if prop44_tags not in sentence:\n                        sentence = f"{prop44_tags}より, " + sentence\n'
_HOPF_APPLICABILITY = '                    # R4F: the source paragraph immediately BEFORE Prop. 4.4\n                    # establishes the n=4 Hopf fibration.  Cite only the\n                    # actually proved MapInjective step and its cited GIVEN.\n                    # Do not invoke the later Lemma 5.4 naming nu_4.\n                    from homotopy_groups import TodaSuspensionMap\n                    mapping = statement.map\n                    i = getattr(getattr(mapping, "target_group", None),\n                                "group_dimension", None)\n                    if (isinstance(mapping, TodaSuspensionMap)\n                            and type(i) is int and i >= 4\n                            and mapping.source_group == TodaPrimaryGroup(i - 1, 3)\n                            and mapping.target_group == TodaPrimaryGroup(i, 4)\n                            and len(step.premises) == 1\n                            and step.premises[0].rule is ProofRule.GIVEN\n                            and type(step.premises[0].conclusion)\n                                is TodaProp44UniversalStatement\n                            and step.premises[0].conclusion\n                                == TodaProp44UniversalStatement()):\n                        # Keep the R4E result sentence and its [R] tag intact.\n                        # Add the source-order-safe applicability as separate prose.\n                        application = (\n                            r"$n=4$ の Hopf fibration $h:S^7\\to S^4$ により, "\n                            r"$\\alpha=h\\in\\pi_7^4$, "\n                            r"$H(\\alpha)=\\pm\\iota_7$ と取れる. "\n                            + f"{prop44_tags}を "\n                            + rf"$(n,i)=(4,{i})$ に適用できる."\n                        )\n                        lines.extend((application, ""))\n'


def updated_hopf_application(source: str) -> str:
    """Replace one presentation-only span within the shared Renderer."""
    transformed = checked_replacement(
        source, _INJECTION_ANCHOR,
        _INJECTION_ANCHOR + _HOPF_APPLICABILITY,
        "R4F cited Prop44 injectivity narrative",
    )
    before = ast.parse(source)
    after = ast.parse(transformed)
    if len(before.body) != len(after.body):
        raise RuntimeError("R4F module outline changed")
    changed = [(left, right) for left, right in zip(before.body, after.body)
               if ast.dump(left, include_attributes=False) !=
                  ast.dump(right, include_attributes=False)]
    if len(changed) != 1 or not all(
        isinstance(item, ast.FunctionDef)
        and item.name == "render_model_backed_narrative_markdown"
        for pair in changed for item in pair
    ):
        raise RuntimeError("R4F must change only the shared renderer function")
    return transformed


def main() -> None:
    original, expected = reviewed_r4e_worktree()
    new_text = updated_hopf_application(expected)
    translated = new_text.replace("\n", "\r\n") if b"\r\n" in original else new_text
    replacement = translated.encode("utf-8")
    if original == replacement:
        raise RuntimeError("R4F is already applied")
    OUTPUT.mkdir(exist_ok=True)
    backup = OUTPUT / (RENDERER + ".before")
    backup.write_bytes(original)
    (OUTPUT / (RENDERER + ".FULL")).write_bytes(replacement)
    func = next(x for x in ast.parse(new_text).body
                if isinstance(x, ast.FunctionDef)
                and x.name == "render_model_backed_narrative_markdown")
    full_lines = new_text.splitlines(keepends=True)
    full = "".join(full_lines[func.lineno-1:func.end_lineno])
    function_path = OUTPUT / "render_model_backed_narrative_markdown_FULL.py"
    function_path.write_text(full + "\n", encoding="utf-8")
    (ROOT / RENDERER).write_bytes(replacement)
    print("R4F_PATCHED=" + str(ROOT / RENDERER))
    print("R4F_BACKUP=" + str(backup))
    print("R4F_FULL_FUNCTION=" + str(function_path))
    print("R4F_FULL_FILE=" + str(OUTPUT / (RENDERER + ".FULL")))


if __name__ == "__main__":
    main()
