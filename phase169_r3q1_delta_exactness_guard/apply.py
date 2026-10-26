"""Minimal guarded in-place patch of the common typed prose path."""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
OUTPUT = PKG / "output"
RENDERER = ROOT / "phase168_r3_5_model_renderer.py"
TYPED = ROOT / "phase168_r3_27_typed_statement_projection.py"


def whole_function(code: str, name: str) -> str:
    match = [node for node in ast.parse(code).body
             if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(match) != 1:
        raise RuntimeError("Missing or ambiguous function: " + name)
    node = match[0]
    return "".join(code.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def patch_renderer(code: str) -> str:
    # Retire the optional R3P special-case shortcut if it was installed.
    r3p = (
        "        from phase169_r3p_ehp_narrative_reason import project_ehp_reasoned_lines\n"
        "        reasoned_lines = project_ehp_reasoned_lines(model, index)\n"
        "        if reasoned_lines is not None:\n"
        "            for reasoned_line in reasoned_lines:\n"
        "                lines.extend((reasoned_line, \"\"))\n"
        "            continue\n"
    )
    code = code.replace(r3p, "")
    # Undo the optional R3P reference-display fork; citations remain untouched.
    r3p_refs = (
        "        source_bodies = citation.statement_bodies\n"
        "        if not source_bodies:\n"
        "            from phase169_r3p_ehp_narrative_reason import source_bodies_for_terminal_proof\n"
        "            source_bodies = source_bodies_for_terminal_proof(model, citation)\n"
    )
    if r3p_refs in code:
        code = code.replace(r3p_refs, "")
        code = code.replace("        for sentence in source_bodies:\n",
                            "        for sentence in citation.statement_bodies:\n")
    old = (
        "        body_line = body_by_step.get(index)\n"
        "        if body_line is None:\n"
        "            sentence = typed_sentence(step.conclusion, step)\n"
        "            if sentence is not None:\n"
    )
    new = (
        "        body_line = body_by_step.get(index)\n"
        "        sentence = typed_sentence(step.conclusion, step)\n"
        "        if sentence is not None:\n"
    )
    if old in code:
        if code.count(old) != 1:
            raise RuntimeError("Ambiguous renderer entry point")
        start = code.index(old)
        body_start = start + len(old)
        # Only the inner reasoned sentence block is dedented by one level.
        terminator = "\n        else:\n            tags = ",
        end = code.find(terminator[0], body_start)
        if end < 0:
            raise RuntimeError("Renderer fallthrough branch changed")
        body = code[body_start:end]
        lines = body.splitlines(keepends=True)
        if not lines or any(line.strip() and not line.startswith("                ") for line in lines):
            raise RuntimeError("Unexpected renderer reasoned block indentation")
        dedented = "".join(line[4:] if line.strip() else line for line in lines)
        code = (code[:start] + new + dedented
                + "\n        elif body_line is not None:\n            tags = "
                + code[end + len(terminator[0]):])
    elif new not in code:
        raise RuntimeError("Renderer already edited differently; refusing to patch")
    return code


def patch_typed(code: str) -> str:
    helper = (PKG / "full_functions" / "map_property_sentence_FULL.py").read_text(encoding="utf-8")
    anchor = "def typed_sentence(statement, step):\n"
    if helper not in code:
        if code.count(anchor) != 1:
            raise RuntimeError("Missing typed_sentence")
        code = code.replace(anchor, helper.rstrip() + "\n\n" + anchor, 1)
    anchor_at = code.index(anchor)
    # Remove only the legacy family-specific map branch.  The new common
    # projector handles precisely the same statements with validated premises.
    first = code.find("    if isinstance(statement, TodaDeltaZeroStatement):\n", anchor_at)
    second = code.find("    if isinstance(statement, EHPImageEqualsKernelStatement):\n", anchor_at)
    if first >= 0 and second > first:
        between = code[first:second]
        if ("if isinstance(statement, (MapInjective, MapSurjective" not in between
                or "if isinstance(statement, GeneratorImage)" not in between):
            raise RuntimeError("Typed map region changed")
        # Keep GeneratorImage handling unchanged.
        gen_start = between.index("    if isinstance(statement, GeneratorImage):\n")
        map_start = between.index("    if isinstance(statement, (MapInjective, MapSurjective")
        image_part = between[gen_start:map_start]
        code = code[:first] + image_part + code[second:]
    elif "    map_sentence = map_property_sentence(statement, step)\n" not in code:
        raise RuntimeError("Unexpected typed_sentence body")
    if "    map_sentence = map_property_sentence(statement, step)\n" not in code:
        code = code.replace(anchor, anchor +
            "    map_sentence = map_property_sentence(statement, step)\n"
            "    if map_sentence is not None:\n"
            "        return map_sentence\n", 1)
    # Delta map math is a single TeX command, not an escaped backslash pair.
    code = code.replace('        return r"\\\\Delta"\n', '        return r"\\Delta"\n')
    return code


def main() -> None:
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    print("R3Q1_GIT_BRANCH=" + branch)
    if branch != "develop":
        raise RuntimeError("R3Q requires develop")
    originals = [(RENDERER, RENDERER.read_text(encoding="utf-8-sig")),
                 (TYPED, TYPED.read_text(encoding="utf-8-sig"))]
    patched = [(RENDERER, originals[0][1], patch_renderer(originals[0][1])),
               (TYPED, originals[1][1], patch_typed(originals[1][1]))]
    for path, before, after in patched:
        ast.parse(after, filename=path.name)
        if path is RENDERER and "project_ehp_reasoned_lines" in after:
            raise RuntimeError("R3P path was not retired")
        if path is TYPED and after.count("def map_property_sentence(") != 1:
            raise RuntimeError("Duplicated map-property projector")
    OUTPUT.mkdir(exist_ok=True)
    for path, before, after in patched:
        backup = OUTPUT / (path.name + ".before")
        if before != after and backup.exists() and backup.read_text(encoding="utf-8") != before:
            raise RuntimeError("Existing backup differs from current pre-patch code: " + str(backup))
        if before != after and not backup.exists():
            backup.write_text(before, encoding="utf-8")
        (OUTPUT / (path.name + ".FULL")).write_text(after, encoding="utf-8")
        for fname in (["render_model_backed_narrative_markdown"] if path is RENDERER
                      else ["typed_sentence", "map_property_sentence", "map_symbol_tex"]):
            (OUTPUT / (fname + "_FULL.py")).write_text(whole_function(after, fname) + "\n", encoding="utf-8")
    for path, before, after in patched:
        if before != after:
            path.write_text(after, encoding="utf-8")
            print("R3Q1_PATCHED=" + path.name)
        else:
            print("R3Q1_ALREADY_INSTALLED=" + path.name)
    print("R3Q1_FULL_CODE=" + str(OUTPUT))
    print("R3Q1_PATCH_COMPLETE=True")


if __name__ == "__main__":
    main()
