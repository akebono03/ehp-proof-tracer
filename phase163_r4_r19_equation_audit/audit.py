"""Phase 163 R4-R19: provenance-preserving equation audit, no registry writes."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from phase163_r4_r15_chapter1.inventory import extract
from phase163_r4_r18_prose_registry.integrate import integrate

# Manually selected, line-anchored review examples from the supplied Chapter I TeX.
# A candidate designation does not establish a new mathematical statement.
REVIEWED = {
    81: ("EXISTING_DEFINITION", "TODA-S000011", "S^n の定義式"),
    87: ("EXISTING_DEFINITION", "TODA-S000012", "psi_n の型の指定"),
    107: ("DEFINITION_COMPONENT", "TODA-S000012", "psi_n の境界での性質"),
    156: ("EXISTING_DEFINITION", "TODA-S000013", "基点付きホモトピー類の定義"),
    173: ("INDEPENDENT_CANDIDATE", "", "誘導写像 f^*, g_* の定義と型"),
    180: ("INDEPENDENT_CANDIDATE", "", "合成の結合律"),
    183: ("INDEPENDENT_CANDIDATE", "", "誘導写像の合成則"),
    191: ("EXISTING_DEFINITION", "TODA-S000014", "wedge の定義"),
    201: ("INDEPENDENT_CANDIDATE", "", "smash product の結合性"),
    211: ("INDEPENDENT_CANDIDATE", "", "球面の smash product と球面の対応（次元・記号要照合）"),
    234: ("INDEPENDENT_CANDIDATE", "", "smash product の性質の列挙"),
    260: ("INDEPENDENT_CANDIDATE", "", "smash product に関する合成則"),
    274: ("EXISTING_DEFINITION", "TODA-S000015", "懸垂の定義"),
    294: ("INDEPENDENT_CANDIDATE", "", "懸垂に関する性質の列挙"),
    334: ("EXISTING_DEFINITION", "TODA-S000016", "懸垂集合の加法定義"),
    354: ("INDEPENDENT_CANDIDATE", "", "ホモトピー集合と基本群の対応"),
    366: ("INDEPENDENT_CANDIDATE", "", "後合成の加法性"),
    369: ("INDEPENDENT_CANDIDATE", "", "前合成の加法性"),
    395: ("DEFINITION_COMPONENT", "TODA-S000017", "ループ写像の定義"),
    406: ("INDEPENDENT_CANDIDATE", "", "loop の合成保存"),
    450: ("EXISTING_CLAIM", "TODA-S000018", "loop-suspension 随伴による全単射"),
    473: ("INDEPENDENT_CANDIDATE", "", "Omega_0 の自然性関係"),
    488: ("DEFINITION_COMPONENT", "TODA-S000019", "二次合成の前提となる零合成条件"),
    510: ("DEFINITION_COMPONENT", "TODA-S000019", "二次合成を表す H の定義"),
    527: ("EXISTING_DEFINITION", "TODA-S000019", "二次合成の集合表記"),
    675: ("UNRESOLVED_CONTEXT", "", "命題直後の関係式、独立性の確認が必要"),
    947: ("UNRESOLVED_CONTEXT", "", "命題内・証明内のどちらの結論か確認が必要"),
    1076: ("EXISTING_DEFINITION", "TODA-S000020", "cone の定義"),
    1115: ("INDEPENDENT_CANDIDATE", "", "cone の懸垂と貼り合わせの対応"),
    1216: ("DEFINITION_COMPONENT", "", "p の定義、所属命題との関係を要確認"),
    1227: ("UNRESOLVED_CONTEXT", "", "p_* 関係式が命題本文の一部か要確認"),
}


def audit(source: Path) -> tuple[list[dict], dict]:
    raw = source.read_bytes()
    rows = extract(raw.decode('utf-8-sig'))
    integrated = integrate(source)
    known = {e['statement_id'] for e in integrated['entries']}
    named = [r for r in rows if r['category'] == 'named_statement']
    results = []
    for index, row in enumerate(rows, 1):
        line = row['start_line']
        if row['category'] == 'named_statement':
            matching = [e for e in integrated['entries'] if e.get('tex_label') == row['label']]
            if len(matching) != 1:
                raise ValueError('Named statement identity mismatch: ' + row['label'])
            status, linked, detail = 'EXISTING_NAMED', matching[0]['statement_id'], '既登録の名前付き命題'
            reviewed = True
        elif line in REVIEWED:
            status, linked, detail = REVIEWED[line]
            reviewed = True
        else:
            status, linked, detail = 'NEEDS_FULL_TEXT_REVIEW', '', '構文抽出のみ。数学的役割は未判定'
            reviewed = False
        if linked and linked not in known:
            raise ValueError('Unknown reserved ID: ' + linked)
        results.append({
            'candidate_no': index, 'start_line': line, 'end_line': row['end_line'],
            'tex_category': row['category'], 'tex_label': row['label'],
            'review_status': status, 'linked_reserved_id': linked,
            'review_note_ja': detail, 'manually_selected_for_review': reviewed,
            'new_statement_id': '', 'legacy_equivalence': 'UNVERIFIED',
            'source_excerpt': row['tex_excerpt'],
        })
    if len(rows) != 102 or len(named) != 9:
        raise ValueError('Source candidate inventory changed; manual re-review required')
    counts = {status: sum(r['review_status'] == status for r in results)
              for status in sorted({r['review_status'] for r in results})}
    summary = {
        'phase': '163 R4-R19', 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'syntactic_candidates': len(results), 'existing_integrated_records': len(known),
        'category_counts': counts,
        'reviewed_examples': sum(r['manually_selected_for_review'] for r in results),
        'unresolved_candidates': counts.get('NEEDS_FULL_TEXT_REVIEW', 0) + counts.get('UNRESOLVED_CONTEXT', 0),
        'new_statement_ids_assigned': 0, 'existing_ids_modified': 0,
        'printed_original_verified': 0, 'legacy_equivalence_verified': 0,
        'search_connected': 0, 'exhaustive_semantic_review': False,
    }
    return results, summary


def run(source: Path, output: Path) -> dict:
    rows, summary = audit(source)
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'equation_review.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R4-R19 — 第1章 数式と独立主張の照合', '',
             '候補102箇所を既存24件の登録レコードと照合した。数式候補数は独立命題数ではない。',
             '分類した行は添付 TeX の内容に基づく個別の予備判定であり、原典・数学的同一性の検証ではない。',
             '', '## 集計', '']
    lines.extend(f'- {k}: {v}' for k,v in summary['category_counts'].items())
    lines.extend(['', '## 独立登録候補（正式登録前）', ''])
    lines.extend(f"- TeX {r['start_line']}行: {r['review_note_ja']}" for r in rows if r['review_status'] == 'INDEPENDENT_CANDIDATE')
    lines.extend(['', '## 未完了', '',
                  '本文・インライン式の全文照合、命題内部の成分分割、67成分との数学的同一性、印刷原典照合。',
                  '新規 ID 発行・ProofRepository 変更・証明探索接続はいずれも行わない。',
                  '全体 pytest は Phase 163 終了時のみ実施する。', ''])
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    return summary


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--source', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(run(args.source, args.output), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
