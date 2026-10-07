from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_dangling_connectors,
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


def _body_pi6_3_repair43() -> str:
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
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r20_repair43_has_no_dangling_connector_paragraphs_or_lines():
  body = _body_pi6_3_repair43()
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  for paragraph in body.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    assert stripped not in standalone_connectors

    lines = tuple(
      line.strip()
      for line in paragraph.splitlines()
      if line.strip()
    )

    if not lines:
      continue

    assert lines[
      -1
    ] not in standalone_connectors


def test_phase157_r20_repair43_keeps_valid_numbered_derivation_connector():
  markdown = "\n\n".join(
    (
      r"$a=b\tag{4}$",
      r"$b=c\tag{7}$",
      "(4) と (7) より,",
      r"$a=c$",
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      markdown
    )
  )

  assert "(4) と (7) より," in rendered


def test_phase157_r20_repair43_removes_unreferenced_numbered_connector():
  markdown = "\n\n".join(
    (
      r"$a=b$",
      "(4) と (7) より,",
      r"$a=c$",
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      markdown
    )
  )

  assert "(4) と (7) より," not in rendered


def test_phase157_r20_repair43_reference_marker_does_not_keep_redundant_connector_prefix():
  body = _body_pi6_3_repair43()

  assert (
    "以上より, [R"
    not in body
  )
  assert (
    "したがって, [R"
    not in body
  )
  assert (
    "これらより, [R"
    not in body
  )


def test_phase157_r20_repair43_required_reason_sentences_remain():
  body = _body_pi6_3_repair43()

  assert (
    "完全性より, "
    r"$\ker \Delta=\operatorname{Im}H="
    r"\pi_{7}^{5}$ である."
    in body
  )
  assert (
    "この完全性と $Δ=0$ より, "
    r"$\ker E=\operatorname{Im}Δ=0$ である."
    in body
  )
  assert (
    r"$\operatorname{ord}(\eta_{3}^{3})=2$ "
    r"かつ $2\nu'=\eta_{3}^{3}$ より, "
    r"$4\nu'=0$ かつ $2\nu'\neq0$ である."
    in body
  )
