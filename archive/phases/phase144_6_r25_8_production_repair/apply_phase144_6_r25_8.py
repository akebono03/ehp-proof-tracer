from pathlib import Path

TARGET = Path("toda_upstream_bootstrap.py")

OLD = '''  membership_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == HomotopyGroupMembershipStatement(
        element=nu_prime,
        group_dimension=6,
        sphere_dimension=3,
      )
    ),
    "nu-prime membership",
  )

  eta3_definition_step = ProofStep(
'''

NEW = '''  raw_membership_step = _find_unique_step(
    raw_result.steps,
    lambda step: (
      step.conclusion
      == HomotopyGroupMembershipStatement(
        element=nu_prime,
        group_dimension=6,
        sphere_dimension=3,
      )
    ),
    "nu-prime membership",
  )

  membership_step = ProofStep(
    conclusion=raw_membership_step.conclusion,
    premises=(
      bracket_membership_step,
      *raw_membership_step.premises,
    ),
    rule=raw_membership_step.rule,
  )

  eta3_definition_step = ProofStep(
'''

text = TARGET.read_text(encoding="utf-8")
if OLD not in text:
    if NEW in text:
        print("R25-8 production repair already applied.")
    else:
        raise RuntimeError(
          "R25-8 membership-step anchor not found"
        )
else:
    TARGET.write_text(
      text.replace(OLD, NEW, 1),
      encoding="utf-8",
    )
    print("R25-8 production repair applied.")

test_target = Path(
  "tests/test_phase144_6_r25_8_depth2_definition_provenance.py"
)
test_text = r'''from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)
from toda_upstream_bootstrap import (
  build_toda_53_nu_prime_steps,
)


def _depth2_pi6_3_data():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  return (
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def test_phase144_6_r25_8_nu_prime_membership_keeps_bracket_provenance():
  membership_step, _, _ = (
    build_toda_53_nu_prime_steps()
  )

  assert isinstance(
    membership_step.conclusion,
    HomotopyGroupMembershipStatement,
  )
  assert any(
    isinstance(
      premise.conclusion,
      TodaBracketMembershipStatement,
    )
    for premise in membership_step.premises
  )


def test_phase144_6_r25_8_depth2_recovers_definition_argument():
  (
    _,
    _,
    _,
    arguments,
  ) = _depth2_pi6_3_data()

  assert (
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
    in tuple(
      argument.role
      for argument in arguments
    )
  )


def test_phase144_6_r25_8_depth2_narrative_restores_definition():
  (
    presentation,
    _,
    _,
    _,
  ) = _depth2_pi6_3_data()

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert r"$\nu'$ を定める." in rendered
  assert (
    r"\nu' \in "
    r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in rendered
  )


def test_phase144_6_r25_8_depth2_hides_internal_pi5_3_support():
  (
    presentation,
    _,
    _,
    _,
  ) = _depth2_pi6_3_data()

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    r"\pi_{5}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
    not in rendered
  )
'''
test_target.write_text(test_text,encoding="utf-8")
print(f"Wrote {test_target}")
