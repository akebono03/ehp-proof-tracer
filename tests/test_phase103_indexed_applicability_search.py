from dataclasses import dataclass

import pytest

import rule_applicability
from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from rule_applicability import (
  InferenceRulePremisePatternIndex,
  build_inference_rule_premise_pattern_index,
  find_indexed_inference_rule_applicability_candidates,
  find_inference_rule_applicability_candidates,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase103IndexedStatement:
  value: str


@dataclass(frozen=True)
class Phase103IndexedDerivedStatement(
  Phase103IndexedStatement
):
  pass


@dataclass(frozen=True)
class Phase103IndexedOtherStatement:
  value: str


def register_rule(
  catalog,
  *,
  key,
  patterns,
):
  entry = InferenceRuleCatalogEntry(
    key=key,
    rule=InferenceRule(
      name=key,
      premise_patterns=patterns,
    ),
    conclusion_type=object,
  )

  catalog.register(
    entry
  )

  return entry


def candidate_signature(
  candidates,
):
  return tuple(
    (
      candidate.catalog_entry.key,
      candidate.premise_index,
      candidate.premise_pattern,
      candidate.source_step,
      candidate.bindings,
    )
    for candidate in candidates
  )


def build_indexed_catalog():
  catalog = InferenceRuleCatalog()

  register_rule(
    catalog,
    key="phase103.index.wildcard",
    patterns=(
      PremisePattern(),
    ),
  )

  register_rule(
    catalog,
    key="phase103.index.statement",
    patterns=(
      PremisePattern(
        statement_type=(
          Phase103IndexedStatement
        ),
      ),
    ),
  )

  register_rule(
    catalog,
    key="phase103.index.other",
    patterns=(
      PremisePattern(
        statement_type=(
          Phase103IndexedOtherStatement
        ),
      ),
    ),
  )

  register_rule(
    catalog,
    key="phase103.index.proof-rule",
    patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase103IndexedStatement
        ),
      ),
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=(
          Phase103IndexedStatement
        ),
      ),
    ),
  )

  register_rule(
    catalog,
    key="phase103.index.relation",
    patterns=(
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      PremisePattern(
        statement_type=Relation,
        relation_type=(
          RelationType.ZERO
        ),
      ),
    ),
  )

  return catalog


@pytest.mark.parametrize(
  "source_step",
  (
    ProofStep(
      conclusion=Phase103IndexedStatement(
        value="base",
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=(
        Phase103IndexedDerivedStatement(
          value="derived",
        )
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=(
        Phase103IndexedOtherStatement(
          value="other",
        )
      ),
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=Relation(
        lhs="x",
        rhs="y",
        relation_type=(
          RelationType.EQUALITY
        ),
      ),
      premises=(),
      rule=ProofRule.RELATION,
    ),
  ),
)
def test_phase103_6b_indexed_search_preserves_bruteforce_candidates(
  source_step,
):
  catalog = build_indexed_catalog()

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  brute = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  indexed = (
    find_indexed_inference_rule_applicability_candidates(
      index,
      source_step,
    )
  )

  assert (
    candidate_signature(
      indexed
    )
    == candidate_signature(
      brute
    )
  )


def test_phase103_6b_index_preserves_catalog_and_premise_order():
  catalog = build_indexed_catalog()

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103IndexedStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  references = (
    index.compatible_references(
      source_step
    )
  )

  assert tuple(
    reference.ordinal
    for reference in references
  ) == tuple(
    sorted(
      reference.ordinal
      for reference in references
    )
  )


def test_phase103_6b_index_keeps_subclass_isinstance_semantics():
  catalog = InferenceRuleCatalog()

  base_entry = register_rule(
    catalog,
    key="phase103.index.base",
    patterns=(
      PremisePattern(
        statement_type=(
          Phase103IndexedStatement
        ),
      ),
    ),
  )

  source_step = ProofStep(
    conclusion=(
      Phase103IndexedDerivedStatement(
        value="derived",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  references = (
    index.compatible_references(
      source_step
    )
  )

  assert len(
    references
  ) == 1

  assert (
    references[
      0
    ].catalog_entry
    is base_entry
  )


def test_phase103_6b_index_reduces_matcher_calls_for_unrelated_types(
  monkeypatch,
):
  catalog = InferenceRuleCatalog()

  register_rule(
    catalog,
    key="phase103.index.matching",
    patterns=(
      PremisePattern(
        statement_type=(
          Phase103IndexedStatement
        ),
      ),
    ),
  )

  for index_number in range(
    100
  ):
    statement_type = dataclass(
      frozen=True
    )(
      type(
        (
          "Phase103Unrelated"
          f"{index_number}"
        ),
        (),
        {
          "__annotations__": {
            "value": str,
          },
        },
      )
    )

    register_rule(
      catalog,
      key=(
        "phase103.index.unrelated."
        f"{index_number}"
      ),
      patterns=(
        PremisePattern(
          statement_type=(
            statement_type
          ),
        ),
      ),
    )

  source_step = ProofStep(
    conclusion=(
      Phase103IndexedStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  original_matcher = (
    rule_applicability
    .match_premise_pattern
  )

  calls = []

  def counting_matcher(
    pattern,
    step,
  ):
    calls.append(
      pattern
    )
    return original_matcher(
      pattern,
      step,
    )

  monkeypatch.setattr(
    rule_applicability,
    "match_premise_pattern",
    counting_matcher,
  )

  find_inference_rule_applicability_candidates(
    catalog,
    source_step,
  )

  brute_calls = len(
    calls
  )

  calls.clear()

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  find_indexed_inference_rule_applicability_candidates(
    index,
    source_step,
  )

  indexed_calls = len(
    calls
  )

  assert (
    brute_calls
    == 101
  )

  assert (
    indexed_calls
    == 1
  )


def test_phase103_6b_index_rejects_invalid_catalog():
  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    InferenceRulePremisePatternIndex(
      object()
    )


def test_phase103_6b_indexed_search_rejects_invalid_index():
  source_step = ProofStep(
    conclusion=(
      Phase103IndexedStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    TypeError,
    match=(
      "index must be an "
      "InferenceRulePremisePatternIndex"
    ),
  ):
    find_indexed_inference_rule_applicability_candidates(
      object(),
      source_step,
    )
