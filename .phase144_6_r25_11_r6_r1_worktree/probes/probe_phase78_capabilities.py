import sys
from pathlib import Path

from proof import ProofRule


TESTS_DIR = (
  Path(__file__)
  .resolve()
  .parents[1]
  / "tests"
)

if str(TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(TESTS_DIR),
  )

from test_phase78_stable_g0_to_g7_integration import (
  build_phase78_11_data,
)


def build_phase78_representative_result():
  data = build_phase78_11_data()

  aggregate_step = (
    data[
      "aggregate_step"
    ]
  )

  ancestors = (
    data[
      "ancestors"
    ]
  )

  return {
    "data": data,
    "aggregate_step": (
      aggregate_step
    ),
    "statement": (
      aggregate_step
      .conclusion
    ),
    "aggregate_derived": (
      aggregate_step.rule
      == ProofRule.INFERENCE
    ),
    "aggregate_is_given": (
      aggregate_step.rule
      == ProofRule.GIVEN
    ),
    "all_direct_branches_inference": all(
      step.rule
      == ProofRule.INFERENCE
      for step
      in data[
        "premise_steps"
      ]
    ),
    "g0_reachable": any(
      ancestor
      is data[
        "g0_step"
      ]
      for ancestor
      in ancestors
    ),
    "g1_reachable": any(
      ancestor
      is data[
        "g1_step"
      ]
      for ancestor
      in ancestors
    ),
    "g2_reachable": any(
      ancestor
      is data[
        "g2_step"
      ]
      for ancestor
      in ancestors
    ),
    "g3_reachable": any(
      ancestor
      is data[
        "g3_step"
      ]
      for ancestor
      in ancestors
    ),
    "g4_reachable": any(
      ancestor
      is data[
        "g4_step"
      ]
      for ancestor
      in ancestors
    ),
    "g5_reachable": any(
      ancestor
      is data[
        "g5_step"
      ]
      for ancestor
      in ancestors
    ),
    "g6_reachable": any(
      ancestor
      is data[
        "g6_step"
      ]
      for ancestor
      in ancestors
    ),
    "g7_reachable": any(
      ancestor
      is data[
        "g7_step"
      ]
      for ancestor
      in ancestors
    ),
    "final_is_self_ancestor": any(
      ancestor
      is aggregate_step
      for ancestor
      in ancestors
    ),
    "final_conclusion_in_ancestors": any(
      ancestor.conclusion
      == aggregate_step.conclusion
      for ancestor
      in ancestors
    ),
  }


def _heading(
  title,
):
  print()
  print(
    "=" * 72
  )
  print(
    title
  )
  print(
    "=" * 72
  )
  print()


def main():
  result = (
    build_phase78_representative_result()
  )

  print(
    "EHP Proof Tracer"
  )
  print(
    "Phase 78 stable G_0 through G_7 "
    "capability demonstration"
  )

  _heading(
    "Stable G_0 through G_7 result"
  )

  print(
    "G_0 = Z{iota}"
  )
  print()
  print(
    "(G_1;2) = Z/2{eta}"
  )
  print(
    "(G_2;2) = Z/2{eta^2}"
  )
  print(
    "(G_3;2) = Z/8{nu}"
  )
  print(
    "(G_4;2) = 0"
  )
  print(
    "(G_5;2) = 0"
  )
  print(
    "(G_6;2) = Z/2{nu^2}"
  )
  print(
    "(G_7;2) = Z/16{sigma}"
  )
  print()

  print(
    "statement type = "
    f"{type(result['statement']).__name__}"
  )
  print(
    "aggregate derived = "
    f"{result['aggregate_derived']}"
  )
  print(
    "aggregate is GIVEN = "
    f"{result['aggregate_is_given']}"
  )

  _heading(
    "Proof-style derivation"
  )

  print(
    "[0] Ordinary zero-stem branch"
  )
  print()
  print(
    "pi_3^3=Z{iota_3}"
  )
  print(
    "-> ordinary pi_3(S^3)=Z{iota_3}"
  )
  print(
    "-> pi_3(S^3) isomorphic to G_0"
  )
  print(
    "-> iota_3 stabilizes to iota"
  )
  print(
    "-> G_0=Z{iota}"
  )
  print()

  print(
    "[1] One-stem"
  )
  print(
    "pi_4^3=Z/2{eta_3}"
  )
  print(
    "-> (G_1;2)=Z/2{eta}"
  )
  print()

  print(
    "[2] Two-stem"
  )
  print(
    "pi_6^4=Z/2{eta_4^2}"
  )
  print(
    "eta_4^2 -> eta^2"
  )
  print(
    "-> (G_2;2)=Z/2{eta^2}"
  )
  print()

  print(
    "[3] Three-stem"
  )
  print(
    "pi_8^5=Z/8{nu_5}"
  )
  print(
    "-> (G_3;2)=Z/8{nu}"
  )
  print()

  print(
    "[4] Four-stem"
  )
  print(
    "pi_10^6=0"
  )
  print(
    "-> (G_4;2)=0"
  )
  print()

  print(
    "[5] Five-stem"
  )
  print(
    "pi_12^7=0"
  )
  print(
    "-> (G_5;2)=0"
  )
  print()

  print(
    "[6] Six-stem"
  )
  print(
    "pi_14^8=Z/2{nu_8^2}"
  )
  print(
    "nu_8^2 -> nu^2"
  )
  print(
    "-> (G_6;2)=Z/2{nu^2}"
  )
  print()

  print(
    "[7] Seven-stem"
  )
  print(
    "pi_16^9=Z/16{sigma_9}"
  )
  print(
    "-> (G_7;2)=Z/16{sigma}"
  )

  _heading(
    "Provenance / integration"
  )

  print(
    "all eight direct branches are INFERENCE = "
    f"{result['all_direct_branches_inference']}"
  )
  print(
    "G_0 branch reachable = "
    f"{result['g0_reachable']}"
  )
  print(
    "G_1 branch reachable = "
    f"{result['g1_reachable']}"
  )
  print(
    "G_2 branch reachable = "
    f"{result['g2_reachable']}"
  )
  print(
    "G_3 branch reachable = "
    f"{result['g3_reachable']}"
  )
  print(
    "G_4 branch reachable = "
    f"{result['g4_reachable']}"
  )
  print(
    "G_5 branch reachable = "
    f"{result['g5_reachable']}"
  )
  print(
    "G_6 branch reachable = "
    f"{result['g6_reachable']}"
  )
  print(
    "G_7 branch reachable = "
    f"{result['g7_reachable']}"
  )
  print(
    "aggregate derived = "
    f"{result['aggregate_derived']}"
  )
  print(
    "aggregate is GIVEN = "
    f"{result['aggregate_is_given']}"
  )

  _heading(
    "Representation boundary"
  )

  print(
    "G_0 is ordinary StableHomotopyGroup(stem=0)."
  )
  print(
    "G_0 is not represented as a "
    "StablePrimaryComponent."
  )
  print()
  print(
    "G_1 through G_7 are represented as "
    "2-primary stable components."
  )
  print()
  print(
    "eta^2 and nu^2 remain Composition "
    "expressions."
  )
  print(
    "No stable composition type checker "
    "was introduced."
  )
  print()
  print(
    "G_4 and G_5 retain theorem-specific "
    "stable-zero statements."
  )

  _heading(
    "Applicability / non-circularity"
  )

  print(
    "final is self-ancestor = "
    f"{result['final_is_self_ancestor']}"
  )
  print(
    "final conclusion appears in ancestors = "
    f"{result['final_conclusion_in_ancestors']}"
  )

  _heading(
    "Phase 78 representative probe boundary"
  )

  print(
    "Displayed:"
  )
  print(
    "  G_0 ordinary stable group"
  )
  print(
    "  G_1 through G_7 2-primary stable groups"
  )
  print(
    "  finite anchor -> stable result chains"
  )
  print(
    "  aggregate provenance"
  )
  print(
    "  representation boundary"
  )
  print(
    "  non-circularity"
  )
  print()

  print(
    "Not added in Phase 78-11:"
  )
  print(
    "  new mathematical stable-group results"
  )
  print(
    "  generic E-infinity map object"
  )
  print(
    "  generic stable-group database"
  )
  print(
    "  generic stable cyclic transport"
  )
  print(
    "  generic stable zero transport"
  )
  print(
    "  generic stable composition typing"
  )
  print(
    "  automatic proof narrative generation"
  )
  print(
    "  persistent Proof Repository"
  )
  print()

  print(
    "The proof-style derivation above is "
    "hand-authored presentation code."
  )
  print(
    "It is not generated automatically "
    "from the ProofStep graph."
  )


if __name__ == "__main__":
  main()


