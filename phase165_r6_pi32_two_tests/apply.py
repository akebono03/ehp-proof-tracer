from pathlib import Path
import ast, shutil, datetime
p=Path('tests/test_phase49_probe.py')
if not p.is_file(): raise SystemExit('ERROR: run from repository root')
s=p.read_text(encoding='utf-8')
tree=ast.parse(s)
replacements={
 'test_phase49_probe_derives_final_pi_3_2_group': '''def test_phase49_probe_derives_final_pi_3_2_group():
  from pathlib import Path
  from hopf_facts import ETA_2
  from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
  from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
  from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
  from phase165_r52_partial_proof import ProofSearchStatus
  from proof import ProofRule, Relation

  source = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
  bridge = build_shared_typed_bridge(sources=(build_adopted_typed_reference_registry(source),))
  result = search_shared_group_goal(
    n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,
  )
  assert result.status is ProofSearchStatus.COMPLETE
  assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
  assert any(
    step.rule is ProofRule.INFERENCE and step.conclusion == result.conclusion
    for step in result.proven_steps
  )
''',
 'test_phase49_probe_all_derived_steps_preserve_inference_rule': '''def test_phase49_probe_all_derived_steps_preserve_inference_rule():
  from pathlib import Path
  from hopf_facts import ETA_2
  from homotopy_groups import FreeCyclicGroup
  from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
  from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
  from phase165_r52_partial_proof import ProofSearchStatus
  from proof import ProofRule

  source = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
  bridge = build_shared_typed_bridge(sources=(build_adopted_typed_reference_registry(source),))
  result = search_shared_group_goal(
    n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,
  )
  assert result.status is ProofSearchStatus.COMPLETE
  derived = tuple(step for step in result.proven_steps if step.rule is ProofRule.INFERENCE)
  assert derived
  assert all(step.inference_rule is not None for step in derived)
  assert any(step.conclusion == result.conclusion for step in derived)
'''
}
lines=s.splitlines(keepends=True)
chunks=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in replacements:
  old=''.join(lines[node.lineno-1:node.end_lineno])
  if 'build_phase49_representative_result()' not in old: raise SystemExit(f'GUARD FAILED for {node.name}; no modification')
  chunks.append((node.lineno-1,node.end_lineno,replacements[node.name]))
if len(chunks)!=2: raise SystemExit('GUARD FAILED: expected exactly two functions')
backup=Path('phase165_r6_audit_results/runner_backup/pi32_two_tests_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
backup.mkdir(parents=True,exist_ok=True)
shutil.copy2(p,backup/p.name)
for a,b,repl in reversed(chunks): lines[a:b]=[repl+'\n']
new=''.join(lines)
ast.parse(new)
p.write_text(new,encoding='utf-8')
print('PATCHED:',p,'BACKUP:',backup,'UNCHANGED OTHER TESTS:',21)
