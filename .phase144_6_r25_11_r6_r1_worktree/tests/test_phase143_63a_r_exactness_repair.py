from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render(n, k):
  presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
  return render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    sidecar,
    arguments,
  )


def test_phase143_63a_r_exactness_sentence_is_not_double_wrapped():
  for n, k in ((3, 3), (5, 3), (9, 7)):
    rendered = _render(n, k)
    assert "$$" not in rendered
    assert "$ は完全である.$ は完全である." not in rendered


def test_phase143_63a_r_pi8_5_exactness_is_single_japanese_sentence():
  rendered = _render(5, 3)
  expected = (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  assert rendered.count(expected) == 1


def test_phase143_63a_r_pi16_9_exactness_is_single_japanese_sentence():
  rendered = _render(9, 7)
  expected = (
    r"$\pi_{12}^{5} \xrightarrow{H} "
    r"\pi_{12}^{9} \xrightarrow{\Delta} "
    r"\pi_{10}^{4}$ は完全である."
  )
  assert rendered.count(expected) == 1


def test_phase143_63a_r_provenance_suppression_remains():
  rendered = _render(9, 7)
  assert "Toda Lemma 5.14 sigma_8 branch" not in rendered
  assert "TodaLemma514Sigma8Statement" not in rendered


def test_phase143_63a_r_pi8_5_direct_premise_placement_remains():
  rendered = _render(5, 3)
  assert (
    r"$2\nu_{5} = E^{2}\nu'$"
    "\n\n"
    r"$\operatorname{ord}\left(E^{2}\nu'\right) = 4$"
    "\n\n"
    "以上より、"
    "\n\n"
    r"$\operatorname{ord}\left(\nu_{5}\right) = 8$"
    in rendered
  )
