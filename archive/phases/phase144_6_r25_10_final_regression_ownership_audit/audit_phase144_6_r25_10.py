from dataclasses import fields,is_dataclass
import importlib
import importlib.util
import inspect
from pathlib import Path
import sys

TARGETS=((3,3),(5,3),(4,6),(5,7),(8,7),(9,7))

def fm(x):
  if is_dataclass(x):
    return {f.name:getattr(x,f.name) for f in fields(x)}
  if isinstance(x,dict): return dict(x)
  if isinstance(x,tuple): return {str(i):v for i,v in enumerate(x)}
  if hasattr(x,"__dict__"): return dict(vars(x))
  return {"value":x}

def show(label,x):
  print(label)
  for k,v in fm(x).items():
    try: s=str(v)
    except Exception as e: s=f"<str failed {type(e).__name__}: {e}>"
    print(f"  {k} = {s}")

def group(x):
  d=fm(x)
  return (d.get("n"),d.get("k")) if "n" in d and "k" in d else None

def load_test_module(module_name):
  prefix = "tests."

  if not module_name.startswith(prefix):
    return importlib.import_module(module_name)

  short_name = module_name[len(prefix):]
  path = (
    Path(__file__).resolve().parent.parent
    / "tests"
    / f"{short_name}.py"
  )

  if not path.is_file():
    raise ModuleNotFoundError(
      f"test module file not found: {path}"
    )

  cache_name = (
    "_phase144_6_r25_10_"
    + short_name
  )

  if cache_name in sys.modules:
    return sys.modules[cache_name]

  spec = importlib.util.spec_from_file_location(
    cache_name,
    path,
  )

  if (
    spec is None
    or spec.loader is None
  ):
    raise ImportError(
      f"cannot create module spec for {path}"
    )

  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[cache_name] = module
  spec.loader.exec_module(
    module
  )
  return module


def call(mod,fn):
  return getattr(
    load_test_module(mod),
    fn,
  )()

def counts(label,rows,expected):
  rows=tuple(rows)
  print(f"{label}: total={len(rows)} expected={expected} delta={len(rows)-expected:+d}")
  for t in TARGETS:
    print(f"  n={t[0]} k={t[1]} count={sum(group(r)==t for r in rows)}")
  return rows

print("="*78)
print("Phase 144-6 R25-10 final regression ownership audit")
print("production changes: none")
print("="*78)

print("\nA. Inventory population ownership\n"+"-"*78)
specs=(
("phase37","tests.test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit","build_semantic_equivalence_and_rendering_inventory",353),
("phase38","tests.test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit","build_visibility_occurrences",291),
("phase39","tests.test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit","build_narrative_necessity_inventory",194),
("phase40","tests.test_phase144_6_r5_40_narrative_contribution_placement_order_audit","build_placement_inventory",190),
)
for label,mod,fn,expected in specs:
  rows=counts(label,call(mod,fn),expected)
  pi6=tuple(r for r in rows if group(r)==(3,3))
  print(f"  pi6_count={len(pi6)}")
  if label in ("phase39","phase40"):
    for i,r in enumerate(pi6): show(f"  pi6[{i}]",r)

print("\nB. Ordered contributions by representative group\n"+"-"*78)
m=load_test_module("tests.test_phase144_6_r5_43_r2_recursive_repr_repair")
from toda_group_proof_narrative_argument_multi_renderer import render_toda_group_proof_narrative_multi_argument_markdown
from toda_group_proof_narrative_contribution_ordering import build_toda_group_proof_narrative_ordered_contributions
for n,k in TARGETS:
  p,s,b,a,agg,chains=m._context(n,k)
  base=render_toda_group_proof_narrative_multi_argument_markdown(p,b,s,a)
  ordered=build_toda_group_proof_narrative_ordered_contributions(p,b,s,a,chains,current_markdown=base)
  print(f"pi_{n+k}^{n}: arguments={len(a)} contributions={sum(len(x) for x in ordered)} populated={tuple(i for i,x in enumerate(ordered) if x)}")
  if (n,k)==(3,3):
    for ai,rs in enumerate(ordered):
      for ci,r in enumerate(rs): show(f"  pi6 argument[{ai}] contribution[{ci}]",r)

print("\nC. Completion ownership\n"+"-"*78)
m=load_test_module("tests.test_phase144_6_r5_43_11d_final_completion_audit")
for r in m.build_completion_inventory(): show(f"completion n={r.n} k={r.k}",r)

print("\nD. Detached boundary raw inventory\n"+"-"*78)
m=load_test_module("tests.test_phase144_6_r5_43_11c_r2_argument_participation_guard")
for i,r in enumerate(m._inventory()): show(f"boundary[{i}]",r)

print("\nE. pi6 transition inventory\n"+"-"*78)
m=load_test_module("tests.test_phase144_6_r5_43_3")
connected,inventory=m.build_transition_inventory()
print(f"transition_count={len(inventory)}")
for i,r in enumerate(inventory): show(f"transition[{i}]",r)
print("Numbering/connector lines:")
for i,line in enumerate(connected.splitlines(),1):
  if any(x in line for x in ("(1)","(2)","(3)","(4)","(5)","より",r"\nu'")):
    print(f"  {i:04d}: {line}")

print("\nF. Public depth=2 Narrative boundary\n"+"-"*78)
from toda_calculation_facade import build_standard_toda_report
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation,build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
report=build_standard_toda_report(n=3,k=3)
gr=report.candidates[0].source_candidate.group_result
replay=build_toda_group_result_proof_replay(gr,max_depth=2)
p=build_toda_group_proof_presentation(replay)
c=build_toda_group_proof_narrative_semantic_closure_presentation(p)
s=build_toda_group_proof_narrative_semantic_sidecar(c)
b=build_toda_group_proof_narrative_blocks(c,semantic_sidecar=s)
a=build_toda_group_proof_narrative_arguments(c,b,semantic_sidecar=s)
print(f"source_nodes={len(p.nodes)} closure_nodes={len(c.nodes)} arguments={len(a)}")
for i,x in enumerate(a): print(f"  argument[{i}] role={x.role.value} conclusion_block_role={x.conclusion_block.role.value} conclusion_steps={len(x.conclusion_block.steps)}")
rendered=render_toda_group_proof_narrative_markdown(p)
for i,line in enumerate(rendered.splitlines(),1): print(f"{i:04d}: {line}")

print("\nG. Recursive-repr ownership\n"+"-"*78)
m=load_test_module("tests.test_phase144_6_r5_43_r2_recursive_repr_repair")
if hasattr(m,"_group_key"):
  print(inspect.getsource(m._group_key))

print("\n"+"="*78)
print("R25-10 ownership audit completed. No production files modified.")
print("="*78)



