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
  / "phase159_pi3_2_visible_dependency_topological_order_repair1_backup"
)


NEW_FUNCTION = r'''def normalize_toda_group_proof_narrative_zero_map_exactness_reason(
  presentation: TodaGroupProofPresentation,
  markdown: str,
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

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    for prefix in (
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
      "完全性より, ",
    ):
      if stripped.startswith(
        prefix
      ):
        stripped = stripped[
          len(
            prefix
          ):
        ]
        break

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  for node in presentation.nodes:
    zero_step = node.proof_step
    zero_line = (
      _render_generic_narrative_step(
        zero_step
      )
    )

    if (
      not zero_line
      or "は零写像である."
      not in zero_line
    ):
      continue

    exactness_premises = tuple(
      premise
      for premise in zero_step.premises
      if classify_toda_proof_step_role(
        premise
      )
      in (
        TodaProofDependencyRole.EHP_EXACTNESS,
        TodaProofDependencyRole.EHP_WINDOW,
      )
    )
    injective_premises = tuple(
      premise
      for premise in zero_step.premises
      if (
        classify_toda_proof_step_role(
          premise
        )
        is TodaProofDependencyRole.MAP_PROPERTY
        and "は単射である."
        in (
          _render_generic_narrative_step(
            premise
          )
          or ""
        )
      )
    )

    if (
      len(
        exactness_premises
      )
      != 1
      or len(
        injective_premises
      )
      != 1
    ):
      continue

    target_key = paragraph_match_key(
      zero_line
    )
    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matching_indices
    ) != 1:
      continue

    paragraph_index = matching_indices[
      0
    ]
    paragraph = paragraphs[
      paragraph_index
    ]
    stripped = paragraph.strip()

    if stripped.startswith(
      "完全性より, "
    ):
      continue

    leading_length = (
      len(
        paragraph
      )
      - len(
        paragraph.lstrip()
      )
    )
    leading = paragraph[
      :leading_length
    ]

    paragraphs[
      paragraph_index
    ] = (
      leading
      + "完全性より, "
      + stripped
    )

  return "\n\n".join(
    paragraphs
  )


'''


FUNCTION_ANCHOR = (
  "def order_toda_group_proof_narrative_visible_step_dependencies(\n"
)

CALL_ANCHOR = r'''  rendered = (
    order_toda_group_proof_narrative_visible_step_dependencies(
      presentation,
      rendered,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
'''

CALL_BLOCK = r'''  rendered = (
    normalize_toda_group_proof_narrative_zero_map_exactness_reason(
      presentation,
      rendered,
    )
  )
'''


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

if FUNCTION_ANCHOR not in source:
  fail(
    "previous Phase 159 visible-step ordering implementation not found"
  )

if (
  "def normalize_toda_group_proof_narrative_zero_map_exactness_reason(\n"
  not in source
):
  source = source.replace(
    FUNCTION_ANCHOR,
    NEW_FUNCTION
    + FUNCTION_ANCHOR,
    1,
  )

if CALL_ANCHOR not in source:
  fail(
    "visible-step ordering pipeline call not found"
  )

render_tail = source.split(
  "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(",
  1,
)[-1]

if (
  "normalize_toda_group_proof_narrative_zero_map_exactness_reason(\n"
  not in render_tail
):
  source = source.replace(
    CALL_ANCHOR,
    CALL_ANCHOR
    + CALL_BLOCK,
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
  "Applied Phase 159 pi3_2 visible dependency ordering repair1."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
