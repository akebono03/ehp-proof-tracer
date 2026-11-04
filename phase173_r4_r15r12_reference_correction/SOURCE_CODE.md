# Phase 173 R4-R15R12R2 — 配布ソースコード全文

本パッケージで配布する全 Python / PowerShell ファイルを、import を含めて省略せず記載する。

変更される本番関数・既存テスト関数の全文は、DryRun の `FULL_CHANGED_UNITS.md` に別途生成される。

変更対象は、本番3ファイル、既存テスト2ファイルであり、R15R12R2 は配布側 `patch_existing_test` と `tests/test_static.py` のみの追加修正である。

## `__init__.py`

```python
"""Phase 173 R4-R15R12: citation-backed common Reference rendering."""
```

## `patch.py`

```python
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
```

## `install.py`

```python
"""Fail-closed installer for reviewed reference projection and Web math fixes."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess

from .patch import CHANGED_PATHS, changed_units, patch_source

EXPECTED_HEAD = 'e2996ec2ff496203f94daa9bc22550c5e69a6b11'
EXPECTED_BLOBS = {
    'phase168_r3_37c_reference_projection.py': '63c10c79a94df66e6b3f9ed9e2ad9d81f39f481e',
    'phase168_r3_3_proof_narrative_model.py': '2e8def26cfdd9444d480f149e0ae7a2c2d53b525',
    'web_group_proof_common.py': '2a7b6f47a6445f6b4c51d6eeeffa7645d2a48e1f',
    'phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py': '7970809e62c3a334210498550df9b6ca296b68f4',
    'phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py': '1ddb4a47322799f3b3eaaa5705da5316ad57007b',
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ('git', *args), cwd=root, check=True, capture_output=True,
        text=True, encoding='utf-8', errors='replace',
    )
    return completed.stdout.strip()


def preflight(root: Path) -> dict[str, tuple[bytes, bytes]]:
    root = root.resolve()
    if git(root, 'branch', '--show-current') != 'develop':
        raise RuntimeError('R15R12 requires branch develop')
    head = git(root, 'rev-parse', 'HEAD')
    remote = git(root, 'rev-parse', 'origin/develop')
    if head != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError(
            f'Unreviewed HEAD: local={head}, remote={remote}; expected {EXPECTED_HEAD}'
        )
    if git(root, 'diff', '--cached', '--name-only'):
        raise RuntimeError('Staged source changes require review')
    updated: dict[str, tuple[bytes, bytes]] = {}
    for rel in CHANGED_PATHS:
        path = root / rel
        if not path.is_file():
            raise RuntimeError('Missing reviewed file: ' + rel)
        blob = git(root, 'hash-object', f'--path={rel}', rel)
        if blob != EXPECTED_BLOBS[rel]:
            raise RuntimeError(f'Unreviewed or already patched file: {rel}: {blob}')
        old = path.read_bytes()
        new = patch_source(rel, old)
        if old == new:
            raise RuntimeError('Patch did not change ' + rel)
        updated[rel] = (old, new)
    return updated


def full_units(root: Path, updates: dict[str, tuple[bytes, bytes]]) -> None:
    output = root / 'phase173_r4_r15r12_reference_correction' / 'FULL_CHANGED_UNITS.md'
    chunks = ['# R15R12 Complete changed units', '',
              'All modified functions and their complete module imports appear below.', '']
    for rel in CHANGED_PATHS:
        chunks.extend((changed_units(rel, updates[rel][0]), ''))
    output.write_text('\n'.join(chunks) + '\n', encoding='utf-8')
    print('PHASE173_R4_R15R12_FULL_CHANGED_UNITS=' + str(output), flush=True)


def install(root: Path) -> None:
    updates = preflight(root)
    directory = root / 'phase173_r4_r15r12_reference_correction'
    backups = directory / 'backups'
    state_path = directory / 'installed_state.json'
    if state_path.exists():
        raise RuntimeError('Prior R15R12 installation state already exists')
    backups.mkdir(parents=True, exist_ok=True)
    for rel, (original, _) in updates.items():
        target = backups / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(original)
    written = []
    try:
        for rel, (_, updated) in updates.items():
            target = root / rel
            temp = target.with_name(target.name + '.r15r12.tmp')
            try:
                temp.write_bytes(updated)
                os.replace(temp, target)
            finally:
                if temp.exists():
                    temp.unlink()
            written.append(rel)
        state_path.write_text(json.dumps({
            'expected_head': EXPECTED_HEAD,
            'changed_files': list(CHANGED_PATHS),
            'production_file_count': len(CHANGED_PATHS),
        }, indent=2) + '\n', encoding='utf-8')
    except Exception:
        for rel in reversed(written):
            (root / rel).write_bytes((backups / rel).read_bytes())
        raise
    full_units(root, updates)
    print('PHASE173_R4_R15R12R1_PATCHED_FILES=5', flush=True)


def restore(root: Path) -> None:
    directory = root / 'phase173_r4_r15r12_reference_correction'
    state_path = directory / 'installed_state.json'
    if not state_path.is_file():
        raise RuntimeError('No R15R12 installation to restore')
    state = json.loads(state_path.read_text(encoding='utf-8'))
    if state.get('expected_head') != EXPECTED_HEAD or tuple(state.get('changed_files', ())) != CHANGED_PATHS:
        raise RuntimeError('Invalid R15R12 state file')
    backups = directory / 'backups'
    for rel in CHANGED_PATHS:
        backup = backups / rel
        if not backup.is_file():
            raise RuntimeError('Missing backup: ' + rel)
        # Refuse to overwrite subsequent user edits: expected patch has to match.
        current = (root / rel).read_bytes()
        if current != patch_source(rel, backup.read_bytes()):
            raise RuntimeError('Production file changed after installation: ' + rel)
    for rel in CHANGED_PATHS:
        (root / rel).write_bytes((backups / rel).read_bytes())
    state_path.unlink()
    print('PHASE173_R4_R15R12_RESTORED=PASS', flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--install', action='store_true')
    mode.add_argument('--restore', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.restore:
        restore(root)
    elif args.dry_run:
        updates = preflight(root)
        full_units(root, updates)
        print('PHASE173_R4_R15R12_SOURCE_GUARD=PASS', flush=True)
        print('PHASE173_R4_R15R12_DRY_RUN=PASS', flush=True)
        print('PHASE173_R4_R15R12_PRODUCTION_EDIT=NONE', flush=True)
    else:
        install(root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## `audit.py`

```python
"""Focused, public Web audit for general reference formatting and proof status."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


def inspect_complete(n: int, k: int) -> dict[str, object]:
    """Use the real typed search and inspect source-backed Reference output."""
    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise RuntimeError(f'Expected a completed source-first proof n={n}, k={k}')
    model = build_linked_proof_narrative_model(result, contexts[-1])
    markdown = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode='narrative', citation_source='model',
    )
    if view.key != 'generic-complete-proof' or view.partial_result:
        raise RuntimeError('A completed proof changed status')
    prop44 = [c for c in model.citations if
              (c.reference.locator or c.reference.label) == 'Proposition 4.4']
    lemma54 = [c for c in model.citations if
               (c.reference.locator or c.reference.label) == 'Lemma 5.4']
    prop_correct = all(
        any(r'\xrightarrow{\;\cong\;}' in s and r'\alpha\circ\gamma' in s
            for s in c.statement_bodies)
        for c in prop44
    ) and 'Steenrod1951' not in markdown
    lemma_correct = all(
        any(r'H(\nu_4)=\iota_7' in s and r"2E\nu_4=E^2\nu'" in s
            for s in c.statement_bodies)
        for c in lemma54
    )
    prior_rendered = any(
        any(segment.kind == 'inline_math' and r'\pi_{' in segment.value
            for segment in line.segments)
        and any('先行データベース結果' in segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    row = {
        'n': n, 'k': k,
        'source_reference_count': len(model.citations),
        'prop44_body_present': bool(prop44) and prop_correct,
        'lemma54_body_present': bool(lemma54) and lemma_correct,
        'prior_db_tex_rendered': prior_rendered,
        'named_complete': True,
        'open_goals': len(result.open_goals),
    }
    row['passed'] = all((row['prop44_body_present'], row['lemma54_body_present'],
                         row['prior_db_tex_rendered'], not result.open_goals))
    print(f'PHASE173_R4_R15R12_N={n}_K={k} ' +
          f'PROP44={row["prop44_body_present"]} LEMMA54={row["lemma54_body_present"]} '
          f'DB_TEX={prior_rendered} COMPLETE={row["named_complete"]}', flush=True)
    return row


def inspect_partial(k: int) -> dict[str, object]:
    """Do not promote abstract-only results into named-generator proofs."""
    goal = exact_prior_database_result(4, k)
    if goal is None:
        raise RuntimeError('Registered target is missing')
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode='narrative', citation_source='model',
    )
    headings = [line.prefix for line in view.rendered_lines if line.kind == 'heading']
    passed = (
        result.abstract_structure is not None
        and result.conclusion is None
        and result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and bool(result.open_goals)
        and view.key == 'generic-partial-proof' and view.partial_result
        and headings.count('証明済みの抽象群構造') == 1
    )
    row = {'k': k, 'open_goals': len(result.open_goals), 'named_pending': passed,
           'abstract_heading_count': headings.count('証明済みの抽象群構造'),
           'passed': passed}
    print(f'PHASE173_R4_R15R12_K={k} NAMED_PENDING={passed} '
          f'OPEN_GOALS={len(result.open_goals)}', flush=True)
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    completed = [inspect_complete(4, k) for k in (3, 4, 7)]
    partial = [inspect_partial(k) for k in (8, 31)]
    passed = all(row['passed'] for row in completed + partial)
    data = {
        'phase': '173-R4-R15R12',
        'head_reviewed': 'e2996ec2ff496203f94daa9bc22550c5e69a6b11',
        'completed': completed,
        'partial': partial,
        'full_pytest_performed': False,
        'proof_search_changed': False,
        'passed': passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE173_R4_R15R12_AUDIT=' + ('PASS' if passed else 'FAIL'), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 fetch failed' }
    python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 source guard failed' }
    python -m pytest -q -p no:cacheprovider phase173_r4_r15r12_reference_correction/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R12 static tests failed' }
    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R12_DRY_RUN_TESTS=PASS'
        Write-Output 'PHASE173_R4_R15R12R2_STATIC_PYTEST=PASS'
        Write-Output 'PHASE173_R4_R15R12_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --install
        if ($LASTEXITCODE -ne 0) { throw 'R15R12 installation failed' }
        try {
            python -m pytest -q -p no:cacheprovider `
                phase173_r4_r15r12_reference_correction/tests/test_integration.py `
                phase172_r5_prior_reference_display/tests/test_projection.py `
                phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py `
                phase169_r4e_citation_binding/tests/test_r4e_citation_binding.py `
                phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 focused tests failed' }
            Write-Output 'PHASE173_R4_R15R12_FOCUSED_PYTEST=PASS'
            Write-Output 'PHASE173_R4_R15R12R2_FOCUSED_PYTEST=PASS'
            python -m phase173_r4_r15r12_reference_correction.audit `
                --output (Join-Path $PSScriptRoot 'reference_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 Web audit failed' }
            Write-Output 'PHASE173_R4_R15R12_PHASE_COMPLETED=False'
            Write-Output 'PHASE173_R4_R15R12R2_AUDIT=PASS'
        } catch {
            python -m phase173_r4_r15r12_reference_correction.install --root "$RepoRoot" --restore
            if ($LASTEXITCODE -ne 0) { throw 'R15R12 rollback requires manual inspection' }
            throw
        }
    }
} finally {
    Pop-Location
}
```

## `tests/__init__.py`

```python
"""R15R12 focused tests."""
```

## `tests/test_static.py`

```python
"""Patch safety, reviewed AST scopes, and isolated Web inline-math behavior."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

import pytest

from phase173_r4_r15r12_reference_correction.install import preflight
from phase173_r4_r15r12_reference_correction.patch import (
    CHANGED_PATHS,
    MODEL_PATH,
    REFERENCE_PATH,
    WEB_PATH,
    R4E_TEST_PATH,
    TEST_PATH,
    patch_source,
)


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def reviewed_sources():
    return preflight(ROOT)


def test_reviewed_patch_changes_five_files(reviewed_sources) -> None:
    assert tuple(reviewed_sources) == CHANGED_PATHS
    assert len(CHANGED_PATHS) == 5
    for path, (before, after) in reviewed_sources.items():
        assert before != after
        ast.parse(after.decode('utf-8-sig'))
        with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
            patch_source(path, after)


def test_prop44_typing_and_unnecessary_prelude_removed(reviewed_sources) -> None:
    before, after = reviewed_sources[REFERENCE_PATH]
    assert 'Proposition 4.4 直前の記述（Steenrod1951 を引用）' in before.decode('utf-8-sig')
    updated = after.decode('utf-8-sig')
    assert 'Steenrod1951' not in updated
    assert r'\alpha\circ\gamma' in updated
    assert r'\xrightarrow{\;\cong\;}' in updated
    assert 'project_cited_proof_step_reference_bodies' in updated


def test_model_uses_only_cited_proof_steps(reviewed_sources) -> None:
    _, after = reviewed_sources[MODEL_PATH]
    text = after.decode('utf-8-sig')
    assert 'project_cited_proof_step_reference_bodies(' in text
    assert 'tuple(steps[j] for j in associations[i])' in text
    assert 'project_reference_bodies(registry, tuple(assertion_ids[i]))' in text


def test_strong_reference_math_is_parsed_not_displayed_verbatim(reviewed_sources) -> None:
    _, after = reviewed_sources[WEB_PATH]
    tree = ast.parse(after.decode('utf-8-sig'))
    node = next(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef)
        and item.name == '_build_group_proof_inline_segments'
    )

    @dataclass(frozen=True)
    class Segment:
        kind: str
        value: str

    namespace = {'WebGroupProofInlineSegmentView': Segment}
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    exec(compile(module, '<reviewed-web-inline>', 'exec'), namespace)
    render = namespace['_build_group_proof_inline_segments']
    sample = r'**[R2] 先行データベース結果 $\pi_{6}^{3}$（sphere.csv, n=3, k=3）.**'
    segments = render(sample)
    assert sum(segment.kind == 'inline_math' for segment in segments) == 1
    assert any(segment.kind == 'inline_math' and segment.value == r'\pi_{6}^{3}'
               for segment in segments)
    assert any(segment.kind == 'strong' and '先行データベース結果' in segment.value
               for segment in segments)
    assert render('**plain text**') == (Segment('strong', 'plain text'),)
    assert render('**unpaired $ dollar**') == (Segment('strong', 'unpaired $ dollar'),)


def test_mixed_newlines_fail_closed(reviewed_sources) -> None:
    original, _ = reviewed_sources[WEB_PATH]
    normalized = original.replace(b'\r\n', b'\n')
    mixed = normalized.replace(b'\n', b'\r\n', 1)
    if normalized.count(b'\n') > 1:
        with pytest.raises(RuntimeError, match='Mixed line endings'):
            patch_source(WEB_PATH, mixed)


def test_first_success_step_count_contract_in_both_historical_tests(reviewed_sources) -> None:
    """Retain the actual proof as the oracle, never fabricate an eighteenth step."""
    for path in (TEST_PATH, R4E_TEST_PATH):
        before, after = reviewed_sources[path]
        old = before.decode('utf-8-sig')
        new = after.decode('utf-8-sig')
        assert 'assert len(result.proven_steps) == 18' in old
        assert 'assert len(view.steps) == 18' in old
        assert 'assert len(result.proven_steps) == 18' not in new
        assert 'assert len(view.steps) == 18' not in new
        assert 'assert any(step.conclusion == result.conclusion for step in result.proven_steps)' in new
        assert 'assert len(view.steps) == len(pi64[0].proven_steps)' in new
        assert patch_source(path, before) == after
        with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
            patch_source(path, after)


def test_r4g_prior_result_does_not_assume_28_steps(reviewed_sources) -> None:
    """The prior completed proof remains valid regardless of search-path length."""
    before, after = reviewed_sources[TEST_PATH]
    original = before.decode('utf-8-sig')
    modified = after.decode('utf-8-sig')
    assert 'assert len(previous.proven_steps) == 28' in original
    assert 'assert len(previous.proven_steps) == 28' not in modified
    assert (
        'assert any(step.conclusion == previous.conclusion '
        'for step in previous.proven_steps)'
    ) in modified
    assert 'assert previous.status is ProofSearchStatus.COMPLETE' in modified
    assert patch_source(TEST_PATH, before) == after
    with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
        patch_source(TEST_PATH, after)
```

## `tests/test_integration.py`

```python
"""Actual source-first Proof Tree to canonical Narrative Model to Web regressions."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope='module')
def verified_pi74():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion is not None and not result.open_goals
    assert contexts
    model = build_linked_proof_narrative_model(result, contexts[-1])
    return result, model


def test_prop44_reference_displays_full_isomorphism_not_prelude(verified_pi74) -> None:
    result, model = verified_pi74
    prop = tuple(c for c in model.citations
                 if (c.reference.locator or c.reference.label) == 'Proposition 4.4')
    assert len(prop) == 1
    body = '\n'.join(prop[0].statement_bodies)
    assert r'\alpha\in\pi_{2n-1}^{n}' in body
    assert r'H(\alpha)=\pm\iota_{2n-1}' in body
    assert r'\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}' in body
    assert r'\xrightarrow{\;\cong\;}' in body
    assert r'(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma' in body
    assert r'E:\pi_{i-1}^{n-1}\to\pi_i^{n}' in body
    markdown = render_model_backed_narrative_markdown(result, model)
    assert 'Steenrod1951' not in markdown
    assert 'Proposition 4.4 直前の記述' not in markdown


def test_verified_lemma54_reference_body_is_visible(verified_pi74) -> None:
    result, model = verified_pi74
    lemma = tuple(c for c in model.citations
                  if (c.reference.locator or c.reference.label) == 'Lemma 5.4')
    assert len(lemma) == 1
    text = '\n'.join(lemma[0].statement_bodies)
    assert r'\nu_4\in\pi_7^4' in text
    assert r'H(\nu_4)=\iota_7' in text
    assert r"2E\nu_4=E^2\nu'" in text
    assert text in render_model_backed_narrative_markdown(result, model)


def test_verified_prior_database_latex_is_inline_math(verified_pi74) -> None:
    result, model = verified_pi74
    view = build_standard_web_group_proof_view(
        n=4, k=3, mode='narrative', citation_source='model',
    )
    assert view.key == 'generic-complete-proof' and not view.partial_result
    refs = tuple(line for line in view.rendered_lines if
                 any('先行データベース結果' in seg.value for seg in line.segments))
    assert refs
    assert any(any(seg.kind == 'inline_math' and r'\pi_{6}^{3}' in seg.value
                   for seg in line.segments) for line in refs)
    assert result.open_goals == model.open_goals == ()


@pytest.mark.parametrize('n,k', ((3, 3), (4, 4), (4, 7)))
def test_other_completed_groups_not_promoted_or_downgraded(n: int, k: int) -> None:
    view = build_standard_web_group_proof_view(
        n=n, k=k, mode='narrative', citation_source='model',
    )
    assert view.key == 'generic-complete-proof'
    assert not view.partial_result
    assert view.rendered_lines


@pytest.mark.parametrize('k', (8, 31))
def test_abstract_only_groups_remain_partial(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode='narrative', citation_source='model',
    )
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert view.key == 'generic-partial-proof' and view.partial_result
    assert sum(line.kind == 'heading' and line.prefix == '証明済みの抽象群構造'
               for line in view.rendered_lines) == 1
```

