"""Phase 165 R5-R16: conservative, read-only final retirement assessment."""
from __future__ import annotations

import ast
import json
from pathlib import Path

LEGACY_TARGETS = {
    'phase162_web_narrative_integration.py': (
        'build_phase162_web_validated_isomorphism_markdown',
        '_build_phase162_legacy_validated_isomorphism_markdown',
        '_build_phase162_existing_group_connection',
    ),
    'phase162_r3_narrative_connection.py': (
        'render_phase162_r3_narrative',
        'render_phase162_r3_with_public_references',
    ),
    'toda_group_proof_narrative_proof_chain_renderer.py': (
        'render_toda_group_proof_narrative_from_proof_chains_markdown',
    ),
    'toda_group_proof_narrative_concrete_transport.py': (
        'render_concrete_transport_proof_from_steps',
    ),
}


def _read_tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))


def _imports_from(tree: ast.AST, module: str, symbol: str) -> bool:
    return any(
        isinstance(node, ast.ImportFrom)
        and node.module == module
        and any(alias.name == symbol for alias in node.names)
        for node in ast.walk(tree)
    )


def _definition_names(tree: ast.Module) -> set[str]:
    return {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def _has_name(tree: ast.AST, name: str) -> bool:
    return any(isinstance(n, ast.Name) and n.id == name for n in ast.walk(tree))


def audit(root: Path) -> dict:
    root = root.resolve()
    required = list(LEGACY_TARGETS) + [
        'phase162_ehp_leaf_inputs.py',
        'phase162_pi5_3_web_replay.py',
        'web_group_proof.py',
        'cli.py',
        'main.py',
    ]
    missing = [p for p in required if not (root / p).is_file()]
    result: dict = {'phase': '165 R5-R16', 'missing_files': missing, 'guards': {}, 'legacy_symbols': {}, 'status': 'PRECONDITION_FAILED', 'full_pytest_run': False}
    if missing:
        return result
    try:
        trees = {path: _read_tree(root / path) for path in required}
    except (OSError, SyntaxError, UnicodeError) as exc:
        result['parse_error'] = str(exc)
        return result

    replay = trees['phase162_pi5_3_web_replay.py']
    web = trees['phase162_web_narrative_integration.py']
    result['guards'] = {
        'shared_leaves_defined': '_phase162_ehp_leaves' in _definition_names(trees['phase162_ehp_leaf_inputs.py']),
        'replay_uses_shared_leaves': _imports_from(replay, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves'),
        'old_web_reexports_shared_leaves': _imports_from(web, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves'),
        'web_public_group_entry_exists': 'build_standard_web_group_proof_view' in _definition_names(trees['web_group_proof.py']) or 'build_web_partial_group_proof_view' in _definition_names(trees['web_group_proof.py']),
        'cli_uses_canonical_renderer': _has_name(trees['cli.py'], 'render_partial_proof_markdown'),
        'main_uses_canonical_renderer': _has_name(trees['main.py'], 'render_partial_proof_markdown'),
    }

    found = 0
    for path, names in LEGACY_TARGETS.items():
        defined = _definition_names(trees[path])
        for name in names:
            present = name in defined
            result['legacy_symbols'][f'{path}:{name}'] = 'PRESENT' if present else 'ABSENT'
            found += int(present)
    result['legacy_definitions_present'] = found
    # Count local Python references conservatively. This is not a full dynamic-call analysis.
    references = {}
    for path in sorted(root.rglob('*.py')):
        if any(part in {'.git', '.venv', 'venv', '__pycache__', '.phase165_r5_r11_backup'} for part in path.relative_to(root).parts):
            continue
        if any(part.startswith('phase165_r5_r16_') for part in path.relative_to(root).parts):
            continue
        try:
            tree = _read_tree(path)
        except (OSError, UnicodeError, SyntaxError):
            continue
        for target, names in LEGACY_TARGETS.items():
            module = target.removesuffix('.py')
            for name in names:
                if _imports_from(tree, module, name):
                    key = f'{module}.{name}'
                    references.setdefault(key, []).append(str(path.relative_to(root)))
    result['direct_imports'] = {key: sorted(set(paths)) for key, paths in references.items()}
    if not all(result['guards'].values()):
        result['status'] = 'PRECONDITION_FAILED'
    elif found:
        result['status'] = 'PUBLIC_PATH_UNIFIED_LEGACY_REMAINS'
    else:
        result['status'] = 'STATIC_RETIREMENT_CANDIDATE_NEEDS_RUNTIME_VERIFICATION'
    return result


def main() -> int:
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    report = audit(root)
    out = Path(__file__).resolve().parent / 'audit_output'
    out.mkdir(exist_ok=True)
    (out / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    text = [
        '# Phase 165 R5-R16 Renderer retirement gate',
        '',
        f"Status: **{report['status']}**",
        '',
        f"Legacy definitions remaining: **{report.get('legacy_definitions_present', 'unknown')}**",
        '',
        '## Guards',
        '',
    ]
    text.extend(f'- {key}: {"PASS" if value else "FAIL"}' for key, value in report.get('guards', {}).items())
    text.extend(['', '## Legacy symbol inventory', ''])
    text.extend(f'- `{key}`: {value}' for key, value in report.get('legacy_symbols', {}).items())
    text.extend(['', '## Direct import sites', ''])
    text.extend(f'- `{key}`: {", ".join(value)}' for key, value in report.get('direct_imports', {}).items())
    text.extend(['', 'This audit is read-only. It does not prove absence of dynamic imports or external API use.', 'Known Phase162 fixture regressions are not suppressed.', 'Full pytest was not run.'])
    (out / 'review.md').write_text('\n'.join(text) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report['status'] == 'PRECONDITION_FAILED' else 0


if __name__ == '__main__':
    raise SystemExit(main())
