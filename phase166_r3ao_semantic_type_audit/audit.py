"""Read-only semantic type audit for 112 group-target expressions."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

import pandas as pd

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase166_r3af_goal_adapter import database_group_goal_candidates, database_zero_group_goal_candidates
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from repository import SphereRepository
from toda_human_readable_renderer import render_toda_public_group_relation_latex

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / 'results'


def selected_goal(n: int, k: int):
    zero = database_zero_group_goal_candidates(n=n, k=k)
    if zero:
        return 'zero', zero[0]
    if k >= 2:
        structured = database_structured_group_goal_candidates(n=n, k=k)
        if structured:
            return 'structured', structured[0]
    simple = database_group_goal_candidates(n=n, k=k)
    if simple:
        return 'simple', simple[0]
    return 'missing', None


def expression_dimensions(expression):
    """Return (source, target, issues), checking all composition interfaces."""
    if isinstance(expression, HomotopyElement):
        issues = []
        if type(expression.source) is not int or type(expression.target) is not int:
            issues.append('missing_atomic_dimensions')
        if type(expression.dimension) is int and expression.dimension != expression.target:
            issues.append('atomic_dimension_mismatch')
        return expression.source, expression.target, issues
    if isinstance(expression, (Suspension, IteratedSuspension)):
        source, target, issues = expression_dimensions(expression.expression)
        exponent = 1 if isinstance(expression, Suspension) else expression.exponent
        if type(exponent) is not int or exponent < 0:
            issues.append('invalid_suspension_exponent')
            return None, None, issues
        return (source + exponent if source is not None else None,
                target + exponent if target is not None else None, issues)
    if isinstance(expression, Composition):
        ls, lt, left_issues = expression_dimensions(expression.left)
        rs, rt, right_issues = expression_dimensions(expression.right)
        issues = left_issues + right_issues
        if ls is None or rt is None:
            issues.append('unverifiable_composition_interface')
        elif ls != rt:
            issues.append('composition_interface_mismatch')
        return rs, lt, issues
    return None, None, ['unhandled_expression_type']


def audit_one(repo, generators, n: int, k: int):
    source, statement = selected_goal(n, k)
    rows = repo._rows(n, k)
    components = repo.get_group(n, k).components
    record = {'n': n, 'k': k, 'source': source, 'status': 'pass', 'issues': [],
              'generator_checks': [], 'latex': None}
    if statement is None:
        record['issues'].append('missing_goal')
    else:
        record['latex'] = render_toda_public_group_relation_latex(statement)
        if not record['latex']:
            record['issues'].append('missing_latex')
    if source == 'zero':
        if len(components) != 1 or components[0].order != 0:
            record['issues'].append('zero_group_db_mismatch')
    elif source != 'missing':
        rhs = statement.rhs
        parts = rhs.summands if isinstance(rhs, DirectSumGroup) else (rhs,)
        if len(parts) != len(components):
            record['issues'].append('component_count_mismatch')
        for idx, (part, component) in enumerate(zip(parts, components)):
            issues = []
            if isinstance(part, FiniteCyclicGroup):
                if part.order != component.order:
                    issues.append('order_mismatch')
            elif isinstance(part, FreeCyclicGroup):
                if component.order != float('inf'):
                    issues.append('order_mismatch')
            else:
                issues.append('unsupported_group_component')
            generator = getattr(part, 'generator', None)
            if generator is not None:
                src, tgt, type_issues = expression_dimensions(generator)
                issues.extend(type_issues)
                if src != n + k or tgt != n:
                    issues.append('generator_ambient_dimension_mismatch')
            else:
                src = tgt = None
            if source == 'structured':
                cursor = n
                for identifier in component.element:
                    if identifier not in generators.index:
                        issues.append('unknown_element_id')
                        break
                    row = generators.loc[identifier]
                    if not isinstance(row, pd.Series):
                        issues.append('ambiguous_element_id')
                        break
                    if cursor < int(row['n']):
                        issues.append('factor_below_minimum_dimension')
                    cursor += int(row['k'])
                if cursor != n + k:
                    issues.append('element_stem_sum_mismatch')
            else:
                # The simple adapter builds a single HomotopyElement from a
                # generator label; it does not reconstruct Element IDs.
                # Degree is checkable, but mathematical identity remains open.
                if not component.element:
                    issues.append('missing_element_id_for_semantic_comparison')
                else:
                    cursor = n
                    for identifier in component.element:
                        if identifier not in generators.index:
                            issues.append('unknown_element_id')
                            break
                        cursor += int(generators.loc[identifier]['k'])
                    if cursor != n + k:
                        issues.append('simple_element_stem_sum_mismatch')
            record['generator_checks'].append({
                'index': idx, 'db_generator': component.generator,
                'element_ids': component.element, 'source_dimension': src,
                'target_dimension': tgt, 'issues': issues,
            })
            record['issues'].extend(issues)
    if record['issues']:
        record['status'] = 'issue'
    elif source == 'simple':
        record['status'] = 'partially_verified'
    return record


def run():
    repo = SphereRepository(ROOT / 'data' / 'sphere.csv')
    generators = pd.read_csv(ROOT / 'data' / 'HyoujiGen.csv').set_index('id')
    records = [audit_one(repo, generators, n, k)
               for n in range(2, 16) for k in range(8)]
    summary = {
        'phase': '166-r3ao-semantic-type-audit',
        'count': len(records),
        'source_counts': dict(Counter(r['source'] for r in records)),
        'status_counts': dict(Counter(r['status'] for r in records)),
        'issue_counts': dict(Counter(issue for r in records for issue in r['issues'])),
        'production_code_modified': False,
        'proof_search_executed': False,
        'scope': 'group orders, generator degree, composition interfaces and Element-ID stems; simple-name identity not fully verified',
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'report.json').write_text(json.dumps({'summary': summary, 'records': records}, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 166 R3-AO 型・次元の意味的監査', '', '## Summary', '', '```json', json.dumps(summary, ensure_ascii=False, indent=2), '```', '', '## 各群', '']
    for rec in records:
        lines.extend([f"### n={rec['n']} k={rec['k']} — {rec['status']}", '',
                      f"取得経路: {rec['source']}", '',
                      f"TeX: `{rec['latex']}`", '',
                      f"検出事項: {', '.join(rec['issues']) if rec['issues'] else 'なし'}", ''])
        for gen in rec['generator_checks']:
            lines.append(f"- {gen['db_generator']}: Element={gen['element_ids']}, source={gen['source_dimension']}, target={gen['target_dimension']}, issues={gen['issues']}")
        lines.append('')
    (OUT / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    return summary


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
    print('REPORT:', OUT / 'report.json')
