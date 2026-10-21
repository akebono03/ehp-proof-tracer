"""Read-only dynamic audit of the actual π4³ Web proof path."""
from __future__ import annotations
import json
import traceback
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent


def main():
    import web_group_proof
    import phase165_r56_presentation_adapter as adapter
    import toda_group_proof_narrative_renderer as renderer
    import phase165_r57_r10_step_narrative as step_renderer
    import toda_group_proof_narrative_references as references
    from proof import ProofRule

    events = []
    original_adapter = adapter.render_completed_shared_narrative
    original_step = step_renderer.render_completed_from_proofsteps
    original_render = renderer.render_toda_group_proof_narrative_markdown
    original_refs = references.render_toda_group_proof_narrative_reference_entries_markdown

    def adapter_probe(result):
        event = {"stage": "completed_adapter", "status": str(getattr(result.status, 'value', result.status)), "proven_steps": len(result.proven_steps)}
        roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
        if len(roots) == 1:
            from phase165_r57_r10_step_narrative import ordered_proof_ancestry, has_transport_proof_ancestry
            ancestry = ordered_proof_ancestry(roots[0])
            event['ancestry_count'] = len(ancestry)
            event['transport_ancestry'] = has_transport_proof_ancestry(roots[0])
            event['given'] = [{"rule": getattr(s.inference_rule, 'name', None), "locator": getattr(getattr(s.inference_rule, 'literature_reference', None), 'locator', None), "conclusion_type": type(s.conclusion).__name__, "conclusion": repr(s.conclusion)[:600]} for s in ancestry if s.rule is ProofRule.GIVEN]
            event['rule_names'] = [getattr(s.inference_rule, 'name', None) for s in ancestry if s.rule is ProofRule.INFERENCE]
        events.append(event)
        return original_adapter(result)

    def step_probe(result, root):
        events.append({"stage": "alternate_proofstep_renderer"})
        return original_step(result, root)

    def renderer_probe(presentation):
        events.append({"stage": "public_presentation_renderer"})
        return original_render(presentation)

    def refs_probe(entries, statement_lines_by_reference_number=None):
        events.append({"stage": "reference_renderer", "entries": [{"number": e.number, "locator": getattr(e.reference, 'locator', None), "steps": [{"type": type(s.conclusion).__name__, "inference": getattr(s.inference_rule, 'name', None)} for s in e.proof_steps]} for e in entries], "statement_lines": statement_lines_by_reference_number})
        return original_refs(entries, statement_lines_by_reference_number)

    report = {"phase": "167 R1", "mode": "READ_ONLY_DYNAMIC", "target": "pi_4^3", "events": events, "full_pytest_run": False, "production_changes": False}
    try:
        with patch.object(adapter, 'render_completed_shared_narrative', adapter_probe), patch.object(step_renderer, 'render_completed_from_proofsteps', step_probe), patch.object(renderer, 'render_toda_group_proof_narrative_markdown', renderer_probe), patch.object(references, 'render_toda_group_proof_narrative_reference_entries_markdown', refs_probe):
            # Web entry (not a simulated or synthesized ProofStep).
            view = web_group_proof.build_standard_web_group_proof_view(3, 1, 2, 'narrative')
        report['web_view'] = {'key': view.key, 'mode': view.mode, 'line_count': len(view.rendered_lines), 'partial_result': getattr(view, 'partial_result', None)}
        lines = []
        for line in view.rendered_lines:
            if isinstance(line, str):
                lines.append(line)
            else:
                lines.append(str(getattr(line, 'prefix', '')) + ' ' + str(getattr(line, 'statement_latex', '') or '') + ' ' + str(getattr(line, 'suffix', '')))
        (OUT / 'web_lines.txt').write_text('\n'.join(lines), encoding='utf-8')
        section = '\n'.join(lines).split('使用する結果', 1)[-1].split('証明', 1)[0]
        report['observed'] = {'ref_5_1': '(5.1)' in section, 'ref_5_1_formula': ('pi_' in section and 'iota' in section) or ('pi_' in section and 'mathbb' in section), 'english_rule': 'infinite cyclic quotient structure' in '\n'.join(lines), 'reference_section': section[:6000]}
    except Exception:
        report['error'] = traceback.format_exc()
    (OUT / 'dynamic_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    print('REPORT:', OUT / 'dynamic_report.json')

if __name__ == '__main__':
    main()
