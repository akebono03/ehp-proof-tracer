from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
  ProofStep,
  Relation,
  VariableBinding,
  match_premise_pattern,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class InferenceRuleApplicabilityCandidate:
  catalog_entry: InferenceRuleCatalogEntry
  premise_index: int
  premise_pattern: PremisePattern
  source_step: ProofStep
  bindings: tuple[
    VariableBinding,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.catalog_entry,
      InferenceRuleCatalogEntry,
    ):
      raise TypeError(
        "catalog_entry must be an "
        "InferenceRuleCatalogEntry"
      )

    if (
      isinstance(
        self.premise_index,
        bool,
      )
      or not isinstance(
        self.premise_index,
        int,
      )
    ):
      raise TypeError(
        "premise_index must be an int"
      )

    premise_patterns = (
      self.catalog_entry
      .rule
      .premise_patterns
    )

    if (
      self.premise_index < 0
      or self.premise_index
      >= len(
        premise_patterns
      )
    ):
      raise ValueError(
        "premise_index must identify a "
        "catalog-entry rule premise"
      )

    if not isinstance(
      self.premise_pattern,
      PremisePattern,
    ):
      raise TypeError(
        "premise_pattern must be a "
        "PremisePattern"
      )

    if (
      premise_patterns[
        self.premise_index
      ]
      != self.premise_pattern
    ):
      raise ValueError(
        "premise_pattern must match the "
        "catalog-entry rule premise"
      )

    if not isinstance(
      self.source_step,
      ProofStep,
    ):
      raise TypeError(
        "source_step must be a ProofStep"
      )

    if not isinstance(
      self.bindings,
      tuple,
    ):
      raise TypeError(
        "bindings must be a tuple"
      )

    if any(
      not isinstance(
        binding,
        VariableBinding,
      )
      for binding in self.bindings
    ):
      raise TypeError(
        "bindings must contain only "
        "VariableBinding objects"
      )

  @property
  def inference_rule(
    self,
  ) -> InferenceRule:
    return self.catalog_entry.rule

  @property
  def matched_statement(
    self,
  ):
    return self.source_step.conclusion

  @property
  def fixed_point_safe(
    self,
  ) -> bool:
    return self.catalog_entry.fixed_point_safe


@dataclass(frozen=True)
class InferenceRulePremisePatternReference:
  catalog_entry: InferenceRuleCatalogEntry
  premise_index: int
  premise_pattern: PremisePattern
  ordinal: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.catalog_entry,
      InferenceRuleCatalogEntry,
    ):
      raise TypeError(
        "catalog_entry must be an "
        "InferenceRuleCatalogEntry"
      )

    if (
      isinstance(
        self.premise_index,
        bool,
      )
      or not isinstance(
        self.premise_index,
        int,
      )
    ):
      raise TypeError(
        "premise_index must be an int"
      )

    patterns = (
      self.catalog_entry
      .rule
      .premise_patterns
    )

    if (
      self.premise_index < 0
      or self.premise_index >= len(
        patterns
      )
    ):
      raise ValueError(
        "premise_index must identify a "
        "catalog-entry rule premise"
      )

    if not isinstance(
      self.premise_pattern,
      PremisePattern,
    ):
      raise TypeError(
        "premise_pattern must be a "
        "PremisePattern"
      )

    if (
      patterns[
        self.premise_index
      ]
      != self.premise_pattern
    ):
      raise ValueError(
        "premise_pattern must match the "
        "catalog-entry rule premise"
      )

    if (
      isinstance(
        self.ordinal,
        bool,
      )
      or not isinstance(
        self.ordinal,
        int,
      )
    ):
      raise TypeError(
        "ordinal must be an int"
      )

    if self.ordinal < 0:
      raise ValueError(
        "ordinal must be non-negative"
      )


class InferenceRulePremisePatternIndex:
  def __init__(
    self,
    catalog,
  ) -> None:
    if not isinstance(
      catalog,
      InferenceRuleCatalog,
    ):
      raise TypeError(
        "catalog must be an "
        "InferenceRuleCatalog"
      )

    self._catalog = catalog

    references = []
    wildcard_statement_type = []
    statement_type_buckets = {}
    ordinal = 0

    for entry in catalog.entries():
      for (
        premise_index,
        premise_pattern,
      ) in enumerate(
        entry.rule.premise_patterns
      ):
        if not isinstance(
          premise_pattern,
          PremisePattern,
        ):
          raise TypeError(
            "rule premise_patterns must contain "
            "only PremisePattern objects"
          )

        reference = (
          InferenceRulePremisePatternReference(
            catalog_entry=entry,
            premise_index=premise_index,
            premise_pattern=(
              premise_pattern
            ),
            ordinal=ordinal,
          )
        )

        references.append(
          reference
        )

        statement_type = (
          premise_pattern
          .statement_type
        )

        if statement_type is None:
          wildcard_statement_type.append(
            reference
          )
        else:
          statement_type_buckets.setdefault(
            statement_type,
            [],
          ).append(
            reference
          )

        ordinal += 1

    self._references = tuple(
      references
    )

    self._wildcard_statement_type = tuple(
      wildcard_statement_type
    )

    self._statement_type_buckets = {
      statement_type: tuple(
        bucket
      )
      for (
        statement_type,
        bucket,
      ) in statement_type_buckets.items()
    }

  @property
  def catalog(
    self,
  ) -> InferenceRuleCatalog:
    return self._catalog

  @property
  def references(
    self,
  ) -> tuple[
    InferenceRulePremisePatternReference,
    ...,
  ]:
    return self._references

  def compatible_references(
    self,
    source_step,
  ) -> tuple[
    InferenceRulePremisePatternReference,
    ...,
  ]:
    if not isinstance(
      source_step,
      ProofStep,
    ):
      raise TypeError(
        "source_step must be a ProofStep"
      )

    conclusion = (
      source_step.conclusion
    )

    references = list(
      self._wildcard_statement_type
    )

    for (
      statement_type,
      bucket,
    ) in (
      self._statement_type_buckets
      .items()
    ):
      if isinstance(
        conclusion,
        statement_type,
      ):
        references.extend(
          bucket
        )

    references.sort(
      key=lambda reference: (
        reference.ordinal
      )
    )

    compatible = []

    for reference in references:
      pattern = (
        reference.premise_pattern
      )

      if (
        pattern.proof_rule is not None
        and source_step.rule
        != pattern.proof_rule
      ):
        continue

      if (
        pattern.relation_type
        is not None
      ):
        if not isinstance(
          conclusion,
          Relation,
        ):
          continue

        if (
          conclusion.relation_type
          != pattern.relation_type
        ):
          continue

      compatible.append(
        reference
      )

    return tuple(
      compatible
    )


def build_inference_rule_premise_pattern_index(
  catalog,
):
  return InferenceRulePremisePatternIndex(
    catalog
  )


def find_inference_rule_applicability_candidates(
  catalog,
  source_step,
):
  if not isinstance(
    catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "catalog must be an "
      "InferenceRuleCatalog"
    )

  if not isinstance(
    source_step,
    ProofStep,
  ):
    raise TypeError(
      "source_step must be a ProofStep"
    )

  candidates = []

  for entry in catalog.entries():
    for (
      premise_index,
      premise_pattern,
    ) in enumerate(
      entry.rule.premise_patterns
    ):
      bindings = (
        match_premise_pattern(
          premise_pattern,
          source_step,
        )
      )

      if bindings is None:
        continue

      candidates.append(
        InferenceRuleApplicabilityCandidate(
          catalog_entry=entry,
          premise_index=premise_index,
          premise_pattern=(
            premise_pattern
          ),
          source_step=source_step,
          bindings=bindings,
        )
      )

  return tuple(
    candidates
  )


def find_indexed_inference_rule_applicability_candidates(
  index,
  source_step,
):
  if not isinstance(
    index,
    InferenceRulePremisePatternIndex,
  ):
    raise TypeError(
      "index must be an "
      "InferenceRulePremisePatternIndex"
    )

  if not isinstance(
    source_step,
    ProofStep,
  ):
    raise TypeError(
      "source_step must be a ProofStep"
    )

  candidates = []

  for reference in (
    index.compatible_references(
      source_step
    )
  ):
    bindings = (
      match_premise_pattern(
        reference.premise_pattern,
        source_step,
      )
    )

    if bindings is None:
      continue

    candidates.append(
      InferenceRuleApplicabilityCandidate(
        catalog_entry=(
          reference.catalog_entry
        ),
        premise_index=(
          reference.premise_index
        ),
        premise_pattern=(
          reference.premise_pattern
        ),
        source_step=source_step,
        bindings=bindings,
      )
    )

  return tuple(
    candidates
  )
