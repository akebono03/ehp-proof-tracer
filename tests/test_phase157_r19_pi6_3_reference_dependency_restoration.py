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


def test_phase157_r19_pi6_3_has_five_named_public_references():
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
    r"$\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}$ とすると,"
    in reference
  )
  assert (
    r"$\nu' \in \pi_{6}^{3}$."
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


def test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support():
  _, body = _reference_and_body()

  full_exactness = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  eta6_definition = (
    r"$\eta_{6}=E\eta_{5}$."
  )
  pi7_5 = (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
  )
  surjective = (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である."
  )
  kernel_reason = (
    "完全性より, "
    r"$\ker \Delta=\operatorname{Im}H="
    r"\pi_{7}^{5}$."
  )
  delta_zero = (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像である."
  )
  injective = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )

  assert full_exactness in body
  assert eta6_definition in body
  assert "[R5]より" in body
  assert "[R3]より" in body
  assert pi7_5 in body
  assert surjective in body
  assert kernel_reason in body
  assert delta_zero in body
  assert injective in body
  assert (
    r"H\left(\nu'\eta_{6}\right)"
    in body
  )
  assert (
    r"\eta_{5}^{2}"
    in body
  )

  assert body.index(
    full_exactness
  ) < body.index(
    eta6_definition
  )
  assert body.index(
    eta6_definition
  ) < body.index(
    "[R5]より"
  )
  assert body.index(
    "[R5]より"
  ) < body.index(
    "[R3]より"
  )
  assert body.index(
    "[R3]より"
  ) < body.index(
    surjective
  )
  assert body.index(
    surjective
  ) < body.index(
    kernel_reason
  )
  assert body.index(
    kernel_reason
  ) < body.index(
    delta_zero
  )
  assert body.index(
    delta_zero
  ) < body.index(
    injective
  )


def test_phase157_r19_pi6_3_uses_canonical_reference_consequences():
  _, body = _reference_and_body()

  assert (
    r"$2\nu' = \eta_{3}^{3}"
    in body
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}"
    in body
    or r"$H\left(\nu'\right)=\eta_{5}"
    in body
  )
  assert (
    "[R4]より" in body
  )
  assert (
    r"$\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$."
    in body
  )

  forbidden = (
    "`TodaEtaFamilyDefinitionStatement`",
    "`TodaDeltaMap`",
    "`ScalarGreaterEqualStatement`",
    "`TodaPrimaryGroupMembershipStatement`",
    r"$E^{2}\eta_{3} = \eta_{5}\tag{5}$.",
    r"\eta_{2}\eta_{3}\eta_{4}",
    r"\eta_{3}\eta_{4}\eta_{5}",
  )

  for text in forbidden:
    assert text not in body


