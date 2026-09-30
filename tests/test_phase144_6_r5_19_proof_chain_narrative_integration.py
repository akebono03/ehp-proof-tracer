import pytest
from functools import lru_cache

from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)


_uncached_context = _context

@lru_cache(maxsize=None)
def _context(n, k):
  return _uncached_context(n, k)

def _uncached_render_pair(n, k):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(n, k)

  legacy_generic = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chain_generic = (
    render_toda_group_proof_narrative_from_proof_chains_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )

  return (
    legacy_generic,
    proof_chain_generic,
    proof_chains,
  )


@lru_cache(maxsize=None)
def _render_pair(n, k):
  return _uncached_render_pair(n, k)

def test_phase144_6_r5_19_proof_chain_integration_preserves_generic_output():
  for n, k in TARGETS:
    legacy_generic, proof_chain_generic, proof_chains = (
      _render_pair(n, k)
    )

    assert proof_chain_generic == legacy_generic


def test_phase144_6_r5_19_pi6_3_is_available_through_proof_chain_entrypoint():
  legacy_generic, proof_chain_generic, proof_chains = (
    _render_pair(3, 3)
  )

  assert proof_chain_generic
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in proof_chain_generic
  )


def test_phase144_6_r5_19_all_six_groups_are_available_through_entrypoint():
  expected_targets = {
    (3, 3): r"\pi_{6}^{3}",
    (5, 3): r"\pi_{8}^{5}",
    (4, 6): r"\pi_{10}^{4}",
    (5, 7): r"\pi_{12}^{5}",
    (8, 7): r"\pi_{15}^{8}",
    (9, 7): r"\pi_{16}^{9}",
  }

  for n, k in TARGETS:
    legacy_generic, proof_chain_generic, proof_chains = (
      _render_pair(n, k)
    )

    assert expected_targets[
      (n, k)
    ] in proof_chain_generic


def test_phase144_6_r5_19_rejects_missing_proof_chain():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  with pytest.raises(
    ValueError,
    match="exactly one chain for each argument",
  ):
    render_toda_group_proof_narrative_from_proof_chains_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains[:-1],
    )


def test_phase144_6_r5_19_rejects_duplicate_argument_index():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  duplicate_chains = (
    proof_chains[0],
    proof_chains[0],
    proof_chains[2],
  )

  with pytest.raises(
    ValueError,
    match="duplicate argument_index",
  ):
    render_toda_group_proof_narrative_from_proof_chains_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      duplicate_chains,
    )


def test_phase144_6_r5_19_rejects_foreign_proof_chain_argument():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  foreign_proof_chain = _context(5, 3)[5][0]

  mixed_chains = (
    foreign_proof_chain,
    *proof_chains[1:],
  )

  with pytest.raises(
    ValueError,
    match=(
      "proof_chain argument must be the argument "
      "at proof_chain argument_index"
    ),
  ):
    render_toda_group_proof_narrative_from_proof_chains_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      mixed_chains,
    )


def test_phase144_6_r5_19_rejects_foreign_semantic_sidecar():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  foreign_semantic_sidecar = _context(5, 3)[1]

  with pytest.raises(
    ValueError,
    match="semantic_sidecar must belong to presentation",
  ):
    render_toda_group_proof_narrative_from_proof_chains_markdown(
      presentation,
      blocks,
      foreign_semantic_sidecar,
      arguments,
      proof_chains,
    )
