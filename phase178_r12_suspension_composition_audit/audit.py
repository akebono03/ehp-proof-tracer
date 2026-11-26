"""Inspect actual typed zero-image dependencies and preview notation only."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).parent.name
BASE = '4235e902a0a6eea227ab9ec8ab8ebe4529b9aae4'
PREFIX = 'PHASE178_R12_'
TESTS = (
    PACKAGE + '/tests/test_audit.py',
    'phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py',
    'phase177_r17r6r1_suspension_composition_display/tests/test_display.py',
    'phase178_r11_hopf_zero_reason_display/tests/test_sentence_layout_audit.py',
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def emit(key, value):
    print(PREFIX + key + '=' + str(value), flush=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8').strip()


def preflight():
    head = git('rev-parse', 'HEAD')
    require(Path(git('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    require(git('branch', '--show-current') == 'develop', 'WRONG_BRANCH')
    require(head == BASE == git('rev-parse', 'origin/develop'), 'REVIEWED_HEAD_REQUIRED')
    require(not git('status', '--porcelain', '--untracked-files=no'), 'TRACKED_CHANGES_REFUSED')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    for path in TESTS:
        require((ROOT / path).is_file(), 'MISSING_TEST:' + path)
    return head


def ancestor_indices(parents, index):
    """Return strict ancestors of a topologically ordered identity graph."""
    if type(index) is not int or not 0 <= index < len(parents):
        raise ValueError('invalid index')
    for i, row in enumerate(parents):
        if any(type(p) is not int or not 0 <= p < i for p in row):
            raise ValueError('invalid premise edge')
    pending = list(parents[index])
    seen = set()
    while pending:
        p = pending.pop()
        if p not in seen:
            seen.add(p)
            pending.extend(parents[p])
    return frozenset(seen)


def locate_sentence(lines, boundary, sentence, numbers):
    """Find an exact unique body line, with only its actual source tag allowed."""
    if not sentence:
        return None
    candidates = {sentence}
    if len(numbers) == 1:
        candidates.add(f'[R{numbers[0]}]より, ' + sentence)
    hits = [i for i in range(boundary + 1, len(lines)) if lines[i] in candidates]
    return hits[0] if len(hits) == 1 else None


def preview_notation(lines, boundary, rows):
    """Preview spelling changes only; ambiguous or shared line ownership is refused."""
    output = list(lines)
    edits = []
    owners = {}
    for row in rows:
        pos = row['body_line_index']
        if pos is not None:
            owners.setdefault(pos, []).append(row['index'])
    for row in rows:
        pos = row['body_line_index']
        old, new = row['typed_sentence'], row['canonical_sentence']
        if (pos is None or pos <= boundary or len(owners[pos]) != 1
                or not old or not new or old == new):
            continue
        if lines[pos] == old:
            replacement = new
        elif len(row['ancestor_citations']) == 1 and lines[pos] == f"[R{row['ancestor_citations'][0]}]より, " + old:
            replacement = f"[R{row['ancestor_citations'][0]}]より, " + new
        else:
            continue
        output[pos] = replacement
        edits.append({'index': row['index'], 'line': pos + 1,
                      'before': lines[pos], 'after': replacement})
    return output, edits


def inspect_model(model, markdown):
    """Read actual proof edges, typed statements, sources and renderer anchors."""
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME, right_zero_transport_inputs
    from phase177_r17r4r1_prop25_suspension_elision.projection import replayed
    from proof import ProofRule
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    steps = model.steps
    numbers = model.step_citation_numbers
    require(len(steps) == 20 and len(numbers) == len(steps), 'MODEL_STEP_COUNT_CHANGED')
    lookup = {id(s): i for i, s in enumerate(steps)}
    require(len(lookup) == len(steps), 'DUPLICATE_STEP_IDENTITY')
    parents = tuple(tuple(lookup.get(id(p)) for p in s.premises) for s in steps)
    scope = root_ancestor_step_indices(steps, model.root_index)
    ancestors = tuple(ancestor_indices(parents, i) for i in range(len(steps)))
    users = tuple(tuple(j for j, ps in enumerate(parents) if i in ps) for i in range(len(steps)))
    lines = markdown.splitlines()
    require(lines.count('証明') == 1, 'BODY_BOUNDARY_AMBIGUOUS')
    boundary = lines.index('証明')
    rows, typed = [], {}
    for i, step in enumerate(steps):
        value = step.conclusion
        cites = sorted({n for j in ancestors[i] | {i} if steps[j].rule is ProofRule.GIVEN for n in numbers[j]})
        sentence = typed_sentence(value, step)
        pos = locate_sentence(lines, boundary, sentence, cites)
        row = {'index': i, 'in_root_scope': i in scope, 'root': i == model.root_index,
               'proof_rule': step.rule.name, 'inference_rule': getattr(step.inference_rule, 'name', None),
               'statement_type': type(value).__name__, 'statement': repr(value),
               'premises': list(parents[i]), 'users': list(users[i]), 'ancestors': sorted(ancestors[i]),
               'own_citations': list(numbers[i]), 'ancestor_citations': cites,
               'typed_sentence': sentence, 'body_line_index': pos,
               'actual_line': lines[pos] if pos is not None else None,
               'canonical_sentence': None, 'right_zero_transport_verified': False}
        if (i in scope and type(value) is GeneratorImage
                and type(value.map) is TodaSuspensionMap and type(value.target_generator) is Zero
                and type(value.source_generator) is Composition):
            domain, target = value.map.source_group, value.map.target_group
            factors = typed_composition_factors(value.source_generator)
            if (type(domain) is TodaPrimaryGroup and type(target) is TodaPrimaryGroup
                    and factors is not None and len(factors) >= 2
                    and expression_endpoints(value.source_generator) == (domain.group_dimension, domain.sphere_dimension)
                    and target == TodaPrimaryGroup(domain.group_dimension + 1, domain.sphere_dimension + 1)):
                row['factors'] = [repr(f) for f in factors]
                row['map'] = repr(value.map)
                row['replayed'] = replayed(step)
                typed[i] = (value.map, factors)
                if (step.rule is ProofRule.INFERENCE and row['replayed'] and i != model.root_index
                        and not numbers[i] and sentence and sentence.startswith('$E(') and sentence.endswith(')=0$.')):
                    latex = render_toda_public_group_generator_latex(value.source_generator)
                    if latex and '\n' not in latex and '\r' not in latex:
                        row['canonical_sentence'] = '$E(' + latex + ')=0$.'
                if row['inference_rule'] == RULE_NAME and len(parents[i]) == 1:
                    base = steps[parents[i][0]].conclusion
                    row['right_zero_transport_verified'] = (row['replayed'] and right_zero_transport_inputs(value, base) == (base,))
        rows.append(row)
    candidates = []
    for i, key in typed.items():
        for j in sorted(ancestors[i] & typed.keys()):
            if key == typed[j]:
                candidates.append({'earlier': j, 'later': i,
                                   'same_typed_map_and_ordered_factors': True,
                                   'direct_premise': j in parents[i],
                                   'earlier_users': list(users[j]), 'later_users': list(users[i]),
                                   'earlier_citations': list(numbers[j]), 'later_citations': list(numbers[i]),
                                   'decision': 'REVIEW_REQUIRED_NO_ELISION'})
    preview, edits = preview_notation(lines, boundary, rows)
    require(preview[:boundary + 1] == lines[:boundary + 1] and len(preview) == len(lines), 'PREVIEW_CHANGED_LAYOUT_OR_REFERENCES')
    return rows, candidates, edits, '\n'.join(preview) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    base = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='attempt_', dir=base))
    report = {'gate': 'FAIL_R12_AUDIT', 'dry_run': args.dry_run, 'full_pytest': 'NOT_RUN',
              'production_changes': 0, 'new_math_rules': 0, 'new_given': 0, 'elided_steps': 0}
    try:
        head = preflight()
        report['head'] = head
        emit('HEAD', head)
        if args.dry_run:
            report['gate'] = 'PASS_R12_READ_ONLY_DRYRUN'
        else:
            import phase168_r3_5_model_renderer as renderer
            from phase178_r11_hopf_zero_reason_display.audit import inspect_actual

            real = renderer.render_model_backed_narrative_markdown
            calls = []

            def observed(result, model):
                markdown = real(result, model)
                calls.append((result, model, markdown))
                return markdown

            with patch.object(renderer, 'render_model_backed_narrative_markdown', observed):
                summary = inspect_actual(folder)
            require(len(calls) == 1, 'RENDER_CAPTURE_MISSING_OR_AMBIGUOUS')
            result, model, markdown = calls[0]
            before = (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals)
            rows, candidates, edits, preview = inspect_model(model, markdown)
            require(before == (model.steps, model.citations, model.step_citation_numbers, model.root_index, model.open_goals), 'MODEL_CHANGED')
            require(any('factors' in row for row in rows), 'TYPED_ZERO_COMPOSITION_NOT_FOUND')
            (folder / 'narrative.md').write_text(markdown, encoding='utf-8')
            (folder / 'notation_preview.md').write_text(preview, encoding='utf-8')
            report.update(audit=summary, steps=rows, duplicate_candidates=candidates, notation_preview_edits=edits)
            emit('ROOT_STATUS', summary['status'])
            emit('ROOT_STEPS', summary['proven_step_count'])
            emit('ROOT_OPEN_GOALS', summary['open_goal_count'])
            emit('REFERENCES', len(model.citations))
            emit('TRUST_STATUS', summary['trust_status'])
            emit('TARGET_GIVEN_COUNT', summary['target_given_count'])
            emit('DUPLICATE_CANDIDATES', len(candidates))
            emit('NOTATION_PREVIEW_EDITS', len(edits))
            emit('PREVIEW', folder / 'notation_preview.md')
            command = [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--import-mode=importlib', *TESTS]
            report['focused_command'] = command
            subprocess.run(command, cwd=ROOT, check=True)
            require(preflight() == head, 'POST_AUDIT_INTEGRITY_FAILED')
            report['gate'] = 'PASS_R12_TYPED_DISPLAY_AUDIT_ONLY'
    except Exception as exc:
        report.update(error=repr(exc), traceback=traceback.format_exc())
        emit('ERROR', repr(exc))
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')
    emit('REPORT', folder / 'report.json')
    emit('FULL_PYTEST', 'NOT_RUN')
    emit('GATE', report['gate'])
    return 0 if report['gate'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
