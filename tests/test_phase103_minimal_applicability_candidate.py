from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ProofStep,
  VariableBinding,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase103ExampleStatement:
  value: object


@dataclass(frozen=True)
class Phase103OtherStatement:
  value: object


def build_phase103_2_data(
  *,
  fixed_point_safe=False,
):
  variable = PatternVariable(
    name="value",
  )

  premise_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=Phase103ExampleStatement,
    statement_pattern=(
      Phase103ExampleStatement(
        value=variable,
      )
    ),
  )

  rule = InferenceRule(
    name=(
      "phase103 minimal "
      "applicability candidate rule"
    ),
    premise_patterns=(
      premise_pattern,
    ),
  )

  catalog_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase103.minimal."
        "applicability-candidate"
      ),
      rule=rule,
      conclusion_type=(
        Phase103OtherStatement
      ),
      fixed_point_safe=(
        fixed_point_safe
      ),
    )
  )

  source_step = ProofStep(
    conclusion=(
      Phase103ExampleStatement(
        value="known",
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  binding = VariableBinding(
    variable=variable,
    value="known",
  )

  return {
    "variable": variable,
    "premise_pattern": (
      premise_pattern
    ),
    "rule": rule,
    "catalog_entry": (
      catalog_entry
    ),
    "source_step": source_step,
    "binding": binding,
  }


def test_phase103_2_candidate_accepts_minimum_valid_data():
  data = build_phase103_2_data()

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )
  )

  assert (
    candidate.catalog_entry
    is data[
      "catalog_entry"
    ]
  )

  assert (
    candidate.premise_index
    == 0
  )

  assert (
    candidate.premise_pattern
    is data[
      "premise_pattern"
    ]
  )

  assert (
    candidate.source_step
    is data[
      "source_step"
    ]
  )

  assert (
    candidate.bindings
    == ()
  )


def test_phase103_2_candidate_exposes_derived_rule_statement_and_safety():
  data = build_phase103_2_data(
    fixed_point_safe=True,
  )

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )
  )

  assert (
    candidate.inference_rule
    is data[
      "rule"
    ]
  )

  assert (
    candidate.matched_statement
    is data[
      "source_step"
    ].conclusion
  )

  assert (
    candidate.fixed_point_safe
    is True
  )


def test_phase103_2_candidate_preserves_variable_bindings():
  data = build_phase103_2_data()

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
      bindings=(
        data[
          "binding"
        ],
      ),
    )
  )

  assert (
    candidate.bindings
    == (
      data[
        "binding"
      ],
    )
  )


def test_phase103_2_candidate_does_not_require_fixed_point_safe_rule():
  data = build_phase103_2_data(
    fixed_point_safe=False,
  )

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )
  )

  assert (
    candidate.fixed_point_safe
    is False
  )


def test_phase103_2_candidate_rejects_invalid_catalog_entry():
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "catalog_entry must be an "
      "InferenceRuleCatalogEntry"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=object(),
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )


@pytest.mark.parametrize(
  "premise_index",
  (
    True,
    "0",
  ),
)
def test_phase103_2_candidate_rejects_non_int_premise_index(
  premise_index,
):
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "premise_index must be an int"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=premise_index,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )


@pytest.mark.parametrize(
  "premise_index",
  (
    -1,
    1,
  ),
)
def test_phase103_2_candidate_rejects_out_of_range_premise_index(
  premise_index,
):
  data = build_phase103_2_data()

  with pytest.raises(
    ValueError,
    match=(
      "premise_index must identify a "
      "catalog-entry rule premise"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=premise_index,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
    )


def test_phase103_2_candidate_rejects_invalid_premise_pattern():
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "premise_pattern must be a "
      "PremisePattern"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=object(),
      source_step=data[
        "source_step"
      ],
    )


def test_phase103_2_candidate_rejects_premise_pattern_from_other_position():
  data = build_phase103_2_data()

  second_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=(
      Phase103OtherStatement
    ),
  )

  rule = InferenceRule(
    name=(
      "phase103 two-premise rule"
    ),
    premise_patterns=(
      data[
        "premise_pattern"
      ],
      second_pattern,
    ),
  )

  entry = InferenceRuleCatalogEntry(
    key=(
      "phase103.two-premise"
    ),
    rule=rule,
    conclusion_type=(
      Phase103OtherStatement
    ),
  )

  with pytest.raises(
    ValueError,
    match=(
      "premise_pattern must match the "
      "catalog-entry rule premise"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=entry,
      premise_index=0,
      premise_pattern=second_pattern,
      source_step=data[
        "source_step"
      ],
    )


def test_phase103_2_candidate_rejects_invalid_source_step():
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "source_step must be a ProofStep"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=object(),
    )


def test_phase103_2_candidate_rejects_non_tuple_bindings():
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "bindings must be a tuple"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
      bindings=[
        data[
          "binding"
        ],
      ],
    )


def test_phase103_2_candidate_rejects_non_binding_member():
  data = build_phase103_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "bindings must contain only "
      "VariableBinding objects"
    ),
  ):
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "catalog_entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "premise_pattern"
      ],
      source_step=data[
        "source_step"
      ],
      bindings=(
        object(),
      ),
    )
