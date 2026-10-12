"""Phase 163 R4-R57: read-only source-evidenced condition boundary audit."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

SOURCE_FILES = {'(2.9)': 'Toda_02_2(2).tex', '(2.10)': 'Toda_02_2(2).tex', '(4.3)': 'Toda_04_2(2).tex'}

# These are local source passages, not globally established mathematical hypotheses.
CONTEXT_RULES = {
    '(2.9)': (
        ('DENOMINATOR_PROPERTY', r'\partial\Ker(h_{m*})', r'm\) が奇数または \(i<3m-1\)',
         '商の分母の自明性に関する場合分け。Delta 全体の適用条件ではない。'),
    ),
    '(2.10)': (
        ('KERNEL_STATEMENT', r'H\pi_{i+1}(S^{m+1})', r'\Delta\) の kernel',
         '核の説明であって、Delta^{-1} の全域的可逆性の証明ではない。'),
    ),
    '(4.3)': (
        ('SURROUNDING_NOTATION', r'\pis{i}{S^n;p}', r'p$-成分',
         '周辺の p-成分の記法説明。式 (4.3) の場合分けとは別に保持する。'),
    ),
}
UNVERIFIED = {
    '(2.9)': ('m,i の量化と値域', 'Delta の全域的な定義可能範囲', '記号 (h_{m*})^{-1} の意味・存在・一意性'),
    '(2.10)': ('m,i の量化と値域', 'Delta^{-1} の逆写像としての存在・一意性', '記号 Omega_1^{-1} と partial^{-1} の意味'),
    '(4.3)': ('i,n の量化と値域', 'E^{-1} の逆像／逆写像としての厳密な意味', '3場合の重複・網羅性の形式的検証'),
}

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _source_evidence(lines, marker, expected, label):
    for number, line in enumerate(lines, start=1):
        if expected in line and any(marker in previous for previous in lines[max(0, number-3):number]):
            return {'source_line': number, 'source_text': line.strip(), 'status': label}
    raise ValueError('missing source evidence: '+marker+' / '+expected)


def build_boundary_report(scope, sources, *, scope_digest=None):
    if scope.get('phase') != '163 R4-R56' or scope.get('scope_record_count') != 3:
        raise ValueError('unexpected R56 input')
    if any(scope.get(k) for k in ('production_registry_modified','production_ids_allocated','proof_search_connected')):
        raise ValueError('input has production mutations')
    items=scope['scope_items']
    if {i['locator'] for i in items} != set(SOURCE_FILES) or len(items)!=3:
        raise ValueError('unexpected definition set')
    entries=[]
    for item in items:
        locator=item['locator']
        file_name=SOURCE_FILES[locator]
        if item['source_file'] != file_name or item['formal_mathematical_ast_parsed'] or item['production_registration_applied']:
            raise ValueError('source identity or boundary mismatch: '+locator)
        if item['scope_status'] != 'SOURCE_TEX_EXPLICIT_NOT_FORMAL_AST':
            raise ValueError('scope status changed: '+locator)
        if file_name not in sources:
            raise ValueError('missing TeX source: '+file_name)
        lines=sources[file_name].splitlines()
        start=item['equation_source_line']
        if start<1 or start>len(lines) or ('label{'+locator[1:-1]+'}' not in lines[start-1]):
            raise ValueError('equation line mismatch: '+locator)
        # Explicit conditions remain exact R56 extracts; do not infer quantifiers.
        cases=[]
        for case in item['cases']:
            evidence=_source_evidence(lines,case['condition_tex'],case['value_tex'],'EXPLICIT_CASE_IN_EQUATION')
            cases.append({'condition_tex':case['condition_tex'],'value_tex':case['value_tex'],**evidence})
        contextual=[]
        for kind,marker,expected,note in CONTEXT_RULES[locator]:
            evidence=_source_evidence(lines,marker,expected,'CONTEXTUAL_NOT_GLOBAL_PRECONDITION')
            contextual.append({'kind':kind,'note':note,**evidence})
        entry={
            'locator':locator,'source_file':file_name,'source_unit_id':item['source_unit_id'],
            'trial_assertion_id':item['trial_assertion_id'],'defined_symbol':item['defined_symbol'],
            'publication_position':item['publication_position'],
            'equation_source_line':start,'variables':item['variables'],
            'explicit_domain_tex':item['domain_tex'],'explicit_codomain_tex':item['codomain_tex'],
            'explicit_cases':cases,'contextual_evidence':contextual,
            'unverified_assumptions':list(UNVERIFIED[locator]),
            'global_preconditions_verified':False,
            'mathematical_semantics_verified':False,
            'original_edition_verified':False,
            'source_sha256':hashlib.sha256(sources[file_name].encode('utf-8')).hexdigest(),
            'registration_applied':False,
        }
        entries.append(entry)
    return {
        'phase':'163 R4-R57','mode':'READ_ONLY_EXPLICIT_CONTEXTUAL_UNVERIFIED_BOUNDARY',
        'r56_input_sha256':scope_digest,
        'definition_count':len(entries),
        'explicit_case_count':sum(len(x['explicit_cases']) for x in entries),
        'contextual_evidence_count':sum(len(x['contextual_evidence']) for x in entries),
        'unverified_assumption_count':sum(len(x['unverified_assumptions']) for x in entries),
        'global_preconditions_verified_count':0,
        'mathematical_ast_count':0,'untouched_definition_candidate_count':scope['untouched_candidate_count'],
        'pending_other_candidates_count':scope['pending_other_candidates_count'],
        'production_registry_modified':False,'production_ids_allocated':False,
        'proof_search_connected':False,'original_edition_verified':False,'items':entries,
    }


def write_report(result, directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    (directory/'boundary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    columns=['locator','source_file','publication_position','defined_symbol','equation_source_line','explicit_cases','contextual_evidence','unverified_assumptions','global_preconditions_verified']
    with (directory/'boundary.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns);writer.writeheader()
        for item in result['items']:
            writer.writerow({k:json.dumps(item[k],ensure_ascii=False) if isinstance(item[k],list) else item[k] for k in columns})
    text=['# Phase 163 R4-R57 条件の根拠境界監査','',
          '対象：(2.9)、(2.10)、(4.3)。出典は現在の TeX であり原本照合済みとはしない。','',
          '## 集計',
          f"- 定義：{result['definition_count']}件",
          f"- 明示の場合分け：{result['explicit_case_count']}件",
          f"- 周辺文脈の根拠：{result['contextual_evidence_count']}件",
          f"- 未検証の仮定：{result['unverified_assumption_count']}件",'']
    for item in result['items']:
        text.extend([f"## {item['locator']} {item['defined_symbol']}",
                     f"- TeX: {item['source_file']}、式開始行 {item['equation_source_line']}",
                     f"- 明示の場合分け：{len(item['explicit_cases'])}件",])
        for e in item['contextual_evidence']:
            text.append(f"- 文脈情報 L{e['source_line']}：{e['note']}")
        for a in item['unverified_assumptions']:
            text.append(f'- 未検証：{a}')
        text.append('')
    text.extend(['本番台帳、Statement ID、証明探索には変更を加えない。',
                 '量化範囲、逆写像の存在、数学的同値性、原本との照合は未検証。','全体 pytest は実施しない。',''])
    (directory/'report.md').write_text('\n'.join(text),encoding='utf-8')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--scope',required=True)
    parser.add_argument('--sources',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    scope=json.loads(Path(args.scope).read_text(encoding='utf-8'))
    sources={name:(Path(args.sources)/name).read_text(encoding='utf-8') for name in set(SOURCE_FILES.values())}
    result=build_boundary_report(scope,sources,scope_digest=sha256(args.scope))
    write_report(result,args.output)
    print(json.dumps({k:v for k,v in result.items() if k!='items'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
