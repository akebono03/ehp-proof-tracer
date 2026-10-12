"""Phase 163 R4-R58: read-only registration-readiness classification."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED = {
    '(2.9)': (r'\Delta', 40, 'tex-unit:toda:ch02:0013'),
    '(2.10)': (r'\Delta^{-1}', 41, 'tex-unit:toda:ch02:0014'),
    '(4.3)': (r'\pi_i^n', 65, 'tex-unit:toda:ch04:0003'),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assess(trial, scope, boundary, *, digests=None):
    """Validate R55-57 evidence and classify archival versus semantic readiness."""
    if trial.get('phase') != '163 R4-R55' or scope.get('phase') != '163 R4-R56' or boundary.get('phase') != '163 R4-R57':
        raise ValueError('unexpected phase input')
    if trial.get('trial_definition_count') != 3 or scope.get('scope_record_count') != 3 or boundary.get('definition_count') != 3:
        raise ValueError('unexpected record count')
    for document in (trial, scope, boundary):
        for key in ('production_registry_modified', 'production_ids_allocated', 'proof_search_connected', 'original_edition_verified'):
            if document.get(key) is not False:
                raise ValueError('unsafe or incomplete source boundary: '+key)
    by_trial={item['locator']:item for item in trial['trial_items']}
    by_scope={item['locator']:item for item in scope['scope_items']}
    by_boundary={item['locator']:item for item in boundary['items']}
    if len(by_trial)!=3 or len(by_scope)!=3 or len(by_boundary)!=3 or set(by_trial)!=set(EXPECTED) or set(by_scope)!=set(EXPECTED) or set(by_boundary)!=set(EXPECTED):
        raise ValueError('input locator mismatch or duplicate')
    records=[]
    for locator,(symbol,position,unit) in EXPECTED.items():
        t,s,b=by_trial[locator],by_scope[locator],by_boundary[locator]
        common=('source_unit_id','trial_assertion_id','defined_symbol','publication_position')
        for key in common:
            if t[key]!=s[key] or s[key]!=b[key]:
                raise ValueError('identity mismatch: '+locator+' '+key)
        if t['source_unit_id']!=unit or t['publication_position']!=position or t['defined_symbol']!=symbol:
            raise ValueError('unexpected source identity: '+locator)
        if t['trial_reference_id'] == t['trial_assertion_id'] or not t['trial_reference_id'].startswith('trial:r55:'):
            raise ValueError('invalid trial-only identity')
        if t['tex_sha256']!=s['source_tex_sha256'] or t['trial_assertion_id']!=b['trial_assertion_id']:
            raise ValueError('source/identity digest mismatch')
        if s['variables']!=b['variables'] or s['domain_tex']!=b['explicit_domain_tex'] or s['codomain_tex']!=b['explicit_codomain_tex']:
            raise ValueError('scope mismatch')
        if [(c['condition_tex'],c['value_tex']) for c in s['cases']]!=[(c['condition_tex'],c['value_tex']) for c in b['explicit_cases']]:
            raise ValueError('case mismatch')
        if t['mathematical_ast_parsed'] or s['formal_mathematical_ast_parsed'] or b['mathematical_semantics_verified']:
            raise ValueError('semantic verification must not be asserted')
        if t['production_registration_applied'] or s['production_registration_applied'] or b['registration_applied']:
            raise ValueError('production registration already applied')
        if b['global_preconditions_verified'] or not b['unverified_assumptions']:
            raise ValueError('missing unresolved prerequisites')
        if not b['contextual_evidence'] or b['original_edition_verified']:
            raise ValueError('incomplete evidence boundary')
        if not s['variables'] or (locator!='(4.3)' and (not s['domain_tex'] or not s['codomain_tex'])):
            raise ValueError('missing explicit scope')
        if locator=='(4.3)' and len(s['cases'])!=3:
            raise ValueError('missing case evidence')
        records.append({
            'locator':locator,'source_unit_id':unit,'defined_symbol':symbol,
            'publication_position':position,'trial_reference_id':t['trial_reference_id'],
            'trial_assertion_id':t['trial_assertion_id'],'tex_sha256':t['tex_sha256'],
            'source_file':b['source_file'],'source_line':b['equation_source_line'],
            'metadata_complete':True,'source_grounded_content_present':True,
            'explicit_scope_evidence_present':True,'original_edition_verified':False,
            'archival_staging_status':'READY_WITH_UNVERIFIED_SEMANTICS',
            'semantic_registration_status':'BLOCKED_BY_UNVERIFIED_SEMANTICS',
            'proof_eligibility':'NOT_ELIGIBLE',
            'unresolved_semantics':list(b['unverified_assumptions']),
            'unresolved_semantics_count':len(b['unverified_assumptions']),
            'formal_mathematical_ast':False,'mathematical_equivalence_verified':False,
            'id_policy':'PRESERVE_EXISTING_IDS; TRIAL_IDS_NOT_PROMOTED; ASSIGN_ONLY_AFTER_COLLISION_CHECK',
            'production_registration_applied':False,
        })
    if len({r['trial_assertion_id'] for r in records})!=3 or len({r['publication_position'] for r in records})!=3:
        raise ValueError('duplicate identity / order')
    return {
        'phase':'163 R4-R58','mode':'READ_ONLY_REGISTRATION_READINESS',
        'input_sha256':digests or {},
        'definition_count':3,'archival_staging_ready_count':3,
        'semantic_registration_ready_count':0,'proof_eligible_count':0,
        'unresolved_semantics_count':sum(r['unresolved_semantics_count'] for r in records),
        'trial_ids_promoted_count':0,'production_ids_allocated':False,
        'production_registry_modified':False,'proof_search_connected':False,
        'original_edition_verified':False,'untouched_definition_candidate_count':16,
        'pending_other_candidates_count':237,'records':records,
    }


def write_report(result, directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    (directory/'readiness.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    columns=['locator','publication_position','source_unit_id','defined_symbol','archival_staging_status','semantic_registration_status','proof_eligibility','unresolved_semantics_count','id_policy']
    with (directory/'readiness.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns);writer.writeheader()
        for record in result['records']:
            writer.writerow({k:record[k] for k in columns})
    lines=['# Phase 163 R4-R58 正式登録準備監査','','対象：(2.9)、(2.10)、(4.3)。既存 R55-R57 の証拠記録に基づく読み取り専用の判定。','','## 結果',
           '- 原文に根拠を持つ保管候補として準備完了：3件',
           '- 数学的意味を検証済みの正式 Assertion：0件',
           '- Proof 用に利用可能：0件',
           '- 未検証事項：9件',
           '- 本番 ID 発行：0件','','## 項目別']
    for record in result['records']:
        lines.extend(['',f"### {record['locator']} {record['defined_symbol']}",f"- 文献掲載順：{record['publication_position']}",'- 出典・定義対象・TeX 内容・明示範囲：保管候補として準備完了','- 数学的意味の検証：未完了','- 未解決：'+ '／'.join(record['unresolved_semantics'])])
    lines.extend(['','## ID と利用の境界','仮 ID を正式 ID として昇格しない。既存 ID は不変。衝突検査と登録方針の確定前に本番登録しない。','メタデータ登録の準備完了は、数学的検証の完了・引用可能性・証明探索での利用を意味しない。','原本照合および全体 pytest は未実施。'])
    (directory/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--trial',required=True);parser.add_argument('--scope',required=True)
    parser.add_argument('--boundary',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args(argv)
    inputs={name:Path(getattr(args,name)) for name in ('trial','scope','boundary')}
    objects={name:json.loads(path.read_text(encoding='utf-8-sig')) for name,path in inputs.items()}
    result=assess(objects['trial'],objects['scope'],objects['boundary'],digests={name:digest(path) for name,path in inputs.items()})
    write_report(result,args.output)
    print(json.dumps({key:value for key,value in result.items() if key!='records'},ensure_ascii=False,indent=2))
    print('R4-R58 read-only readiness audit complete. Full pytest not run.')


if __name__=='__main__':
    main()
