from collections import Counter
from dataclasses import dataclass

from audit_phase144_6_r5_23 import (
  _canonical_fact_targets,
  _step_contains_target,
)
from audit_phase144_6_r5_35 import (
  VISIBILITY_GAP_KEYS,
  build_pi6_gap_necessity,
  _local_body,
  _effective_hidden_ids,
  _necessity_for_chain,
)
from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  TARGETS,
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


@dataclass(frozen=True)
class NecessaryCoverageRecord:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  statement_type: str
  provider_anchor: bool
  distance_to_conclusion: int | None
  step_render: str
  exact_render_present: bool
  normalized_render_present: bool


@dataclass(frozen=True)
class Pi6CoverageRecord:
  key: str
  argument_index: int
  argument_role: str
  necessary: bool
  provider_anchor: bool
  hidden: bool
  step_render: str | None
  exact_render_present: bool
  normalized_render_present: bool


def _normalize_markdown(text):
  return "".join(text.split())


def _coverage(step_render, markdown):
  exact = step_render in markdown
  normalized = _normalize_markdown(step_render) in _normalize_markdown(markdown)
  return exact, normalized


def build_necessary_current_display_coverage():
  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(n, k)
    markdown = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )

    for argument_index, argument in enumerate(arguments):
      conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
      if conclusion_step is None:
        continue
      body = _local_body(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
      hidden_ids = _effective_hidden_ids(
        presentation,
        blocks,
        body,
        semantic_sidecar,
        argument,
      )
      chain_ids, anchors, distances, reachable_anchors, necessity = (
        _necessity_for_chain(
          presentation,
          body,
          proof_chains[argument_index],
          conclusion_step,
        )
      )
      block_by_id = {
        id(step): block
        for block in body
        for step in block.steps
      }
      step_by_id = {
        id(step): step
        for block in body
        for step in block.steps
      }

      for step_id in chain_ids & hidden_ids:
        if not necessity.get(step_id, ()):
          continue
        step = step_by_id.get(step_id)
        block = block_by_id.get(step_id)
        if step is None or block is None:
          continue
        rendered = _render_generic_narrative_step(step)
        exact, normalized = _coverage(rendered, markdown)
        rows.append(
          NecessaryCoverageRecord(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            block_role=block.role.value,
            statement_type=type(step.conclusion).__name__,
            provider_anchor=step_id in anchors,
            distance_to_conclusion=distances.get(step_id),
            step_render=rendered,
            exact_render_present=exact,
            normalized_render_present=normalized,
          )
        )

  return tuple(rows)


def build_pi6_gap_current_display_coverage():
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(3, 3)
  markdown = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  targets = _canonical_fact_targets()
  necessity_rows = build_pi6_gap_necessity()
  necessity_by_key_argument = {
    (row.key, row.argument_index): row
    for row in necessity_rows
  }
  rows = []

  for argument_index, argument in enumerate(arguments):
    matching_by_key = {}
    for key in VISIBILITY_GAP_KEYS:
      matches = tuple(
        dict.fromkeys(
          step
          for block in blocks
          for step in block.steps
          if _step_contains_target(step, targets[key])
        )
      )
      matching_by_key[key] = matches

    for key in VISIBILITY_GAP_KEYS:
      necessity = necessity_by_key_argument.get((key, argument_index))
      if necessity is None:
        continue
      matches = matching_by_key[key]
      step = next(
        (
          candidate
          for candidate in matches
          if (
            type(candidate.conclusion).__name__
            == necessity.statement_type
          )
        ),
        matches[0] if matches else None,
      )
      rendered = None if step is None else _render_generic_narrative_step(step)
      exact, normalized = (
        (False, False)
        if rendered is None
        else _coverage(rendered, markdown)
      )
      rows.append(
        Pi6CoverageRecord(
          key=key,
          argument_index=argument_index,
          argument_role=argument.role.value,
          necessary=necessity.necessary_for_any_anchor,
          provider_anchor=necessity.provider_anchor,
          hidden=necessity.hidden,
          step_render=rendered,
          exact_render_present=exact,
          normalized_render_present=normalized,
        )
      )

  return tuple(rows)


def _top(counter, limit=40):
  return counter.most_common(limit)


def print_audit():
  inventory = build_necessary_current_display_coverage()
  pi6 = build_pi6_gap_current_display_coverage()

  print("=" * 78)
  print("Phase 144-6-R5-36 necessary contribution current-display coverage audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. pi_6^3 genuine visibility gaps: current display coverage")
  print("-" * 78)
  for row in pi6:
    print(
      f"{row.key}: argument={row.argument_index} role={row.argument_role} "
      f"necessary={row.necessary} anchor={row.provider_anchor} "
      f"hidden={row.hidden} exact_present={row.exact_render_present} "
      f"normalized_present={row.normalized_render_present}"
    )
    if row.step_render is not None:
      print(f"  step_render={row.step_render}")

  print("\\nB. Six-group necessary hidden contribution coverage")
  print("-" * 78)
  total_exact = 0
  total_normalized = 0
  for n, k in TARGETS:
    rows = tuple(row for row in inventory if (row.n, row.k) == (n, k))
    exact = sum(row.exact_render_present for row in rows)
    normalized = sum(row.normalized_render_present for row in rows)
    total_exact += exact
    total_normalized += normalized
    print(
      f"pi_{n + k}^{n}: necessary={len(rows)} "
      f"exact_present={exact} normalized_present={normalized} "
      f"genuinely_missing={len(rows)-normalized}"
    )
  print(
    f"totals: necessary={len(inventory)} exact_present={total_exact} "
    f"normalized_present={total_normalized} "
    f"genuinely_missing={len(inventory)-total_normalized}"
  )

  missing = tuple(
    row for row in inventory
    if not row.normalized_render_present
  )
  present = tuple(
    row for row in inventory
    if row.normalized_render_present
  )

  print("\\nC. Genuinely missing necessary contribution semantics")
  print("-" * 78)
  print("Block roles")
  for name, count in _top(Counter(row.block_role for row in missing)):
    print(f"{count:4d}  {name}")
  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in missing)):
    print(f"{count:4d}  {name}")
  print("\\nArgument roles")
  for name, count in _top(Counter(row.argument_role for row in missing)):
    print(f"{count:4d}  {name}")

  print("\\nD. Already represented necessary contribution semantics")
  print("-" * 78)
  print("Block roles")
  for name, count in _top(Counter(row.block_role for row in present)):
    print(f"{count:4d}  {name}")
  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in present)):
    print(f"{count:4d}  {name}")

  print("\\nE. Genuinely missing cross classification")
  print("-" * 78)
  cross = Counter(
    (
      row.argument_role,
      row.block_role,
      row.statement_type,
      "anchor" if row.provider_anchor else "chain",
    )
    for row in missing
  )
  for key, count in _top(cross):
    print(f"{count:4d}  {key}")

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "Coverage is diagnostic: a necessary hidden contribution is counted as "
    "already represented when its generic single-step rendering occurs in "
    "the current final multi-Argument Narrative, with a whitespace-insensitive "
    "secondary check."
  )
  print(
    "This does not yet prove semantic equivalence between differently worded "
    "sentences. A large genuinely-missing population requires a finer semantic "
    "coverage audit before any production visibility rule."
  )
  print(
    "No production frontier, renderer, ProofChain, ownership, deduplication, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
