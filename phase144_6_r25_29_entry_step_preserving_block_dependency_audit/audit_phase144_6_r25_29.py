from collections import Counter

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_argument_local_body import extract_toda_group_proof_narrative_argument_local_body_blocks
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_blocks import TodaGroupProofNarrativeMathematicalBlockRole, build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay

TARGETS=((3,3),(5,3),(4,6),(5,7),(8,7),(9,7))

def _data(n,k):
  report=build_standard_toda_report(n=n,k=k)
  group_result=report.candidates[0].source_candidate.group_result
  replay=build_complete_toda_group_result_proof_replay(group_result)
  presentation=build_toda_group_proof_presentation(replay)
  sidecar=build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks=build_toda_group_proof_narrative_blocks(presentation,semantic_sidecar=sidecar)
  arguments=build_toda_group_proof_narrative_arguments(presentation,blocks,semantic_sidecar=sidecar)
  return presentation,blocks,sidecar,arguments

def _indices(presentation,blocks):
  step_index_by_id={id(node.proof_step):i for i,node in enumerate(presentation.nodes)}
  block_index_by_step_id={id(step):bi for bi,block in enumerate(blocks) for step in block.steps}
  block_index_by_identity={id(block):bi for bi,block in enumerate(blocks)}
  return step_index_by_id,block_index_by_step_id,block_index_by_identity

def _step_dependencies(presentation,sidecar,step_index_by_id):
  deps=[[] for _ in presentation.nodes]
  def add(dependent,prerequisite):
    di=step_index_by_id[id(dependent)]
    pi=step_index_by_id[id(prerequisite)]
    if pi not in deps[di]: deps[di].append(pi)
  for edge in presentation.edges: add(edge.parent_step,edge.premise_step)
  for semantic in sidecar.dependency_semantics: add(semantic.dependent_step,semantic.prerequisite_step)
  return tuple(tuple(row) for row in deps)

def _simulation(presentation,blocks,sidecar,arguments,argument_index):
  step_index_by_id,block_index_by_step_id,block_index_by_identity=_indices(presentation,blocks)
  deps=_step_dependencies(presentation,sidecar,step_index_by_id)
  conclusion_blocks=tuple(block_index_by_identity[id(a.conclusion_block)] for a in arguments)
  conclusion_steps=tuple(frozenset(step_index_by_id[id(s)] for s in a.conclusion_block.steps) for a in arguments)
  cb=conclusion_blocks[argument_index]
  current_steps=conclusion_steps[argument_index]
  boundary_steps=frozenset(si for ai,ss in enumerate(conclusion_steps) if ai!=argument_index for si in ss)
  entries=[]
  for csi in current_steps:
    for di in deps[csi]:
      db=block_index_by_step_id[id(presentation.nodes[di].proof_step)]
      if db!=cb and di not in entries: entries.append(di)
  ordered=[]; visited=set(); active=set()
  def visit(si):
    if si in boundary_steps or si in current_steps or si in visited or si in active: return
    active.add(si)
    for di in deps[si]: visit(di)
    active.remove(si); visited.add(si); ordered.append(si)
  for si in entries: visit(si)
  projected=[]; seen=set()
  for si in ordered:
    bi=block_index_by_step_id[id(presentation.nodes[si].proof_step)]
    if bi!=cb and bi not in seen:
      seen.add(bi); projected.append(bi)
  projected.append(cb)
  current=extract_toda_group_proof_narrative_argument_local_body_blocks(
    presentation,blocks,sidecar,arguments,argument_index
  )
  current_indices=tuple(block_index_by_identity[id(b)] for b in current)
  return current_indices,tuple(projected),tuple(entries),tuple(ordered)

def _exactness(indices,blocks):
  return sum(blocks[i].role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS for i in indices)

def _role_counts(indices,blocks):
  return dict(Counter(blocks[i].role.value for i in indices))

def _summaries_for_target(n,k):
  presentation,blocks,sidecar,arguments=_data(n,k)
  rows=[]
  for ai,argument in enumerate(arguments):
    current,simulated,entries,visited=_simulation(presentation,blocks,sidecar,arguments,ai)
    current_set=frozenset(current[:-1]); simulated_set=frozenset(simulated[:-1])
    rows.append({
      "argument_index":ai,"role":argument.role.value,
      "current_blocks":len(current),"current_exactness":_exactness(current,blocks),
      "simulated_blocks":len(simulated),"simulated_exactness":_exactness(simulated,blocks),
      "removed_blocks":len(current_set-simulated_set),"added_blocks":len(simulated_set-current_set),
      "entry_steps":len(entries),"visited_steps":len(visited),
      "simulated_role_counts":_role_counts(simulated,blocks),
      "current_indices":current,"simulated_indices":simulated,
    })
  return presentation,blocks,arguments,rows

def main():
  print("Phase 144-6 R25-29 Entry-Step-Preserving Block Dependency Audit")
  print("Production changes: none")
  for n,k in TARGETS:
    presentation,blocks,arguments,rows=_summaries_for_target(n,k)
    print("\n"+"="*78); print(f"pi_{n+k}^{n}"); print("="*78)
    print("steps:",len(presentation.nodes),"blocks:",len(blocks),"arguments:",len(arguments))
    largest=sorted(rows,key=lambda r:(r["current_blocks"],r["removed_blocks"]),reverse=True)[:10]
    for r in largest:
      print(f'argument {r["argument_index"]:03d} role={r["role"]}')
      print(f'  current: blocks={r["current_blocks"]} exactness={r["current_exactness"]}')
      print(f'  entry-step-preserving: blocks={r["simulated_blocks"]} exactness={r["simulated_exactness"]} entry_steps={r["entry_steps"]} visited_steps={r["visited_steps"]}')
      print(f'  delta: removed={r["removed_blocks"]} added={r["added_blocks"]}')
      print("  simulated roles:",r["simulated_role_counts"])
    print("target summary:")
    print("  max current blocks:",max(r["current_blocks"] for r in rows))
    print("  max simulated blocks:",max(r["simulated_blocks"] for r in rows))
    print("  max current exactness:",max(r["current_exactness"] for r in rows))
    print("  max simulated exactness:",max(r["simulated_exactness"] for r in rows))
    print("  arguments reduced:",sum(r["simulated_blocks"]<r["current_blocks"] for r in rows),"/",len(rows))
    print("  arguments expanded:",sum(r["simulated_blocks"]>r["current_blocks"] for r in rows),"/",len(rows))
  _,_,_,rows=_summaries_for_target(3,3)
  print("\n"+"="*78); print("pi_6^3 preservation check"); print("="*78)
  for r in rows:
    print(f'argument {r["argument_index"]:03d} role={r["role"]} current={r["current_blocks"]}/{r["current_exactness"]} simulated={r["simulated_blocks"]}/{r["simulated_exactness"]} removed={r["removed_blocks"]} added={r["added_blocks"]}')

if __name__=="__main__": main()
