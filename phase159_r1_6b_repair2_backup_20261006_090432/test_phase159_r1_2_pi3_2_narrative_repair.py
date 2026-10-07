from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
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
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
)


def _phase159_r1_2_pi3_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_2_pi3_2_definition_uses_semantic_prose():
  presentation = _phase159_r1_2_pi3_2_presentation()
  definition_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaPi32Eta2DefinitionStatement,
    )
  )

  rendered = _render_generic_narrative_step(
    definition_step
  )

  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert r"H(\eta_{2}) = \iota_{3}" in rendered
  assert r"\eta_{2} \in \pi_{3}^{2}" in rendered
  assert "を定める." in rendered


def test_phase159_r1_3_pi3_2_public_target_has_no_show_sentence():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  target = (
    "## 証明対象\n\n"
    "\\[\n"
    r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}."
    "\n\\]"
  )

  assert target in rendered
  assert "を示す." not in rendered
  assert "を示す。" not in rendered


def test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  long_exact = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$ は完全である."
  )

  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  exactness_lines = tuple(
    line
    for line in proof_body.splitlines()
    if r"\xrightarrow{" in line
  )

  assert exactness_lines == (
    long_exact,
  )

def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\tag{1}$ は単射."
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\tag{2}$ は全射."
  )
  isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert "(1), (2) より, " + isomorphism in rendered
  assert rendered.index(injective) < rendered.index(surjective)
  assert rendered.index(surjective) < rendered.index(isomorphism)

def test_phase159_r1_3_pi3_2_public_definition_uses_isomorphism_semantics():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    "この同型写像により, "
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
    in rendered
  )
  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert rendered.rstrip().endswith("□")


def test_phase159_r1_4_pi3_2_public_math_sentences_end_with_period():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert r"$\pi_{2}^{1} = 0$." in rendered
  assert r"$\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$." in rendered
  assert (
    r"以上より, $\pi_{3}^{2} = "
    r"\mathbb{Z}\{\eta_{2}\}$."
    in rendered
  )


def test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は単射."
    in rendered
  )
  assert (
    r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
    "は零写像."
    in rendered
  )

  assert "は単射である." not in rendered
  assert "は全射である." not in rendered
  assert "は同型写像である." not in rendered
  assert "は零写像である." not in rendered
