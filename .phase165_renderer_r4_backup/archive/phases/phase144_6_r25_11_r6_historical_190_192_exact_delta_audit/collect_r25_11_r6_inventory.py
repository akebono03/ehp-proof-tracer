import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import importlib.util
import json
from pathlib import Path
import sys

from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_contribution_ordering import (
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
  _contribution_insertion_indices,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


@dataclass(frozen=True)
class Row:
  n: int
  k: int
  argument_role: str
  discourse_role: str
  statement_type: str
  rendered: str
  provider_anchor: bool
  placement: str
  provider_key_count: int
  insertable: bool


def _load_foundation():
  path = (
    Path("tests")
    / "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
  )
  name = "_r25_11_r6_foundation"
  spec = importlib.util.spec_from_file_location(
    name,
    path,
  )
  if spec is None or spec.loader is None:
    raise ImportError(
      f"cannot load {path}"
    )
  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


def _normalized(text):
  return "".join(
    text.split()
  )


def _discourse_by_argument_id(arguments):
  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  return {
    id(argument): discourse_roles[position]
    for position, argument in enumerate(
      ordered_arguments
    )
  }


def build_inventory():
  foundation = _load_foundation()
  rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate,
      proof_chains,
    ) = foundation._context(
      n,
      k,
    )
    base = (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
        current_markdown=base,
      )
    )
    insertion_indices = (
      _contribution_insertion_indices(
        base,
        blocks,
        arguments,
        ordered,
      )
    )
    discourse = _discourse_by_argument_id(
      arguments
    )

    for argument_index, contributions in enumerate(
      ordered
    ):
      argument = arguments[
        argument_index
      ]
      discourse_role = discourse[
        id(argument)
      ]

      for contribution_index, contribution in enumerate(
        contributions
      ):
        step = contribution.proof_step
        rows.append(
          Row(
            n=n,
            k=k,
            argument_role=argument.role.value,
            discourse_role=discourse_role.value,
            statement_type=type(
              step.conclusion
            ).__name__,
            rendered=_normalized(
              _render_generic_narrative_step(
                step
              )
            ),
            provider_anchor=(
              contribution.provider_anchor
            ),
            placement=(
              contribution.placement.value
            ),
            provider_key_count=len(
              contribution.provider_keys
            ),
            insertable=(
              insertion_indices[
                argument_index
              ][
                contribution_index
              ]
              is not None
            ),
          )
        )

  return tuple(
    rows
  )


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--label",
    required=True,
  )
  parser.add_argument(
    "--output",
    required=True,
  )
  args = parser.parse_args()

  rows = build_inventory()
  payload = {
    "label": args.label,
    "selected_total": len(
      rows
    ),
    "group_counts": {
      f"pi_{n + k}^{n}": sum(
        1
        for row in rows
        if (
          row.n,
          row.k,
        ) == (
          n,
          k,
        )
      )
      for n, k in TARGETS
    },
    "participating": sum(
      1
      for row in rows
      if row.discourse_role != "detached"
    ),
    "detached": sum(
      1
      for row in rows
      if row.discourse_role == "detached"
    ),
    "detached_insertable": sum(
      1
      for row in rows
      if (
        row.discourse_role == "detached"
        and row.insertable
      )
    ),
    "rows": [
      asdict(
        row
      )
      for row in rows
    ],
  }

  Path(
    args.output
  ).write_text(
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ),
    encoding="utf-8",
  )

  print(
    f"{args.label}: selected={payload['selected_total']} "
    f"participating={payload['participating']} "
    f"detached={payload['detached']} "
    f"detached_insertable={payload['detached_insertable']}"
  )
  for group, count in payload[
    "group_counts"
  ].items():
    print(
      f"  {group}: {count}"
    )


if __name__ == "__main__":
  main()
