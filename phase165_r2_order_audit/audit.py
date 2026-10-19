"""Read-only narrative ordering audit for Phase 165 R2."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown
from phase165_r57_r10_step_narrative import ordered_proof_ancestry
from proof import ProofRule

ROOT = Path.cwd()
OUT = ROOT / 'phase165_r2_order_audit_results'
OUT.mkdir(exist_ok=True)
TARGET = ROOT / 'toda_group_proof_narrative_renderer.py'


def relevant_lines(markdown: str) -> list[dict]:
    keys = ('infinite cyclic quotient structure', 'eta', '\\eta', '\\ker E', '第一同型定理', '\\cong', '\\pi_{n}^{n}', '\\pi_{5}^{5}', '\\operatorname{Im}', '完全性より', '以上より')
    return [{'line': number, 'text': line} for number, line in enumerate(markdown.splitlines(), 1) if any(key in line for key in keys)]


def inspect(n: int, k: int) -> dict:
    result = search_group_from_registered_goal(n=n, k=k)
    markdown = render_partial_proof_markdown(result)
    name = f'pi{n+k}_{n}'
    (OUT / f'{name}.md').write_text(markdown, encoding='utf-8')
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion] if result.conclusion is not None else []
    ancestry = ordered_proof_ancestry(roots[0]) if len(roots) == 1 else ()
    steps = [{'index': i, 'statement_type': type(s.conclusion).__name__, 'rule': s.rule.value, 'inference_name': getattr(s.inference_rule,'name',None), 'premise_count': len(s.premises)} for i,s in enumerate(ancestry)]
    report = {'group': name, 'status': result.status.value, 'root_count': len(roots), 'ancestry_count': len(ancestry), 'steps': steps, 'narrative_evidence': relevant_lines(markdown)}
    (OUT / f'{name}_steps.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report


def main() -> None:
    source = TARGET.read_text(encoding='utf-8')
    tree = ast.parse(source)
    occurrences = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == 'render_toda_group_proof_narrative_markdown']
    report = {'source_path': str(TARGET), 'r2_terminal_insertion_present': 'Phase 165 R2: retain typed quotient derivations' in source, 'public_renderer_definitions': [{'start': n.lineno, 'end': n.end_lineno} for n in occurrences], 'results': [inspect(2,1), inspect(3,1)]}
    (OUT / 'audit_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    for item in report['results']:
        print(item['group'], item['status'], 'steps', item['ancestry_count'])
        print('  matching narrative lines',len(item['narrative_evidence']))
    print('R2 terminal insertion present:', report['r2_terminal_insertion_present'])
    print('Report:', OUT / 'audit_result.json')
    if any(item['status'] != 'complete' for item in report['results']):
        raise SystemExit('One or more proofs are not complete; see report.')


if __name__ == '__main__':
    main()
