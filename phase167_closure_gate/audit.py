from __future__ import annotations
import json
from pathlib import Path
from web_group_proof import build_standard_web_group_proof_view

results = []
failures = []
for n in range(2, 32):
    view = build_standard_web_group_proof_view(n, 1, max_depth=2, mode='narrative')
    rows = [(line.prefix or '', line.statement_latex or '', line.suffix or '') for line in view.rendered_lines]
    full = '\n'.join(' '.join(row) for row in rows)
    headings = [p for p, _, _ in rows if p.startswith('**[R')]
    completed = '証明未完成' not in full and '□' in full
    entry = {'n': n, 'k': 1, 'complete_display': completed, 'row_count': len(rows), 'references': headings}
    results.append(entry)
    if not completed:
        failures.append(f'n={n}: 1-stem proof not complete in public narrative')

pi43 = next((x for x in results if x['n'] == 3), None)
view = build_standard_web_group_proof_view(3, 1, max_depth=2, mode='narrative')
rows = [(line.prefix or '', line.statement_latex or '', line.suffix or '') for line in view.rendered_lines]
heads = [prefix for prefix, _, _ in rows if prefix.startswith('**[R')]
if any('4.2' in heading for heading in heads):
    failures.append('pi4^3: Proposition 4.2 occurs in Reference')
for formula in (r'\pi_{4}^{5} = 0', r'\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}'):
    matches = [(p, m) for p, m, _ in rows if m.strip() == formula]
    if not any('[R1]' in p and 'より' in p for p, _ in matches):
        failures.append('pi4^3: missing [R1] specialization: ' + formula)

report = {'cases': results, 'pi43_references': heads, 'failures': failures}
output = Path(__file__).resolve().parent / 'stem1_audit.json'
output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
for entry in results:
    print(f"STEM1 n={entry['n']} complete={entry['complete_display']} references={len(entry['references'])}")
print('AUDIT_REPORT:', output)
print('AUDIT_FINDINGS:', len(failures))
for failure in failures:
    print('FINDING:', failure)
