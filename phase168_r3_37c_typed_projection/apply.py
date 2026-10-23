"""Minimal guarded patch. Emits full changed definitions."""
from pathlib import Path
import ast
import difflib

ROOT=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent/'output'
OUT.mkdir(exist_ok=True)


def patch(path, changes, names):
    target=ROOT/path
    raw=target.read_bytes()
    crlf=b'\r\n' in raw
    old=raw.decode('utf-8').replace('\r\n','\n')
    new=old
    for before, after in changes:
        if new.count(before)!=1:
            raise RuntimeError(f'Unexpected anchor count {new.count(before)} for {path}')
        new=new.replace(before,after,1)
    tree=ast.parse(new)
    for name in names:
        nodes=[node for node in tree.body if isinstance(node,(ast.ClassDef,ast.FunctionDef)) and node.name==name]
        if len(nodes)!=1:
            raise RuntimeError(f'Definition unavailable: {name}')
        node=nodes[0]
        (OUT/(path+'_'+name+'_FULL.py')).write_text('\n'.join(new.splitlines()[node.lineno-1:node.end_lineno])+'\n',encoding='utf-8')
    (OUT/(path+'.before')).write_text(old,encoding='utf-8')
    (OUT/(path+'.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True))),encoding='utf-8')
    target.write_bytes(new.replace('\n','\r\n').encode('utf-8') if crlf else new.encode('utf-8'))
    print('PATCHED',path)


def main():
    patch('phase168_r3_3_proof_narrative_model.py',[
        ('    reference_ids: tuple[str, ...] = ()\n','    reference_ids: tuple[str, ...] = ()\n    statement_bodies: tuple[str, ...] = ()\n'),
        ('    citations = tuple(\n','    from phase168_r3_37c_reference_projection import project_reference_bodies\n    citations = tuple(\n'),
        ('            reference_ids=tuple(reference_ids[i]),\n','            reference_ids=tuple(reference_ids[i]),\n            statement_bodies=project_reference_bodies(registry, tuple(assertion_ids[i])),\n')
    ],['NarrativeCitation','build_proof_narrative_model'])
    patch('phase168_r3_27_typed_statement_projection.py',[
        ('    if isinstance(statement, TodaDeltaZeroStatement):\n', """    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            if source is not None and target is not None and type(mapping.exponent) is int:
                symbol = 'E' if mapping.exponent == 1 else rf'E^{{{mapping.exponent}}}'
                return rf'${symbol}: {source}\to {target}$ は同型である.'
    if isinstance(statement, TodaDeltaZeroStatement):
""")
    ],['typed_sentence'])
    patch('phase168_r3_5_model_renderer.py',[
        ('        lines.append(f"**[R{citation.number}] {locator}.**")\n        lines.append("")\n', '        lines.append(f"**[R{citation.number}] {locator}.**")\n        lines.append("")\n        for sentence in citation.statement_bodies:\n            lines.extend((sentence, ""))\n')
    ],['render_model_backed_narrative_markdown'])


if __name__=='__main__':
    main()
