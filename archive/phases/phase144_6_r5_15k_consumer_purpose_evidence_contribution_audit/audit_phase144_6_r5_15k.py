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



class EvidenceContribution(Enum):
  ESTABLISH_GROUP = "ESTABLISH_GROUP"
  ESTABLISH_MAP = "ESTABLISH_MAP"
  ESTABLISH_ISOMORPHISM = "ESTABLISH_ISOMORPHISM"
  ESTABLISH_INJECTIVITY = "ESTABLISH_INJECTIVITY"
  ESTABLISH_SURJECTIVITY = "ESTABLISH_SURJECTIVITY"
  ESTABLISH_ZERO = "ESTABLISH_ZERO"
  ESTABLISH_ORDER = "ESTABLISH_ORDER"
  ESTABLISH_DECOMPOSITION = "ESTABLISH_DECOMPOSITION"
  ESTABLISH_RELATION = "ESTABLISH_RELATION"
  PROVIDE_REFERENCE = "PROVIDE_REFERENCE"
  PROVIDE_PRECONDITION = "PROVIDE_PRECONDITION"
  SHARED_SEMANTIC_INPUT = "SHARED_SEMANTIC_INPUT"
  UNRESOLVED = "UNRESOLVED"


def dataclass_values(value):
  if not is_dataclass(value):
    return ()
  return tuple(getattr(value, field.name) for field in fields(value))


def structurally_contains(container, needle):
  if container is needle or container == needle:
    return True
  if isinstance(container, (tuple, list)):
    return any(structurally_contains(item, needle) for item in container)
  if is_dataclass(container):
    return any(structurally_contains(value, needle) for value in dataclass_values(container))
  return False


def shared_semantic_values(premise, consumer):
  if not is_dataclass(consumer):
    return ()
  premise_values = dataclass_values(premise) if is_dataclass(premise) else (premise,)
  shared = []
  for consumer_value in dataclass_values(consumer):
    for premise_value in premise_values:
      if structurally_contains(consumer_value, premise_value) or structurally_contains(premise_value, consumer_value):
        shape = value_shape(consumer_value)
        if shape not in ("int", "bool", "str"):
          shared.append(shape)
  return tuple(sorted(set(shared)))


def consumer_purpose(consumer, parent_role):
  features = semantic_features(consumer)
  purposes = set()

  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE:
    purposes.add("GROUP_STRUCTURE")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.ORDER:
    purposes.add("ORDER")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    purposes.add("MAP_PROPERTY")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    purposes.add("DEFINITION")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION:
    purposes.add("CALCULATION")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    purposes.add("REFERENCE")
  if parent_role is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    purposes.add("PRECONDITION")

  if "MAP_FIELD" in features:
    purposes.add("MAP_STATEMENT")
  if "GROUP_FIELD" in features or "GROUP_STRUCTURE_FIELD" in features:
    purposes.add("GROUP_STATEMENT")
  if "ORDER_RELATION" in features:
    purposes.add("ORDER_STATEMENT")
  if "AUDIT_NAME_HINT_ISOMORPHISM" in features:
    purposes.add("AUDIT_ISOMORPHISM")
  if "AUDIT_NAME_HINT_DECOMPOSITION" in features:
    purposes.add("AUDIT_DECOMPOSITION")

  return tuple(sorted(purposes)) or ("UNCLASSIFIED_CONSUMER",)


def infer_contribution(premise, consumer, premise_role, parent_role):
  shared = shared_semantic_values(premise, consumer)
  premise_features = semantic_features(premise)
  consumer_features = semantic_features(consumer)

  if premise_role is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    return EvidenceContribution.PROVIDE_REFERENCE, shared
  if premise_role is TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    return EvidenceContribution.PROVIDE_PRECONDITION, shared
  if premise_role is TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE:
    return EvidenceContribution.ESTABLISH_GROUP, shared
  if premise_role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    if "AUDIT_NAME_HINT_ISOMORPHISM" in premise_features:
      return EvidenceContribution.ESTABLISH_ISOMORPHISM, shared
    return EvidenceContribution.ESTABLISH_MAP, shared
  if premise_role is TodaGroupProofNarrativeMathematicalBlockRole.ORDER:
    return EvidenceContribution.ESTABLISH_ORDER, shared

  if isinstance(premise, Relation):
    if premise.relation_type is RelationType.ZERO:
      return EvidenceContribution.ESTABLISH_ZERO, shared
    if premise.relation_type is RelationType.ORDER:
      return EvidenceContribution.ESTABLISH_ORDER, shared
    return EvidenceContribution.ESTABLISH_RELATION, shared

  if "AUDIT_NAME_HINT_ISOMORPHISM" in premise_features:
    return EvidenceContribution.ESTABLISH_ISOMORPHISM, shared
  if "AUDIT_NAME_HINT_DECOMPOSITION" in premise_features:
    return EvidenceContribution.ESTABLISH_DECOMPOSITION, shared

  if shared:
    return EvidenceContribution.SHARED_SEMANTIC_INPUT, shared

  return EvidenceContribution.UNRESOLVED, shared


def main():
  print("=" * 146)
  print("Phase 144-6-R5-15K consumer-purpose / evidence-contribution audit")
  print("=" * 146)
  print("Audit only. No production code, tests, or project documents are modified.")
  print("The audit studies SUPPORT_ONLY edges using consumer purpose plus premise contribution.")
  print("Statement/rule names are diagnostics only; they never decide visibility.")
  print()

  rows = []

  for n, k in TARGETS:
    result = group_result(n, k)
    provenance, full_depth, presentation, sidecar, blocks, arguments, transitions = full_state(result)
    comps = final_components(presentation)
    claims = required_claim_arguments(arguments, comps)
    providers = provider_steps(presentation, provenance, comps)
    visible = r4_visible_ids(presentation, blocks, sidecar, arguments, claims)
    blocks_by_step = block_by_step_id(blocks)
    transition_roles = transition_roles_by_edge(transitions)

    claim_ids = {
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
        id(parent) in claim_ids,
        id(parent) in provider_ids,
      )
      if relation not in (
        SupportRelation.PROVIDER_INPUT,
        SupportRelation.RESIDUAL_SUPPORT,
      ):
        continue

      contribution, shared = infer_contribution(
        premise.conclusion,
        parent.conclusion,
        premise_block.role,
        parent_block.role,
      )
      rows.append({
        "target": (n, k),
        "relation": relation,
        "visible": id(premise) in visible,
        "premise_role": premise_block.role,
        "parent_role": parent_block.role,
        "premise": premise.conclusion,
        "consumer": parent.conclusion,
        "purpose": consumer_purpose(parent.conclusion, parent_block.role),
        "contribution": contribution,
        "shared": shared,
      })

  provider_rows = [row for row in rows if row["relation"] is SupportRelation.PROVIDER_INPUT]
  residual_rows = [row for row in rows if row["relation"] is SupportRelation.RESIDUAL_SUPPORT]

  print("DIRECT PROVIDER_INPUT CONTRIBUTIONS")
  print("-" * 146)
  for row in provider_rows:
    print(
      f"target={row['target']} visible={'Y' if row['visible'] else 'N'} "
      f"contribution={row['contribution'].value:<26} "
      f"premise_role={row['premise_role'].value:<15} parent_role={row['parent_role'].value:<15}"
    )
    print(f"  purpose={','.join(row['purpose'])}")
    print(f"  shared={','.join(row['shared']) if row['shared'] else 'NONE'}")
    print(
      f"  premise={type(row['premise']).__name__} "
      f"consumer={type(row['consumer']).__name__}"
    )

  print()
  print("PROVIDER CONTRIBUTION VISIBILITY MATRIX")
  print("-" * 146)
  matrix = Counter(
    (row["contribution"].value, row["purpose"], row["visible"])
    for row in provider_rows
  )
  for (contribution, purpose, visible), count in sorted(matrix.items()):
    print(
      f"{contribution:<26} visible={'Y' if visible else 'N'} count={count:3d} "
      f"purpose={','.join(purpose)}"
    )

  print()
  print("VISIBLE RESIDUAL CONTRIBUTION COUNTS")
  print("-" * 146)
  visible_residual = [row for row in residual_rows if row["visible"]]
  visible_counts = Counter(row["contribution"].value for row in visible_residual)
  for contribution, count in visible_counts.most_common():
    print(f"{count:4d} x {contribution}")

  print()
  print("VISIBLE/HIDDEN RESIDUAL CONTRIBUTION COLLISIONS")
  print("-" * 146)
  by_key = defaultdict(list)
  for row in residual_rows:
    key = (row["contribution"].value, row["purpose"], row["shared"])
    by_key[key].append(row)

  mixed = []
  for key, key_rows in by_key.items():
    vis = Counter(row["visible"] for row in key_rows)
    if vis[True] and vis[False]:
      mixed.append((key, key_rows, vis))

  for (contribution, purpose, shared), key_rows, vis in sorted(
    mixed, key=lambda item: (-item[2][True], item[0][0], item[0][1])
  ):
    print(
      f"contribution={contribution:<26} visible={vis[True]:4d} hidden={vis[False]:4d} "
      f"purpose={','.join(purpose)} shared={','.join(shared) if shared else 'NONE'}"
    )
    visible_types = Counter(type(row["premise"]).__name__ for row in key_rows if row["visible"])
    hidden_types = Counter(type(row["premise"]).__name__ for row in key_rows if not row["visible"])
    print("  visible_types=" + ", ".join(f"{k}:{v}" for k, v in visible_types.most_common(6)))
    print("  hidden_types=" + ", ".join(f"{k}:{v}" for k, v in hidden_types.most_common(6)))

  print()
  print("VISIBLE UNRESOLVED / SHARED-SEMANTIC SAMPLES")
  print("-" * 146)
  samples = [
    row for row in visible_residual
    if row["contribution"] in (
      EvidenceContribution.UNRESOLVED,
      EvidenceContribution.SHARED_SEMANTIC_INPUT,
    )
  ]
  seen = set()
  for row in samples:
    key = (
      type(row["premise"]).__name__,
      type(row["consumer"]).__name__,
      row["contribution"].value,
      row["purpose"],
      row["shared"],
    )
    if key in seen:
      continue
    seen.add(key)
    print(
      f"target={row['target']} contribution={row['contribution'].value:<26} "
      f"premise_role={row['premise_role'].value:<15} parent_role={row['parent_role'].value:<15}"
    )
    print(
      f"  purpose={','.join(row['purpose'])} "
      f"shared={','.join(row['shared']) if row['shared'] else 'NONE'}"
    )
    print(
      f"  premise={type(row['premise']).__name__} "
      f"consumer={type(row['consumer']).__name__}"
    )
    if len(seen) >= 36:
      break

  print()
  print("=" * 146)
  print("SUMMARY")
  print("=" * 146)
  print(f"provider_input_total={len(provider_rows)}")
  print(f"provider_input_visible={sum(row['visible'] for row in provider_rows)}")
  print(f"provider_input_hidden={sum(not row['visible'] for row in provider_rows)}")
  print(f"provider_contribution_count={len(set(row['contribution'] for row in provider_rows))}")
  print(f"residual_total={len(residual_rows)}")
  print(f"residual_visible={len(visible_residual)}")
  print(f"residual_hidden={sum(not row['visible'] for row in residual_rows)}")
  print(f"visible_residual_contribution_count={len(visible_counts)}")
  print(f"visible_residual_unresolved={sum(row['contribution'] is EvidenceContribution.UNRESOLVED for row in visible_residual)}")
  print(f"visible_residual_shared_semantic={sum(row['contribution'] is EvidenceContribution.SHARED_SEMANTIC_INPUT for row in visible_residual)}")
  print(f"mixed_contribution_purpose_shared_keys={len(mixed)}")

  print()
  print("INTERPRETATION")
  print("1. The unit of analysis is the proof edge premise -> consumer, not the premise statement alone.")
  print("2. Consumer purpose combines generic Narrative block role with structural consumer features.")
  print("3. Evidence contribution is inferred from premise block role, relation kind, structural features, and semantic overlap.")
  print("4. Concrete n/k values and inference-rule names are not used.")
  print("5. Class-name hints inherited from 15J remain diagnostic features only; they do not decide visibility.")
  print("6. If provider visible/hidden inputs separate by contribution + consumer purpose, contribution semantics is promising.")
  print("7. If residual mixed collisions remain large, the next audit should inspect explicit typed semantic contribution metadata rather than add more graph heuristics.")
  print("8. This audit does not change production visibility.")

if __name__ == "__main__":
  main()
