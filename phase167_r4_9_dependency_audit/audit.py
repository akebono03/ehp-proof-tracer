from __future__ import annotations
import json
from pathlib import Path

import toda_group_proof_narrative_contribution_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

original = renderer.link_toda_group_proof_narrative_reference_body_consumers
captured = []

def instrument(presentation, body_markdown, reference_entries):
    mapping = renderer._phase154_r5_reference_source_steps_by_number(presentation, reference_entries)
    def brief(step):
        rule = getattr(step, 'inference_rule', None)
        reference = getattr(rule, 'literature_reference', None)
        return {
            'id': id(step),
            'rule': str(getattr(step, 'rule', '')),
            'rule_name': getattr(rule, 'name', None),
            'locator': getattr(reference, 'locator', None),
            'conclusion_type': type(step.conclusion).__name__,
            'conclusion': repr(step.conclusion)[:600],
            'premises': [id(x) for x in step.premises],
            'rendered': renderer._render_generic_narrative_step(step),
        }
    nodes = [node.proof_step for node in presentation.nodes]
    edges = list(presentation.edges)
    relevant = []
    for number, steps in mapping.items():
        for source in steps:
            descendants = [e.parent_step for e in edges if e.premise_step is source]
            relevant.append({
                'reference_number': number,
                'source': brief(source),
                'direct_consumers': [brief(x) for x in descendants],
            })
    result = original(presentation, body_markdown, reference_entries)
    captured.append({
        'root': brief(presentation.root_step),
        'nodes': [brief(x) for x in nodes],
        'reference_entries': [{'number': x.number,'locator': x.reference.locator,
          'proof_step_ids': [id(y) for y in x.proof_steps]} for x in reference_entries],
        'source_relationships': relevant,
        'edge_count': len(edges),
        'input_body': body_markdown,
        'output_body': result,
    })
    return result

renderer.link_toda_group_proof_narrative_reference_body_consumers = instrument
try:
    view = build_standard_web_group_proof_view(3, 1, max_depth=2, mode='narrative')
    rows = [{'prefix': line.prefix, 'math': line.statement_latex, 'suffix': line.suffix}
            for line in view.rendered_lines]
    output = {'captured': captured, 'web_rows': rows}
    destination = Path(__file__).resolve().parent / 'audit_report.json'
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print('AUDIT_REPORT:', destination)
    print('CAPTURED_CALLS:', len(captured))
    for item in rows:
        if 'pi_{4}^{5}' in (item['math'] or '') or 'pi_{5}^{5}' in (item['math'] or ''):
            print('ROW:', json.dumps(item, ensure_ascii=False))
    for idx, obj in enumerate(captured):
        print('CALL:', idx, 'REFERENCES:', [(r['number'],r['locator']) for r in obj['reference_entries']])
        for record in obj['source_relationships']:
            if record['source']['locator'] == '(5.1)' or any('Zero' in x['conclusion_type'] for x in record['direct_consumers']):
                print('SOURCE:', record['reference_number'],record['source']['conclusion_type'],record['source']['rule_name'])
                for child in record['direct_consumers']:
                    print('CHILD:',child['conclusion_type'],child['rule_name'],'premises=',len(child['premises']),'rendered=',child['rendered'])
finally:
    renderer.link_toda_group_proof_narrative_reference_body_consumers = original
