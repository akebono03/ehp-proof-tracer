import re

from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_proof_block,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


_BLOCK_LABEL_PATTERN = re.compile(
  r"\[B\d{2}\]"
)


def _render_multi_argument(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase143_49_pi6_3_narrative_hides_dependency_labels():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    _BLOCK_LABEL_PATTERN.search(
      rendered
    )
    is None
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in rendered
  )


def test_phase143_49_pi8_5_narrative_hides_dependency_labels():
  rendered = _render_multi_argument(
    5,
    3,
  )

  assert (
    _BLOCK_LABEL_PATTERN.search(
      rendered
    )
    is None
  )
  assert (
    r"\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}"
    in rendered
  )
  assert (
    "次の完全列を考える."
    in rendered
  )


def test_phase143_49_pi15_8_narrative_hides_dependency_labels():
  rendered = _render_multi_argument(
    8,
    7,
  )

  assert (
    _BLOCK_LABEL_PATTERN.search(
      rendered
    )
    is None
  )
  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )


def test_phase143_49_pi16_9_narrative_hides_dependency_labels():
  rendered = _render_multi_argument(
    9,
    7,
  )

  assert (
    _BLOCK_LABEL_PATTERN.search(
      rendered
    )
    is None
  )
  assert (
    r"\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}"
    in rendered
  )
  assert (
    "次の完全列を考える."
    in rendered
  )


def test_phase143_49_generic_block_renderer_keeps_dependency_labels_by_default():
  (
    presentation,
    blocks,
    _sidecar,
    _arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered_blocks = tuple(
    "\n".join(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
      )
    )
    for block_index in range(
      len(
        blocks
      )
    )
  )
  rendered = "\n".join(
    rendered_blocks
  )

  assert (
    _BLOCK_LABEL_PATTERN.search(
      rendered
    )
    is not None
  )
