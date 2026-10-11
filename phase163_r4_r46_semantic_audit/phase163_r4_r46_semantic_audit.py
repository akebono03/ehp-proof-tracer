"""R4-R46 conservative, read-only TeX anchors for 23 existing assertions.

Anchor evidence is not a mathematical proof, source verification, or a registry update.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

# Explicit editorial reviews of the five target references. None is inferred at runtime.
# Regexes find a short literal mathematical witness; status separately records its strength.
RULES = {
    'circle_higher_homotopy_zero': ('EXPLICIT', r'\\pi\^\{1\}_\{i\}\s*=\s*0', '式 (5.1) に直接記載'),
    'sphere_connectivity_zero': ('EXPLICIT', r'\\pi\^\{n\}_\{i\}\s*=\s*0', '式 (5.1) に直接記載'),
    'stable_negative_zero': ('EXPLICIT', r'G_k=\(G_k;2\)=0', '式 (5.1) に直接記載'),
    'diagonal_identity_group': ('SURROUNDING_TEXT', r'\\pi\^\{n\}_\{n\}=\\gen\{\\iota_n\}', '番号付き (5.1) の直後の無番号表示'),
    'stable_zero_stem': ('SURROUNDING_TEXT', r'G_0=\\gen\{\\iota\}', '番号付き (5.1) の直後の無番号表示'),
    'diagonal_suspension_isomorphism': ('NOT_LOCATED', None, '式 (5.1) 自体には懸垂同型の主張を確認できない'),
    'pi3_2_group_relation': ('EXPLICIT', r'\\pi\^\{2\}_\{3\}=\\gen\{\\eta_2\}', '命題に直接記載'),
    'eta2_hopf_relation': ('EXPLICIT', r'H\(\\eta_2\)=\\iota_3', '命題に直接記載'),
    'delta_iota5_relation': ('EXPLICIT', r'\\Delta\(\\iota_5\)=\\pm\s*2', '命題に直接記載'),
    'higher_eta_group_relation': ('EXPLICIT', r'\\pi\^\{n\}_\{n\+1\}=\\gen\{\\eta_n\}', '命題に一般式として直接記載'),
    'pi4_2_group_relation': ('SPECIALIZATION', r'\\pi\^\{n\}_\{n\+2\}=\\gen\{\\eta_n\^\{2\}\}', 'n=2 の特殊化。文献内の別個の列挙ではない'),
    'pi5_3_group_relation': ('SPECIALIZATION', r'\\pi\^\{n\}_\{n\+2\}=\\gen\{\\eta_n\^\{2\}\}', 'n=3 の特殊化。文献内の別個の列挙ではない'),
    'pi6_4_group_relation': ('SPECIALIZATION', r'\\pi\^\{n\}_\{n\+2\}=\\gen\{\\eta_n\^\{2\}\}', 'n=4 の特殊化。文献内の別個の列挙ではない'),
    'higher_eta_squared_group_relation': ('EXPLICIT', r'\\pi\^\{n\}_\{n\+2\}=\\gen\{\\eta_n\^\{2\}\}', 'n>=2 の一般式に直接記載'),
    'pi5_2_group_relation': ('EXPLICIT', r'\\pi\^\{2\}_\{5\}=\\gen\{\\eta_\{2\}\^\{3\}\}', '命題に直接記載'),
    'pi6_3_group_relation': ('EXPLICIT', r'\\pi\^\{3\}_\{6\}=\\gen\{\\nu\x27\}', '命題に直接記載'),
    'pi7_4_group_relation': ('EXPLICIT', r'\\pi\^\{4\}_\{7\}=\\gen\{\\nu_\{4\}\}', '命題に直接記載'),
    'pi8_5_group_relation': ('SPECIALIZATION', r'\\pi\^\{n\}_\{n\+3\}=\\gen\{\\nu_\{n\}\}', 'n=5 の特殊化'),
    'higher_nu_group_relation': ('EXPLICIT', r'\\pi\^\{n\}_\{n\+3\}=\\gen\{\\nu_\{n\}\}', 'n>=5 の一般式に直接記載'),
    'nu_prime_bracket_definition': ('SURROUNDING_TEXT', r'\\nu\x27\\in\\todai\[1\]\{\\eta_3,2\\iota_4,\\eta_4\}', '式 (5.3) の直前の記述'),
    'nu_prime_membership': ('EXPLICIT', r'\\nu\x27\\in\\pi_6\^3', '式 (5.3) に直接記載'),
    'nu_prime_hopf_relation': ('EXPLICIT', r'H\(\\nu\x27\)=\\eta_5', '式 (5.3) に直接記載'),
    'nu_prime_double_relation': ('EXPLICIT', r'2\\nu\x27=\\eta_3\\circ\\eta_4\\circ\\eta_5', '式 (5.3) に直接記載'),
}


def compact(tex: str) -> str:
    """Remove whitespace only; retain mathematical commands and punctuation."""
    return re.sub(r'\s+', '', tex)


def anchor_in_lines(lines: list[str], pattern: str | None, start: int, end: int):
    if pattern is None:
        return None
    # A short TeX witness may wrap across lines, so search each 4-line block.
    for index in range(max(0, start - 1), min(len(lines), end)):
        sample = compact('\n'.join(lines[index:index + 4]))
        if re.search(pattern, sample):
            return {'line_start': index + 1, 'line_end': min(len(lines), index + 4),
                    'evidence_excerpt': '\n'.join(lines[index:index + 4]),
                    'evidence_sha256': hashlib.sha256(sample.encode('utf-8')).hexdigest()}
    return None


def audit(review: dict, tex: str, *, expected_sha256: str | None = None) -> dict:
    if review.get('phase') != '163 R4-R45' or review.get('mode') != 'READ_ONLY_COMPONENT_EVIDENCE':
        raise ValueError('R4-R45 review.json is required')
    if expected_sha256 and hashlib.sha256(tex.encode('utf-8')).hexdigest() != expected_sha256:
        raise ValueError('TeX fingerprint mismatch')
    packets = review['packets']
    if len(packets) != 5 or sum(len(p['assertions']) for p in packets) != 23:
        raise ValueError('Expected five references and 23 assertions')
    lines = tex.splitlines()
    results = []
    seen = set()
    for packet in packets:
        if packet['chapter'] != 5:
            raise ValueError('Priority references must be chapter 5')
        start = packet['source_line']
        # Local vicinity allows unlabeled statements adjacent to numbered environments.
        low = max(1, start - 18)
        high = start + max(35, len(packet['tex_lines']) + 8)
        for assertion in packet['assertions']:
            assertion_id = assertion['assertion_id']
            key = assertion_id.rsplit(':', 1)[-1]
            if assertion_id in seen or key not in RULES:
                raise ValueError(f'Unexpected or duplicate assertion: {assertion_id}')
            seen.add(assertion_id)
            category, pattern, note = RULES[key]
            witness = anchor_in_lines(lines, pattern, low, high)
            if category != 'NOT_LOCATED' and witness is None:
                status = 'ANCHOR_NOT_FOUND'
            else:
                status = category
            results.append({
                'reference_id': packet['reference_id'], 'assertion_id': assertion_id,
                'component_position_existing': assertion['component_position_existing'],
                'status': status, 'editorial_note': note,
                'tex_witness': witness,
                'semantic_confirmation': status == 'EXPLICIT',
                'component_order_newly_confirmed': False,
                'source_verified': False, 'structured': False,
            })
    if len(results) != 23 or set(RULES) != {r['assertion_id'].rsplit(':', 1)[-1] for r in results}:
        raise ValueError('Priority assertion coverage is incomplete')
    return {'phase': '163 R4-R46', 'mode': 'READ_ONLY_SEMANTIC_ANCHOR_AUDIT',
            'source_sha256': review['source_sha256'],
            'assertion_count': len(results), 'status_counts': dict(Counter(r['status'] for r in results)),
            'semantic_matches_confirmed_from_explicit_tex': sum(r['semantic_confirmation'] for r in results),
            'component_positions_newly_confirmed': 0, 'results': results,
            'registration_applied': False, 'id_allocated': False, 'proof_search_connected': False,
            'source_verified': False}


def write_results(data: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'audit.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'assertion_anchors.csv').open('w', newline='', encoding='utf-8-sig') as handle:
        fields = ['reference_id', 'assertion_id', 'component_position_existing', 'status',
                  'tex_line_start', 'tex_line_end', 'editorial_note']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in data['results']:
            witness = row['tex_witness'] or {}
            writer.writerow({'reference_id': row['reference_id'], 'assertion_id': row['assertion_id'],
                             'component_position_existing': row['component_position_existing'],
                             'status': row['status'], 'tex_line_start': witness.get('line_start'),
                             'tex_line_end': witness.get('line_end'), 'editorial_note': row['editorial_note']})
    lines = ['# Phase 163 R4-R46 数学的主張の TeX 対応監査', '',
             '式の直接記載と一般式の特殊化・周辺記述を区別する。TeX の引用は原本照合を意味しない。', '',
             '| Reference | Assertion | 判定 | TeX 行 |', '|---|---|---|---|']
    for row in data['results']:
        w = row['tex_witness']
        ln = str(w['line_start']) if w else '—'
        lines.append(f"| {row['reference_id']} | `{row['assertion_id']}` | {row['status']} | {ln} |")
    lines += ['', '## 判定の意味', '',
              '- EXPLICIT: TeX に主張の直接的な記号表記を検出した。数学的完全性・原本一致の証明ではない。',
              '- SPECIALIZATION: TeX の一般式からパラメータを代入する必要がある。',
              '- SURROUNDING_TEXT: 参照環境の前後に記載され、環境の内部ではない。',
              '- NOT_LOCATED: 当該参照から明示的な根拠が見つからない。',
              '- ANCHOR_NOT_FOUND: 想定した記号形式が存在せず、保留。', '',
              '## 個別の観察', '']
    for row in data['results']:
        lines.append(f"- `{row['assertion_id']}`: {row['editorial_note']}（{row['status']}）")
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--review', type=Path, required=True)
    p.add_argument('--tex', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    review = json.loads(args.review.read_text(encoding='utf-8'))
    raw = args.tex.read_bytes()
    expected = review['source_sha256']['5']
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('Toda chapter 5 SHA-256 mismatch')
    data = audit(review, raw.decode('utf-8-sig'))
    write_results(data, args.output)
    print(json.dumps({k: v for k, v in data.items() if k != 'results'}, ensure_ascii=False, indent=2))
    print('No TeX, Registry, or ID changed; full pytest suite not run.')


if __name__ == '__main__':
    main()
