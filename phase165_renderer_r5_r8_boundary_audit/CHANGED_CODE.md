# Phase 165 R5-R8 変更コード全文

既存コードに変更はない。以下の3ファイルをプロジェクトルート下に新規追加する。

## audit.py

```python
"""Read-only Phase 165 R5-R8 public-entry boundary audit."""
from __future__ import annotations

import ast
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / 'audit_output'
LEGACY_MODULE = 'phase162_web_narrative_integration.py'
LEGACY_NARRATIVE = 'phase162_r3_narrative_connection.py'
CANONICAL = 'toda_group_proof_narrative_renderer.py'
PUBLIC_ENTRIES = ('web_group_proof.py', 'main.py', 'cli.py')
SECONDARY_ENTRIES = ('web_generator_proof.py', 'web_generator_exploration.py',
                     'web_generator_execution.py', 'web_operation_query_proof.py')
BOUNDARIES = {
    'web_group_proof.py': ('build_standard_web_group_proof_view',),
    'main.py': ('_run_group_proof_command', '_run_show_proof_command'),
    'cli.py': ('_run_group_command', '_run_element_command'),
    'phase162_web_narrative_integration.py': ('build_phase162_web_validated_isomorphism_markdown',),
    'toda_group_proof_outline_renderer.py': ('render_toda_group_proof_outline_markdown',),
    'toda_group_result_proof_replay_renderer.py': ('render_toda_group_result_proof_replay_markdown',),
    'phase165_r52_r3_web_adapter.py': ('build_partial_web_group_proof_view',),
    'phase165_r52_partial_proof.py': ('render_partial_proof_markdown',),
}


def active_sources(project: Path) -> list[Path]:
    """Project-root active modules only; archives, probes and past audit files excluded."""
    return sorted(p for p in project.glob('*.py') if '.phase' not in p.name
                  and not p.name.startswith(('audit_', 'probe_')))


def shortest_path(graph: dict[str, set[str]], start: str, finish: str):
    if start not in graph or finish not in graph:
        return None
    queue = deque([(start,)])
    seen = {start}
    while queue:
        chain = queue.popleft()
        if chain[-1] == finish:
            return list(chain)
        for neighbor in sorted(graph.get(chain[-1], ())):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(chain + (neighbor,))
    return None


def investigate(project: Path) -> dict:
    sources = active_sources(project)
    modules = {p.stem: p.name for p in sources}
    edges = {p.name: set() for p in sources}
    direct = []
    parse_errors = []
    functions = {}
    for path in sources:
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except SyntaxError as error:
            parse_errors.append({'file':path.name,'line':error.lineno,'message':str(error)})
            continue
        aliases = {}
        module_aliases = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in modules:
                target = modules[node.module]
                edges[path.name].add(target)
                for alias in node.names:
                    aliases[alias.asname or alias.name] = (target, alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in modules:
                        target = modules[alias.name]
                        edges[path.name].add(target)
                        module_aliases[alias.asname or alias.name] = target
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                target = symbol = None
                if isinstance(node.func, ast.Name) and node.func.id in aliases:
                    target, symbol = aliases[node.func.id]
                elif (isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name)
                      and node.func.value.id in module_aliases):
                    target = module_aliases[node.func.value.id]
                    symbol = node.func.attr
                if target is not None:
                    direct.append({'caller':path.name,'target':target,'symbol':symbol,'line':node.lineno})
        for fn in [node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))]:
            if fn.name not in BOUNDARIES.get(path.name, ()):
                continue
            called = []
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    if isinstance(node.func,ast.Name):
                        called.append(node.func.id)
                    elif isinstance(node.func,ast.Attribute):
                        called.append(node.func.attr)
            functions[f'{path.name}:{fn.name}'] = {'line':fn.lineno,'calls':sorted(set(called))}
    legacy_callers = [c for c in direct if c['target'] in (LEGACY_MODULE,LEGACY_NARRATIVE)]
    roots = [p for p in (*PUBLIC_ENTRIES,*SECONDARY_ENTRIES) if p in edges]
    paths = {root: {module:shortest_path(edges,root,module)
                    for module in (CANONICAL,LEGACY_MODULE,LEGACY_NARRATIVE)} for root in roots}
    references = {}
    for symbol in ('build_phase162_web_validated_isomorphism_markdown','render_phase162_r3_narrative',
                   'render_toda_group_proof_outline_markdown','render_toda_group_result_proof_replay_markdown'):
        references[symbol] = [c for c in direct if c['symbol']==symbol]
    essential = {
        'legacy_phase162_web_has_no_public_import_route':all(paths.get(root,{}).get(LEGACY_MODULE) is None for root in PUBLIC_ENTRIES),
        'legacy_phase162_narrative_has_no_public_import_route':all(paths.get(root,{}).get(LEGACY_NARRATIVE) is None for root in PUBLIC_ENTRIES),
        'web_group_proof_imports_canonical': paths.get('web_group_proof.py',{}).get(CANONICAL) is not None,
        'no_ast_errors': not parse_errors,
    }
    return {'phase':'165 R5-R8','status':'REVIEW_REQUIRED','timestamp_utc':datetime.now(timezone.utc).isoformat(),
            'scanned_active_root_python':len(sources),'parse_errors':parse_errors,
            'checks':essential,'paths':paths,'legacy_import_calls':legacy_callers,
            'symbol_callers':references,'entry_function_calls':functions,
            'limitations':[
                'Import connectivity is an overapproximation of execution, not a runtime function-level proof.',
                'No import path does not exclude dynamic imports, imports through packages, monkeypatching or reflection.',
                'Public root list covers known Web/CLI entry modules only; all possible callers are not enumerated.',
                'A function name with no detected imported calls may be used indirectly or externally.',
                'The historical Phase 162 fixture failures are not resolved by this audit.',
                'No mathematical validation and no full pytest are performed.',
            ]}


def render_report(data: dict) -> str:
    lines = ['# Phase 165 R5-R8 公開境界監査', '',f"判定: **{data['status']}**", '',
             '## 静的チェック','']
    for name, value in data['checks'].items():
        lines.append(f"- {'PASS' if value else 'REVIEW'}: `{name}`")
    lines += ['', '## 公開入口と旧経路・正規 Renderer の import 経路', '']
    for root, targets in data['paths'].items():
        lines.append(f'### `{root}`')
        for target, chain in targets.items():
            lines.append(f"- `{target}`: {' → '.join('`'+p+'`' for p in chain) if chain else '検出なし'}")
    lines += ['', '## 旧 Phase 162 関連の直接 import 呼び出し','']
    lines += [f"- `{x['caller']}:{x['line']}` → `{x['target']}` / `{x['symbol']}`" for x in data['legacy_import_calls']] or ['- 検出なし']
    lines += ['', '## 境界関数に対する直接呼出元', '']
    for symbol, callers in data['symbol_callers'].items():
        lines.append(f'### `{symbol}`')
        lines += [f"- `{x['caller']}:{x['line']}` → `{x['target']}`" for x in callers] or ['- 検出なし']
    lines += ['', '## 公開・旧関数の内部で呼ばれる名前（関数単位の補助証拠）','']
    for key, value in data['entry_function_calls'].items():
        lines.append(f"- `{key}:{value['line']}`: " + ', '.join(f'`{x}`' for x in value['calls']))
    lines += ['', '## 限界', ''] + ['- '+x for x in data['limitations']]
    return '\n'.join(lines)+'\n'


def main() -> None:
    data = investigate(PROJECT)
    OUTPUT.mkdir(exist_ok=True,parents=True)
    (OUTPUT/'audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUTPUT/'review.md').write_text(render_report(data),encoding='utf-8')
    print(json.dumps({'status':data['status'],'checks':data['checks'],
                      'old_phase162_direct_calls':len(data['legacy_import_calls']),
                      'known_root_paths':len(data['paths']),
                      'parse_errors':len(data['parse_errors']),
                      'report':str(OUTPUT/'review.md'), 'full_pytest_run':False},ensure_ascii=False,indent=2))
    if data['parse_errors']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
```

## test_audit.py

```python
"""Focused tests for the R5-R8 inspection algorithm."""
from pathlib import Path

from audit import investigate, render_report, shortest_path, active_sources


def test_shortest_path_tracks_import_chain():
    graph = {'a.py': {'b.py'}, 'b.py': {'c.py'}, 'c.py': set()}
    assert shortest_path(graph, 'a.py', 'c.py') == ['a.py', 'b.py', 'c.py']


def test_shortest_path_rejects_disconnected_modules():
    graph = {'a.py':set(), 'b.py':set()}
    assert shortest_path(graph,'a.py','b.py') is None


def test_active_sources_does_not_include_backups(tmp_path: Path):
    for name in ('web_group_proof.py','web_group_proof.phase165_r48_backup.py','audit_old.py'):
        (tmp_path/name).write_text('pass\n',encoding='utf-8')
    assert [p.name for p in active_sources(tmp_path)] == ['web_group_proof.py']


def test_investigate_finds_legacy_callers_and_public_isolation(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('from canonical import entry\n\ndef route():\n    return entry()\n',encoding='utf-8')
    (tmp_path/'canonical.py').write_text('def entry():\n    return 1\n',encoding='utf-8')
    (tmp_path/'phase162_web_narrative_integration.py').write_text('from phase162_r3_narrative_connection import render_phase162_r3_narrative\n\ndef old():\n    return render_phase162_r3_narrative()\n',encoding='utf-8')
    (tmp_path/'phase162_r3_narrative_connection.py').write_text('def render_phase162_r3_narrative():\n    return "old"\n',encoding='utf-8')
    result=investigate(tmp_path)
    assert result['checks']['legacy_phase162_web_has_no_public_import_route']
    assert len(result['legacy_import_calls']) == 1
    assert result['legacy_import_calls'][0]['symbol']=='render_phase162_r3_narrative'


def test_investigate_detects_public_import_of_legacy(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('from phase162_web_narrative_integration import old\n',encoding='utf-8')
    (tmp_path/'phase162_web_narrative_integration.py').write_text('def old():\n    return 1\n',encoding='utf-8')
    data=investigate(tmp_path)
    assert not data['checks']['legacy_phase162_web_has_no_public_import_route']


def test_report_contains_actual_paths_and_limitations(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('pass\n',encoding='utf-8')
    report=render_report(investigate(tmp_path))
    assert '公開入口' in report
    assert '限界' in report
    assert 'web_group_proof.py' in report
```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = "$package$([IO.Path]::PathSeparator)$project$([IO.Path]::PathSeparator)$env:PYTHONPATH"
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python -m pytest -q (Join-Path $package 'test_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R8 audit unit tests failed' }
& $python (Join-Path $package 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R8 audit failed. Inspect audit_output.' }
Write-Output 'R5-R8 public-entry boundary evidence recorded; REVIEW REQUIRED. Application source unchanged; full pytest NOT run.'
```
