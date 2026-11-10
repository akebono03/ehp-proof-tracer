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
