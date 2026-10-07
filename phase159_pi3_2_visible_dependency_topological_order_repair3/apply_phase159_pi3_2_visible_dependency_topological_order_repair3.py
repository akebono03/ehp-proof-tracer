from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py"
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_visible_dependency_topological_order_repair3_backup"
)


NEW_FUNCTION = r'''def order_toda_group_proof_narrative_visible_step_dependencies(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  if not paragraphs:
    return markdown

  def strip_leading_prose(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            stripped = suffix[
              len(
                prefix
              ):
            ]
            break

    prefixes = (
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
      "完全性より, ",
    )

    changed = True

    while changed:
      changed = False

      for prefix in prefixes:
        if stripped.startswith(
          prefix
        ):
          stripped = stripped[
            len(
              prefix
            ):
          ]
          changed = True
          break

    return stripped

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    return (
      _phase157_r11_reference_statement_match_key(
        strip_leading_prose(
          paragraph
        )
      )
    )

  step_ids_by_key = {}

  for node in presentation.nodes:
    proof_step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      continue

    key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )
    proof_step_id = id(
      proof_step
    )

    step_ids_by_key.setdefault(
      key,
      set(),
    ).add(
      proof_step_id
    )

  paragraph_indices_by_step_id = {}

  for paragraph_index, paragraph in enumerate(
    paragraphs
  ):
    key = paragraph_match_key(
      paragraph
    )
    step_ids = step_ids_by_key.get(
      key,
      set(),
    )

    if len(
      step_ids
    ) != 1:
      continue

    proof_step_id = next(
      iter(
        step_ids
      )
    )
    paragraph_indices_by_step_id.setdefault(
      proof_step_id,
      [],
    ).append(
      paragraph_index
    )

  visible_index_by_step_id = {
    proof_step_id: indices[0]
    for proof_step_id, indices
    in paragraph_indices_by_step_id.items()
    if len(
      indices
    ) == 1
  }

  if len(
    visible_index_by_step_id
  ) < 2:
    return markdown

  source_index_by_argument_id = {
    id(
      argument
    ): argument_index
    for argument_index, argument in enumerate(
      arguments
    )
  }
  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  owner_argument_index_by_step_id = {}
  local_step_ids_by_argument_index = {}

  for argument in ordered_arguments:
    argument_index = source_index_by_argument_id[
      id(
        argument
      )
    ]
    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    local_step_ids = {
      id(
        proof_step
      )
      for block in local_body
      for proof_step in block.steps
    }

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if conclusion_step is not None:
      local_step_ids.add(
        id(
          conclusion_step
        )
      )

    local_step_ids_by_argument_index[
      argument_index
    ] = frozenset(
      local_step_ids
    )

    for proof_step_id in local_step_ids:
      if (
        proof_step_id
        not in visible_index_by_step_id
      ):
        continue

      owner_argument_index_by_step_id.setdefault(
        proof_step_id,
        argument_index,
      )

  reordered = list(
    paragraphs
  )

  for argument in ordered_arguments:
    argument_index = source_index_by_argument_id[
      id(
        argument
      )
    ]
    owned_step_ids = {
      proof_step_id
      for proof_step_id, owner_index
      in owner_argument_index_by_step_id.items()
      if owner_index == argument_index
    }

    if len(
      owned_step_ids
    ) < 2:
      continue

    successors = {
      proof_step_id: set()
      for proof_step_id in owned_step_ids
    }
    indegree = {
      proof_step_id: 0
      for proof_step_id in owned_step_ids
    }

    for edge in presentation.edges:
      premise_id = id(
        edge.premise_step
      )
      consumer_id = id(
        edge.parent_step
      )

      if (
        premise_id
        not in owned_step_ids
        or consumer_id
        not in owned_step_ids
        or premise_id == consumer_id
      ):
        continue

      if consumer_id in successors[
        premise_id
      ]:
        continue

      successors[
        premise_id
      ].add(
        consumer_id
      )
      indegree[
        consumer_id
      ] += 1

    if not any(
      successors.values()
    ):
      continue

    remaining = set(
      owned_step_ids
    )
    ordered_step_ids = []
    preferred_ready_step_ids = set()

    while remaining:
      ready = [
        proof_step_id
        for proof_step_id in remaining
        if indegree[
          proof_step_id
        ] == 0
      ]

      if not ready:
        ordered_step_ids = []
        break

      preferred_ready = [
        proof_step_id
        for proof_step_id in ready
        if proof_step_id
        in preferred_ready_step_ids
      ]
      candidates = (
        preferred_ready
        if preferred_ready
        else ready
      )
      candidates.sort(
        key=lambda proof_step_id: (
          visible_index_by_step_id[
            proof_step_id
          ],
        )
      )
      chosen = candidates[
        0
      ]
      ordered_step_ids.append(
        chosen
      )
      remaining.remove(
        chosen
      )
      newly_ready_step_ids = set()

      for successor in successors[
        chosen
      ]:
        if successor not in remaining:
          continue

        indegree[
          successor
        ] -= 1

        if indegree[
          successor
        ] == 0:
          newly_ready_step_ids.add(
            successor
          )

      preferred_ready_step_ids = (
        newly_ready_step_ids
      )

    if not ordered_step_ids:
      continue

    current_step_ids = tuple(
      sorted(
        owned_step_ids,
        key=lambda proof_step_id: (
          visible_index_by_step_id[
            proof_step_id
          ]
        ),
      )
    )
    ordered_step_ids = tuple(
      ordered_step_ids
    )

    if ordered_step_ids == current_step_ids:
      continue

    paragraph_slots = tuple(
      visible_index_by_step_id[
        proof_step_id
      ]
      for proof_step_id in current_step_ids
    )
    paragraph_by_step_id = {
      proof_step_id: paragraphs[
        visible_index_by_step_id[
          proof_step_id
        ]
      ]
      for proof_step_id in owned_step_ids
    }

    for paragraph_index, proof_step_id in zip(
      paragraph_slots,
      ordered_step_ids,
    ):
      reordered[
        paragraph_index
      ] = paragraph_by_step_id[
        proof_step_id
      ]

  return "\n\n".join(
    reordered
  )


'''


START = (
  "def order_toda_group_proof_narrative_visible_step_dependencies(\n"
)
END = (
  "\n\ndef order_toda_group_proof_narrative_visible_relation_dependencies(\n"
)


def fail(message: str) -> None:
  print(
    "ERROR:",
    message,
    file=sys.stderr,
  )
  raise SystemExit(
    1
  )


if not TARGET.exists():
  fail(
    f"target file not found: {TARGET}"
  )

source = TARGET.read_text(
  encoding="utf-8"
)

start_index = source.find(
  START
)
end_index = source.find(
  END,
  start_index,
)

if (
  start_index < 0
  or end_index < 0
):
  fail(
    "visible-step ordering function boundaries not found"
  )

source = (
  source[
    :start_index
  ]
  + NEW_FUNCTION
  + source[
    end_index + 2:
  ]
)

BACKUP_DIR.mkdir(
  parents=True,
  exist_ok=True,
)

backup_target = (
  BACKUP_DIR
  / TARGET.name
)

if not backup_target.exists():
  shutil.copy2(
    TARGET,
    backup_target,
  )

TARGET.write_text(
  source,
  encoding="utf-8",
)

TEST_TARGET.parent.mkdir(
  parents=True,
  exist_ok=True,
)
shutil.copy2(
  TEST_SOURCE,
  TEST_TARGET,
)

print(
  "Applied Phase 159 pi3_2 visible dependency ordering repair3."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
