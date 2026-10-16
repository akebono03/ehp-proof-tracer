"""R6-1 continuation: read-only, evidence-preserving search-branch inventory."""
from __future__ import annotations
import ast
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRY = ('phase165_r52_r9_shared_math', 'phase165_r3_recursive_search', 'phase165_goal_only_search', 'phase165_r52_r2_search_adapter')
KNOWN_GROUP_ADAPTERS = {'phase165_r52_r23_existing_rule_adapter': 'expand_existing_pi43_rules'}
MATH_TOKENS = ('TodaPrimaryGroup', 'pi32_goal', 'pi43', 'pi4_3', 'pi3_2', 'pi5_3', 'pi4_2', 'pi54', 'pi5_4')
SEARCH_WORDS = ('goal', 'expand', 'search', 'backward', 'provider', 'rule', 'reconstruct')


def _imports(tree: ast.AST) -> set[str]:
    values = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            values.add(node.module)
        if isinstance(node, ast.Import):
            values.update(alias.name for alias in node.names)
    return values


def _branch_evidence(node: ast.AST, lines: list[str]) -> list[dict]:
    findings = []
    for branch in ast.walk(node):
        if not isinstance(branch, (ast.If, ast.IfExp, ast.Match)):
            continue
        condition = branch.test if isinstance(branch, (ast.If, ast.IfExp)) else branch.subject
        start = condition.lineno - 1
        end = getattr(condition, 'end_lineno', condition.lineno)
        if end - start > 100:
            expression = ' '.join(lines[start:start + 100])
        else:
            expression = ' '.join(lines[start:end])
        if not any(token in expression for token in MATH_TOKENS):
            continue
        concrete = any(token in expression for token in ('pi32_goal', 'pi43', 'pi4_3', 'pi3_2', 'pi5_3', 'pi4_2', 'pi54', 'pi5_4'))
        findings.append({'line': branch.lineno, 'expression': expression[:240],
                         'kind': 'NAMED_GROUP_BRANCH' if concrete else 'GROUP_TYPE_BRANCH_REVIEW'})
    return findings


def classify(root: Path) -> dict:
    if not root.is_dir():
        raise ValueError('repository root not found')
    modules = {}
    skipped = []
    for path in sorted(root.glob('*.py')):
        try:
            source = path.read_text(encoding='utf-8-sig')
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            skipped.append({'file': path.name, 'reason': type(exc).__name__})
            continue
        functions = []
        source_lines = source.splitlines()
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            name = node.name
            if not any(word in name.lower() for word in SEARCH_WORDS):
                continue
            branches = _branch_evidence(node, source_lines)
            functions.append({'name': name, 'line': node.lineno, 'branches': branches})
        modules[path.stem] = {'file': path.name, 'imports': sorted(_imports(tree)), 'functions': functions,
                              'source': source}
    incoming = defaultdict(list)
    for module, info in modules.items():
        for dependency in info['imports']:
            if dependency in modules:
                incoming[dependency].append(module)
    seen = set()
    queue = deque((name, (name,)) for name in ENTRY if name in modules)
    reachable = {}
    while queue:
        name, path = queue.popleft()
        if name in seen:
            continue
        seen.add(name)
        reachable[name] = list(path)
        for dependency in modules[name]['imports']:
            if dependency in modules and dependency not in seen:
                queue.append((dependency, path + (dependency,)))
    rows = []
    for module, info in modules.items():
        for function in info['functions']:
            branches = function['branches']
            if module in KNOWN_GROUP_ADAPTERS and function['name'] == KNOWN_GROUP_ADAPTERS[module]:
                category = 'ACTIVE_GROUP_SPECIFIC_ADAPTER' if module in reachable else 'GROUP_SPECIFIC_ADAPTER_NOT_REACHED_BY_IMPORT_GRAPH'
            elif branches and any(x['kind'] == 'NAMED_GROUP_BRANCH' for x in branches):
                category = 'NAMED_GROUP_BRANCH_REVIEW'
            elif branches:
                category = 'GROUP_TYPE_BRANCH_REVIEW'
            elif module in reachable:
                category = 'REACHABLE_COMMON_OR_UNCLASSIFIED'
            else:
                category = 'NOT_REACHABLE_FROM_SELECTED_ENTRIES'
            rows.append({'file': info['file'], 'function': function['name'], 'line': function['line'],
                         'category': category, 'reachable_by_imports': module in reachable,
                         'import_path': reachable.get(module, []), 'importers': sorted(incoming[module]),
                         'conditions': branches})
    shared = modules.get('phase165_r52_r9_shared_math', {}).get('source', '')
    adapter = modules.get('phase165_r52_r23_existing_rule_adapter', {}).get('source', '')
    checks = {
        'pi43_adapter_imported': 'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules' in shared,
        'pi43_adapter_in_shared_provider': 'expand_existing_pi43_rules,' in shared,
        'pi43_adapter_has_fixed_target': 'TodaPrimaryGroup(4, 3)' in adapter,
        'generic_backward_provider_connected': 'generic_provider(goal)' in shared,
    }
    summary = Counter(row['category'] for row in rows)
    return {'phase': '165 R6-1 continuation', 'mode': 'READ_ONLY',
            'scope': 'repository-root Python modules, top-level named search functions and module import graph',
            'limitations': ['import reachability is an over-approximation, not runtime call proof',
                            'dynamic imports and classes/nested functions may be missed',
                            'named-group branches require human semantic judgment',
                            'prior 450 candidates are not reproduced verbatim by this different classifier'],
            'entry_modules': list(ENTRY), 'checks': checks, 'counts': dict(summary),
            'python_files': len(modules), 'functions_examined': len(rows),
            'reachable_module_count': len(reachable), 'skipped': skipped, 'records': rows}


def main():
    report = classify(ROOT)
    folder = Path(__file__).resolve().parent
    (folder / 'classification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 165 R6-1 追加監査', '', '静的 import グラフであり、実行時呼び出しの証明ではありません。', '',
             '## 件数', '']
    lines += [f'- {k}: {v}' for k,v in sorted(report['counts'].items())]
    lines += ['', '## 接続確認', '']
    lines += [f'- {k}: {v}' for k,v in report['checks'].items()]
    lines += ['', '## 審査が必要な候補', '']
    for item in report['records']:
        if item['category'] in {'ACTIVE_GROUP_SPECIFIC_ADAPTER', 'NAMED_GROUP_BRANCH_REVIEW', 'GROUP_SPECIFIC_ADAPTER_NOT_REACHED_BY_IMPORT_GRAPH'}:
            lines.append(f"- `{item['file']}:{item['line']}` `{item['function']}` — {item['category']} (import-reachable: {item['reachable_by_imports']})")
    lines += ['', '## 制限', ''] + [f'- {x}' for x in report['limitations']]
    (folder / 'classification.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'phase': report['phase'], 'python_files': report['python_files'],
                      'functions_examined': report['functions_examined'], 'counts': report['counts'],
                      'checks': report['checks'], 'output': str(folder / 'classification.json')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
