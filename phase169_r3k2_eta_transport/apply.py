"""R3K2: guarded renderer-only patch installed into the existing repository."""
from __future__ import annotations

import ast
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


ELEMENT_TEX_FUNCTION = r'''def element_tex(value):
    """Render only supported generators; normalize typed consecutive eta composites."""
    from expression import Composition

    if isinstance(value, Multiple) and type(value.coefficient) is int:
        inner = element_tex(value.expression)
        return f"{value.coefficient}{inner}" if inner is not None else None
    if isinstance(value, Composition):
        left, right = value.left, value.right
        if not (isinstance(left, HomotopyElement)
                and isinstance(right, HomotopyElement)):
            return None
        left_symbol = getattr(left, "generator", None)
        right_symbol = getattr(right, "generator", None)
        left_index = (getattr(left_symbol, "index", None) if left_symbol is not None
                      else (left.dimension if left.name == "η" else None))
        right_index = (getattr(right_symbol, "index", None) if right_symbol is not None
                       else (right.dimension if right.name == "η" else None))
        left_eta = (left_symbol.family == "η" if left_symbol is not None
                    else left.name == "η")
        right_eta = (right_symbol.family == "η" if right_symbol is not None
                     else right.name == "η")
        if (type(left_index) is int and type(right_index) is int
                and left_eta and right_eta
                and getattr(left_symbol, "decoration", None) is None
                and getattr(right_symbol, "decoration", None) is None
                and right_index == left_index + 1
                and element_tex(left) == rf"\eta_{{{left_index}}}"
                and element_tex(right) == rf"\eta_{{{right_index}}}"):
            return rf"\eta_{{{left_index}}}^{{2}}"
        return None
    if isinstance(value, HomotopyElement):
        symbol = value.generator
        if symbol is not None and type(symbol.index) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}.get(symbol.family)
            if family is not None:
                return f"{family}_{{{symbol.index}}}"
        if value.name in ("η", "ι", "ν", "σ") and type(value.dimension) is int:
            family = {"η": r"\eta", "ι": r"\iota", "ν": r"\nu", "σ": r"\sigma"}[value.name]
            return f"{family}_{{{value.dimension}}}"
    return None
'''

SUPPRESS_TRANSPORT_INTERMEDIATES = '''    # A certified composite GeneratorImage incorporates its two verified
    # generator-suspension premises. Suppress their separate prose only when
    # they are uncited, used by that image alone, and its eta-square image
    # can actually be displayed. No ProofSteps or citations are discarded.
    if not incomplete:
        for image_index in order:
            image_step = model.steps[image_index]
            image = image_step.conclusion
            if (image_step.rule is not ProofRule.INFERENCE
                    or not isinstance(image, GeneratorImage)
                    or not isinstance(image.map, TodaSuspensionMap)
                    or len(image_step.premises) != 2
                    or element_tex(image.source_generator) is None
                    or element_tex(image.target_generator) is None
                    or not cited_general_ancestor_numbers(
                        image_step, TodaEtaFamilyGeneralDefinition
                    )
                    or not all(isinstance(parent.conclusion, GeneratorSuspension)
                               for parent in image_step.premises)):
                continue
            for parent in image_step.premises:
                parent_index = unique_step_index(parent)
                if (parent_index is not None and parent_index in order
                        and parent_index != model.root_index
                        and parent.rule is ProofRule.INFERENCE
                        and not model.step_citation_numbers[parent_index]
                        and only_consumed_by(parent, image_step)):
                    suppressed_body_indices.add(parent_index)
'''

OLD_ETA_SOURCE = '''                            if (isinstance(statement, GeneratorSuspension)
                                and _eta_pair(statement) is not None)
                            else ()'''
NEW_ETA_SOURCE = '''                            if ((isinstance(statement, GeneratorSuspension)
                                 and _eta_pair(statement) is not None)
                                or (isinstance(statement, GeneratorImage)
                                    and isinstance(statement.map, TodaSuspensionMap)
                                    and element_tex(statement.source_generator) is not None
                                    and element_tex(statement.target_generator) is not None))
                            else ()'''


def extract_function(source: str, function_name: str) -> tuple[ast.FunctionDef, str]:
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one function: {function_name}")
    node = matches[0]
    lines = source.splitlines(keepends=True)
    return node, "".join(lines[node.lineno - 1:node.end_lineno])


def replace_whole_function(source: str, name: str, replacement: str) -> str:
    node, _ = extract_function(source, name)
    lines = source.splitlines(keepends=True)
    new_lines = replacement.rstrip() + "\n"
    return "".join(lines[:node.lineno - 1]) + new_lines + "".join(lines[node.end_lineno:])


def patch_renderer(func: str) -> str:
    original = func
    import_line = "    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension\n"
    if func.count(import_line) != 1:
        raise RuntimeError("R3K2 renderer import anchor changed")
    if "from phase165_r14_r6_generic_iso import GeneratorImage" not in func:
        func = func.replace(import_line, import_line +
                            "    from phase165_r14_r6_generic_iso import GeneratorImage\n", 1)
    locator = "        locator = citation.reference.locator or citation.reference.label\n"
    if func.count(locator) != 1:
        raise RuntimeError("R3K2 citation locator anchor changed")
    func = func.replace(locator, locator +
        '        if locator == "Chapter V, i)":\n'
        '            locator = "η 系列の定義（Chapter V, i）"\n', 1)
    if func.count(OLD_ETA_SOURCE) != 1:
        raise RuntimeError("R3K2 typed-eta citation anchor changed")
    func = func.replace(OLD_ETA_SOURCE, NEW_ETA_SOURCE, 1)
    # The former import-text anchor matches both 4-space and 8-space
    # indentation in R3K; locate the unique top-level body loop instead.
    body_loop = "    for index in order:\n"
    if func.splitlines(keepends=True).count(body_loop) != 1:
        raise RuntimeError("R3K2 body-loop anchor changed")
    if ("    def unique_step_index(premise):\n" not in func
            or "    def only_consumed_by(candidate, consumer):\n" not in func
            or "    displayed_cyclic_math = set()\n" not in func):
        raise RuntimeError("R3K2 R3K suppression dependencies changed")
    func = func.replace(body_loop, SUPPRESS_TRANSPORT_INTERMEDIATES + body_loop, 1)
    if func == original:
        raise RuntimeError("No renderer changes applied")
    ast.parse(func)
    return func


def main() -> None:
    if Path.cwd().resolve() != ROOT.resolve():
        raise RuntimeError("Run R3K2 from repository root")
    if not (ROOT / ".git").exists():
        raise RuntimeError("Not inside the Git repository")
    if not (ROOT / "phase169_r3k_narrative_projection.py").is_file():
        raise RuntimeError("R3K implementation must be installed before R3K2")
    report = ROOT / "phase169_r3k_narrative_localization/output/pi5_3_after_audit.json"
    if not report.is_file():
        raise RuntimeError("R3K audited output is missing")
    import json
    state = json.loads(report.read_text(encoding="utf-8-sig"))
    if not (state.get("status") == "complete" and state.get("all_citations_mentioned", True)):
        raise RuntimeError("R3K result has not passed the expected audit")
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError(f"Expected develop, got {branch}")
    print("R3K2_GIT_BRANCH=develop")
    print("R3K2_PREFLIGHT_OK=True")
    typed_file = ROOT / "phase168_r3_27_typed_statement_projection.py"
    renderer_file = ROOT / "phase168_r3_5_model_renderer.py"
    typed_original = typed_file.read_text(encoding="utf-8-sig")
    renderer_original = renderer_file.read_text(encoding="utf-8-sig")
    _, old_element = extract_function(typed_original, "element_tex")
    if "if isinstance(value, Composition):" in old_element:
        raise RuntimeError("element_tex already handles Composition; inspect first")
    if 'def element_tex(value):' not in old_element:
        raise RuntimeError("element_tex baseline changed")
    _, renderer_func = extract_function(renderer_original, "render_model_backed_narrative_markdown")
    if "project_proven_map_property" not in renderer_func:
        raise RuntimeError("R3K local renderer does not appear installed")
    new_typed = replace_whole_function(typed_original, "element_tex", ELEMENT_TEX_FUNCTION)
    new_renderer_func = patch_renderer(renderer_func)
    new_renderer = replace_whole_function(renderer_original,
                                          "render_model_backed_narrative_markdown",
                                          new_renderer_func)
    ast.parse(new_typed)
    ast.parse(new_renderer)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    backups = [(typed_file, typed_original), (renderer_file, renderer_original)]
    for path, previous in backups:
        (OUTPUT / (path.name + ".before")).write_text(previous, encoding="utf-8")
    (OUTPUT / "element_tex.full.py").write_text(ELEMENT_TEX_FUNCTION, encoding="utf-8")
    (OUTPUT / "render_model_backed_narrative_markdown.full.py").write_text(new_renderer_func, encoding="utf-8")
    (OUTPUT / "phase168_r3_27_typed_statement_projection.py.full.py").write_text(new_typed, encoding="utf-8")
    (OUTPUT / "phase168_r3_5_model_renderer.py.full.py").write_text(new_renderer, encoding="utf-8")
    typed_file.write_text(new_typed, encoding="utf-8")
    renderer_file.write_text(new_renderer, encoding="utf-8")
    print("R3K2_PATCHED=" + typed_file.name)
    print("R3K2_PATCHED=" + renderer_file.name)
    print("R3K2_FULL_FUNCTIONS=" + str(OUTPUT))
    print("R3K2_PATCH_COMPLETE=True")


if __name__ == "__main__":
    main()
