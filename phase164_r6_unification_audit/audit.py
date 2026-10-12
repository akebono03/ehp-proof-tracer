from __future__ import annotations
import ast
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase164_r6_output'
CATEGORIES = {
 '01_statement_registry': ('registry', 'repository', 'statement', 'theorem_fact'),
 '02_proofstep': ('proofstep', 'proof_step', 'proof_rule', 'apply_inference', 'given'),
 '03_proof_engine': ('backward', 'inference', 'proof_reconstruction', 'proof_engine'),
 '04_replay': ('replay', 'proof_tree', 'proof_graph'),
 '05_presentation': ('presentation', 'proof_view', 'step_view'),
 '06_renderer': ('renderer', 'narrative', 'markdown'),
 '07_references': ('reference', 'citation', 'literature', 'provenance'),
 '08_web': ('web_', 'web_app', 'html'),
 '09_legacy_phase': ('phase1', 'phase_', 'legacy'),
}
ENTRY_FILES = ('web_group_proof.py', 'web_generator_proof.py', 'web_operation_query_proof.py', 'web_app.py')
GITHUB_BASELINE = {
 'proof.py':'2eb683053eaf7146bd89afbc581a386af08b8060',
 'web_group_proof.py':'e3d28d4e72a4b4aa1d2213dc064128da6bae7317',
 'web_generator_proof.py':'84bb90e6741e200cb4985a34198380a0134d54be',
 'web_operation_query_proof.py':'44136e9d73a43120e140383ee43e0c5a786c2102',
 'toda_group_proof_narrative_renderer.py':'565ccf320dd899822b8660f7ab83451b25828155',
 'phase162_web_narrative_integration.py':'d85bbcc3a149a4c72558cf5ca504d35d49b1bfdb',
}

def inspect_file(path: Path) -> dict:
    content = path.read_text(encoding='utf-8-sig')
    result = {'path':path.relative_to(ROOT).as_posix(), 'lines':len(content.splitlines()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'imports':[], 'definitions':[], 'calls':[], 'parse_error':None}
    try:
        tree=ast.parse(content,filename=str(path))
    except SyntaxError as exc:
        result['parse_error']=f'{exc.msg} at {exc.lineno}'
        return result
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            result['imports'].extend(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom):
            if node.module:result['imports'].append(node.module)
        elif isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            result['definitions'].append({'name':node.name,'line':node.lineno,'kind':type(node).__name__})
        elif isinstance(node,ast.Call):
            func=node.func
            if isinstance(func,ast.Name): result['calls'].append({'name':func.id,'line':node.lineno})
            elif isinstance(func,ast.Attribute):result['calls'].append({'name':func.attr,'line':node.lineno})
    return result

def run():
    OUT.mkdir(exist_ok=True)
    # Top-level production modules only; archived phase assets are indexed separately.
    modules=sorted(ROOT.glob('*.py'))
    records=[inspect_file(p) for p in modules]
    module_names={p.stem for p in modules}
    internal_edges=[]
    for item in records:
        for target in item['imports']:
            if target.split('.')[0] in module_names:
                internal_edges.append({'from':item['path'],'to':target.split('.')[0]+'.py'})
    test_files=sorted(p for p in ROOT.rglob('test_*.py') if not any(part.lower() in {'archive','.git','.venv','venv','__pycache__','phase164_r6_output'} for part in p.relative_to(ROOT).parts))
    test_lookup={name:[p.relative_to(ROOT).as_posix() for p in test_files if name.replace('.py','') in p.read_text(encoding='utf-8-sig',errors='replace')][:30] for name in ENTRY_FILES}
    categories={}
    for category,keys in CATEGORIES.items():
        ranked=[]
        for item in records:
            hits=[d for d in item['definitions'] if any(key in d['name'].lower() for key in keys)]
            if hits or any(key in item['path'].lower() for key in keys):
                ranked.append({'path':item['path'],'definitions':hits[:80], 'count':len(hits)})
        categories[category]=ranked
    baseline=[]
    for path,sha in GITHUB_BASELINE.items():
        candidate=ROOT/path
        baseline.append({'path':path,'github_blob_sha':sha,'local_exists':candidate.is_file(),'local_git_blob_sha':hashlib.sha1(b'blob '+str(candidate.stat().st_size).encode()+b'\0'+candidate.read_bytes()).hexdigest() if candidate.is_file() else None})
    for record in baseline:record['matches_github_blob']=record['local_git_blob_sha']==record['github_blob_sha'] if record['local_exists'] else None
    step_sites=[]
    for item in records:
        for c in item['calls']:
            if c['name'] in ('ProofStep','apply_inference_match','find_inference_match') or 'proof_replay' in c['name'].lower():step_sites.append({'file':item['path'],'line':c['line'],'call':c['name']})
    report={'phase':'164 R6','mode':'READ_ONLY_STATIC_AUDIT','timestamp_utc':datetime.now(timezone.utc).isoformat(),'production_module_count':len(records),'test_file_count':len(test_files),'parse_error_count':sum(bool(x['parse_error']) for x in records),'categories':categories,'entrypoint_related_tests':test_lookup,'internal_import_edges':internal_edges,'proofstep_and_replay_call_sites':step_sites,'github_baseline_comparison':baseline,'production_modules':records,'test_files':[p.relative_to(ROOT).as_posix() for p in test_files]}
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Phase 164 R6 全経路監査（読み取り専用）','','この報告は静的な候補の棚卸しであり、削除安全性・数学的意味・実行経路の証明ではありません。','','## 概況',f'- Production Python modules: {len(records)}',f'- Test files: {len(test_files)}',f'- Parse errors: {report["parse_error_count"]}','','## GitHub とローカル（Git blob SHA による照合）']
    for x in baseline:lines.append(f'- `{x["path"]}`: {"一致" if x["matches_github_blob"] else "差異" if x["local_exists"] else "不在"}')
    lines+=['','## 9分野の候補ファイル数']
    for category,items in categories.items():lines.append(f'- {category}: {len(items)}')
    lines+=['','## 入口と関連テスト（ファイル内の名称出現で抽出）']
    for name,tests in test_lookup.items():lines.append(f'- {name}: {len(tests)}候補 / '+(', '.join(tests[:12]) if tests else '未検出'))
    lines+=['','## 次段階への判定','- 削除許可: **なし**（依存・実行・テストを追加確認するまで保留）','- 全体 pytest: **未実行**','- 変更した既存プロジェクトコード: **なし**','- 詳細: `audit.json` の definitions / calls / imports / test_files / github_baseline_comparison を参照']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines))
if __name__=='__main__':run()
