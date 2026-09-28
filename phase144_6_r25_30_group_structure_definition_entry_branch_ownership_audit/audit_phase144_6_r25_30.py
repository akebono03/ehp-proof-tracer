from collections import deque

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import build_toda_group_proof_narrative_arguments
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay

TARGETS=((5,7),(8,7),(9,7))
AUDITED_ROLES=frozenset(("establish_group_structure","establish_definition"))
LARGE_BRANCH_BLOCK_THRESHOLD=900

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

def _dependencies(presentation,sidecar,step_index_by_id):
  deps=[[] for _ in presentation.nodes]
  kinds=[{} for _ in presentation.nodes]
  def add(dependent,prerequisite,kind):
    di=step_index_by_id[id(dependent)]; pi=step_index_by_id[id(prerequisite)]
    if pi not in deps[di]: deps[di].append(pi)
    kinds[di].setdefault(pi,[]).append(kind)
  for edge in presentation.edges: add(edge.parent_step,edge.premise_step,"proof")
  for semantic in sidecar.dependency_semantics: add(semantic.dependent_step,semantic.prerequisite_step,"semantic")
  return tuple(tuple(r) for r in deps),tuple(kinds)

def _closure(deps,starts,excluded=frozenset()):
  visited=set(); active=set()
  def visit(si):
    if si in excluded or si in visited or si in active: return
    active.add(si)
    for di in deps[si]: visit(di)
    active.remove(si); visited.add(si)
  for si in starts: visit(si)
  return frozenset(visited)

def _project(step_indices,presentation,block_index_by_step_id):
  return frozenset(block_index_by_step_id[id(presentation.nodes[si].proof_step)] for si in step_indices)

def _exactness(block_indices,blocks):
  return sum(blocks[bi].role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS for bi in block_indices)

def _statement_type(presentation,step_index):
  return type(presentation.nodes[step_index].proof_step.conclusion).__name__

def _rule_name(presentation,step_index):
  rule=presentation.nodes[step_index].proof_step.inference_rule
  return None if rule is None else rule.name

def _shortest_contact(deps,start,boundary_owner_by_step):
  queue=deque(((start,(start,)),)); seen={start}
  while queue:
    current,path=queue.popleft()
    owners=boundary_owner_by_step.get(current,())
    if owners: return path,owners
    for child in deps[current]:
      if child in seen: continue
      seen.add(child); queue.append((child,path+(child,)))
  return (),()

def _argument_rows(n,k):
  presentation,blocks,sidecar,arguments=_data(n,k)
  step_index_by_id,block_index_by_step_id,block_index_by_identity=_indices(presentation,blocks)
  deps,kinds=_dependencies(presentation,sidecar,step_index_by_id)
  conclusion_steps=[]
  for argument in arguments:
    conclusion_steps.append(frozenset(step_index_by_id[id(s)] for s in argument.conclusion_block.steps))
  rows=[]
  for ai,argument in enumerate(arguments):
    if argument.role.value not in AUDITED_ROLES: continue
    current_conclusion=conclusion_steps[ai]
    other_boundary=frozenset(si for oi,ss in enumerate(conclusion_steps) if oi!=ai for si in ss)
    boundary_owner={}
    for oi,ss in enumerate(conclusion_steps):
      if oi==ai: continue
      for si in ss: boundary_owner.setdefault(si,[]).append(oi)
    entries=[]
    for csi in current_conclusion:
      for di in deps[csi]:
        if di in current_conclusion: continue
        if di not in entries: entries.append(di)
    entry_rows=[]
    for entry in entries:
      entry_closure=_closure(deps,(entry,),excluded=other_boundary|current_conclusion)
      entry_blocks=_project(entry_closure,presentation,block_index_by_step_id)
      child_rows=[]
      for child in deps[entry]:
        if child in other_boundary or child in current_conclusion: continue
        child_closure=_closure(deps,(child,),excluded=other_boundary|current_conclusion|{entry})
        child_blocks=_project(child_closure,presentation,block_index_by_step_id)
        path,owners=_shortest_contact(deps,child,boundary_owner)
        child_rows.append({
          "step":child,"block":block_index_by_step_id[id(presentation.nodes[child].proof_step)],
          "type":_statement_type(presentation,child),"rule":_rule_name(presentation,child),
          "blocks":len(child_blocks),"steps":len(child_closure),"exactness":_exactness(child_blocks,blocks),
          "contact_path":path,"contact_owners":tuple(owners),
          "kinds":tuple(kinds[entry].get(child,())),
        })
      child_rows.sort(key=lambda r:(r["blocks"],r["steps"]),reverse=True)
      entry_rows.append({
        "step":entry,"block":block_index_by_step_id[id(presentation.nodes[entry].proof_step)],
        "type":_statement_type(presentation,entry),"rule":_rule_name(presentation,entry),
        "blocks":len(entry_blocks),"steps":len(entry_closure),"exactness":_exactness(entry_blocks,blocks),
        "children":child_rows,
      })
    entry_rows.sort(key=lambda r:(r["blocks"],r["steps"]),reverse=True)
    rows.append({"argument_index":ai,"role":argument.role.value,"entries":entry_rows})
  return presentation,blocks,arguments,rows

def main():
  print("Phase 144-6 R25-30 Group-Structure / Definition Entry-Branch Ownership Audit")
  print("Production changes: none")
  for n,k in TARGETS:
    presentation,blocks,arguments,rows=_argument_rows(n,k)
    print("\\n"+"="*78); print(f"pi_{n+k}^{n}"); print("="*78)
    print("steps:",len(presentation.nodes),"blocks:",len(blocks),"arguments:",len(arguments))
    for row in rows:
      if not row["entries"]: continue
      max_blocks=max(e["blocks"] for e in row["entries"])
      if max_blocks<LARGE_BRANCH_BLOCK_THRESHOLD: continue
      print(f'argument {row["argument_index"]:03d} role={row["role"]} entries={len(row["entries"])}')
      for ei,e in enumerate(row["entries"]):
        print(f'  entry {ei}: S{e["step"]} B{e["block"]} type={e["type"]} blocks={e["blocks"]} steps={e["steps"]} exactness={e["exactness"]}')
        print(f'    rule={e["rule"]!r}')
        print(f'    children={len(e["children"])} large_children={sum(c["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD for c in e["children"])}')
        for ci,c in enumerate(e["children"][:12]):
          print(f'    child {ci}: S{c["step"]} B{c["block"]} kinds={c["kinds"]} type={c["type"]} blocks={c["blocks"]} steps={c["steps"]} exactness={c["exactness"]}')
          print(f'      rule={c["rule"]!r}')
          if c["contact_path"]:
            print("      nearest other-argument contact:", " -> ".join(f"S{x}" for x in c["contact_path"]), "owners=",c["contact_owners"])
          else:
            print("      nearest other-argument contact: none")
  print("\\n"+"="*78)
  print("Interpretation counters")
  print("="*78)
  for n,k in TARGETS:
    _,_,_,rows=_argument_rows(n,k)
    audited=sum(1 for r in rows if r["entries"])
    giant=sum(1 for r in rows if r["entries"] and max(e["blocks"] for e in r["entries"])>=LARGE_BRANCH_BLOCK_THRESHOLD)
    single=sum(1 for r in rows for e in r["entries"] if e["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD and sum(c["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD for c in e["children"])==1)
    multi=sum(1 for r in rows for e in r["entries"] if e["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD and sum(c["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD for c in e["children"])>1)
    print(f"pi_{n+k}^{n}: audited_arguments={audited} giant_arguments={giant} giant_entries_single_large_child={single} giant_entries_multi_large_child={multi}")

if __name__=="__main__": main()
