"""R57-R9: read-only comparison of public and fallback narrative paths.

No production module is edited. The live stable-renderer hook is disabled only
inside one Python process, and restored before the audit returns.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re


@contextmanager
def replace_attribute(obj, name, replacement):
    """Temporarily replace one attribute and restore it on every exit."""
    sentinel = object()
    original = getattr(obj, name, sentinel)
    if original is sentinel:
        raise AttributeError(name)
    setattr(obj, name, replacement)
    try:
        yield original
    finally:
        setattr(obj, name, original)


def _step_record(step):
    rule = getattr(step, 'inference_rule', None)
    return {
        'rule': str(getattr(getattr(step, 'rule', None), 'value', getattr(step, 'rule', None))),
        'inference_rule': getattr(rule, 'name', None),
        'conclusion_type': type(getattr(step, 'conclusion', None)).__name__,
        'conclusion_repr': repr(getattr(step, 'conclusion', None)),
        'premise_count': len(getattr(step, 'premises', ())),
        'premise_types': [type(getattr(p, 'conclusion', None)).__name__ for p in getattr(step, 'premises', ())],
    }


def _math_signatures(text):
    """Conservative diagnostic only; not a theorem-proving equivalence test."""
    return {
        'has_reference': '使用する結果' in text,
        'has_proof': '証明' in text,
        'has_toda45': '(4.5)' in text,
        'has_prop51': 'Proposition 5.1' in text,
        'has_suspension': bool(re.search(r'\\?E|懸垂|suspension', text)),
        'has_qed': '□' in text,
        'has_unresolved': '未解決 Goal' in text or '証明未完成' in text,
        'length': len(text),
    }


def _run():
    import toda_group_proof_narrative_renderer as narrative
    import phase165_r52_r3_web_adapter as adapter
    import web_group_proof as web

    captured = []
    def spy(result):
        captured.append(result)
        return original_render(result)

    hook = '_phase160_r7_render_stable_finite_cyclic_transport_narrative'
    original_hook = getattr(narrative, hook)
    hit = []
    def observing_hook(presentation):
        answer = original_hook(presentation)
        hit.append({'called': True, 'intercepted': answer is not None})
        return answer

    with replace_attribute(adapter, 'render_partial_proof_markdown', spy) as original_render:
        with replace_attribute(narrative, hook, observing_hook):
            original_view = web.build_standard_web_group_proof_view(4, 1, max_depth=2, mode='narrative')
    if len(captured) != 1:
        raise RuntimeError(f'expected one observed typed search result, got {len(captured)}')
    result = captured[0]
    # The exact same search result is used for both render passes, so search
    # nondeterminism cannot explain their differences.
    baseline = original_render(result)
    with replace_attribute(narrative, hook, lambda presentation: None):
        common_only = original_render(result)

    # A branch which returns a narrative is an active bypass, even when both
    # texts happen to contain the same final formula.
    intercepted = any(item['intercepted'] for item in hit)
    records = [_step_record(step) for step in result.proven_steps]
    all_names = [s['inference_rule'] or '' for s in records]
    transport_evidence = [s for s in records if 'transport' in (s['inference_rule'] or '').lower() or '4.5' in (s['inference_rule'] or '')]
    report = {
        'phase': '165 R57-R9',
        'mode': 'READ_ONLY_COMPARE_LIVE_AND_NO_STABLE_RENDER_BRANCH',
        'target': 'pi_5^4',
        'proof_status': str(getattr(result.status, 'value', result.status)),
        'structure_status': str(getattr(result.structure_status, 'value', result.structure_status)),
        'conclusion': repr(result.conclusion),
        'proven_step_count': len(result.proven_steps),
        'open_goal_count': len(result.open_goals),
        'steps': records,
        'transport_proofstep_count': len(transport_evidence),
        'stable_renderer_branch_called': bool(hit),
        'stable_renderer_branch_intercepted': intercepted,
        'baseline_signatures': _math_signatures(baseline),
        'without_branch_signatures': _math_signatures(common_only),
        'narrative_identical': baseline == common_only,
        'baseline_narrative': baseline,
        'without_branch_narrative': common_only,
        'production_modified': False,
        'live_stable_renderer_deletion_allowed': False,
        'full_pytest_run': False,
    }
    report['finding'] = (
        'ACTIVE_LEGACY_NARRATIVE_BYPASS' if intercepted else
        'STABLE_BRANCH_NOT_USED_FOR_THIS_COMPLETED_PROOF'
    )
    report['interpretation'] = (
        'Display equality does not certify the Toda (4.5) transport ancestry. '
        'Inspect steps and compare the reference/equation rendering before deletion.'
    )
    return report


def main():
    folder = Path(__file__).resolve().parent
    root = folder.parent
    report = _run()
    output = root / 'phase165_r57_r9_renderer_comparison.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('steps', 'baseline_narrative', 'without_branch_narrative')}, ensure_ascii=False, indent=2))
    print('Trace saved:', output)
    print('Full pytest NOT run')


if __name__ == '__main__':
    main()
