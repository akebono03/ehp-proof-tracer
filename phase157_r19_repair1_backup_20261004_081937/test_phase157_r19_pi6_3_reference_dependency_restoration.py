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
    3,
    3,
  )
  replay = build_toda_group_result_proof_replay(
    report.group_result,
    depth=2,
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

  assert "Proposition 5.6." in reference
  assert "(5.3)." in reference
  assert "Proposition 5.3." in reference
  assert "Proposition 5.1." in reference
  assert "Proposition 2.2." in reference

  assert (
    r"$H(\alpha\circ E\beta) = H(\alpha)\circ E\beta$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in reference
  )
  assert (
    r"$H\left(\nu'\right) = E^{2}\eta_{3}$."
    not in reference
  )


def test_phase157_r19_pi6_3_delta_zero_has_visible_dependency_chain():
  _, body = _reference_and_body()

  exactness = (
    r"\pi_{7}^{3}"
    r" \xrightarrow{H} "
    r"\pi_{7}^{5}"
    r" \xrightarrow{\Delta} "
    r"\pi_{5}^{2}"
  )
  hopf_value = (
    r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$."
  )
  pi7_5_group = (
    r"\pi_{7}^{5}"
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

  assert exactness in body
  assert hopf_value in body
  assert pi7_5_group in body
  assert hopf_surjective in body
  assert delta_zero in body
  assert suspension_injective in body

  assert body.index(
    exactness
  ) < body.index(
    hopf_surjective
  )
  assert body.index(
    hopf_value
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


def test_phase157_r19_pi6_3_prop53_and_prop22_are_used_in_body():
  reference, body = _reference_and_body()

  prop53_marker = next(
    (
      line.split(
        "]",
        1,
      )[0]
      + "]"
      for line in reference.splitlines()
      if "Proposition 5.3." in line
    ),
    None,
  )
  prop22_marker = next(
    (
      line.split(
        "]",
        1,
      )[0]
      + "]"
      for line in reference.splitlines()
      if "Proposition 2.2." in line
    ),
    None,
  )

  assert prop53_marker is not None
  assert prop22_marker is not None
  assert prop53_marker in body
  assert prop22_marker in body
