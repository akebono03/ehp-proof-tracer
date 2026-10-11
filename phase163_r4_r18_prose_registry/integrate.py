"""Phase 163 R4-R18: curated Chapter I prose claims, without proof-search changes."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from phase163_r4_r17_statement_registration.register import register

# Reviewed against the supplied Toda_01.tex. These are source anchors, not
# claims of verification against Toda's printed original publication.
# (unique text anchor, kind, content in Japanese, formal status)
CURATED = (
    (r'I^n=\{(t_1,\ldots,t_n)\mid 0\le t_i\le 1\}', 'Definition', '単位立方体 I^n の定義', 'definition'),
    (r'S^n=\{(t_1,\ldots,t_{n+1})\mid t_1^2+\cdots+t_{n+1}^2=1\}', 'Definition', '単位 n 球面 S^n の定義', 'definition'),
    (r'\psi_n:I^n\longrightarrow S^n', 'Definition', '単位立方体から球面への標準写像 ψ_n の定義', 'definition'),
    (r'[X,Y]=\{\, [f]\ \mid\ f:(X,x_0)\to (Y,y_0)\,\}', 'Definition', '基点付きホモトピー類 [X,Y] の定義', 'definition'),
    (r'A\vee B=\bigl(A\times\{b_0\}\bigr)\cup\bigl(\{a_0\}\times B\bigr)', 'Definition', 'A∨B と reduced join（本文表記）の構成', 'definition'),
    (r'\Ex^n X\ :=\ X\ \wedge\ S^n', 'Definition', 'n 重 suspension E^n X の定義', 'definition'),
    (r'(f+g)(d_X(x,t)) :=', 'Definition', '[EX,Y] の加法を誘導する写像演算の定義', 'definition'),
    (r'\Ox Y=\{\ \ell:(I,\partial I)\to (Y,y_0)\ \}', 'Definition', 'loop 空間 ΩY の定義', 'definition'),
    (r'\Omega_0:\ [EX,Y]\xrightarrow{\ \cong\ }[X, \Ox Y]', 'Claim', '懸垂とループのホモトピー集合の自然な全単射', 'stated_claim'),
    (r'\{\alpha,\ \Ex^n\beta,\ \Ex^n\gamma\}_n\ \subset\ [\Ex^{n+1}W, Z]', 'Definition', 'secondary composition（Toda bracket）の定義', 'definition'),
    (r'CX=(X\times I)/\bigl(X\times\{1\}\ \cup\ x_0\times I\bigr)', 'Definition', 'mapping cone に用いる CX の定義', 'definition'),
    (r"$\alpha$ の \emph{extension} と呼ぶ.", 'Definition', 'extension（拡張）の定義', 'definition'),
    (r"\(\widetilde{\gamma}\) を \(\gamma\) の \emph{coextension} と呼ぶ.", 'Definition', 'coextension（余拡張）の定義', 'definition'),
    (r'extension $\overline\alpha$ が存在するための必要十分条件は,', 'Claim', 'extension 存在の必要十分条件', 'stated_claim'),
    (r'coextension $\widetilde{\gamma}$ が存在するための必要十分条件は,', 'Claim', 'coextension 存在の必要十分条件', 'stated_claim'),
)


def integrate(source: Path) -> dict:
    data = source.read_bytes()
    text = data.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n')
    named = register(source)['entries']
    result = []
    positions = []
    for entry in named:
        marker = '\\label{' + entry['tex_label'] + '}'
        location = text.find(marker)
        if location < 0:
            raise ValueError('Named statement label not found: ' + marker)
        positions.append(location)
        result.append({**entry, 'registry_status': 'reserved', 'review_status': 'supplied_tex_reviewed',
                       'source_offset': location, 'entry_scope': 'named_statement'})
    for i, (anchor, kind, meaning, semantic_kind) in enumerate(CURATED, 10):
        if text.count(anchor) != 1:
            raise ValueError(f'Anchor changed or duplicated; review required: {meaning}')
        offset = text.index(anchor)
        result.append({
            'statement_id': f'TODA-S{i:06d}', 'chapter': 1, 'section': 'Chapter I',
            'kind': kind, 'locator': f'Chapter I, line {text.count(chr(10), 0, offset) + 1}',
            'source_line': text.count('\n', 0, offset) + 1,
            'source_offset': offset, 'source_anchor_tex': anchor,
            'source_statement_sha256': hashlib.sha256(anchor.encode()).hexdigest(),
            'statement_type': semantic_kind, 'summary_ja': meaning,
            'entry_scope': 'prose_or_display', 'registry_status': 'reserved',
            'review_status': 'supplied_tex_reviewed',
            'source_status': 'unchecked', 'search_status': 'unconnected',
            'legacy_identity_status': 'unverified', 'existing_component_keys': [],
            'formal_statement_compiled': False,
        })
    result.sort(key=lambda e: e['source_offset'])
    # Existing order_key is retained for named statements; insertion only adds
    # fractional placements in intervals 0..1, 1..2, ..., 9..10.
    for k in range(len(positions) + 1):
        left = Fraction(k, 1)
        gap = [e for e in result if e['entry_scope'] != 'named_statement'
               and sum(p < e['source_offset'] for p in positions) == k]
        for ordinal, e in enumerate(gap, 1):
            position = left + Fraction(ordinal, len(gap) + 1)
            e['order_key'] = str(position.numerator) if position.denominator == 1 else f'{position.numerator}/{position.denominator}'
    if len({e['statement_id'] for e in result}) != len(result):
        raise ValueError('Duplicate Statement ID')
    if len({Fraction(e['order_key']) for e in result}) != len(result):
        raise ValueError('Duplicate position')
    if result != sorted(result, key=lambda e: Fraction(e['order_key'])):
        raise ValueError('Source order differs from publication keys')
    return {'schema_version': 'r4-r18-1', 'source_sha256': hashlib.sha256(data).hexdigest(),
            'source_file': source.name, 'entries': result,
            'scope_note': 'Selected explicit prose definitions/claims and nine named statements only; not a full Chapter I catalog.'}


def run(source: Path, output: Path) -> dict:
    data = integrate(source)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'chapter1_integrated.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {'phase': '163 R4-R18', 'named_statements_preserved': 9,
               'new_explicit_items_reserved': len(CURATED), 'total_records': len(data['entries']),
               'printed_original_verified': 0, 'legacy_equivalence_verified': 0,
               'proof_search_connected': 0, 'full_chapter_exhaustive': False,
               'note': 'More prose and equations need semantic review before completeness can be claimed.'}
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R4-R18 — 第1章の本文項目登録', '',
             '添付 TeX を照合し、明示的な定義・主張を既存9件の命題と掲載順で統合した。',
             'ID は既存台帳との数学的同一性が確認されるまで予約状態。印刷原典未照合。',
             '第1章全文の網羅は未達。名称付き命題内部の成分分割は未実施。', '', '## 掲載順', '']
    for e in data['entries']:
        lines.append(f"- {e['order_key']} | {e['statement_id']} | {e['kind']} | {e['locator']} | " + e.get('summary_ja', e.get('summary_en', '')))
    lines.extend(['', '## 未完了', '', '独立 Equation の全文精査、本文の残余主張、命題内成分、既存67成分の照合。',
                  'Backward Search は未接続。全体 pytest は Phase 終了時のみ。', ''])
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
