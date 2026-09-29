from collections import Counter

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
    di=step_index_by_id[id(dependent)]
    pi=step_index_by_id[id(prerequisite)]
    if pi not in deps[di]:
      deps[di].append(pi)
    kinds[di].setdefault(pi,[]).append(kind)
  for edge in presentation.edges:
    add(edge.parent_step,edge.premise_step,"proof")
  for semantic in sidecar.dependency_semantics:
    add(semantic.dependent_step,semantic.prerequisite_step,"semantic")
  return tuple(tuple(row) for row in deps),tuple(kinds)

def _closure(deps,starts,boundary_steps):
  visited=set()
  active=set()
  def visit(si):
    if si in boundary_steps or si in visited or si in active:
      return
    active.add(si)
    for di in deps[si]:
      visit(di)
    active.remove(si)
    visited.add(si)
  for si in starts:
    visit(si)
  return frozenset(visited)

def _project(step_indices,presentation,block_index_by_step_id):
  return frozenset(
    block_index_by_step_id[id(presentation.nodes[si].proof_step)]
    for si in step_indices
  )

def _exactness(block_indices,blocks):
  return sum(
    blocks[bi].role
    is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    for bi in block_indices
  )

def _statement_type(presentation,si):
  return type(presentation.nodes[si].proof_step.conclusion).__name__

def _rule_name(presentation,si):
  rule=presentation.nodes[si].proof_step.inference_rule
  return None if rule is None else rule.name

def _audit_target(n,k):
  presentation,blocks,sidecar,arguments=_data(n,k)
  step_index_by_id,block_index_by_step_id,block_index_by_identity=_indices(presentation,blocks)
  deps,kinds=_dependencies(presentation,sidecar,step_index_by_id)

  conclusion_block_by_argument=tuple(
    block_index_by_identity[id(argument.conclusion_block)]
    for argument in arguments
  )
  owner_arguments_by_block={}
  for ai,bi in enumerate(conclusion_block_by_argument):
    owner_arguments_by_block.setdefault(bi,[]).append(ai)

  conclusion_steps_by_argument=tuple(
    frozenset(step_index_by_id[id(step)] for step in argument.conclusion_block.steps)
    for argument in arguments
  )

  rows=[]
  for ai,argument in enumerate(arguments):
    if argument.role.value not in AUDITED_ROLES:
      continue

    current_steps=conclusion_steps_by_argument[ai]
    other_boundary_steps=frozenset(
      si
      for oi,step_indices in enumerate(conclusion_steps_by_argument)
      if oi!=ai
      for si in step_indices
    )

    entries=[]
    for conclusion_step in current_steps:
      for entry_step in deps[conclusion_step]:
        if entry_step in current_steps:
          continue
        if entry_step in entries:
          continue
        entries.append(entry_step)

    entry_rows=[]
    for entry_step in entries:
      entry_block=block_index_by_step_id[id(presentation.nodes[entry_step].proof_step)]
      owners=tuple(
        owner
        for owner in owner_arguments_by_block.get(entry_block,())
        if owner!=ai
      )
      is_boundary=bool(owners)

      if is_boundary:
        entry_rows.append({
          "classification":"argument_boundary",
          "step":entry_step,
          "block":entry_block,
          "type":_statement_type(presentation,entry_step),
          "rule":_rule_name(presentation,entry_step),
          "kinds":tuple(
            kind
            for conclusion_step in current_steps
            for kind in kinds[conclusion_step].get(entry_step,())
          ),
          "owner_arguments":owners,
          "owner_roles":tuple(arguments[owner].role.value for owner in owners),
          "blocks":0,
          "steps":0,
          "exactness":0,
          "children":(),
        })
        continue

      entry_closure=_closure(
        deps,
        (entry_step,),
        other_boundary_steps|current_steps,
      )
      entry_blocks=_project(
        entry_closure,
        presentation,
        block_index_by_step_id,
      )

      child_rows=[]
      for child_step in deps[entry_step]:
        child_block=block_index_by_step_id[id(presentation.nodes[child_step].proof_step)]
        child_owners=tuple(
          owner
          for owner in owner_arguments_by_block.get(child_block,())
          if owner!=ai
        )
        if child_owners:
          child_rows.append({
            "classification":"argument_boundary",
            "step":child_step,
            "block":child_block,
            "type":_statement_type(presentation,child_step),
            "rule":_rule_name(presentation,child_step),
            "kinds":tuple(kinds[entry_step].get(child_step,())),
            "owner_arguments":child_owners,
            "owner_roles":tuple(arguments[owner].role.value for owner in child_owners),
            "blocks":0,
            "steps":0,
            "exactness":0,
          })
          continue

        child_closure=_closure(
          deps,
          (child_step,),
          other_boundary_steps|current_steps,
        )
        child_blocks=_project(
          child_closure,
          presentation,
          block_index_by_step_id,
        )
        child_rows.append({
          "classification":"owned",
          "step":child_step,
          "block":child_block,
          "type":_statement_type(presentation,child_step),
          "rule":_rule_name(presentation,child_step),
          "kinds":tuple(kinds[entry_step].get(child_step,())),
          "owner_arguments":(),
          "owner_roles":(),
          "blocks":len(child_blocks),
          "steps":len(child_closure),
          "exactness":_exactness(child_blocks,blocks),
        })

      child_rows.sort(
        key=lambda row:(
          row["classification"]=="owned",
          row["blocks"],
          row["steps"],
        ),
        reverse=True,
      )

      entry_rows.append({
        "classification":"owned",
        "step":entry_step,
        "block":entry_block,
        "type":_statement_type(presentation,entry_step),
        "rule":_rule_name(presentation,entry_step),
        "kinds":tuple(
          kind
          for conclusion_step in current_steps
          for kind in kinds[conclusion_step].get(entry_step,())
        ),
        "owner_arguments":(),
        "owner_roles":(),
        "blocks":len(entry_blocks),
        "steps":len(entry_closure),
        "exactness":_exactness(entry_blocks,blocks),
        "children":tuple(child_rows),
      })

    rows.append({
      "argument_index":ai,
      "role":argument.role.value,
      "declared_child_arguments":argument.child_argument_indices,
      "entries":tuple(entry_rows),
    })

  return presentation,blocks,arguments,rows

def main():
  print("Phase 144-6 R25-30-R3 Argument-Boundary Entry Classification Audit")
  print("Production changes: none")
  print("Existing repository test changes: none")

  for n,k in TARGETS:
    presentation,blocks,arguments,rows=_audit_target(n,k)
    print("\\n"+"="*78)
    print(f"pi_{n+k}^{n}")
    print("="*78)
    print("steps:",len(presentation.nodes),"blocks:",len(blocks),"arguments:",len(arguments))

    classifications=Counter()
    for row in rows:
      classifications.update(entry["classification"] for entry in row["entries"])
      print(
        f'argument {row["argument_index"]:03d} '
        f'role={row["role"]} '
        f'declared_child_arguments={row["declared_child_arguments"]}'
      )
      for ei,entry in enumerate(row["entries"]):
        print(
          f'  entry {ei}: classification={entry["classification"]} '
          f'S{entry["step"]} B{entry["block"]} type={entry["type"]}'
        )
        print(
          f'    edge_kinds={entry["kinds"]} '
          f'owners={entry["owner_arguments"]} '
          f'owner_roles={entry["owner_roles"]}'
        )
        print(f'    rule={entry["rule"]!r}')
        if entry["classification"]=="argument_boundary":
          print("    traversal=STOP")
          continue

        print(
          f'    closure: blocks={entry["blocks"]} '
          f'steps={entry["steps"]} exactness={entry["exactness"]}'
        )
        large_children=sum(
          child["classification"]=="owned"
          and child["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD
          for child in entry["children"]
        )
        boundary_children=sum(
          child["classification"]=="argument_boundary"
          for child in entry["children"]
        )
        print(
          f'    children={len(entry["children"])} '
          f'large_owned_children={large_children} '
          f'boundary_children={boundary_children}'
        )
        for ci,child in enumerate(entry["children"][:12]):
          print(
            f'    child {ci}: classification={child["classification"]} '
            f'S{child["step"]} B{child["block"]} '
            f'type={child["type"]} edge_kinds={child["kinds"]}'
          )
          if child["classification"]=="argument_boundary":
            print(
              f'      owners={child["owner_arguments"]} '
              f'owner_roles={child["owner_roles"]} traversal=STOP'
            )
          else:
            print(
              f'      blocks={child["blocks"]} '
              f'steps={child["steps"]} exactness={child["exactness"]}'
            )
          print(f'      rule={child["rule"]!r}')

    print("classification summary:",dict(classifications))

  print("\\n"+"="*78)
  print("Cross-target ownership summary")
  print("="*78)
  for n,k in TARGETS:
    _,_,arguments,rows=_audit_target(n,k)
    boundary_entries=[
      (row,entry)
      for row in rows
      for entry in row["entries"]
      if entry["classification"]=="argument_boundary"
    ]
    owned_giant_entries=[
      (row,entry)
      for row in rows
      for entry in row["entries"]
      if (
        entry["classification"]=="owned"
        and entry["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD
      )
    ]
    declared_pairs={
      (row["argument_index"],child)
      for row in rows
      for child in row["declared_child_arguments"]
    }
    classified_pairs={
      (row["argument_index"],owner)
      for row,entry in boundary_entries
      for owner in entry["owner_arguments"]
    }
    print(
      f"pi_{n+k}^{n}: "
      f"boundary_entries={len(boundary_entries)} "
      f"owned_giant_entries={len(owned_giant_entries)} "
      f"declared_child_pairs={len(declared_pairs)} "
      f"classified_boundary_pairs={len(classified_pairs)} "
      f"pair_match={declared_pairs==classified_pairs}"
    )

if __name__=="__main__":
  main()
