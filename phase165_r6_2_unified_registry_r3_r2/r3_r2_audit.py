"""Read-only AST mapping of non-R8 providers to explicitly referenced rule factories."""
from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from pathlib import Path

from phase165_r6_2_unified_registry_r3.r3_inventory import audit as r3_audit, dotted, read_source


def imports_for(tree: ast.AST) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result[alias.asname or alias.name.split('.')[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                if alias.name != '*':
                    result[alias.asname or alias.name] = node.module + '.' + alias.name
    return result


def resolve(symbol: str, imports: dict[str, str], owner: str) -> str:
    parts = symbol.split('.')
    if parts[0] in imports:
        return imports[parts[0]] + ('.' + '.'.join(parts[1:]) if len(parts) > 1 else '')
    if len(parts) == 1:
        return owner + '.' + symbol
    return symbol


def top_functions(tree: ast.AST) -> dict[str, ast.FunctionDef]:
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def inspect_function(root: Path, identifier: str, known_rules: set[str]) -> dict:
    parts = identifier.rsplit('.', 1)
    if len(parts) != 2:
        return {'provider_id': identifier, 'status': 'DYNAMIC_OR_UNRESOLVED', 'rule_links': []}
    module, name = parts
    path = root / (module.replace('.', '/') + '.py')
    if not path.is_file():
        return {'provider_id': identifier, 'status': 'SOURCE_NOT_FOUND', 'rule_links': []}
    tree = read_source(path)
    fn = top_functions(tree).get(name)
    if fn is None:
        return {'provider_id': identifier, 'status': 'FUNCTION_NOT_FOUND', 'rule_links': []}
    aliases = imports_for(tree)
    links = []
    calls = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        raw = dotted(node.func)
        if not raw:
            continue
        full = resolve(raw, aliases, module)
        if full in known_rules:
            links.append({'rule_id': full, 'kind': 'DIRECT_R8_FACTORY', 'line': node.lineno})
        elif full.endswith('_inference_rule'):
            links.append({'rule_id': full, 'kind': 'OUTSIDE_R8_OR_UNRESOLVED_FACTORY', 'line': node.lineno})
        elif raw in ('InferenceRule', 'InferenceRuleCatalogEntry') or full.endswith('.InferenceRule'):
            links.append({'rule_id': None, 'kind': 'CONSTRUCTS_RULE_OBJECT', 'line': node.lineno})
        elif raw in ('GoalExpansion', 'build_generic_backward_expansion_provider', 'reverse_rules_from_witnesses', 'generate_seeded_backward_goals') or raw.startswith('expand_'):
            calls.append({'callee': full, 'line': node.lineno})
    links.sort(key=lambda x: (x['line'], str(x['rule_id'])))
    calls.sort(key=lambda x: (x['line'], x['callee']))
    return {'provider_id': identifier, 'status': 'SOURCE_INSPECTED', 'rule_links': links,
            'provider_calls': calls, 'classification': 'RULE_FACTORY_REFERENCED' if links else 'NO_DIRECT_RULE_FACTORY_IDENTIFIED',
            'mathematical_equivalence_verified': False}


def inspect_shared(root: Path, entries: list[dict], known_rules: set[str]) -> list[dict]:
    tree = read_source(root / 'phase165_r52_r9_shared_math.py')
    aliases = imports_for(tree)
    result = []
    seen = set()
    for entry in entries:
        raw = entry['symbol']
        if raw in ('provider(goal)', 'new') or raw.startswith('dynamic') or raw == 'extra_providers':
            identifier = raw
        else:
            identifier = resolve(raw, aliases, 'phase165_r52_r9_shared_math')
        key = (raw, entry['connection'], entry['line'])
        if key in seen:
            continue
        seen.add(key)
        result.append({'reference': raw, 'provider_id': identifier, 'connection': entry['connection'],
                       'line': entry['line'], 'source': 'phase165_r52_r9_shared_math.py'})
    return result


def perform(root: Path) -> dict:
    base = r3_audit(root)
    known = set(base['r8_factory_ids'])
    connections = inspect_shared(root, base['shared_provider_connections'], known)
    inspected = {x['provider_id'] for x in connections}
    inspected.update(x['symbol'] for x in base['other_expand_functions'])
    inspected = sorted(x for x in inspected if x not in ('provider(goal)', 'extra_providers'))
    providers = [inspect_function(root, x, known) for x in inspected]
    links = [link for item in providers for link in item['rule_links']]
    totals = dict(sorted(Counter(link['kind'] for link in links).items()))
    return {'phase': '165 R6-2 Unified Registry R3-2', 'status': 'STATIC_MAPPING_ONLY',
            'r8_factory_count': len(known), 'r3_shared_connection_count': len(connections),
            'r3_other_expand_candidate_count': len(base['other_expand_functions']),
            'shared_connections': connections, 'providers': providers,
            'factory_reference_kinds': totals, 'rule_factory_references': links,
            'duplicate_rule_factory_references': sorted(rule for rule,count in Counter(
                link['rule_id'] for link in links if link['rule_id']).items() if count > 1),
            'runtime_verified': False, 'proof_verified': False, 'production_modified': False,
            'limitations': ['Only direct AST calls are rule mappings, not mathematical equivalence.',
                            'Provider wrappers may invoke other providers transitively; no closure is asserted.',
                            'R3 static inventory is not a complete project-wide enumeration.',
                            'The R1 runtime file may differ from GitHub until committed.']}


def markdown(data: dict) -> str:
    lines = ['# R3-2 Provider と規則の静的対応監査', '',
             '- 状態: `STATIC_MAPPING_ONLY`',
             '- R8 factory: {}'.format(data['r8_factory_count']),
             '- 共通接続参照: {}'.format(data['r3_shared_connection_count']),
             '- その他 expand_ 候補: {}'.format(data['r3_other_expand_candidate_count']),
             '- 証明検証: なし', '', '## 共通接続', '',
             '| 参照名 | 解決した Provider ID | 接続種別 |', '|---|---|---|']
    for x in data['shared_connections']:
        lines.append('| `{}` | `{}` | `{}` |'.format(x['reference'], x['provider_id'], x['connection']))
    lines += ['', '## Provider と Rule factory の対応', '', '| Provider ID | 状態 | 直接参照する規則 |', '|---|---|---|']
    for item in data['providers']:
        rules = ', '.join('`{}` ({})'.format(x['rule_id'] or 'anonymous',x['kind']) for x in item['rule_links']) or '未特定'
        lines.append('| `{}` | `{}` | {} |'.format(item['provider_id'],item['status'],rules))
    lines += ['', '## 注意', '', '直接参照の一致は数学的に同等であることを意味しない。',
              'Provider から Provider への間接呼び出しは実行検証していない。',
              '本番コードは変更しない。', '']
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = perform(args.root.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'provider_rule_mapping.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'provider_rule_mapping.md').write_text(markdown(data), encoding='utf-8')
    print(json.dumps({'status':data['status'], 'r8_factories':data['r8_factory_count'],
                      'connections':data['r3_shared_connection_count'],
                      'expand_candidates':data['r3_other_expand_candidate_count'],
                      'direct_factory_references':len(data['rule_factory_references']),
                      'production_modified':False, 'full_pytest_run':False},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
