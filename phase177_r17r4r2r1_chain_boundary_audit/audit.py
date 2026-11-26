"""Inspect the actual failed display projection without changing the repository."""
from __future__ import annotations

import argparse
import hashlib
import json
import linecache
import os
from pathlib import Path
import sys
import tempfile

from phase177_r2_cited_511_reuse_audit.audit import snapshot
from phase177_r17r4r2_prop25_equality_chain import installer

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'phase177_r17r4r2_prop25_equality_chain'
PINS = {
    'projection.py': '7cbeb23301980982e11ef68727374947ad8aed21c9bae660af8a49dde43473ae',
    'installer.py': '129a208b272302b96f03495f1fbfea48d8d9ed604d9c883078d4904da3f4914c',
    'tests/test_display.py': '507e11423e03d6736b1f74d419e35a237471e33fbab80378b973eb7662552ff0',
}


def preflight():
    for name, pin in PINS.items():
        raw = (ROOT / PACKAGE / name).read_bytes().replace(b'\r\n', b'\n')
        if hashlib.sha256(raw).hexdigest() != pin:
            raise RuntimeError('R17R4R2_PACKAGE_CHANGED:' + name)
    head, changes = installer.preflight()
    for name, (raw, expected, source) in changes.items():
        if raw != expected:
            raise RuntimeError('R17R4R2_HOOK_NOT_INSTALLED:' + name)
    return head


def rule_name(step):
    return step.inference_rule.name if step.inference_rule is not None else None


def observe():
    from phase177_r2_cited_511_reuse_audit.audit import capture
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase177_r17r4r1_prop25_suspension_elision.projection import project_prop25_suspension_elision
    from phase177_r17r4r2_prop25_equality_chain.projection import project_prop25_equality_chain
    from phase176_r3r55_equality_display_isolated.projection import rendered_math
    from phase177_r3_unsigned_delta_composition_isolated.rule import RULE_NAME

    invocation, result, calls, model, view = capture()
    if (result.status.value != 'complete' or result.open_goals
            or view.key != 'generic-complete-proof' or model is None
            or len(model.steps) != 43 or len(result.proven_steps) != 43
            or len(model.citations) != 8):
        raise RuntimeError('BASELINE_PROOF_CHANGED')
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    order = tuple(e.step_index for e in project_narrative_order(model) if e.step_index in scope)
    prior = project_prop25_suspension_elision(model, order)
    if not prior:
        raise RuntimeError('R17R4R1_ELISION_NOT_REPRODUCED')
    lookup = {id(step): i for i, step in enumerate(model.steps)}
    rows = []
    for i, step in enumerate(model.steps):
        rows.append({'index': i, 'rule': rule_name(step), 'trust': step.rule.name,
                     'premises': [lookup.get(id(p)) for p in step.premises],
                     'citations': list(model.step_citation_numbers[i]),
                     'position': order.index(i) if i in order else None,
                     'prior_hidden': i in prior, 'latex': rendered_math(step.conclusion),
                     'conclusion': repr(step.conclusion)})
    for row in rows:
        row['consumers'] = [other['index'] for other in rows if row['index'] in other['premises']]
    prop_indices = {r['index'] for r in rows if r['rule'] == RULE_NAME}
    downstream = set(prop_indices)
    while True:
        expanded = downstream | {r['index'] for r in rows if downstream.intersection(r['premises'])}
        if expanded == downstream:
            break
        downstream = expanded
    targets = {r['index'] for r in rows if r['rule'] == 'equality transitivity' and r['index'] in downstream}
    if not prop_indices or not targets:
        raise RuntimeError('PROP25_CHAIN_NOT_FOUND')
    traces = {i: [] for i in sorted(targets)}
    global_trace = []
    code = project_prop25_equality_chain.__code__

    def tracer(frame, event, arg):
        if frame.f_code is not code:
            return None
        if event == 'line':
            i = frame.f_locals.get('i')
            line = frame.f_lineno
            if i in traces:
                traces[i].append(line)
            elif i is None:
                global_trace.append(line)
        return tracer

    previous_trace = sys.gettrace()
    try:
        sys.settrace(tracer)
        hidden, sentences = project_prop25_equality_chain(model, order, prior)
    finally:
        sys.settrace(previous_trace)
    if hidden or sentences:
        raise RuntimeError('ORIGINAL_FAILURE_NOT_REPRODUCED')
    relevant = set(prop_indices) | targets
    for i in tuple(targets):
        relevant.update(p for p in rows[i]['premises'] if p is not None)
    for i in tuple(relevant):
        relevant.update(p for p in rows[i]['premises'] if p is not None)
    for i in sorted(relevant):
        row = rows[i]
        compact = {k: v for k, v in row.items() if k != 'conclusion'}
        print('PHASE177_R17R4R2R1_NODE=' + json.dumps(compact, ensure_ascii=True), flush=True)
    for i, lines in traces.items():
        checks = [{'line': n, 'source': linecache.getline(code.co_filename, n).strip()}
                  for n in lines]
        print('PHASE177_R17R4R2R1_TRACE=' + json.dumps({'index': i, 'lines': checks}, ensure_ascii=True), flush=True)
    print('PHASE177_R17R4R2R1_PRIOR_HIDDEN=' + str(sorted(prior)))
    print('PHASE177_R17R4R2R1_ROOT_STEPS=43')
    print('PHASE177_R17R4R2R1_REFERENCE_COUNT=8')
    return {'root_index': model.root_index, 'order': list(order), 'prior_hidden': sorted(prior),
            'prop_indices': sorted(prop_indices), 'transitivity_targets': sorted(targets),
            'nodes': rows, 'global_trace': global_trace, 'traces': traces,
            'projection_source': Path(code.co_filename).read_text(encoding='utf-8-sig'),
            'narrative': render_model_backed_narrative_markdown(result, model),
            'references': [{'number': c.number, 'label': c.reference.label,
                            'locator': c.reference.locator, 'steps': list(c.step_indices)}
                           for c in model.citations],
            'hidden': sorted(hidden), 'sentences': sentences}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    before = snapshot()
    head = preflight()
    print('PHASE177_R17R4R2R1_HEAD=' + head, flush=True)
    if args.dry_run:
        if snapshot() != before:
            raise RuntimeError('REPOSITORY_CHANGED')
        print('PHASE177_R17R4R2R1_GATE=PASS_R17R4R2R1_READ_ONLY_DRYRUN')
        return 0
    report = observe()
    if snapshot() != before:
        raise RuntimeError('REPOSITORY_CHANGED')
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / Path(__file__).parent.name
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'chain_boundary.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE177_R17R4R2R1_REPORT=' + str(path))
    print('PHASE177_R17R4R2R1_NEW_MATH_RULES=0')
    print('PHASE177_R17R4R2R1_NEW_GIVEN=0')
    print('PHASE177_R17R4R2R1_FULL_PYTEST=NOT_RUN')
    print('PHASE177_R17R4R2R1_GATE=PASS_R17R4R2R1_FAILURE_BOUNDARY_CAPTURED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
