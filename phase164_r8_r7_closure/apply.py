"""Phase 164 R8-R7: guarded generic ProofStep replace closure and residual audit."""
from __future__ import annotations

import ast
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ARCHIVE = json.loads((HERE / 'r8_r6_replace_sites.json').read_text(encoding='utf-8'))
FACTORY = 'phase164_r8_proofstep_factory.py'
RENDERER = 'toda_group_proof_narrative_contribution_renderer.py'
FUNCTION = '_phase157_r20_specialize_reference_value'
OLD = '  return replace(\n    value,\n    **changes,\n  )'
NEW = '''  if isinstance(value, ProofStep):
    return replace_legacy_proof_step_fields(value, **changes)

  return replace(
    value,
    **changes,
  )'''
ADDITION = '''\n\ndef replace_legacy_proof_step_fields(step: ProofStep, **changes) -> ProofStep:
    """Route a legacy dataclass projection through the common factory.

    This retains the old rule and provenance status. It does not validate a
    substituted conclusion and must not be used to claim a new inference.
    """
    from dataclasses import fields, replace
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    allowed = {field.name for field in fields(ProofStep)}
    if not set(changes).issubset(allowed):
        raise TypeError("unknown ProofStep field")
    if "rule" in changes and changes["rule"] is not step.rule:
        raise ValueError("legacy projection must preserve proof rule")
    return replace(step, **changes)
'''


def _function(tree, name):
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(nodes) != 1:
        raise ValueError(f'exactly one function {name} required')
    return nodes[0]


def _import_append(src):
    tree = ast.parse(src)
    nodes = [n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == 'phase164_r8_proofstep_factory']
    if len(nodes) != 1 or not any(a.name == 'project_reference_component_step' for a in nodes[0].names):
        raise ValueError('expected R8-R6 renderer factory import')
    node = nodes[0]
    lines = src.splitlines(keepends=True)
    lines.insert(node.end_lineno, '\nfrom phase164_r8_proofstep_factory import (\n    replace_legacy_proof_step_fields,\n)\n')
    return ''.join(lines)


def prepare(root):
    old = {}
    out = {}
    for name in (FACTORY, RENDERER):
        blob = (root / name).read_bytes()
        src = blob.decode('utf-8-sig').replace('\r\n', '\n')
        ast.parse(src)
        old[name] = blob
        out[name] = src
    if 'def replace_legacy_proof_step_fields(' in out[FACTORY]:
        raise ValueError('R8-R7 factory helper already exists')
    if 'def project_reference_component_step(' not in out[FACTORY]:
        raise ValueError('R8-R6 factory migration missing')
    out[FACTORY] += ADDITION
    tree = ast.parse(out[RENDERER]); fn = _function(tree, FUNCTION)
    lines = out[RENDERER].splitlines(keepends=True)
    scope = ''.join(lines[fn.lineno-1:fn.end_lineno])
    if scope.count(OLD) != 1 or out[RENDERER].count(OLD) != 1:
        raise ValueError('generic dataclass replacement changed; abort')
    out[RENDERER] = _import_append(out[RENDERER].replace(OLD, NEW, 1))
    for name in out:
        ast.parse(out[name])
        newline = '\r\n' if b'\r\n' in old[name] else '\n'
        out[name] = out[name].replace('\n', newline).encode('utf-8')
    return old, out


def _all_replaces(root):
    grouped = defaultdict(list)
    for site in ARCHIVE:
        if site['r8_r6_classification'] == 'proofstep_reconstruction_migrate':
            continue
        grouped[site['file']].append(site)
    result = []
    for name, expected in sorted(grouped.items()):
        tree = ast.parse((root / name).read_text(encoding='utf-8-sig'), filename=name)
        calls = sorted((n for n in ast.walk(tree) if isinstance(n, ast.Call) and
                        ((isinstance(n.func, ast.Name) and n.func.id == 'replace') or
                         (isinstance(n.func, ast.Attribute) and n.func.attr == 'replace'))),
                       key=lambda n: (n.lineno, n.col_offset))
        expected.sort(key=lambda x: (x['line'], x['function']))
        if len(calls) != len(expected):
            raise ValueError(f'{name}: residual replace site drift: {len(calls)} vs {len(expected)}')
        for call, site in zip(calls, expected):
            if isinstance(call.func, ast.Attribute):
                category = 'METHOD_REPLACE_NOT_DATACLASS'
            elif name == RENDERER and site['function'] == FUNCTION and site['line'] == 1117:
                category = 'GENERIC_REPLACE_GUARDED_PROOFSTEP_BRANCH'
            elif name == RENDERER and site['function'] == FUNCTION and site['line'] == 1037:
                category = 'SCALARSUM_TYPE_GUARDED'
            elif name == RENDERER and site['function'] == '_phase157_r20_specialize_reference_value':
                raise ValueError('unknown generic replace in recursive specialization')
            else:
                category = 'NON_PROOFSTEP_DOMAIN_DATACLASS'
            result.append({'file': name, 'original_line': site['line'], 'current_line': call.lineno,
                           'function': site['function'], 'category': category,
                           'argument': ast.unparse(call.args[0]) if call.args else None})
    if len(result) != 65:
        raise ValueError(f'expected 65 residual replace matches, got {len(result)}')
    return result


def _scope_counter(root):
    from collections import Counter
    core = ast.parse((root / 'proof.py').read_text(encoding='utf-8-sig'))
    constructors = sum(1 for n in ast.walk(core) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'ProofStep')
    inference = sum(1 for n in ast.walk(core) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'apply_inference_match')
    if (constructors, inference) != (8, 2):
        raise ValueError(f'proof.py engine changed: {(constructors, inference)}')
    return {'typed_core_constructors': constructors, 'core_inference_delegations': inference,
            'core_total': constructors + inference, 'core_exemption_reason': 'proof.py is the dependency root; its validated constructors and inference runners cannot depend on an importing factory'}


def _code_report(out):
    blocks = ['# Phase 164 R8-R7 変更コード全文', '']
    wanted = {FACTORY: ['replace_legacy_proof_step_fields'], RENDERER: [FUNCTION]}
    for name, funcs in wanted.items():
        src = out[name].decode('utf-8')
        tree = ast.parse(src); lines = src.splitlines()
        imports = '\n'.join('\n'.join(lines[n.lineno-1:n.end_lineno]) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)))
        blocks.extend([f'## {name}', '', '### import 全文', '', f'```python\n{imports}\n```', '', '### 変更した関数全文', ''])
        for func in funcs:
            node = _function(tree, func)
            blocks.extend([f'```python\n' + '\n'.join(lines[node.lineno-1:node.end_lineno]) + '\n```', ''])
    return '\n'.join(blocks)


def scan_unmigrated(root):
    """Narrow productive audit; exclude tooling, backups, tests and factory itself."""
    excluded_prefix = ('apply_', 'audit_', 'diagnose_', 'debug_', 'fix_', 'run_', 'probe_', 'inspect_', 'test_', 'check_', 'migrate_', 'patch_')
    excluded_middle = ('_backup', '_bak', '_old', '_before_apply', '_pre_change', '_snapshot')
    residual = []
    for path in sorted(root.glob('*.py')):
        if path.name in ('proof.py', FACTORY) or path.name.startswith(excluded_prefix) or any(t in path.name for t in excluded_middle):
            continue
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=path.name)
        aliases = {'ProofStep', 'apply_inference_match'}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'proof':
                aliases |= {a.asname for a in node.names if a.name in ('ProofStep', 'apply_inference_match') and a.asname}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id in aliases:
                residual.append({'file':path.name,'line':node.lineno,'call':node.func.id})
    return residual


def run(root, dry_run=False):
    root = Path(root)
    old, out = prepare(root)
    sites = _all_replaces(root)
    core = _scope_counter(root)
    if scan_unmigrated(root):
        raise ValueError('unmigrated direct production ProofStep calls remain: '+repr(scan_unmigrated(root)[:10]))
    if dry_run:
        return {'dry_run':True,'changed_files':list(out),'replace_sites':len(sites),
                'core_engine_sites':core['core_total'], 'guarded_generic_sites':1}
    backup = root / ('phase164_r8_r7_backup_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.mkdir(exist_ok=False)
    for name, blob in old.items():
        (backup / name).write_bytes(blob)
    wrote = []
    try:
        for name, blob in out.items():
            if (root / name).read_bytes() != old[name]:
                raise ValueError(f'{name} changed during migration')
            (root/name).write_bytes(blob)
            wrote.append(name)
        # All production direct constructors (outside foundation and factory) must remain absent.
        residual = scan_unmigrated(root)
        if residual:
            raise ValueError(f'unmigrated ProofStep site: {residual[:5]}')
    except Exception:
        for name in wrote:
            (root/name).write_bytes(old[name])
        raise
    status = {'phase':'164 R8-R7','status':'R8_FACTORY_ROUTING_CLOSED_WITH_LEGACY_PROVENANCE_LIMITATION',
              'r8_factory_routing_closed': True, 'mathematical_certification_closed':False,
              'changed_files':list(out),'backup_dir':str(backup), 'replace_site_count':65,
              'replace_classification':dict(Counter(s['category'] for s in sites)),
              'core_engine':core,'unmigrated_direct_production_calls':0,
              'full_pytest_run':False,
              'limitations':['Legacy GIVEN/INFERENCE centralization is not proof certification',
                             'This AST scan covers root production files with the established exclusions; indirect/dynamic aliases require separate runtime checks',
                             'Generic projection of a ProofStep retains legacy status and is not derivation']}
    output = root/'phase164_r8_r7_output'; output.mkdir(exist_ok=True)
    (output/'audit.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'replace_sites.json').write_text(json.dumps(sites,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output/'CHANGED_CODE.md').write_text(_code_report(out),encoding='utf-8')
    return status

if __name__ == '__main__':
    print(json.dumps(run(Path.cwd(), '--dry-run' in sys.argv),ensure_ascii=False,indent=2))
