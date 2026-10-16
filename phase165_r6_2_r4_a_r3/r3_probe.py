"""Read-only source-factory identity and actual registered Goal proposal probe."""
from __future__ import annotations

from collections import Counter
from importlib import import_module
import inspect
import json
from pathlib import Path
import sys


def inspect_factory_module(module_name, *, loader=import_module):
    from proof import InferenceRule
    module = loader(module_name)
    output = []
    for name, factory in sorted(vars(module).items()):
        if not (name.endswith('_inference_rule') and callable(factory)
                and getattr(factory, '__module__', None) == module.__name__):
            continue
        row = {'rule_id': module_name + '.' + name, 'module': module_name,
               'factory': name, 'factory_source_line': None,
               'status': 'UNKNOWN', 'name': None,
               'pattern_backward_candidate': False, 'goal_probe_status': 'NOT_TESTED',
               'search_connection': 'STATIC_R8_DEFAULT_PATH_ONLY'}
        try:
            row['factory_source_line'] = inspect.getsourcelines(factory)[1]
        except (OSError, TypeError):
            pass
        try:
            signature = inspect.signature(factory)
            required = [p for p in signature.parameters.values()
                        if p.default is inspect.Parameter.empty and p.kind in (
                            inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD,
                            inspect.Parameter.KEYWORD_ONLY)]
            if required:
                row['status'] = 'REQUIRES_INPUT'
            else:
                rule = factory()
                if not isinstance(rule, InferenceRule):
                    row['status'] = 'NOT_INFERENCE_RULE'
                else:
                    row['status'] = 'INSTANTIATED'
                    row['name'] = rule.name
                    row['pattern_backward_candidate'] = (
                        rule.conclusion_pattern is not None and bool(rule.premise_patterns))
                    row['premise_count'] = len(rule.premise_patterns)
        except (Exception,) as exc:
            row['status'] = 'FACTORY_ERROR'
            row['error'] = type(exc).__name__ + ': ' + str(exc)[:300]
        output.append(row)
    return output


def collect(root: Path, module_names=None):
    sys.path.insert(0, str(root.resolve()))
    from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
    modules = tuple(module_names) if module_names is not None else DEFAULT_RULE_MODULES
    rows = []
    errors = []
    r8_comp = {}
    for module in modules:
        try:
            entries = inspect_factory_module(module)
            rows.extend(entries)
            discovered, report = discover_inference_rules((module,))
            ours = Counter(x['name'] for x in entries if x['status'] == 'INSTANTIATED')
            theirs = Counter(x.name for x in discovered)
            r8_comp[module] = {'match': ours == theirs, 'r3': sum(ours.values()),
                               'r8': len(discovered), 'r8_skipped': list(report.skipped_factories)}
        except Exception as exc:
            errors.append({'module': module, 'error': type(exc).__name__ + ': ' + str(exc)[:300]})
    # Existing typed Goals are used as probes only when independently available.
    # No fake Goal, witness, or ProofStep is constructed in this audit.
    return {
        'phase': '165 R6-2 R4-A-R3', 'status': 'OK' if not errors and all(v['match'] for v in r8_comp.values()) else 'INCOMPLETE',
        'mode': 'READ_ONLY_FACTORY_IDENTITY', 'source_root': str(root.resolve()),
        'rules': rows, 'r8_comparison': r8_comp, 'errors': errors,
        'counts': {'factories': len(rows), 'instantiated': sum(x['status'] == 'INSTANTIATED' for x in rows),
                   'pattern_backward_candidates': sum(x['pattern_backward_candidate'] for x in rows),
                   'goal_verified': 0, 'proof_verified': 0},
        'limitations': [
            'Source factory ID is module.function; it is stable only while the source location and name remain unchanged.',
            'R8 and this probe instantiate factories separately; rule-name multisets are compared, not object identity.',
            'A conclusion/premise pattern is not evidence of a successful Goal match.',
            'No registered Goal application is performed in this conservative pass; goal_verified remains zero.',
            'STATIC_R8_DEFAULT_PATH_ONLY is not a runtime proof of common search reachability.',
            'Imports and factory execution can have production side effects; the probe itself writes only its report.',
        ],
    }


def markdown(data):
    c = data['counts']
    lines = ['# Phase 165 R6-2 R4-A-R3 規則識別子監査', '',
             '- 状態: `' + data['status'] + '`',
             '- 対象: `' + data['source_root'] + '`', '',
             '| 指標 | 件数 |', '|---|---:|']
    for key, value in c.items():
        lines.append('| ' + key + ' | ' + str(value) + ' |')
    lines += ['', '## 規則別の識別結果', '',
              '| Rule ID | status | rule.name | 逆向き構造候補 | Goal 実証 |',
              '|---|---|---|---|---|']
    for r in data['rules']:
        cells = [r['rule_id'], r['status'], r.get('name') or '—',
                 '候補' if r['pattern_backward_candidate'] else '未確認', r['goal_probe_status']]
        lines.append('| ' + ' | '.join(str(x).replace('|', '/') for x in cells) + ' |')
    lines += ['', '## R8 との一致', '']
    for module, value in data['r8_comparison'].items():
        lines.append('- `' + module + '`: ' + ('一致' if value['match'] else '不一致'))
    lines += ['', '## 制約', ''] + ['- ' + x for x in data['limitations']]
    lines += ['', '## 次段階', '',
              '実際の既存 Goal と出典証人を用いる適用テストと、共通探索の再帰到達性検証は R4-A-R4 に分離する。', '']
    return '\n'.join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    data = collect(args.root)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'rule_identity.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (args.out / 'rule_identity.md').write_text(markdown(data), encoding='utf-8')
    print(json.dumps({'status': data['status'], 'counts': data['counts'], 'out': str(args.out)}, ensure_ascii=False, indent=2))
    if data['status'] != 'OK':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
