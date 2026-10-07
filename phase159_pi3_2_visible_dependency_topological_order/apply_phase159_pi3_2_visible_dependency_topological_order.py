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
  / "phase159_pi3_2_visible_dependency_topological_order_backup"
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

  owner_argument_indices_by_step_id = {}

  for argument_index, argument in enumerate(
    arguments
  ):
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

    for proof_step_id in local_step_ids:
      owner_argument_indices_by_step_id.setdefault(
        proof_step_id,
        set(),
      ).add(
        argument_index
      )

  visible_step_ids = set(
    visible_index_by_step_id
  )
  successors = {
    proof_step_id: set()
    for proof_step_id in visible_step_ids
  }
  indegree = {
    proof_step_id: 0
    for proof_step_id in visible_step_ids
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
      not in visible_step_ids
      or consumer_id
      not in visible_step_ids
      or premise_id == consumer_id
    ):
      continue

    premise_owners = (
      owner_argument_indices_by_step_id.get(
        premise_id,
        set(),
      )
    )
    consumer_owners = (
      owner_argument_indices_by_step_id.get(
        consumer_id,
        set(),
      )
    )

    if not (
      premise_owners
      & consumer_owners
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
    return markdown

  remaining = set(
    visible_step_ids
  )
  ordered_step_ids = []

  while remaining:
    ready = [
      proof_step_id
      for proof_step_id in remaining
      if indegree[
        proof_step_id
      ] == 0
    ]

    if not ready:
      return markdown

    ready.sort(
      key=lambda proof_step_id: (
        visible_index_by_step_id[
          proof_step_id
        ],
      )
    )
    chosen = ready[
      0
    ]
    ordered_step_ids.append(
      chosen
    )
    remaining.remove(
      chosen
    )

    for successor in successors[
      chosen
    ]:
      if successor in remaining:
        indegree[
          successor
        ] -= 1

  current_step_ids = tuple(
    sorted(
      visible_step_ids,
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
    return markdown

  visible_paragraph_indices = tuple(
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
    for proof_step_id in visible_step_ids
  }

  reordered = list(
    paragraphs
  )

  for paragraph_index, proof_step_id in zip(
    visible_paragraph_indices,
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


CALL_BLOCK = r'''  rendered = (
    order_toda_group_proof_narrative_visible_step_dependencies(
      presentation,
      rendered,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
'''


CALL_ANCHOR = r'''  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
'''


FUNCTION_ANCHOR = (
  "def order_toda_group_proof_narrative_visible_relation_dependencies(\n"
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

if (
  "def order_toda_group_proof_narrative_visible_step_dependencies(\n"
  not in source
):
  if FUNCTION_ANCHOR not in source:
    fail(
      "function insertion anchor not found"
    )

  source = source.replace(
    FUNCTION_ANCHOR,
    NEW_FUNCTION
    + FUNCTION_ANCHOR,
    1,
  )

render_tail = source.split(
  "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(",
  1,
)[-1]

if (
  "order_toda_group_proof_narrative_visible_step_dependencies(\n"
  not in render_tail
):
  if CALL_ANCHOR not in source:
    fail(
      "pipeline insertion anchor not found"
    )

  source = source.replace(
    CALL_ANCHOR,
    CALL_BLOCK
    + CALL_ANCHOR,
    1,
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
  "Applied Phase 159 pi3_2 visible dependency topological ordering."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
