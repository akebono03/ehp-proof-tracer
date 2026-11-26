"""Read-only final audit for the completed n=3, k=6 proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
BASE = 'd796ba7a9a8a32d458163f261cd8e19e60f5b949'
TARGET = 'phase168_r3_5_model_renderer.py'
PREVIOUS = 'phase178_r12r2_zero_composition_elision/'
PACKAGE_HASHES = {'phase178_r12r2_zero_composition_elision/projection.py': 'b90d179156a4464ac71c5f9a1a919ae00500c350a592fd26bf2990bcb0006d88', 'phase178_r12r2_zero_composition_elision/__init__.py': 'c1abc48a2ca1ad501347514c4b2324e58f57513c4acd4a87ec53858f1dff2848', 'phase178_r12r2_zero_composition_elision/installer.py': 'c5f9ab7e0328fabd4f9d26e7a9a6a75a245d656134f7a5b914588505b11ca303', 'phase178_r12r2_zero_composition_elision/run.ps1': 'c0fe587ef9ed556a21fcb54f7f623885df467c5d491bac37e980677b20cf5b75', 'phase178_r12r2_zero_composition_elision/audit.py': '651b9dfa3be210b33a36d7995059bf43a1751ca71503412dcfc58a947fb828ff', 'phase178_r12r2_zero_composition_elision/README.md': '0f2d7cb365961975c5f8c71a2d1bb9399ff6544ea29708f79bc4b8231813d2de', 'phase178_r12r2_zero_composition_elision/tests/test_projection.py': '329376dc55822e75680ed4abaa5b39e7b7d18d3766a4a306dbcb0c41443414b9'}
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    PREVIOUS + 'tests/test_projection.py',
    'phase178_r12r1_suspension_composition_display/tests/test_projection.py',
    'phase178_r12_suspension_composition_audit/tests/test_audit.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_sentence_layout_audit.py',
    'phase178_r10_equal_cardinality_reason_display/tests/test_projection.py',
    'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py',
    'phase175_r3r9_lemma57_explicit_public/tests/test_rule.py',
    'phase175_r4r12r13r2_delta_injective_e_surjective/tests/test_rule.py',
    'phase178_r4_delta_surjective_zero_suspension_isolated/tests/test_rule.py',
    'phase178_r6_finite_group_cardinality_isolated/tests/test_rule.py',
    'phase178_r8_finite_group_surjective_injective_isolated/tests/test_rule.py',
    'phase171_r20r2_first_successful_search/tests/test_first_successful_search.py',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def normalized(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def digest(raw):
    return hashlib.sha256(normalized(raw).encode('utf-8')).hexdigest()


def emit(key, value):
    print('PHASE178_R13_' + key + '=' + str(value), flush=True)


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    head = gt('rev-parse', 'HEAD')
    require(gt('branch', '--show-current') == 'develop' and head == gt('rev-parse', 'origin/develop'), 'HEAD_OR_BRANCH_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE, 'REVIEWED_ANCESTRY_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    committed = set(gt('diff', '--name-only', BASE, head).splitlines())
    allowed = {TARGET, *PACKAGE_HASHES}
    require(committed <= allowed, 'UNREVIEWED_COMMITTED_CHANGES:' + repr(sorted(committed - allowed)))
    dirty = set(gt('diff', '--name-only', 'HEAD').splitlines())
    require(dirty <= {TARGET}, 'UNRELATED_TRACKED_CHANGES:' + repr(sorted(dirty - {TARGET})))
    for path, expected in PACKAGE_HASHES.items():
        require(digest((ROOT / path).read_bytes()) == expected, 'R12R2_PACKAGE_CHANGED:' + path)
    require(gt('rev-parse', BASE + ':' + TARGET) == 'cb9026fb04c0f85983d14c757eec1de706e02d1b', 'BASE_RENDERER_CHANGED')
    from phase178_r12r2_zero_composition_elision.installer import proposed_source
    expected = proposed_source(normalized(git('show', BASE + ':' + TARGET)))
    require(normalized((ROOT / TARGET).read_bytes()) == expected, 'R12R2_NOT_INSTALLED_EXACTLY')
    require(all((ROOT / path).is_file() for path in TESTS), 'FOCUSED_TEST_MISSING')
    gt('diff', '--check')
    return {'head': head, 'renderer_sha256': digest((ROOT / TARGET).read_bytes()),
            'tracked_status': gt('status', '--porcelain', '--untracked-files=no')}


# The exact group structure is audited on typed objects. The following lines
# are the already reviewed R12R2 body anchors, independent of spacing in DB prose.
FIRST = r"[R4]より, $E(\eta_{2}\nu'\eta_{6})=0$."
SECOND = r"[R4]より, $E(\eta_{2}\nu'\eta_{6}^{2})=0$."
BASE_LINE = r"[R4]より, $E(\eta_{2}\nu')=0$."


def check_narrative(markdown):
    lines = markdown.splitlines()
    require(lines.count('証明') == 1, 'BODY_BOUNDARY_AMBIGUOUS')
    boundary = lines.index('証明')
    refs, body = lines[:boundary], lines[boundary + 1:]
    headers = [int(m[1]) for line in refs if (m := re.match(r'^\*\*\[R(\d+)\] ', line))]
    require(headers == [1, 2, 3, 4, 5], 'REFERENCE_ORDER_CHANGED')
    header = '**[R4] Lemma 5.7.**'
    require(refs.count(header) == 1, 'LEMMA_REFERENCE_MISSING')
    start = refs.index(header)
    end = next((i for i in range(start + 1, len(refs)) if refs[i].startswith('**[R')), len(refs))
    require(any(re.sub(r'[\s{}]', '', s) == r"$E(\eta_2\nu')=0$." for s in refs[start+1:end]), 'LEMMA_CLAUSE_MISSING')
    require(body.count(FIRST) == body.count(SECOND) == 1 and BASE_LINE not in body, 'ZERO_IMAGE_DISPLAY_CHANGED')
    require(body.index(FIRST) < body.index(SECOND), 'ZERO_IMAGE_DISPLAY_ORDER_CHANGED')
    require([s for s in body if s.strip()][-1] == '□', 'PROOF_END_MISSING')
    return {'reference_headers': headers, 'zero_image_body_count': 2, 'base_in_reference_only': True}


def inspect_actual(folder):
    import phase168_r3_5_model_renderer as renderer
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase175_r3r9_lemma57_explicit_public.source import verify_explicit_lemma57_source
    from phase178_r12r2_zero_composition_elision.audit import inspect_actual as previous_audit
    from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
    from proof import ProofRule
    source = verify_explicit_lemma57_source(ROOT)
    real = renderer.render_model_backed_narrative_markdown
    captured = []

    def observed(result, model):
        markdown = real(result, model)
        captured.append((result, model, markdown))
        return markdown

    with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
        summary = previous_audit(folder)
    # The preceding audit also renders the same model twice with display hooks
    # disabled. Its first capture is the actual public Web rendering.
    require(len(captured) == 3, 'PUBLIC_RENDER_CAPTURE_AMBIGUOUS')
    result, model, markdown = captured[0]
    require(all(r is result and m is model for r, m, _ in captured), 'BASELINE_MODEL_CHANGED')
    require(markdown == (folder / 'narrative.md').read_text(encoding='utf-8'), 'PUBLIC_NARRATIVE_MISMATCH')
    target = TodaPrimaryGroup(9, 3)
    require(result.target == target and type(result.conclusion) is TodaPrimaryGroupZeroStatement and result.conclusion.group == target, 'WRONG_TYPED_ROOT')
    require(model.steps[model.root_index].conclusion == result.conclusion and model.steps[model.root_index].rule is ProofRule.INFERENCE, 'ROOT_NOT_INFERRED')
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    lookup = {id(s): i for i, s in enumerate(model.steps)}
    rows = []
    for i in sorted(scope):
        step = model.steps[i]
        parents = [lookup[id(p)] for p in step.premises]
        require(all(p in scope and p < i for p in parents), 'NON_TOPOLOGICAL_PREMISES')
        require(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE), 'UNSUPPORTED_STEP_KIND')
        if step.rule is ProofRule.INFERENCE:
            require(replayed(step), 'INFERENCE_REPLAY_FAILED:' + str(i))
        else:
            require(not parents, 'GIVEN_HAS_PREMISES')
        rows.append({'index': i, 'rule': step.rule.name, 'inference': getattr(step.inference_rule, 'name', None),
                     'premises': parents, 'statement': repr(step.conclusion), 'citations': list(model.step_citation_numbers[i])})
    require(len(model.steps) == 20 and len(model.citations) == 5 and summary['target_given_count'] == 0, 'ROOT_INVARIANTS_CHANGED')
    display = check_narrative(markdown)
    (folder / 'root_ancestry.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    citations = [{'number': c.number, 'locator': c.reference.locator, 'step_indices': c.step_indices,
                  'assertion_ids': c.assertion_ids, 'reference_ids': c.reference_ids} for c in model.citations]
    (folder / 'citations.json').write_text(json.dumps(citations, ensure_ascii=False, indent=2), encoding='utf-8')
    emit('ROOT_STATUS', summary['status'])
    emit('ROOT_STEPS', summary['proven_step_count'])
    emit('ROOT_OPEN_GOALS', summary['open_goal_count'])
    emit('REFERENCES', len(citations))
    emit('TRUST_STATUS', summary['trust_status'])
    emit('TARGET_GIVEN_COUNT', summary['target_given_count'])
    emit('ROOT_ANCESTORS', len(scope))
    emit('FINAL_NARRATIVE', 'VERIFIED')
    emit('LEMMA57_SOURCE', 'VERIFIED_ADOPTED_TRANSCRIPTION')
    return dict(summary, display=display, root_ancestry_count=len(scope), citations=citations, lemma57_source=source)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R13', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN', 'production_changes': 0}
    try:
        before = preflight()
        report['preflight'] = before
        emit('HEAD', before['head'])
        if args.dry_run:
            report['gate'] = 'PASS_R13_READ_ONLY_DRYRUN'
        else:
            report['audit'] = inspect_actual(folder)
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            require(preflight() == before, 'WORKTREE_CHANGED_DURING_AUDIT')
            report['gate'] = 'PASS_R13_N3_FINAL_VERIFIED_PROOF_AUDIT'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
