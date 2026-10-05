from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render_pi6_3() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_and_body() -> tuple[
  str,
  str,
]:
  rendered = _render_pi6_3()
  reference, body = rendered.split(
    "\n## 証明\n",
    1,
  )

  return (
    reference,
    body,
  )


def test_phase157_r19_pi6_3_public_references_name_all_used_results():
  reference, _ = _reference_and_body()

  assert "**[R1] Proposition 5.6.**" in reference
  assert "**[R2] (5.3).**" in reference
  assert "**[R3] Proposition 5.3.**" in reference
  assert "**[R4] Proposition 5.1.**" in reference
  assert "**[R5] Proposition 2.2.**" in reference

  assert (
    r"$\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}$."
    in reference
  )
  assert (
    r"$2\nu' = \eta_{3}^{3}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )
  assert (
    r"$\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}$."
    in reference
  )
  assert (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
    in reference
  )
  assert (
    r"$H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$."
    in reference
  )


def test_phase157_r19_pi6_3_delta_zero_has_only_shallow_visible_support():
  _, body = _reference_and_body()

  hopf_calculation = (
    r"$H\left(\nu'\eta_{6}\right)"
    r"=H\left(\nu'\right)\eta_{6}"
    r"=\eta_{5}\eta_{6}"
    r"=\eta_{5}^{2}$."
  )
  pi7_5_group = (
    r"$\pi_{7}^{5}"
    r"=\mathbb{Z}/2\{\eta_{5}^{2}\}$."
  )
  hopf_surjective = (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である."
  )
  delta_zero = (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である."
  )
  suspension_injective = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )

  assert "[R5] と [R2] より" in body
  assert "[R3]より" in body
  assert hopf_calculation in body
  assert pi7_5_group in body
  assert hopf_surjective in body
  assert delta_zero in body
  assert suspension_injective in body

  assert body.index(
    hopf_calculation
  ) < body.index(
    pi7_5_group
  )
  assert body.index(
    pi7_5_group
  ) < body.index(
    hopf_surjective
  )
  assert body.index(
    hopf_surjective
  ) < body.index(
    delta_zero
  )
  assert body.index(
    delta_zero
  ) < body.index(
    suspension_injective
  )

  forbidden = (
    "`TodaEtaFamilyDefinitionStatement`",
    "`TodaDeltaMap`",
    "`ScalarGreaterEqualStatement`",
    "`TodaPrimaryGroupMembershipStatement`",
    r"\pi_{3}^{2}",
    "Toda pi_3^2",
  )

  for text in forbidden:
    assert text not in body


def test_phase157_r19_pi6_3_prop51_and_prop22_are_used_in_body():
  _, body = _reference_and_body()

  assert (
    "[R4]より, "
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
    in body
  )
  assert "[R5] と [R2] より" in body
