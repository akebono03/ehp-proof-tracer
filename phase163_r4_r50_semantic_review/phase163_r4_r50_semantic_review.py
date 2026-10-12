"""Phase 163 R4-R50: scoped, source-anchored read-only mathematical role review."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SOURCE_NAMES = {1:'Toda_01_corrected.tex',2:'Toda_02_2(2).tex',3:'Toda_03_2(2).tex',4:'Toda_04_2(2).tex',5:'Toda_05_2(6).tex'}

# Each decision is a reviewed statement about the *role of this passage*.
# It is not an assertion of mathematical truth or original-edition verification.
# Role and possible registration are kept separate.
PROSE_DECISIONS = {
 81: ('DEFINITION_CANDIDATE','composition of pointed homotopy classes'),
 82: ('DEFINITION_CANDIDATE','iterated suspension of a space; display 18'),
 83: ('DEFINITION_CANDIDATE','addition and inverse of suspended maps; display 22'),
 84: ('AUXILIARY_CONTEXT','identification of a quotient map in a proof'),
 85: ('PROOF_LOCAL_CONSTRUCTION','temporary map K used in a proof'),
 86: ('AUXILIARY_CONTEXT','quotient-map description used locally'),
 87: ('PROOF_LOCAL_CONSTRUCTION','temporary map H double-prime in a proof'),
 88: ('DEFINITION_CANDIDATE','reduced cone CX; display 72'),
 89: ('AUXILIARY_CONTEXT','quotient map accompanying definition of cone'),
 90: ('DEFINITION_CANDIDATE','extension of a homotopy class'),
 91: ('DEFINITION_CANDIDATE','coextension of a homotopy class'),
 92: ('AUXILIARY_CONTEXT','map recalling already defined suspension'),
 150: ('AUXILIARY_CONTEXT','notation for a reduced product'),
 151: ('AUXILIARY_CONTEXT','mapping-track fibration in local argument'),
 152: ('DEFINITION_CANDIDATE','Delta homomorphism'),
 153: ('DEFINITION_CANDIDATE','inverse Delta construction'),
 246: ('PROOF_LOCAL_CONSTRUCTION','substitution into Theorem 3.6'),
 247: ('PROOF_LOCAL_CONSTRUCTION','parameter substitution for a proof'),
 260: ('DEFINITION_CANDIDATE','subgroup pi_i^n'),
 316: ('DEFINITION_CANDIDATE','nu_4 generator; display at chapter 5 line 571'),
}

# A small sample of *display passages*, explicitly identified by R4-R49 index.
# Linked definition displays are grouped with their prose, not new source units.
DISPLAY_DECISIONS = {
 1: ('DEFINITION_CANDIDATE','unit sphere S^n'),
 4: ('DEFINITION_CANDIDATE','pointed homotopy classes [X,Y]'),
 18: ('DEFINITION_COMPONENT','iterated suspension; linked prose index 82'),
 22: ('DEFINITION_COMPONENT','addition on suspension maps; linked prose index 83'),
 24: ('DEFINITION_COMPONENT','inverse on suspension maps; linked prose index 83'),
 39: ('DEFINITION_CANDIDATE','secondary composition/Toda bracket construction'),
 72: ('DEFINITION_COMPONENT','cone formula; linked prose index 88'),
 104: ('CLAIM_IN_PROSE','reduced product induces homotopy group isomorphism'),
 105: ('EXISTING_STATEMENT_CONTEXT','specialization of preceding numbered equation (2.3)'),
}

LINKED_DISPLAY_TO_PROSE = {18:82,22:83,24:83,72:88}


def evaluate(triage: dict, catalog: dict, sources: Path) -> dict:
    if triage.get('phase') != '163 R4-R49' or catalog.get('phase') != '163 R4-R47':
        raise ValueError('Expected R4-R49 triage and R4-R47 catalog')
    queue = triage['review_queue']
    if len(queue) != 316 or [r['r48_index'] for r in queue] != list(range(1,317)):
        raise ValueError('R4-R49 queue incomplete or reordered')
    if len(catalog['items']) != 108 or catalog['source_sha256'] != triage['source_sha256']:
        raise ValueError('Catalog/source baseline changed')
    digest = hashlib.sha256(json.dumps(catalog, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    if digest != triage['catalog_snapshot_sha256']:
        raise ValueError('Catalog snapshot changed')
    source_lines = {}
    for chapter, name in SOURCE_NAMES.items():
        content = (sources / name).read_bytes()
        if hashlib.sha256(content).hexdigest() != catalog['source_sha256'][str(chapter)]:
            raise ValueError(f'Source digest changed: {name}')
        source_lines[chapter] = content.decode('utf-8-sig').splitlines()
    reviewed = []
    for row in queue:
        item = dict(row)
        index, status = row['r48_index'], row['triage_status']
        chapter, line = row['chapter'], row['source_line']
        if not (1 <= line <= len(source_lines[chapter])):
            raise ValueError('Source line out of range')
        item['source_anchor'] = {'chapter':chapter,'line':line,'file':SOURCE_NAMES[chapter]}
        item['paired_prose_index'] = LINKED_DISPLAY_TO_PROSE.get(index)
        if status in ('NESTED_DISPLAY_FRAGMENT','LEXICAL_FALSE_POSITIVE'):
            item['role_decision'] = 'LEXICALLY_EXCLUDED'
            item['review_note'] = row['reason']
            item['review_level'] = 'LEXICAL_ONLY'
        elif index in PROSE_DECISIONS:
            if status != 'DEFINITION_CUE_REVIEW_REQUIRED':
                raise ValueError('Prose decision attached to unexpected category')
            item['role_decision'], item['review_note'] = PROSE_DECISIONS[index]
            item['review_level'] = 'CONTEXT_REVIEWED'
        elif index in DISPLAY_DECISIONS:
            if status != 'DISPLAY_REVIEW_REQUIRED':
                raise ValueError('Display decision attached to unexpected category')
            item['role_decision'], item['review_note'] = DISPLAY_DECISIONS[index]
            item['review_level'] = 'CONTEXT_REVIEWED'
        else:
            item['role_decision'] = 'PENDING_MATHEMATICAL_REVIEW'
            item['review_note'] = 'No contextual adjudication made in R4-R50'
            item['review_level'] = 'PENDING'
        item['registration_decision'] = 'NOT_APPLIED'
        item['original_edition_verified'] = False
        reviewed.append(item)
    counts = dict(sorted(Counter(row['role_decision'] for row in reviewed).items()))
    return {
       'phase':'163 R4-R50','mode':'READ_ONLY_SCOPED_CONTEXT_REVIEW',
       'original_candidate_count':316,'registered_source_count':108,
       'source_sha256':catalog['source_sha256'],'catalog_snapshot_sha256':digest,
       'role_counts':counts,'context_reviewed_count':sum(r['review_level']=='CONTEXT_REVIEWED' for r in reviewed),
       'pending_mathematical_review_count':counts.get('PENDING_MATHEMATICAL_REVIEW',0),
       'distinct_new_statement_count_confirmed':0,
       'registration_applied':False,'registry_modified':False,'ids_allocated':False,
       'proof_search_connected':False,'original_edition_verified':False,'review_queue':reviewed,
    }


def write_report(result: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out/'review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    fields = ['r48_index','chapter','source_line','triage_status','role_decision','review_level','review_note','paired_prose_index','review_group_id','excerpt','context']
    with (out/'review_queue.csv').open('w',encoding='utf-8-sig',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(result['review_queue'])
    lines=['# Phase 163 R4-R50 数学的役割の限定監査','','TeX 第1〜5章の既存108登録環境と ID は変更していない。','',
           '## 判定状況','']
    for key,value in result['role_counts'].items():lines.append(f'- {key}: {value}件')
    lines += ['',f'- 前後文脈を確認した候補: {result["context_reviewed_count"]}件',
              f'- 数学的判定を保留した候補: {result["pending_mathematical_review_count"]}件',
              '- 独立した新規命題として確定した件数: 0件',
              '', '## 判定の境界','',
              'DEFINITION_CANDIDATE は定義として登録するための候補であり、本番登録や原本照合の完了を意味しない。',
              'DEFINITION_COMPONENT は同一の定義に付随する表示式で、別登録を意味しない。',
              'CLAIM_IN_PROSE は文中の主張であり、独立した文献命題として登録するかは未決定。',
              'PROOF_LOCAL_CONSTRUCTION と AUXILIARY_CONTEXT は限定された文脈に基づく役割の判断である。',
              '残りの数学的判断を行っていない数式は PENDING_MATHEMATICAL_REVIEW のまま保持する。',
              '第3章の安定群 G_k、第5章の他の生成元定義は20件の文章検出には必ずしも含まれず、表示式候補の監査で補完が必要。',
              '', 'Registry・TeX・既存 catalog・Statement ID・証明探索は変更しない。全体 pytest は未実施。','']
    (out/'report.md').write_text('\n'.join(lines),encoding='utf-8')


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--triage',type=Path,required=True)
    parser.add_argument('--catalog',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=evaluate(json.loads(args.triage.read_text(encoding='utf-8')),
                    json.loads(args.catalog.read_text(encoding='utf-8')),args.inputs)
    write_report(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k!='review_queue'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
