"""Phase 162 R10-R5: read-only provenance audit of pi_5^3 Web prose."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path


def normalize_math(value: str) -> str:
    return re.sub(r"\s+", "", value).replace(r"\left", "").replace(r"\right", "")


def math_expressions(line: str) -> tuple[str, ...]:
    return tuple(match.group(1) for match in re.finditer(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", line))


def ancestor_distances(root):
    distances = {id(root): 0}
    queue = deque([root])
    while queue:
        parent = queue.popleft()
        for premise in parent.premises:
            if id(premise) not in distances:
                distances[id(premise)] = distances[id(parent)] + 1
                queue.append(premise)
    return distances


def analyze():
    from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
    from toda_group_proof_presentation import build_toda_group_proof_presentation
    from toda_group_proof_narrative_renderer import (
        _render_group_proof_narrative_latex,
        render_toda_group_proof_narrative_markdown,
    )
    from toda_group_proof_narrative_transport_link import render_suspension_transport_link
    from toda_group_proof_narrative_references import extract_toda_group_proof_step_literature_reference
    from toda_literature_statement_boundary import classify_toda_literature_statement_step

    replay = build_phase162_pi5_3_web_replay(max_depth=40)
    presentation = build_toda_group_proof_presentation(replay)
    markdown = render_toda_group_proof_narrative_markdown(presentation)
    root = replay.root_step
    steps = [node.proof_step for node in presentation.nodes]
    ids = {id(step): index for index, step in enumerate(steps)}
    distances = ancestor_distances(root)
    reverse = defaultdict(list)
    for parent in steps:
        for premise in parent.premises:
            if id(premise) in ids:
                reverse[ids[id(premise)]].append(ids[id(parent)])
    step_records = []
    expressions = defaultdict(list)
    for i, step in enumerate(steps):
        latex = _render_group_proof_narrative_latex(step)
        ref = extract_toda_group_proof_step_literature_reference(step)
        boundary = classify_toda_literature_statement_step(step)
        recorded_ref = getattr(step, 'foundational_reference', None)
        item = {
            'id': i,
            'depth_from_root': distances.get(id(step)),
            'proof_rule': str(getattr(step.rule, 'value', step.rule)),
            'inference_rule': getattr(step.inference_rule, 'name', None),
            'statement_type': type(step.conclusion).__name__,
            'statement_latex': latex,
            'parent_node_ids': sorted(reverse[i]),
            'premise_node_ids': [ids[id(p)] for p in step.premises if id(p) in ids],
            'reference_locator': getattr(ref, 'locator', None),
            'fixed_boundary': getattr(getattr(boundary, 'classification', None), 'value', None),
            'foundational_reference': getattr(recorded_ref, 'key', None),
        }
        step_records.append(item)
        if latex:
            expressions[normalize_math(latex)].append(i)
    transport_paragraph = render_suspension_transport_link(root, _render_group_proof_narrative_latex)
    sections = markdown.split('## 証明', 1)
    body = sections[1] if len(sections) == 2 else ''
    rows = []
    heading = 'proof'
    for number, raw in enumerate(body.splitlines(), start=1):
        line = raw.strip()
        if not line or line in ('\\[', '\\]', '---', '□'):
            continue
        latex_items = math_expressions(line)
        if not latex_items and line.startswith('\\') and line != '\\]':
            latex_items = (line,)
        matched = sorted({index for expr in latex_items for index in expressions.get(normalize_math(expr), ())})
        if transport_paragraph and line in transport_paragraph:
            origin = 'TRANSPORT_APPENDIX'
        elif latex_items and matched:
            origin = 'STEP_EXACT_MATH'
        elif latex_items:
            origin = 'MATH_WITHOUT_EXACT_STEP'
        else:
            origin = 'CONNECTOR_OR_PROSE'
        rows.append({'line': number, 'text': line, 'math': list(latex_items), 'candidate_step_ids': matched, 'origin': origin})
    duplicates = defaultdict(list)
    for rec in step_records:
        if rec['statement_latex']:
            duplicates[normalize_math(rec['statement_latex'])].append(rec['id'])
    duplicates = [{'statement_latex': step_records[indices[0]]['statement_latex'], 'step_ids': indices}
                  for indices in duplicates.values() if len(indices) > 1]
    lines_by_step = defaultdict(list)
    for line in rows:
        for sid in line['candidate_step_ids']:
            lines_by_step[sid].append(line['line'])
    for rec in step_records:
        rec['body_line_numbers'] = lines_by_step.get(rec['id'], [])
    return {
        'summary': {
            'nodes': len(steps), 'presentation_edges': len(presentation.edges),
            'body_lines': len(rows), 'line_origins': dict(Counter(row['origin'] for row in rows)),
            'duplicate_conclusions': len(duplicates),
            'matched_steps': len(lines_by_step),
            'unmatched_steps': len(steps) - len(lines_by_step),
        },
        'root_conclusion': repr(root.conclusion),
        'steps': step_records, 'body_lines': rows, 'duplicate_conclusions': duplicates,
        'transport_paragraph': transport_paragraph,
        'web_markdown': markdown,
        'interpretation_warning': 'Exact LaTeX matching finds candidate origins, not proof of semantic relevance. Non-matches may reflect formatting or multi-line LaTeX.',
    }


def write_reports(data: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'phase162_r10_r5_prose_origin.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 162 R10-R5: 証明本文の由来監査', '', '## 概要', '']
    lines.extend(f'- {key}: {value}' for key, value in data['summary'].items())
    lines += ['', '## 本文の行と候補 ProofStep', '', '| 行 | 分類 | 候補ノード | 本文 |', '|---:|---|---|---|']
    for item in data['body_lines']:
        snippet = item['text'].replace('|', '\\|').replace('`', "'")[:160]
        lines.append(f"| {item['line']} | {item['origin']} | {item['candidate_step_ids']} | {snippet} |")
    lines += ['', '## 証明木の全ノード', '', '| ノード | 深さ | 規則 | 前提 | 親 | 文献 | 数式 | 本文行 |', '|---:|---:|---|---|---|---|---|---|']
    for item in data['steps']:
        math = (item['statement_latex'] or item['statement_type']).replace('|','\\|')[:120]
        lines.append(f"| {item['id']} | {item['depth_from_root']} | {item['proof_rule']} | {item['premise_node_ids']} | {item['parent_node_ids']} | {item['reference_locator']} | {math} | {item['body_line_numbers']} |")
    lines += ['', '## 同じ数式を持つ複数ノード', '']
    for item in data['duplicate_conclusions']:
        lines.append(f"- {item['step_ids']}: `{item['statement_latex']}`")
    lines += ['', '## stable 移送追加段落', '', data['transport_paragraph'] or 'なし', '', '## 注意', '', data['interpretation_warning']]
    (output_dir / 'phase162_r10_r5_prose_origin.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (output_dir / 'phase162_r10_r5_web_narrative.md').write_text(data['web_markdown'], encoding='utf-8')


def main():
    data = analyze()
    out = Path.cwd()
    write_reports(data, out)
    print('Phase 162 R10-R5 read-only audit')
    print('Nodes:', data['summary']['nodes'])
    print('Edges:', data['summary']['presentation_edges'])
    print('Line origins:', data['summary']['line_origins'])
    print('Duplicate conclusions:', data['summary']['duplicate_conclusions'])
    print('Transport appendix:', bool(data['transport_paragraph']))
    for name in ('phase162_r10_r5_prose_origin.md', 'phase162_r10_r5_prose_origin.json', 'phase162_r10_r5_web_narrative.md'):
        print('Report:', out / name)


if __name__ == '__main__':
    main()
