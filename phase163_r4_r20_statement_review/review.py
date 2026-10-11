"""Phase 163 R4-R20: review equation claims conservatively; no production writes."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from phase163_r4_r18_prose_registry.integrate import integrate
from phase163_r4_r19_equation_audit.audit import audit

# (TeX display start line, classification, detailed claim, assumptions, issue)
# Labels are provisional, not claims of verification against printed Toda.
CLAIMS = (
    (173, 'definition_component', '誘導写像 f* と g* の定義域・値域', '基点付き写像 f:X→Y, g:Y→Z を固定', ''),
    (180, 'independent_claim', '合成の結合律 (γ∘β)∘α=γ∘(β∘α)', '合成可能な基点付きホモトピー類 α,β,γ', ''),
    (183, 'independent_claim', '前合成・後合成の反変／共変合成則', '写像 f1,f2,g1,g2 が合成可能', ''),
    (201, 'independent_claim', 'reduced join の結合性を表す自然な同相', '基点付き空間 A,B,C', '原稿の reduced join と通常の smash product の用語の違いを確認'),
    (211, 'needs_mathematical_correction', '原稿は S^m∧S^n ≅ S^(m+n+1) と記載', '球面 S^m,S^n', '通常の smash product は S^(m+n)。reduced join の記号・次元の整合性を要確認'),
    (234, 'compound_claim', 'reduced join のホモトピー不変性・結合性・合成保存', '基点付き写像 f,g,h 等が定義され合成可能', '0),i),ii) は分割候補'),
    (260, 'compound_claim', 'ホモトピー類の reduced join の結合性・合成保存', '関連するホモトピー類が合成可能', 'i),ii) は分割候補'),
    (294, 'compound_claim', '懸垂のホモトピー不変性・反復・合成保存', 'n,m は反復懸垂を定義できる非負整数、写像・類は合成可能', '0),i),ii) は分割候補'),
    (354, 'independent_claim', '[EX,Y] と π1(Y^X_0) の自然同型', 'X locally compact（局所コンパクト）という本文条件', '写像空間の位相・基点条件を確認'),
    (366, 'independent_claim', '後合成 f* が [EX,Y] の加法を保存', 'f:Y→Z、α,α′∈[EX,Y]', ''),
    (369, 'independent_claim', 'E[g] による前合成が [EX,Y] の加法を保存', 'g:W→X、α,α′∈[EX,Y]', ''),
    (406, 'independent_claim', 'Ω(β∘α)=Ωβ∘Ωα', '合成可能な基点付きホモトピー類 α,β', ''),
    (473, 'compound_claim', 'Ω0 の前合成・後合成に関する自然性（4式）', '本文の f:X→Y,g:EY→Z,h:Z→W、α,β,γ', '4式の独立性・型を個別確認'),
    (1115, 'independent_claim', 'E^n(Y∪β CX) と E^nY∪E^nβ CE^nX の対応', 'β:X→Y は貼り合わせ写像、n 重懸垂が定義される', '同一視の厳密性・自然性を確認'),
)


def review(source: Path) -> tuple[dict, list[dict]]:
    raw = source.read_bytes()
    integrated = integrate(source)
    rows, audit_summary = audit(source)
    if hashlib.sha256(raw).hexdigest() != audit_summary['source_sha256']:
        raise ValueError('Source hash mismatch')
    lookup = {r['start_line']: r for r in rows if r['review_status'] == 'INDEPENDENT_CANDIDATE'}
    if sorted(lookup) != sorted(x[0] for x in CLAIMS):
        raise ValueError('R4-R19 independent candidates changed; review required')
    entries = integrated['entries']
    ids = {e['statement_id'] for e in entries}
    if len(ids) != 24:
        raise ValueError('R4-R18 registry changed; review required')
    source_lines = raw.decode('utf-8-sig').splitlines()
    detailed = []
    for line, category, meaning, conditions, issue in CLAIMS:
        original = lookup[line]
        snippet = '\n'.join(source_lines[line-1:original['end_line']])
        if not snippet.strip():
            raise ValueError('Empty source span')
        detailed.append({
            'candidate_no': original['candidate_no'], 'source_line': line,
            'source_end_line': original['end_line'],
            'review_class': category, 'claim_ja': meaning,
            'hypotheses_ja': conditions, 'verification_issue_ja': issue,
            'source_tex': snippet, 'source_span_sha256': hashlib.sha256(snippet.encode()).hexdigest(),
            'statement_id': '', 'id_status': 'NOT_ISSUED',
            'printed_source_status': 'UNVERIFIED',
            'existing_registry_equivalence': 'UNVERIFIED',
            'formal_statement_status': 'NOT_COMPILED',
            'search_status': 'UNCONNECTED',
        })
    # Remaining 65 candidates: show enclosing environment evidence, without
    # asserting semantic classification from TeX syntax alone.
    pending = []
    for r in rows:
        if r['review_status'] not in {'NEEDS_FULL_TEXT_REVIEW', 'UNRESOLVED_CONTEXT'}:
            continue
        line = r['start_line']
        before = '\n'.join(source_lines[max(0, line-7):line-1])
        after = '\n'.join(source_lines[r['end_line']:min(len(source_lines),r['end_line']+6)])
        pending.append({**r, 'preceding_context': before, 'following_context': after,
                        'next_action': '本文と前後の証明環境を読んで所属と独立性を判定',
                        'semantic_decision': 'PENDING_MANUAL_REVIEW'})
    if len(pending) != 65:
        raise ValueError('Pending queue changed; audit required')
    result = {
        'phase': '163 R4-R20', 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'preserved_records': len(entries), 'detailed_independent_candidates': len(detailed),
        'review_by_kind': {k: sum(r['review_class'] == k for r in detailed)
                           for k in sorted({r['review_class'] for r in detailed})},
        'remaining_semantic_pending': len(pending),
        'new_statement_ids_issued': 0, 'existing_ids_modified': 0,
        'printed_original_verified': 0, 'legacy_equivalence_verified': 0,
        'proof_search_connected': 0, 'exhaustive_review': False,
        'major_issue': 'S^m wedge S^n dimension in supplied TeX requires mathematical verification',
    }
    return {'summary': result, 'claims': detailed, 'reserved_catalog': integrated}, pending


def run(source: Path, output: Path) -> dict:
    result, pending = review(source)
    output.mkdir(parents=True, exist_ok=True)
    (output/'statement_review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (output/'summary.json').write_text(json.dumps(result['summary'], ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    with (output/'pending_65.csv').open('w', encoding='utf-8-sig', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=list(pending[0]))
        writer.writeheader()
        writer.writerows(pending)
    lines = ['# Phase 163 R4-R20 — 第1章の独立主張精査', '',
             '添付 TeX を基準とする暫定審査。印刷原典照合・既存67成分との同一性確認は未実施。',
             '既存24 IDを維持し、14候補にはIDをまだ発行しない。', '',
             '## 14候補の内容と条件', '']
    for x in result['claims']:
        lines.append(f"- {x['source_line']}行 [{x['review_class']}] {x['claim_ja']}。条件：{x['hypotheses_ja']}。" +
                     (f"要確認：{x['verification_issue_ja']}。" if x['verification_issue_ja'] else ''))
    lines += ['', '## 未完了', '',
              '残り65箇所を保留として前後文脈付きCSVに保存。数学的に内容を読んで独立性を判定する必要がある。',
              '通常の smash product と原稿の reduced join の次元記法に注意する。',
              '全体 pytest は Phase 終了時のみ。', '']
    (output/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    return result['summary']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
