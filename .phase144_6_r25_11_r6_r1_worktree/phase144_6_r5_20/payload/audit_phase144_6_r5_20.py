from dataclasses import dataclass
from enum import Enum

from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)
from toda_group_proof_narrative_renderer import (
  _render_phase134_3_pi6_3_narrative_markdown,
)


class ParityKind(Enum):
  MATHEMATICAL_FACT = "mathematical_fact"
  ORDERING = "ordering"
  DISCOURSE = "discourse"
  STRUCTURE = "structure"


class ParityStatus(Enum):
  PRESENT = "present"
  MISSING = "missing"


@dataclass(frozen=True)
class ParityRequirement:
  key: str
  kind: ParityKind
  dedicated_needles: tuple[str, ...]
  generic_alternatives: tuple[tuple[str, ...], ...]
  description: str


@dataclass(frozen=True)
class ParityResult:
  requirement: ParityRequirement
  status: ParityStatus
  matched_alternative_index: int | None


def parity_requirements():
  return (
    ParityRequirement(
      key="eta3_zero_precondition",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"2\eta_{3}=0",),
      generic_alternatives=((r"2\eta_{3} = 0",), (r"2\eta_{3}=0",)),
      description="Lemma 5.2 application precondition 2 eta_3 = 0.",
    ),
    ParityRequirement(
      key="nu_prime_bracket_definition",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}",
      ),
      generic_alternatives=(
        (r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}",),
        (r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}",),
      ),
      description="Definition of nu-prime by the Toda bracket.",
    ),
    ParityRequirement(
      key="nu_prime_membership",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"\nu'\in\pi_{6}^{3}",),
      generic_alternatives=(
        (r"\nu' \in \pi_{6}^{3}",),
        (r"\nu'\in\pi_{6}^{3}",),
      ),
      description="Membership nu-prime in pi_6^3.",
    ),
    ParityRequirement(
      key="hopf_nu_prime",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"H(\nu')=\eta_{5}",),
      generic_alternatives=(
        (r"H(\nu') = \eta_{5}",),
        (r"H(\nu')=\eta_{5}",),
      ),
      description="Hopf image H(nu-prime)=eta_5.",
    ),
    ParityRequirement(
      key="double_nu_prime",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"2\nu'", r"\eta_{3}^{3}"),
      generic_alternatives=(
        (r"2\nu'", r"\eta_{3}^{3}"),
        (r"2\nu'", r"\eta_{3}\eta_{4}\eta_{5}"),
      ),
      description="The relation 2 nu-prime = eta_3^3.",
    ),
    ParityRequirement(
      key="pi5_3_group",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\pi_{5}^{3}",
        r"\mathbb{Z}/2\{\eta_{3}^{2}\}",
      ),
      generic_alternatives=(
        (r"\pi_{5}^{3}", r"\mathbb{Z}/2\{\eta_{3}^{2}\}"),
        (r"\pi_{5}^{3}", r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"),
      ),
      description="pi_5^3 group used in the order argument.",
    ),
    ParityRequirement(
      key="pi5_2_group",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\pi_{5}^{2}",
        r"\mathbb{Z}/2\{\eta_{2}^{3}\}",
      ),
      generic_alternatives=(
        (r"\pi_{5}^{2}", r"\mathbb{Z}/2\{\eta_{2}^{3}\}"),
        (r"\pi_{5}^{2}", r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}"),
      ),
      description="pi_5^2 group used at the left side of the short exact sequence.",
    ),
    ParityRequirement(
      key="ehp_exactness_window",
      kind=ParityKind.STRUCTURE,
      dedicated_needles=(
        r"\pi_{7}^{3}",
        r"\pi_{7}^{5}",
        r"\pi_{5}^{2}",
        r"\pi_{6}^{3}",
        r"\pi_{6}^{5}",
      ),
      generic_alternatives=(
        (
          r"\pi_{7}^{3}",
          r"\pi_{7}^{5}",
          r"\pi_{5}^{2}",
          r"\pi_{6}^{3}",
          r"\pi_{6}^{5}",
        ),
      ),
      description="EHP exactness window used to determine the order.",
    ),
    ParityRequirement(
      key="nu_eta6_membership",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"\nu'\eta_{6}\in\pi_{7}^{3}",),
      generic_alternatives=(
        (r"\nu'\eta_{6} \in \pi_{7}^{3}",),
        (r"\nu'\eta_{6}\in\pi_{7}^{3}",),
      ),
      description="Membership of nu-prime eta_6 in pi_7^3.",
    ),
    ParityRequirement(
      key="hopf_nu_eta6",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"H(\nu'\eta_{6})", r"\eta_{5}^{2}"),
      generic_alternatives=(
        (r"H(\nu'\eta_{6})", r"\eta_{5}^{2}"),
        (r"H(\nu'\eta_{6})", r"\eta_{5}\eta_{6}"),
      ),
      description="Hopf calculation showing the generator eta_5^2 is hit.",
    ),
    ParityRequirement(
      key="pi7_5_group",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\pi_{7}^{5}",
        r"\mathbb{Z}/2\{\eta_{5}^{2}\}",
      ),
      generic_alternatives=(
        (r"\pi_{7}^{5}", r"\mathbb{Z}/2\{\eta_{5}^{2}\}"),
        (r"\pi_{7}^{5}", r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}"),
      ),
      description="pi_7^5 is cyclic of order two on eta_5^2.",
    ),
    ParityRequirement(
      key="hopf_pi7_surjective",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"H:\pi_{7}^{3}\to\pi_{7}^{5}",
        r"\text{は全射である",
      ),
      generic_alternatives=(
        (r"H: \pi_{7}^{3}", r"\pi_{7}^{5}", "全射"),
        (r"H:\pi_{7}^{3}", r"\pi_{7}^{5}", "全射"),
      ),
      description="Surjectivity of H: pi_7^3 -> pi_7^5.",
    ),
    ParityRequirement(
      key="delta_zero",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\Delta:\pi_{7}^{5}\to\pi_{5}^{2}",
        r"\text{は零写像である",
      ),
      generic_alternatives=(
        (r"\Delta: \pi_{7}^{5}", r"\pi_{5}^{2}", "零写像"),
        (r"\Delta:\pi_{7}^{5}", r"\pi_{5}^{2}", "零写像"),
      ),
      description="Delta is zero by exactness and Hopf surjectivity.",
    ),
    ParityRequirement(
      key="suspension_injective",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"E:\pi_{5}^{2}\to\pi_{6}^{3}",
        r"\text{は単射である",
      ),
      generic_alternatives=(
        (r"E: \pi_{5}^{2}", r"\pi_{6}^{3}", "単射"),
        (r"E:\pi_{5}^{2}", r"\pi_{6}^{3}", "単射"),
      ),
      description="Injectivity of E: pi_5^2 -> pi_6^3.",
    ),
    ParityRequirement(
      key="eta3_cube_order_two",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"\eta_{3}^{3}", r"\text{ の位数は }2"),
      generic_alternatives=(
        (r"\eta_{3}^{3}", "位数", "2"),
        (r"\eta_{3}\eta_{4}\eta_{5}", "位数", "2"),
      ),
      description="eta_3^3 has order two.",
    ),
    ParityRequirement(
      key="nu_prime_order_four",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(r"\nu'", r"\text{ の位数は }4"),
      generic_alternatives=(
        (r"\nu'", "位数", "4"),
      ),
      description="nu-prime has order four.",
    ),
    ParityRequirement(
      key="pi6_5_group",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\pi_{6}^{5}",
        r"\mathbb{Z}/2\{\eta_{5}\}",
      ),
      generic_alternatives=(
        (r"\pi_{6}^{5}", r"\mathbb{Z}/2\{\eta_{5}\}"),
      ),
      description="pi_6^5 group at the right side of the short exact sequence.",
    ),
    ParityRequirement(
      key="hopf_pi6_surjective",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"H:\pi_{6}^{3}\to\pi_{6}^{5}",
        r"\text{は全射である",
      ),
      generic_alternatives=(
        (r"H: \pi_{6}^{3}", r"\pi_{6}^{5}", "全射"),
        (r"H:\pi_{6}^{3}", r"\pi_{6}^{5}", "全射"),
      ),
      description="Surjectivity of H: pi_6^3 -> pi_6^5.",
    ),
    ParityRequirement(
      key="short_exact_sequence",
      kind=ParityKind.STRUCTURE,
      dedicated_needles=(
        r"0\longrightarrow\pi_{5}^{2}",
        r"\xrightarrow{E}\pi_{6}^{3}",
        r"\xrightarrow{H}\pi_{6}^{5}",
        r"\longrightarrow 0",
      ),
      generic_alternatives=(
        (
          r"0\longrightarrow \pi_{5}^{2}",
          r"\xrightarrow{E} \pi_{6}^{3}",
          r"\xrightarrow{H} \pi_{6}^{5}",
          r"\longrightarrow 0",
        ),
        (
          r"0\longrightarrow\pi_{5}^{2}",
          r"\xrightarrow{E}\pi_{6}^{3}",
          r"\xrightarrow{H}\pi_{6}^{5}",
          r"\longrightarrow 0",
        ),
      ),
      description="Short exact sequence determining the final group structure.",
    ),
    ParityRequirement(
      key="final_group",
      kind=ParityKind.MATHEMATICAL_FACT,
      dedicated_needles=(
        r"\pi_{6}^{3}",
        r"\mathbb{Z}/4\{\nu'\}",
      ),
      generic_alternatives=(
        (r"\pi_{6}^{3}", r"\mathbb{Z}/4\{\nu'\}"),
      ),
      description="Final group pi_6^3 = Z/4{nu-prime}.",
    ),
    ParityRequirement(
      key="precondition_before_definition",
      kind=ParityKind.ORDERING,
      dedicated_needles=(r"2\eta_{3}=0", r"\nu' \in"),
      generic_alternatives=(),
      description="The precondition appears before the nu-prime definition.",
    ),
    ParityRequirement(
      key="order_purpose_lead",
      kind=ParityKind.DISCOURSE,
      dedicated_needles=(
        r"$\nu'$ の位数を決定するために",
        "EHP 完全列",
      ),
      generic_alternatives=(
        (r"$\nu'$ の位数", "完全列"),
        (r"$\nu'$ の位数を", "完全列"),
      ),
      description="The EHP sequence is introduced as the method for determining order.",
    ),
    ParityRequirement(
      key="final_exactness_purpose",
      kind=ParityKind.DISCOURSE,
      dedicated_needles=("短完全列",),
      generic_alternatives=(
        ("短完全列",),
      ),
      description="The final group-structure argument explicitly uses the short exact sequence.",
    ),
  )


def _all_needles(text, needles):
  return all(needle in text for needle in needles)


def _ordering_precondition_before_definition(text):
  zero_positions = tuple(
    position
    for needle in (r"2\eta_{3} = 0", r"2\eta_{3}=0")
    for position in (text.find(needle),)
    if position >= 0
  )
  definition_positions = tuple(
    position
    for needle in (
      r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}",
      r"\nu'\in\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}",
    )
    for position in (text.find(needle),)
    if position >= 0
  )
  return (
    bool(zero_positions)
    and bool(definition_positions)
    and min(zero_positions) < min(definition_positions)
  )


def evaluate_requirement(requirement, generic_text):
  if requirement.key == "precondition_before_definition":
    return ParityResult(
      requirement=requirement,
      status=(
        ParityStatus.PRESENT
        if _ordering_precondition_before_definition(generic_text)
        else ParityStatus.MISSING
      ),
      matched_alternative_index=(
        0
        if _ordering_precondition_before_definition(generic_text)
        else None
      ),
    )

  for index, alternative in enumerate(requirement.generic_alternatives):
    if _all_needles(generic_text, alternative):
      return ParityResult(
        requirement=requirement,
        status=ParityStatus.PRESENT,
        matched_alternative_index=index,
      )

  return ParityResult(
    requirement=requirement,
    status=ParityStatus.MISSING,
    matched_alternative_index=None,
  )


def build_parity_audit():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  dedicated = _render_phase134_3_pi6_3_narrative_markdown(
    presentation
  )
  generic = render_toda_group_proof_narrative_from_proof_chains_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )

  requirements = parity_requirements()

  for requirement in requirements:
    if not _all_needles(dedicated, requirement.dedicated_needles):
      raise AssertionError(
        "dedicated pi_6^3 Narrative no longer satisfies frozen parity "
        f"requirement: {requirement.key}"
      )

  results = tuple(
    evaluate_requirement(requirement, generic)
    for requirement in requirements
  )

  return dedicated, generic, results


def print_audit():
  dedicated, generic, results = build_parity_audit()
  present = tuple(
    result for result in results
    if result.status is ParityStatus.PRESENT
  )
  missing = tuple(
    result for result in results
    if result.status is ParityStatus.MISSING
  )

  print("=" * 78)
  print("Phase 144-6-R5-20 pi_6^3 dedicated <-> ProofChain generic parity audit")
  print("production changes: none")
  print("=" * 78)
  print(f"dedicated_chars={len(dedicated)}")
  print(f"proof_chain_generic_chars={len(generic)}")
  print(f"requirements={len(results)}")
  print(f"present={len(present)}")
  print(f"missing={len(missing)}")

  print("\\nRequirement results")
  print("-" * 78)
  for result in results:
    print(
      f"{result.status.value:>7} "
      f"{result.requirement.kind.value:<17} "
      f"{result.requirement.key}"
    )
    print(f"        {result.requirement.description}")

  print("\\nMissing by kind")
  print("-" * 78)
  for kind in ParityKind:
    keys = tuple(
      result.requirement.key
      for result in missing
      if result.requirement.kind is kind
    )
    print(f"{kind.value}: {len(keys)}")
    for key in keys:
      print(f"  - {key}")

  print("\\nDecision")
  print("-" * 78)
  if not missing:
    print("semantic_parity_ready=True")
    print(
      "All frozen dedicated pi_6^3 mathematical, ordering, discourse, and "
      "structure requirements are present in the ProofChain generic Narrative."
    )
    print(
      "The next step may audit public-route replacement and dedicated-renderer "
      "removal safety."
    )
  else:
    print("semantic_parity_ready=False")
    print(
      "Do not remove the dedicated pi_6^3 renderer and do not switch the public "
      "route yet."
    )
    print(
      "Each missing item must be resolved by a generic ProofChain/Narrative rule, "
      "not by adding a pi_6^3-specific rendering branch."
    )


if __name__ == "__main__":
  print_audit()
