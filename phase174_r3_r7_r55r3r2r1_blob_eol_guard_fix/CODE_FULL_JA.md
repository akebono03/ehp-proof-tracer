# R55R3R2R1 変更コード全文（新規パッケージ）

実装前の既存 GitHub `develop` HEAD は `d923ff2a34b6ba9d4c23d3da0221402f0b815f46`。

既存の対象は3ファイル・3関数。変更後の実コードは `output/` に全文を生成する。新規パッケージ `install.py` の修正関数は下記の全文を参照。

## install.py

```python
"""Undo R55R3 bespoke narrative and use existing shared typed/reference projections.

Only three pinned, previously reviewed source files are modified.  The local
untracked R55R3 and optional R55R3R1 packages are removed after exact review.
No proof search, inference rule, source registry, or registered GIVEN is changed.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
REVIEWED_HEAD = 'd923ff2a34b6ba9d4c23d3da0221402f0b815f46'
REFERENCE = 'phase168_r3_37c_reference_projection.py'
RENDERER = 'phase168_r3_5_model_renderer.py'
TYPED = 'phase168_r3_27_typed_statement_projection.py'
PINNED = {
    REFERENCE: '0a7800b3bd9d140fc22c1b92ab74bcdf48740546',
    RENDERER: '913a7030e209a689f58a5215013d3708140052e7',
    TYPED: '26ce3632fe1b32bab7e822e8f701409b26f4f04a',
}
LEGACY_A = 'phase174_r3_r7_r55r3_common_proof_display'
LEGACY_B = 'phase174_r3_r7_r55r3r1_public_sentence_correction'
REFERENCE_OLD = '''            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
'''
REFERENCE_LEGACY = '''            if sentence is None:
                from phase174_r3_r7_r55r3_common_proof_display.projection import (
                    project_cited_general_reference_body,
                )
                sentence = project_cited_general_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
'''
REFERENCE_SHARED = '''            if sentence is None:
                sentence = _project_certified_general_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
'''
RENDERER_OLD = '''        sentence = typed_sentence(step.conclusion, step)
        if index != model.root_index:
'''
RENDERER_LEGACY = '''        sentence = typed_sentence(step.conclusion, step)
        from phase174_r3_r7_r55r3_common_proof_display.projection import (
            project_certified_proof_sentence,
        )
        sentence = project_certified_proof_sentence(model, index, sentence)
        if index != model.root_index:
'''
TYPED_OLD = '''    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
    from toda_rules import Toda45IsomorphismStatement
'''
TYPED_SHARED = '''    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
    # Only project the mathematical content already present in a typed claim.
    # These are shared statement formatters, not a proof-tree-specific narrative.
    from expression import Zero
    from proof import Relation, RelationType
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27TypedHopfDeltaStatement, typed_specialization,
    )
    if type(statement) is Prop27TypedHopfDeltaStatement:
        if (type(statement.n) is int and statement.n >= 2
                and statement.n % 2 == 0
                and statement == typed_specialization(statement.n)):
            sign = r"\\pm" if statement.sign_undetermined else ""
            return (
                rf"$H(\\Delta(\\iota_{{{statement.source_iota_dimension}}}))="
                rf"{sign}{statement.absolute_coefficient}"
                rf"\\iota_{{{statement.target_iota_dimension}}}$."
            )
        return None
    if type(statement) is KernelMultipleStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(statement.source_generator)
        if (source is not None and target is not None
                and symbol is not None and generator is not None
                and type(statement.multiple) is int
                and statement.multiple >= 1
                and statement.domain == mapping.source_group):
            return (
                rf"$\\ker({symbol}:{source}\\to {target})="
                rf"{statement.multiple}\\mathbb{{Z}}\\{{{generator}\\}}$."
            )
        return None
    if (type(statement) is Relation
            and statement.relation_type is RelationType.EQUALITY
            and isinstance(statement.rhs, Zero)):
        from toda_conclusion_latex_renderer import (
            render_repository_conclusion_latex,
        )
        try:
            latex = render_repository_conclusion_latex(statement)
        except (TypeError, ValueError):
            return None
        return "$" + latex + "$."
    from toda_rules import Toda45IsomorphismStatement
'''


def _run_git(*arguments: str, binary: bool = False):
    result = subprocess.run(('git',) + arguments, cwd=ROOT, capture_output=True,
                            check=False)
    if result.returncode:
        raise RuntimeError('git ' + ' '.join(arguments) + ': '
                           + result.stderr.decode('utf-8', 'replace'))
    return result.stdout if binary else result.stdout.decode('utf-8', 'replace').strip()


def _source(data: bytes) -> tuple[str, bytes, str]:
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    actual = data[len(bom):]
    if b'\r' in actual.replace(b'\r\n', b''):
        raise RuntimeError('Mixed or CR-only line endings are not allowed')
    eol = '\r\n' if b'\r\n' in actual else '\n'
    return actual.decode('utf-8').replace('\r\n', '\n'), bom, eol


def _build_bytes(text: str, bom: bytes, eol: str) -> bytes:
    return bom + text.replace('\n', eol).encode('utf-8')


def _once(text: str, before: str, after: str, label: str) -> str:
    if text.count(before) != 1:
        raise RuntimeError('Expected exactly one reviewed anchor: ' + label)
    return text.replace(before, after, 1)


def _git_blob(data: bytes) -> str:
    """Hash the original Git blob bytes, preserving CRLF and any UTF-8 BOM."""
    if not isinstance(data, bytes):
        raise TypeError('Git blob input must be bytes')
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def _extract_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == name]
    if len(functions) != 1:
        raise RuntimeError('Function must be unique: ' + name)
    node = functions[0]
    return ''.join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def construct_sources() -> dict[str, tuple[Path, bytes, bytes]]:
    """Allow only old verified R55R3 hooks, bare HEAD, or our exact new code."""
    if _run_git('branch', '--show-current') != 'develop':
        raise RuntimeError('Worktree branch must be develop')
    root = _run_git('rev-parse', '--show-toplevel')
    if root.replace('\\', '/').lower() != str(ROOT).replace('\\', '/').lower():
        raise RuntimeError('Extract ZIP directly into repository root')
    base_ok = subprocess.run(('git', 'merge-base', '--is-ancestor', REVIEWED_HEAD, 'HEAD'),
                             cwd=ROOT, check=False).returncode == 0
    if not base_ok:
        raise RuntimeError('HEAD is not descended from reviewed GitHub develop')
    for name, sha in PINNED.items():
        if _run_git('rev-parse', 'HEAD:' + name) != sha:
            raise RuntimeError('Reviewed Git blob has changed: ' + name)

    helper = (PACKAGE / 'reference_body_helper.txt').read_text(encoding='utf-8')
    assert helper.startswith('def _project_certified_general_reference_body(')
    proposals: dict[str, tuple[Path, bytes, bytes]] = {}
    for name in PINNED:
        path = ROOT / name
        raw = path.read_bytes()
        text, bom, eol = _source(raw)
        committed_raw = _run_git('show', 'HEAD:' + name, binary=True)
        if _git_blob(committed_raw) != PINNED[name]:
            raise RuntimeError('Committed file baseline blob mismatch: ' + name)
        committed, _, _ = _source(committed_raw)
        if name == REFERENCE:
            legacy = _once(committed, REFERENCE_OLD, REFERENCE_LEGACY, name)
            expected = _once(committed, REFERENCE_OLD, REFERENCE_SHARED, name)
            anchor = '\ndef project_reference_bodies(registry, assertion_ids):'
            if expected.count(anchor) != 1:
                raise RuntimeError('Shared reference function boundary changed')
            expected = expected.replace(anchor, '\n\n' + helper + anchor, 1)
        elif name == RENDERER:
            legacy = _once(committed, RENDERER_OLD, RENDERER_LEGACY, name)
            expected = committed
        else:
            legacy = committed
            expected = _once(committed, TYPED_OLD, TYPED_SHARED, name)
        if text not in (committed, legacy, expected):
            raise RuntimeError('Unreviewed user code in target, refusing overwrite: ' + name)
        if name == TYPED and text not in (committed, expected):
            raise RuntimeError('Unexpected typed projection edit')
        if name != TYPED and text == committed:
            # The earlier R55R3 patch is expected to have been run, but
            # allow idempotent recovery if a hook was already manually reverted.
            pass
        ast.parse(expected, filename=name)
        proposals[name] = (path, raw, _build_bytes(expected, bom, eol))
    return proposals


def _legacy_manifest() -> dict:
    return json.loads((PACKAGE / 'legacy_manifest.json').read_text(encoding='utf-8'))


def _legacy_files(name: str) -> list[Path]:
    """Verify each old generated file before deletion; unknown user edits abort."""
    directory = ROOT / name
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise RuntimeError('Old package path is not a directory: ' + name)
    tracked = _run_git('ls-files', '--', name)
    if tracked:
        raise RuntimeError('Legacy package has tracked files; refuse directory deletion: ' + name)
    if directory.is_symlink():
        raise RuntimeError('Legacy package is a symbolic link: ' + name)
    entries = list(directory.rglob('*'))
    if any(entry.is_symlink() for entry in entries):
        raise RuntimeError('Unexpected symbolic link inside old Narrative package: ' + name)
    manifest = _legacy_manifest()['packages'][name]
    files = [p for p in entries if p.is_file()]
    for path in files:
        relative = path.relative_to(directory).as_posix()
        if relative in manifest:
            source, _, _ = _source(path.read_bytes())
            digest = hashlib.sha256(source.encode('utf-8')).hexdigest()
            valid = manifest[relative]
            if relative == 'projection.py':
                valid = valid + [_legacy_manifest()['corrected_projection_sha256']]
            if digest not in valid:
                raise RuntimeError('Unreviewed legacy file; refusing deletion: ' + str(path))
        elif '__pycache__/' in relative or relative.endswith('.pyc'):
            continue
        elif relative.startswith('output/'):
            if relative in (
                'output/phase168_r3_37c_reference_projection.FULL.py',
                'output/phase168_r3_5_model_renderer.FULL.py',
            ):
                target = (REFERENCE if 'reference_projection' in relative else RENDERER)
                original, _, _ = _source(_run_git('show', 'HEAD:' + target, binary=True))
                before, after = ((REFERENCE_OLD, REFERENCE_LEGACY) if target == REFERENCE
                                 else (RENDERER_OLD, RENDERER_LEGACY))
                expected = _once(original, before, after, 'legacy output ' + target)
                printed, _, _ = _source(path.read_bytes())
                if printed != expected:
                    raise RuntimeError('Unknown generated original full module: ' + relative)
            elif relative == 'output/CHANGED_FUNCTIONS_FULL_JA.md':
                doc = path.read_text(encoding='utf-8-sig')
                if not doc.startswith('# R55R3 変更後の関数全文'):
                    raise RuntimeError('Unknown generated R55R3 function output: ' + relative)
            else:
                raise RuntimeError('Unknown legacy output: ' + relative)
        else:
            raise RuntimeError('Unknown file in legacy package: ' + str(path))
    return files


def guard() -> tuple[dict[str, tuple[Path, bytes, bytes]], list[Path]]:
    proposals = construct_sources()
    old_dirs = [ROOT / name for name in (LEGACY_A, LEGACY_B) if (ROOT / name).exists()]
    for name in (LEGACY_A, LEGACY_B):
        _legacy_files(name)
    return proposals, old_dirs


def _write_outputs(proposals: dict[str, tuple[Path, bytes, bytes]]) -> None:
    output = PACKAGE / 'output'
    output.mkdir(exist_ok=True)
    labels = {
        REFERENCE: 'project_reference_bodies',
        RENDERER: 'render_model_backed_narrative_markdown',
        TYPED: 'typed_sentence',
    }
    fragments = []
    for name, (_, _, new_data) in proposals.items():
        source, _, _ = _source(new_data)
        (output / name).write_text(source, encoding='utf-8')
        # Local imports only changed within these full functions; the original
        # module top-level imports are printed in each full source file.
        func = _extract_function(source, labels[name])
        fragments.append('## ' + name + ' — ' + labels[name] + '\n\n```python\n'
                         + func + '\n```\n')
    helper = _extract_function(_source(proposals[REFERENCE][2])[0],
                               '_project_certified_general_reference_body')
    fragments.insert(0, '## New common reference helper — insertion before project_reference_bodies\n\n'
                     + '```python\n' + helper + '\n```\n')
    (output / 'CHANGED_FUNCTIONS_FULL_JA.md').write_text(
        '# R55R3R2R1 変更後関数全文\n\n' + '\n'.join(fragments), encoding='utf-8',
    )


def install(*, dry_run: bool) -> dict[str, object]:
    proposals, old_dirs = guard()
    report = {
        'reviewed_head': REVIEWED_HEAD,
        'local_head': _run_git('rev-parse', 'HEAD'),
        'targets': list(proposals),
        'legacy_directories': [str(x) for x in old_dirs],
        'already_applied': all(old == new for _, old, new in proposals.values())
                           and not old_dirs,
        'new_math_rules': 0,
        'new_given': 0,
        'full_pytest': False,
    }
    if dry_run:
        return report
    for name, (path, old_data, new_data) in proposals.items():
        if old_data != new_data:
            path.write_bytes(new_data)
            print('PHASE174_R55R3R2R1_REPLACED=' + name)
    _write_outputs(proposals)
    # Delete the reviewed, untracked, obsolete Narrative implementation and
    # its obsolete tests/installers, not the retained R55R2 read-only audit.
    for folder in old_dirs:
        shutil.rmtree(folder)
        print('PHASE174_R55R3R2R1_REMOVED_LEGACY=' + str(folder.relative_to(ROOT)))
    for name, (path, _, new_data) in proposals.items():
        if path.read_bytes() != new_data:
            raise RuntimeError('Post-write verification failed: ' + name)
    for folder in old_dirs:
        if folder.exists():
            raise RuntimeError('Legacy module deletion did not complete: ' + str(folder))
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    report = install(dry_run=args.dry_run)
    key = 'PHASE174_R55R3R2R1_'
    print(key + 'LOCAL_HEAD=' + report['local_head'])
    print(key + 'SOURCE_GUARD=PASS')
    print(key + 'LEGACY_REMOVAL_COUNT=' + str(len(report['legacy_directories'])))
    print(key + 'NEW_GIVEN=0')
    print(key + 'NEW_MATH_RULES=0')
    print(key + 'GATE=' + ('PASS_PREFLIGHT_ONLY' if args.dry_run
                           else 'PASS_SOURCE_RESET_AND_LEGACY_REMOVAL'))
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## tests/test_payload.py

```python
"""Tests executable without the EHP production repository."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install import (
    PACKAGE, REFERENCE_OLD, REFERENCE_LEGACY, REFERENCE_SHARED,
    RENDERER_OLD, RENDERER_LEGACY, TYPED_OLD, TYPED_SHARED,
    _once, _git_blob, _source,
)


def test_patch_anchors_are_unique_and_source_first() -> None:
    assert 'project_cited_general_reference_body' in REFERENCE_LEGACY
    assert 'phase174_r3_r7_r55r3_common_proof_display' not in REFERENCE_SHARED
    assert _once(REFERENCE_OLD, REFERENCE_OLD, REFERENCE_SHARED, 'reference') == REFERENCE_SHARED
    assert 'project_certified_proof_sentence' in RENDERER_LEGACY
    assert 'project_certified_proof_sentence' not in RENDERER_OLD


def test_shared_typed_block_is_syntactically_valid() -> None:
    mock = 'def typed_sentence(statement, step):\n' + TYPED_SHARED
    mock += '    return None\n'
    ast.parse(mock)
    assert 'step.premises' not in TYPED_SHARED
    assert 'n==6' not in TYPED_SHARED
    assert r'\mathrm{upper}' not in TYPED_SHARED
    assert r'\mathrm{lower}' not in TYPED_SHARED


def test_reference_formatter_cannot_infer_proof_steps() -> None:
    source = (PACKAGE / 'reference_body_helper.txt').read_text(encoding='utf-8')
    ast.parse(source)
    assert 'ProofStep(' not in source
    assert 'InferenceRule(' not in source
    assert 'project_certified_proof_sentence' not in source
    assert '_typed_upper_delta_transition' not in source


def test_old_modules_deletion_is_whitelisted_by_zip_hash() -> None:
    data = json.loads((PACKAGE / 'legacy_manifest.json').read_text(encoding='utf-8'))
    assert set(data['packages']) == {
        'phase174_r3_r7_r55r3_common_proof_display',
        'phase174_r3_r7_r55r3r1_public_sentence_correction',
    }
    for files in data['packages'].values():
        assert 'install.py' in files
        assert 'run.ps1' in files
        assert all(len(value) == 1 and len(value[0]) == 64 for value in files.values())


def test_blob_guard_hashes_raw_git_bytes_before_line_ending_normalization() -> None:
    """A CRLF file must keep its Git object identity when decoded for patching."""
    raw_crlf = b'def f():\r\n    return 6\r\n'
    raw_lf = b'def f():\n    return 6\n'
    raw_bom = b'\xef\xbb\xbf' + raw_crlf
    normalized, bom, eol = _source(raw_crlf)
    assert normalized == 'def f():\n    return 6\n'
    assert bom == b''
    assert eol == '\r\n'
    assert _git_blob(raw_crlf) != _git_blob(raw_lf)
    assert _git_blob(raw_crlf) != _git_blob(raw_bom)
    assert len(_git_blob(raw_crlf)) == 40
    assert _git_blob(raw_crlf) == hashlib.sha1(
        b'blob ' + str(len(raw_crlf)).encode('ascii') + b'\0' + raw_crlf
    ).hexdigest()


def test_blob_guard_rejects_text_input_before_any_git_check() -> None:
    import pytest

    with pytest.raises(TypeError, match='must be bytes'):
        _git_blob('a\r\n')
```

## tests/test_static.py

```python
"""Static regression: no target-specific R55R3 proof prose survives."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install import (
    PACKAGE, REFERENCE, RENDERER, TYPED, ROOT, LEGACY_A, LEGACY_B,
    REFERENCE_LEGACY, REFERENCE_SHARED, RENDERER_LEGACY, TYPED_SHARED,
    construct_sources,
)


def test_no_special_r55r3_modules_or_hooks() -> None:
    assert not (ROOT / LEGACY_A).exists()
    assert not (ROOT / LEGACY_B).exists()
    reference = (ROOT / REFERENCE).read_text(encoding='utf-8-sig')
    renderer = (ROOT / RENDERER).read_text(encoding='utf-8-sig')
    typed = (ROOT / TYPED).read_text(encoding='utf-8-sig')
    assert REFERENCE_LEGACY not in reference
    assert RENDERER_LEGACY not in renderer
    assert REFERENCE_SHARED in reference
    assert TYPED_SHARED in typed
    assert 'project_certified_proof_sentence' not in renderer
    assert '_typed_upper_delta_transition' not in renderer
    assert 'r55r3_common_proof_display' not in renderer
    for source in (reference, renderer, typed):
        ast.parse(source)


def test_shared_reference_helper_is_only_a_citation_formatter() -> None:
    source = (ROOT / REFERENCE).read_text(encoding='utf-8-sig')
    fragment = (PACKAGE / 'reference_body_helper.txt').read_text(encoding='utf-8')
    assert fragment in source
    helper = source[source.index('def _project_certified_general_reference_body('):]
    helper = helper[:helper.index('\ndef project_reference_bodies(')]
    for forbidden in ('project_certified_proof_sentence',
                      '_typed_upper_delta_transition', 'pi_12^7', '(n,k)'):
        assert forbidden not in helper


def test_installer_is_idempotent_after_removal() -> None:
    proposals = construct_sources()
    assert set(proposals) == {REFERENCE, RENDERER, TYPED}
    assert all(original == expected for _, original, expected in proposals.values())
```

## tests/test_typed.py

```python
"""Render typed conclusions generically; no selected Group-query target."""
from __future__ import annotations

import pytest


@pytest.mark.parametrize('n', [4, 6, 8])
def test_even_n_prop27_typed_statement_latex(n: int) -> None:
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization

    sentence = typed_sentence(typed_specialization(n), None)
    assert sentence is not None
    assert rf'\iota_{{{2 * n + 1}}}' in sentence
    assert rf'\iota_{{{2 * n - 1}}}' in sentence
    assert r'\pm2' in sentence
    assert r'\mathrm{upper}' not in sentence
    assert r'\mathrm{lower}' not in sentence


@pytest.mark.parametrize('n', [6, 8])
def test_kernel_multiple_statement_is_formatted_from_its_own_type(n: int) -> None:
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r14_r6_generic_iso import MapSurjective
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        upper_delta_surjectivity_inputs,
    )
    from phase168_r3_27_typed_statement_projection import typed_sentence

    mapping = TodaDeltaMap(TodaPrimaryGroup(2*n+1, 2*n+1),
                           TodaPrimaryGroup(2*n-1, n))
    required = upper_delta_surjectivity_inputs(MapSurjective(mapping))
    assert required is not None
    kernel = required[2]
    display = typed_sentence(kernel, None)
    assert display is not None
    assert r'\ker(' in display
    assert r'\mathbb{Z}' in display
    assert r'\mathrm{upper}' not in display
    assert r'\mathrm{lower}' not in display


def test_general_zero_relation_is_not_target_specific() -> None:
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    source = CitedFamilyAnnihilator(
        left_family_id=4, right_family_id=2,
        minimum_left_index=6, right_index_offset=3,
        citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
    )
    for n in (6, 8):
        relation = canonical_annihilator_instance(source, n)
        assert relation is not None
        sentence = typed_sentence(relation, None)
        assert sentence is not None
        assert r'\nu' in sentence and r'\eta' in sentence
        assert '0' in sentence
```

## tests/test_public.py

```python
"""Verify the published source-first proof after bespoke narrative deletion."""
from __future__ import annotations

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.audit import inspect_shared_display


def test_real_public_proof_uses_shared_typed_and_reference_projection() -> None:
    observed = inspect_shared_display()
    assert observed['source_first_root_complete'] is True
    assert observed['root_ancestor_steps'] == 28
    assert observed['dedicated_r55r3_narrative_remaining'] is False
    assert observed['r7_typed_formula_visible'] is True
    assert observed['new_givens'] == 0
    assert observed['new_math_rules'] == 0
    assert observed['both_http_200'] is True
    assert observed['both_http_complete'] is True
```

## audit.py

```python
"""Review the production typed proof and the absence of R55R3 narrative hooks."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install import (
    ROOT, LEGACY_A, LEGACY_B, construct_sources, _run_git,
)


def inspect_shared_display() -> dict[str, object]:
    from phase174_r3_r7_r55r2_reference_tree_audit.audit import inspect_public_proof
    from phase174_r3_r7_r54_public_http_narrative_audit.audit import inspect_public_http_proof
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization

    if (ROOT / LEGACY_A).exists() or (ROOT / LEGACY_B).exists():
        raise RuntimeError('A bespoke R55R3 narrative package is still installed')
    reference = (ROOT / 'phase168_r3_37c_reference_projection.py').read_text(encoding='utf-8-sig')
    renderer = (ROOT / 'phase168_r3_5_model_renderer.py').read_text(encoding='utf-8-sig')
    if ('project_certified_proof_sentence' in renderer
            or 'r55r3_common_proof_display' in reference
            or 'r55r3_common_proof_display' in renderer
            or '_typed_upper_delta_transition' in renderer):
        raise RuntimeError('Obsolete R55R3 special Narrative hook remains')
    report = inspect_public_proof()
    if report['status'] != 'complete' or report['root_ancestor_steps'] != 28 or report['open_goals']:
        raise RuntimeError('The certified public root proof was changed')
    if not (report['r2']['reference_body_present']
            and report['r7']['reference_body_present']
            and report['source_proof']['upper_delta_four_distinct_inference_premises']
            and report['narrative']['r7_hopf_delta_specialization_in_proof']):
        raise RuntimeError('Certified typed formulas or literature bodies missing')
    # Stable typed formula in another legitimate (even) n, independent of
    # the n=6 public proof. No group-specific narrative is permitted.
    generalized = typed_sentence(typed_specialization(8), None)
    if generalized is None or r'\iota_{17}' not in generalized or r'\iota_{15}' not in generalized:
        raise RuntimeError('The shared theorem formatter only handles n=6')
    html = inspect_public_http_proof()
    if not html['both_http_200'] or not html['both_complete_proof']:
        raise RuntimeError('The shared HTTP proof presentation regressed')
    if any(row['repeated_intro_count'] != 1 for row in html['cases']):
        raise RuntimeError('The shared proof introduction is duplicated')
    return {
        'target': 'pi_12^7 = 0',
        'source_first_root_complete': True,
        'root_ancestor_steps': report['root_ancestor_steps'],
        'r2_r7_reference_body_count': len(report['r2']['statement_bodies']) + len(report['r7']['statement_bodies']),
        'r2_general_source_formula': report['r2']['statement_bodies'],
        'r7_general_source_formula': report['r7']['statement_bodies'],
        'r7_typed_formula_visible': report['narrative']['r7_hopf_delta_specialization_in_proof'],
        'r2_n6_zero_formula_visible': report['narrative']['r2_n6_zero_relation_in_proof'],
        'source_signed_lower_delta_displayed_as_cited': report['narrative']['unnecessary_lower_delta_plusminus_in_proof'],
        'generic_n8_prop27_formula': generalized,
        'dedicated_r55r3_narrative_remaining': False,
        'both_http_200': True,
        'both_http_complete': True,
        'new_givens': 0,
        'new_math_rules': 0,
        'full_pytest': False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    info = None
    if args.dry_run:
        construct_sources()
        gate = 'PASS_REVIEWED_SOURCE_PREFLIGHT'
    else:
        info = inspect_shared_display()
        gate = 'PASS_R55R3_NARRATIVE_REMOVED_SHARED_TYPED_DISPLAY'
    result = {
        'phase':'174-R3-R7-R55R3R2', 'head':_run_git('rev-parse','HEAD'),
        'observations':info, 'gate':gate,
    }
    directory = Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir())) / (
        'EHPProofTracerAudit/phase174_r3_r7_r55r3r2'
    )
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ('preflight.json' if args.dry_run else 'shared_display.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE174_R55R3R2R1_LOCAL_HEAD=' + result['head'])
    if info:
        for key, value in info.items():
            print('PHASE174_R55R3R2R1_' + key.upper() + '=' + str(value))
    print('PHASE174_R55R3R2R1_REPORT=' + str(path))
    print('PHASE174_R55R3R2R1_GATE=' + gate)
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

## run.ps1

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R55R3R2R1_DRYRUN=PASS'
        Write-Output '(END)'
        exit 0
    }

    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.install
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 deletion and guarded replacement failed' }

    # Focused test only; full suite is reserved for the Phase 174 final gate.
    python -m pytest -q --import-mode=importlib `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_payload.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_static.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_typed.py `
        .\phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix\tests\test_public.py `
        .\phase174_r3_r7_r55_common_exactness_intro\tests\test_http.py `
        .\phase174_r3_r7_r37_upper_delta_surjectivity_isolated\tests\test_rule.py
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 focused pytest failed' }

    python -m phase174_r3_r7_r55r3r2r1_blob_eol_guard_fix.audit
    if ($LASTEXITCODE -ne 0) { throw 'R55R3R2R1 public proof audit failed' }
    Write-Output 'PHASE174_R55R3R2R1_FOCUSED_TESTS=PASS'
    Write-Output '(END)'
}
finally {
    Pop-Location
}
```

## reference_body_helper.txt

```text
def _project_certified_general_reference_body(assertion: object, registry: object,
                                         statement: object) -> str | None:
    """Show already-cited general laws when source identity and typed data agree."""
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin, ReferenceKind,
        UnifiedStatementRegistry,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
    )
    from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
        Prop27UniversalLiteratureStatement,
    )

    if not isinstance(registry, UnifiedStatementRegistry) or not isinstance(assertion, AssertionEntry):
        return None
    try:
        if registry.assertion(assertion.assertion_id) is not assertion:
            return None
        reference = registry.reference(assertion.reference_id)
    except KeyError:
        return None
    if (assertion.kind is not AssertionKind.STATEMENT
            or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.dependencies
            or assertion.content is not statement
            or not isinstance(reference.publication_position, int)
            or reference.publication_position <= 0):
        return None

    if type(statement) is CitedFamilyAnnihilator:
        if (statement != CitedFamilyAnnihilator(
                left_family_id=4, right_family_id=2,
                minimum_left_index=6, right_index_offset=3,
                citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
            )
                or not assertion.assertion_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general:statement')
                or not assertion.reference_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general')
                or assertion.scope != 'nu_n composed eta_(n+3) = 0, n>=6'
                or reference.kind is not ReferenceKind.EQUATION
                or reference.locator != '(5.9)'
                or reference.source_id != (
                    'sources/toda/Toda_05_2.tex '
                    '(adopted; printed edition unchecked)'
                )):
            return None
        return r'$n\ge6$ に対して, $\nu_n\circ\eta_{n+3}=0$.'

    if type(statement) is Prop27UniversalLiteratureStatement:
        if (statement != Prop27UniversalLiteratureStatement()
                or not assertion.assertion_id.endswith(
                    ':typed_literature:assertion:toda:prop2.7')
                or not assertion.reference_id.endswith(
                    ':typed_literature:toda:prop2.7')
                or assertion.scope != ('n >= 2', 'n even', 'sign undetermined')
                or reference.kind is not ReferenceKind.PROPOSITION
                or reference.locator != 'Proposition 2.7'
                or reference.source_id != 'toda:tex:ch2:0018'):
            return None
        return (r'$n\ge2$ を偶数とすると, '
                r'$H(\Delta(\iota_{2n+1}))=\pm2\iota_{2n-1}$.')
    return None
```

## __init__.py

```python
"""Phase 174 source-guarded removal of Phase R55R3 dedicated narrative."""
```
