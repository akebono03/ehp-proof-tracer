from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import toda_group_proof_narrative_contribution_renderer as renderer
from web_group_proof import build_standard_web_group_proof_view

OUTPUT = Path(__file__).resolve().parent / 'audit_report.json'
ORIGINAL = renderer.link_toda_group_proof_narrative_reference_body_consumers
CAPTURED = []


def instrument(presentation, body_markdown, reference_entries):
    source_by_number = renderer._phase154_r5_reference_source_steps_by_number(
        presentation, reference_entries
    )
    references = []
    for entry in reference_entries:
        source_steps = source_by_number.get(entry.number, ())
        consumers = []
        for source in source_steps:
            for edge in presentation.edges:
                if edge.premise_step is not source:
                    continue
                child = edge.parent_step
                consumers.append({
                    'source_type': type(source.conclusion).__name__,
                    'conclusion_type': type(child.conclusion).__name__,
                    'conclusion': renderer._render_generic_narrative_step(child),
                    'premise_count': len(child.premises),
                    'direct_source': any(p is source for p in child.premises),
                })
        references.append({
            'number': entry.number,
            'locator': entry.reference.locator,
            'source_count': len(source_steps),
            'consumers': consumers,
        })
    output = ORIGINAL(presentation, body_markdown, reference_entries)
    CAPTURED.append({
        'references': references,
        'before': body_markdown,
        'after': output,
    })
    return output


def main():
    cases = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (3, 2), (4, 2)]
    reports = []
    for n, k in cases:
        CAPTURED.clear()
        renderer.link_toda_group_proof_narrative_reference_body_consumers = instrument
        try:
            view = build_standard_web_group_proof_view(n, k, max_depth=2, mode='narrative')
            rows = [
                {'prefix': x.prefix, 'math': x.statement_latex or '', 'suffix': x.suffix}
                for x in view.rendered_lines
            ]
            report = {
                'n': n, 'k': k,
                'rows': rows,
                'calls': list(CAPTURED),
                'reference_heading_rows': [
                    x['prefix'] for x in rows if re.search(r'\[R\d+\]', x['prefix'])
                    and ('(4.5)' in x['prefix'] or '(5.1)' in x['prefix']
                         or 'Proposition 4.2' in x['prefix'] or 'Proposition 5.1' in x['prefix'])
                ],
                'reference_prop42': any(
                    'Proposition 4.2' in x['prefix'] for x in rows
                ),
            }
            reports.append(report)
            print(f'CASE n={n} k={k}: rows={len(rows)} calls={len(CAPTURED)} references={report["reference_heading_rows"]}')
        except Exception as exc:
            reports.append({'n': n, 'k': k, 'error': repr(exc)})
            print(f'CASE n={n} k={k}: ERROR {exc!r}')
        finally:
            renderer.link_toda_group_proof_narrative_reference_body_consumers = ORIGINAL

    target = next(r for r in reports if r['n'] == 3 and r['k'] == 1)
    assertions = {}
    if 'rows' in target:
        rows = target['rows']
        headings = [r['prefix'] for r in rows if 'Proposition 4.2' in r['prefix']]
        math = [r['math'] for r in rows]
        whole_sequences = [x for x in math if all(token in x for token in
                           (r'\pi_{5}^{5}', r'\pi_{3}^{2}', r'\pi_{4}^{3}', r'\pi_{4}^{5}'))]
        assertions = {
            'pi43_prop42_absent_from_reference': not headings,
            'pi43_whole_ehp_sequence_once': len(whole_sequences) == 1,
            'pi43_zero_cited': any(r'\pi_{4}^{5} = 0' == r['math'].strip()
                                   and '[R' in r['prefix'] and 'より' in r['prefix'] for r in rows),
            'pi43_diagonal_cited': any(r'\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}' == r['math'].strip()
                                       and '[R' in r['prefix'] and 'より' in r['prefix'] for r in rows),
        }
    report_data = {'cases': reports, 'pi43_regression': assertions}
    OUTPUT.write_text(json.dumps(report_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('AUDIT_REPORT:', OUTPUT)
    for key, value in assertions.items():
        print('CHECK:', key, 'PASS' if value else 'FAIL')
    if not assertions or not all(assertions.values()):
        raise SystemExit('Pi43 regression failed; see audit_report.json')
    if any('error' in r for r in reports):
        raise SystemExit('Some cases could not be audited; see audit_report.json')


if __name__ == '__main__':
    main()
