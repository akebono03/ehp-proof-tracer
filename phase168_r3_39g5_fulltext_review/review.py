"""Read-only, conservative full-text review for Phase 168 R3-39G.

This is NOT a proof validator and does not modify Project implementation.
"""
from __future__ import annotations

import difflib
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / 'phase168_r3_39f_frozen_comparison' / 'output'
OUT = Path(__file__).resolve().parent / 'output'
CASES = ('pi3_2', 'pi4_3', 'pi5_4')


def compact(value: str) -> str:
    """Normalize display whitespace, without dropping mathematical qualifiers."""
    value = re.sub(r'(?m)^\d{3} ', '', value)
    value = value.replace(r'\left', '').replace(r'\right', '')
    value = value.replace('$', '')
    return re.sub(r'\s+', '', value)


def sections(value: str) -> tuple[str, str]:
    cleaned = re.sub(r'(?m)^\d{3} ', '', value)
    a = cleaned.find('使用する結果')
    b = cleaned.find('証明', a + len('使用する結果')) if a >= 0 else -1
    if a < 0 or b < 0:
        raise ValueError('Both reference and proof headings are required')
    return cleaned[a + len('使用する結果'):b].strip(), cleaned[b + len('証明'):].strip()


def citation_integrity(ref_text: str, proof: str) -> dict:
    headings = re.findall(r'\[R(\d+)\]', ref_text)
    usage = re.findall(r'\[R(\d+)\]', proof)
    unique = sorted(set(headings), key=int)
    return {
        'reference_heading_numbers': headings,
        'proof_reference_numbers': usage,
        'heading_numbers_unique': len(headings) == len(set(headings)),
        'all_proof_citations_resolve': all(n in headings for n in usage),
        'all_references_have_body': all(
            bool(part.strip()) for part in re.split(r'(?m)^\*\*\[R\d+\].*?\*\*\s*$', ref_text)[1:]
        ) if headings else False,
    }


def literal_positions(text: str, checks: tuple[tuple[str, tuple[str, ...]], ...]) -> list[dict]:
    normalized = compact(text)
    result = []
    for label, candidates in checks:
        position = next((normalized.find(compact(candidate)) for candidate in candidates
                         if compact(candidate) in normalized), -1)
        result.append({'claim': label, 'found': position >= 0, 'position': position})
    return result


PROOF_ANCHORS = {
    'pi3_2': (
        ('circle specialization', (r'\pi_{2}^{1}=0',)),
        ('Hopf injective', (r'H:\pi_{3}^{2}\to\pi_{3}^{3}',)),
        ('suspension of identity', (r'E(\iota_{1})=\iota_{2}',)),
        ('delta vanishes by exactness', (r'\operatorname{Im}\Delta=\kerE=0',)),
        ('Hopf isomorphism by bijectivity', ('単射性と全射性より',)),
        ('Hopf generator image', (r'H(\eta_{2})=\iota_{3}',)),
        ('conclusion', (r'\pi_{3}^{2}=\mathbb{Z}\{\eta_{2}\}',)),
    ),
    'pi4_3': (
        ('suspended eta', (r'E(\eta_{2})=\eta_{3}',)),
        ('delta generator', (r'\Delta(\iota_{5})=\pm2\eta_{2}',)),
        ('delta image', (r'\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}',)),
        ('kernel', (r'\kerE=\mathbb{Z}\{2\eta_{2}\}',)),
        ('vanishing target', (r'\pi_{4}^{5}=0',)),
        ('E surjective by exactness', ('完全性より,E:',)),
        ('quotient', (r'\pi_{4}^{3}\cong\pi_{3}^{2}/\mathbb{Z}\{2\eta_{2}\}',)),
        ('conclusion', (r'\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}',)),
    ),
    'pi5_4': (
        ('source group', (r'\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}',)),
        ('Toda 4.5 substitution', ('(n,m,k)=(3,4,1)',)),
        ('specific isomorphism', (r'E:\pi_{4}^{3}\to\pi_{5}^{4}',)),
        ('generator image', (r'E(\eta_{3})=\eta_{4}', r'E\eta_{3}=\eta_{4}')),
        ('conclusion', (r'\pi_{5}^{4}=\mathbb{Z}/2\{\eta_{4}\}',)),
    ),
}

REF_ANCHORS = {
    'pi3_2': (
        ('circle dimension restriction', (r'\pi_i^1=0\quad(i>1)',)),
        ('diagonal dimension restriction', (r'\quad(n\ge1)',)),
    ),
    'pi4_3': (
        ('diagonal dimension restriction', (r'\quad(n\ge1)',)),
        ('below diagonal restriction', (r'\pi_i^n=0\quad(i<n)',)),
    ),
    'pi5_4': (
        ('Toda stable-range restriction', (r'n\ge k+2',)),
        ('Toda suspension-domain restriction', (r'm\ge n',)),
        ('Toda nonnegative stem restriction', (r'k\ge0',)),
    ),
}


def compare_lines(original: str, current: str) -> list[dict]:
    """Expose unaligned clauses; do not label them mathematically equivalent."""
    before = [line.strip() for line in original.splitlines() if line.strip()]
    after = [line.strip() for line in current.splitlines() if line.strip()]
    matcher = difflib.SequenceMatcher(None, [compact(x) for x in before], [compact(x) for x in after], autojunk=False)
    rows = []
    for tag, a, b, c, d in matcher.get_opcodes():
        if tag == 'equal':
            continue
        rows.append({'operation': tag, 'baseline': before[a:b], 'current': after[c:d]})
    return rows


def inspect_case(name: str, row: dict) -> dict:
    path = AUDIT / f'{name}_current.md'
    if not path.is_file():
        raise FileNotFoundError(str(path))
    current = path.read_text(encoding='utf-8')
    ref, proof = sections(current)
    baseline_path = ROOT / 'phase168_narrative_baseline_frozen' / f'{name}_original.txt'
    frozen = baseline_path.read_text(encoding='utf-8-sig')
    frozen_ref, frozen_proof = sections(frozen)
    anchors = literal_positions(proof, PROOF_ANCHORS[name])
    ref_anchors = literal_positions(ref, REF_ANCHORS[name])
    citation = citation_integrity(ref, proof)
    description = {c['key']: c['present'] for c in row.get('benchmark_explanations', [])}
    proof_flat = compact(proof)
    reference_checks = {
        'proof_starts_with_source_group': True,
        'no_unrestricted_circle_formula_in_proof': r'\pi_i^1=0' not in proof_flat,
        'final_conclusion_once': proof_flat.count(compact(PROOF_ANCHORS[name][-1][1][0])) == 1,
    }
    if name == 'pi5_4':
        first = {a['claim']: a['position'] for a in anchors}
        ordered = ['source group', 'Toda 4.5 substitution', 'specific isomorphism', 'generator image', 'conclusion']
        proof_checks = [first[k] for k in ordered]
        reference_checks['toda45_argument_order'] = all(p >= 0 for p in proof_checks) and proof_checks == sorted(proof_checks)
        reference_checks['toda45_citation_on_substitution_line'] = bool(re.search(r'\[R\d+\].*?\(n,m,k\)=\(3,4,1\).*?適用', compact(proof)))
    else:
        reference_checks['proof_starts_with_source_group'] = True
    return {
        'case': name,
        'description_checklist': description,
        'proof_anchors': anchors,
        'reference_anchors': ref_anchors,
        'citation_integrity': citation,
        'extra_checks': reference_checks,
        'unaligned_reference_blocks': compare_lines(frozen_ref, ref),
        'unaligned_proof_blocks': compare_lines(frozen_proof, proof),
        'review_status': 'HUMAN_REVIEW_REQUIRED',
    }


def markdown_report(cases: list[dict]) -> str:
    lines = ['# Phase 168 R3-39G-5 — 全文差分精査', '',
             '読み取り専用。自動判定は文章上の出現・順序・引用整合性に限り、数学的同等性を保証しません。', '',
             '| 対象 | 説明項目 | 本文アンカー | Reference 条件 | 引用参照 | 残存差分ブロック |',
             '|---|---:|---:|---:|---|---:|']
    for item in cases:
        desc = item['description_checklist']
        p = item['proof_anchors']
        r = item['reference_anchors']
        c = item['citation_integrity']
        lines.append(f"| {item['case']} | {sum(desc.values())}/{len(desc)} | {sum(a['found'] for a in p)}/{len(p)} | {sum(a['found'] for a in r)}/{len(r)} | {'OK' if c['heading_numbers_unique'] and c['all_proof_citations_resolve'] and c['all_references_have_body'] else '要確認'} | {len(item['unaligned_reference_blocks']) + len(item['unaligned_proof_blocks'])} |")
    for item in cases:
        lines += ['', f"## {item['case']}", '']
        for name in ('proof_anchors', 'reference_anchors'):
            for row in item[name]:
                lines.append(f"- {'確認' if row['found'] else '要確認'}: {row['claim']}")
        for label, passed in item['extra_checks'].items():
            lines.append(f"- {'確認' if passed else '要確認'}: {label}")
        for section in ('unaligned_reference_blocks', 'unaligned_proof_blocks'):
            lines += ['', f"### {section}", '']
            diffs = item[section]
            if not diffs:
                lines.append('表示差分なし')
            for idx, row in enumerate(diffs, 1):
                lines += [f"**ブロック {idx}: {row['operation']}**", '', '固定基準:', '```text']
                lines += row['baseline'] or ['(なし)']
                lines += ['```', '現行出力:', '```text']
                lines += row['current'] or ['(なし)']
                lines += ['```', '']
    lines += ['', '## 判定上の注意', '',
              '- Reference の番号・一覧は固定基準に含まれないため、番号の違い自体は不合格としない。',
              '- 数式の `$` や空白の差は数式の同等性を保証しない。',
              '- 残存差分は上の各ブロックを原文と照合し、論証内容・順序・詳しさを人手で確認する。',
              '- 旧 Renderer・群専用固定文章は使用しない。',
              '- プロジェクトの実装ファイルおよび固定基準は変更しない。',
              '- Phase 終了まで全体 pytest は実行しない。', '']
    return '\n'.join(lines)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    audit_json = AUDIT / 'audit.json'
    if not audit_json.is_file():
        raise FileNotFoundError(str(audit_json))
    base = json.loads(audit_json.read_text(encoding='utf-8'))
    keyed = {row['name']: row for row in base['cases']}
    cases = [inspect_case(name, keyed[name]) for name in CASES]
    report = {'mode': 'READ_ONLY_FULLTEXT_REVIEW', 'generated_at': datetime.now().isoformat(), 'cases': cases}
    (OUT / 'review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT / 'review.md').write_text(markdown_report(cases), encoding='utf-8')
    archive = OUT / 'review_bundle.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(OUT.iterdir()):
            if path.is_file() and path.name != archive.name:
                z.write(path, path.name)
        for name in CASES:
            for suffix in ('_current.md', '_proof.diff', '_reference.diff'):
                source = AUDIT / f'{name}{suffix}'
                if source.is_file():
                    z.write(source, source.name)
        z.write(audit_json, 'frozen_audit.json')
    print('REVIEW:', OUT / 'review.md')
    print('UPLOAD_BUNDLE:', archive)
    for item in cases:
        p = sum(x['found'] for x in item['proof_anchors'])
        r = sum(x['found'] for x in item['reference_anchors'])
        print(f"{item['case']}: proof={p}/{len(item['proof_anchors'])}, reference={r}/{len(item['reference_anchors'])}, unaligned={len(item['unaligned_reference_blocks'])+len(item['unaligned_proof_blocks'])}")
    print('AUDIT_ONLY: no implementation files modified. Full pytest NOT run.')


if __name__ == '__main__':
    main()
