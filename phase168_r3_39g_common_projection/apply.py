"""R3-39G minimal, guarded edits of existing common narrative projection."""
from __future__ import annotations
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'output'
OUT.mkdir(exist_ok=True)


def replace_function(path: str, name: str, edit):
    file = ROOT / path
    source = file.read_text(encoding='utf-8')
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    lines = source.splitlines(keepends=True)
    old = ''.join(lines[node.lineno - 1:node.end_lineno])
    new = edit(old)
    if new == old:
        raise RuntimeError('No change for ' + path + ':' + name)
    ast.parse(new)
    lines[node.lineno - 1:node.end_lineno] = [new.rstrip('\n') + '\n']
    file.write_text(''.join(lines), encoding='utf-8')
    (OUT / (path + '_' + name + '_FULL.py')).write_text(new.rstrip() + '\n', encoding='utf-8')
    print('PATCHED', path, name)


def typed(old):
    needle = '''    if isinstance(statement, TodaDeltaZeroStatement):
'''
    assert old.count(needle) == 1
    # The current delta-zero typed inference expresses a certified exactness consequence.
    old = old.replace('''return (rf"完全性と懸垂写像の同型性より, "
                        rf"$\\Delta: {source}\\to {target}$ は零写像である.")''', '''return (rf"完全性より, $\\operatorname{{Im}}\\Delta=\\ker E=0$ なので, "
                        rf"$\\Delta: {source}\\to {target}$ は零写像である.")''')
    target = '''            return rf"${symbol}: {source}\\to {target}$ は{label}."'''
    assert old.count(target) == 1
    replacement = '''            # Wording is justified only by the typed inference represented in
            # the Proof Tree, not by the goal's dimension or a source lookup.
            from proof import ProofRule
            if step is not None and step.rule is ProofRule.INFERENCE:
                if isinstance(statement, (MapInjective, MapSurjective)):
                    if step.premises and any(
                        "exact" in str(getattr(p.inference_rule, "name", "")).lower()
                        or isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement))
                        for p in step.premises
                    ):
                        return rf"完全性より, ${symbol}: {source}\\to {target}$ は{label}である."
                    # An EHP surjectivity or injectivity inference can have
                    # exactness deeper than its immediate typed premises.
                    def has_exactness(p, seen):
                        if id(p) in seen:
                            return False
                        seen.add(id(p))
                        if isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement)):
                            return True
                        return any(has_exactness(q, seen) for q in p.premises)
                    if any(has_exactness(p, set()) for p in step.premises):
                        return rf"完全性より, ${symbol}: {source}\\to {target}$ は{label}である."
                if isinstance(statement, (MapIsomorphism, TodaSuspensionIsomorphismStatement)):
                    has_inj = any(isinstance(p.conclusion, MapInjective) for p in step.premises)
                    has_surj = any(isinstance(p.conclusion, MapSurjective) for p in step.premises)
                    if has_inj and has_surj:
                        return rf"単射性と全射性より, ${symbol}: {source}\\to {target}$ は同型である."
            return rf"${symbol}: {source}\\to {target}$ は{label}."'''
    return old.replace(target,replacement)


def ordered(old):
    anchor = '    held = {i for group in postponed.values() for i in group}\n'
    assert old.count(anchor) == 1
    insert = '''    # Delay an already-present generator image until its source group and
    # typed suspension isomorphism have been presented. No steps are added.
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from homotopy_groups import TodaSuspensionMap, TodaIteratedSuspensionMap
    from toda_rules import Toda45IsomorphismStatement
    for index, step in enumerate(model.steps):
        statement = step.conclusion
        if not isinstance(statement, (GeneratorImage, GeneratorSuspension)):
            continue
        if not isinstance(statement.map, TodaSuspensionMap):
            continue
        source_index = next((j for j in range(index + 1, len(model.steps))
                             if getattr(model.steps[j].conclusion, "lhs", None)
                             == statement.map.source_group), None)
        iso_index = next((j for j in range(index + 1, len(model.steps))
                          if isinstance(model.steps[j].conclusion, Toda45IsomorphismStatement)
                          and isinstance(getattr(model.steps[j].conclusion, "map", None), TodaIteratedSuspensionMap)
                          and model.steps[j].conclusion.map.exponent == 1
                          and model.steps[j].conclusion.map.source_group == statement.map.source_group
                          and model.steps[j].conclusion.map.target_group == statement.map.target_group), None)
        if source_index is not None and iso_index is not None:
            postponed.setdefault(max(source_index, iso_index), []).append(index)
'''
    # Existing postponed entries are reserved for quotient statements; both can coexist.
    return old.replace(anchor,insert+anchor)


def reference(old):
    needle='''        if sentence is not None and sentence not in result:
'''
    assert old.count(needle)==1
    addon='''        # The diagonal group formula is a schema; its applicability is part
        # of the cited statement, not an optional display decoration.
        if (sentence is not None and "\\\\pi_{n}^{n}" in sentence
                and "\\\\mathbb{Z}" in sentence and "n\\\\ge" not in sentence):
            sentence = sentence.removesuffix(".") + r"\\quad(n\\ge 1)$." if sentence.endswith("$.") else sentence
'''
    # Replace $ terminator correctly rather than add expression after math closing.
    addon='''        if (sentence is not None and r"\\pi_{n}^{n}" in sentence
                and r"\\mathbb{Z}" in sentence and r"n\\ge" not in sentence
                and sentence.endswith("$.")):
            sentence = sentence[:-2] + r"\\quad(n\\ge 1)$."
'''
    return old.replace(needle,addon+needle)


def renderer(old):
    needle = '''    for entry in order:
'''
    assert old.count(needle) == 1
    updated = '''    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from expression import ScalarSymbol
    for entry in order:
'''
    old = old.replace(needle, updated)
    needle = '''        step = model.steps[index]
'''
    assert old.count(needle) == 1
    updated = '''        step = model.steps[index]
        # The symbolic circle theorem belongs in Reference; the proof uses
        # its certified integer specialization and must not lose i > 1.
        statement = step.conclusion
        if (isinstance(statement, TodaPrimaryGroupZeroStatement)
                and statement.group.sphere_dimension == 1
                and isinstance(statement.group.group_dimension, ScalarSymbol)):
            continue
'''
    return old.replace(needle, updated)


if __name__ == '__main__':
    replace_function('phase168_r3_27_typed_statement_projection.py', 'typed_sentence', typed)
    replace_function('phase168_r3_29_order_projection.py', 'project_narrative_order', ordered)
    replace_function('phase168_r3_37c_reference_projection.py', 'project_reference_bodies', reference)
    replace_function('phase168_r3_5_model_renderer.py', 'render_model_backed_narrative_markdown', renderer)
