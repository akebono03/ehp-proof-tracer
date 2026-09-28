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

from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)


def _proof_graph_is_acyclic(step):
  visiting = set()
  visited = set()

  def visit(current):
    current_id = id(current)

    if current_id in visiting:
      return False

    if current_id in visited:
      return True

    visiting.add(current_id)

    for premise in current.premises:
      if not visit(premise):
        return False

    visiting.remove(current_id)
    visited.add(current_id)
    return True

  return visit(step)


def build_phase77_representative_result():
  data = build_phase77_6_data()

  final_step = data["final_step"]
  final_statement = final_step.conclusion
  ancestors = data["ancestors"]

  phase76_specific_rule_reachable = any(
    ancestor.inference_rule is not None
    and ancestor.inference_rule.name.startswith("Toda (5.16)")
    for ancestor in ancestors
  )

  return {
    "data": data,
    "final_step": final_step,
    "final_statement": final_statement,
    "final_derived": final_step.rule == ProofRule.INFERENCE,
    "final_is_given": final_step.rule == ProofRule.GIVEN,
    "typed_setup_is_given": (
      data["typed_setup_step"].rule == ProofRule.GIVEN
    ),
    "phase75_theorem36_bridge_reachable": any(
      ancestor is data["phase75_theorem36_bridge_step"]
      for ancestor in ancestors
    ),
    "phase75_sigma8_reachable": any(
      ancestor is data["phase75_sigma8_step"]
      for ancestor in ancestors
    ),
    "first_branch_reachable": any(
      ancestor is data["first_term_step"]
      for ancestor in ancestors
    ),
    "second_branch_reachable": any(
      ancestor is data["second_term_step"]
      for ancestor in ancestors
    ),
    "theorem36_sum_reachable": any(
      ancestor is data["bracket_sum_step"]
      for ancestor in ancestors
    ),
    "sigma_bridge_reachable": any(
      ancestor is data["suspension_bridge_step"]
      for ancestor in ancestors
    ),
    "sigma_definition_reachable": any(
      ancestor is data["sigma_definition_step"]
      for ancestor in ancestors
    ),
    "scaled_composition_reachable": any(
      ancestor is data["composition_step"]
      for ancestor in ancestors
    ),
    "same_odd_parameter": (
      final_statement.odd_parameter
      is data["phase75_sigma8_step"].conclusion.odd_parameter
    ),
    "first_bracket_uses_e7_beta": (
      final_statement.first_bracket.second.exponent == 7
    ),
    "phase76_specific_rule_reachable": phase76_specific_rule_reachable,
    "final_is_self_ancestor": any(
      ancestor is final_step
      for ancestor in ancestors
    ),
    "final_conclusion_in_ancestors": any(
      ancestor.conclusion == final_statement
      for ancestor in ancestors
    ),
    "proof_graph_acyclic": _proof_graph_is_acyclic(final_step),
  }


def _heading(title):
  print()
  print("=" * 72)
  print(title)
  print("=" * 72)
  print()


def main():
  result = build_phase77_representative_result()
  final_statement = result["final_statement"]

  print("EHP Proof Tracer")
  print("Phase 77 capability demonstration")

  _heading("Toda Lemma 5.16 result")

  print("Assume t>0,")
  print("beta in pi_(t+4)(S^m),")
  print("beta composed with nu_(t+4) = 0.")
  print()
  print("Then for the same odd x inherited from the Phase 75 sigma_8 construction,")
  print()
  print("E^4 beta composed with sigma_(t+8)")
  print("is contained in")
  print("(-1)^m x {nu_(m+4), E^7 beta, nu_(t+11)}_7")
  print("+")
  print("(-1)^t x {E^4 beta, nu_(t+8), 2 nu_(t+11)}_(t+3).")
  print()
  print(f"statement type = {type(final_statement).__name__}")
  print(f"derived = {result['final_derived']}")
  print(f"is GIVEN = {result['final_is_given']}")

  _heading("Proof-style derivation")

  print("[1] Typed hypotheses")
  print()
  print("t>0")
  print("beta in pi_(t+4)(S^m)")
  print("beta composed with nu_(t+4)=0")
  print()
  print("The first Toda bracket is typed with E^7 beta:")
  print("{nu_(m+4), E^7 beta, nu_(t+11)}_7.")
  print()
  print("[2] Theorem 3.6 specialization")
  print()
  print("Phase 75 provides alpha-star in pi_15(S^8).")
  print("Theorem 3.6 gives")
  print()
  print("E^4 beta composed with E^t alpha-star")
  print("in")
  print("(-1)^m {nu_(m+4), E^7 beta, nu_(t+11)}_7")
  print("+")
  print("(-1)^t {E^4 beta, nu_(t+8), 2 nu_(t+11)}_(t+3).")
  print()
  print("[3] Phase 75 sigma_8 relation")
  print()
  print("For the same odd x used in the sigma_8 construction:")
  print("E sigma_8 = x E alpha-star.")
  print()
  print("Since t>0:")
  print("E^t sigma_8 = x E^t alpha-star.")
  print()
  print("Also sigma_(t+8)=E^t sigma_8.")
  print()
  print("[4] Left composition by E^4 beta")
  print()
  print("E^4 beta composed with sigma_(t+8)")
  print("=")
  print("x (E^4 beta composed with E^t alpha-star).")
  print()
  print("[5] Toda Lemma 5.16")
  print()
  print("E^4 beta composed with sigma_(t+8)")
  print("in")
  print("(-1)^m x {nu_(m+4), E^7 beta, nu_(t+11)}_7")
  print("+")
  print("(-1)^t x {E^4 beta, nu_(t+8), 2 nu_(t+11)}_(t+3).")

  _heading("Provenance / integration")

  print(f"typed setup remains GIVEN = {result['typed_setup_is_given']}")
  print(
    "Phase 75 Theorem 3.6 bridge reachable = "
    f"{result['phase75_theorem36_bridge_reachable']}"
  )
  print(
    "Phase 75 sigma_8 statement reachable = "
    f"{result['phase75_sigma8_reachable']}"
  )
  print(f"first bracket branch reachable = {result['first_branch_reachable']}")
  print(f"second bracket branch reachable = {result['second_branch_reachable']}")
  print(f"Theorem 3.6 bracket-sum reachable = {result['theorem36_sum_reachable']}")
  print(f"E^t sigma_8 bridge reachable = {result['sigma_bridge_reachable']}")
  print(f"sigma_(t+8) definition reachable = {result['sigma_definition_reachable']}")
  print(f"scaled composition reachable = {result['scaled_composition_reachable']}")
  print(f"same odd x preserved = {result['same_odd_parameter']}")
  print(f"final Lemma 5.16 derived = {result['final_derived']}")
  print(f"final Lemma 5.16 is GIVEN = {result['final_is_given']}")

  _heading("Applicability / non-circularity")

  print(f"first bracket uses E^7 beta = {result['first_bracket_uses_e7_beta']}")
  print(
    "Phase 76 Toda (5.16) rule reachable = "
    f"{result['phase76_specific_rule_reachable']}"
  )
  print(f"final is self-ancestor = {result['final_is_self_ancestor']}")
  print(
    "final conclusion appears in ancestors = "
    f"{result['final_conclusion_in_ancestors']}"
  )
  print(f"proof graph acyclic = {result['proof_graph_acyclic']}")

  _heading("Literature / source")

  print("[Toda Lemma 5.16]")
  print("Locator: Lemma 5.16")
  print("Author: H. Toda")
  print("Source: Composition Methods in Homotopy Groups of Spheres")
  print("Year: 1962")
  print()
  print("Source note:")
  print("The printed lemma contains E^n beta in the first bracket,")
  print("but n is unbound there. The immediately following proof text")
  print("uses E^7 beta, and Toda-bracket typing also forces exponent 7.")
  print("The canonical machine representation therefore uses E^7 beta.")

  _heading("Phase 77 representative probe boundary")

  print("Displayed:")
  print("  typed Lemma 5.16 hypotheses")
  print("  corrected first bracket with E^7 beta")
  print("  first / second Theorem 3.6 bracket branches")
  print("  Theorem 3.6 bracket-sum containment")
  print("  same odd x from the Phase 75 sigma_8 construction")
  print("  E^t sigma_8 = x E^t alpha-star")
  print("  sigma_(t+8)=E^t sigma_8")
  print("  scaled composition bridge")
  print("  final Lemma 5.16 bracket-sum consequence")
  print("  provenance / non-circularity")
  print()
  print("Not added in Phase 77-7:")
  print("  new mathematical inference rules")
  print("  generic Toda-bracket sum algebra")
  print("  generic odd existential solver")
  print("  generic sign / coefficient solver")
  print("  generic symbolic suspension induction")
  print("  automatic proof narrative generation")
  print("  persistent Proof Repository")
  print()
  print("The proof-style derivation above is hand-authored presentation code.")
  print("It is not generated automatically from the ProofStep graph.")
  print()
  print("Next mathematical boundary:")
  print("  deferred stable clause (G_7;2)=Z/16{sigma}")


if __name__ == "__main__":
  main()
