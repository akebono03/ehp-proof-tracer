"""Read-only public baseline and isolated source projection comparison."""
from __future__ import annotations

import argparse
from dataclasses import replace
import difflib
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from phase165_r52_partial_proof import ProofSearchStatus
from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r54_narrative_audit import audit as baseline
from phase176_r3r55r1_public_equality_projection import apply as connected
from phase176_r3r56_cited_source_display_isolated.projection import project_cited_sources

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
PINS = {
    'phase175_r3r11_cited_hopf_narrative/projection.py': 'a9ecbffc4b89c2da84bc523fd9388b44d476fb26',
    'phase175_r3r9_lemma57_explicit_public/source.py': '0dbd07c4dbca7e3b3fcbbabf94126e111e21b1ab',
    'phase176_r3r27r1_toda55_quadruple_isolated/source.py': '3e174ff8ffb656f069e1318591785bb7697c7736',
    'phase169_r10d2_general_family_definition/family_citation.py': 'b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8',
    'phase171_r2h_prop22_cited_hopf/source.py': '856eafdc6640a35ba1f891c6eeb7cfbf23c2a8b5',
    'phase176_r3r36_composite_right_hopf_isolated/source.py': 'c2dc7f2a2be1a68d8eccac57f12657ca149254d6',
}


def preflight():
    connected.check_dependencies()
    raw = connected.TARGET.read_bytes()
    if connected.updated_source(raw) != raw:
        raise RuntimeError('R55R1_NOT_APPLIED')
    for path, pin in PINS.items():
        text, _ = normalize((ROOT / path).read_bytes())
        if not pinned(text, pin):
            raise RuntimeError('UNREVIEWED_SOURCE_DISPLAY_DEPENDENCY:' + path)


def observe():
    import phase168_r3_5_model_renderer as renderer
    original = renderer.render_model_backed_narrative_markdown
    captured = []

    def capture(result, model):
        markdown = original(result, model)
        captured.append((result, model, markdown))
        return markdown

    with patch.object(renderer, 'render_model_backed_narrative_markdown', capture):
        report, actual, partial = baseline.observe()
    complete = [x for x in captured if x[0].status is ProofSearchStatus.COMPLETE]
    incomplete = [x for x in captured if x[0].status is not ProofSearchStatus.COMPLETE]
    if len(complete) != 1 or len(incomplete) != 1:
        raise RuntimeError('UNEXPECTED_RENDER_COUNT')
    result, model, before = complete[0]
    if before != actual or incomplete[0][2] != partial:
        raise RuntimeError('PUBLIC_RENDER_MISMATCH')
    snapshot = baseline.snapshot(model)
    after = project_cited_sources(before, model)
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    for name, text in [('before.md', before), ('shadow.md', after), ('partial.md', partial)]:
        (folder / name).write_text(text, encoding='utf-8')
    (folder / 'narrative.diff').write_text(''.join(difflib.unified_diff(
        before.splitlines(True), after.splitlines(True), fromfile='before', tofile='shadow')), encoding='utf-8')
    old = baseline.inspect_markdown(before, report['steps'])
    new = baseline.inspect_markdown(after, report['steps'])
    # Target indices are audit expectations only, never projection inputs.
    refs = new['references']
    by_number = {int(k): v for k, v in refs.items()}
    from phase175_r3r9_lemma57_explicit_public.source import PARTICULAR_CLAUSE
    expected_zero = '$' + PARTICULAR_CLAUSE.replace(r'\circ', '') + '$.'
    if expected_zero not in by_number[2]['body'] or not any(r'\Delta' in x for x in by_number[2]['body']):
        raise RuntimeError('MERGED_LEMMA_CLAUSES_NOT_VISIBLE')
    if r'$n\ge 5$ に対し, $4\nu_n=\eta_n^3$.' not in by_number[10]['body']:
        raise RuntimeError('QUADRUPLE_CLAUSE_NOT_VISIBLE')
    if not by_number[6]['uses'] or not by_number[9]['uses']:
        raise RuntimeError('SOURCE_APPLICATION_TAG_MISSING')
    if set(old['references']) != set(new['references']):
        raise RuntimeError('REFERENCE_NUMBERS_CHANGED')
    # Only body citation prefixes may change; compare math and every other word.
    old_body = before.split('\n証明\n', 1)[1]
    new_body = after.split('\n証明\n', 1)[1]
    old_body = old_body.replace('[R10]を用いて, ', '[R9], [R10]を用いて, ')
    row20 = next(row for row in report['steps'] if row['index'] == 20)
    sentence20 = '$' + row20['latex'] + '$.'
    old_body = old_body.replace('\n' + sentence20, '\n[R6]より, ' + sentence20)
    if old_body != new_body:
        raise RuntimeError('UNEXPECTED_BODY_CHANGE')
    if (new['identities'] or new['repeated_equations'] or new['reversed_equations']
            or (report['proof_steps'], report['inference_steps'], report['given_steps']) != (62, 51, 11)
            or result.open_goals or len(model.citations) != 10 or baseline.snapshot(model) != snapshot):
        raise RuntimeError('R55R1_INVARIANT_CHANGED')
    if project_cited_sources(partial, incomplete[0][1]) != partial:
        raise RuntimeError('PARTIAL_CHANGED')
    if project_cited_sources(after, model) != after:
        raise RuntimeError('PROJECTION_NOT_IDEMPOTENT')
    missing = replace(model, citations=tuple(replace(c, assertion_ids=()) for c in model.citations))
    if project_cited_sources(before, missing) != before:
        raise RuntimeError('UNBOUND_CITATION_CHANGED_DISPLAY')
    out = {'gate': 'PASS_R3R56_ISOLATED_CITED_SOURCE_DISPLAY', 'status': result.status.value,
           'proof_steps': 62, 'inference_steps': 51, 'given_steps': 11, 'citation_count': 10,
           'open_goals': [], 'references_without_explicit_body_use': new['references_without_explicit_body_use'],
           'empty_reference_bodies': new['empty_reference_bodies'], 'model_unchanged': True,
           'partial_render_unchanged': True, 'public_connection': 'NOT_APPLIED',
           'new_math_rules': 0, 'new_given_registrations': 0, 'full_pytest': 'NOT_RUN'}
    return out, folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    preflight()
    if args.dry_run:
        print('PHASE176_R3R56_GATE=PASS_R3R56_DRYRUN')
        return 0
    git = baseline.prior.git
    before = (git('diff', '--binary', 'HEAD'), git('status', '--porcelain'))
    report, folder = observe()
    if before != (git('diff', '--binary', 'HEAD'), git('status', '--porcelain')):
        raise RuntimeError('AUDIT_CHANGED_REPOSITORY')
    report['repository_unchanged'] = True
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key != 'gate':
            print('PHASE176_R3R56_' + key.upper() + '=' + json.dumps(value, ensure_ascii=False))
    print('ARTIFACTS=' + str(folder))
    print('PHASE176_R3R56_GATE=' + report['gate'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
