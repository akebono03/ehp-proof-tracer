"""Guarded modifications to current repository functions; backups are created."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil
import sys

ROOT=Path.cwd()
PACKAGE=Path(__file__).resolve().parent
IDENTITY=PACKAGE/'phase162_r10_reference_identity.py'
FILES={
    'toda_literature_statement_boundary.py': ('classify_toda_literature_statement_step',),
    'toda_group_proof_narrative_references.py': (
        'extract_toda_group_proof_step_literature_reference',
        'filter_toda_group_proof_narrative_reference_entries_by_body_usage',
    ),
}


def locate(text,name):
    module=ast.parse(text)
    matches=[n for n in module.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name]
    if len(matches)!=1:
        raise RuntimeError('Expected exactly one function: '+name)
    node=matches[0]
    lines=text.splitlines(keepends=True)
    start=sum(map(len,lines[:node.lineno-1]))
    end=sum(map(len,lines[:node.end_lineno]))
    return start,end,text[start:end]


def alter(path,name,source):
    if name=='classify_toda_literature_statement_step':
        anchor='  inference_rule = proof_step.inference_rule'
        add="""  from phase162_r10_reference_identity import fixed_citation_identity
  citation = fixed_citation_identity(proof_step)
  if citation is not None and proof_step.rule is ProofRule.INFERENCE:
    return TodaLiteratureStatementBoundary(
      classification=TodaLiteratureStatementClassification.FIXED_STATEMENT,
      reference_locator=citation[0],
      component_key=citation[1],
    )

"""
        # Leaf remains a GIVEN; its actual fixed proof statement is the wrapper inference.
        if anchor not in source:raise RuntimeError('Missing classification anchor')
        return source.replace(anchor,add+anchor,1)
    if name=='extract_toda_group_proof_step_literature_reference':
        anchor='  inference_rule = proof_step.inference_rule'
        add="""  from phase162_r10_reference_identity import fixed_citation_identity
  citation = fixed_citation_identity(proof_step)
  if citation is not None:
    return LiteratureReference(
      label="Toda " + citation[0],
      locator=citation[0],
    )

"""
        if anchor not in source:raise RuntimeError('Missing reference extraction anchor')
        return source.replace(anchor,add+anchor,1)
    if name=='filter_toda_group_proof_narrative_reference_entries_by_body_usage':
        anchor="  used_reference_numbers = set(\n    body_reference_numbers\n  )"
        if anchor not in source:raise RuntimeError('Missing body reference filter anchor')
        replacement=anchor+"""
  from phase162_r10_reference_identity import is_cited_inference
  for entry in entries:
    if any(is_cited_inference(step) for step in entry.proof_steps):
      used_reference_numbers.add(entry.number)
"""
        # Don't early return if zero markers: cited fixed steps may still be used.
        early="""  if not body_reference_numbers:
    return (
      entries,
      statement_lines_by_reference_number,
      body_markdown,
    )

"""
        early_crlf=early.replace('\n','\r\n')
        if early in source:source=source.replace(early,'',1)
        elif early_crlf in source:source=source.replace(early_crlf,'',1)
        else:raise RuntimeError('Missing early return guard')
        return source.replace(anchor,replacement,1)
    raise RuntimeError('Unknown function '+name)


def main():
    updates={}
    old_units={}
    for filename,names in FILES.items():
        target=ROOT/filename
        if not target.is_file():raise RuntimeError('Missing production file '+filename)
        original=target.read_text(encoding='utf-8')
        current=original
        for name in names:
            start,end,source=locate(current,name)
            if 'phase162_r10_reference_identity' in source:
                raise RuntimeError('Already patched: '+name)
            new=alter(filename,name,source)
            current=current[:start]+new+current[end:]
            old_units[(filename,name)]=source
        # This classification function currently imports ProofStep but not ProofRule.
        if filename=='toda_literature_statement_boundary.py':
            # Use a local import to avoid touching unrelated import blocks.
            start,end,source=locate(current,'classify_toda_literature_statement_step')
            source=source.replace('  from phase162_r10_reference_identity import fixed_citation_identity',
                                  '  from proof import ProofRule\n  from phase162_r10_reference_identity import fixed_citation_identity',1)
            current=current[:start]+source+current[end:]
        ast.parse(current,filename=filename)
        updates[target]=current
    new_target=ROOT/IDENTITY.name
    if new_target.exists() and new_target.read_bytes()!=IDENTITY.read_bytes():
        raise RuntimeError('Conflicting existing helper module')
    # Build a complete, replaceable function report before any change.
    report=['# R10-R4: full modified functions','', '## Modified files and functions',
            '- toda_literature_statement_boundary.py: classify_toda_literature_statement_step',
            '- toda_group_proof_narrative_references.py: extract_toda_group_proof_step_literature_reference, filter_toda_group_proof_narrative_reference_entries_by_body_usage',
            '- New module: phase162_r10_reference_identity.py','',
            '## Imports', 'No top-level imports changed; all new imports are local to the full functions shown below.','']
    for target,content in updates.items():
        for name in FILES[target.name]:
            source=locate(content,name)[2]
            report += ['## '+target.name+' — '+name,'```python',source.rstrip(),'```','']
    report += ['## New complete module','```python',IDENTITY.read_text(encoding='utf-8').rstrip(),'```','']
    (PACKAGE/'CHANGED_CODE.md').write_text('\n'.join(report),encoding='utf-8')
    for target,content in updates.items():
        backup=target.with_name(target.name+'.phase162_r10_r4.bak')
        if not backup.exists():shutil.copy2(target,backup)
        target.write_text(content,encoding='utf-8')
        print('Updated:',target.name,'Backup:',backup.name)
    if not new_target.exists():new_target.write_bytes(IDENTITY.read_bytes())
    print('Installed:',new_target.name)
    print('Full changed functions:',PACKAGE/'CHANGED_CODE.md')

if __name__=='__main__':main()
