"""Read-only R4-B reference / symbolic-specialization audit."""
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
    extract_toda_group_proof_step_literature_reference,
)
from toda_literature_statement_boundary import classify_toda_literature_statement_step
from toda_stable_transport import build_canonical_toda_45_isomorphism_step
from toda_group_proof_narrative_renderer import (
    _phase158_baseline_render_toda_group_proof_narrative_markdown,
)


def walk_steps(root):
    """Traverse exactly the premise edges of the supplied proof tree."""
    queue = deque([(root, 0)])
    seen = set()
    while queue:
        step, depth = queue.popleft()
        if id(step) in seen:
            continue
        seen.add(id(step))
        yield step, depth
        queue.extend((premise, depth + 1) for premise in step.premises)


def step_record(step, depth, root):
    rule = step.inference_rule
    explicit = None if rule is None else rule.literature_reference
    selected = extract_toda_group_proof_step_literature_reference(step)
    boundary = classify_toda_literature_statement_step(step)
    if explicit is not None:
        origin = 'explicit'
    elif selected is not None:
        origin = 'inferred_or_boundary'
    else:
        origin = 'absent'
    return {
        'depth': depth,
        'is_root': step is root,
        'conclusion_type': type(step.conclusion).__name__,
        'conclusion': repr(step.conclusion),
        'rule_name': None if rule is None else rule.name,
        'premises': len(step.premises),
        'explicit_reference': None if explicit is None else explicit.locator,
        'selected_reference': None if selected is None else selected.locator,
        'reference_origin': origin,
        'boundary': None if boundary is None else str(boundary.classification),
        'boundary_component': None if boundary is None else boundary.component_key,
    }


def audit_group(n):
    presentation, _, _, _ = _method_evidence_data(n, 1)
    root = presentation.root_step
    steps = list(walk_steps(root))
    records = [step_record(s, d, root) for s, d in steps]
    entries = build_toda_group_proof_narrative_reference_entries(presentation)
    reference_entries = [{
        'locator': e.reference.locator,
        'step_conclusions': [repr(s.conclusion) for s in e.proof_steps],
        'includes_root': any(s is root for s in e.proof_steps),
        'includes_equivalent_root_conclusion': any(s.conclusion == root.conclusion for s in e.proof_steps),
    } for e in entries]
    iso_in_tree = [r for r in records if r['conclusion_type'] == 'Toda45IsomorphismStatement']
    canonical = build_canonical_toda_45_isomorphism_step(presentation.source_replay.group_result.target)
    baseline = _phase158_baseline_render_toda_group_proof_narrative_markdown(presentation)
    return {
        'target': f'pi_{n+1}^{n}',
        'root': repr(root.conclusion),
        'tree_step_count': len(records),
        'presentation_node_count': len(presentation.nodes),
        'presentation_edge_count': len(presentation.edges),
        'steps': records,
        'presentation_references_before_filtering': reference_entries,
        'tree_toda45_steps': iso_in_tree,
        'canonical_toda45_comparison_only': {
            'conclusion': repr(canonical.conclusion),
            'premises': [repr(p.conclusion) for p in canonical.premises],
            'warning': 'Built separately for comparison; existence does not establish membership in the existing root ancestry.',
        },
        'baseline': baseline,
        'flags': {
            'baseline_has_symbolic_n': r'\eta_{n}' in baseline or r'\pi_{n + 1}^{n}' in baseline,
            'baseline_contains_toda45_reference': '(4.5)' in baseline.split('## 証明', 1)[0],
            'baseline_has_target_in_reference_section': f'\\pi_{{{n+1}}}^{{{n}}}' in baseline.split('## 証明', 1)[0],
        },
    }


def write_report(groups, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'audit.json').write_text(json.dumps(groups, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    lines = ['# Phase 162 R4-B Reference / specialization audit', '', '観測結果。数学的な特殊化の妥当性を自動証明したものではない。', '']
    for group in groups:
        lines += [f"## {group['target']}", '', f"Tree steps: {group['tree_step_count']}; Presentation nodes: {group['presentation_node_count']}; edges: {group['presentation_edge_count']}", '', '### Reference candidates before filtering', '']
        for entry in group['presentation_references_before_filtering']:
            lines.append(f"- {entry['locator']}: includes root={entry['includes_root']}; equivalent root conclusion={entry['includes_equivalent_root_conclusion']}")
        lines += ['', '### Explicit / inferred references in full root ancestry', '']
        for i, rec in enumerate(group['steps']):
            if rec['selected_reference']:
                lines.append(f"- Step {i}: {rec['selected_reference']} ({rec['reference_origin']}); {rec['conclusion_type']}; boundary={rec['boundary']}")
        lines += ['', '### Toda (4.5) in tree', '']
        for rec in group['tree_toda45_steps']:
            lines.append(f"- {rec['conclusion']}")
        lines += ['', '### Independently built canonical specialization (not tree evidence)', '', f"- {group['canonical_toda45_comparison_only']['conclusion']}", '', '### Baseline flags', '']
        for key, value in group['flags'].items():
            lines.append(f'- {key}: {value}')
        lines += ['', '### Baseline Markdown', '', '```text', group['baseline'].rstrip(), '```', '']
    (output_dir / 'comparison.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'audit_output')
    args = parser.parse_args()
    groups = [audit_group(4), audit_group(5)]
    write_report(groups, args.output)
    for group in groups:
        print(group['target'], group['flags'])
    print('Wrote:', args.output / 'comparison.md', 'and', args.output / 'audit.json')


if __name__ == '__main__':
    main()
