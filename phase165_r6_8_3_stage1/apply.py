from pathlib import Path
import ast
import shutil

ROOT=Path.cwd()
P53=ROOT/'probes/probe_phase53_capabilities.py'
P54=ROOT/'probes/probe_phase54_capabilities.py'
paths=(P53,P54)
for path in paths:
    if not path.is_file():
        raise SystemExit(f'MISSING: {path}')

NEW53='''def build_phase53_representative_result():
  """Transport a current, checked pi_4^3 proof; never execute Phase 50."""
  pi43_proof = search_group_from_registered_goal(n=3, k=1)
  if pi43_proof.status is not ProofSearchStatus.COMPLETE or pi43_proof.open_goals:
    raise ValueError("pi_4^3 shared backward proof is incomplete")
  source_step = next(
    (step for step in pi43_proof.proven_steps
     if step.conclusion == pi43_proof.conclusion), None)
  if source_step is None or source_step.rule is not ProofRule.INFERENCE:
    raise ValueError("pi_4^3 requires a derived root ProofStep")
  source_relation = source_step.conclusion
  if (not isinstance(source_relation, Relation)
      or source_relation.relation_type is not RelationType.EQUALITY
      or source_relation.lhs != TodaPrimaryGroup(group_dimension=4, sphere_dimension=3)
      or not isinstance(source_relation.rhs, FiniteCyclicGroup)
      or source_relation.rhs.order != 2):
    raise ValueError("pi_4^3 proof has unexpected group structure")
  eta_3 = source_relation.rhs.generator
  n = ScalarSymbol(name="n")
  stable_range = ScalarGreaterEqualStatement(left=3, right=ScalarSum(left=1, right=2))
  suspension_range = ScalarGreaterEqualStatement(left=n, right=3)
  target_group = TodaPrimaryGroup(group_dimension=ScalarSum(left=n, right=1), sphere_dimension=n)
  suspension_map = TodaIteratedSuspensionMap(
    exponent=ScalarSum(left=n, right=ScalarProduct(left=-1, right=3)),
    source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3),
    target_group=target_group,
  )
  premise_steps = (
    source_step,
    ProofStep(conclusion=stable_range, premises=(), rule=ProofRule.GIVEN),
    ProofStep(conclusion=suspension_range, premises=(), rule=ProofRule.GIVEN),
    ProofStep(conclusion=suspension_map, premises=(), rule=ProofRule.GIVEN),
  )
  rules = (
    toda_45_isomorphism_inference_rule(),
    toda_45_pi4_3_finite_cyclic_transport_inference_rule(),
  )
  target_relation = Relation(
    lhs=target_group,
    rhs=FiniteCyclicGroup(order=2, generator=IteratedSuspension(
      expression=eta_3, exponent=suspension_map.exponent)),
    relation_type=RelationType.EQUALITY,
  )
  result = run_inference_until_stable_with_history(rules, premise_steps)
  toda45_steps = tuple(step for step in result.steps if
    isinstance(step.conclusion, Toda45IsomorphismStatement)
    and step.conclusion.map == suspension_map)
  transported_steps = tuple(step for step in result.steps if step.conclusion == target_relation)
  if not toda45_steps or not transported_steps:
    raise ValueError("Toda (4.5) finite cyclic transport was not derived")
  return {
    "pi43_proof": pi43_proof,
    "source_group_steps": (source_step,),
    "n": n,
    "stable_range": stable_range,
    "suspension_range": suspension_range,
    "suspension_map": suspension_map,
    "target_group": target_group,
    "target_relation": target_relation,
    "premise_steps": premise_steps,
    "rules": rules,
    "result": result,
    "toda45_steps": toda45_steps,
    "transported_steps": transported_steps,
  }
'''

def replace_function(src: str,name:str,new:str):
    tree=ast.parse(src)
    node=next((node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name==name),None)
    if node is None:
        raise ValueError(f'function missing: {name}')
    lines=src.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1])+new+'\n'+''.join(lines[node.end_lineno:])

s53=P53.read_text(encoding='utf-8')
s54=P54.read_text(encoding='utf-8')
if 'build_phase50_representative_result' not in s53 or '"phase50_final_steps"' not in s54:
    raise SystemExit('Existing files do not match the audited legacy baseline; no changes made')
s53=replace_function(s53,'build_phase53_representative_result',NEW53)
s53=s53.replace('from probes.probe_phase50_capabilities import (\n  build_phase50_representative_result,\n  print_separator,\n)', 'from probes.probe_phase49_capabilities import (\n  print_separator,\n)')
s53=s53.replace('"phase50_final_steps"', '"source_group_steps"')
s53='from phase165_r55_nk_only_goal import search_group_from_registered_goal\nfrom phase165_r52_partial_proof import ProofSearchStatus\n'+s53
ns54=s54.replace('"phase50_final_steps"','"source_group_steps"')
# Phase 54 retains its original public diagnostics, but no Phase 50 proof data.
assert 'build_phase50_representative_result' not in s53
assert '"phase50_final_steps"' not in ns54
ast.parse(s53);ast.parse(ns54)
for path in paths:
    backup=path.with_suffix('.py.phase165_r6_8_3_stage1.bak')
    if not backup.exists():
        shutil.copy2(path,backup)
P53.write_text(s53,encoding='utf-8')
P54.write_text(ns54,encoding='utf-8')
print('APPLIED: Phase 53 and Phase 54 only; Phase 55 NOT modified')
