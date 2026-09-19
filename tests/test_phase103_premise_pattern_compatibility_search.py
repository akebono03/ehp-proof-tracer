from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
  find_inference_rule_applicability_candidates,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase103SearchStatement:
  value: object


@dataclass(frozen=True)
class Phase103OtherStatement:
  value: object


def make_entry(
  *,
  key,
  premise_patterns,
  fixed_point_safe=False,
):
  return InferenceRuleCatalogEntry(
    key=key,
    rule=InferenceRule(
      name=key,
      premise_patterns=(
        premise_patterns
      ),
    ),
    conclusion_type=(
      Phase103OtherStatement
    ),
    fixed_point_safe=(
      fixed_point_safe
    ),
  )


def test_phase103_3_finds_matching_type_only_premise():
  catalog = InferenceRuleCatalog()

  pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=Phase103SearchStatement,
  )

  entry = make_entry(
    key="phase103.type-only",
    premise_patterns=(
      pattern,
    ),
  )

  catalog.register(
    entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  candidate = candidates[0]

  assert isinstance(
    candidate,
    InferenceRuleApplicabilityCandidate,
  )

  assert (
    candidate.catalog_entry
    is entry
  )

  assert (
    candidate.premise_index
    == 0
  )

  assert (
    candidate.premise_pattern
    is pattern
  )

  assert (
    candidate.source_step
    is source_step
  )

  assert (
    candidate.bindings
    == ()
  )


def test_phase103_3_preserves_pattern_variable_bindings():
  catalog = InferenceRuleCatalog()

  variable = PatternVariable(
    name="value",
  )

  pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=Phase103SearchStatement,
    statement_pattern=(
      Phase103SearchStatement(
        value=variable,
      )
    ),
  )

  catalog.register(
    make_entry(
      key="phase103.binding",
      premise_patterns=(
        pattern,
      ),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  assert len(
    candidates[0].bindings
  ) == 1

  assert (
    candidates[
      0
    ].bindings[
      0
    ].variable
    == variable
  )

  assert (
    candidates[
      0
    ].bindings[
      0
    ].value
    == "known"
  )


def test_phase103_3_finds_multiple_matching_premise_positions():
  catalog = InferenceRuleCatalog()

  first_pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  second_pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  entry = make_entry(
    key="phase103.multiple-premises",
    premise_patterns=(
      first_pattern,
      second_pattern,
    ),
  )

  catalog.register(
    entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert tuple(
    candidate.premise_index
    for candidate in candidates
  ) == (
    0,
    1,
  )

  assert all(
    candidate.catalog_entry
    is entry
    for candidate in candidates
  )


def test_phase103_3_preserves_catalog_registration_order():
  catalog = InferenceRuleCatalog()

  pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  first_entry = make_entry(
    key="phase103.first",
    premise_patterns=(
      pattern,
    ),
  )

  second_entry = make_entry(
    key="phase103.second",
    premise_patterns=(
      pattern,
    ),
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert tuple(
    candidate.catalog_entry
    for candidate in candidates
  ) == (
    first_entry,
    second_entry,
  )


def test_phase103_3_preserves_alias_entries():
  catalog = InferenceRuleCatalog()

  pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  rule = InferenceRule(
    name="phase103 shared rule",
    premise_patterns=(
      pattern,
    ),
  )

  first_entry = InferenceRuleCatalogEntry(
    key="phase103.alias.first",
    rule=rule,
    conclusion_type=(
      Phase103OtherStatement
    ),
  )

  second_entry = InferenceRuleCatalogEntry(
    key="phase103.alias.second",
    rule=rule,
    conclusion_type=(
      Phase103OtherStatement
    ),
  )

  catalog.register(
    first_entry
  )

  catalog.register(
    second_entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert tuple(
    candidate.catalog_entry
    for candidate in candidates
  ) == (
    first_entry,
    second_entry,
  )

  assert (
    candidates[
      0
    ].inference_rule
    is rule
  )

  assert (
    candidates[
      1
    ].inference_rule
    is rule
  )


def test_phase103_3_does_not_filter_unsafe_entries():
  catalog = InferenceRuleCatalog()

  pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  unsafe_entry = make_entry(
    key="phase103.unsafe",
    premise_patterns=(
      pattern,
    ),
    fixed_point_safe=False,
  )

  catalog.register(
    unsafe_entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  assert (
    candidates[
      0
    ].catalog_entry
    is unsafe_entry
  )

  assert (
    candidates[
      0
    ].fixed_point_safe
    is False
  )


def test_phase103_3_excludes_non_matching_statement_type():
  catalog = InferenceRuleCatalog()

  catalog.register(
    make_entry(
      key="phase103.unrelated",
      premise_patterns=(
        PremisePattern(
          statement_type=(
            Phase103OtherStatement
          ),
        ),
      ),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
    == ()
  )


def test_phase103_3_excludes_non_matching_proof_rule():
  catalog = InferenceRuleCatalog()

  catalog.register(
    make_entry(
      key="phase103.rule-mismatch",
      premise_patterns=(
        PremisePattern(
          proof_rule=ProofRule.RELATION,
          statement_type=(
            Phase103SearchStatement
          ),
        ),
      ),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
    == ()
  )


def test_phase103_3_uses_relation_pattern_matching():
  catalog = InferenceRuleCatalog()

  lhs_variable = PatternVariable(
    name="lhs",
  )

  relation_pattern = Relation(
    lhs=lhs_variable,
    rhs=0,
    relation_type=RelationType.EQUALITY,
  )

  premise_pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    relation_type=RelationType.EQUALITY,
    relation_pattern=(
      relation_pattern
    ),
  )

  catalog.register(
    make_entry(
      key="phase103.relation",
      premise_patterns=(
        premise_pattern,
      ),
    )
  )

  source_relation = Relation(
    lhs="known-element",
    rhs=0,
    relation_type=RelationType.EQUALITY,
  )

  source_step = ProofStep(
    conclusion=source_relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  assert (
    candidates[
      0
    ].matched_statement
    is source_relation
  )

  assert (
    candidates[
      0
    ].bindings[
      0
    ].variable
    == lhs_variable
  )

  assert (
    candidates[
      0
    ].bindings[
      0
    ].value
    == "known-element"
  )


def test_phase103_3_entry_with_no_premises_produces_no_candidate():
  catalog = InferenceRuleCatalog()

  catalog.register(
    make_entry(
      key="phase103.no-premises",
      premise_patterns=(),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
    == ()
  )


def test_phase103_3_search_does_not_execute_rule():
  catalog = InferenceRuleCatalog()

  calls = []

  pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  entry = InferenceRuleCatalogEntry(
    key="phase103.no-execution",
    rule=InferenceRule(
      name="phase103 no execution",
      premise_patterns=(
        pattern,
      ),
      conclusion_builder=(
        lambda premises: (
          calls.append(
            premises
          )
          or Phase103OtherStatement(
            value="derived",
          )
        )
      ),
    ),
    conclusion_type=(
      Phase103OtherStatement
    ),
  )

  catalog.register(
    entry
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  assert (
    calls
    == []
  )


def test_phase103_3_search_does_not_evaluate_match_guard():
  catalog = InferenceRuleCatalog()

  calls = []

  pattern = PremisePattern(
    statement_type=Phase103SearchStatement,
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase103.no-guard",
      rule=InferenceRule(
        name="phase103 no guard",
        premise_patterns=(
          pattern,
        ),
        match_guard=(
          lambda premises, bindings: (
            calls.append(
              (
                premises,
                bindings,
              )
            )
            or True
          )
        ),
      ),
      conclusion_type=(
        Phase103OtherStatement
      ),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  candidates = (
    find_inference_rule_applicability_candidates(
      catalog,
      source_step,
    )
  )

  assert len(
    candidates
  ) == 1

  assert (
    calls
    == []
  )


def test_phase103_3_rejects_invalid_catalog():
  source_step = ProofStep(
    conclusion=(
      Phase103SearchStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    find_inference_rule_applicability_candidates(
      object(),
      source_step,
    )


def test_phase103_3_rejects_invalid_source_step():
  catalog = InferenceRuleCatalog()

  with pytest.raises(
    TypeError,
    match=(
      "source_step must be a ProofStep"
    ),
  ):
    find_inference_rule_applicability_candidates(
      catalog,
      object(),
    )
