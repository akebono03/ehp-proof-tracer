import pytest
from proof import (
  InferenceMatch,
  InferenceRule,
  InferenceRunResult,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  apply_inference_matches,
  derive_inference_steps,
  derive_new_inference_steps,
  find_applicable_inference_rules,
  find_inference_match,
  find_inference_matches,
  find_matching_premises,
  is_inference_rule_applicable,
  matches_inference_rule,
  matches_premise_pattern,
  merge_proof_steps,
  run_inference_round,
  run_inference_until_stable,
  run_inference_until_stable_with_history,
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


def test_inference_rule_is_applicable():
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

  assert is_inference_rule_applicable(
    rule,
    (
      step,
    ),
  )


def test_inference_rule_is_not_applicable():
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

  assert not is_inference_rule_applicable(
    rule,
    (
      step,
    ),
  )


def test_inference_rule_applicable_with_multiple_patterns():
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

  assert is_inference_rule_applicable(
    rule,
    (
      given_step,
      relation_step,
    ),
  )


def test_inference_rule_not_applicable_when_premise_missing():
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

  assert not is_inference_rule_applicable(
    rule,
    (
      relation_step,
    ),
  )


def test_empty_inference_rule_is_applicable():
  rule = InferenceRule(
    name="no premise rule",
  )

  assert is_inference_rule_applicable(
    rule,
    (),
  )


def test_empty_inference_rule_is_applicable_with_available_steps():
  rule = InferenceRule(
    name="no premise rule",
  )

  step = ProofStep(
    conclusion="unused fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert is_inference_rule_applicable(
    rule,
    (
      step,
    ),
  )


def test_inference_rule_applicability_searches_available_steps():
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

  assert is_inference_rule_applicable(
    rule,
    (
      given_step,
      relation_step,
    ),
  )


def test_inference_rule_applicability_does_not_reuse_step():
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
    conclusion="only given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not is_inference_rule_applicable(
    rule,
    (
      step,
    ),
  )


def test_inference_rule_applicability_uses_distinct_steps():
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

  assert is_inference_rule_applicable(
    rule,
    (
      first_step,
      second_step,
    ),
  )


def test_inference_rule_applicability_matches_relation_type():
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

  assert is_inference_rule_applicable(
    rule,
    (
      equality_step,
      zero_step,
    ),
  )


def test_inference_rule_applicability_rejects_wrong_relation_type():
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

  assert not is_inference_rule_applicable(
    rule,
    (
      step,
    ),
  )


def test_is_inference_rule_applicable_accepts_single_step():
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

  assert is_inference_rule_applicable(
    rule,
    step,
  )


def test_is_inference_rule_applicable_accepts_list():
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

  assert is_inference_rule_applicable(
    rule,
    [
      step,
    ],
  )


def test_is_inference_rule_applicable_rejects_invalid_rule():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    is_inference_rule_applicable(
      "invalid",
      (
        step,
      ),
    )


def test_is_inference_rule_applicable_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    is_inference_rule_applicable(
      rule,
      "invalid",
    )


def test_is_inference_rule_applicable_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    is_inference_rule_applicable(
      rule,
      [
        "invalid",
      ],
    )


def test_find_applicable_inference_rules():
  given_rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  relation_rule = InferenceRule(
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

  result = (
    find_applicable_inference_rules(
      (
        given_rule,
        relation_rule,
      ),
      (
        given_step,
      ),
    )
  )

  assert result == (
    given_rule,
  )


def test_find_applicable_inference_rules_multiple_matches():
  first_rule = InferenceRule(
    name="first given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  second_rule = InferenceRule(
    name="second given rule",
    premise_patterns=(
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

  result = (
    find_applicable_inference_rules(
      (
        first_rule,
        second_rule,
      ),
      (
        given_step,
      ),
    )
  )

  assert result == (
    first_rule,
    second_rule,
  )


def test_find_applicable_inference_rules_preserves_order():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
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

  result = (
    find_applicable_inference_rules(
      (
        second_rule,
        first_rule,
      ),
      (
        given_step,
      ),
    )
  )

  assert result == (
    second_rule,
    first_rule,
  )


def test_find_applicable_inference_rules_returns_empty():
  relation_rule = InferenceRule(
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

  result = (
    find_applicable_inference_rules(
      (
        relation_rule,
      ),
      (
        given_step,
      ),
    )
  )

  assert result == ()


def test_find_applicable_inference_rules_empty_rules():
  given_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    find_applicable_inference_rules(
      (),
      (
        given_step,
      ),
    )
  )

  assert result == ()


def test_find_applicable_inference_rules_includes_empty_rule():
  empty_rule = InferenceRule(
    name="no premise rule",
  )

  relation_rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  result = (
    find_applicable_inference_rules(
      (
        relation_rule,
        empty_rule,
      ),
      (),
    )
  )

  assert result == (
    empty_rule,
  )


def test_find_applicable_inference_rules_multiple_patterns():
  combined_rule = InferenceRule(
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

  given_rule = InferenceRule(
    name="given rule",
    premise_patterns=(
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

  result = (
    find_applicable_inference_rules(
      (
        combined_rule,
        given_rule,
      ),
      (
        given_step,
        relation_step,
      ),
    )
  )

  assert result == (
    combined_rule,
    given_rule,
  )


def test_find_applicable_inference_rules_relation_type():
  zero_rule = InferenceRule(
    name="zero relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
  )

  equality_rule = InferenceRule(
    name="equality relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
      ),
    ),
  )

  zero_relation = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  zero_step = ProofStep(
    conclusion=zero_relation,
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = (
    find_applicable_inference_rules(
      (
        equality_rule,
        zero_rule,
      ),
      (
        zero_step,
      ),
    )
  )

  assert result == (
    zero_rule,
  )


def test_find_applicable_inference_rules_accepts_single_rule():
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

  result = (
    find_applicable_inference_rules(
      rule,
      step,
    )
  )

  assert result == (
    rule,
  )


def test_find_applicable_inference_rules_accepts_list():
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

  result = (
    find_applicable_inference_rules(
      [
        rule,
      ],
      [
        step,
      ],
    )
  )

  assert result == (
    rule,
  )


def test_find_applicable_inference_rules_rejects_invalid_rules():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    find_applicable_inference_rules(
      "invalid",
      (
        step,
      ),
    )


def test_find_applicable_inference_rules_rejects_invalid_rule_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_applicable_inference_rules(
      [
        rule,
        "invalid",
      ],
      (),
    )


def test_find_applicable_inference_rules_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_applicable_inference_rules(
      (
        rule,
      ),
      "invalid",
    )


def test_find_applicable_inference_rules_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_applicable_inference_rules(
      (
        rule,
      ),
      [
        "invalid",
      ],
    )


def test_inference_match():
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

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )

  assert (
    match.inference_rule
    == rule
  )

  assert match.premises == (
    step,
  )


def test_find_inference_match():
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

  result = find_inference_match(
    rule,
    (
      step,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )


def test_find_inference_match_returns_none():
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
    find_inference_match(
      rule,
      (
        step,
      ),
    )
    is None
  )


def test_find_inference_match_preserves_pattern_order():
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

  result = find_inference_match(
    rule,
    (
      given_step,
      relation_step,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      relation_step,
      given_step,
    ),
  )


def test_find_inference_match_empty_rule():
  rule = InferenceRule(
    name="no premise rule",
  )

  result = find_inference_match(
    rule,
    (),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(),
  )


def test_find_inference_match_empty_rule_with_steps():
  rule = InferenceRule(
    name="no premise rule",
  )

  step = ProofStep(
    conclusion="unused fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_inference_match(
    rule,
    (
      step,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(),
  )


def test_find_inference_match_relation_type():
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

  result = find_inference_match(
    rule,
    (
      equality_step,
      zero_step,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      zero_step,
    ),
  )


def test_find_inference_match_accepts_single_step():
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

  result = find_inference_match(
    rule,
    step,
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )


def test_find_inference_match_accepts_list():
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

  result = find_inference_match(
    rule,
    [
      step,
    ],
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )


def test_find_inference_match_rejects_invalid_rule():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    find_inference_match(
      "invalid",
      (
        step,
      ),
    )


def test_find_inference_match_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_inference_match(
      rule,
      "invalid",
    )


def test_find_inference_match_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_inference_match(
      rule,
      [
        "invalid",
      ],
    )


def test_find_inference_matches():
  given_rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  relation_rule = InferenceRule(
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

  result = find_inference_matches(
    (
      given_rule,
      relation_rule,
    ),
    (
      given_step,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=given_rule,
      premises=(
        given_step,
      ),
    ),
  )


def test_find_inference_matches_multiple():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = find_inference_matches(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
      relation_step,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=first_rule,
      premises=(
        given_step,
      ),
    ),
    InferenceMatch(
      inference_rule=second_rule,
      premises=(
        relation_step,
      ),
    ),
  )


def test_find_inference_matches_preserves_rule_order():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = find_inference_matches(
    (
      second_rule,
      first_rule,
    ),
    (
      step,
    ),
  )

  assert tuple(
    match.inference_rule
    for match in result
  ) == (
    second_rule,
    first_rule,
  )


def test_find_inference_matches_returns_empty():
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

  assert find_inference_matches(
    (
      rule,
    ),
    (
      step,
    ),
  ) == ()


def test_find_inference_matches_empty_rules():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_matches(
    (),
    (
      step,
    ),
  ) == ()


def test_find_inference_matches_includes_empty_rule():
  relation_rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  empty_rule = InferenceRule(
    name="no premise rule",
  )

  result = find_inference_matches(
    (
      relation_rule,
      empty_rule,
    ),
    (),
  )

  assert result == (
    InferenceMatch(
      inference_rule=empty_rule,
      premises=(),
    ),
  )


def test_find_inference_matches_multiple_patterns():
  combined_rule = InferenceRule(
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

  result = find_inference_matches(
    (
      combined_rule,
    ),
    (
      given_step,
      relation_step,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=combined_rule,
      premises=(
        relation_step,
        given_step,
      ),
    ),
  )


def test_find_inference_matches_relation_type():
  zero_rule = InferenceRule(
    name="zero rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=Relation,
        relation_type=RelationType.ZERO,
      ),
    ),
  )

  equality_rule = InferenceRule(
    name="equality rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
        statement_type=Relation,
        relation_type=RelationType.EQUALITY,
      ),
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

  result = find_inference_matches(
    (
      equality_rule,
      zero_rule,
    ),
    (
      step,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=zero_rule,
      premises=(
        step,
      ),
    ),
  )


def test_find_inference_matches_accepts_single_rule():
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

  result = find_inference_matches(
    rule,
    step,
  )

  assert result == (
    InferenceMatch(
      inference_rule=rule,
      premises=(
        step,
      ),
    ),
  )


def test_find_inference_matches_accepts_list():
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

  result = find_inference_matches(
    [
      rule,
    ],
    [
      step,
    ],
  )

  assert result == (
    InferenceMatch(
      inference_rule=rule,
      premises=(
        step,
      ),
    ),
  )


def test_find_inference_matches_rejects_invalid_rules():
  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    find_inference_matches(
      "invalid",
      (
        step,
      ),
    )


def test_find_inference_matches_rejects_invalid_rule_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_inference_matches(
      [
        rule,
        "invalid",
      ],
      (),
    )


def test_find_inference_matches_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_inference_matches(
      (
        rule,
      ),
      "invalid",
    )


def test_find_inference_matches_rejects_invalid_step_in_list():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    find_inference_matches(
      (
        rule,
      ),
      [
        "invalid",
      ],
    )


def test_inference_rule_conclusion_builder_defaults_to_none():
  rule = InferenceRule(
    name="example rule",
  )

  assert (
    rule.conclusion_builder
    is None
  )


def test_inference_rule_conclusion_builder():
  def builder(premises):
    return "derived fact"

  rule = InferenceRule(
    name="example rule",
    conclusion_builder=builder,
  )

  assert (
    rule.conclusion_builder
    is builder
  )


def test_inference_rule_conclusion_builder_is_backward_compatible():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  assert (
    rule.conclusion_builder
    is None
  )


def test_apply_inference_match():
  def builder(premises):
    return "derived fact"

  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=builder,
  )

  premise_step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      premise_step,
    ),
  )

  result = apply_inference_match(
    match
  )

  assert result.conclusion == (
    "derived fact"
  )

  assert result.premises == (
    premise_step,
  )

  assert (
    result.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.inference_rule
    == rule
  )


def test_apply_inference_match_builder_receives_premises():
  received = []

  def builder(premises):
    received.extend(
      premises
    )
    return "derived fact"

  rule = InferenceRule(
    name="given inference",
    conclusion_builder=builder,
  )

  first_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.RELATION,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      first_step,
      second_step,
    ),
  )

  apply_inference_match(
    match
  )

  assert received == [
    first_step,
    second_step,
  ]


def test_apply_inference_match_builder_result_is_conclusion():
  conclusion = Relation(
    lhs="alpha",
    rhs="beta",
  )

  def builder(premises):
    return conclusion

  rule = InferenceRule(
    name="relation inference",
    conclusion_builder=builder,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  result = apply_inference_match(
    match
  )

  assert (
    result.conclusion
    == conclusion
  )


def test_apply_inference_match_multiple_premises():
  def builder(premises):
    return (
      premises[0].conclusion,
      premises[1].conclusion,
    )

  rule = InferenceRule(
    name="combined inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=builder,
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

  match = find_inference_match(
    rule,
    (
      given_step,
      relation_step,
    ),
  )

  result = apply_inference_match(
    match
  )

  assert result.conclusion == (
    "relation fact",
    "given fact",
  )

  assert result.premises == (
    relation_step,
    given_step,
  )


def test_apply_inference_match_preserves_pattern_order():
  received = []

  def builder(premises):
    received.extend(
      step.rule
      for step in premises
    )
    return "derived"

  rule = InferenceRule(
    name="ordered inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=builder,
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation_step = ProofStep(
    conclusion="relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  match = find_inference_match(
    rule,
    (
      given_step,
      relation_step,
    ),
  )

  apply_inference_match(
    match
  )

  assert received == [
    ProofRule.RELATION,
    ProofRule.GIVEN,
  ]


def test_apply_inference_match_premise_free_rule():
  def builder(premises):
    assert premises == ()
    return "axiomatic conclusion"

  rule = InferenceRule(
    name="premise free inference",
    conclusion_builder=builder,
  )

  match = find_inference_match(
    rule,
    (),
  )

  result = apply_inference_match(
    match
  )

  assert (
    result.conclusion
    == "axiomatic conclusion"
  )

  assert result.premises == ()

  assert (
    result.rule
    == ProofRule.INFERENCE
  )

  assert (
    result.inference_rule
    == rule
  )


def test_apply_inference_match_rejects_invalid_match():
  with pytest.raises(TypeError):
    apply_inference_match(
      "invalid"
    )


def test_apply_inference_match_requires_conclusion_builder():
  rule = InferenceRule(
    name="rule without builder",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  with pytest.raises(ValueError):
    apply_inference_match(
      match
    )


def test_apply_inference_match_rejects_non_callable_builder():
  rule = InferenceRule(
    name="invalid builder rule",
    conclusion_builder="invalid",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  with pytest.raises(TypeError):
    apply_inference_match(
      match
    )


def test_find_inference_match_does_not_require_builder():
  rule = InferenceRule(
    name="matching only rule",
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

  result = find_inference_match(
    rule,
    (
      step,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )


def test_find_inference_matches_do_not_require_builders():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = find_inference_matches(
    (
      first_rule,
      second_rule,
    ),
    (
      step,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=first_rule,
      premises=(
        step,
      ),
    ),
    InferenceMatch(
      inference_rule=second_rule,
      premises=(
        step,
      ),
    ),
  )


def test_apply_found_inference_match():
  def builder(premises):
    return (
      "derived from "
      + premises[0].conclusion
    )

  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=builder,
  )

  step = ProofStep(
    conclusion="given fact",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = find_inference_match(
    rule,
    (
      step,
    ),
  )

  result = apply_inference_match(
    match
  )

  assert (
    result.conclusion
    == "derived from given fact"
  )

  assert result.premises == (
    step,
  )

  assert (
    result.inference_rule
    == rule
  )


def test_apply_inference_matches():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  first_step = ProofStep(
    conclusion="first given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion="second given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(
      first_step,
    ),
  )

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(
      second_step,
    ),
  )

  result = apply_inference_matches(
    (
      first_match,
      second_match,
    ),
  )

  assert len(result) == 2

  assert (
    result[0].conclusion
    == "first derived"
  )

  assert (
    result[1].conclusion
    == "second derived"
  )


def test_apply_inference_matches_preserves_order():
  first_rule = InferenceRule(
    name="first rule",
    conclusion_builder=lambda premises: (
      "first"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(),
  )

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(),
  )

  result = apply_inference_matches(
    (
      second_match,
      first_match,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "second",
    "first",
  )


def test_apply_inference_matches_preserves_premises():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      step,
    ),
  )

  result = apply_inference_matches(
    (
      match,
    ),
  )

  assert result[0].premises == (
    step,
  )


def test_apply_inference_matches_preserves_rules():
  first_rule = InferenceRule(
    name="first rule",
    conclusion_builder=lambda premises: (
      "first"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  result = apply_inference_matches(
    (
      InferenceMatch(
        inference_rule=first_rule,
        premises=(),
      ),
      InferenceMatch(
        inference_rule=second_rule,
        premises=(),
      ),
    ),
  )

  assert (
    result[0].inference_rule
    == first_rule
  )

  assert (
    result[1].inference_rule
    == second_rule
  )


def test_apply_inference_matches_empty():
  assert apply_inference_matches(
    (),
  ) == ()


def test_apply_inference_matches_accepts_single_match():
  rule = InferenceRule(
    name="rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  result = apply_inference_matches(
    match,
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_apply_inference_matches_accepts_list():
  rule = InferenceRule(
    name="rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  result = apply_inference_matches(
    [
      match,
    ],
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_apply_inference_matches_rejects_invalid_input():
  with pytest.raises(TypeError):
    apply_inference_matches(
      "invalid"
    )


def test_apply_inference_matches_rejects_invalid_match_in_list():
  rule = InferenceRule(
    name="rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  with pytest.raises(TypeError):
    apply_inference_matches(
      [
        match,
        "invalid",
      ],
    )


def test_apply_found_inference_matches():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
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

  matches = find_inference_matches(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
      relation_step,
    ),
  )

  derived_steps = (
    apply_inference_matches(
      matches
    )
  )

  assert tuple(
    step.conclusion
    for step in derived_steps
  ) == (
    "first derived",
    "second derived",
  )

  assert (
    derived_steps[0].premises
    == (
      given_step,
    )
  )

  assert (
    derived_steps[1].premises
    == (
      relation_step,
    )
  )


def test_derive_inference_steps():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_inference_steps(
    (
      rule,
    ),
    (
      step,
    ),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )

  assert result[0].premises == (
    step,
  )

  assert (
    result[0].inference_rule
    == rule
  )


def test_derive_inference_steps_multiple_rules():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation_step = ProofStep(
    conclusion="relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = derive_inference_steps(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
      relation_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "first derived",
    "second derived",
  )


def test_derive_inference_steps_preserves_rule_order():
  first_rule = InferenceRule(
    name="first rule",
    conclusion_builder=lambda premises: (
      "first"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  result = derive_inference_steps(
    (
      second_rule,
      first_rule,
    ),
    (),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "second",
    "first",
  )


def test_derive_inference_steps_returns_empty():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert derive_inference_steps(
    (
      rule,
    ),
    (
      step,
    ),
  ) == ()


def test_derive_inference_steps_empty_rules():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert derive_inference_steps(
    (),
    (
      step,
    ),
  ) == ()


def test_derive_inference_steps_accepts_single_rule_and_step():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_inference_steps(
    rule,
    step,
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_derive_inference_steps_accepts_lists():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_inference_steps(
    [
      rule,
    ],
    [
      step,
    ],
  )

  assert len(result) == 1


def test_derive_inference_steps_rejects_invalid_rules():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    derive_inference_steps(
      "invalid",
      (
        step,
      ),
    )


def test_derive_inference_steps_rejects_invalid_steps():
  rule = InferenceRule(
    name="rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  with pytest.raises(TypeError):
    derive_inference_steps(
      (
        rule,
      ),
      "invalid",
    )


def test_derive_inference_steps_requires_builder_for_matched_rule():
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

  with pytest.raises(ValueError):
    derive_inference_steps(
      (
        rule,
      ),
      (
        step,
      ),
    )


def test_run_inference_round():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (
      rule,
    ),
    (
      step,
    ),
  )

  assert len(result) == 2

  assert result[0] == step

  assert (
    result[1].conclusion
    == "derived"
  )

  assert result[1].premises == (
    step,
  )

  assert (
    result[1].rule
    == ProofRule.INFERENCE
  )

  assert (
    result[1].inference_rule
    == rule
  )


def test_run_inference_round_appends_multiple_derived_steps():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation_step = ProofStep(
    conclusion="relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = run_inference_round(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
      relation_step,
    ),
  )

  assert result[:2] == (
    given_step,
    relation_step,
  )

  assert tuple(
    step.conclusion
    for step in result[2:]
  ) == (
    "first derived",
    "second derived",
  )


def test_run_inference_round_preserves_available_step_order():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
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
    rule=ProofRule.RELATION,
  )

  result = run_inference_round(
    (
      rule,
    ),
    (
      first_step,
      second_step,
    ),
  )

  assert result[:2] == (
    first_step,
    second_step,
  )


def test_run_inference_round_preserves_derived_step_order():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (
      second_rule,
      first_rule,
    ),
    (
      step,
    ),
  )

  assert tuple(
    derived_step.conclusion
    for derived_step in result[1:]
  ) == (
    "second",
    "first",
  )


def test_run_inference_round_no_applicable_rules():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (
      rule,
    ),
    (
      step,
    ),
  )

  assert result == (
    step,
  )


def test_run_inference_round_empty_rules():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (),
    (
      step,
    ),
  )

  assert result == (
    step,
  )


def test_run_inference_round_empty_steps():
  rule = InferenceRule(
    name="no premise rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = run_inference_round(
    (
      rule,
    ),
    (),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )

  assert result[0].premises == ()

  assert (
    result[0].rule
    == ProofRule.INFERENCE
  )


def test_run_inference_round_accepts_single_rule_and_step():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    rule,
    step,
  )

  assert result[0] == step

  assert (
    result[1].conclusion
    == "derived"
  )


def test_run_inference_round_accepts_lists():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    [
      rule,
    ],
    [
      step,
    ],
  )

  assert isinstance(
    result,
    tuple,
  )

  assert result[0] == step

  assert (
    result[1].conclusion
    == "derived"
  )


def test_run_inference_round_rejects_invalid_rules():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    run_inference_round(
      "invalid",
      (
        step,
      ),
    )


def test_run_inference_round_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    run_inference_round(
      (
        rule,
      ),
      "invalid",
    )


def test_run_inference_round_requires_builder_for_matched_rule():
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

  with pytest.raises(ValueError):
    run_inference_round(
      (
        rule,
      ),
      (
        step,
      ),
    )


def test_merge_proof_steps():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  derived_step = ProofStep(
    conclusion="derived",
    premises=(
      available_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (
      available_step,
    ),
    (
      derived_step,
    ),
  )

  assert result == (
    available_step,
    derived_step,
  )


def test_merge_proof_steps_skips_existing_conclusion():
  available_step = ProofStep(
    conclusion="same conclusion",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  derived_step = ProofStep(
    conclusion="same conclusion",
    premises=(
      available_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (
      available_step,
    ),
    (
      derived_step,
    ),
  )

  assert result == (
    available_step,
  )


def test_merge_proof_steps_skips_duplicate_derived_conclusion():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_derived_step = ProofStep(
    conclusion="derived",
    premises=(
      available_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  second_derived_step = ProofStep(
    conclusion="derived",
    premises=(
      available_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (
      available_step,
    ),
    (
      first_derived_step,
      second_derived_step,
    ),
  )

  assert result == (
    available_step,
    first_derived_step,
  )


def test_merge_proof_steps_preserves_available_order():
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

  derived_step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (
      second_step,
      first_step,
    ),
    (
      derived_step,
    ),
  )

  assert result == (
    second_step,
    first_step,
    derived_step,
  )


def test_merge_proof_steps_preserves_first_new_step_order():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_derived_step = ProofStep(
    conclusion="first derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  second_derived_step = ProofStep(
    conclusion="second derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (
      available_step,
    ),
    (
      second_derived_step,
      first_derived_step,
    ),
  )

  assert result == (
    available_step,
    second_derived_step,
    first_derived_step,
  )


def test_merge_proof_steps_empty_available():
  derived_step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    (),
    (
      derived_step,
    ),
  )

  assert result == (
    derived_step,
  )


def test_merge_proof_steps_empty_derived():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = merge_proof_steps(
    (
      available_step,
    ),
    (),
  )

  assert result == (
    available_step,
  )


def test_merge_proof_steps_accepts_single_steps():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  derived_step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    available_step,
    derived_step,
  )

  assert result == (
    available_step,
    derived_step,
  )


def test_merge_proof_steps_accepts_lists():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  derived_step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = merge_proof_steps(
    [
      available_step,
    ],
    [
      derived_step,
    ],
  )

  assert result == (
    available_step,
    derived_step,
  )


def test_merge_proof_steps_rejects_invalid_available_steps():
  derived_step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  with pytest.raises(TypeError):
    merge_proof_steps(
      "invalid",
      (
        derived_step,
      ),
    )


def test_merge_proof_steps_rejects_invalid_derived_steps():
  available_step = ProofStep(
    conclusion="available",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    merge_proof_steps(
      (
        available_step,
      ),
      "invalid",
    )


def test_run_inference_round_does_not_duplicate_existing_conclusion():
  rule = InferenceRule(
    name="derive existing",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "already known"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  existing_step = ProofStep(
    conclusion="already known",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (
      rule,
    ),
    (
      given_step,
      existing_step,
    ),
  )

  assert result == (
    given_step,
    existing_step,
  )


def test_run_inference_round_does_not_duplicate_same_derived_conclusion():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_round(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
    ),
  )

  assert len(result) == 2

  assert result[0] == given_step

  assert (
    result[1].conclusion
    == "same derived"
  )

  assert (
    result[1].inference_rule
    == first_rule
  )


def test_run_inference_round_is_idempotent_for_same_derivation():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_result = run_inference_round(
    (
      rule,
    ),
    (
      given_step,
    ),
  )

  second_result = run_inference_round(
    (
      rule,
    ),
    first_result,
  )

  assert second_result == first_result


def test_derive_new_inference_steps():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      rule,
    ),
    (
      given_step,
    ),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )

  assert result[0].premises == (
    given_step,
  )

  assert (
    result[0].rule
    == ProofRule.INFERENCE
  )

  assert (
    result[0].inference_rule
    == rule
  )


def test_derive_new_inference_steps_excludes_existing_conclusion():
  rule = InferenceRule(
    name="derive existing",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "already known"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  existing_step = ProofStep(
    conclusion="already known",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      rule,
    ),
    (
      given_step,
      existing_step,
    ),
  )

  assert result == ()


def test_derive_new_inference_steps_excludes_duplicate_derived_conclusion():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      first_rule,
      second_rule,
    ),
    (
      given_step,
    ),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "same derived"
  )

  assert (
    result[0].inference_rule
    == first_rule
  )


def test_derive_new_inference_steps_returns_only_new_conclusions():
  existing_rule = InferenceRule(
    name="existing rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "already known"
    ),
  )

  new_rule = InferenceRule(
    name="new rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "new conclusion"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  existing_step = ProofStep(
    conclusion="already known",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      existing_rule,
      new_rule,
    ),
    (
      given_step,
      existing_step,
    ),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "new conclusion"
  )

  assert (
    result[0].inference_rule
    == new_rule
  )


def test_derive_new_inference_steps_preserves_new_step_order():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      second_rule,
      first_rule,
    ),
    (
      given_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "second derived",
    "first derived",
  )


def test_derive_new_inference_steps_returns_empty_when_no_rule_matches():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (
      rule,
    ),
    (
      given_step,
    ),
  )

  assert result == ()


def test_derive_new_inference_steps_empty_rules():
  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    (),
    (
      given_step,
    ),
  )

  assert result == ()


def test_derive_new_inference_steps_empty_available_steps():
  rule = InferenceRule(
    name="premise free rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = derive_new_inference_steps(
    (
      rule,
    ),
    (),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )

  assert result[0].premises == ()


def test_derive_new_inference_steps_returns_empty_after_same_derivation():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_round = run_inference_round(
    (
      rule,
    ),
    (
      given_step,
    ),
  )

  result = derive_new_inference_steps(
    (
      rule,
    ),
    first_round,
  )

  assert result == ()


def test_derive_new_inference_steps_accepts_single_rule_and_step():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    rule,
    given_step,
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_derive_new_inference_steps_accepts_lists():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_new_inference_steps(
    [
      rule,
    ],
    [
      given_step,
    ],
  )

  assert isinstance(
    result,
    tuple,
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_derive_new_inference_steps_rejects_invalid_rules():
  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    derive_new_inference_steps(
      "invalid",
      (
        given_step,
      ),
    )


def test_derive_new_inference_steps_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    derive_new_inference_steps(
      (
        rule,
      ),
      "invalid",
    )


def test_derive_new_inference_steps_requires_builder_for_matched_rule():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  given_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(ValueError):
    derive_new_inference_steps(
      (
        rule,
      ),
      (
        given_step,
      ),
    )


def test_run_inference_until_stable():
  first_rule = InferenceRule(
    name="derive second",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  second_rule = InferenceRule(
    name="derive third",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=lambda premises: (
      "third"
    ),
  )

  initial_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      first_rule,
      second_rule,
    ),
    (
      initial_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "first",
    "second",
    "third",
  )


def test_run_inference_until_stable_requires_multiple_rounds():
  first_rule = InferenceRule(
    name="given to relation",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  second_rule = InferenceRule(
    name="relation to final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
      ),
    ),
    conclusion_builder=lambda premises: (
      "final"
    ),
  )

  initial_step = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      first_rule,
      second_rule,
    ),
    (
      initial_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "initial",
    Relation(
      lhs="alpha",
      rhs="beta",
    ),
    "final",
  )


def test_run_inference_until_stable_returns_initial_steps_when_no_rule_matches():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      rule,
    ),
    (
      initial_step,
    ),
  )

  assert result == (
    initial_step,
  )


def test_run_inference_until_stable_empty_rules():
  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (),
    (
      initial_step,
    ),
  )

  assert result == (
    initial_step,
  )


def test_run_inference_until_stable_empty_initial_steps():
  rule = InferenceRule(
    name="premise free rule",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = run_inference_until_stable(
    (
      rule,
    ),
    (),
  )

  assert len(result) == 1

  assert (
    result[0].conclusion
    == "derived"
  )


def test_run_inference_until_stable_preserves_initial_order():
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

  result = run_inference_until_stable(
    (),
    (
      second_step,
      first_step,
    ),
  )

  assert result == (
    second_step,
    first_step,
  )


def test_run_inference_until_stable_preserves_derivation_order():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      second_rule,
      first_rule,
    ),
    (
      initial_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "given",
    "second derived",
    "first derived",
  )


def test_run_inference_until_stable_does_not_duplicate_conclusions():
  rule = InferenceRule(
    name="repeated rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      rule,
    ),
    (
      initial_step,
    ),
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "given",
    "derived",
  )


def test_run_inference_until_stable_preserves_dependencies():
  first_rule = InferenceRule(
    name="derive second",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second"
    ),
  )

  second_rule = InferenceRule(
    name="derive third",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
      ),
    ),
    conclusion_builder=lambda premises: (
      "third"
    ),
  )

  initial_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    (
      first_rule,
      second_rule,
    ),
    (
      initial_step,
    ),
  )

  second_step = result[1]
  third_step = result[2]

  assert second_step.premises == (
    initial_step,
  )

  assert third_step.premises == (
    second_step,
  )


def test_run_inference_until_stable_accepts_single_rule_and_step():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    rule,
    initial_step,
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "given",
    "derived",
  )


def test_run_inference_until_stable_accepts_lists():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = run_inference_until_stable(
    [
      rule,
    ],
    [
      initial_step,
    ],
  )

  assert isinstance(
    result,
    tuple,
  )

  assert tuple(
    step.conclusion
    for step in result
  ) == (
    "given",
    "derived",
  )


def test_run_inference_until_stable_rejects_invalid_rules():
  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    run_inference_until_stable(
      "invalid",
      (
        initial_step,
      ),
    )


def test_run_inference_until_stable_rejects_invalid_steps():
  rule = InferenceRule(
    name="given rule",
  )

  with pytest.raises(TypeError):
    run_inference_until_stable(
      (
        rule,
      ),
      "invalid",
    )


def test_run_inference_until_stable_requires_builder_for_matched_rule():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(ValueError):
    run_inference_until_stable(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )


def test_inference_run_result():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = InferenceRunResult(
    steps=(
      step,
    ),
    round_history=(),
  )

  assert result.steps == (
    step,
  )

  assert result.round_history == ()

  assert result.round_count == 0


def test_run_inference_until_stable_with_history():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )
  )

  assert isinstance(
    result,
    InferenceRunResult,
  )

  assert tuple(
    step.conclusion
    for step in result.steps
  ) == (
    "given",
    "derived",
  )

  assert result.round_count == 1

  assert len(
    result.round_history
  ) == 1

  assert tuple(
    step.conclusion
    for step in result.round_history[0]
  ) == (
    "derived",
  )


def test_run_inference_until_stable_with_history_multiple_rounds():
  first_rule = InferenceRule(
    name="given to relation",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  second_rule = InferenceRule(
    name="relation to final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
      ),
    ),
    conclusion_builder=lambda premises: (
      "final"
    ),
  )

  initial_step = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      (
        initial_step,
      ),
    )
  )

  assert result.round_count == 2

  assert tuple(
    step.conclusion
    for step in result.round_history[0]
  ) == (
    Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  assert tuple(
    step.conclusion
    for step in result.round_history[1]
  ) == (
    "final",
  )

  assert tuple(
    step.conclusion
    for step in result.steps
  ) == (
    "initial",
    Relation(
      lhs="alpha",
      rhs="beta",
    ),
    "final",
  )


def test_run_inference_until_stable_with_history_excludes_empty_terminal_round():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )
  )

  assert result.round_count == 1

  assert result.round_history == (
    (
      result.steps[1],
    ),
  )


def test_run_inference_until_stable_with_history_no_new_steps():
  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (),
      (
        initial_step,
      ),
    )
  )

  assert result.steps == (
    initial_step,
  )

  assert result.round_history == ()

  assert result.round_count == 0


def test_run_inference_until_stable_with_history_empty_initial_state():
  result = (
    run_inference_until_stable_with_history(
      (),
      (),
    )
  )

  assert result.steps == ()
  assert result.round_history == ()
  assert result.round_count == 0


def test_run_inference_until_stable_with_history_records_multiple_new_steps_in_round():
  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "first derived"
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "second derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      (
        initial_step,
      ),
    )
  )

  assert result.round_count == 1

  assert tuple(
    step.conclusion
    for step in result.round_history[0]
  ) == (
    "first derived",
    "second derived",
  )


def test_run_inference_until_stable_with_history_preserves_dependencies():
  first_rule = InferenceRule(
    name="derive relation",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  second_rule = InferenceRule(
    name="derive final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=Relation,
      ),
    ),
    conclusion_builder=lambda premises: (
      "final"
    ),
  )

  initial_step = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      (
        initial_step,
      ),
    )
  )

  relation_step = (
    result.round_history[0][0]
  )

  final_step = (
    result.round_history[1][0]
  )

  assert relation_step.premises == (
    initial_step,
  )

  assert final_step.premises == (
    relation_step,
  )


def test_run_inference_until_stable_with_history_final_steps_match_simple_api():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  simple_result = (
    run_inference_until_stable(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )
  )

  detailed_result = (
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )
  )

  assert (
    detailed_result.steps
    == simple_result
  )


def test_run_inference_until_stable_with_history_accepts_single_rule_and_step():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      initial_step,
    )
  )

  assert result.round_count == 1

  assert tuple(
    step.conclusion
    for step in result.steps
  ) == (
    "given",
    "derived",
  )


def test_run_inference_until_stable_with_history_accepts_lists():
  rule = InferenceRule(
    name="given inference",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      [
        rule,
      ],
      [
        initial_step,
      ],
    )
  )

  assert isinstance(
    result,
    InferenceRunResult,
  )

  assert result.round_count == 1


def test_run_inference_until_stable_with_history_rejects_invalid_rules():
  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    run_inference_until_stable_with_history(
      "invalid",
      (
        initial_step,
      ),
    )


def test_run_inference_until_stable_with_history_rejects_invalid_steps():
  rule = InferenceRule(
    name="rule",
  )

  with pytest.raises(TypeError):
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      "invalid",
    )


def test_run_inference_until_stable_with_history_requires_builder_for_matched_rule():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  initial_step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(ValueError):
    run_inference_until_stable_with_history(
      (
        rule,
      ),
      (
        initial_step,
      ),
    )







