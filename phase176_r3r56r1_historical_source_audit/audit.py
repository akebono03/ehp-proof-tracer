"""Compare historical and current renderers on the SAME verified proof tree."""
from __future__ import annotations

import argparse
import ast
from dataclasses import replace
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
from unittest.mock import patch

from phase176_r3r46r1_prior_group_availability.apply import normalize, pinned
from phase176_r3r55r1_public_equality_projection import apply as connection
from phase176_r3r56_cited_source_display_isolated import audit as r56
from phase176_r3r54_narrative_audit.audit import snapshot

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent.name
TEST = ROOT / 'phase175_r3r11_cited_hopf_narrative/tests/test_projection.py'
TEST_PIN = 'f533e0601dc41597ba57eddcd0d210e082ef66cc'
TEST_NAMES = ('test_references_and_zero_composition_are_explicit',
              'test_hopf_chain_is_source_bound_and_compact')


def namespace_pair(assertions, references, assertion_id, reference_id):
    """Accept only a common numbered namespace for BOTH registry identities."""
    def prefixes(values, expected):
        found = set()
        for value in values:
            match = re.fullmatch(r'(shared:[0-9]+:)' + re.escape(expected), value)
            if match is not None:
                found.add(match.group(1))
        return found
    common = prefixes(assertions, assertion_id) & prefixes(references, reference_id)
    return len(common) == 1


def preflight():
    r56.preflight()
    source, _ = normalize(TEST.read_bytes())
    if not pinned(source, TEST_PIN):
        raise RuntimeError('UNREVIEWED_HISTORICAL_TEST')


def load_tests():
    spec = importlib.util.spec_from_file_location('_r56r1_historical_tests', TEST)
    if spec is None or spec.loader is None:
        raise RuntimeError('HISTORICAL_TEST_IMPORT_FAILED')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shadow_lookup(original, model, scope, **kwargs):
    """Audit-only alternate lookup, retaining the original typed GIVEN guards."""
    found = original(model, scope, **kwargs)
    if found is not None:
        return found
    assertion = kwargs['assertion_id']
    reference = kwargs['reference_id']
    candidates = tuple(c for c in model.citations
                       if c.reference.locator == kwargs['locator']
                       and namespace_pair(c.assertion_ids, c.reference_ids, assertion, reference))
    if len(candidates) != 1:
        return None
    candidate = candidates[0]
    augmented = replace(candidate, assertion_ids=candidate.assertion_ids + (assertion,),
                        reference_ids=candidate.reference_ids + (reference,))
    view = replace(model, citations=tuple(augmented if c is candidate else c for c in model.citations))
    found = original(view, scope, **kwargs)
    if found is None or found[0] is not augmented:
        return None
    return candidate, found[1]


def run_original_assertions(module, pair, render):
    outcomes = {}
    with patch.object(module, 'render_model_backed_narrative_markdown', render):
        for name in TEST_NAMES:
            try:
                getattr(module, name)(pair)
            except AssertionError as exc:
                outcomes[name] = {'status': 'FAIL', 'detail': str(exc)}
            else:
                outcomes[name] = {'status': 'PASS'}
    return outcomes


def observe(folder):
    import phase168_r3_5_model_renderer as renderer
    import phase175_r3r11_cited_hopf_narrative.projection as old
    from phase175_r3r9_lemma57_explicit_public.source import (
        ASSERTION_ID, REFERENCE_ID, TodaLemma57ExplicitNuPrimeZero,
    )
    tests = load_tests()
    pair = tests.pi73_verified.__wrapped__()
    result, model = pair
    before = snapshot(model)
    source, _ = connection.baseline_source(connection.TARGET.read_bytes())
    node = connection.function_node(source)
    namespace = dict(vars(renderer))
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<pinned pre-R55 renderer>', 'exec'), namespace)
    prior = namespace[node.name]
    current = renderer.render_model_backed_narrative_markdown
    scope = old._completed_scope(model)
    if scope is None:
        raise RuntimeError('EXPECTED_COMPLETE_VERIFIED_MODEL')
    args = dict(statement_type=TodaLemma57ExplicitNuPrimeZero, assertion_id=ASSERTION_ID,
                reference_id=REFERENCE_ID, locator='Lemma 5.7')
    original = old._source_citation
    old_match = original(model, scope, **args)
    new_match = shadow_lookup(original, model, scope, **args)
    a = run_original_assertions(tests, pair, prior)
    b = run_original_assertions(tests, pair, current)
    prior_text = prior(result, model)
    current_text = current(result, model)
    with patch.object(old, '_source_citation', lambda m, s, **kw: shadow_lookup(original, m, s, **kw)):
        c = run_original_assertions(tests, pair, current)
        shadow_text = current(result, model)
    for name, value in [('pre_r55.md', prior_text), ('current.md', current_text), ('namespace_shadow.md', shadow_text)]:
        (folder / name).write_text(value, encoding='utf-8')
    citations = [{'number': x.number, 'locator': x.reference.locator,
                  'assertion_ids': x.assertion_ids, 'reference_ids': x.reference_ids,
                  'step_indices': x.step_indices} for x in model.citations]
    previous_failures = [k for k,v in a.items() if v['status'] == 'FAIL']
    current_failures = [k for k,v in b.items() if v['status'] == 'FAIL']
    shadow_failures = [k for k,v in c.items() if v['status'] == 'FAIL']
    report = {'status': result.status.value, 'open_goals': len(result.open_goals),
              'proof_steps': len(model.steps), 'citations': citations,
              'pre_r55_assertions': a, 'current_assertions': b, 'namespace_shadow_assertions': c,
              'pre_r55_failures': previous_failures, 'current_failures': current_failures,
              'shadow_failures': shadow_failures, 'legacy_source_match': old_match is not None,
              'namespace_source_match': new_match is not None,
              'namespace_source_index': None if new_match is None else new_match[1],
              'model_unchanged': before == snapshot(model),
              'preexisting_on_same_model': previous_failures == current_failures == list(TEST_NAMES),
              'namespace_only_restores_both': not shadow_failures and old_match is None and new_match is not None,
              'production_changes': 0, 'historical_test_changes': 0, 'full_pytest': 'NOT_RUN'}
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key, value in report.items():
        if key not in ('citations', 'pre_r55_assertions', 'current_assertions', 'namespace_shadow_assertions'):
            print('PHASE176_R3R56R1_'+key.upper()+'='+json.dumps(value, ensure_ascii=False))
    print('REPORT='+str(folder/'report.json'))
    if not report['model_unchanged'] or result.open_goals:
        raise RuntimeError('PROOF_MODEL_CHANGED_OR_INCOMPLETE')
    if not report['preexisting_on_same_model']:
        raise RuntimeError('HISTORICAL_FAILURE_NOT_ISOLATED: inspect report before continuing')
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    preflight()
    if args.dry_run:
        print('PHASE176_R3R56R1_GATE=PASS_R3R56R1_DRYRUN')
        return 0
    from phase176_r3r46r1_prior_group_availability.pytest_runner import canonical_hopf_modules
    canonical_hopf_modules()
    git = r56.baseline.prior.git
    before = (git('diff','--binary','HEAD'), git('status','--porcelain'))
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    report = observe(folder)
    if before != (git('diff','--binary','HEAD'), git('status','--porcelain')):
        raise RuntimeError('REPOSITORY_CHANGED')
    print('PHASE176_R3R56R1_GATE=PASS_R3R56R1_HISTORICAL_FAILURE_ISOLATED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
