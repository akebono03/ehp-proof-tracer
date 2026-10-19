from pathlib import Path
import ast, hashlib, json, shutil, subprocess, sys
from datetime import datetime, timezone

ROOT = Path.cwd()
PATCHES = json.loads((Path(__file__).parent / 'patches.json').read_text(encoding='utf-8'))
REPORT = ROOT / 'phase165_r6_audit_results' / 'phase164_web_migration' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
REPORT.mkdir(parents=True, exist_ok=True)
prepared = []
for rel, info in PATCHES.items():
    path = ROOT / rel
    original = path.read_bytes()
    actual = hashlib.sha256(original).hexdigest()
    if actual != info['sha256']:
        raise SystemExit(f'STOP: source differs from audited SHA-256 for {rel}; no changes applied')
    source = original.decode('utf-8')
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    positions = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            positions[node.name] = (node.lineno, node.end_lineno)
    replacements = []
    for name, content in info['functions'].items():
        if name not in positions:
            raise SystemExit(f'STOP: function missing: {rel}:{name}; no changes applied')
        start, end = positions[name]
        replacements.append((start,end,content))
    for start,end,content in sorted(replacements,reverse=True):
        lines[start-1:end] = [content.rstrip() + '\n\n']
    new = ''.join(lines)
    ast.parse(new)
    prepared.append((rel,path,original,new))
for rel,path,original,new in prepared:
    backup = REPORT / rel
    backup.parent.mkdir(parents=True,exist_ok=True)
    backup.write_bytes(original)
    path.write_text(new,encoding='utf-8')
    print('PATCHED:',rel)
(REPORT/'report.json').write_text(json.dumps({'modified_files':[item[0] for item in prepared],'backup':str(REPORT),'full_pytest_run':False},indent=2),encoding='utf-8')
print('BACKUP:',REPORT)
cmd=[sys.executable,'-m','pytest','-q',*PATCHES.keys()]
result=subprocess.run(cmd,cwd=ROOT)
print('Phase164 limited pytest exit:',result.returncode,'; full pytest NOT run')
raise SystemExit(result.returncode)
