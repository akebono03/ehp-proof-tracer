from __future__ import annotations
import ast
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_renderer_architecture_audit_output'
FILES = (
 'web_group_proof.py', 'phase164_r5_r2_common_replay.py', 'toda_group_proof_presentation.py',
 'toda_group_proof_narrative_renderer.py', 'toda_group_proof_generic_narrative_renderer.py',
 'toda_group_proof_narrative_reason_renderer.py','toda_group_proof_narrative_reasons.py',
 'toda_group_proof_narrative_semantics.py','toda_group_proof_narrative_references.py',
 'toda_group_proof_narrative_contribution_renderer.py','toda_group_proof_narrative_blocks.py',
 'toda_group_proof_narrative_arguments.py','toda_group_proof_narrative_argument_multi_renderer.py',
 'toda_group_proof_narrative_classifier.py','toda_group_proof_narrative_exactness_method_renderer.py',
 'toda_group_proof_narrative_transport_link.py','phase164_r9_narrative_contract.py',
 'toda_group_proof_outline_renderer.py','toda_group_proof_narrative_provenance_catalog.py',
 'toda_group_proof_narrative_aggregate_semantics.py',
)
FOCUS = ('render_toda_group_proof_narrative_markdown',
 'render_toda_group_proof_narrative_multi_argument_with_contributions_markdown',
 'insert_toda_group_proof_narrative_reason_prose',
 'build_toda_group_proof_narrative_reason_sidecar',
 'build_toda_group_proof_narrative_reference_entries',
 'filter_toda_group_proof_narrative_reference_entries_by_body_usage',
 'build_standard_web_group_proof_view')
KEYWORDS = ('reference','reason','normalize','suppress','specialize','reorder','order_', 'exactness','stable','render','link_')

def direct_calls(node):
    result=[]
    for descendant in ast.walk(node):
        if isinstance(descendant,ast.Call):
            f=descendant.func
            if isinstance(f,ast.Name): result.append({'name':f.id,'line':descendant.lineno})
            elif isinstance(f,ast.Attribute): result.append({'name':f.attr,'line':descendant.lineno})
    return result

def main():
    OUT.mkdir(exist_ok=True)
    records={}; all_defs=defaultdict(list); edges=[]
    for file in FILES:
        path=ROOT/file
        record={'exists':path.exists()}
        records[file]=record
        if not path.exists(): continue
        try:
            source=path.read_text(encoding='utf-8-sig')
            tree=ast.parse(source,filename=file)
        except (OSError,SyntaxError,UnicodeError) as ex:
            record['parse_error']=str(ex);continue
        lines=source.splitlines()
        record['line_count']=len(lines)
        defs=[]; imports=[]; duplicate=[]
        for n in tree.body:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                obj={'name':n.name,'type':type(n).__name__,'line':n.lineno,'end_line':n.end_lineno}
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    obj['calls']=direct_calls(n)
                    obj['feature_calls']=[c for c in obj['calls'] if any(k in c['name'].lower() for k in KEYWORDS)]
                    for c in obj['calls']:
                        edges.append({'from':f'{file}:{n.name}@{n.lineno}','to':c['name'],'line':c['line']})
                defs.append(obj)
                all_defs[n.name].append({'file':file,'line':n.lineno,'type':obj['type']})
            elif isinstance(n,ast.ImportFrom):
                imports.append({'module':n.module,'symbols':[x.name for x in n.names],'line':n.lineno})
        count=Counter(d['name'] for d in defs)
        duplicates={k:v for k,v in count.items() if v>1}
        record.update({'top_level_definitions':defs,'duplicate_top_level_names':duplicates,'imports':imports,
                       'indicators':{term:sum(term in ln for ln in lines) for term in ('ReasonSidecar','render_toda_group_proof_narrative_markdown','filter_toda_group_proof_narrative_reference_entries_by_body_usage','normalize_public_narrative_contract')}})
    global_multi={k:v for k,v in all_defs.items() if len(v)>1}
    same_file={file:rec.get('duplicate_top_level_names',{}) for file,rec in records.items() if rec.get('duplicate_top_level_names')}
    tests=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'tests').glob('test_*.py') if any(x in p.name.lower() for x in ('renderer','reason','reference','narrative','web_group','phase165_r14_r4','pi3_2','exactness')) ) if (ROOT/'tests').exists() else []
    data={'phase':'165 renderer architecture audit','mode':'READ_ONLY_AST_STATIC_AUDIT','scope':list(FILES),'files':records,
          'intra_file_duplicate_definitions':same_file,'cross_file_name_matches':global_multi,
          'call_edges':edges,'selected_existing_tests':tests,'production_files_modified':False,'pytest_run':False,
          'limitations':['AST call edges are syntactic; dynamic dispatch and branch feasibility are not proven.',
                         'Function definitions earlier in the same scope may remain reachable through aliases.',
                         'This report does not certify mathematical correctness or final Web output.']}
    (OUT/'audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    md=['# Phase 165 共通 Renderer 全体監査','','## Scope and limits',
        '読み取り専用 AST 監査。動的な実行順序、数学的正当性、Web 出力の完全性は別途実行時検証が必要。','',
        '## ファイル別機能と呼び出し','']
    for file,rec in records.items():
        md.extend([f'### `{file}`',f'- 存在: {rec["exists"]}'])
        if 'parse_error' in rec:md.append(f'- 解析エラー: `{rec["parse_error"]}`')
        if 'top_level_definitions' in rec:
            md.append(f'- 行数: {rec["line_count"]} / トップレベル定義: {len(rec["top_level_definitions"])}')
            if rec['duplicate_top_level_names']:md.append(f'- **同名再定義: {rec["duplicate_top_level_names"]}**')
            for d in rec['top_level_definitions']:
                if d['type']!='ClassDef' and (d['name'] in FOCUS or any(x in d['name'].lower() for x in ('reference','reason','render','normaliz','exactness','reorder','stable'))):
                    feat=', '.join(f'{x["name"]}@{x["line"]}' for x in d.get('feature_calls',[])[:24]);md.append(f'- `{d["name"]}` L{d["line"]}–{d["end_line"]}; relevant calls: {feat or "(none detected)"}')
        md.append('')
    md.extend(['## 同名定義と優先順位（静的確認）',''])
    for file,entries in same_file.items():
        for name in entries:
            occ=[d for d in records[file]['top_level_definitions'] if d['name']==name]
            md.append(f'- `{file}` の `{name}`: '+', '.join(f'L{x["line"]}' for x in occ)+'. 通常のグローバル参照は最後の定義を参照するが、以前の関数を別名へ束縛している場合は旧実装も有効。')
    md.extend(['','## 対象テスト候補', '']+[f'- `{p}`' for p in tests]+['','## R49 / R50 の確認事項',
      '- R49: DeltaZero および MapIsomorphism の ProofStep が Sidecar に入り、理由がどこで挿入/消失するかを表示段階ごとに確認。',
      '- R50: 文献抽出 → 固定命題境界 → 使用判定 → body-consumer link → Reference section を段階ごとに確認。',
      '- 実装変更前に同名再定義と後段の正規化で意味情報が消えるか検証。',
      '- 旧 Phase の特化経路を消さずに一般経路への統合可否を判断。',
      '', '## 制約', *['- '+x for x in data['limitations']]])
    (OUT/'report.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'phase':'165 Renderer Architecture Audit','mode':data['mode'],'inspected_files':len(records),'existing_files':sum(x['exists'] for x in records.values()),'same_file_duplicate_definition_files':list(same_file),'existing_test_candidates':len(tests),'report':str(OUT/'report.md'),'production_files_modified':False,'pytest_run':False},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
