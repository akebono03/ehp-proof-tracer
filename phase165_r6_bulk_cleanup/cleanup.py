"""Conservative, auditable cleanup of obsolete leaf test modules (Phase 165 R6)."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PHASE = re.compile(r'^test_phase(\d+)(?:_|$)')
MISSING = re.compile(r"No module named ['\"]([^'\"]+)['\"]")
HEADER = re.compile(r'^\s*_+\s+ERROR collecting\s+(.*?)\s+_+\s*$',re.M)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    output = set()
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            output.update(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom) and node.module:
            output.add(node.module)
    return output

def blocks(log: str) -> dict[str,str]:
    marks = list(HEADER.finditer(log))
    return {m.group(1).strip(): log[m.end():(marks[i+1].start() if i+1<len(marks) else len(log))] for i,m in enumerate(marks)}

def plan(root: Path, report: dict, log: str) -> dict:
    expected = report.get('error_files',[])
    if len(expected)!=380:
        raise ValueError('Expected corrected 380 error files; refusing stale input')
    failures=set(expected)
    tests=sorted((root/'tests').glob('test_*.py'))
    parsed={}
    parse_errors={}
    for path in tests:
        try:
            parsed[path.relative_to(root).as_posix()]=imports(path)
        except (UnicodeError,SyntaxError,ValueError) as ex:
            parse_errors[path.as_posix()]=str(ex)
    reverse=defaultdict(set)
    for path,names in parsed.items():
        for n in names:
            reverse[n].add(path)
    chunks=blocks(log)
    rows=[]
    for raw in sorted(failures):
        rel=raw.replace('\\','/').strip()
        path=root/rel
        stem=path.stem
        m=PHASE.match(stem)
        reasons=[]
        if not path.is_file(): reasons.append('SOURCE_NOT_FOUND')
        if not m or int(m.group(1))>=130: reasons.append('PROTECTED_MODERN_OR_NON_PHASE_TEST')
        if parse_errors: reasons.append('UNPARSEABLE_TEST_EXISTS')
        names=parsed.get(rel,set())
        block=chunks.get(raw,chunks.get(rel,''))
        missing=set(MISSING.findall(block))
        legacy_direct=sorted(n for n in names if n.startswith('repository_') and n in missing and not (root/(n.replace('.','/')+'.py')).is_file())
        if not legacy_direct: reasons.append('NO_PROVEN_DIRECT_REMOVED_REPOSITORY_MODULE')
        incoming=sorted((reverse.get(stem,set())|reverse.get('tests.'+stem,set()))-{rel})
        if incoming: reasons.append('IMPORTED_BY_OTHER_TESTS')
        if rel not in parsed: reasons.append('NOT_PARSED')
        rows.append({'path':rel,'sha256':digest(path) if path.is_file() else None,'direct_removed_modules':legacy_direct,'incoming':incoming,'decision':'REMOVE' if not reasons else 'KEEP','reasons':reasons})
    return {'scope':'Phase<130 directly imports a missing repository_* module; never imported by other tests','input_errors':len(failures),'decisions':rows,'parse_errors':parse_errors}

def apply(root: Path, data: dict, backup:Path)->int:
    selected=[r for r in data['decisions'] if r['decision']=='REMOVE']
    for r in selected:
        if digest(root/r['path'])!=r['sha256']:
            raise RuntimeError('Source file changed: '+r['path'])
        if (backup/r['path']).exists():
            raise RuntimeError('Backup collision: '+r['path'])
    for r in selected:
        target=backup/r['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(root/r['path'],target)
        if digest(target)!=r['sha256']:
            raise RuntimeError('Backup checksum mismatch: '+r['path'])
    for r in selected:
        (root/r['path']).unlink()
        r['result']='REMOVED_AFTER_BACKUP'
    return len(selected)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args()
    root=args.root.resolve()
    base=root/'phase165_r6_audit_results'/'recollection'
    report=json.loads((base/'report.json').read_text(encoding='utf-8'))
    log=(base/'collection.log').read_text(encoding='utf-8',errors='replace')
    data=plan(root,report,log)
    session=root/'phase165_r6_audit_results'/'bulk_cleanup'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    session.mkdir(parents=True,exist_ok=False)
    count=0 if args.dry_run else apply(root,data,session/'backup')
    data['removed']=count
    data['retained']=sum(r['decision']=='KEEP' for r in data['decisions'])
    data['status']='DRY_RUN' if args.dry_run else 'APPLIED'
    (session/'report.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Removed:',count,'Retained:',data['retained'])
    print('Report:',session/'report.json')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
