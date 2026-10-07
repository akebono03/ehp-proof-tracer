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
SAFE_BACKUP = (
  REPO_ROOT
  / "phase159_pi3_2_visible_dependency_topological_order_repair2_backup"
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_SOURCE = (
  PACKAGE_DIR
  / "payload"
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
TEST_TARGET = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi3_2_visible_dependency_topological_order.py"
)
BACKUP_DIR = (
  REPO_ROOT
  / "phase159_pi3_2_visible_dependency_topological_order_repair5_backup"
)

FUNCTION_NAME = (
  "order_toda_group_proof_narrative_visible_step_dependencies"
)


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

  if (
    start > 0
    and source[
      start - 1
    ] != "\n"
  ):
    fail(
      "function marker is not at top level: "
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
    ].rstrip() + "\n"

  return source[
    start:
    next_def + 1
  ]


def replace_top_level_function(
  source: str,
  function_name: str,
  replacement: str,
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
      "current function not found: "
      + function_name
    )

  if (
    start > 0
    and source[
      start - 1
    ] != "\n"
  ):
    fail(
      "current function marker is not at top level: "
      + function_name
    )

  next_def = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    return (
      source[
        :start
      ]
      + replacement.rstrip()
      + "\n"
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      next_def + 1:
    ]
  )


if not TARGET.exists():
  fail(
    "target file not found: "
    + str(
      TARGET
    )
  )

if not SAFE_BACKUP.exists():
  fail(
    "repair2 backup not found: "
    + str(
      SAFE_BACKUP
    )
  )

if not TEST_SOURCE.exists():
  fail(
    "test payload not found: "
    + str(
      TEST_SOURCE
    )
  )

current_source = TARGET.read_text(
  encoding="utf-8",
)
safe_source = SAFE_BACKUP.read_text(
  encoding="utf-8",
)

safe_function = extract_top_level_function(
  safe_source,
  FUNCTION_NAME,
)

if (
  "preferred_ready_step_ids"
  in safe_function
):
  fail(
    "repair2 backup is not the expected repair1 stable function"
  )

if (
  "ready.sort("
  not in safe_function
):
  fail(
    "safe function does not contain stable ready.sort ordering"
  )

restored_source = replace_top_level_function(
  current_source,
  FUNCTION_NAME,
  safe_function,
)

BACKUP_DIR.mkdir(
  parents=True,
  exist_ok=True,
)

production_backup = (
  BACKUP_DIR
  / TARGET.name
)

if not production_backup.exists():
  shutil.copy2(
    TARGET,
    production_backup,
  )

test_backup = (
  BACKUP_DIR
  / TEST_TARGET.name
)

if (
  TEST_TARGET.exists()
  and not test_backup.exists()
):
  shutil.copy2(
    TEST_TARGET,
    test_backup,
  )

TARGET.write_text(
  restored_source,
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
  "Applied Phase 159 pi3_2 visible dependency ordering repair5."
)
print(
  "Restored function from repair2 backup "
  "(repair1 successful state)."
)
print(
  f"Production backup: {production_backup}"
)
print(
  f"Test: {TEST_TARGET}"
)
