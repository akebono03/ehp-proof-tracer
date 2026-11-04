"""Reviewed, exact-source transformations for Phase 173 R4-R15R12.

Pure transformations only. They neither read a proof database nor infer facts.
"""
from __future__ import annotations

import ast

REFERENCE_PATH = 'phase168_r3_37c_reference_projection.py'
MODEL_PATH = 'phase168_r3_3_proof_narrative_model.py'
WEB_PATH = 'web_group_proof_common.py'
TEST_PATH = 'phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py'
R4E_TEST_PATH = 'phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py'
CHANGED_PATHS = (REFERENCE_PATH, MODEL_PATH, WEB_PATH, TEST_PATH, R4E_TEST_PATH)


def _replace_exact(source: str, original: str, replacement: str, label: str) -> str:
    if source.count(original) != 1 or replacement in source:
        raise RuntimeError('Unreviewed or already-patched source: ' + label)
    return source.replace(original, replacement, 1)


def patch_reference(source: str) -> str:
    """Correct the typed Prop 4.4 text and project the cited Lemma 5.4 source."""
    original_import = (
        'from web_group_proof_common import _group_proof_statement_latex\n\n\n'
        'def project_reference_bodies(registry, assertion_ids):'
    )
    new_helpers = r'''from web_group_proof_common import _group_proof_statement_latex


def _verified_source_sentence(statement: object) -> str | None:
    """Render a fully source-screened typed statement without deducing a fact."""
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource

    if type(statement) is TodaLemma54TypedSource and statement == TodaLemma54TypedSource():
        return (
            r"$\nu_4\in\pi_7^4$, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$."
        )
    return None


def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Use an already cited GIVEN statement if registry links do not expose its body.

    The citation must already own the exact source step; simply finding a
    literature locator or a mathematically similar statement is insufficient.
    """
    from proof import LiteratureReference, ProofRule, ProofStep

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    candidates = tuple(
        (step, _verified_source_sentence(step.conclusion))
        for step in cited_steps
        if isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
        and not step.premises
    )
    verified = tuple(
        sentence for step, sentence in candidates
        if sentence is not None and locator == "Lemma 5.4"
    )
    return verified if len(verified) == 1 else ()


def project_reference_bodies(registry, assertion_ids):'''
    source = _replace_exact(source, original_import, new_helpers, 'reference helper placement')
    original = '''            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()
                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):
                sentence = (
                    r"Proposition 4.4 直前の記述（Steenrod1951 を引用）: "
                    r"$n=2,4,8$ では Hopf fibration "
                    r"$h:S^{2n-1}\\to S^n$ が存在する."
                    + "\\n"
                    r"$\\alpha\\in\\pi_{2n-1}^{n}$, "
                    r"$H(\\alpha)=\\pm\\iota_{2n-1}$ とすると, "
                    r"$E:\\pi_{i-1}^{n-1}\\to\\pi_i^{n}$ は単射."
                )
'''
    replacement = '''            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()
                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):
                sentence = (
                    r"$\\alpha\\in\\pi_{2n-1}^{n}$ で "
                    r"$H(\\alpha)=\\pm\\iota_{2n-1}$ とする."
                    "\\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\\n"
                    r"$\\pi_{i-1}^{n-1}\\oplus\\pi_i^{2n-1}"
                    r"\\xrightarrow{\\;\\cong\\;}\\pi_i^n,\\quad"
                    r"(\\beta,\\gamma)\\longmapsto E\\beta+\\alpha\\circ\\gamma$."
                    "\\n"
                    r"特に $E:\\pi_{i-1}^{n-1}\\to\\pi_i^{n}$ は単射である."
                )
'''
    source = _replace_exact(source, original, replacement, 'Proposition 4.4 body')
    anchor = '''        for statement in statements:
            sentence = None
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):'''
    updated = '''        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):'''
    source = _replace_exact(source, anchor, updated, 'typed source body entry')
    ast.parse(source)
    return source


def patch_model(source: str) -> str:
    """Copy body from a real, cited source-step when explicit link is absent."""
    original_import = '    from phase168_r3_37c_reference_projection import project_reference_bodies\n'
    new_import = '''    from phase168_r3_37c_reference_projection import (
        project_reference_bodies, project_cited_proof_step_reference_bodies,
    )
'''
    source = _replace_exact(source, original_import, new_import, 'model reference imports')
    original = '            statement_bodies=project_reference_bodies(registry, tuple(assertion_ids[i])),\n'
    replacement = '''            statement_bodies=(
                project_reference_bodies(registry, tuple(assertion_ids[i]))
                or project_cited_proof_step_reference_bodies(
                    reference, tuple(steps[j] for j in associations[i]),
                )
            ),
'''
    source = _replace_exact(source, original, replacement, 'model cited-source bodies')
    ast.parse(source)
    return source


def patch_web(source: str) -> str:
    """Let the common inline renderer interpret $...$ inside **...**."""
    original = '''    strong_value = line[position + 2:closing]
    segments.append(WebGroupProofInlineSegmentView(
      kind="strong" if strong_value else "text",
      value=strong_value if strong_value else "****",
    ))
    cursor = closing + 2
'''
    replacement = '''    strong_value = line[position + 2:closing]
    chunks = strong_value.split("$")
    if (len(chunks) > 1 and len(chunks) % 2 == 1
        and all(chunks[i] for i in range(1, len(chunks), 2))):
      for i, chunk in enumerate(chunks):
        if chunk:
          segments.append(WebGroupProofInlineSegmentView(
            kind="inline_math" if i % 2 else "strong", value=chunk,
          ))
    else:
      segments.append(WebGroupProofInlineSegmentView(
        kind="strong" if strong_value else "text",
        value=strong_value if strong_value else "****",
      ))
    cursor = closing + 2
'''
    source = _replace_exact(source, original, replacement, 'common strong+math parsing')
    ast.parse(source)
    return source

def patch_existing_test(source: str) -> str:
    """Update superseded R4G display assertions while retaining source gates."""
    start = 'def test_r4g_fibration_is_in_same_source_bound_reference(pi64):\n'
    end = '\n\ndef test_r4g_typed_prop44_cannot_accept_fake_fibration_metadata():'
    if source.count(start) != 1 or source.count(end) != 1:
        raise RuntimeError('Unreviewed R4G test function')
    before, suffix = source.split(start, 1)
    original_body, rest = suffix.split(end, 1)
    if (original_body.count('Proposition 4.4 直前の記述') != 1
            or original_body.count('Steenrod1951') != 0
            or original_body.count('assert text in reference') != 1):
        raise RuntimeError('Unreviewed R4G test assertions')
    rewritten = r'''def test_r4g_fibration_is_in_same_source_bound_reference(pi64):
    """Source prelude stays verified; Reference displays the proposition itself."""
    _, model, reference, body = pi64
    assert len(model.citations) == 5
    prop44 = [c for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    assert len(prop44) == 1
    citation = prop44[0]
    assert len(citation.assertion_ids) == 1
    assert len(citation.statement_bodies) == 1
    text = citation.statement_bodies[0]
    assert "Proposition 4.4 直前の記述" not in text
    assert "Steenrod1951" not in text
    assert r"$\alpha\in\pi_{2n-1}^{n}$" in text
    assert r"$H(\alpha)=\pm\iota_{2n-1}$" in text
    assert r"\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}" in text
    assert r"\xrightarrow{\;\cong\;}" in text
    assert r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma" in text
    assert r"E:\pi_{i-1}^{n-1}\to\pi_i^{n}" in text
    assert text in reference
    assert f"[R{citation.number}]より" in body
    assert r"$h:S^7\to S^4$" in body
    assert "Lemma 5.4" not in reference + body
    assert body.rstrip().endswith("□")
'''
    source = before + rewritten + end + rest
    source = _replace_exact(
        source,
        '    assert len(result.proven_steps) == 18',
        '    assert any(step.conclusion == result.conclusion for step in result.proven_steps)',
        'R4G first-success fixture',
    )
    source = _replace_exact(
        source,
        '    assert len(view.steps) == 18',
        '    assert len(view.steps) == len(pi64[0].proven_steps)',
        'R4G Web step cardinality',
    )
    source = _replace_exact(
        source,
        '    assert len(previous.proven_steps) == 28',
        '    assert any(step.conclusion == previous.conclusion for step in previous.proven_steps)',
        'R4G prior first-success proof',
    )
    old_check = '    assert any("Proposition 4.4 直前" in line for line in lines)'
    new_check = (
        '    assert any(r"\\xrightarrow{\\;\\cong\\;}" in line for line in lines)\n'
        '    assert not any("Proposition 4.4 直前" in line for line in lines)'
    )
    source = _replace_exact(source, old_check, new_check, 'R4G Web Reference test')
    ast.parse(source)
    return source


def patch_r4e_test(source: str) -> str:
    """Remove obsolete fixed proof-length assumptions, keep source and Web checks."""
    source = _replace_exact(
        source,
        '    assert len(result.proven_steps) == 18',
        '    assert any(step.conclusion == result.conclusion for step in result.proven_steps)',
        'R4E verified complete fixture',
    )
    source = _replace_exact(
        source,
        'def test_r4e_standard_web_path_remains_verified_and_complete():',
        'def test_r4e_standard_web_path_remains_verified_and_complete(pi64):',
        'R4E Web fixture usage',
    )
    source = _replace_exact(
        source,
        '    assert len(view.steps) == 18',
        '    assert len(view.steps) == len(pi64[0].proven_steps)',
        'R4E Web result consistency',
    )
    ast.parse(source)
    return source


def patch_source(path: str, content: bytes) -> bytes:
    """Patch only an explicitly reviewed module while retaining line endings."""
    if not isinstance(content, bytes):
        raise TypeError('content must be bytes')
    if path not in CHANGED_PATHS:
        raise ValueError('Unreviewed source path: ' + path)
    if b'\r\n' in content:
        if b'\n' in content.replace(b'\r\n', b''):
            raise RuntimeError('Mixed line endings in ' + path)
        normalized = content.replace(b'\r\n', b'\n')
        if b'\r' in normalized:
            raise RuntimeError('Mixed line endings in ' + path)
        newline = b'\r\n'
    else:
        normalized = content
        if b'\r' in normalized:
            raise RuntimeError('Unexpected CR in ' + path)
        newline = b'\n'
    text = normalized.decode('utf-8-sig')
    transforms = {
        REFERENCE_PATH: patch_reference,
        MODEL_PATH: patch_model,
        WEB_PATH: patch_web,
        TEST_PATH: patch_existing_test,
        R4E_TEST_PATH: patch_r4e_test,
    }
    modified = transforms[path](text).encode('utf-8')
    return modified if newline == b'\n' else modified.replace(b'\n', newline)


def changed_units(path: str, content: bytes) -> str:
    """Export full imports, whole modified classes/functions and new helpers."""
    source = patch_source(path, content).decode('utf-8-sig').replace('\r\n', '\n')
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    functions = {
        REFERENCE_PATH: ('_verified_source_sentence', 'project_cited_proof_step_reference_bodies', 'project_reference_bodies'),
        MODEL_PATH: ('build_proof_narrative_model',),
        WEB_PATH: ('_build_group_proof_inline_segments',),
        TEST_PATH: ('pi64', 'test_r4g_fibration_is_in_same_source_bound_reference',
                    'test_r4g_web_and_pi53_existing_route_unchanged'),
        R4E_TEST_PATH: ('pi64', 'test_r4e_standard_web_path_remains_verified_and_complete'),
    }[path]
    selected = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in functions]
    if len(selected) != len(functions):
        raise RuntimeError('Missing changed function in ' + path)
    first = min(node.lineno for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    header = ''.join(lines[:first-1])
    chunks = ['# ' + path, '', '## Complete imports and module prefix', '', '```python',
              header.rstrip(), '```', '']
    for name in functions:
        node = next(node for node in selected if node.name == name)
        start_line = min([node.lineno] + [deco.lineno for deco in node.decorator_list])
        chunks.extend(['## Complete function: ' + name, '', '```python',
                       ''.join(lines[start_line-1:node.end_lineno]).rstrip(), '```', ''])
    return '\n'.join(chunks)
