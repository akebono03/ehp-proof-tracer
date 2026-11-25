"""Audit the actual connected public route; compare the same model to R54."""
from __future__ import annotations

import ast
import difflib
import json
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r55_equality_display_isolated import audit as isolated
from phase176_r3r55r1_public_equality_projection.apply import (
    TARGET, artifact_folder, baseline_source, check_dependencies, function_node,
    updated_source,
)


def observe():
    import phase168_r3_5_model_renderer as renderer
    import phase176_r3r55_equality_display_isolated.projection as projection

    raw = TARGET.read_bytes()
    if updated_source(raw) != raw:
        raise RuntimeError('PUBLIC_CONNECTION_NOT_APPLIED')
    base, _ = baseline_source(raw)
    node = function_node(base)
    namespace = dict(vars(renderer))
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<pinned pre-R55 renderer>', 'exec'), namespace)
    before_renderer = namespace[node.name]
    current_renderer = renderer.render_model_backed_narrative_markdown
    original_projection = projection.project_redundant_equalities
    captures, plans = [], []

    def capture(result, model):
        snapshot = baseline.snapshot(model)
        new = current_renderer(result, model)
        old = before_renderer(result, model)
        if baseline.snapshot(model) != snapshot:
            raise RuntimeError('MODEL_CHANGED_DURING_COMPARISON')
        captures.append((result, model, old, new))
        return new

    def observe_projection(model, order, hidden, protected):
        plan = original_projection(model, order, hidden, protected)
        plans.append((model, dict(plan)))
        return plan

    # Call through real Web adapter, R53 trust replay and public Renderer.
    # Neither a fabricated proof nor shadow text is returned to the Web route.
    with patch.object(renderer, 'render_model_backed_narrative_markdown', capture), \
         patch.object(projection, 'project_redundant_equalities', observe_projection):
        report, actual, partial = baseline.observe()
    complete = [c for c in captures if c[0].status is ProofSearchStatus.COMPLETE]
    incomplete = [c for c in captures if c[0].status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1 or len(plans) != 1:
        raise RuntimeError('UNEXPECTED_RENDER_OR_PROJECTION_CALL_COUNT')
    result, model, before, after = complete[0]
    if plans[0][0] is not model or after != actual or incomplete[0][3] != partial:
        raise RuntimeError('PUBLIC_MODEL_RENDER_IDENTITY_MISMATCH')
    plan = plans[0][1]
    folder = artifact_folder()
    (folder / 'before.md').write_text(before, encoding='utf-8')
    (folder / 'actual_narrative.md').write_text(after, encoding='utf-8')
    (folder / 'partial_prefix_narrative.md').write_text(partial, encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(
        before.splitlines(True), after.splitlines(True), fromfile='before', tofile='public')), encoding='utf-8')
    (folder / 'plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    if set(plan) != isolated.EXPECTED:
        raise RuntimeError('PUBLIC_PROJECTION_PLAN_CHANGED:' + repr(plan))
    old, new = isolated.compare_display(before, after, report['steps'])
    if sum(len(x['lines']) for x in old['identities']) != 9:
        raise RuntimeError('UNEXPECTED_PRECONNECTION_BASELINE')
    if incomplete[0][2] != incomplete[0][3]:
        raise RuntimeError('PARTIAL_RENDER_CHANGED')
    if (report['proof_steps'], report['inference_steps'], report['given_steps'], len(model.citations)) != (62, 51, 11, 10):
        raise RuntimeError('PROOF_OR_CITATION_COUNTS_CHANGED')
    if result.open_goals or report['web_key'] != 'generic-complete-proof':
        raise RuntimeError('PUBLIC_ROOT_NOT_COMPLETE')
    by_index = {row['index']: row for row in report['steps']}
    body = after.split('\n証明\n', 1)[1]
    for i in (0, 10, 11, 12, 13, 17, 20, 21, 25, 56, 58, 61):
        if not by_index[i]['latex'] or by_index[i]['latex'] not in body:
            raise RuntimeError('RETAINED_WITNESS_MISSING:' + str(i))
    for i in (29, 36, 43):
        if by_index[i]['typed_sentence'].split('$')[1] not in body:
            raise RuntimeError('CITED_SUSPENSION_WITNESS_MISSING:' + str(i))
    return {'gate': 'PASS_R3R55R1_PUBLIC_EQUALITY_PROJECTION_CONNECTED',
            'status': result.status.value, 'web_key': report['web_key'],
            'proof_steps': report['proof_steps'], 'inference_steps': report['inference_steps'],
            'given_steps': report['given_steps'], 'open_goals': [], 'citation_count': len(model.citations),
            'suppressed_indices': sorted(plan), 'reasons': plan,
            'identities_before': 9, 'identities_after': len(new['identities']),
            'repeated_equations_after': new['repeated_equations'],
            'reversed_equations_after': new['reversed_equations'],
            'reference_section_unchanged': True, 'explicit_reference_use_set_unchanged': True,
            'model_unchanged': True, 'partial_render_unchanged': True,
            'public_connection': 'APPLIED', 'kernel_renderer_verified': report['kernel_renderer_verified'],
            'new_math_rules': 0, 'new_given_registrations': 0, 'full_pytest': 'NOT_RUN'}


def main():
    check_dependencies()
    git = baseline.prior.git
    before = (git('diff', '--binary', 'HEAD'), git('status', '--porcelain'))
    report = observe()
    if before != (git('diff', '--binary', 'HEAD'), git('status', '--porcelain')):
        raise RuntimeError('AUDIT_CHANGED_REPOSITORY')
    report['repository_unchanged_during_audit'] = True
    folder = artifact_folder()
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'gate':
            print('PHASE176_R3R55R1_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(folder / 'report.json'))
    print('NARRATIVE=' + str(folder / 'actual_narrative.md'))
    print('PHASE176_R3R55R1_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
