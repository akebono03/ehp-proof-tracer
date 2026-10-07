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
  / "phase159_pi3_2_visible_dependency_topological_order_repair2_backup"
)


OLD_LOOP = r'''  remaining = set(
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
'''


NEW_LOOP = r'''  remaining = set(
    visible_step_ids
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
      return markdown

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

if (
  "def order_toda_group_proof_narrative_visible_step_dependencies(\n"
  not in source
):
  fail(
    "Phase 159 visible-step ordering function not found"
  )

if OLD_LOOP not in source:
  if NEW_LOOP in source:
    print(
      "Repair2 ordering loop is already applied."
    )
  else:
    fail(
      "expected stable topological loop not found"
    )
else:
  source = source.replace(
    OLD_LOOP,
    NEW_LOOP,
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
  "Applied Phase 159 pi3_2 visible dependency ordering repair2."
)
print(
  f"Backup: {backup_target}"
)
print(
  f"Test:   {TEST_TARGET}"
)
