"""Phase 164 R8-R6: guarded ProofStep display/reference creation routing."""
from __future__ import annotations

import ast
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL_AUDIT = json.loads((HERE / 'r8_r4_sites.json').read_text(encoding='utf-8'))
FACTORY = 'phase164_r8_proofstep_factory.py'
REFERENCE = 'phase162_reference_boundary.py'
RENDERER = 'toda_group_proof_narrative_contribution_renderer.py'
OLD_REFERENCE = 'return replace(result, foundational_reference=citation_identity)'
NEW_REFERENCE = 'return annotate_derived_reference_step(result, citation_identity)'
OLD_RENDER = '''  component_step = ProofStep(
    conclusion=component,
    premises=(),
    rule=proof_step.rule,
    note=proof_step.note,
    inference_rule=proof_step.inference_rule,
  )'''
NEW_RENDER = '''  component_step = project_reference_component_step(
    proof_step, component
  )'''
ADD_FACTORY = '''\n\ndef annotate_derived_reference_step(step: ProofStep, reference) -> ProofStep:
    """Preserve an inferred step's ancestry while attaching known citation identity.

    A reference label alone does not certify a statement's mathematical truth.
    """
    from dataclasses import replace
    from proof import FoundationalReferenceIdentity
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE:
        raise TypeError("step must be an inferred ProofStep")
    if not isinstance(reference, FoundationalReferenceIdentity):
        raise TypeError("reference must be a FoundationalReferenceIdentity")
    if step.foundational_reference is not None and step.foundational_reference != reference:
        raise ValueError("cannot overwrite another foundational reference")
    return replace(step, foundational_reference=reference)


def project_reference_component_step(source_step: ProofStep, component) -> ProofStep:
    """Create a display-only projection without promoting its evidence status.

    This is NOT an inference and must never be inserted as a proof-tree node.
    """
    if not isinstance(source_step, ProofStep):
        raise TypeError("source_step must be a ProofStep")
    return ProofStep(
        conclusion=component,
        premises=(),
        rule=source_step.rule,
        note=source_step.note,
        inference_rule=source_step.inference_rule,
    )
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def add_import(source, symbol):
    # Keep import changes explicit and confined to the top-level import section.
    tree = ast.parse(source)
    start = next((i for i,n in enumerate(tree.body) if isinstance(n,(ast.Import,ast.ImportFrom))), None)
    if start is None:
        raise ValueError('no import section')
    last = tree.body[start]
    for node in tree.body[start+1:]:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            last=node
        else:
            break
    lines=source.splitlines(keepends=True)
    lines.insert(last.end_lineno, '\nfrom phase164_r8_proofstep_factory import (\n    ' + symbol + ',\n)\n')
    result=''.join(lines)
    ast.parse(result)
    return result


def replace_exact(source, old, new, label):
    if source.count(old) != 1:
        raise ValueError(f'{label}: expected exactly one old site; observed {source.count(old)}')
    source=source.replace(old,new,1)
    ast.parse(source)
    return source


def prepare(root):
    root=Path(root)
    prepared={}
    line_endings={}
    for name in (FACTORY,REFERENCE,RENDERER):
        blob=(root/name).read_bytes()
        if blob.startswith(b'\xef\xbb\xbf'):
            raise ValueError(f'{name}: BOM not supported by guarded patch')
        source=blob.decode('utf-8')
        line_endings[name]='\r\n' if '\r\n' in source else '\n'
        source=source.replace('\r\n','\n')
        ast.parse(source)
        prepared[name]=(blob,source)
    factory=prepared[FACTORY][1]
    if factory.count('def create_legacy_given_proof_step(')!=1 or factory.count('def create_legacy_specialization_proof_step(')!=1:
        raise ValueError('R8-R5 factory missing')
    if 'def annotate_derived_reference_step(' in factory or 'def project_reference_component_step(' in factory:
        raise ValueError('R8-R6 factory additions already exist')
    factory += ADD_FACTORY
    ast.parse(factory)
    ref=replace_exact(prepared[REFERENCE][1],OLD_REFERENCE,NEW_REFERENCE,REFERENCE)
    ref=add_import(ref,'annotate_derived_reference_step')
    render=replace_exact(prepared[RENDERER][1],OLD_RENDER,NEW_RENDER,RENDERER)
    render=add_import(render,'project_reference_component_step')
    return {FACTORY:(prepared[FACTORY][0],factory.replace('\n',line_endings[FACTORY])),
            REFERENCE:(prepared[REFERENCE][0],ref.replace('\n',line_endings[REFERENCE])),
            RENDERER:(prepared[RENDERER][0],render.replace('\n',line_endings[RENDERER]))}


def source_sites(root):
    """Match the archived 66 review sites to current code by per-file call order.

    R8-R5 inserted imports so its line numbers are not R8-R4 line numbers.
    A changed call count fails closed rather than picking a nearest unrelated call.
    """
    from collections import defaultdict
    original=defaultdict(list)
    for site in ORIGINAL_AUDIT['sites']:
        if site['category']=='dataclass_replace_type_review':
            original[site['file']].append(site)
    results=[]
    for filename, archived in sorted(original.items()):
        tree=ast.parse((root/filename).read_text(encoding='utf-8-sig'),filename=filename)
        calls=sorted((n for n in ast.walk(tree) if isinstance(n,ast.Call)
                      and (isinstance(n.func,ast.Name) and n.func.id=='replace'
                           or isinstance(n.func,ast.Attribute) and n.func.attr=='replace')),
                     key=lambda n:(n.lineno,n.col_offset))
        archived.sort(key=lambda s:(s['line'],s['function']))
        if len(calls)!=len(archived):
            raise ValueError(f'{filename}: replace count drift: {len(calls)} != {len(archived)}')
        for site,call in zip(archived,calls):
            classification='non_proofstep_or_review'
            if filename==REFERENCE and site['function']=='cite_verified_fixed_statement':
                classification='proofstep_reconstruction_migrate'
            elif isinstance(call.func,ast.Attribute):
                classification='method_replace_not_dataclasses'
            results.append({**site,'current_line':call.lineno,'r8_r6_classification':classification})
    return results


def changed_code(sources):
    output='# Phase 164 R8-R6 変更コード全文\n\n'
    for name,(_,source) in sources.items():
        tree=ast.parse(source)
        lines=source.splitlines()
        imports='\n'.join('\n'.join(lines[node.lineno-1:node.end_lineno]) for node in tree.body if isinstance(node,(ast.Import,ast.ImportFrom)))
        if name==FACTORY:
            names={'annotate_derived_reference_step','project_reference_component_step'}
        elif name==REFERENCE:
            names={'cite_verified_fixed_statement'}
        else:
            names={'_phase153_r6_render_reference_statement'}
        blocks=[]
        for node in tree.body:
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.name in names:
                blocks.append('\n'.join(lines[node.lineno-1:node.end_lineno]))
        if len(blocks)!=len(names):
            raise ValueError(f'cannot locate changed function in {name}: {names}')
        output+=f'## {name}\n\n### import 全文\n\n```python\n{imports}\n```\n\n### 変更した関数全文\n\n'
        output+='\n\n'.join('```python\n'+block+'\n```' for block in blocks)+'\n\n'
    return output


def run(root,dry_run=False):
    root=Path(root)
    sources=prepare(root)
    residual=source_sites(root)
    if len(residual)!=66:
        raise ValueError(f'expected 66 replace sites, found {len(residual)}')
    if dry_run:
        return {'dry_run':True,'files':len(sources),'replace_sites':len(residual),'proofstep_replace_sites':sum(s['r8_r6_classification']=='proofstep_reconstruction_migrate' for s in residual)}
    backup=root/('phase164_r8_r6_backup_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.mkdir(exist_ok=False)
    for name,(before,after) in sources.items():
        (backup/name).write_bytes(before)
    written=[]
    try:
        for name,(before,after) in sources.items():
            target=root/name
            if target.read_bytes()!=before:
                raise ValueError(f'file changed between preparation and write: {name}')
            target.write_bytes(after.encode('utf-8'))
            written.append(name)
    except Exception:
        for name in written:
            (root/name).write_bytes((backup/name).read_bytes())
        raise
    output=root/'phase164_r8_r6_output'
    output.mkdir(exist_ok=True)
    report={'phase':'164 R8-R6','status':'DYNAMIC_AND_PROOFSTEP_REPLACE_CENTRALIZED_WITH_REVIEW_REMAINDER',
            'changed_files':list(sources),'backup_dir':str(backup),'replace_review_count':66,
            'proofstep_replace_migrated':1,'other_replace_sites':65,
            'core_engine_sites':10,'dynamic_projection_migrated':1,
            'full_pytest_run':False,'r8_closed':False,
            'limitation':'R8-R5 legacy GIVEN and direct INFERENCE remain noncertifying; 65 remaining replace sites are not all proven non-ProofStep by static analysis.'}
    (output/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'replace_sites.json').write_text(json.dumps(residual,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'CHANGED_CODE.md').write_text(changed_code(sources),encoding='utf-8')
    return report

if __name__=='__main__':
    print(json.dumps(run(Path.cwd(),dry_run='--dry-run' in sys.argv),ensure_ascii=False,indent=2))
