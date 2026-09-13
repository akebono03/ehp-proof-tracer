from functools import lru_cache

from expression import (
  HomotopyElement,
  Multiple,
  TodaBracket,
)
from homotopy_groups import (
  HomotopyGroup,
)
from proof import (
  ProofRule,
  apply_inference_match,
  find_inference_match,
)
from test_phase55_prop51_integration import (
  build_phase55_5_integration,
)
from test_phase70_pi11_6_delta_iota13 import (
  build_phase70_8_data,
)
from test_phase72r5_ordinary_ehp_211_exactness import (
  build_phase72r5_pi10_s5_data,
)
from test_phase72r6_ordinary_primary_bridge import (
  build_phase72r6_data,
)
from test_phase72r7_primary_composition_indeterminacy import (
  build_phase72r7_data,
)
from toda_rules import (
  TodaLemma510BracketModuloStatement,
  TodaLemma510HopfBracketContainsStatement,
  TodaLemma510IndexedHopfBracketContainsStatement,
  TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  TodaLemma510Split115Statement,
  toda_lemma510_corrected_exactness_core_inference_rule,
  toda_lemma510_corrected_modulo_integration_inference_rule,
  toda_lemma510_eta8_two_iota9_zero_inference_rule,
  toda_lemma510_hopf_from_split_inference_rule,
  toda_lemma510_prop26_indexed_hopf_inference_rule,
  toda_lemma510_split_115_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase72r8_data():
  phase55 = (
    build_phase55_5_integration()
  )

  phase70 = (
    build_phase70_8_data()
  )

  phase72r5 = (
    build_phase72r5_pi10_s5_data()
  )

  phase72r6 = (
    build_phase72r6_data()
  )

  phase72r7 = (
    build_phase72r7_data()
  )

  prop51_step = (
    phase55[
      "integration_steps"
    ][
      0
    ]
  )

  delta_iota11_step = (
    phase70[
      "phase70_7"
    ][
      "delta_iota11_step"
    ]
  )

  hopf_delta_step = (
    phase70[
      "hopf_value_step"
    ]
  )

  nu6_eta9_zero_step = (
    phase72r7[
      "nu6_eta9_zero_step"
    ]
  )

  eta8_zero_rule = (
    toda_lemma510_eta8_two_iota9_zero_inference_rule()
  )

  eta8_zero_match = find_inference_match(
    eta8_zero_rule,
    (
      prop51_step,
    ),
  )

  assert (
    eta8_zero_match
    is not None
  )

  eta8_zero_step = (
    apply_inference_match(
      eta8_zero_match
    )
  )

  prop26_rule = (
    toda_lemma510_prop26_indexed_hopf_inference_rule()
  )

  prop26_match = find_inference_match(
    prop26_rule,
    (
      nu6_eta9_zero_step,
      eta8_zero_step,
      delta_iota11_step,
    ),
  )

  assert (
    prop26_match
    is not None
  )

  indexed_hopf_step = (
    apply_inference_match(
      prop26_match
    )
  )

  split_rule = (
    toda_lemma510_split_115_inference_rule()
  )

  split_match = find_inference_match(
    split_rule,
    (
      indexed_hopf_step,
    ),
  )

  assert (
    split_match
    is not None
  )

  split_step = (
    apply_inference_match(
      split_match
    )
  )

  hopf_transport_rule = (
    toda_lemma510_hopf_from_split_inference_rule()
  )

  hopf_transport_match = find_inference_match(
    hopf_transport_rule,
    (
      indexed_hopf_step,
      split_step,
    ),
  )

  assert (
    hopf_transport_match
    is not None
  )

  ordinary_hopf_step = (
    apply_inference_match(
      hopf_transport_match
    )
  )

  core_rule = (
    toda_lemma510_corrected_exactness_core_inference_rule()
  )

  core_match = find_inference_match(
    core_rule,
    (
      ordinary_hopf_step,
      hopf_delta_step,
      phase72r5[
        "exactness_step"
      ],
    ),
  )

  assert (
    core_match
    is not None
  )

  core_step = (
    apply_inference_match(
      core_match
    )
  )

  integration_rule = (
    toda_lemma510_corrected_modulo_integration_inference_rule()
  )

  integration_match = find_inference_match(
    integration_rule,
    (
      core_step,
      phase72r7[
        "final_step"
      ],
      phase72r6[
        "final_step"
      ],
    ),
  )

  assert (
    integration_match
    is not None
  )

  final_step = (
    apply_inference_match(
      integration_match
    )
  )

  return {
    "phase55": phase55,
    "phase70": phase70,
    "phase72r5": phase72r5,
    "phase72r6": phase72r6,
    "phase72r7": phase72r7,
    "prop51_step": prop51_step,
    "delta_iota11_step": (
      delta_iota11_step
    ),
    "hopf_delta_step": (
      hopf_delta_step
    ),
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
    "eta8_zero_rule": (
      eta8_zero_rule
    ),
    "eta8_zero_step": (
      eta8_zero_step
    ),
    "prop26_rule": prop26_rule,
    "indexed_hopf_step": (
      indexed_hopf_step
    ),
    "split_rule": split_rule,
    "split_step": split_step,
    "hopf_transport_rule": (
      hopf_transport_rule
    ),
    "ordinary_hopf_step": (
      ordinary_hopf_step
    ),
    "core_rule": core_rule,
    "core_step": core_step,
    "integration_rule": (
      integration_rule
    ),
    "final_step": final_step,
  }


def test_phase72r8_eta8_two_iota9_zero_is_inference():
  data = build_phase72r8_data()

  assert (
    data[
      "eta8_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r8_prop26_produces_indexed_bracket():
  data = build_phase72r8_data()

  statement = (
    data[
      "indexed_hopf_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaLemma510IndexedHopfBracketContainsStatement,
  )

  assert (
    statement.bracket.index
    == 1
  )


def test_phase72r8_prop26_is_inference():
  data = build_phase72r8_data()

  assert (
    data[
      "indexed_hopf_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r8_prop26_uses_exact_three_dependencies():
  data = build_phase72r8_data()

  assert (
    data[
      "indexed_hopf_step"
    ].premises
    == (
      data[
        "nu6_eta9_zero_step"
      ],
      data[
        "eta8_zero_step"
      ],
      data[
        "delta_iota11_step"
      ],
    )
  )


def test_phase72r8_split_115_is_inference():
  data = build_phase72r8_data()

  assert isinstance(
    data[
      "split_step"
    ].conclusion,
    TodaLemma510Split115Statement,
  )

  assert (
    data[
      "split_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72r8_split_115_removes_index():
  data = build_phase72r8_data()

  split = (
    data[
      "split_step"
    ].conclusion
  )

  assert (
    split.indexed_bracket.index
    == 1
  )

  assert (
    split.ordinary_bracket.index
    is None
  )


def test_phase72r8_ordinary_hopf_is_derived_through_split():
  data = build_phase72r8_data()

  step = (
    data[
      "ordinary_hopf_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510HopfBracketContainsStatement,
  )

  assert (
    step.conclusion.bracket.index
    is None
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72r8_core_uses_ordinary_exactness():
  data = build_phase72r8_data()

  assert (
    data[
      "core_step"
    ].premises[
      2
    ]
    is data[
      "phase72r5"
    ][
      "exactness_step"
    ]
  )


def test_phase72r8_core_is_ordinary():
  data = build_phase72r8_data()

  statement = (
    data[
      "core_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  )

  assert (
    statement.source_group
    == HomotopyGroup(
      group_dimension=10,
      sphere_dimension=5,
    )
  )

  assert (
    statement.target_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase72r8_final_uses_corrected_three_branches():
  data = build_phase72r8_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "core_step"
      ],
      data[
        "phase72r7"
      ][
        "final_step"
      ],
      data[
        "phase72r6"
      ][
        "final_step"
      ],
    )
  )


def test_phase72r8_final_is_inference_not_given():
  data = build_phase72r8_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72r8_final_ambient_group_is_ordinary():
  data = build_phase72r8_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert isinstance(
    statement,
    TodaLemma510BracketModuloStatement,
  )

  assert (
    statement.ambient_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )

  assert (
    statement.modulus
    == 2
  )


def test_phase72r8_final_bracket_is_unindexed():
  data = build_phase72r8_data()

  bracket = (
    data[
      "final_step"
    ].conclusion
    .bracket
  )

  assert isinstance(
    bracket,
    TodaBracket,
  )

  assert (
    bracket.index
    is None
  )


def test_phase72r8_final_value_is_delta_iota13():
  data = build_phase72r8_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .element
    is data[
      "hopf_delta_step"
    ].conclusion
    .argument
  )


def test_phase72r8_indexed_and_ordinary_brackets_are_distinct():
  data = build_phase72r8_data()

  assert (
    data[
      "indexed_hopf_step"
    ].conclusion
    .bracket
    != data[
      "ordinary_hopf_step"
    ].conclusion
    .bracket
  )


