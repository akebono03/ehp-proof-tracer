from repository_proof_scope import (
  build_repository_proof_scope,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def test_phase103_6_standard_catalog_is_nonempty():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert (
    catalog.entries()
  )


def test_phase103_6_standard_catalog_contains_only_production_inference_rules():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  production_rules = {
    id(
      node.proof_step.inference_rule
    )
    for node in scope.nodes
    if (
      node.proof_step.inference_rule
      is not None
    )
  }

  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert all(
    id(
      entry.rule
    ) in production_rules
    for entry in catalog.entries()
  )


def test_phase103_6_standard_catalog_deduplicates_rule_identity():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  rule_ids = tuple(
    id(
      entry.rule
    )
    for entry in catalog.entries()
  )

  assert len(
    rule_ids
  ) == len(
    set(
      rule_ids
    )
  )


def test_phase103_6_standard_catalog_is_discovery_only():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert all(
    entry.fixed_point_safe
    is False
    for entry in catalog.entries()
  )


def test_phase103_6_standard_catalog_keys_are_stable_shape():
  catalog = (
    build_standard_production_applicability_catalog()
  )

  assert all(
    entry.key.startswith(
      "standard.production.applicability."
    )
    for entry in catalog.entries()
  )
