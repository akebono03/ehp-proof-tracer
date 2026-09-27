from collections import Counter, defaultdict
from dataclasses import fields, is_dataclass
from enum import Enum

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  HomotopyGroup,
  TodaPrimaryGroup,
)
from proof import Relation, RelationType
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_aggregate_statement_catalog import is_toda_group_proof_aggregate_statement
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
)

TARGETS = ((3, 3), (5, 3), (4, 6), (5, 7), (8, 7), (9, 7))


class EvidenceFunction(Enum):
  ESTABLISH = "ESTABLISH"
  COMPUTE = "COMPUTE"
  EXACTNESS = "EXACTNESS"
  TRANSPORT = "TRANSPORT"
  REFERENCE = "REFERENCE"
  SUPPORT_ONLY = "SUPPORT_ONLY"


class SupportRelation(Enum):
  CLAIM_INPUT = "CLAIM_INPUT"
  PROVIDER_INPUT = "PROVIDER_INPUT"
  REFERENCE_INPUT = "REFERENCE_INPUT"
  DEFINITION_INPUT = "DEFINITION_INPUT"
  STRUCTURAL_INPUT = "STRUCTURAL_INPUT"
  COMPUTATION_INPUT = "COMPUTATION_INPUT"
  PRECONDITION_INPUT = "PRECONDITION_INPUT"
  MAP_INPUT = "MAP_INPUT"
  AGGREGATE_INPUT = "AGGREGATE_INPUT"
  RESIDUAL_SUPPORT = "RESIDUAL_SUPPORT"


def group_result(n, k):
  return build_standard_toda_report(n=n, k=k).candidates[0].source_candidate.group_result


def full_state(result):
  provenance = extract_toda_recursive_proof_provenance(result)
  full_depth = max(node.shortest_depth for node in provenance.nodes)
  replay = build_toda_group_result_proof_replay(result, max_depth=full_depth)
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
  blocks = build_toda_group_proof_narrative_blocks(presentation, semantic_sidecar=sidecar)
  arguments = build_toda_group_proof_narrative_arguments(
    presentation, blocks, semantic_sidecar=sidecar
  )
  transitions = extract_toda_group_proof_narrative_transitions(
    presentation, blocks, arguments
  )
  return provenance, full_depth, presentation, sidecar, blocks, arguments, transitions


def final_components(presentation):
  s = presentation.root_step.conclusion
  if not (
    isinstance(s, Relation)
    and s.relation_type is RelationType.EQUALITY
    and isinstance(s.lhs, TodaPrimaryGroup)
  ):
    return ()
  target, structure = s.lhs, s.rhs
  summands = structure.summands if isinstance(structure, DirectSumGroup) else (structure,)
  out = []
  for summand in summands:
    if isinstance(summand, FreeCyclicGroup):
      out.append(("generator", target, summand.generator, None))
    elif isinstance(summand, FiniteCyclicGroup):
      out.append(("generator", target, summand.generator, None))
      out.append(("order", target, summand.generator, summand.order))
  return tuple(out)


def required_claim_arguments(arguments, comps):
  out = []
  for index, argument in enumerate(arguments):
    subject = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
    include = argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION:
      include = any(c[2] == subject for c in comps)
    if argument.role is TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER:
      step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
      s = None if step is None else step.conclusion
      include = (
        isinstance(s, Relation)
        and s.relation_type is RelationType.ORDER
        and any(c[0] == "order" and c[2] == subject and c[3] == s.rhs for c in comps)
      )
    if include:
      out.append((index, argument))
  return tuple(out)


def provider_steps(presentation, provenance, comps):
  out = []
  for node in provenance.nodes:
    step, s = node.proof_step, node.proof_step.conclusion
    if isinstance(s, TodaProp515Pi12_5HopfIsomorphismStatement):
      if any(c[1] == s.map.source_group for c in comps):
        out.append(step)
    elif isinstance(s, Toda515Sigma8TransportedDecompositionStatement):
      if any(c[1] == s.prop44_isomorphism.map.target_group for c in comps):
        out.append(step)
    elif isinstance(s, Toda48Pi16_9OrderAndE4InjectiveStatement):
      if any(c[0] == "order" and c[1] == s.target_group and c[3] == s.target_order for c in comps):
        out.append(step)
  for step in presentation.root_step.premises:
    if isinstance(
      step.conclusion,
      (
        Toda56Nu4DecompositionStatement,
        Toda515Sigma8TransportedDecompositionStatement,
        TodaProp515Pi12_5HopfIsomorphismStatement,
        Toda48Pi16_9OrderAndE4InjectiveStatement,
      ),
    ):
      out.append(step)
  unique, seen = [], set()
  for step in out:
    key = (type(step.conclusion).__name__, repr(step.conclusion))
    if key not in seen:
      seen.add(key)
      unique.append(step)
  return tuple(unique)


def block_by_step_id(blocks):
  return {id(step): block for block in blocks for step in block.steps}


def r4_visible_ids(presentation, blocks, sidecar, arguments, claims):
  visible = set()
  for index, argument in claims:
    local = extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation, blocks, sidecar, arguments, index
    )
    hidden = _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation, blocks, local, sidecar, argument
    )
    visible.update(
      id(step)
      for block in local
      for step in block.steps
      if id(step) not in hidden
    )
  return visible


def transition_roles_by_edge(transitions):
  roles = defaultdict(set)
  for transition in transitions:
    for source in transition.source_blocks:
      roles[(id(source), id(transition.target_block))].add(transition.role)
  return roles


def classify_evidence_function(premise_step, parent_step, premise_block, parent_block, transition_roles):
  if extract_toda_group_proof_step_literature_reference(premise_step) is not None:
    return EvidenceFunction.REFERENCE
  edge_roles = transition_roles.get((id(premise_block), id(parent_block)), set())
  if (
    TodaGroupProofNarrativeTransitionRole.CALCULATION_CHAIN in edge_roles
    or (
      premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
      and parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
    )
  ):
    return EvidenceFunction.COMPUTE
  if (
    premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    or parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ):
    return EvidenceFunction.EXACTNESS
  if (
    premise_block.role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    and parent_block.role in (
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.TRANSPORT
  if (
    TodaGroupProofNarrativeTransitionRole.DERIVATION in edge_roles
    or parent_block.role in (
      TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
    )
  ):
    return EvidenceFunction.ESTABLISH
  return EvidenceFunction.SUPPORT_ONLY


def classify_support_relation(
  premise_block,
  parent_block,
  parent_is_claim,
  parent_is_provider,
):
  if parent_is_provider:
    return SupportRelation.PROVIDER_INPUT
  if parent_is_claim:
    return SupportRelation.CLAIM_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    return SupportRelation.REFERENCE_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    return SupportRelation.DEFINITION_INPUT
  if parent_block.role in (
    TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
  ):
    return SupportRelation.STRUCTURAL_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION:
    return SupportRelation.COMPUTATION_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    return SupportRelation.PRECONDITION_INPUT
  if parent_block.role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    return SupportRelation.MAP_INPUT
  if (
    any(is_toda_group_proof_aggregate_statement(step.conclusion) for step in parent_block.steps)
    or any(is_toda_group_proof_aggregate_statement(step.conclusion) for step in premise_block.steps)
  ):
    return SupportRelation.AGGREGATE_INPUT
  return SupportRelation.RESIDUAL_SUPPORT


def value_shape(value):
  if isinstance(value, TodaPrimaryGroup):
    return "toda_primary_group"
  if isinstance(value, HomotopyGroup):
    return "homotopy_group"
  if (
    is_dataclass(value)
    and hasattr(value, "source_group")
    and hasattr(value, "target_group")
  ):
    return "homotopy_map"
  if isinstance(value, DirectSumGroup):
    return "direct_sum_group"
  if isinstance(value, FiniteCyclicGroup):
    return "finite_cyclic_group"
  if isinstance(value, FreeCyclicGroup):
    return "free_cyclic_group"
  if isinstance(value, Relation):
    return "relation"
  if isinstance(value, bool):
    return "bool"
  if isinstance(value, int):
    return "int"
  if isinstance(value, str):
    return "str"
  if isinstance(value, tuple):
    inner = sorted({value_shape(item) for item in value})
    return "tuple[" + ",".join(inner) + "]"
  if isinstance(value, list):
    inner = sorted({value_shape(item) for item in value})
    return "list[" + ",".join(inner) + "]"
  if is_dataclass(value):
    return "dataclass"
  return type(value).__name__


def statement_shape(statement):
  if isinstance(statement, Relation):
    return (
      "relation:"
      + statement.relation_type.value
      + ":"
      + value_shape(statement.lhs)
      + "->"
      + value_shape(statement.rhs)
    )
  if not is_dataclass(statement):
    return "opaque:" + type(statement).__name__
  shapes = []
  for field in fields(statement):
    value = getattr(statement, field.name)
    shapes.append(value_shape(value))
  return "dataclass{" + ",".join(sorted(shapes)) + "}"


def semantic_features(statement):
  features = set()
  if isinstance(statement, Relation):
    features.add("RELATION")
    if statement.relation_type is RelationType.EQUALITY:
      features.add("EQUALITY")
    if statement.relation_type is RelationType.ORDER:
      features.add("ORDER_RELATION")
    for value in (statement.lhs, statement.rhs):
      features.add(value_shape(value).upper())
    return tuple(sorted(features))

  if is_dataclass(statement):
    for field in fields(statement):
      value = getattr(statement, field.name)
      shape = value_shape(value)
      if shape in ("toda_primary_group", "homotopy_group"):
        features.add("GROUP_FIELD")
      elif shape == "homotopy_map":
        features.add("MAP_FIELD")
      elif shape == "relation":
        features.add("RELATION_FIELD")
      elif shape in ("direct_sum_group", "finite_cyclic_group", "free_cyclic_group"):
        features.add("GROUP_STRUCTURE_FIELD")
      elif shape == "bool":
        features.add("BOOLEAN_PROPERTY")
      elif shape == "int":
        features.add("INTEGER_PARAMETER")
      elif shape == "dataclass":
        features.add("NESTED_SEMANTIC_OBJECT")
      elif shape.startswith("tuple[") or shape.startswith("list["):
        features.add("COLLECTION_FIELD")
      else:
        features.add("DOMAIN_OBJECT_FIELD")

  name = type(statement).__name__.lower()
  # These lexical flags are audit labels only. They are never used to decide
  # visibility or to classify a production rule.
  if "isomorphism" in name:
    features.add("AUDIT_NAME_HINT_ISOMORPHISM")
  if "finitedimensional" in name:
    features.add("AUDIT_NAME_HINT_FINITE_DIMENSIONAL")
  if "lemma" in name:
    features.add("AUDIT_NAME_HINT_LEMMA")
  if "decomposition" in name:
    features.add("AUDIT_NAME_HINT_DECOMPOSITION")
  return tuple(sorted(features))


def main():
  print("=" * 142)
  print("Phase 144-6-R5-15J typed provider-input / residual statement-shape audit")
  print("=" * 142)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("Visibility is NOT classified by statement class name or inference-rule name.")
  print("Structural shapes use dataclass field value types; lexical name hints are printed only as diagnostics.")
  print()

  provider_rows = []
  residual_rows = []

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments, transitions = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    visible = r4_visible_ids(presentation, blocks, sidecar, arguments, claims)
    blocks_by_step = block_by_step_id(blocks)
    transition_roles = transition_roles_by_edge(transitions)

    claim_steps = {
      id(step)
      for _, argument in claims
      for step in (extract_toda_group_proof_narrative_argument_conclusion_step(argument),)
      if step is not None
    }
    provider_ids = {id(step) for step in providers}

    for edge in provenance.edges:
      premise, parent = edge.premise_step, edge.parent_step
      premise_block = blocks_by_step.get(id(premise))
      parent_block = blocks_by_step.get(id(parent))
      if premise_block is None or parent_block is None:
        continue
      function = classify_evidence_function(
        premise, parent, premise_block, parent_block, transition_roles
      )
      if function is not EvidenceFunction.SUPPORT_ONLY:
        continue
      relation = classify_support_relation(
        premise_block,
        parent_block,
        id(parent) in claim_steps,
        id(parent) in provider_ids,
      )
      row = {
        "target": (n, k),
        "visible": id(premise) in visible,
        "relation": relation,
        "premise_role": premise_block.role,
        "parent_role": parent_block.role,
        "premise": premise.conclusion,
        "parent": parent.conclusion,
        "shape": statement_shape(premise.conclusion),
        "features": semantic_features(premise.conclusion),
      }
      if relation is SupportRelation.PROVIDER_INPUT:
        provider_rows.append(row)
      if relation is SupportRelation.RESIDUAL_SUPPORT:
        residual_rows.append(row)

  print("DIRECT PROVIDER_INPUT INVENTORY")
  print("-" * 142)
  for row in provider_rows:
    print(
      f"target={row['target']} visible={'Y' if row['visible'] else 'N'} "
      f"premise_role={row['premise_role'].value:<15} parent_role={row['parent_role'].value:<15} "
      f"premise={type(row['premise']).__name__:<52} parent={type(row['parent']).__name__}"
    )
    print(f"  shape={row['shape']}")
    print(f"  features={','.join(row['features'])}")

  print()
  print("PROVIDER_INPUT SHAPE COLLISIONS")
  print("-" * 142)
  by_shape = defaultdict(list)
  for row in provider_rows:
    by_shape[row["shape"]].append(row)
  for shape, rows in sorted(by_shape.items()):
    vis = Counter(row["visible"] for row in rows)
    print(
      f"shape={shape} total={len(rows)} visible={vis[True]} hidden={vis[False]} "
      f"mixed={'Y' if vis[True] and vis[False] else 'N'}"
    )
    for row in rows:
      print(
        f"  target={row['target']} visible={'Y' if row['visible'] else 'N'} "
        f"type={type(row['premise']).__name__} features={','.join(row['features'])}"
      )

  print()
  print("VISIBLE RESIDUAL_SUPPORT SHAPE COUNTS")
  print("-" * 142)
  visible_residual = [row for row in residual_rows if row["visible"]]
  visible_shapes = Counter(row["shape"] for row in visible_residual)
  for shape, count in visible_shapes.most_common():
    print(f"{count:4d} x {shape}")

  print()
  print("VISIBLE RESIDUAL_SUPPORT FEATURE COUNTS")
  print("-" * 142)
  feature_counts = Counter(
    feature
    for row in visible_residual
    for feature in row["features"]
  )
  for feature, count in feature_counts.most_common():
    print(f"{count:4d} x {feature}")

  print()
  print("VISIBLE/HIDDEN RESIDUAL SHAPE COLLISIONS")
  print("-" * 142)
  residual_by_shape = defaultdict(list)
  for row in residual_rows:
    residual_by_shape[row["shape"]].append(row)
  mixed_count = 0
  for shape, rows in sorted(residual_by_shape.items()):
    vis = Counter(row["visible"] for row in rows)
    if not (vis[True] and vis[False]):
      continue
    mixed_count += 1
    print(
      f"shape={shape} total={len(rows)} visible={vis[True]} hidden={vis[False]}"
    )
    visible_types = Counter(type(row["premise"]).__name__ for row in rows if row["visible"])
    hidden_types = Counter(type(row["premise"]).__name__ for row in rows if not row["visible"])
    print("  visible_types=" + ", ".join(f"{k}:{v}" for k, v in visible_types.most_common(8)))
    print("  hidden_types=" + ", ".join(f"{k}:{v}" for k, v in hidden_types.most_common(8)))

  print()
  print("VISIBLE RESIDUAL TYPE/SHAPE SAMPLES")
  print("-" * 142)
  seen = set()
  for row in visible_residual:
    key = (type(row["premise"]).__name__, row["shape"])
    if key in seen:
      continue
    seen.add(key)
    print(
      f"target={row['target']} premise_role={row['premise_role'].value:<15} "
      f"parent_role={row['parent_role'].value:<15} "
      f"premise={type(row['premise']).__name__:<52} parent={type(row['parent']).__name__}"
    )
    print(f"  shape={row['shape']}")
    print(f"  features={','.join(row['features'])}")
    if len(seen) >= 32:
      break

  print()
  print("=" * 142)
  print("SUMMARY")
  print("=" * 142)
  print(f"provider_input_total={len(provider_rows)}")
  print(f"provider_input_visible={sum(row['visible'] for row in provider_rows)}")
  print(f"provider_input_hidden={sum(not row['visible'] for row in provider_rows)}")
  print(f"provider_shape_count={len(by_shape)}")
  print(
    "provider_mixed_shape_count="
    + str(sum(
      1
      for rows in by_shape.values()
      if any(row['visible'] for row in rows)
      and any(not row['visible'] for row in rows)
    ))
  )
  print(f"residual_total={len(residual_rows)}")
  print(f"residual_visible={len(visible_residual)}")
  print(f"residual_hidden={sum(not row['visible'] for row in residual_rows)}")
  print(f"visible_residual_shape_count={len(visible_shapes)}")
  print(f"mixed_residual_shape_count={mixed_count}")
  print()
  print("INTERPRETATION")
  print("1. If provider visible/hidden inputs have distinct structural shapes, generic typed provider-input semantics may be sufficient.")
  print("2. If the same provider structural shape is both visible and hidden, field-type shape alone cannot decide Narrative relevance.")
  print("3. Name hints are diagnostics only and must not become production visibility rules.")
  print("4. A small number of visible residual shapes would support adding generic semantic statement-shape categories.")
  print("5. A large number of mixed visible/hidden residual shapes means structural shape still lacks consumer-purpose semantics.")
  print("6. Relation values and concrete field contents are deliberately excluded from the shape key to avoid target-specific matching.")
  print("7. The next step should add production metadata only if this audit identifies stable semantic categories across representative groups.")
  print("8. This audit does not change production visibility.")

if __name__ == "__main__":
  main()
