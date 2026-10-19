from __future__ import annotations
import ast
import shutil
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
PHASE58=ROOT/"probes"/"probe_phase58_capabilities.py"
RULES=ROOT/"toda_rules.py"
TEST=Path(__file__).resolve().parent/"test_phase165_r6_8_eta_name_fix.py"

def extract_function(text,name):
    node=next((x for x in ast.parse(text).body if isinstance(x,ast.FunctionDef) and x.name==name),None)
    if node is None:
        raise ValueError("Missing function: "+name)
    lines=text.splitlines(keepends=True)
    return node, "".join(lines[node.lineno-1:node.end_lineno])

def replacement(text,old,new,label):
    count=text.count(old)
    if count!=1:
        raise ValueError(f"{label}: expected one occurrence, found {count}")
    return text.replace(old,new,1)

old58=PHASE58.read_text(encoding="utf-8-sig")
oldrules=RULES.read_text(encoding="utf-8-sig")
if "pi4_3_proof = search_group_from_registered_goal" in old58:
    raise SystemExit("ABORT: prior Phase58 cutover is already present")
node,fn=extract_function(oldrules,"toda_53_eta3_twice_zero_inference_rule")
old_compare="""    return (
      group_relation.rhs.generator
      == eta_3
    )"""
new_compare="""    candidate = group_relation.rhs.generator
    return (
      isinstance(candidate, HomotopyElement)
      and candidate.dimension == eta_3.dimension
      and candidate.source == eta_3.source
      and candidate.target == eta_3.target
      and candidate.generator == eta_3.generator
      and candidate.name in ("η₃", "η_3")
    )"""
updated_fn=replacement(fn,old_compare,new_compare,"eta3 comparison")
newrules=replacement(oldrules,fn,updated_fn,"rule function")
old_import="""from probes.probe_phase50_capabilities import (
  build_phase50_representative_result,
  print_separator,
)"""
new_import="""from probes.probe_phase49_capabilities import (
  print_separator,
)
from phase165_r55_nk_only_goal import (
  search_group_from_registered_goal,
)
from phase165_r52_partial_proof import (
  ProofSearchStatus,
)"""
old_setup="""  phase50 = (
    build_phase50_representative_result()
  )"""
new_setup="""  pi4_3_proof = search_group_from_registered_goal(n=3, k=1)
  if pi4_3_proof.status is not ProofSearchStatus.COMPLETE:
    raise ValueError("pi_4^3 common proof is incomplete")
  if pi4_3_proof.open_goals:
    raise ValueError("pi_4^3 common proof has open goals")
"""
old_step="""  pi4_3_step = (
    phase50[
      "final_group_steps"
    ][
      0
    ]
  )"""
new_step="""  pi4_3_step = next(
    (
      step for step in reversed(pi4_3_proof.proven_steps)
      if step.conclusion == pi4_3_proof.conclusion
      and step.rule is ProofRule.INFERENCE
    ),
    None,
  )
  if pi4_3_step is None:
    raise ValueError("pi_4^3 common proof has no inferred conclusion")
"""
new58=old58
for left,right,name in [
    (old_import,new_import,"import"),
    (old_setup,new_setup,"setup"),
    (old_step,new_step,"step"),
    ('    "phase50": phase50,','    "phase50": {"final_group_steps": (pi4_3_step,)},',"return-key")]:
    new58=replacement(new58,left,right,name)
ast.parse(new58);ast.parse(newrules)
backups=[]
try:
    for path,old in ((PHASE58,old58),(RULES,oldrules)):
        backup=path.with_name(path.name+".r6_8_eta_name_fix.bak")
        if backup.exists():
            raise ValueError("Existing backup: "+str(backup))
    for path,old in ((PHASE58,old58),(RULES,oldrules)):
        backup=path.with_name(path.name+".r6_8_eta_name_fix.bak")
        backup.write_text(old,encoding="utf-8")
        backups.append((path,backup))
    RULES.write_text(newrules,encoding="utf-8")
    PHASE58.write_text(new58,encoding="utf-8")
    print("APPLIED:",RULES,PHASE58,flush=True)
    res=subprocess.run([sys.executable,"-m","pytest","-q",str(TEST)],cwd=ROOT,timeout=100)
    if res.returncode!=0:
        raise RuntimeError("Targeted tests failed")
except Exception as exc:
    for path,backup in backups:
        shutil.copyfile(backup,path)
    print("ROLLED BACK:",exc,flush=True)
    raise SystemExit(1)
print("R6-8 targeted PASS; full pytest NOT run",flush=True)
