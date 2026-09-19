from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
  ProofStep,
  VariableBinding,
)
from rule_catalog import (
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
