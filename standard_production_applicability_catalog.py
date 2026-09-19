from expression import (
  IteratedSuspension,
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


def _is_generic_relation_representative_rule(
  inference_rule: InferenceRule,
) -> bool:
  return (
    inference_rule
    == equality_symmetry_inference_rule()
    or inference_rule
    == equality_transitivity_inference_rule()
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


def _representative_relevance_category(
  inference_rule: InferenceRule,
  conclusion_type: type,
) -> RuleRelevanceCategory:
  if (
    conclusion_type
    is Toda53NuPrimeBracketSpecializationStatement
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
