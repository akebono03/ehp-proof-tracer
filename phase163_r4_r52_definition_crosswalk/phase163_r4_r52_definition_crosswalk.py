"""Phase 163 R4-R52: read-only crosswalk for definition candidates and R4-R47 snapshot."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE_NAMES = {1: 'Toda_01_corrected.tex', 2: 'Toda_02_2(2).tex', 3: 'Toda_03_2(2).tex', 4: 'Toda_04_2(2).tex', 5: 'Toda_05_2(6).tex'}
# Editorial labels, not Statement IDs. Keep R4-R48 index as immutable audit trace.
LABELS = {
    1: 'unit_sphere', 4: 'pointed_homotopy_classes', 39: 'secondary_composition',
    81: 'composition_homotopy_classes', 82: 'iterated_suspension',
    83: 'addition_inverse_suspension', 88: 'reduced_cone', 90: 'extension',
    91: 'coextension', 152: 'delta_homomorphism', 153: 'inverse_delta',
    238: 'stable_homotopy_group', 240: 'stable_composition',
    243: 'stable_toda_bracket', 260: 'pi_i_n_subgroup',
    277: 'nu_n_notation', 278: 'eta_n_cubed_notation',
    293: 'nu_n_squared_notation', 316: 'nu4_generator_notation',
}


def catalog_digest(catalog: dict) -> str:
    return hashlib.sha256(json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def audit(review: dict, catalog: dict, inputs: Path) -> dict:
    if review.get('phase') != '163 R4-R51' or review.get('mode') != 'READ_ONLY_PRIORITY_SEMANTIC_REVIEW':
        raise ValueError('R4-R51 review required')
    if catalog.get('phase') != '163 R4-R47' or catalog.get('item_count') != 108 or len(catalog.get('items', [])) != 108:
        raise ValueError('R4-R47 catalog required')
    if review.get('catalog_snapshot_sha256') != catalog_digest(catalog):
        raise ValueError('Catalog snapshot mismatch')
    if review.get('source_sha256') != catalog.get('source_sha256'):
        raise ValueError('Source snapshots differ')
    for chapter, name in SOURCE_NAMES.items():
        path = inputs / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != catalog['source_sha256'][str(chapter)]:
            raise ValueError(f'TeX file changed: {name}')
    rows = review.get('review_queue', [])
    if len(rows) != 316 or [r['r48_index'] for r in rows] != list(range(1, 317)):
        raise ValueError('R4-R51 review queue incomplete')
    if review.get('pending_mathematical_review_count') != 237:
        raise ValueError('Unexpected pending review count')
    if sum(r['role_decision'] == 'DEFINITION_CANDIDATE' for r in rows) != 19:
        raise ValueError('Definition candidate count changed')
    # The R4-R47 catalog is a frozen export of the existing bridge. Its assertion IDs
    # are currently statement-kind records; never infer an equivalent definition ID.
    refs = catalog.get('existing_reference_ids', [])
    assertions = catalog.get('existing_assertion_ids', [])
    if len(refs) != 23 or len(assertions) != 67 or len(refs) != len(set(refs)) or len(assertions) != len(set(assertions)):
        raise ValueError('Unexpected Registry snapshot')
    if any(not isinstance(v, str) or not v for v in refs + assertions):
        raise ValueError('Invalid Registry snapshot ID')
    if any(r.startswith('toda:Definition ') for r in refs):
        raise ValueError('Definition reference found: requires direct matching review')
    if review.get('registration_applied') is not False or review.get('ids_allocated') is not False:
        raise ValueError('Prior registration state is not read-only')
    by_index = {r['r48_index']: r for r in rows}
    actual = {r['r48_index'] for r in rows if r['role_decision'] == 'DEFINITION_CANDIDATE'}
    if actual != set(LABELS):
        raise ValueError('Definition candidate identity changed')
    # R4-R47 recorded source units and existing references separately. None of these
    # prose/display definition anchors has a direct registered Definition locator.
    result_rows = []
    for index, label in sorted(LABELS.items(), key=lambda item: (by_index[item[0]]['chapter'], by_index[item[0]]['source_line'], item[0])):
        row = by_index[index]
        chapter = row['chapter']
        line = row['source_line']
        if row['review_level'] != 'CONTEXT_REVIEWED' or row.get('registration_decision') != 'NOT_APPLIED':
            raise ValueError(f'Candidate {index} has invalid review state')
        if row.get('original_edition_verified') is not False:
            raise ValueError(f'Candidate {index} claims edition verification')
        if row['source_anchor'] != {'chapter': chapter, 'line': line, 'file': SOURCE_NAMES[chapter]}:
            raise ValueError(f'Candidate {index} has changed anchor')
        raw_lines = (inputs / SOURCE_NAMES[chapter]).read_text(encoding='utf-8-sig').splitlines()
        if not (1 <= line <= len(raw_lines)):
            raise ValueError(f'Candidate {index} is outside its source')
        # Preserve original excerpt/context as evidence; do not silently normalize TeX.
        if row['original_category'] == 'PROSE_DEFINITION_CUE':
            if raw_lines[line - 1].strip() != row['excerpt'].strip():
                raise ValueError(f'Prose source anchor differs: {index}')
        elif row['original_category'] == 'OUTSIDE_DISPLAY':
            if not raw_lines[line - 1].strip().startswith('\\['):
                raise ValueError(f'Display source anchor differs: {index}')
        else:
            raise ValueError(f'Invalid candidate category: {index}')
        related = [r['r48_index'] for r in rows if r.get('paired_prose_index') == index and r['role_decision'] == 'DEFINITION_COMPONENT']
        result_rows.append({
            'r48_index': index, 'chapter': chapter, 'source_line': line,
            'editorial_key': label, 'role_decision': row['role_decision'],
            'source_file': SOURCE_NAMES[chapter], 'excerpt': row['excerpt'],
            'context': row['context'], 'component_indices': related,
            'direct_definition_reference_id': None, 'direct_definition_assertion_id': None,
            'direct_match_status': 'NO_REGISTERED_DEFINITION_ENTRY_IN_R47_SNAPSHOT',
            'semantic_overlap_status': 'UNRESOLVED_REVIEW_REQUIRED',
            'new_registration_status': 'NOT_DECIDED',
            'original_edition_verified': False,
        })
    return {
        'phase': '163 R4-R52', 'mode': 'READ_ONLY_DEFINITION_CROSSWALK',
        'catalog_snapshot_sha256': catalog_digest(catalog),
        'source_sha256': catalog['source_sha256'],
        'registered_source_count': len(catalog['items']),
        'existing_reference_count': len(refs), 'existing_assertion_count': len(assertions),
        'definition_candidate_count': len(result_rows),
        'direct_definition_match_count': 0,
        'semantic_overlap_unresolved_count': len(result_rows),
        'pending_mathematical_review_count': review['pending_mathematical_review_count'],
        'definition_component_count': sum(r['role_decision'] == 'DEFINITION_COMPONENT' for r in rows),
        'distinct_new_statement_count_confirmed': 0,
        'registry_snapshot_only': True, 'live_registry_verified': False,
        'registration_applied': False, 'registry_modified': False,
        'ids_allocated': False, 'proof_search_connected': False,
        'original_edition_verified': False, 'candidates': result_rows,
    }


def write_results(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / 'crosswalk.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    columns = ['r48_index', 'chapter', 'source_line', 'editorial_key', 'source_file', 'direct_match_status',
               'semantic_overlap_status', 'new_registration_status', 'component_indices', 'excerpt', 'context']
    with (output / 'crosswalk.csv').open('w', newline='', encoding='utf-8-sig') as fp:
        writer = csv.DictWriter(fp, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        for item in result['candidates']:
            writer.writerow({**item, 'component_indices': ','.join(map(str, item['component_indices']))})
    lines = ['# Phase 163 R4-R52 定義候補の既存台帳照合', '',
             'R4-R47 の Registry スナップショットを用いた読み取り専用照合。現行 Registry の再取得は行っていない。', '',
             f'- 既存 Reference: {result["existing_reference_count"]} 件',
             f'- 既存 Assertion: {result["existing_assertion_count"]} 件',
             f'- 定義候補: {result["definition_candidate_count"]} 件',
             '- 登録済み Definition への直接一致: 0 件（R4-R47 スナップショット上）',
             '- 内容の重複判定が必要: 19 件',
             '- 新規登録確定: 0 件',
             f'- 数学的判定保留: {result["pending_mathematical_review_count"]} 件', '',
             '## 候補（章・TeX 行番号・監査用キー）', '']
    lines.extend(f'- 第{x["chapter"]}章 L{x["source_line"]}: {x["editorial_key"]} (R4-R48 #{x["r48_index"]})' for x in result['candidates'])
    lines += ['', '## 判断境界', '',
              '既存の主張 Assertion と数学的内容が重複する可能性は否定していない。',
              '監査用キーは Statement ID ではない。新規 ID・Reference・Assertion は発行しない。',
              '第1〜5章 TeX、既存108環境、Registry、証明探索に変更は加えない。',
              '原本照合および全体 pytest は実施していない。', '']
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--review', required=True, type=Path)
    parser.add_argument('--catalog', required=True, type=Path)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.review.read_text(encoding='utf-8')),
                   json.loads(args.catalog.read_text(encoding='utf-8')), args.inputs)
    write_results(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != 'candidates'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
