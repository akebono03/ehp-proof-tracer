from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  Relation,
  RelationType,
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



