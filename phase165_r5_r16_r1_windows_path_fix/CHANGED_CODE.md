# Phase 165 R5-R16-R1 コード全文

変更対象は監査 ZIP 内の `audit.py` の関数 `audit()` と `test_audit.py` の新規関数 `test_windows_path_conversion_uses_forward_slashes()`、および `test_audit.py` の import 行。アプリケーション側は変更しない。

変更した `audit.py` を全文掲載する（関数・import 省略なし）。

## audit.py（全文）

```python
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
                    references.setdefault(key, []).append(path.relative_to(root).as_posix())
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

```

## test_audit.py（全文、import とテスト関数）

```python
from pathlib import Path, PureWindowsPath

from audit import audit


def _fixture(tmp_path: Path, legacy: bool = True) -> Path:
    files = {
        'phase162_ehp_leaf_inputs.py': 'def _phase162_ehp_leaves():\n    return ()\n',
        'phase162_pi5_3_web_replay.py': 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n',
        'phase162_web_narrative_integration.py': 'from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n',
        'phase162_r3_narrative_connection.py': '',
        'toda_group_proof_narrative_proof_chain_renderer.py': '',
        'toda_group_proof_narrative_concrete_transport.py': '',
        'web_group_proof.py': 'def build_web_partial_group_proof_view():\n    return render_partial_proof_markdown\n',
        'cli.py': 'render_partial_proof_markdown = object()\n',
        'main.py': 'render_partial_proof_markdown = object()\n',
    }
    if legacy:
        files['phase162_web_narrative_integration.py'] += 'def build_phase162_web_validated_isomorphism_markdown():\n    return "old"\n'
    for path, content in files.items():
        (tmp_path / path).write_text(content, encoding='utf-8')
    return tmp_path


def test_present_old_renderer_must_not_claim_retired(tmp_path):
    result = audit(_fixture(tmp_path))
    assert result['status'] == 'PUBLIC_PATH_UNIFIED_LEGACY_REMAINS'
    assert result['legacy_definitions_present'] == 1


def test_no_old_renderer_only_static_candidate(tmp_path):
    result = audit(_fixture(tmp_path, legacy=False))
    assert result['status'] == 'STATIC_RETIREMENT_CANDIDATE_NEEDS_RUNTIME_VERIFICATION'


def test_missing_shared_leaf_is_precondition_failure(tmp_path):
    root = _fixture(tmp_path)
    (root / 'phase162_ehp_leaf_inputs.py').unlink()
    assert audit(root)['status'] == 'PRECONDITION_FAILED'


def test_missing_compat_reexport_is_precondition_failure(tmp_path):
    root = _fixture(tmp_path)
    (root / 'phase162_web_narrative_integration.py').write_text('def build_phase162_web_validated_isomorphism_markdown():\n    pass\n', encoding='utf-8')
    assert audit(root)['status'] == 'PRECONDITION_FAILED'


def test_no_false_positive_for_nonexistent_symbols(tmp_path):
    result = audit(_fixture(tmp_path))
    assert result['legacy_symbols']['phase162_r3_narrative_connection.py:render_phase162_r3_narrative'] == 'ABSENT'


def test_direct_test_import_is_recorded(tmp_path):
    root = _fixture(tmp_path)
    tests = root / 'tests'
    tests.mkdir()
    (tests / 'test_old.py').write_text('from phase162_web_narrative_integration import build_phase162_web_validated_isomorphism_markdown\n', encoding='utf-8')
    result = audit(root)
    assert result['direct_imports']['phase162_web_narrative_integration.build_phase162_web_validated_isomorphism_markdown'] == ['tests/test_old.py']


def test_windows_path_conversion_uses_forward_slashes():
    assert PureWindowsPath("tests", "test_old.py").as_posix() == "tests/test_old.py"

```

## run.ps1（全文）

```powershell
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$package;$root"
python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R16 audit tests failed.' }
python (Join-Path $package 'audit.py') $root
if ($LASTEXITCODE -ne 0) { throw 'R5-R16 prerequisites failed. No application changes were performed.' }
Write-Host 'R5-R16 retirement audit recorded. No application files modified; full pytest NOT run.'

```
