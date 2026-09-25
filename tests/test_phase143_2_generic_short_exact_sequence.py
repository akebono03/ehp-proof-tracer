import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
import toda_group_proof_generic_narrative_renderer as generic_renderer
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  render_toda_group_proof_generic_proof_markdown,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def _pi6_3_data():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=3,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )

  return (
    presentation,
    blocks,
  )


def test_phase143_2_detects_generic_short_exact_sequence():
  presentation, blocks = (
    _pi6_3_data()
  )

  sequences = tuple(
    sequence
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
    for sequence in (
      _generic_short_exact_sequence_latex(
        presentation,
        node.proof_step,
      ),
    )
    if sequence is not None
  )

  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in sequences
  )


def test_phase143_2_generic_proof_renders_short_exact_sequence():
  presentation, blocks = (
    _pi6_3_data()
  )

  rendered = (
    render_toda_group_proof_generic_proof_markdown(
      presentation,
      blocks,
    )
  )

  assert "次の短完全列を得る." in rendered
  assert (
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0"
    in rendered
  )


def test_phase143_2_requires_both_map_properties():
  presentation, blocks = (
    _pi6_3_data()
  )

  exactness_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  synthesized = tuple(
    _generic_short_exact_sequence_latex(
      presentation,
      proof_step,
    )
    for proof_step in exactness_steps
  )

  assert any(
    sequence is not None
    for sequence in synthesized
  )
  assert any(
    sequence is None
    for sequence in synthesized
  )


def test_phase143_2_short_exact_rule_has_no_pi6_specific_hardcoding():
  source = inspect.getsource(
    generic_renderer._generic_short_exact_sequence_latex
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
    "pi_{5}^{2}",
    "pi_{6}^{3}",
    "pi_{6}^{5}",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
