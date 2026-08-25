import pytest
from proof import (
  InferenceApplicationResult,
  InferenceMatch,
  InferenceRejectionReason,
  InferenceRoundResult,
  InferenceRule,
  InferenceRunResult,
  InferenceTerminationReason,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  VariableBinding,
  apply_inference_match,
  apply_inference_matches,
  apply_inference_matches_with_results,
  classify_inference_application_results,
  derive_inference_round_result,
  derive_inference_steps,
  derive_new_inference_steps,
  find_applicable_inference_rules,
  find_inference_match,
  find_inference_matches,
  find_all_matching_premises,
  find_inference_matches_for_rule,
  find_matching_premises,
  is_inference_rule_applicable,
  lookup_variable_binding,
  match_inference_rule_bindings,
  matches_inference_rule,
  match_premise_pattern,
  matches_premise_pattern,
  match_pattern_value,
  match_relation_pattern,
  merge_proof_steps,
  merge_variable_bindings,
  partition_new_and_duplicate_proof_steps,
  run_inference_round,
  run_inference_until_stable,
  run_inference_until_stable_with_history,
  substitute_pattern_value,
  substitute_relation_pattern,  
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
    round_results=(),
    termination_reason=(
      InferenceTerminationReason.FIXED_POINT
    ),
  )

  assert result.steps == (
    step,
  )

  assert result.round_results == ()

  assert result.round_history == ()

  assert result.round_count == 0

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


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


def test_inference_termination_reason_values():
  assert (
    InferenceTerminationReason.FIXED_POINT.value
    == "fixed_point"
  )

  assert (
    InferenceTerminationReason.MAX_ROUNDS.value
    == "max_rounds"
  )


def test_run_inference_until_stable_with_history_reports_fixed_point():
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

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_run_inference_until_stable_with_history_stops_at_max_rounds():
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
      max_rounds=1,
    )
  )

  assert result.round_count == 1

  assert tuple(
    step.conclusion
    for step in result.steps
  ) == (
    "initial",
    Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.MAX_ROUNDS
  )


def test_run_inference_until_stable_with_history_max_rounds_zero():
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
      max_rounds=0,
    )
  )

  assert result.steps == (
    initial_step,
  )

  assert result.round_history == ()

  assert result.round_count == 0

  assert (
    result.termination_reason
    == InferenceTerminationReason.MAX_ROUNDS
  )


def test_run_inference_until_stable_with_history_reaches_fixed_point_before_limit():
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
      max_rounds=10,
    )
  )

  assert result.round_count == 1

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_run_inference_until_stable_with_history_limit_equal_to_productive_rounds():
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
      max_rounds=2,
    )
  )

  assert result.round_count == 2

  assert (
    result.termination_reason
    == InferenceTerminationReason.MAX_ROUNDS
  )


def test_run_inference_until_stable_with_history_rejects_negative_max_rounds():
  with pytest.raises(ValueError):
    run_inference_until_stable_with_history(
      (),
      (),
      max_rounds=-1,
    )


def test_run_inference_until_stable_with_history_rejects_non_integer_max_rounds():
  with pytest.raises(TypeError):
    run_inference_until_stable_with_history(
      (),
      (),
      max_rounds=1.5,
    )


def test_run_inference_until_stable_with_history_rejects_bool_max_rounds():
  with pytest.raises(TypeError):
    run_inference_until_stable_with_history(
      (),
      (),
      max_rounds=True,
    )


def test_run_inference_until_stable_respects_max_rounds():
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
    max_rounds=1,
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
  )


def test_inference_round_result():
  step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = InferenceRoundResult(
    new_steps=(
      step,
    ),
  )

  assert result.new_steps == (
    step,
  )


def test_inference_round_result_is_structurally_equal():
  step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  first = InferenceRoundResult(
    new_steps=(
      step,
    ),
  )

  second = InferenceRoundResult(
    new_steps=(
      step,
    ),
  )

  assert first == second


def test_run_inference_until_stable_with_round_results():
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

  assert len(
    result.round_results
  ) == 1

  assert isinstance(
    result.round_results[0],
    InferenceRoundResult,
  )

  assert tuple(
    step.conclusion
    for step
    in result.round_results[
      0
    ].new_steps
  ) == (
    "derived",
  )


def test_round_results_preserve_round_order():
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

  assert len(
    result.round_results
  ) == 2

  assert isinstance(
    result.round_results[0],
    InferenceRoundResult,
  )

  assert isinstance(
    result.round_results[1],
    InferenceRoundResult,
  )

  assert isinstance(
    result.round_results[
      0
    ].new_steps[
      0
    ].conclusion,
    Relation,
  )

  assert (
    result.round_results[
      1
    ].new_steps[
      0
    ].conclusion
    == "final"
  )


def test_round_history_is_compatibility_view_of_round_results():
  first_step = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  second_step = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  first_round = InferenceRoundResult(
    new_steps=(
      first_step,
    ),
  )

  second_round = InferenceRoundResult(
    new_steps=(
      second_step,
    ),
  )

  result = InferenceRunResult(
    steps=(
      first_step,
      second_step,
    ),
    round_results=(
      first_round,
      second_round,
    ),
    termination_reason=(
      InferenceTerminationReason.FIXED_POINT
    ),
  )

  assert result.round_history == (
    (
      first_step,
    ),
    (
      second_step,
    ),
  )

  assert result.round_count == 2


def test_inference_round_result_matches_default_to_empty():
  step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = InferenceRoundResult(
    new_steps=(
      step,
    ),
  )

  assert result.matches == ()


def test_derive_inference_round_result():
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

  result = (
    derive_inference_round_result(
      (
        rule,
      ),
      (
        step,
      ),
    )
  )

  assert isinstance(
    result,
    InferenceRoundResult,
  )

  assert len(
    result.matches
  ) == 1

  assert (
    result.matches[0].inference_rule
    == rule
  )

  assert result.matches[0].premises == (
    step,
  )

  assert tuple(
    derived_step.conclusion
    for derived_step
    in result.new_steps
  ) == (
    "derived",
  )


def test_derive_inference_round_result_new_steps_match_simple_api():
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

  round_result = (
    derive_inference_round_result(
      (
        rule,
      ),
      (
        step,
      ),
    )
  )

  new_steps = (
    derive_new_inference_steps(
      (
        rule,
      ),
      (
        step,
      ),
    )
  )

  assert (
    round_result.new_steps
    == new_steps
  )


def test_derive_inference_round_result_no_matches():
  rule = InferenceRule(
    name="relation inference",
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

  result = (
    derive_inference_round_result(
      (
        rule,
      ),
      (
        step,
      ),
    )
  )

  assert result.matches == ()
  assert result.new_steps == ()


def test_derive_inference_round_result_keeps_all_matches_before_duplicate_filtering():
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

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    derive_inference_round_result(
      (
        first_rule,
        second_rule,
      ),
      (
        step,
      ),
    )
  )

  assert len(
    result.matches
  ) == 2

  assert tuple(
    match.inference_rule
    for match
    in result.matches
  ) == (
    first_rule,
    second_rule,
  )

  assert len(
    result.new_steps
  ) == 1

  assert (
    result.new_steps[0].conclusion
    == "same derived"
  )

  assert (
    result.new_steps[0].inference_rule
    == first_rule
  )


def test_run_inference_until_stable_records_round_matches():
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

  round_result = (
    result.round_results[0]
  )

  assert len(
    round_result.matches
  ) == 1

  assert (
    round_result.matches[
      0
    ].inference_rule
    == rule
  )

  assert (
    round_result.matches[
      0
    ].premises
    == (
      initial_step,
    )
  )


def test_run_inference_until_stable_preserves_per_round_matches():
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
    match.inference_rule
    for match
    in result.round_results[
      0
    ].matches
  ) == (
    first_rule,
  )

  assert tuple(
    match.inference_rule
    for match
    in result.round_results[
      1
    ].matches
  ) == (
    first_rule,
    second_rule,
  )


def test_derive_inference_round_result_keeps_match_when_conclusion_is_already_known():
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

  result = (
    derive_inference_round_result(
      (
        rule,
      ),
      (
        given_step,
        existing_step,
      ),
    )
  )

  assert len(
    result.matches
  ) == 2

  assert tuple(
    match.inference_rule
    for match
    in result.matches
  ) == (
    rule,
    rule,
  )

  assert tuple(
    match.premises
    for match
    in result.matches
  ) == (
    (
      given_step,
    ),
    (
      existing_step,
    ),
  )

  assert result.new_steps == ()


def test_inference_round_result_candidate_steps_default_to_empty():
  result = InferenceRoundResult(
    new_steps=(),
  )

  assert result.candidate_steps == ()


def test_inference_round_result_duplicate_rejected_steps_default_to_empty():
  result = InferenceRoundResult(
    new_steps=(),
  )

  assert (
    result.duplicate_rejected_steps
    == ()
  )


def test_partition_new_and_duplicate_proof_steps():
  available = ProofStep(
    conclusion="known",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  new_step = ProofStep(
    conclusion="new",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  duplicate_step = ProofStep(
    conclusion="known",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  (
    new_steps,
    duplicate_rejected_steps,
  ) = (
    partition_new_and_duplicate_proof_steps(
      available,
      (
        new_step,
        duplicate_step,
      ),
    )
  )

  assert new_steps == (
    new_step,
  )

  assert (
    duplicate_rejected_steps
    == (
      duplicate_step,
    )
  )


def test_partition_new_and_duplicate_proof_steps_rejects_same_round_duplicate():
  first = ProofStep(
    conclusion="same",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  second = ProofStep(
    conclusion="same",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  (
    new_steps,
    duplicate_rejected_steps,
  ) = (
    partition_new_and_duplicate_proof_steps(
      (),
      (
        first,
        second,
      ),
    )
  )

  assert new_steps == (
    first,
  )

  assert (
    duplicate_rejected_steps
    == (
      second,
    )
  )


def test_partition_new_and_duplicate_proof_steps_preserves_order():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  third = ProofStep(
    conclusion="third",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  (
    new_steps,
    duplicate_rejected_steps,
  ) = (
    partition_new_and_duplicate_proof_steps(
      (),
      (
        first,
        second,
        third,
      ),
    )
  )

  assert new_steps == (
    first,
    second,
    third,
  )

  assert (
    duplicate_rejected_steps
    == ()
  )


def test_partition_new_and_duplicate_proof_steps_preserves_rejected_order():
  known_a = ProofStep(
    conclusion="a",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  known_b = ProofStep(
    conclusion="b",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  duplicate_a = ProofStep(
    conclusion="a",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  duplicate_b = ProofStep(
    conclusion="b",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  (
    new_steps,
    duplicate_rejected_steps,
  ) = (
    partition_new_and_duplicate_proof_steps(
      (
        known_a,
        known_b,
      ),
      (
        duplicate_b,
        duplicate_a,
      ),
    )
  )

  assert new_steps == ()

  assert (
    duplicate_rejected_steps
    == (
      duplicate_b,
      duplicate_a,
    )
  )


def test_derive_inference_round_result_records_candidate_steps():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="derive",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = derive_inference_round_result(
    rule,
    given,
  )

  assert len(
    result.candidate_steps
  ) == 1

  assert (
    result.candidate_steps[
      0
    ].conclusion
    == "derived"
  )

  assert (
    result.new_steps
    == result.candidate_steps
  )

  assert (
    result.duplicate_rejected_steps
    == ()
  )


def test_derive_inference_round_result_marks_already_known_application():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  known = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = derive_inference_round_result(
    rule,
    (
      given,
      known,
    ),
  )

  assert len(
    result.application_results
  ) == 2

  first_result = (
    result.application_results[0]
  )

  second_result = (
    result.application_results[1]
  )

  assert first_result.match.premises == (
    given,
  )

  assert second_result.match.premises == (
    known,
  )

  assert (
    first_result.accepted
    is False
  )

  assert (
    second_result.accepted
    is False
  )

  assert (
    first_result.rejection_reason
    == InferenceRejectionReason.ALREADY_KNOWN
  )

  assert (
    second_result.rejection_reason
    == InferenceRejectionReason.ALREADY_KNOWN
  )

  assert result.new_steps == ()

  assert (
    result.duplicate_rejected_steps
    == (
      first_result.candidate_step,
      second_result.candidate_step,
    )
  )


def test_derive_inference_round_result_records_same_round_duplicate_candidate():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same"
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
      "same"
    ),
  )

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    given,
  )

  assert len(
    result.matches
  ) == 2

  assert len(
    result.candidate_steps
  ) == 2

  assert tuple(
    step.conclusion
    for step
    in result.candidate_steps
  ) == (
    "same",
    "same",
  )

  assert result.new_steps == (
    result.candidate_steps[0],
  )

  assert (
    result.duplicate_rejected_steps
    == (
      result.candidate_steps[1],
    )
  )


def test_derive_inference_round_result_preserves_candidate_order():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    given,
  )

  assert tuple(
    step.conclusion
    for step
    in result.candidate_steps
  ) == (
    "first",
    "second",
  )


def test_run_inference_until_stable_records_duplicate_rejected_steps_per_round():
  initial = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation = Relation(
    lhs="middle",
    rhs="value",
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      relation
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      initial,
    )
  )

  assert len(
    result.round_results
  ) == 2

  first_round = (
    result.round_results[0]
  )

  second_round = (
    result.round_results[1]
  )

  assert (
    first_round.duplicate_rejected_steps
    == ()
  )

  assert len(
    second_round.duplicate_rejected_steps
  ) == 1

  assert (
    second_round.duplicate_rejected_steps[
      0
    ].conclusion
    == relation
  )

  assert (
    second_round.duplicate_rejected_steps[
      0
    ].inference_rule
    == first_rule
  )


def test_inference_application_result():
  rule = InferenceRule(
    name="given rule",
  )

  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      premise,
    ),
  )

  candidate_step = ProofStep(
    conclusion="derived",
    premises=(
      premise,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  result = InferenceApplicationResult(
    match=match,
    candidate_step=candidate_step,
  )

  assert result.match == match

  assert (
    result.candidate_step
    == candidate_step
  )


def test_inference_application_result_is_structurally_equal():
  rule = InferenceRule(
    name="given rule",
  )

  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      premise,
    ),
  )

  candidate_step = ProofStep(
    conclusion="derived",
    premises=(
      premise,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  first_result = (
    InferenceApplicationResult(
      match=match,
      candidate_step=candidate_step,
    )
  )

  second_result = (
    InferenceApplicationResult(
      match=match,
      candidate_step=candidate_step,
    )
  )

  assert (
    first_result
    == second_result
  )


def test_inference_round_result_application_results_default_to_empty():
  step = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  result = InferenceRoundResult(
    new_steps=(
      step,
    ),
  )

  assert (
    result.application_results
    == ()
  )


def test_apply_inference_matches_with_results():
  rule = InferenceRule(
    name="given inference",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      premise,
    ),
  )

  results = (
    apply_inference_matches_with_results(
      match
    )
  )

  assert len(
    results
  ) == 1

  assert isinstance(
    results[0],
    InferenceApplicationResult,
  )

  assert (
    results[0].match
    == match
  )

  assert (
    results[0].candidate_step.conclusion
    == "derived"
  )

  assert (
    results[0].candidate_step.premises
    == (
      premise,
    )
  )

  assert (
    results[0].candidate_step.inference_rule
    == rule
  )


def test_apply_inference_matches_with_results_multiple():
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

  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(
      premise,
    ),
  )

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(
      premise,
    ),
  )

  results = (
    apply_inference_matches_with_results(
      (
        first_match,
        second_match,
      )
    )
  )

  assert len(
    results
  ) == 2

  assert tuple(
    result.match
    for result
    in results
  ) == (
    first_match,
    second_match,
  )

  assert tuple(
    result.candidate_step.conclusion
    for result
    in results
  ) == (
    "first",
    "second",
  )


def test_apply_inference_matches_with_results_preserves_order():
  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(
      premise,
    ),
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(
      premise,
    ),
  )

  results = (
    apply_inference_matches_with_results(
      (
        second_match,
        first_match,
      )
    )
  )

  assert tuple(
    result.match
    for result
    in results
  ) == (
    second_match,
    first_match,
  )

  assert tuple(
    result.candidate_step.conclusion
    for result
    in results
  ) == (
    "second",
    "first",
  )


def test_apply_inference_matches_with_results_empty():
  assert (
    apply_inference_matches_with_results(
      ()
    )
    == ()
  )


def test_apply_inference_matches_with_results_accepts_list():
  rule = InferenceRule(
    name="given inference",
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  premise = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      premise,
    ),
  )

  results = (
    apply_inference_matches_with_results(
      [
        match,
      ]
    )
  )

  assert len(
    results
  ) == 1

  assert (
    results[0].match
    == match
  )


def test_apply_inference_matches_with_results_rejects_invalid_matches():
  with pytest.raises(TypeError):
    apply_inference_matches_with_results(
      "invalid"
    )


def test_derive_inference_round_result_records_application_results():
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

  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = derive_inference_round_result(
    rule,
    given,
  )

  assert len(
    result.application_results
  ) == 1

  application_result = (
    result.application_results[0]
  )

  assert (
    application_result.match
    == result.matches[0]
  )

  assert (
    application_result.candidate_step
    == result.candidate_steps[0]
  )


def test_derive_inference_round_result_application_results_match_existing_fields():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    given,
  )

  assert tuple(
    application_result.match
    for application_result
    in result.application_results
  ) == result.matches

  assert tuple(
    application_result.candidate_step
    for application_result
    in result.application_results
  ) == result.candidate_steps


def test_derive_inference_round_result_application_results_preserve_duplicate_candidates():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same"
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
      "same"
    ),
  )

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    given,
  )

  assert len(
    result.application_results
  ) == 2

  assert len(
    result.candidate_steps
  ) == 2

  assert len(
    result.new_steps
  ) == 1

  assert len(
    result.duplicate_rejected_steps
  ) == 1

  assert (
    result.application_results[
      0
    ].candidate_step
    == result.new_steps[0]
  )

  assert (
    result.application_results[
      1
    ].candidate_step
    == result.duplicate_rejected_steps[0]
  )


def test_run_inference_until_stable_records_application_results():
  initial = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation = Relation(
    lhs="middle",
    rhs="value",
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      relation
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      initial,
    )
  )

  assert len(
    result.round_results
  ) == 2

  first_round = (
    result.round_results[0]
  )

  second_round = (
    result.round_results[1]
  )

  assert len(
    first_round.application_results
  ) == 1

  assert (
    first_round.application_results[
      0
    ].match.inference_rule
    == first_rule
  )

  assert (
    first_round.application_results[
      0
    ].candidate_step.conclusion
    == relation
  )

  assert len(
    second_round.application_results
  ) == 2

  assert tuple(
    application_result.match.inference_rule
    for application_result
    in second_round.application_results
  ) == (
    first_rule,
    second_rule,
  )

  assert tuple(
    application_result.candidate_step.conclusion
    for application_result
    in second_round.application_results
  ) == (
    relation,
    "final",
  )


def test_inference_rejection_reason_values():
  assert (
    InferenceRejectionReason
    .ALREADY_KNOWN.value
    == "already_known"
  )

  assert (
    InferenceRejectionReason
    .SAME_ROUND_DUPLICATE.value
    == "same_round_duplicate"
  )


def test_inference_application_result_acceptance_defaults():
  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  candidate_step = ProofStep(
    conclusion="candidate",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  result = InferenceApplicationResult(
    match=match,
    candidate_step=candidate_step,
  )

  assert result.accepted is None

  assert (
    result.rejection_reason
    is None
  )


def test_classify_inference_application_result_accepts_new_candidate():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      given,
    ),
  )

  candidate = ProofStep(
    conclusion="derived",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  result = (
    classify_inference_application_results(
      (
        given,
      ),
      InferenceApplicationResult(
        match=match,
        candidate_step=candidate,
      ),
    )
  )

  assert len(
    result
  ) == 1

  assert result[0].accepted is True

  assert (
    result[0].rejection_reason
    is None
  )

  assert (
    result[0].candidate_step
    == candidate
  )


def test_classify_inference_application_result_rejects_already_known():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  known = ProofStep(
    conclusion="derived",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(
      given,
    ),
  )

  candidate = ProofStep(
    conclusion="derived",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  result = (
    classify_inference_application_results(
      (
        given,
        known,
      ),
      InferenceApplicationResult(
        match=match,
        candidate_step=candidate,
      ),
    )
  )

  assert result[0].accepted is False

  assert (
    result[0].rejection_reason
    == InferenceRejectionReason.ALREADY_KNOWN
  )


def test_classify_inference_application_results_rejects_same_round_duplicate():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="first rule",
  )

  second_rule = InferenceRule(
    name="second rule",
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(
      given,
    ),
  )

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(
      given,
    ),
  )

  first_candidate = ProofStep(
    conclusion="same",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=first_rule,
  )

  second_candidate = ProofStep(
    conclusion="same",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=second_rule,
  )

  result = (
    classify_inference_application_results(
      given,
      (
        InferenceApplicationResult(
          match=first_match,
          candidate_step=(
            first_candidate
          ),
        ),
        InferenceApplicationResult(
          match=second_match,
          candidate_step=(
            second_candidate
          ),
        ),
      ),
    )
  )

  assert result[0].accepted is True

  assert (
    result[0].rejection_reason
    is None
  )

  assert result[1].accepted is False

  assert (
    result[1].rejection_reason
    == (
      InferenceRejectionReason
      .SAME_ROUND_DUPLICATE
    )
  )


def test_classify_inference_application_results_preserves_order():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="first rule",
  )

  second_rule = InferenceRule(
    name="second rule",
  )

  first_match = InferenceMatch(
    inference_rule=first_rule,
    premises=(
      given,
    ),
  )

  second_match = InferenceMatch(
    inference_rule=second_rule,
    premises=(
      given,
    ),
  )

  first_candidate = ProofStep(
    conclusion="first",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=first_rule,
  )

  second_candidate = ProofStep(
    conclusion="second",
    premises=(
      given,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=second_rule,
  )

  result = (
    classify_inference_application_results(
      given,
      (
        InferenceApplicationResult(
          match=first_match,
          candidate_step=(
            first_candidate
          ),
        ),
        InferenceApplicationResult(
          match=second_match,
          candidate_step=(
            second_candidate
          ),
        ),
      ),
    )
  )

  assert tuple(
    application_result.candidate_step.conclusion
    for application_result
    in result
  ) == (
    "first",
    "second",
  )


def test_classify_inference_application_results_empty():
  result = (
    classify_inference_application_results(
      (),
      (),
    )
  )

  assert result == ()


def test_classify_inference_application_results_accepts_list():
  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  candidate = ProofStep(
    conclusion="candidate",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  result = (
    classify_inference_application_results(
      [],
      [
        InferenceApplicationResult(
          match=match,
          candidate_step=candidate,
        ),
      ],
    )
  )

  assert result[0].accepted is True


def test_classify_inference_application_results_rejects_invalid_input():
  with pytest.raises(TypeError):
    classify_inference_application_results(
      (),
      "invalid",
    )


def test_classify_inference_application_results_rejects_invalid_item():
  with pytest.raises(TypeError):
    classify_inference_application_results(
      (),
      [
        "invalid",
      ],
    )


def test_derive_inference_round_result_marks_accepted_application():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "derived"
    ),
  )

  result = derive_inference_round_result(
    rule,
    given,
  )

  assert len(
    result.application_results
  ) == 1

  application_result = (
    result.application_results[0]
  )

  assert (
    application_result.accepted
    is True
  )

  assert (
    application_result.rejection_reason
    is None
  )

  assert result.new_steps == (
    application_result.candidate_step,
  )

  assert (
    result.duplicate_rejected_steps
    == ()
  )


def test_derive_inference_round_result_marks_same_round_duplicate():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "same"
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
      "same"
    ),
  )

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    given,
  )

  assert len(
    result.application_results
  ) == 2

  first_result = (
    result.application_results[0]
  )

  second_result = (
    result.application_results[1]
  )

  assert first_result.accepted is True

  assert (
    first_result.rejection_reason
    is None
  )

  assert second_result.accepted is False

  assert (
    second_result.rejection_reason
    == (
      InferenceRejectionReason
      .SAME_ROUND_DUPLICATE
    )
  )

  assert result.new_steps == (
    first_result.candidate_step,
  )

  assert (
    result.duplicate_rejected_steps
    == (
      second_result.candidate_step,
    )
  )


def test_derive_inference_round_result_views_match_application_status():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  known = ProofStep(
    conclusion="known",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = InferenceRule(
    name="accepted rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "new"
    ),
  )

  second_rule = InferenceRule(
    name="known rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      "known"
    ),
  )

  result = derive_inference_round_result(
    (
      first_rule,
      second_rule,
    ),
    (
      given,
      known,
    ),
  )

  accepted_steps = tuple(
    application_result.candidate_step
    for application_result
    in result.application_results
    if application_result.accepted
  )

  rejected_steps = tuple(
    application_result.candidate_step
    for application_result
    in result.application_results
    if (
      application_result.accepted
      is False
    )
  )

  assert (
    accepted_steps
    == result.new_steps
  )

  assert (
    rejected_steps
    == result.duplicate_rejected_steps
  )


def test_run_inference_until_stable_preserves_application_acceptance_status():
  initial = ProofStep(
    conclusion="initial",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation = Relation(
    lhs="middle",
    rhs="value",
  )

  first_rule = InferenceRule(
    name="first rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=lambda premises: (
      relation
    ),
  )

  second_rule = InferenceRule(
    name="second rule",
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

  result = (
    run_inference_until_stable_with_history(
      (
        first_rule,
        second_rule,
      ),
      initial,
    )
  )

  assert result.round_count == 2

  first_round = (
    result.round_results[0]
  )

  second_round = (
    result.round_results[1]
  )

  assert (
    first_round.application_results[
      0
    ].accepted
    is True
  )

  assert (
    second_round.application_results[
      0
    ].accepted
    is False
  )

  assert (
    second_round.application_results[
      0
    ].rejection_reason
    == InferenceRejectionReason.ALREADY_KNOWN
  )

  assert (
    second_round.application_results[
      1
    ].accepted
    is True
  )

  assert (
    second_round.application_results[
      1
    ].rejection_reason
    is None
  )


def test_find_all_matching_premises_single_match():
  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = find_all_matching_premises(
    rule,
    given,
  )

  assert result == (
    (
      given,
    ),
  )


def test_find_all_matching_premises_multiple_single_pattern_matches():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_all_matching_premises(
    rule,
    (
      first,
      second,
    ),
  )

  assert result == (
    (
      first,
    ),
    (
      second,
    ),
  )


def test_find_all_matching_premises_multiple_assignments():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  result = find_all_matching_premises(
    rule,
    (
      first,
      second,
    ),
  )

  assert result == (
    (
      first,
      second,
    ),
    (
      second,
      first,
    ),
  )


def test_find_all_matching_premises_does_not_reuse_step():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  result = find_all_matching_premises(
    rule,
    given,
  )

  assert result == ()


def test_find_all_matching_premises_preserves_pattern_order():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  relation = ProofStep(
    conclusion="relation",
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = InferenceRule(
    name="ordered rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_all_matching_premises(
    rule,
    (
      given,
      relation,
    ),
  )

  assert result == (
    (
      relation,
      given,
    ),
  )


def test_find_all_matching_premises_empty_rule():
  rule = InferenceRule(
    name="empty rule",
  )

  result = find_all_matching_premises(
    rule,
    (),
  )

  assert result == (
    (),
  )


def test_find_all_matching_premises_empty_rule_ignores_available_steps():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="empty rule",
  )

  result = find_all_matching_premises(
    rule,
    given,
  )

  assert result == (
    (),
  )


def test_find_all_matching_premises_returns_empty_when_no_assignment():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  result = find_all_matching_premises(
    rule,
    given,
  )

  assert result == ()


def test_find_all_matching_premises_accepts_list():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_all_matching_premises(
    rule,
    [
      given,
    ],
  )

  assert result == (
    (
      given,
    ),
  )


def test_find_all_matching_premises_rejects_invalid_rule():
  with pytest.raises(TypeError):
    find_all_matching_premises(
      "invalid",
      (),
    )


def test_find_all_matching_premises_rejects_invalid_steps():
  rule = InferenceRule(
    name="rule",
  )

  with pytest.raises(TypeError):
    find_all_matching_premises(
      rule,
      "invalid",
    )


def test_find_inference_matches_for_rule_multiple():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_inference_matches_for_rule(
    rule,
    (
      first,
      second,
    ),
  )

  assert result == (
    InferenceMatch(
      inference_rule=rule,
      premises=(
        first,
      ),
    ),
    InferenceMatch(
      inference_rule=rule,
      premises=(
        second,
      ),
    ),
  )


def test_find_inference_matches_for_rule_returns_empty():
  given = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.RELATION,
      ),
    ),
  )

  assert (
    find_inference_matches_for_rule(
      rule,
      given,
    )
    == ()
  )


def test_find_inference_match_remains_first_match_view():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_inference_match(
    rule,
    (
      first,
      second,
    ),
  )

  assert result == InferenceMatch(
    inference_rule=rule,
    premises=(
      first,
    ),
  )


def test_find_inference_matches_collects_all_matches_per_rule():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="given rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
  )

  result = find_inference_matches(
    rule,
    (
      first,
      second,
    ),
  )

  assert tuple(
    match.premises
    for match in result
  ) == (
    (
      first,
    ),
    (
      second,
    ),
  )


def test_find_inference_matches_preserves_rule_then_assignment_order():
  first = ProofStep(
    conclusion="first",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second = ProofStep(
    conclusion="second",
    premises=(),
    rule=ProofRule.GIVEN,
  )

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

  result = find_inference_matches(
    (
      first_rule,
      second_rule,
    ),
    (
      first,
      second,
    ),
  )

  assert tuple(
    (
      match.inference_rule,
      match.premises,
    )
    for match
    in result
  ) == (
    (
      first_rule,
      (
        first,
      ),
    ),
    (
      first_rule,
      (
        second,
      ),
    ),
    (
      second_rule,
      (
        first,
      ),
    ),
    (
      second_rule,
      (
        second,
      ),
    ),
  )


def test_pattern_variable():
  variable = PatternVariable(
    name="x",
  )

  assert variable.name == "x"


def test_pattern_variable_is_structurally_equal():
  first = PatternVariable(
    name="x",
  )

  second = PatternVariable(
    name="x",
  )

  assert first == second


def test_pattern_variable_with_different_name_is_not_equal():
  first = PatternVariable(
    name="x",
  )

  second = PatternVariable(
    name="y",
  )

  assert first != second


def test_pattern_variable_rejects_non_string_name():
  with pytest.raises(TypeError):
    PatternVariable(
      name=1,
    )


def test_pattern_variable_rejects_empty_name():
  with pytest.raises(ValueError):
    PatternVariable(
      name="",
    )


def test_variable_binding():
  variable = PatternVariable(
    name="x",
  )

  binding = VariableBinding(
    variable=variable,
    value="alpha",
  )

  assert binding.variable == variable
  assert binding.value == "alpha"


def test_variable_binding_is_structurally_equal():
  first = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  second = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  assert first == second


def test_variable_binding_with_different_variable_is_not_equal():
  first = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  second = VariableBinding(
    variable=PatternVariable(
      name="y",
    ),
    value="alpha",
  )

  assert first != second


def test_variable_binding_with_different_value_is_not_equal():
  variable = PatternVariable(
    name="x",
  )

  first = VariableBinding(
    variable=variable,
    value="alpha",
  )

  second = VariableBinding(
    variable=variable,
    value="beta",
  )

  assert first != second


def test_variable_binding_accepts_arbitrary_value():
  relation = Relation(
    lhs="alpha",
    rhs="beta",
  )

  binding = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value=relation,
  )

  assert binding.value == relation


def test_variable_binding_rejects_invalid_variable():
  with pytest.raises(TypeError):
    VariableBinding(
      variable="x",
      value="alpha",
    )


def test_match_pattern_value_binds_pattern_variable():
  variable = PatternVariable(
    name="x",
  )

  result = match_pattern_value(
    variable,
    "alpha",
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_pattern_value_variable_accepts_arbitrary_value():
  variable = PatternVariable(
    name="x",
  )

  relation = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_pattern_value(
    variable,
    relation,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value=relation,
    ),
  )


def test_match_pattern_value_equal_literal_matches_without_binding():
  result = match_pattern_value(
    "alpha",
    "alpha",
  )

  assert result == ()


def test_match_pattern_value_different_literal_does_not_match():
  result = match_pattern_value(
    "alpha",
    "beta",
  )

  assert result is None


def test_match_pattern_value_equal_relation_matches_without_binding():
  relation = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_pattern_value(
    relation,
    Relation(
      lhs="alpha",
      rhs="beta",
    ),
  )

  assert result == ()


def test_match_pattern_value_different_relation_does_not_match():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  value = Relation(
    lhs="alpha",
    rhs="gamma",
  )

  result = match_pattern_value(
    pattern,
    value,
  )

  assert result is None


def test_match_pattern_value_pattern_variable_can_bind_none():
  variable = PatternVariable(
    name="x",
  )

  result = match_pattern_value(
    variable,
    None,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value=None,
    ),
  )


def test_match_relation_pattern_binds_lhs_variable():
  variable = PatternVariable(
    name="x",
  )

  pattern = Relation(
    lhs=variable,
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  value = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_relation_pattern_binds_rhs_variable():
  variable = PatternVariable(
    name="x",
  )

  pattern = Relation(
    lhs="alpha",
    rhs=variable,
  )

  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="beta",
    ),
  )


def test_match_relation_pattern_binds_both_sides():
  lhs_variable = PatternVariable(
    name="x",
  )

  rhs_variable = PatternVariable(
    name="y",
  )

  pattern = Relation(
    lhs=lhs_variable,
    rhs=rhs_variable,
  )

  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=lhs_variable,
      value="alpha",
    ),
    VariableBinding(
      variable=rhs_variable,
      value="beta",
    ),
  )


def test_match_relation_pattern_equal_literals_matches_without_binding():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == ()


def test_match_relation_pattern_rejects_wrong_lhs():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  value = Relation(
    lhs="gamma",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result is None


def test_match_relation_pattern_rejects_wrong_rhs():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  value = Relation(
    lhs="alpha",
    rhs="gamma",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result is None


def test_match_relation_pattern_rejects_wrong_relation_type():
  pattern = Relation(
    lhs=PatternVariable(
      name="x",
    ),
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  value = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.EQUALITY,
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result is None


def test_match_relation_pattern_preserves_binding_order():
  lhs_variable = PatternVariable(
    name="x",
  )

  rhs_variable = PatternVariable(
    name="y",
  )

  pattern = Relation(
    lhs=lhs_variable,
    rhs=rhs_variable,
  )

  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert tuple(
    binding.variable
    for binding in result
  ) == (
    lhs_variable,
    rhs_variable,
  )


def test_match_relation_pattern_rejects_invalid_pattern():
  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  with pytest.raises(TypeError):
    match_relation_pattern(
      "invalid",
      value,
    )


def test_match_relation_pattern_rejects_invalid_value():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  with pytest.raises(TypeError):
    match_relation_pattern(
      pattern,
      "invalid",
    )


def test_merge_variable_bindings_empty():
  result = merge_variable_bindings(
    ()
  )

  assert result == ()


def test_merge_variable_bindings_single():
  binding = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  result = merge_variable_bindings(
    binding
  )

  assert result == (
    binding,
  )


def test_merge_variable_bindings_distinct_variables():
  first = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  second = VariableBinding(
    variable=PatternVariable(
      name="y",
    ),
    value="beta",
  )

  result = merge_variable_bindings(
    (
      first,
      second,
    )
  )

  assert result == (
    first,
    second,
  )


def test_merge_variable_bindings_merges_same_variable_same_value():
  variable = PatternVariable(
    name="x",
  )

  first = VariableBinding(
    variable=variable,
    value="alpha",
  )

  second = VariableBinding(
    variable=variable,
    value="alpha",
  )

  result = merge_variable_bindings(
    (
      first,
      second,
    )
  )

  assert result == (
    first,
  )


def test_merge_variable_bindings_rejects_conflicting_values():
  variable = PatternVariable(
    name="x",
  )

  first = VariableBinding(
    variable=variable,
    value="alpha",
  )

  second = VariableBinding(
    variable=variable,
    value="beta",
  )

  result = merge_variable_bindings(
    (
      first,
      second,
    )
  )

  assert result is None


def test_merge_variable_bindings_preserves_first_binding_order():
  x = PatternVariable(
    name="x",
  )

  y = PatternVariable(
    name="y",
  )

  first = VariableBinding(
    variable=y,
    value="beta",
  )

  second = VariableBinding(
    variable=x,
    value="alpha",
  )

  duplicate = VariableBinding(
    variable=y,
    value="beta",
  )

  result = merge_variable_bindings(
    (
      first,
      second,
      duplicate,
    )
  )

  assert result == (
    first,
    second,
  )


def test_merge_variable_bindings_accepts_list():
  binding = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  result = merge_variable_bindings(
    [
      binding,
    ]
  )

  assert result == (
    binding,
  )


def test_merge_variable_bindings_rejects_invalid_input():
  with pytest.raises(TypeError):
    merge_variable_bindings(
      "invalid"
    )


def test_merge_variable_bindings_rejects_invalid_item():
  binding = VariableBinding(
    variable=PatternVariable(
      name="x",
    ),
    value="alpha",
  )

  with pytest.raises(TypeError):
    merge_variable_bindings(
      (
        binding,
        "invalid",
      )
    )


def test_match_relation_pattern_merges_repeated_variable():
  variable = PatternVariable(
    name="x",
  )

  pattern = Relation(
    lhs=variable,
    rhs=variable,
  )

  value = Relation(
    lhs="alpha",
    rhs="alpha",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_relation_pattern_rejects_conflicting_repeated_variable():
  variable = PatternVariable(
    name="x",
  )

  pattern = Relation(
    lhs=variable,
    rhs=variable,
  )

  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result is None


def test_match_relation_pattern_repeated_structurally_equal_variable():
  pattern = Relation(
    lhs=PatternVariable(
      name="x",
    ),
    rhs=PatternVariable(
      name="x",
    ),
  )

  value = Relation(
    lhs="alpha",
    rhs="alpha",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=PatternVariable(
        name="x",
      ),
      value="alpha",
    ),
  )


def test_match_relation_pattern_distinct_variables_remain_distinct():
  x = PatternVariable(
    name="x",
  )

  y = PatternVariable(
    name="y",
  )

  pattern = Relation(
    lhs=x,
    rhs=y,
  )

  value = Relation(
    lhs="alpha",
    rhs="alpha",
  )

  result = match_relation_pattern(
    pattern,
    value,
  )

  assert result == (
    VariableBinding(
      variable=x,
      value="alpha",
    ),
    VariableBinding(
      variable=y,
      value="alpha",
    ),
  )


def test_premise_pattern_relation_pattern_defaults_to_none():
  pattern = PremisePattern()

  assert (
    pattern.relation_pattern
    is None
  )


def test_premise_pattern_with_relation_pattern():
  relation_pattern = Relation(
    lhs=PatternVariable(
      name="x",
    ),
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  pattern = PremisePattern(
    relation_pattern=relation_pattern,
  )

  assert (
    pattern.relation_pattern
    == relation_pattern
  )


def test_premise_pattern_matches_relation_pattern():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=PatternVariable(
        name="x",
      ),
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_relation_pattern_lhs():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="beta",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_relation_pattern_rhs():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=PatternVariable(
        name="x",
      ),
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_rejects_wrong_relation_pattern_type():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=PatternVariable(
        name="x",
      ),
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_relation_pattern_requires_relation_conclusion():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=PatternVariable(
        name="x",
      ),
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion="not a relation",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert not matches_premise_pattern(
    pattern,
    step,
  )


def test_premise_pattern_relation_pattern_respects_repeated_variable():
  variable = PatternVariable(
    name="x",
  )

  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=variable,
      rhs=variable,
    ),
  )

  matching_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  nonmatching_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert matches_premise_pattern(
    pattern,
    matching_step,
  )

  assert not matches_premise_pattern(
    pattern,
    nonmatching_step,
  )


def test_match_premise_pattern_empty_pattern():
  pattern = PremisePattern()

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = match_premise_pattern(
    pattern,
    step,
  )

  assert result == ()


def test_match_premise_pattern_matches_without_binding():
  pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = match_premise_pattern(
    pattern,
    step,
  )

  assert result == ()


def test_match_premise_pattern_returns_relation_binding():
  variable = PatternVariable(
    name="x",
  )

  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=variable,
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = match_premise_pattern(
    pattern,
    step,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_premise_pattern_returns_multiple_relation_bindings():
  x = PatternVariable(
    name="x",
  )

  y = PatternVariable(
    name="y",
  )

  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=x,
      rhs=y,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = match_premise_pattern(
    pattern,
    step,
  )

  assert result == (
    VariableBinding(
      variable=x,
      value="alpha",
    ),
    VariableBinding(
      variable=y,
      value="beta",
    ),
  )


def test_match_premise_pattern_rejects_wrong_proof_rule():
  pattern = PremisePattern(
    proof_rule=ProofRule.RELATION,
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    match_premise_pattern(
      pattern,
      step,
    )
    is None
  )


def test_match_premise_pattern_rejects_wrong_statement_type():
  pattern = PremisePattern(
    statement_type=Relation,
  )

  step = ProofStep(
    conclusion="not a relation",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    match_premise_pattern(
      pattern,
      step,
    )
    is None
  )


def test_match_premise_pattern_rejects_wrong_relation_type():
  pattern = PremisePattern(
    relation_type=RelationType.ZERO,
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    match_premise_pattern(
      pattern,
      step,
    )
    is None
  )


def test_match_premise_pattern_rejects_wrong_relation_pattern():
  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=PatternVariable(
        name="x",
      ),
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    match_premise_pattern(
      pattern,
      step,
    )
    is None
  )


def test_match_premise_pattern_respects_repeated_variable_consistency():
  variable = PatternVariable(
    name="x",
  )

  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=variable,
      rhs=variable,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = match_premise_pattern(
    pattern,
    step,
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_premise_pattern_rejects_repeated_variable_conflict():
  variable = PatternVariable(
    name="x",
  )

  pattern = PremisePattern(
    relation_pattern=Relation(
      lhs=variable,
      rhs=variable,
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    match_premise_pattern(
      pattern,
      step,
    )
    is None
  )


def test_match_premise_pattern_rejects_invalid_pattern():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    match_premise_pattern(
      "invalid",
      step,
    )


def test_match_premise_pattern_rejects_invalid_step():
  pattern = PremisePattern()

  with pytest.raises(TypeError):
    match_premise_pattern(
      pattern,
      "invalid",
    )


def test_match_inference_rule_bindings_empty_rule():
  rule = InferenceRule(
    name="empty rule",
  )

  result = (
    match_inference_rule_bindings(
      rule,
      (),
    )
  )

  assert result == ()


def test_match_inference_rule_bindings_without_variables():
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

  result = (
    match_inference_rule_bindings(
      rule,
      step,
    )
  )

  assert result == ()


def test_match_inference_rule_bindings_single_premise_binding():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = (
    match_inference_rule_bindings(
      rule,
      step,
    )
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_inference_rule_bindings_merges_shared_variable():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  first_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  second_step = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = (
    match_inference_rule_bindings(
      rule,
      (
        first_step,
        second_step,
      ),
    )
  )

  assert result == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_match_inference_rule_bindings_rejects_shared_variable_conflict():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  first_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  second_step = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = (
    match_inference_rule_bindings(
      rule,
      (
        first_step,
        second_step,
      ),
    )
  )

  assert result is None


def test_match_inference_rule_bindings_preserves_distinct_variables():
  x = PatternVariable(
    name="x",
  )

  y = PatternVariable(
    name="y",
  )

  rule = InferenceRule(
    name="two variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=x,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=y,
        ),
      ),
    ),
  )

  first_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  second_step = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = (
    match_inference_rule_bindings(
      rule,
      (
        first_step,
        second_step,
      ),
    )
  )

  assert result == (
    VariableBinding(
      variable=x,
      value="alpha",
    ),
    VariableBinding(
      variable=y,
      value="beta",
    ),
  )


def test_match_inference_rule_bindings_rejects_premise_mismatch():
  rule = InferenceRule(
    name="relation rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs="alpha",
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="beta",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    match_inference_rule_bindings(
      rule,
      step,
    )
    is None
  )


def test_match_inference_rule_bindings_rejects_wrong_step_count():
  rule = InferenceRule(
    name="two premise rule",
    premise_patterns=(
      PremisePattern(),
      PremisePattern(),
    ),
  )

  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    match_inference_rule_bindings(
      rule,
      step,
    )
    is None
  )


def test_match_inference_rule_bindings_rejects_invalid_rule():
  step = ProofStep(
    conclusion="given",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(TypeError):
    match_inference_rule_bindings(
      "invalid",
      step,
    )


def test_match_inference_rule_bindings_rejects_invalid_steps():
  rule = InferenceRule(
    name="rule",
  )

  with pytest.raises(TypeError):
    match_inference_rule_bindings(
      rule,
      "invalid",
    )


def test_find_all_matching_premises_enforces_shared_binding_consistency():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  alpha_zero = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_alpha = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_beta = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_all_matching_premises(
    rule,
    (
      alpha_zero,
      source_beta,
      source_alpha,
    ),
  )

  assert result == (
    (
      alpha_zero,
      source_alpha,
    ),
  )


def test_find_all_matching_premises_backtracks_over_binding_conflict():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  alpha_zero = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  beta_zero = ProofStep(
    conclusion=Relation(
      lhs="beta",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_beta = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_all_matching_premises(
    rule,
    (
      alpha_zero,
      beta_zero,
      source_beta,
    ),
  )

  assert result == (
    (
      beta_zero,
      source_beta,
    ),
  )


def test_find_all_matching_premises_enumerates_only_binding_consistent_assignments():
  variable = PatternVariable(
    name="x",
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=RelationType.ZERO,
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  alpha_zero = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  beta_zero = ProofStep(
    conclusion=Relation(
      lhs="beta",
      rhs="0",
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_alpha = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_beta = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="beta",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  result = find_all_matching_premises(
    rule,
    (
      alpha_zero,
      beta_zero,
      source_alpha,
      source_beta,
    ),
  )

  assert result == (
    (
      alpha_zero,
      source_alpha,
    ),
    (
      beta_zero,
      source_beta,
    ),
  )


def test_inference_match_bindings_default_to_empty():
  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
  )

  assert match.bindings == ()


def test_inference_match_accepts_bindings():
  variable = PatternVariable(
    "x"
  )

  binding = VariableBinding(
    variable=variable,
    value="alpha",
  )

  rule = InferenceRule(
    name="rule",
  )

  match = InferenceMatch(
    inference_rule=rule,
    premises=(),
    bindings=(
      binding,
    ),
  )

  assert match.bindings == (
    binding,
  )


def test_find_inference_match_stores_binding():
  variable = PatternVariable(
    "x"
  )

  rule = InferenceRule(
    name="variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=(
            RelationType.ZERO
          ),
        ),
      ),
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  match = find_inference_match(
    rule,
    step,
  )

  assert match.bindings == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_find_inference_match_stores_merged_shared_binding():
  variable = PatternVariable(
    "x"
  )

  rule = InferenceRule(
    name="shared variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=(
            RelationType.ZERO
          ),
        ),
      ),
      PremisePattern(
        relation_pattern=Relation(
          lhs="source",
          rhs=variable,
        ),
      ),
    ),
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  source_step = ProofStep(
    conclusion=Relation(
      lhs="source",
      rhs="alpha",
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
      source_step,
    ),
  )

  assert match.premises == (
    zero_step,
    source_step,
  )

  assert match.bindings == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )


def test_find_inference_matches_for_rule_stores_distinct_bindings():
  variable = PatternVariable(
    "x"
  )

  rule = InferenceRule(
    name="variable rule",
    premise_patterns=(
      PremisePattern(
        relation_pattern=Relation(
          lhs=variable,
          rhs="0",
          relation_type=(
            RelationType.ZERO
          ),
        ),
      ),
    ),
  )

  alpha_step = ProofStep(
    conclusion=Relation(
      lhs="alpha",
      rhs="0",
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  beta_step = ProofStep(
    conclusion=Relation(
      lhs="beta",
      rhs="0",
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  matches = (
    find_inference_matches_for_rule(
      rule,
      (
        alpha_step,
        beta_step,
      ),
    )
  )

  assert len(matches) == 2

  assert matches[0].premises == (
    alpha_step,
  )

  assert matches[0].bindings == (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  assert matches[1].premises == (
    beta_step,
  )

  assert matches[1].bindings == (
    VariableBinding(
      variable=variable,
      value="beta",
    ),
  )


def test_lookup_variable_binding():
  variable = PatternVariable(
    "x"
  )

  bindings = (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  assert lookup_variable_binding(
    variable,
    bindings,
  ) == "alpha"


def test_lookup_variable_binding_structurally_equal_variable():
  bindings = (
    VariableBinding(
      variable=PatternVariable(
        "x"
      ),
      value="alpha",
    ),
  )

  assert lookup_variable_binding(
    PatternVariable(
      "x"
    ),
    bindings,
  ) == "alpha"


def test_lookup_variable_binding_returns_none_when_missing():
  bindings = (
    VariableBinding(
      variable=PatternVariable(
        "x"
      ),
      value="alpha",
    ),
  )

  assert (
    lookup_variable_binding(
      PatternVariable(
        "y"
      ),
      bindings,
    )
    is None
  )


def test_lookup_variable_binding_accepts_single_binding():
  variable = PatternVariable(
    "x"
  )

  binding = VariableBinding(
    variable=variable,
    value="alpha",
  )

  assert lookup_variable_binding(
    variable,
    binding,
  ) == "alpha"


def test_lookup_variable_binding_accepts_list():
  variable = PatternVariable(
    "x"
  )

  binding = VariableBinding(
    variable=variable,
    value="alpha",
  )

  assert lookup_variable_binding(
    variable,
    [
      binding,
    ],
  ) == "alpha"


def test_lookup_variable_binding_rejects_invalid_variable():
  with pytest.raises(TypeError):
    lookup_variable_binding(
      "x",
      (),
    )


def test_lookup_variable_binding_rejects_conflicting_bindings():
  variable = PatternVariable(
    "x"
  )

  with pytest.raises(ValueError):
    lookup_variable_binding(
      variable,
      (
        VariableBinding(
          variable=variable,
          value="alpha",
        ),
        VariableBinding(
          variable=variable,
          value="beta",
        ),
      ),
    )


def test_substitute_pattern_value_variable():
  variable = PatternVariable(
    "x"
  )

  bindings = (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  assert substitute_pattern_value(
    variable,
    bindings,
  ) == "alpha"


def test_substitute_pattern_value_literal():
  assert substitute_pattern_value(
    "alpha",
    (),
  ) == "alpha"


def test_substitute_pattern_value_unbound_variable_returns_none():
  variable = PatternVariable(
    "x"
  )

  assert (
    substitute_pattern_value(
      variable,
      (),
    )
    is None
  )


def test_substitute_pattern_value_preserves_arbitrary_literal():
  value = Relation(
    lhs="alpha",
    rhs="beta",
  )

  assert substitute_pattern_value(
    value,
    (),
  ) == value


def test_substitute_relation_pattern_lhs_variable():
  variable = PatternVariable(
    "x"
  )

  pattern = Relation(
    lhs=variable,
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  bindings = (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  result = substitute_relation_pattern(
    pattern,
    bindings,
  )

  assert result == Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )


def test_substitute_relation_pattern_rhs_variable():
  variable = PatternVariable(
    "x"
  )

  pattern = Relation(
    lhs="source",
    rhs=variable,
  )

  bindings = (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  result = substitute_relation_pattern(
    pattern,
    bindings,
  )

  assert result == Relation(
    lhs="source",
    rhs="alpha",
  )


def test_substitute_relation_pattern_both_variables():
  x = PatternVariable(
    "x"
  )

  y = PatternVariable(
    "y"
  )

  pattern = Relation(
    lhs=x,
    rhs=y,
  )

  bindings = (
    VariableBinding(
      variable=x,
      value="alpha",
    ),
    VariableBinding(
      variable=y,
      value="beta",
    ),
  )

  result = substitute_relation_pattern(
    pattern,
    bindings,
  )

  assert result == Relation(
    lhs="alpha",
    rhs="beta",
  )


def test_substitute_relation_pattern_preserves_literals():
  pattern = Relation(
    lhs="alpha",
    rhs="beta",
  )

  result = substitute_relation_pattern(
    pattern,
    (),
  )

  assert result == pattern


def test_substitute_relation_pattern_preserves_metadata():
  variable = PatternVariable(
    "x"
  )

  source = "Toda"

  pattern = Relation(
    lhs=variable,
    rhs="0",
    relation_type=RelationType.ZERO,
    source=source,
    note="example note",
  )

  bindings = (
    VariableBinding(
      variable=variable,
      value="alpha",
    ),
  )

  result = substitute_relation_pattern(
    pattern,
    bindings,
  )

  assert (
    result.relation_type
    == RelationType.ZERO
  )

  assert result.source == source

  assert (
    result.note
    == "example note"
  )


def test_substitute_relation_pattern_unbound_variable_becomes_none():
  variable = PatternVariable(
    "x"
  )

  pattern = Relation(
    lhs=variable,
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  result = substitute_relation_pattern(
    pattern,
    (),
  )

  assert result == Relation(
    lhs=None,
    rhs="0",
    relation_type=RelationType.ZERO,
  )


def test_substitute_relation_pattern_rejects_invalid_pattern():
  with pytest.raises(TypeError):
    substitute_relation_pattern(
      "invalid",
      (),
    )


def test_inference_rule_conclusion_pattern_defaults_to_none():
  rule = InferenceRule(
    name="rule",
  )

  assert (
    rule.conclusion_pattern
    is None
  )


def test_inference_rule_with_conclusion_pattern():
  conclusion_pattern = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name="rule",
    conclusion_pattern=(
      conclusion_pattern
    ),
  )

  assert (
    rule.conclusion_pattern
    == conclusion_pattern
  )


def test_inference_rule_conclusion_pattern_with_variable():
  variable = PatternVariable(
    "x"
  )

  conclusion_pattern = Relation(
    lhs=variable,
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name="rule",
    conclusion_pattern=(
      conclusion_pattern
    ),
  )

  assert (
    rule.conclusion_pattern
    == Relation(
      lhs=variable,
      rhs="0",
      relation_type=RelationType.ZERO,
    )
  )


def test_inference_rule_conclusion_pattern_is_backward_compatible():
  builder = lambda premises: (
    "derived"
  )

  rule = InferenceRule(
    name="rule",
    conclusion_builder=builder,
  )

  assert (
    rule.conclusion_builder
    is builder
  )

  assert (
    rule.conclusion_pattern
    is None
  )


def test_inference_rule_can_hold_builder_and_conclusion_pattern():
  builder = lambda premises: (
    "derived"
  )

  conclusion_pattern = Relation(
    lhs="alpha",
    rhs="0",
    relation_type=RelationType.ZERO,
  )

  rule = InferenceRule(
    name="rule",
    conclusion_builder=builder,
    conclusion_pattern=(
      conclusion_pattern
    ),
  )

  assert (
    rule.conclusion_builder
    is builder
  )

  assert (
    rule.conclusion_pattern
    == conclusion_pattern
  )











