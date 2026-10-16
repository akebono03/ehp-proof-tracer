"""Read-only R4-A-R4 actual registered typed-goal applicability audit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def evaluate_goal(rule, goal, *, r8_factory, generic_factory):
    """Check only emitted typed GoalExpansion proposals; never certify a proof."""
    def collect(factory):
        try:
            expansions = factory((rule,))(goal)
            return {'status': 'PROPOSED' if expansions else 'NO_MATCH',
                    'count': len(expansions),
                    'premise_counts': [len(expansion.subgoals) for expansion in expansions]}
        except Exception as exc:
            return {'status': 'ERROR', 'error': type(exc).__name__ + ': ' + str(exc)[:180]}
    return {'r8': collect(r8_factory), 'r26': collect(generic_factory)}


def probe(root: Path, *, max_goals=250):
    root = root.resolve()
    sys.path.insert(0, str(root))
    from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, create_rule_expansion_provider
    from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from proof import InferenceRule
    from importlib import import_module
    import inspect
    from collections import Counter
    from phase165_r8_rule_provider import discover_inference_rules

    discovered, report = discover_inference_rules()
    inventory = []
    for module_name in DEFAULT_RULE_MODULES:
        module = import_module(module_name)
        for name, factory in sorted(vars(module).items()):
            if not (name.endswith('_inference_rule') and callable(factory)
                    and getattr(factory, '__module__', None) == module.__name__):
                continue
            sig = inspect.signature(factory)
            required = [p for p in sig.parameters.values() if p.default is inspect.Parameter.empty
                        and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                      inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                      inspect.Parameter.KEYWORD_ONLY)]
            if required:
                inventory.append({'rule_id': module_name + '.' + name, 'status': 'REQUIRES_INPUT',
                                  'goal_probe_status': 'NOT_TESTED'})
                continue
            try:
                rule = factory()
                if not isinstance(rule, InferenceRule):
                    inventory.append({'rule_id': module_name + '.' + name, 'status': 'NOT_RULE',
                                      'goal_probe_status': 'NOT_TESTED'})
                    continue
                inventory.append({'rule_id': module_name + '.' + name, 'status': 'INSTANTIATED',
                                  'name': rule.name, 'structural_candidate': bool(rule.conclusion_pattern is not None and rule.premise_patterns),
                                  'rule': rule})
            except Exception as exc:
                inventory.append({'rule_id': module_name + '.' + name, 'status': 'FACTORY_ERROR',
                                  'error': type(exc).__name__ + ': ' + str(exc)[:180],
                                  'goal_probe_status': 'NOT_TESTED'})
    actual_names = Counter(row['name'] for row in inventory if row['status'] == 'INSTANTIATED')
    r8_names = Counter(rule.name for rule in discovered)
    if actual_names != r8_names:
        return {'status': 'IDENTITY_MISMATCH', 'rules': [{k:v for k,v in r.items() if k != 'rule'} for r in inventory],
                'r8_count': len(discovered)}

    try:
        bridge = build_shared_typed_bridge()
        # Registered assertion contents are used verbatim; no guessed group structures.
        source = list(bridge.registry._assertions.values())
        goals = []
        for entry in source:
            content = getattr(entry, 'content', None)
            if content is not None and not any(type(content) is type(old) and content == old for old in goals):
                goals.append(content)
        goal_total = len(goals)
        goals = goals[:max_goals]
        source_status = 'REGISTERED_ASSERTION_CONTENT'
    except Exception as exc:
        goals = []
        goal_total = 0
        source_status = 'REGISTRY_ERROR:' + type(exc).__name__ + ':' + str(exc)[:180]
    results = []
    for entry in inventory:
        rule = entry.pop('rule', None)
        if rule is None:
            results.append(entry)
            continue
        entry['goal_probe_status'] = 'NOT_TESTED' if not goals else 'NO_MATCH'
        entry['r8_proposed'] = 0
        entry['r26_proposed'] = 0
        entry['goal_errors'] = []
        if entry['structural_candidate']:
            for index, goal in enumerate(goals):
                tested = evaluate_goal(rule, goal, r8_factory=create_rule_expansion_provider,
                                       generic_factory=build_generic_backward_expansion_provider)
                for provider, field in [('r8', 'r8_proposed'), ('r26', 'r26_proposed')]:
                    if tested[provider]['status'] == 'PROPOSED':
                        entry[field] += 1
                    elif tested[provider]['status'] == 'ERROR':
                        entry['goal_errors'].append({'goal_index': index, 'provider': provider, 'error': tested[provider]['error']})
            if entry['r8_proposed'] or entry['r26_proposed']:
                entry['goal_probe_status'] = 'PROPOSED'
            elif entry['goal_errors']:
                entry['goal_probe_status'] = 'ERROR'
        results.append(entry)
    return {'status': 'OK' if source_status == 'REGISTERED_ASSERTION_CONTENT' else 'INCOMPLETE',
            'phase': '165 R6-2 R4-A-R4', 'mode': 'READ_ONLY_REGISTERED_GOAL_PROPOSALS',
            'source_status': source_status, 'source_assertions': len(source) if goals else 0,
            'unique_goals_available': goal_total, 'goals_examined': len(goals),
            'truncated': goal_total > max_goals, 'factory_count': len(inventory),
            'instantiated': sum(x['status'] == 'INSTANTIATED' for x in results),
            'structural_candidates': sum(x.get('structural_candidate', False) for x in results),
            'rules_with_r8_proposals': sum(x.get('r8_proposed', 0) > 0 for x in results),
            'rules_with_r26_proposals': sum(x.get('r26_proposed', 0) > 0 for x in results),
            'proof_verified': 0, 'recursive_reachability_verified': 0,
            'rules': results, 'r8_discovered_count': len(discovered),
            'r8_skipped_factories': list(report.skipped_factories),
            'limitations': ['Only registered assertion content is sampled as Goals.',
                            'No group-specific Goal or witness is manufactured.',
                            'A generated GoalExpansion is a proposal, not a completed proof.',
                            'R26 provider execution is confirmed, not recursive reconstruction.',
                            'Only R8 factory-discovered rule family is covered here.',
                            'Registry bridge construction can execute existing production import/build logic.']}


def markdown(data):
    lines = ['# Phase 165 R6-2 R4-A-R4 Goal 適用監査', '',
             '- status: `' + data['status'] + '`',
             '- goal source: `' + data.get('source_status', 'UNKNOWN').replace('|', '/') + '`',
             '- 登録済み Goal（重複除去後）: ' + str(data.get('unique_goals_available', 0)),
             '- 実際に試した Goal: ' + str(data.get('goals_examined', 0)),
             '- R8 候補を出した規則: ' + str(data.get('rules_with_r8_proposals', 0)),
             '- R26 候補を出した規則: ' + str(data.get('rules_with_r26_proposals', 0)),
             '- 完成証明確認: 0（この Phase では試行しない）', '',
             '| Rule ID | status | R8 Goal 数 | R26 Goal 数 |', '|---|---|---:|---:|']
    for entry in data.get('rules', []):
        lines.append('| ' + ' | '.join(str(x).replace('|', '/') for x in (
            entry['rule_id'], entry.get('goal_probe_status', 'NOT_TESTED'),
            entry.get('r8_proposed', '—'), entry.get('r26_proposed', '—'))) + ' |')
    lines += ['', '## 制約', ''] + ['- ' + x for x in data.get('limitations', [])]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--max-goals', type=int, default=250)
    args = parser.parse_args()
    if args.max_goals < 1:
        parser.error('--max-goals must be positive')
    data = probe(args.root, max_goals=args.max_goals)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'goal_applicability.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (args.out / 'goal_applicability.md').write_text(markdown(data), encoding='utf-8')
    print(json.dumps({k: v for k, v in data.items() if k in ('status', 'source_status', 'unique_goals_available', 'goals_examined', 'rules_with_r8_proposals', 'rules_with_r26_proposals', 'proof_verified')}, ensure_ascii=False, indent=2))
    if data['status'] != 'OK':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
