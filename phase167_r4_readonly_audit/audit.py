from __future__ import annotations
import json
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timezone

ROOT = Path.cwd()
OUT = ROOT / 'phase167_r4_readonly_results'
OUT.mkdir(exist_ok=True)

def main():
    import web_group_proof
    import phase165_r56_presentation_adapter as adapter
    import phase165_r57_r10_step_narrative as step_renderer
    import toda_group_proof_narrative_renderer as renderer
    import phase165_r12_r34_r2_semantic_narrative as semantic
    calls = []
    originals = {
        'adapter': adapter.render_completed_shared_narrative,
        'step': step_renderer.render_completed_from_proofsteps,
        'public': renderer.render_toda_group_proof_narrative_markdown,
        'semantic': semantic.semantic_completed_lines,
    }
    def adapter_probe(*args, **kwargs):
        calls.append('completed_adapter')
        return originals['adapter'](*args, **kwargs)
    def step_probe(*args, **kwargs):
        calls.append('proofstep_narrative')
        return originals['step'](*args, **kwargs)
    def public_probe(*args, **kwargs):
        calls.append('public_presentation_renderer')
        return originals['public'](*args, **kwargs)
    def semantic_probe(*args, **kwargs):
        calls.append('semantic_completed_lines')
        return originals['semantic'](*args, **kwargs)
    report = {'mode': 'READ_ONLY', 'production_files_modified': False, 'full_pytest_run': False, 'targets': {}}
    with patch.object(adapter,'render_completed_shared_narrative',adapter_probe), patch.object(step_renderer,'render_completed_from_proofsteps',step_probe), patch.object(renderer,'render_toda_group_proof_narrative_markdown',public_probe), patch.object(semantic,'semantic_completed_lines',semantic_probe):
        for n, k, name in ((2,1,'pi3_2'), (3,1,'pi4_3')):
            calls.clear()
            entry = {'calls': []}
            try:
                view = web_group_proof.build_standard_web_group_proof_view(n,k,2,'narrative')
                lines = []
                for item in view.rendered_lines:
                    if isinstance(item, str):
                        lines.append(item)
                    else:
                        lines.append(str(getattr(item,'prefix','')) + str(getattr(item,'statement_latex','') or '') + str(getattr(item,'suffix','')))
                body = '\n'.join(lines)
                (OUT / (name+'_before.txt')).write_text(body, encoding='utf-8')
                entry.update(key=view.key, mode=view.mode, chars=len(body), lines=len(lines), english_rule='infinite cyclic quotient structure' in body, first_isomorphism='第一同型定理' in body, homomorphism_theorem='準同型定理' in body, raw_eta='2η_{2}' in body)
            except Exception as exc:
                import traceback
                entry['error'] = traceback.format_exc()
            entry['calls'] = list(calls)
            report['targets'][name] = entry
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print('OUTPUT:',OUT)

if __name__ == '__main__':
    main()
