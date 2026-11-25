"""Compare public render with the same model before the R56 display hook."""
from __future__ import annotations

from dataclasses import replace
import difflib
import json
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r56r3_public_cited_source_display.apply import artifact_folder, planned_changes


def observe():
    import phase168_r3_5_model_renderer as renderer
    import phase176_r3r56_cited_source_display_isolated.projection as projection
    from phase175_r3r9_lemma57_explicit_public.source import PARTICULAR_CLAUSE

    original = renderer.render_model_backed_narrative_markdown
    project = projection.project_cited_sources
    captures = []
    calls = []

    def observed_project(markdown, model):
        output = project(markdown, model)
        calls.append((model, output))
        return output

    def observed_render(result, model):
        snapshot = baseline.snapshot(model)
        actual = original(result, model)
        with patch.object(projection, 'project_cited_sources', lambda markdown, model: markdown):
            before = original(result, model)
        if baseline.snapshot(model) != snapshot:
            raise RuntimeError('MODEL_CHANGED_DURING_COMPARISON')
        captures.append((result, model, before, actual))
        return actual

    with patch.object(projection, 'project_cited_sources', observed_project), \
         patch.object(renderer, 'render_model_backed_narrative_markdown', observed_render):
        report, actual, partial = baseline.observe()
    complete = [row for row in captures if row[0].status is ProofSearchStatus.COMPLETE]
    incomplete = [row for row in captures if row[0].status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1:
        raise RuntimeError('UNEXPECTED_RENDER_COUNT')
    result, model, before, public = complete[0]
    if (public != actual or len(calls) != 1 or calls[0][0] is not model
            or calls[0][1].rstrip() + '\n' != actual):
        raise RuntimeError('PUBLIC_HOOK_NOT_OBSERVED')
    if incomplete[0][2] != partial or incomplete[0][3] != partial:
        raise RuntimeError('PARTIAL_DISPLAY_CHANGED')
    snapshot = baseline.snapshot(model)
    if before == actual or project(before, model) != actual or project(actual, model) != actual:
        raise RuntimeError('PUBLIC_DIFFERS_FROM_ISOLATED_PROJECTION')
    if project(partial, incomplete[0][1]) != partial:
        raise RuntimeError('PARTIAL_PROJECTION_CHANGED')
    missing = replace(model, citations=tuple(replace(c, assertion_ids=()) for c in model.citations))
    if project(before, missing) != before:
        raise RuntimeError('UNBOUND_CITATION_CHANGED_DISPLAY')
    old = baseline.inspect_markdown(before, report['steps'])
    new = baseline.inspect_markdown(actual, report['steps'])
    refs = {int(k): v for k, v in new['references'].items()}
    previous = {int(k): v for k, v in old['references'].items()}
    zero = '$' + PARTICULAR_CLAUSE.replace(r'\circ', '') + '$.'
    quad = r'$n\ge 5$ に対し, $4\nu_n=\eta_n^3$.'
    if set(refs) != set(previous):
        raise RuntimeError('REFERENCE_NUMBERS_CHANGED')
    for number, ref in refs.items():
        expected = list(previous[number]['body'])
        if number == 2 and zero not in expected:
            expected.append(zero)
        if number == 10 and quad not in expected:
            expected.append(quad)
        if ref['body'] != expected or ref['header'] != previous[number]['header']:
            raise RuntimeError('UNEXPECTED_REFERENCE_CHANGE:' + str(number))
    if (zero not in refs[2]['body'] or not any(r'\Delta' in x for x in refs[2]['body'])
            or quad not in refs[10]['body'] or not refs[6]['uses'] or not refs[9]['uses']):
        raise RuntimeError('SOURCE_CLAUSE_OR_APPLICATION_MISSING')
    expected_body = before.split('\n証明\n', 1)[1]
    expected_body = expected_body.replace('[R10]を用いて, ', '[R9], [R10]を用いて, ')
    formula = '$' + next(row['latex'] for row in report['steps'] if row['index'] == 20) + '$.'
    expected_body = expected_body.replace('\n' + formula, '\n[R6]より, ' + formula)
    if expected_body != actual.split('\n証明\n', 1)[1]:
        raise RuntimeError('UNEXPECTED_BODY_CHANGE')
    if (new['identities'] or new['repeated_equations'] or new['reversed_equations']
            or new['references_without_explicit_body_use'] or new['empty_reference_bodies'] != [1, 4, 5]
            or (report['proof_steps'], report['inference_steps'], report['given_steps']) != (62, 51, 11)
            or result.open_goals or len(model.citations) != 10 or baseline.snapshot(model) != snapshot):
        raise RuntimeError('PUBLIC_INVARIANT_CHANGED')
    folder = artifact_folder()
    for name, text in [('before.md', before), ('actual_narrative.md', actual), ('partial.md', partial)]:
        (folder / name).write_text(text, encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(
        before.splitlines(True), actual.splitlines(True), fromfile='before', tofile='public')), encoding='utf-8')
    return {'gate': 'PASS_R3R56R3_PUBLIC_CITED_SOURCE_DISPLAY_CONNECTED',
            'status': result.status.value, 'web_key': report['web_key'], 'proof_steps': 62,
            'inference_steps': 51, 'given_steps': 11, 'citation_count': 10, 'open_goals': [],
            'references_without_explicit_body_use': new['references_without_explicit_body_use'],
            'empty_reference_bodies': new['empty_reference_bodies'], 'model_unchanged': True,
            'partial_render_unchanged': True, 'public_connection': 'APPLIED',
            'namespace_guard_reused': True, 'new_math_rules': 0, 'new_given_registrations': 0,
            'full_pytest': 'NOT_RUN'}


def main():
    from phase176_r3r46r1_prior_group_availability.pytest_runner import canonical_hopf_modules
    canonical_hopf_modules()
    if any(raw != changed for raw, changed in planned_changes().values()):
        raise RuntimeError('R56R3_NOT_APPLIED')
    git = baseline.prior.git
    before = (git('diff', '--binary', 'HEAD'), git('status', '--porcelain'))
    report = observe()
    if before != (git('diff', '--binary', 'HEAD'), git('status', '--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED_DURING_AUDIT')
    report['repository_unchanged_during_audit'] = True
    path = artifact_folder() / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'gate':
            print('PHASE176_R3R56R3_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('REPORT=' + str(path))
    print('PHASE176_R3R56R3_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
