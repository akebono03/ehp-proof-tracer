from dataclasses import dataclass
from enum import Enum

from audit_phase144_6_r5_20 import (
  ParityStatus,
  build_parity_audit,
)
from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_frontier_hidden_step_ids,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
)
from toda_group_proof_narrative_proof_chain_renderer import (
  render_toda_group_proof_narrative_from_proof_chains_markdown,
)


MISSING_KEYS = (
  "hopf_nu_prime",
  "pi5_3_group",
  "nu_eta6_membership",
  "hopf_nu_eta6",
  "pi7_5_group",
  "hopf_pi7_surjective",
  "delta_zero",
)


class LossStage(Enum):
  NOT_FOUND_IN_PRESENTATION = "not_found_in_presentation"
  NOT_IN_ARGUMENT_LOCAL_BODY = "not_in_argument_local_body"
  FRONTIER_HIDDEN = "frontier_hidden"
  GENERIC_STEP_RENDER_MISMATCH = "generic_step_render_mismatch"
  FINAL_ASSEMBLY_SUPPRESSED = "final_assembly_suppressed"
  PRESENTATION_MATCH_BUT_PARITY_NEEDLE_MISMATCH = (
    "presentation_match_but_parity_needle_mismatch"
  )


@dataclass(frozen=True)
class FactProbe:
  key: str
  statement_type_needles: tuple[str, ...]
  rendered_needles: tuple[str, ...]


@dataclass(frozen=True)
class FactTrace:
  key: str
  matching_step_count: int
  matching_block_roles: tuple[str, ...]
  proof_chain_provider_hits: int
  local_body_argument_indices: tuple[int, ...]
  frontier_hidden_argument_indices: tuple[int, ...]
  rendered_step_samples: tuple[str, ...]
  final_text_has_rendered_sample: bool
  loss_stage: LossStage


def probes():
  return (
    FactProbe(
      key="hopf_nu_prime",
      statement_type_needles=("Hopf",),
      rendered_needles=(r"H(\nu')", r"\eta_{5}"),
    ),
    FactProbe(
      key="pi5_3_group",
      statement_type_needles=(),
      rendered_needles=(r"\pi_{5}^{3}", r"\mathbb{Z}/2"),
    ),
    FactProbe(
      key="nu_eta6_membership",
      statement_type_needles=("Membership",),
      rendered_needles=(r"\nu'\eta_{6}", r"\pi_{7}^{3}"),
    ),
    FactProbe(
      key="hopf_nu_eta6",
      statement_type_needles=("Hopf",),
      rendered_needles=(r"H(\nu'\eta_{6})", r"\eta_{5}"),
    ),
    FactProbe(
      key="pi7_5_group",
      statement_type_needles=(),
      rendered_needles=(r"\pi_{7}^{5}", r"\mathbb{Z}/2"),
    ),
    FactProbe(
      key="hopf_pi7_surjective",
      statement_type_needles=(),
      rendered_needles=(r"\pi_{7}^{3}", r"\pi_{7}^{5}", "全射"),
    ),
    FactProbe(
      key="delta_zero",
      statement_type_needles=(),
      rendered_needles=(r"\Delta", r"\pi_{7}^{5}", r"\pi_{5}^{2}", "零"),
    ),
  )


def _step_rendering(proof_step):
  try:
    return _render_generic_narrative_step(proof_step)
  except Exception as exc:
    return f"<render-error:{type(exc).__name__}:{exc}>"


def _step_matches_probe(proof_step, probe):
  statement_type = type(proof_step.conclusion).__name__
  if probe.statement_type_needles and not all(
    needle in statement_type
    for needle in probe.statement_type_needles
  ):
    return False

  rendered = _step_rendering(proof_step)
  return all(
    needle in rendered
    for needle in probe.rendered_needles
  )


def _provider_blocks(chain, arguments):
  blocks = []
  for provider in chain.providers:
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind.SUPPORTING_BLOCK
    ):
      blocks.append(provider.supporting_block)
      continue

    child_argument = arguments[provider.child_argument_index]
    blocks.append(child_argument.conclusion_block)
  return tuple(blocks)


def build_missing_fact_traces():
  dedicated, generic_from_phase20, parity_results = build_parity_audit()
  missing_results = {
    result.requirement.key: result
    for result in parity_results
    if result.status is ParityStatus.MISSING
  }
  if tuple(
    key for key in MISSING_KEYS
    if key in missing_results
  ) != MISSING_KEYS:
    raise AssertionError(
      "Phase 20 missing-fact set changed; rerun/review Phase 20 before 21."
    )

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)

  final_text = render_toda_group_proof_narrative_from_proof_chains_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    proof_chains,
  )

  local_bodies = tuple(
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
    for argument_index in range(len(arguments))
  )
  hidden_ids = tuple(
    _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
      presentation,
      blocks,
      local_bodies[argument_index],
      semantic_sidecar,
      arguments[argument_index],
    )
    for argument_index in range(len(arguments))
  )

  traces = []

  for probe in probes():
    matching_steps = tuple(
      proof_step
      for block in blocks
      for proof_step in block.steps
      if _step_matches_probe(proof_step, probe)
    )
    matching_ids = {id(step) for step in matching_steps}

    matching_block_roles = tuple(
      dict.fromkeys(
        block.role.value
        for block in blocks
        if any(id(step) in matching_ids for step in block.steps)
      )
    )

    provider_hits = 0
    for chain in proof_chains:
      for provider_block in _provider_blocks(chain, arguments):
        if any(
          id(step) in matching_ids
          for step in provider_block.steps
        ):
          provider_hits += 1

    local_body_indices = tuple(
      argument_index
      for argument_index, local_body in enumerate(local_bodies)
      if any(
        id(step) in matching_ids
        for block in local_body
        for step in block.steps
      )
    )
    hidden_argument_indices = tuple(
      argument_index
      for argument_index in local_body_indices
      if any(
        step_id in hidden_ids[argument_index]
        for step_id in matching_ids
      )
    )

    samples = tuple(
      dict.fromkeys(
        _step_rendering(step)
        for step in matching_steps
      )
    )[:5]
    final_has_sample = any(
      sample in final_text
      for sample in samples
      if not sample.startswith("<render-error:")
    )

    if not matching_steps:
      loss_stage = LossStage.NOT_FOUND_IN_PRESENTATION
    elif not local_body_indices:
      loss_stage = LossStage.NOT_IN_ARGUMENT_LOCAL_BODY
    elif hidden_argument_indices:
      loss_stage = LossStage.FRONTIER_HIDDEN
    elif any(sample.startswith("<render-error:") for sample in samples):
      loss_stage = LossStage.GENERIC_STEP_RENDER_MISMATCH
    elif not final_has_sample:
      loss_stage = LossStage.FINAL_ASSEMBLY_SUPPRESSED
    else:
      loss_stage = (
        LossStage.PRESENTATION_MATCH_BUT_PARITY_NEEDLE_MISMATCH
      )

    traces.append(
      FactTrace(
        key=probe.key,
        matching_step_count=len(matching_steps),
        matching_block_roles=matching_block_roles,
        proof_chain_provider_hits=provider_hits,
        local_body_argument_indices=local_body_indices,
        frontier_hidden_argument_indices=hidden_argument_indices,
        rendered_step_samples=samples,
        final_text_has_rendered_sample=final_has_sample,
        loss_stage=loss_stage,
      )
    )

  return tuple(traces)


def print_audit():
  traces = build_missing_fact_traces()

  print("=" * 78)
  print("Phase 144-6-R5-21 missing 7 facts generic-provider audit")
  print("production changes: none")
  print("=" * 78)

  for trace in traces:
    print(f"\\n{trace.key}")
    print("-" * 78)
    print(f"matching_steps={trace.matching_step_count}")
    print(
      "block_roles="
      + (
        ",".join(trace.matching_block_roles)
        if trace.matching_block_roles
        else "-"
      )
    )
    print(f"proof_chain_provider_hits={trace.proof_chain_provider_hits}")
    print(
      "local_body_arguments="
      + (
        ",".join(str(index) for index in trace.local_body_argument_indices)
        if trace.local_body_argument_indices
        else "-"
      )
    )
    print(
      "frontier_hidden_arguments="
      + (
        ",".join(str(index) for index in trace.frontier_hidden_argument_indices)
        if trace.frontier_hidden_argument_indices
        else "-"
      )
    )
    print(f"final_text_has_rendered_sample={trace.final_text_has_rendered_sample}")
    print(f"loss_stage={trace.loss_stage.value}")
    for sample in trace.rendered_step_samples:
      print(f"  sample: {sample}")

  print("\\nLoss-stage summary")
  print("-" * 78)
  for stage in LossStage:
    keys = tuple(
      trace.key
      for trace in traces
      if trace.loss_stage is stage
    )
    print(f"{stage.value}: {len(keys)}")
    for key in keys:
      print(f"  - {key}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "Phase 21 diagnoses where each Phase 20 missing fact disappears."
  )
  print(
    "No renderer rule is changed here. The next implementation must target "
    "the observed loss stage generically, without a pi_6^3-specific branch."
  )


if __name__ == "__main__":
  print_audit()
