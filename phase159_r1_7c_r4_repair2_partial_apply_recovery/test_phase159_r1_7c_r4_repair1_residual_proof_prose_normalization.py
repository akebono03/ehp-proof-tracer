
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


def _render_group(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def _proof_body(
  rendered: str,
) -> str:
  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def _reference_section(
  rendered: str,
) -> str:
  return rendered.split(
    "\n## 証明\n",
    1,
  )[0]


def test_phase159_r1_7c_r4_repair1_pi6_removes_residual_proof_prose_fragments():
  body = _proof_body(
    _render_group(
      3,
      3,
    )
  )

  assert r"$\eta_{6}=E\eta_{5}$." in body
  assert r"$\eta_{6}=E\eta_{5}$ である." not in body
  assert "次の短完全列が成り立つ." in body
  assert "次の短完全列を得る." not in body
  assert r"$4\nu'=0$ かつ $2\nu'\neq0$." in body
  assert r"$4\nu'=0$ かつ $2\nu'\neq0$ である." not in body
  assert r"中央の群の位数は $2\cdot2=4$." in body
  assert r"中央の群の位数は $2\cdot2=4$ である." not in body


def test_phase159_r1_7c_r4_repair1_pi8_removes_duplicate_transition_and_math_suffix():
  body = _proof_body(
    _render_group(
      5,
      3,
    )
  )

  assert r"$\eta_{6}=E\eta_{5}$." in body
  assert r"$\eta_{6}=E\eta_{5}$ である." not in body
  assert "以上より, この完全性と " not in body
  assert "したがって, この完全性と " not in body


def test_phase159_r1_7c_r4_repair1_pi6_reference_is_unchanged_in_scope():
  reference = _reference_section(
    _render_group(
      3,
      3,
    )
  )

  assert "**[R2] (5.3).**" in reference
  assert r"$2\nu' = \eta_{3}^{3}$." in reference
  assert r"$H\left(\nu'\right) = \eta_{5}$." in reference


def test_phase159_r1_7c_r4_repair1_pi11_r3_reference_pruning_remains_intact():
  reference = _reference_section(
    _render_group(
      4,
      7,
    )
  )

  assert "Proposition 5.15" in reference
  assert "Proposition 5.8" in reference
  assert "Proposition 4.4" in reference

  assert r"\pi_{9}^{2}=0" not in reference
  assert r"\pi_{6}^{2}" not in reference
  assert r"\pi_{7}^{3}" not in reference
  assert r"\pi_{8}^{4}" not in reference
  assert r"\pi_{9}^{5}" not in reference
