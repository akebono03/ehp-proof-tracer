import pytest
from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_matching_premises,
  matches_inference_rule,
  matches_premise_pattern,
)


def test_premise_pattern_defaults():
  pattern = PremisePattern()

  assert pattern.proof_rule is None
  assert pattern.statement_type is None
  assert pattern.relation_type is None


def test_premise_pattern_relation():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  assert (
    pattern.proof_rule
    == ProofRule.RELATION
  )

  assert (
    pattern.statement_type
    is Relation
  )

  assert (
    pattern.relation_type
    == RelationType.ZERO
  )


def test_inference_rule_without_premise_patterns():
  rule = InferenceRule(
    name="example rule",
  )

  assert (
    rule.premise_patterns
    == ()
  )


def test_inference_rule_with_premise_pattern():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name=(
      "zero relation implies "
      "order bound"
    ),
    description=(
      "If m alpha = 0, "
      "the order of alpha divides m."
    ),
    premise_patterns=(
      pattern,
    ),
  )

  assert (
    rule.premise_patterns
    == (
      pattern,
    )
  )


def test_inference_rule_multiple_premise_patterns():
  first_pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  second_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="combined rule",
    premise_patterns=(
      first_pattern,
      second_pattern,
    ),
  )

  assert (
    rule.premise_patterns
    == (
      first_pattern,
      second_pattern,
    )
  )


def test_premise_pattern_is_structurally_equal():
  pattern1 = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  pattern2 = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  assert pattern1 == pattern2


def test_empty_premise_pattern_matches_any_step():
  pattern = PremisePattern()

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_matches_proof_rule():
  pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_proof_rule():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_matches_statement_type():
  relation = Relation(
    lhs="alpha",
    rhs="beta",
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    statement_type=Relation,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_statement_type():
  step = ProofStep(
    conclusion="not a relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    statement_type=Relation,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_matches_relation_type():
  relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    relation_type=RelationType.ZERO,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_relation_type():
  relation = Relation(
    lhs="alpha",
    rhs="beta",
    relation_type=RelationType.EQUALITY,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    relation_type=RelationType.ZERO,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_relation_type_requires_relation_conclusion():
  step = ProofStep(
    conclusion="not a relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    relation_type=RelationType.ZERO,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_matches_all_conditions():
  relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_requires_all_conditions():
  relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_matches_premise_pattern_rejects_invalid_pattern():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    matches_premise_pattern(
      "invalid",
      step,
    )


def test_matches_premise_pattern_rejects_invalid_step():
  pattern = PremisePattern()

  with pytest.raises(TypeError):
    matches_premise_pattern(
      pattern,
      "invalid",
    )


def test_inference_rule_matches_single_premise():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name="zero relation rule",
    premise_patterns=(
      pattern,
    ),
  )

  relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert matches_inference_rule(
    rule,
    step,
  )


def test_inference_rule_rejects_single_wrong_premise():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
  )

  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      pattern,
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_inference_rule(
    rule,
    step,
  )


def test_inference_rule_matches_multiple_premises():
  first_pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
    statement_type=Relation,
    relation_type=RelationType.ZERO,
  )

  second_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="combined rule",
    premise_patterns=(
      first_pattern,
      second_pattern,
    ),
  )

  relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  relation_step = ProofStep(
    conclusion=relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  given_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_inference_rule(
    rule,
    (
      relation_step,
      given_step,
    ),
  )


def test_inference_rule_rejects_wrong_multiple_premise():
  first_pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
  )

  second_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="combined rule",
    premise_patterns=(
      first_pattern,
      second_pattern,
    ),
  )

  first_step = ProofStep(
    conclusion="relation-like fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  second_step = ProofStep(
    conclusion="wrong second step",
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert not matches_inference_rule(
    rule,
    (
      first_step,
      second_step,
    ),
  )


def test_inference_rule_matching_is_ordered():
  first_pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
  )

  second_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="ordered rule",
    premise_patterns=(
      first_pattern,
      second_pattern,
    ),
  )

  relation_step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  given_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_inference_rule(
    rule,
    (
      given_step,
      relation_step,
    ),
  )


def test_inference_rule_rejects_too_few_steps():
  rule = InferenceRule(
    name="two premise rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert not matches_inference_rule(
    rule,
    (
      step,
    ),
  )


def test_inference_rule_rejects_too_many_steps():
  rule = InferenceRule(
    name="one premise rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  first_step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  second_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_inference_rule(
    rule,
    (
      first_step,
      second_step,
    ),
  )


def test_empty_inference_rule_matches_empty_steps():
  rule = InferenceRule(
    name="no premise rule",
  )

  assert matches_inference_rule(
    rule,
    (),
  )


def test_empty_inference_rule_rejects_nonempty_steps():
  rule = InferenceRule(
    name="no premise rule",
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_inference_rule(
    rule,
    (
      step,
    ),
  )


def test_matches_inference_rule_accepts_single_proof_step():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_inference_rule(
    rule,
    step,
  )


def test_matches_inference_rule_accepts_tuple():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_inference_rule(
    rule,
    (
      step,
    ),
  )


def test_matches_inference_rule_accepts_list():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert matches_inference_rule(
    rule,
    [
      step,
    ],
  )


def test_matches_inference_rule_rejects_invalid_rule():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    matches_inference_rule(
      "invalid",
      step,
    )


def test_matches_inference_rule_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  with pytest.raises(TypeError):
    matches_inference_rule(
      rule,
      "invalid",
    )


def test_matches_inference_rule_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  with pytest.raises(TypeError):
    matches_inference_rule(
      rule,
      [
        "invalid",
      ],
    )


def test_find_matching_premises_single_step():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_matching_premises(
    rule,
    (
      step,
    ),
  )

  assert result == (
    step,
  )


def test_find_matching_premises_searches_available_steps():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  given_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation_step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_matching_premises(
    rule,
    (
      given_step,
      relation_step,
    ),
  )

  assert result == (
    relation_step,
  )


def test_find_matching_premises_multiple_patterns():
  rule = InferenceRule(
    name="combined rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  given_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation_step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_matching_premises(
    rule,
    (
      given_step,
      relation_step,
    ),
  )

  assert result == (
    relation_step,
    given_step,
  )


def test_find_matching_premises_returns_first_match():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  first_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_matching_premises(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert result == (
    first_step,
  )


def test_find_matching_premises_does_not_reuse_step():
  rule = InferenceRule(
    name="two given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="only step",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_matching_premises(
      rule,
      (
        step,
      ),
    )
    is None
  )


def test_find_matching_premises_uses_distinct_steps():
  rule = InferenceRule(
    name="two given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  first_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_matching_premises(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert result == (
    first_step,
    second_step,
  )


def test_find_matching_premises_returns_none_when_missing():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    find_matching_premises(
      rule,
      (
        step,
      ),
    )
    is None
  )


def test_find_matching_premises_partial_failure():
  rule = InferenceRule(
    name="combined rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  relation_step = ProofStep(
    conclusion="relation fact",
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    find_matching_premises(
      rule,
      (
        relation_step,
      ),
    )
    is None
  )


def test_find_matching_premises_empty_rule():
  rule = InferenceRule(
    name="no premise rule",
  )

  result = find_matching_premises(
    rule,
    (),
  )

  assert result == ()


def test_find_matching_premises_empty_rule_ignores_available_steps():
  rule = InferenceRule(
    name="no premise rule",
  )

  step = ProofStep(
    conclusion="unused fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_matching_premises(
    rule,
    (
      step,
    ),
  )

  assert result == ()


def test_find_matching_premises_matches_relation_type():
  rule = InferenceRule(
    name="zero relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
  )

  equality_relation = Relation(
    lhs="alpha",
    rhs="beta",
    relation_type=RelationType.EQUALITY,
  )

  zero_relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  equality_step = ProofStep(
    conclusion=equality_relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  zero_step = ProofStep(
    conclusion=zero_relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_matching_premises(
    rule,
    (
      equality_step,
      zero_step,
    ),
  )

  assert result == (
    zero_step,
  )


def test_find_matching_premises_accepts_single_step():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_matching_premises(
    rule,
    step,
  ) == (
    step,
  )


def test_find_matching_premises_accepts_list():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_matching_premises(
    rule,
    [
      step,
    ],
  ) == (
    step,
  )


def test_find_matching_premises_rejects_invalid_rule():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    find_matching_premises(
      "invalid",
      (
        step,
      ),
    )


def test_find_matching_premises_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_matching_premises(
      rule,
      "invalid",
    )


def test_find_matching_premises_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_matching_premises(
      rule,
      [
        "invalid",
      ],
    )




