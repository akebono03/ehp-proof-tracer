from __future__ import annotations

import json
from pathlib import Path

import pytest


def pytest_addoption(parser):
  group = parser.getgroup(
    "phase155-sharding"
  )
  group.addoption(
    "--phase155-shard-plan",
    action="store",
    default=None,
    help="Path to the Phase155 shard plan JSON.",
  )
  group.addoption(
    "--phase155-shard-index",
    action="store",
    type=int,
    default=None,
    help="1-based shard index to select.",
  )


def _repo_root(config) -> Path:
  return Path(
    str(
      config.rootpath
    )
  ).resolve()


def _audit_only_nodeids(config) -> set[str]:
  path = (
    _repo_root(
      config
    )
    / "tests"
    / "phase155_audit_only_nodeids.txt"
  )

  if not path.exists():
    raise pytest.UsageError(
      "Phase155 audit-only manifest not found: "
      + str(
        path
      )
    )

  return {
    line.strip()
    for line in path.read_text(
      encoding="utf-8"
    ).splitlines()
    if line.strip()
  }


def _load_plan(
  config,
) -> dict:
  raw = config.getoption(
    "--phase155-shard-plan"
  )

  if raw is None:
    return {}

  path = Path(
    raw
  ).resolve()

  if not path.exists():
    raise pytest.UsageError(
      "Phase155 shard plan not found: "
      + str(
        path
      )
    )

  return json.loads(
    path.read_text(
      encoding="utf-8"
    )
  )


def _file_nodeid(
  nodeid: str,
) -> str:
  return nodeid.split(
    "::",
    1,
  )[0].replace(
    "\\",
    "/",
  )


def pytest_collection_modifyitems(
  config,
  items,
):
  audit_only = _audit_only_nodeids(
    config
  )

  routine = []
  deselected = []

  for item in items:
    if item.nodeid in audit_only:
      deselected.append(
        item
      )
    else:
      routine.append(
        item
      )

  if deselected:
    config.hook.pytest_deselected(
      items=deselected
    )

  items[:] = routine

  shard_index = config.getoption(
    "--phase155-shard-index"
  )
  plan_path = config.getoption(
    "--phase155-shard-plan"
  )

  if (
    shard_index is None
    and plan_path is None
  ):
    return

  if (
    shard_index is None
    or plan_path is None
  ):
    raise pytest.UsageError(
      "--phase155-shard-plan and "
      "--phase155-shard-index must be used together."
    )

  plan = _load_plan(
    config
  )
  shard_count = int(
    plan[
      "shard_count"
    ]
  )

  if not (
    1
    <= shard_index
    <= shard_count
  ):
    raise pytest.UsageError(
      "Shard index must be between 1 and "
      + str(
        shard_count
      )
    )

  file_to_shard = {
    key.replace(
      "\\",
      "/",
    ): int(
      value
    )
    for key, value in plan[
      "file_to_shard"
    ].items()
  }

  selected = []
  shard_deselected = []

  for item in items:
    file_nodeid = _file_nodeid(
      item.nodeid
    )
    assigned = file_to_shard.get(
      file_nodeid
    )

    if assigned is None:
      raise pytest.UsageError(
        "Collected test file is missing "
        "from shard plan: "
        + file_nodeid
      )

    if assigned == shard_index:
      selected.append(
        item
      )
    else:
      shard_deselected.append(
        item
      )

  if shard_deselected:
    config.hook.pytest_deselected(
      items=shard_deselected
    )

  items[:] = selected
