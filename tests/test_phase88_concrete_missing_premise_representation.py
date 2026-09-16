from dataclasses import dataclass
from functools import lru_cache

from proof import (
  InferenceRule,
  PatternVariable,
  PremisePattern,
  ProofRule,
  ProofStep,
  VariableBinding,
)
from repository_inference import (
  MissingPremiseProducerLookup,
  PremiseAvailability,
  detect_missing_premises,
  find_missing_premise_producer_lookups,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase88KnownStatement:
  value: object


@dataclass(frozen=True)
class Phase88MissingStatement:
  value: object


@lru_cache(maxsize=1)
def build_phase88_10_data():
  variable = PatternVariable(
    name="phase88.value",
  )

  known_pattern = PremisePattern(
    statement_type=Phase88KnownStatement,
    statement_pattern=(
      Phase88KnownStatement(
        value=variable,
      )
    ),
  )

  missing_pattern = PremisePattern(
    statement_type=Phase88MissingStatement,
    statement_pattern=(
      Phase88MissingStatement(
        value=variable,
      )
    ),
  )

  final_rule = InferenceRule(
    name=(
      "phase88 concrete missing premise "
      "requesting rule"
    ),
    premise_patterns=(
      known_pattern,
      missing_pattern,
    ),
  )

  known_step = ProofStep(
    conclusion=Phase88KnownStatement(
      value="iota17",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  producer_rule = InferenceRule(
    name=(
      "phase88 concrete missing premise "
      "producer rule"
    ),
  )

  catalog = InferenceRuleCatalog()
  catalog.register(
    InferenceRuleCatalogEntry(
      key=(
        "phase88.concrete-missing."
        "producer"
      ),
      rule=producer_rule,
      conclusion_type=(
        Phase88MissingStatement
      ),
      fixed_point_safe=True,
    )
  )

  availability = detect_missing_premises(
    final_rule,
    (
      known_step,
    ),
  )

  lookups = (
    find_missing_premise_producer_lookups(
      availability,
      catalog,
    )
  )

  return {
    "variable": variable,
    "known_pattern": known_pattern,
    "missing_pattern": missing_pattern,
    "final_rule": final_rule,
    "known_step": known_step,
    "producer_rule": producer_rule,
    "catalog": catalog,
    "availability": availability,
    "lookups": lookups,
  }


def test_phase88_10_availability_preserves_selected_bindings():
  data = build_phase88_10_data()

  assert data[
    "availability"
  ].matched_steps == (
    data[
      "known_step"
    ],
    None,
  )

  assert data[
    "availability"
  ].missing_indices == (
    1,
  )

  assert data[
    "availability"
  ].bindings == (
    VariableBinding(
      variable=data[
        "variable"
      ],
      value="iota17",
    ),
  )


def test_phase88_10_lookup_preserves_concrete_requested_statement():
  data = build_phase88_10_data()

  assert len(
    data[
      "lookups"
    ]
  ) == 1

  lookup = data[
    "lookups"
  ][0]

  assert (
    lookup.requested_statement
    == Phase88MissingStatement(
      value="iota17",
    )
  )


def test_phase88_10_lookup_preserves_existing_producer_semantics():
  data = build_phase88_10_data()

  lookup = data[
    "lookups"
  ][0]

  assert (
    lookup.inference_rule
    is data[
      "final_rule"
    ]
  )

  assert (
    lookup.premise_index
    == 1
  )

  assert (
    lookup.premise_pattern
    is data[
      "missing_pattern"
    ]
  )

  assert (
    lookup.producer_rules
    == (
      data[
        "producer_rule"
      ],
    )
  )


def test_phase88_10_unbound_variable_does_not_create_false_concrete_statement():
  variable = PatternVariable(
    name="phase88.unbound",
  )

  missing_pattern = PremisePattern(
    statement_type=Phase88MissingStatement,
    statement_pattern=(
      Phase88MissingStatement(
        value=variable,
      )
    ),
  )

  rule = InferenceRule(
    name="phase88 unbound rule",
    premise_patterns=(
      missing_pattern,
    ),
  )

  availability = detect_missing_premises(
    rule,
    (),
  )

  lookups = (
    find_missing_premise_producer_lookups(
      availability,
      InferenceRuleCatalog(),
    )
  )

  assert availability.bindings == ()

  assert len(
    lookups
  ) == 1

  assert (
    lookups[
      0
    ].requested_statement
    is None
  )


def test_phase88_10_concrete_pattern_needs_no_binding():
  concrete_pattern = PremisePattern(
    statement_type=Phase88MissingStatement,
    statement_pattern=(
      Phase88MissingStatement(
        value="fixed",
      )
    ),
  )

  rule = InferenceRule(
    name="phase88 concrete pattern rule",
    premise_patterns=(
      concrete_pattern,
    ),
  )

  availability = detect_missing_premises(
    rule,
    (),
  )

  lookups = (
    find_missing_premise_producer_lookups(
      availability,
      InferenceRuleCatalog(),
    )
  )

  assert (
    lookups[
      0
    ].requested_statement
    == Phase88MissingStatement(
      value="fixed",
    )
  )


def test_phase88_10_type_only_pattern_has_no_requested_statement():
  type_only_pattern = PremisePattern(
    statement_type=Phase88MissingStatement,
  )

  rule = InferenceRule(
    name="phase88 type-only pattern rule",
    premise_patterns=(
      type_only_pattern,
    ),
  )

  availability = detect_missing_premises(
    rule,
    (),
  )

  lookups = (
    find_missing_premise_producer_lookups(
      availability,
      InferenceRuleCatalog(),
    )
  )

  assert (
    lookups[
      0
    ].requested_statement
    is None
  )


def test_phase88_10_new_fields_preserve_backward_compatible_defaults():
  rule = InferenceRule(
    name="phase88 compatibility rule",
  )

  availability = PremiseAvailability(
    inference_rule=rule,
    matched_steps=(),
    missing_indices=(),
  )

  lookup = MissingPremiseProducerLookup(
    inference_rule=rule,
    premise_index=0,
    premise_pattern=PremisePattern(),
    producer_rules=(),
  )

  assert availability.bindings == ()

  assert (
    lookup.requested_statement
    is None
  )
