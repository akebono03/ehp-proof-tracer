from repository_proof_scope import (
  build_repository_proof_scope,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
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

    catalog.register(
      InferenceRuleCatalogEntry(
        key=(
          "standard.production."
          "applicability."
          f"{entry_index:04d}"
        ),
        rule=inference_rule,
        conclusion_type=type(
          node.proof_step.conclusion
        ),
        fixed_point_safe=False,
      )
    )

    entry_index += 1

  return catalog
