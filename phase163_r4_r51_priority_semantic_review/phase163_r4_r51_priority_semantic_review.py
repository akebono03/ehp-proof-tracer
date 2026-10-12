"""Phase 163 R4-R51: read-only priority semantic review for Toda chapters 3 and 5."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE_NAMES = {1:'Toda_01_corrected.tex',2:'Toda_02_2(2).tex',3:'Toda_03_2(2).tex',4:'Toda_04_2(2).tex',5:'Toda_05_2(6).tex'}

# R4-R50 indices. These are editorial source-role assessments, not new theorems.
# R4-R50 role decisions and their associated evidence are left unchanged.
DECISIONS = {
    230: ('EXISTING_STATEMENT_CONTEXT', 'eta_n group fact cited from Chapter V during a proof', None),
    231: ('EXTERNAL_CITATION_CONTEXT', 'Toda bracket identity with explicit external reference in proof', None),
    238: ('DEFINITION_CANDIDATE', 'stable homotopy group G_k as direct limit', None),
    239: ('DEFINITION_COMPONENT', 'stabilization map E-infinity used with G_k', 238),
    240: ('DEFINITION_CANDIDATE', 'composition on stable homotopy groups', None),
    241: ('EXISTING_STATEMENT_CONTEXT', 'bilinearity discussed as consequence of preceding equations', 240),
    242: ('DEFINITION_COMPONENT', 'vanishing compositions required for stable Toda bracket', 243),
    243: ('DEFINITION_CANDIDATE', 'stable Toda bracket and its indeterminacy', None),
    244: ('DEFINITION_COMPONENT', 'representatives for stable Toda bracket', 243),
    245: ('DEFINITION_COMPONENT', 'stable Toda bracket formula via E-infinity', 243),
    261: ('EXISTING_STATEMENT_CONTEXT', 'degree-zero structure after numbered (5.1)', None),
    264: ('EXISTING_STATEMENT_CONTEXT', 'eta generator structure leading into Proposition 5.1', None),
    277: ('DEFINITION_CANDIDATE', 'nu_n and stable nu defined by suspending nu_4', None),
    278: ('DEFINITION_CANDIDATE', 'eta_n cubed and stable eta cubed composite', None),
    293: ('DEFINITION_CANDIDATE', 'nu_n squared and stable nu squared composition', None),
    315: ('PROOF_LOCAL_CONSTRUCTION', 'sigma_8 chosen in proof with coefficients x and y', None),
}


def review(previous: dict, catalog: dict, sources: Path) -> dict:
    if previous.get('phase') != '163 R4-R50' or previous.get('mode') != 'READ_ONLY_SCOPED_CONTEXT_REVIEW':
        raise ValueError('R4-R50 reviewed input required')
    if catalog.get('phase') != '163 R4-R47' or len(catalog.get('items', [])) != 108:
        raise ValueError('R4-R47 catalog required')
    if previous['source_sha256'] != catalog['source_sha256']:
        raise ValueError('Source digest mismatch')
    digest = hashlib.sha256(json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    if digest != previous['catalog_snapshot_sha256']:
        raise ValueError('Catalog digest mismatch')
    source_lines = {}
    for chapter, name in SOURCE_NAMES.items():
        path = sources / name
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != catalog['source_sha256'][str(chapter)]:
            raise ValueError(f'Source digest mismatch: {name}')
        source_lines[chapter] = raw.decode('utf-8-sig').splitlines()
    before = previous['review_queue']
    if len(before) != 316 or [r['r48_index'] for r in before] != list(range(1, 317)):
        raise ValueError('Incomplete review queue')
    rows = []
    for original in before:
        item = dict(original)
        index = item['r48_index']
        if item['role_decision'] == 'PENDING_MATHEMATICAL_REVIEW' and index in DECISIONS:
            role, reason, pair = DECISIONS[index]
            if item['review_level'] != 'PENDING' or item['triage_status'] != 'DISPLAY_REVIEW_REQUIRED':
                raise ValueError(f'Unexpected state at {index}')
            chapter, line = item['chapter'], item['source_line']
            if chapter not in (3,5) or not (1 <= line <= len(source_lines[chapter])):
                raise ValueError(f'Wrong source anchor: {index}')
            if item['source_anchor'] != {'chapter':chapter,'line':line,'file':SOURCE_NAMES[chapter]}:
                raise ValueError(f'Changed source anchor: {index}')
            # Require the recorded display to begin at the original line, not a nearby proof.
            tex_line = source_lines[chapter][line-1].strip()
            if not (tex_line.startswith('\\[') or tex_line.startswith('\\begin{')):
                raise ValueError(f'Not a display opener: {index}')
            item['role_decision'] = role
            item['review_note'] = reason
            item['review_level'] = 'CONTEXT_REVIEWED'
            item['paired_prose_index'] = pair
        elif index in DECISIONS:
            raise ValueError(f'Decision was already applied: {index}')
        if item['registration_decision'] != 'NOT_APPLIED' or item['original_edition_verified'] is not False:
            raise ValueError('Input registration state must be untouched')
        rows.append(item)
    statuses = dict(sorted(Counter(r['role_decision'] for r in rows).items()))
    changed = [r['r48_index'] for r in rows if r['r48_index'] in DECISIONS]
    if changed != sorted(DECISIONS):
        raise ValueError('Priority review incomplete')
    return {
        'phase':'163 R4-R51','mode':'READ_ONLY_PRIORITY_SEMANTIC_REVIEW',
        'source_sha256': catalog['source_sha256'], 'catalog_snapshot_sha256':digest,
        'registered_source_count':108,'original_candidate_count':316,
        'newly_context_reviewed_count':len(changed), 'newly_context_reviewed_indices':changed,
        'context_reviewed_count':sum(r['review_level']=='CONTEXT_REVIEWED' for r in rows),
        'pending_mathematical_review_count':statuses.get('PENDING_MATHEMATICAL_REVIEW',0),
        'role_counts':statuses, 'distinct_new_statement_count_confirmed':0,
        'registration_applied':False,'registry_modified':False,'ids_allocated':False,
        'proof_search_connected':False,'original_edition_verified':False,
        'review_queue':rows,
    }


def write_results(result: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cols=['r48_index','chapter','source_line','triage_status','role_decision','review_level','review_note','paired_prose_index','excerpt','context']
    with (out/'review_queue.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader();w.writerows(result['review_queue'])
    lines=['# Phase 163 R4-R51 重点監査','','第3章の安定群・安定 Toda bracket と第5章の生成元記法を優先確認。','',
      f'- 新たな文脈確認：{result["newly_context_reviewed_count"]} 件',
      f'- 文脈確認済み合計：{result["context_reviewed_count"]} 件',
      f'- 数学的保留：{result["pending_mathematical_review_count"]} 件',
      '- 確定済み新規命題：0 件','','## 役割別件数','']
    lines.extend(f'- {k}: {v}' for k,v in result['role_counts'].items())
    lines.extend(['','## 判断境界','','DEFINITION_CANDIDATE は定義候補であり、正式登録や原本照合の完了を意味しない。',
      'DEFINITION_COMPONENT は定義の関連式であり、別々の独立定義として登録しない。',
      'EXISTING_STATEMENT_CONTEXT と EXTERNAL_CITATION_CONTEXT は重複した文献命題として登録しない。',
      'PROOF_LOCAL_CONSTRUCTION は証明途中の補助構成である。',
      '本番 Registry、既存 catalog、TeX、Statement ID、証明探索は変更しない。全体 pytest は実行しない。',''])
    (out/'report.md').write_text('\n'.join(lines),encoding='utf-8')


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--review',required=True,type=Path)
    p.add_argument('--catalog',required=True,type=Path)
    p.add_argument('--inputs',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    result=review(json.loads(a.review.read_text(encoding='utf-8')),json.loads(a.catalog.read_text(encoding='utf-8')),a.inputs)
    write_results(result,a.output)
    print(json.dumps({k:v for k,v in result.items() if k != 'review_queue'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
