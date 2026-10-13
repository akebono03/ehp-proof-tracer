"""Read-only trace of exactness premises and renderer recognition for pi3^2."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r14_r41_proof_transfer import build_phase165_r41_pi32_common_replay
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference


def audit_proofstep_rules() -> dict:
    report = build_standard_toda_report(n=2, k=1)
    if len(report.candidates) != 1:
        raise ValueError('Expected one group candidate')
    result = report.candidates[0].source_candidate.group_result
    replay = build_phase165_r41_pi32_common_replay(result, 2, 'narrative')
    presentation = build_toda_group_proof_presentation(replay)
    ordered = []
    seen = set()

    def walk(step, depth):
        if id(step) in seen:
            return
        seen.add(id(step))
        rule = getattr(step, 'inference_rule', None)
        ref = extract_toda_group_proof_step_literature_reference(step)
        statement = step.conclusion
        premises = tuple(step.premises)
        ordered.append({
            'depth': depth,
            'statement_type': type(statement).__name__,
            'conclusion_repr': repr(statement)[:500],
            'rule_kind': getattr(step.rule, 'name', str(step.rule)),
            'rule_name': getattr(rule, 'name', None),
            'rule_description': getattr(rule, 'description', None),
            'premise_types': [type(x.conclusion).__name__ for x in premises],
            'premise_reprs': [repr(x.conclusion)[:220] for x in premises],
            'reference_locator': getattr(ref, 'locator', None),
            'rendered_generic': _render_generic_narrative_step(step),
        })
        for premise in premises:
            walk(premise, depth + 1)

    walk(replay.root_step, 0)
    selected = [row for row in ordered if row['statement_type'] in (
        'MapInjective', 'MapSurjective', 'MapIsomorphism',
        'TodaDeltaZeroStatement', 'MapZero', 'MapZeroMap',
    ) or ('DeltaZero' in row['statement_type'])]
    leaves = [row for row in ordered if not row['premise_types']]
    return {
        'phase': '165 R45',
        'mode': 'READ_ONLY_PROOFSTEP_RULE_AUDIT',
        'root': repr(replay.root_step.conclusion),
        'total_steps': len(ordered),
        'reference_leaf_count': len(leaves),
        'exactness_evidence_steps': [
            row for row in selected
            if any('Exactness' in x for x in row['premise_types'])
        ],
        'map_and_delta_steps': selected,
        'leaf_sources': leaves,
        'all_steps': ordered,
        'production_sources_modified': False,
        'full_pytest_run': False,
    }


def main() -> None:
    output = Path('phase165_r14_r45_output')
    output.mkdir(exist_ok=True)
    report = audit_proofstep_rules()
    path = output / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'phase': report['phase'],
        'total_steps': report['total_steps'],
        'reference_leaf_count': report['reference_leaf_count'],
        'exactness_evidence_step_count': len(report['exactness_evidence_steps']),
        'map_and_delta_step_count': len(report['map_and_delta_steps']),
        'report_path': str(path.resolve()),
        'production_sources_modified': False,
        'full_pytest_run': False,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
