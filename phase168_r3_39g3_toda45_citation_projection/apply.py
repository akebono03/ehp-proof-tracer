"""Phase 168 R3-39G-3: reuse typed specialization and explicit proof citations."""
from __future__ import annotations

import ast
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
FULL = PACKAGE / "full_functions"
FULL.mkdir(exist_ok=True)

PROJECTION = "phase168_r3_27_typed_statement_projection.py"
RENDERER = "phase168_r3_5_model_renderer.py"


def function_text(source: str, name: str) -> tuple[str, ast.FunctionDef]:
    tree = ast.parse(source)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("Expected exactly one top-level function: " + name)
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno]), node


def replace_function(source: str, name: str, revised: str) -> str:
    old, node = function_text(source, name)
    if old == revised:
        raise RuntimeError("No function change: " + name)
    ast.parse(revised)
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [revised.rstrip("\n") + "\n"]
    result = "".join(lines)
    ast.parse(result)
    return result


def replace_once(text: str, before: str, after: str, description: str) -> str:
    if text.count(before) != 1:
        raise RuntimeError("Unexpected current function for " + description)
    return text.replace(before, after)


def patch_projection(source: str) -> str:
    if "def toda45_specialization_evidence(" in source:
        raise RuntimeError("Evidence helper already exists: refusing duplicate installation")
    old, _ = function_text(source, "typed_sentence")
    anchor = "                return rf'${symbol}: {source}\\to {target}$ は同型である.'"
    replacement = """                evidence = toda45_specialization_evidence(step)
                if evidence is not None:
                    _, bindings = evidence
                    values = dict(bindings)
                    return (
                        rf'$(n,m,k)=({values["n"]},{values["m"]},{values["k"]})$ '
                        rf'に適用すると, ${symbol}: {source}\\to {target}$ は同型である.'
                    )
                return rf'${symbol}: {source}\\to {target}$ は同型である.'"""
    changed = replace_once(old, anchor, replacement, "typed Toda (4.5) sentence")
    source = replace_function(source, "typed_sentence", changed)
    header = "def typed_sentence(statement, step):\n"
    helper = '''def toda45_specialization_evidence(step):
    """Return a general cited Toda (4.5) ancestor and checked scalar bindings.

    Only traverse existing ProofStep premises. The existing specialization
    validator supplies all equalities and stable-range checks.
    """
    from proof import ProofRule
    from toda_rules import Toda45IsomorphismStatement
    from phase165_r57_r20_general_specialization import specialize_typed_statement

    if (step is None or step.rule is not ProofRule.INFERENCE
            or not isinstance(step.conclusion, Toda45IsomorphismStatement)):
        return None

    visited = set()

    def find_source(node):
        if id(node) in visited:
            return None
        visited.add(id(node))
        for parent in node.premises:
            if (parent.rule is ProofRule.GIVEN
                    and isinstance(parent.conclusion, Toda45IsomorphismStatement)):
                bindings = specialize_typed_statement(parent.conclusion, step.conclusion)
                if bindings is not None and {"n", "m", "k"}.issubset(dict(bindings)):
                    return parent, bindings
            candidate = find_source(parent)
            if candidate is not None:
                return candidate
        return None

    return find_source(step)


'''
    if source.count(header) != 1:
        raise RuntimeError("Unexpected typed_sentence placement")
    citation_projection = '''def project_toda45_specialization_citation_numbers(model, step_index):
    """Bind Toda (4.5) citations only to their used general Proof Step."""
    step = model.steps[step_index]
    evidence = toda45_specialization_evidence(step)
    if evidence is None:
        return ()
    source_step, _ = evidence
    numbers = []
    for source_index, candidate in enumerate(model.steps):
        if candidate != source_step:
            continue
        for number in model.step_citation_numbers[source_index]:
            if number not in numbers:
                numbers.append(number)
    return tuple(numbers)


'''
    source = source.replace(header, helper + citation_projection + header)
    ast.parse(source)
    (FULL / "toda45_specialization_evidence_FULL.py").write_text(helper, encoding="utf-8")
    (FULL / "project_toda45_specialization_citation_numbers_FULL.py").write_text(
        citation_projection, encoding="utf-8"
    )
    (FULL / "typed_sentence_FULL.py").write_text(changed.rstrip() + "\n", encoding="utf-8")
    return source


def patch_renderer(source: str) -> str:
    old, _ = function_text(source, "render_model_backed_narrative_markdown")
    old_import = "    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence\n"
    new_import = ("    from phase168_r3_27_typed_statement_projection import (\n"
                  "        group_tex, typed_sentence, toda45_specialization_evidence,\n"
                  "    )\n")
    changed = replace_once(old, old_import, new_import, "renderer local imports")
    before = '''                if tags and step.rule is ProofRule.GIVEN:
                    sentence = f"{tags}より, " + sentence
                lines.extend((sentence, ""))'''
    after = '''                if tags and step.rule is ProofRule.GIVEN:
                    sentence = f"{tags}より, " + sentence
                elif step.rule is ProofRule.INFERENCE:
                    sourced_numbers = project_toda45_specialization_citation_numbers(
                        model, index
                    )
                    if sourced_numbers:
                        source_tags = ", ".join(
                            f"[R{number}]" for number in sourced_numbers
                        )
                        sentence = f"{source_tags}を " + sentence
                lines.extend((sentence, ""))'''
    changed = replace_once(changed, before, after, "typed-only citation binding")
    if "for postponed in entry.after_indices" not in changed:
        raise RuntimeError("R3-39G-1 postponed rendering fix has not been applied")
    source = replace_function(source, "render_model_backed_narrative_markdown", changed)
    (FULL / "render_model_backed_narrative_markdown_FULL.py").write_text(changed.rstrip() + "\n", encoding="utf-8")
    return source


def main() -> None:
    # Preflight every edit and parse every output BEFORE writing any target.
    files = ((PROJECTION, patch_projection), (RENDERER, patch_renderer))
    replacements = []
    for relative, patcher in files:
        path = PROJECT / relative
        original = path.read_text(encoding="utf-8")
        revised = patcher(original)
        if original == revised:
            raise RuntimeError("No changes generated: " + relative)
        replacements.append((path, revised))
    for path, revised in replacements:
        path.write_text(revised, encoding="utf-8")
        print("PATCHED", path.name)
    print("FULL_FUNCTIONS:", FULL)


if __name__ == "__main__":
    main()
