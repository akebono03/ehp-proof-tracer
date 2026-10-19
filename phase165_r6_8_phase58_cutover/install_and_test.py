from __future__ import annotations
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
FILE=ROOT/"probes"/"probe_phase58_capabilities.py"
TEST=Path(__file__).resolve().parent/"test_phase165_r6_8_phase58_cutover.py"
source=FILE.read_text(encoding="utf-8-sig")
original=source

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
old_return='    "phase50": phase50,'
new_return='    "phase50": {"final_group_steps": (pi4_3_step,)},'
for old,new in ((old_import,new_import),(old_setup,new_setup),(old_step,new_step),(old_return,new_return)):
    count=source.count(old)
    if count!=1:
        raise SystemExit(f"ABORT: expected one matching code block; found {count}: {old[:55]!r}")
    source=source.replace(old,new,1)
ast.parse(source)
backup=FILE.with_name(FILE.name+".r6_8_original.bak")
if backup.exists():
    raise SystemExit("ABORT: backup already exists; no files changed")
backup.write_text(original,encoding="utf-8")
FILE.write_text(source,encoding="utf-8")
print("APPLIED:",FILE,flush=True)
command=[sys.executable,"-m","pytest","-q",str(TEST)]
try:
    result=subprocess.run(command,cwd=ROOT,timeout=90)
except subprocess.TimeoutExpired:
    result=None
if result is None or result.returncode!=0:
    FILE.write_text(original,encoding="utf-8")
    print("ROLLED_BACK: targeted pytest failed/timed out; backup preserved",flush=True)
    raise SystemExit(1)
print("PASS: targeted test; full pytest NOT run; backup:",backup,flush=True)
