from collections import Counter
from dataclasses import dataclass

from audit_phase144_6_r5_35 import (
  _effective_hidden_ids,
  _local_body,
  _necessity_for_chain,
)
from audit_phase144_6_r5_36 import (
  _coverage,
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
class SemanticCoverageRecord:
  n: int
  k: int
  argument_index: int
  argument_role: str
  block_role: str
  statement_type: str
  provider_anchor: bool
  distance_to_conclusion: int | None
  step_render: str
  direct_render_present: bool
  equivalent_statement_present: bool
  rendering_fallback: bool
  classification: str


def _is_rendering_fallback(step, rendered):
  rule = step.inference_rule
  if rule is not None and rendered == rule.name:
    return True
  return rendered == ("`" + type(step.conclusion).__name__ + "`")


def _visible_statement_catalog(presentation, markdown):
  catalog = []
  for node in presentation.nodes:
    step = node.proof_step
    rendered = _render_generic_narrative_step(step)
    exact, normalized = _coverage(rendered, markdown)
    if not normalized:
      continue
    catalog.append((step.conclusion, step, rendered))
  return tuple(catalog)


def _has_equivalent_visible_statement(step, catalog):
  return any(
    visible_statement == step.conclusion
    and visible_step is not step
    for visible_statement, visible_step, _ in catalog
  )


def build_semantic_equivalence_and_rendering_inventory():
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
    visible_catalog = _visible_statement_catalog(
      presentation,
      markdown,
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
        _, direct_present = _coverage(rendered, markdown)
        if direct_present:
          continue

        equivalent_present = _has_equivalent_visible_statement(
          step,
          visible_catalog,
        )
        fallback = _is_rendering_fallback(step, rendered)

        if equivalent_present:
          classification = "semantic_equivalent_present"
        elif fallback:
          classification = "rendering_gap"
        else:
          classification = "visibility_gap"

        rows.append(
          SemanticCoverageRecord(
            n=n,
            k=k,
            argument_index=argument_index,
            argument_role=argument.role.value,
            block_role=block.role.value,
            statement_type=type(step.conclusion).__name__,
            provider_anchor=step_id in anchors,
            distance_to_conclusion=distances.get(step_id),
            step_render=rendered,
            direct_render_present=False,
            equivalent_statement_present=equivalent_present,
            rendering_fallback=fallback,
            classification=classification,
          )
        )

  return tuple(rows)


def _top(counter, limit=50):
  return counter.most_common(limit)


def print_audit():
  rows = build_semantic_equivalence_and_rendering_inventory()

  print("=" * 78)
  print("Phase 144-6-R5-37 genuinely-missing semantic-equivalence and rendering audit")
  print("production changes: none")
  print("=" * 78)

  print("\\nA. Six-group classification")
  print("-" * 78)
  for n, k in TARGETS:
    group_rows = tuple(row for row in rows if (row.n, row.k) == (n, k))
    counts = Counter(row.classification for row in group_rows)
    print(
      f"pi_{n + k}^{n}: candidates={len(group_rows)} "
      f"semantic_equivalent_present={counts['semantic_equivalent_present']} "
      f"rendering_gap={counts['rendering_gap']} "
      f"visibility_gap={counts['visibility_gap']}"
    )

  counts = Counter(row.classification for row in rows)
  print(
    f"totals: candidates={len(rows)} "
    f"semantic_equivalent_present={counts['semantic_equivalent_present']} "
    f"rendering_gap={counts['rendering_gap']} "
    f"visibility_gap={counts['visibility_gap']}"
  )

  print("\\nB. Rendering-gap statement types")
  print("-" * 78)
  rendering = tuple(row for row in rows if row.classification == "rendering_gap")
  for name, count in _top(Counter(row.statement_type for row in rendering)):
    print(f"{count:4d}  {name}")

  print("\\nC. Visibility-gap semantics after exact statement equivalence")
  print("-" * 78)
  visibility = tuple(row for row in rows if row.classification == "visibility_gap")
  print("Block roles")
  for name, count in _top(Counter(row.block_role for row in visibility)):
    print(f"{count:4d}  {name}")
  print("\\nStatement types")
  for name, count in _top(Counter(row.statement_type for row in visibility)):
    print(f"{count:4d}  {name}")
  print("\\nArgument roles")
  for name, count in _top(Counter(row.argument_role for row in visibility)):
    print(f"{count:4d}  {name}")

  print("\\nD. Semantic-equivalent-present statement types")
  print("-" * 78)
  equivalent = tuple(
    row for row in rows
    if row.classification == "semantic_equivalent_present"
  )
  for name, count in _top(Counter(row.statement_type for row in equivalent)):
    print(f"{count:4d}  {name}")

  print("\\nE. Cross classification")
  print("-" * 78)
  cross = Counter(
    (
      row.classification,
      row.argument_role,
      row.block_role,
      row.statement_type,
      "anchor" if row.provider_anchor else "chain",
    )
    for row in rows
  )
  for key, count in _top(cross):
    print(f"{count:4d}  {key}")

  print("\\nF. Rendering-gap examples")
  print("-" * 78)
  seen = set()
  for row in rendering:
    key = (row.statement_type, row.step_render)
    if key in seen:
      continue
    seen.add(key)
    print(f"{row.statement_type}: {row.step_render}")
    if len(seen) >= 20:
      break

  print("\\nDecision boundary")
  print("-" * 78)
  print(
    "semantic_equivalent_present means an equal conclusion statement exists "
    "on another ProofStep whose current generic rendering is present in the "
    "final multi-Argument Narrative."
  )
  print(
    "rendering_gap means the missing necessary step currently falls back to "
    "its inference-rule name or statement-type placeholder."
  )
  print(
    "visibility_gap means neither exact-statement coverage nor renderer fallback "
    "explains the missing contribution. This is still a conservative structural "
    "classification, not a general mathematical equivalence prover."
  )
  print(
    "No production frontier, renderer, ProofChain, ownership, deduplication, "
    "membership, parity matcher, or public route is changed."
  )


if __name__ == "__main__":
  print_audit()
