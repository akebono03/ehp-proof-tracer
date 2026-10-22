from __future__ import annotations

import inspect
import json
from pathlib import Path
from unittest.mock import patch

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import ordered_proof_ancestry
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from proof import ProofRule
from toda_rules import TodaEtaFamilyDefinitionStatement
import toda_group_proof_narrative_renderer as renderer
import toda_group_proof_narrative_shared_components as shared
from web_group_proof import build_standard_web_group_proof_view

OUT = Path(__file__).resolve().parent

def signature(statement):
    if isinstance(statement, (GeneratorSuspension, GeneratorImage)):
        return (statement.map, statement.source_generator.generator, statement.target_generator.generator)
    if isinstance(statement, TodaEtaFamilyDefinitionStatement):
        return (statement.element.generator, statement.iterated_suspension)
    return None

def main():
    original = shared._render_generic_narrative_step
    original_in_renderer = renderer._render_generic_narrative_step
    events = []
    result = search_group_from_registered_goal(n=3, k=1)
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
    assert len(roots) == 1
    ancestry = ordered_proof_ancestry(roots[0])
    selected = {id(step): i for i, step in enumerate(ancestry) if isinstance(step.conclusion, (GeneratorSuspension, GeneratorImage, TodaEtaFamilyDefinitionStatement))}

    def record(step):
        output = original(step)
        if id(step) in selected:
            frames = inspect.stack(context=0)[1:7]
            events.append({
                'index': selected[id(step)],
                'conclusion_type': type(step.conclusion).__name__,
                'output': output,
                'call_chain': [{'file': f.filename.rsplit('\\',1)[-1].rsplit('/',1)[-1], 'function': f.function, 'line': f.lineno} for f in frames],
                'premise_indices': [next((i for i, s in enumerate(ancestry) if s is p), None) for p in step.premises],
            })
        return output

    with patch.object(shared, '_render_generic_narrative_step', record), patch.object(renderer, '_render_generic_narrative_step', record):
        view = build_standard_web_group_proof_view(3,1,2,'narrative')
    lines = [s if isinstance(s,str) else (str(getattr(s,'prefix','')) + str(getattr(s,'statement_latex','') or '') + str(getattr(s,'suffix',''))) for s in view.rendered_lines]
    report = {'status': str(result.status), 'complete_view': view.key, 'step_count': len(ancestry), 'events': events, 'web_lines': lines, 'production_modified': False}
    (OUT/'trace.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('READ_ONLY:', len(events), 'typed rendering events; Web lines:',len(lines))
    print('REPORT:', OUT/'trace.json')

if __name__ == '__main__':
    main()
