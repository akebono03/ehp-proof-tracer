"""Phase 163 R4-R75: source-grounded ownership review, without registration."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

# Evidence-grounded proposals only; they are NOT mathematical verification.
# The numbered proposition owning a proof must still be checked in full TeX.
DECISIONS = {
    66: ("PARAPHRASE_OF_PRECEDING_PROPOSITION", "ch1:preceding-proposition:at-953", "直前の proposition 終了後の『要するに』による言い換え。独立 Reference の新設を保留。", "\\end{proposition}"),
    67: ("PROOF_COSET_EXPRESSION", "ch1:coset-comparison:1004-1027", "coset 比較の一方の部分群を記述。関連する #68, #69 と同じ議論に属する候補。", "coset"),
    68: ("PROOF_COSET_EXPRESSION", "ch1:coset-comparison:1004-1027", "同じ coset 比較の他方の部分群。#67, #69 と独立に登録しない。", "coset"),
    69: ("PROOF_COSET_EXPRESSION", "ch1:coset-comparison:1004-1027", "前の二つの部分群を比較する包含部分。TeX 誤記候補 E^[n+1] を要確認。", "この群は"),
    133: ("PROOF_SPECTRAL_SEQUENCE_STEP", "ch2:spectral-sequence:705-818", "スペクトル列の計算中の分解式。番号付き命題との境界は未確認。", "E_\\infty"),
    142: ("CONCLUSION_OF_NUMBERED_PROOF", "ch2:delta-proof:1021-1026", "\\qed と同じ式中にある証明の結論。既存番号付き主張との一致を確認する。", "\\qed"),
    256: ("EHP_EXACTNESS_PROOF_FRAGMENT", "ch4:ehp-proof:283-291", "『残る問題は』に続く完全列の一部分。完全性を証明する文脈に帰属。", "残る問題は"),
    120: ("UNNUMBERED_ASSERTION_CASE", "ch2:cup-product-by-parity:549-559", "m 偶数の積の公式。直前の m 奇数の場合との一体的登録を要確認。", "m$ が偶数"),
    122: ("UNNUMBERED_ASSERTION_CASE", "ch2:cohomology-maps:560-578", "条件付き i* 同型。#123 と同じ周辺段落でも Assertion は別にする案。", "i<pm"),
    123: ("UNNUMBERED_ASSERTION_CASE", "ch2:cohomology-maps:560-578", "h* の単射性に関する式。#122 と同じ Reference 内の別 Assertion 候補。", "単射同型"),
    140: ("UNNUMBERED_ASSERTION_CASE", "ch2:relative-composition:991-999", "境界写像と h_m* の合成に関する二つの関係。1つの出典段落に2 Assertion の可能性。", "相対ホモトピー群"),
}
HOLD_IDS = {66, 67, 68, 69, 133, 142, 256}
ASSERTION_IDS = {120, 122, 123, 140}


def review(previous: dict) -> dict:
    if previous.get('phase') != '163 R4-R74' or previous.get('source_phase') != '163 R4-R73':
        raise ValueError('Expected R74 source')
    proposals = previous.get('proposals')
    if not isinstance(proposals, list) or len(proposals) != 65:
        raise ValueError('Expected 65 R74 candidates')
    ids = [r['r48_index'] for r in proposals]
    if len(set(ids)) != 65 or not set(DECISIONS).issubset(ids):
        raise ValueError('Source identifiers mismatch')
    if previous.get('preserved_prior_editorial_proposal_count') != 172:
        raise ValueError('Prior editorial proposal count changed')
    if previous.get('mathematical_role_verified_count') != 0 or previous.get('production_registry_modified') is not False:
        raise ValueError('Unexpected production mutation or verification')
    focused = []
    for row in proposals:
        index = row['r48_index']
        if hashlib.sha256(row['excerpt'].encode('utf-8')).hexdigest() != row['excerpt_sha256']:
            raise ValueError(f'Excerpt changed: {index}')
        if index not in DECISIONS:
            continue
        expected = 'HOLD_BOUNDARY_REVIEW' if index in HOLD_IDS else 'UNNUMBERED_ASSERTION_REVIEW'
        if row['proposed_review_role'] != expected:
            raise ValueError(f'Unexpected source role: {index}')
        role, group, rationale, anchor = DECISIONS[index]
        if anchor not in row['context'] and anchor not in row['excerpt']:
            raise ValueError(f'Expected evidence anchor missing: {index}')
        focused.append({
            'r48_index': index,
            'chapter': row['chapter'],
            'source_file': row['source_file'],
            'source_line': row['source_line'],
            'excerpt_sha256': row['excerpt_sha256'],
            'excerpt': row['excerpt'],
            'context': row['context'],
            'previous_role': row['proposed_review_role'],
            'proposed_ownership': role,
            'provisional_group': group,
            'reason': rationale,
            'evidence_anchor': anchor,
            'source_boundary_verified': False,
            'mathematical_role_verified': False,
            'registration_allowed': False,
            'production_reference_id': None,
            'production_assertion_ids': [],
        })
    groups = {}
    for row in focused:
        groups.setdefault(row['provisional_group'], []).append(row['r48_index'])
    return {
        'phase': '163 R4-R75',
        'mode': 'READ_ONLY_FOCUSED_OWNERSHIP_PROPOSALS',
        'source_phase': '163 R4-R74',
        'r74_candidate_count': len(proposals),
        'previously_reviewed_count': 172,
        'focused_boundary_count': len(focused),
        'hold_review_count': len(HOLD_IDS),
        'unnumbered_assertion_review_count': len(ASSERTION_IDS),
        'untouched_r74_count': len(proposals)-len(focused),
        'ownership_group_count': len(groups),
        'ownership_groups': dict(sorted(groups.items())),
        'proposed_ownership_counts': dict(sorted(Counter(x['proposed_ownership'] for x in focused).items())),
        'input_proposal_sha256': hashlib.sha256(json.dumps(proposals, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest(),
        'source_boundary_verified_count': 0,
        'mathematical_role_verified_count': 0,
        'original_edition_verified': False,
        'semantic_registration_allowed_count': 0,
        'production_registry_modified': False,
        'production_ids_allocated': False,
        'proof_search_connected': False,
        'full_suite_run': False,
        'focused_proposals': focused,
    }


def write_reports(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output/'ownership_proposals.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    fields = ['r48_index', 'chapter', 'source_file', 'source_line', 'proposed_ownership', 'provisional_group', 'reason', 'evidence_anchor', 'excerpt', 'context', 'registration_allowed']
    with (output/'ownership_proposals.csv').open('w', encoding='utf-8-sig', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result['focused_proposals'])
    lines = ['# Phase 163 R4-R75：出典帰属の重点監査案', '', '保留7件と番号なし主張候補4件を確認。帰属案であって原本・数学的境界の検証ではない。', '', '## 集約案', '']
    for group, indices in result['ownership_groups'].items():
        lines.append(f'- `{group}`: {", ".join("#"+str(i) for i in indices)}')
    lines += ['', '## 原文と判断根拠', '']
    for row in result['focused_proposals']:
        lines += [f"### R48 #{row['r48_index']}（第{row['chapter']}章 {row['source_line']}行）", '', f"- 帰属案: `{row['proposed_ownership']}`", f"- 集約先（暫定）: `{row['provisional_group']}`", f"- 根拠: {row['reason']}", '', '```tex', row['excerpt'], '```', '', '```text', row['context'], '```', '']
    lines += ['## 未完了事項', '', '- 引用原本の照合、番号付き命題との境界、数学的妥当性はいずれも未検証。', '- R74 の残り54件および R73 の172件を変更せず、正式登録を行わない。']
    (output/'report.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    source = root/'phase163_r4_r74_output'/'remaining_boundary_proposals.json'
    result = review(json.loads(source.read_text(encoding='utf-8')))
    write_reports(result, root/'phase163_r4_r75_output')
    print(json.dumps({k:v for k,v in result.items() if k!='focused_proposals'}, indent=2, ensure_ascii=False))
    print('R75 focused ownership review complete. Full pytest not run.')


if __name__ == '__main__':
    main()
