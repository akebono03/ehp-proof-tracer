from __future__ import annotations

from pathlib import Path
import shutil
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_post_reference_locality_reapply.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_post_reference_locality_reapply.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_post_reference_locality_reapply_repair16_backup"
)
ANCHOR = '  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    prune_toda_group_proof_narrative_root_zero_direct_premise_references(\n      presentation,\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  reference_section = (\n'
REPLACEMENT = '  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    prune_toda_group_proof_narrative_root_zero_direct_premise_references(\n      presentation,\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  rendered = (\n    order_toda_group_proof_narrative_injective_image_order_reason(\n      rendered,\n      reason_sidecar,\n    )\n  )\n\n  reference_section = (\n'


def fail(
  message: str,
) -> None:
  print(
    "ERROR:",
    message,
    file=sys.stderr,
  )
  raise SystemExit(
    1
  )


def extract_top_level_function(
  source: str,
  function_name: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    fail(
      "function not found: "
      + function_name
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    return source[
      start:
    ]

  return source[
    start:
    next_def + 1
  ]


if not TARGET.exists():
  fail(
    "target file not found: "
    + str(
      TARGET
    )
  )

source = TARGET.read_text(
  encoding="utf-8",
)

if REPLACEMENT in source:
  updated = source
elif ANCHOR in source:
  updated = source.replace(
    ANCHOR,
    REPLACEMENT,
    1,
  )
else:
  fail(
    "post-reference locality anchor not found"
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
  updated,
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

changed_function = extract_top_level_function(
  updated,
  "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
)

changed_function_output = (
  PACKAGE_DIR
  / "patched_render_function_after_apply.py.txt"
)
changed_function_output.write_text(
  changed_function,
  encoding="utf-8",
)

print(
  "Applied Phase 159 pi3_2 post-reference locality re-apply repair16."
)
print(
  "Backup: "
  + str(
    backup_target
  )
)
print(
  "Test:   "
  + str(
    TEST_TARGET
  )
)
print(
  "Full changed function: "
  + str(
    changed_function_output
  )
)
