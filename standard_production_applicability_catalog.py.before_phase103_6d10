from barratt_hilton_rules import (
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarSymbol,
  Suspension,
)
from map_property_rules import (
  InjectiveMapStatement,
)
from proof import (
  InferenceRule,
  Relation,
  RelationType,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  RuleRelevanceCategory,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
)


def _single_equality_premise_pattern(
  inference_rule: InferenceRule,
):
  patterns = (
    inference_rule.premise_patterns
  )

  if len(
    patterns
  ) != 1:
    return None

  pattern = patterns[
    0
  ]

  if (
    pattern.statement_type
    is not Relation
    or pattern.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      pattern.relation_pattern,
      Relation,
    )
    or pattern.relation_pattern.relation_type
    is not RelationType.EQUALITY
  ):
    return None

  return (
    pattern.relation_pattern
  )


def _is_equality_preserved_under_right_composition_rule(
  inference_rule: InferenceRule,
) -> bool:
  premise_relation = (
    _single_equality_premise_pattern(
      inference_rule
    )
  )

  conclusion = (
    inference_rule.conclusion_pattern
  )

  if (
    premise_relation is None
    or not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      conclusion.lhs,
      Composition,
    )
    or not isinstance(
      conclusion.rhs,
      Composition,
    )
  ):
    return False

  return (
    conclusion.lhs.left
    == premise_relation.lhs
    and conclusion.rhs.left
    == premise_relation.rhs
    and conclusion.lhs.right
    == conclusion.rhs.right
  )


def _is_equality_preserved_under_left_composition_rule(
  inference_rule: InferenceRule,
) -> bool:
  premise_relation = (
    _single_equality_premise_pattern(
      inference_rule
    )
  )

  conclusion = (
    inference_rule.conclusion_pattern
  )

  if (
    premise_relation is None
    or not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      conclusion.lhs,
      Composition,
    )
    or not isinstance(
      conclusion.rhs,
      Composition,
    )
  ):
    return False

  return (
    conclusion.lhs.left
    == conclusion.rhs.left
    and conclusion.lhs.right
    == premise_relation.lhs
    and conclusion.rhs.right
    == premise_relation.rhs
  )


def _is_equality_preserved_under_multiple_rule(
  inference_rule: InferenceRule,
) -> bool:
  premise_relation = (
    _single_equality_premise_pattern(
      inference_rule
    )
  )

  conclusion = (
    inference_rule.conclusion_pattern
  )

  if (
    premise_relation is None
    or not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      conclusion.lhs,
      Multiple,
    )
    or not isinstance(
      conclusion.rhs,
      Multiple,
    )
  ):
    return False

  return (
    conclusion.lhs.coefficient
    == conclusion.rhs.coefficient
    and conclusion.lhs.expression
    == premise_relation.lhs
    and conclusion.rhs.expression
    == premise_relation.rhs
  )


def _is_nested_integer_multiple_rule(
  inference_rule: InferenceRule,
) -> bool:
  if inference_rule.premise_patterns:
    return False

  conclusion = (
    inference_rule.conclusion_pattern
  )

  if (
    not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      conclusion.lhs,
      Multiple,
    )
    or not isinstance(
      conclusion.lhs.expression,
      Multiple,
    )
    or not isinstance(
      conclusion.rhs,
      Multiple,
    )
  ):
    return False

  outer = (
    conclusion.lhs.coefficient
  )

  inner = (
    conclusion
    .lhs
    .expression
    .coefficient
  )

  return (
    not isinstance(
      outer,
      bool,
    )
    and isinstance(
      outer,
      int,
    )
    and not isinstance(
      inner,
      bool,
    )
    and isinstance(
      inner,
      int,
    )
    and conclusion.rhs.coefficient
    == outer * inner
    and conclusion.rhs.expression
    == conclusion.lhs.expression.expression
  )


def _is_generic_relation_representative_rule(
  inference_rule: InferenceRule,
) -> bool:
  return (
    inference_rule
    == equality_symmetry_inference_rule()
    or inference_rule
    == equality_transitivity_inference_rule()
    or _is_equality_preserved_under_right_composition_rule(
      inference_rule
    )
    or _is_equality_preserved_under_left_composition_rule(
      inference_rule
    )
    or _is_equality_preserved_under_multiple_rule(
      inference_rule
    )
    or _is_nested_integer_multiple_rule(
      inference_rule
    )
  )


def _is_injective_map_reflection_rule(
  inference_rule: InferenceRule,
) -> bool:
  patterns = (
    inference_rule.premise_patterns
  )

  if len(
    patterns
  ) != 2:
    return False

  injective_pattern = patterns[
    0
  ]

  equality_pattern = patterns[
    1
  ]

  return (
    injective_pattern.proof_rule
    is None
    and injective_pattern.statement_type
    is InjectiveMapStatement
    and injective_pattern.statement_pattern
    is None
    and injective_pattern.relation_type
    is None
    and injective_pattern.relation_pattern
    is None
    and equality_pattern.proof_rule
    is None
    and equality_pattern.statement_type
    is Relation
    and equality_pattern.statement_pattern
    is None
    and equality_pattern.relation_type
    is RelationType.EQUALITY
    and equality_pattern.relation_pattern
    is None
    and inference_rule.conclusion_pattern
    is None
    and callable(
      inference_rule.conclusion_builder
    )
    and callable(
      inference_rule.match_guard
    )
  )


def _is_first_iterated_suspension_bridge_rule(
  inference_rule: InferenceRule,
) -> bool:
  if inference_rule.premise_patterns:
    return False

  conclusion_pattern = (
    inference_rule.conclusion_pattern
  )

  if not isinstance(
    conclusion_pattern,
    Relation,
  ):
    return False

  if (
    conclusion_pattern.relation_type
    is not RelationType.EQUALITY
  ):
    return False

  if not isinstance(
    conclusion_pattern.lhs,
    IteratedSuspension,
  ):
    return False

  if not isinstance(
    conclusion_pattern.rhs,
    Suspension,
  ):
    return False

  return (
    conclusion_pattern.lhs.exponent
    == 1
    and conclusion_pattern.lhs.expression
    == conclusion_pattern.rhs.expression
  )


def _barratt_hilton_representative_rules(
):
  alpha = HomotopyElement(
    name="phase103_alpha",
    dimension=1,
  )

  beta = HomotopyElement(
    name="phase103_beta",
    dimension=1,
  )

  p = ScalarSymbol(
    name="phase103_p",
  )

  q = ScalarSymbol(
    name="phase103_q",
  )

  k = ScalarSymbol(
    name="phase103_k",
  )

  h = ScalarSymbol(
    name="phase103_h",
  )

  return (
    barratt_hilton_first_inference_rule(
      alpha=alpha,
      beta=beta,
      p=p,
      q=q,
      k=k,
      h=h,
    ),
    barratt_hilton_second_inference_rule(
      alpha=alpha,
      beta=beta,
      p=p,
      q=q,
      k=k,
      h=h,
    ),
  )


_BARRATT_HILTON_REPRESENTATIVE_RULES = (
  _barratt_hilton_representative_rules()
)


def _same_nested_rule_factory(
  inference_rule: InferenceRule,
  representative_rule: InferenceRule,
) -> bool:
  inference_builder = (
    inference_rule.conclusion_builder
  )

  representative_builder = (
    representative_rule
    .conclusion_builder
  )

  inference_guard = (
    inference_rule.match_guard
  )

  representative_guard = (
    representative_rule
    .match_guard
  )

  return (
    callable(
      inference_builder
    )
    and callable(
      representative_builder
    )
    and callable(
      inference_guard
    )
    and callable(
      representative_guard
    )
    and getattr(
      inference_builder,
      "__code__",
      None,
    )
    is getattr(
      representative_builder,
      "__code__",
      None,
    )
    and getattr(
      inference_guard,
      "__code__",
      None,
    )
    is getattr(
      representative_guard,
      "__code__",
      None,
    )
  )


def _is_barratt_hilton_theorem_specific_rule(
  inference_rule: InferenceRule,
) -> bool:
  return any(
    _same_nested_rule_factory(
      inference_rule,
      representative_rule,
    )
    for representative_rule
    in _BARRATT_HILTON_REPRESENTATIVE_RULES
  )


def _representative_relevance_category(
  inference_rule: InferenceRule,
  conclusion_type: type,
) -> RuleRelevanceCategory:
  if (
    conclusion_type
    is Toda53NuPrimeBracketSpecializationStatement
    or _is_barratt_hilton_theorem_specific_rule(
      inference_rule
    )
  ):
    return (
      RuleRelevanceCategory
      .THEOREM_SPECIFIC
    )

  if (
    _is_generic_relation_representative_rule(
      inference_rule
    )
  ):
    return (
      RuleRelevanceCategory
      .GENERIC_RELATION
    )

  if (
    _is_injective_map_reflection_rule(
      inference_rule
    )
  ):
    return (
      RuleRelevanceCategory
      .MAP_PROPERTY
    )

  if (
    _is_first_iterated_suspension_bridge_rule(
      inference_rule
    )
  ):
    return (
      RuleRelevanceCategory
      .BRIDGE
    )

  return (
    RuleRelevanceCategory
    .UNCLASSIFIED
  )


def build_standard_production_applicability_catalog(
) -> InferenceRuleCatalog:
  repository = (
    build_standard_production_proof_repository()
  )

  scope = build_repository_proof_scope(
    repository
  )

  catalog = InferenceRuleCatalog()
  seen_rule_ids = set()
  entry_index = 0

  for node in scope.nodes:
    inference_rule = (
      node.proof_step.inference_rule
    )

    if inference_rule is None:
      continue

    rule_id = id(
      inference_rule
    )

    if rule_id in seen_rule_ids:
      continue

    seen_rule_ids.add(
      rule_id
    )

    conclusion_type = type(
      node.proof_step.conclusion
    )

    catalog.register(
      InferenceRuleCatalogEntry(
        key=(
          "standard.production."
          "applicability."
          f"{entry_index:04d}"
        ),
        rule=inference_rule,
        conclusion_type=conclusion_type,
        fixed_point_safe=False,
        relevance_category=(
          _representative_relevance_category(
            inference_rule,
            conclusion_type,
          )
        ),
      )
    )

    entry_index += 1

  return catalog
