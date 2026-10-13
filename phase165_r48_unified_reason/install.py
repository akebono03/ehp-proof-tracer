from __future__ import annotations
import ast
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
GENERIC=ROOT/"toda_group_proof_generic_narrative_renderer.py"
PUBLIC=ROOT/"toda_group_proof_narrative_renderer.py"

def replace_function(source,name,transform):
    tree=ast.parse(source)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
    if len(nodes)!=1:
        raise RuntimeError(f"Expected one {name}, got {len(nodes)}")
    node=nodes[0]
    lines=source.splitlines(keepends=True)
    old="".join(lines[node.lineno-1:node.end_lineno])
    new=transform(old)
    updated="".join(lines[:node.lineno-1])+new+"".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated

def patch_generic(body):
    marker="phase165_r48_unified_exactness"
    if marker in body:
        return body
    old="""    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )
"""
    new="""    # phase165_r48_unified_exactness: derive the lead from proof premises.
    exactness_premise = any(
      isinstance(premise, ProofStep)
      and isinstance(premise.conclusion, TodaProp42ExactnessStatement)
      for premise in proof_step.premises
    )
    if proof_step.inference_rule is not None and exactness_premise:
      lines.append("完全性より,")
      lines.append("")

    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )
"""
    if body.count(old)!=1: raise RuntimeError("Unknown generic block structure")
    return body.replace(old,new,1)

def patch_public(body):
    old="""  rendered = (
    _phase159_r1_6c_link_proof_reasons(
      presentation,
      rendered,
    )
  )
"""
    if old not in body: raise RuntimeError("Old linker call not found in Phase159 route")
    if body.count(old)!=1: raise RuntimeError("Unexpected repeated linker")
    return body.replace(old,"",1)

def remove_old_linker(source):
    tree=ast.parse(source)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)
           and n.name=="_phase159_r1_6c_link_proof_reasons"]
    if len(nodes)!=1: raise RuntimeError("Old linker not uniquely identified")
    node=nodes[0]
    lines=source.splitlines(keepends=True)
    updated="".join(lines[:node.lineno-1]+lines[node.end_lineno:])
    ast.parse(updated)
    if "_phase159_r1_6c_link_proof_reasons(" in updated:
        raise RuntimeError("Old linker still called; refusing deletion")
    return updated

def transform(generic,public):
    if "phase165_r48_unified_exactness" not in generic:
        generic=replace_function(generic,"_render_generic_narrative_proof_block",patch_generic)
    if "_phase159_r1_6c_link_proof_reasons(" in public:
        public=replace_function(public,
            "_phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown",
            patch_public)
        public=remove_old_linker(public)
    return generic,public

def main():
    before_g=GENERIC.read_text(encoding="utf8")
    before_p=PUBLIC.read_text(encoding="utf8")
    new_g,new_p=transform(before_g,before_p)
    for path,old,new in [(GENERIC,before_g,new_g),(PUBLIC,before_p,new_p)]:
        if old==new: continue
        backup=path.with_name(path.stem+".phase165_r48_backup.py")
        if not backup.exists(): shutil.copy2(path,backup)
        path.write_text(new,encoding="utf8")
        print("Updated",path.name,"backup",backup.name)
    print("Removed obsolete text-matching reason linker; no R43 add-on")

if __name__=="__main__":
    main()
