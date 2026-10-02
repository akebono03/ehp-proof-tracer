from __future__ import annotations

import argparse
from pathlib import Path


START = "# PHASE155_AUDIT_BOUNDARY_START"
END = "# PHASE155_AUDIT_BOUNDARY_END"


BLOCK = r'''
# PHASE155_AUDIT_BOUNDARY_START

PHASE155_AUDIT_ONLY_NODEIDS_PATH = (
    TESTS_DIR
    / "phase155_audit_only_nodeids.txt"
)

PHASE155_AUDIT_ONLY_NODEIDS = frozenset(
    line.strip()
    for line in PHASE155_AUDIT_ONLY_NODEIDS_PATH.read_text(
        encoding="utf-8",
    ).splitlines()
    if line.strip()
)


def pytest_addoption(parser):
    parser.addoption(
        "--include-phase155-audits",
        action="store_true",
        default=False,
        help=(
            "include Phase155 historical audit-only tests "
            "in normal collection"
        ),
    )


def pytest_collection_modifyitems(
    config,
    items,
):
    if config.getoption(
        "--include-phase155-audits"
    ):
        return

    retained = []
    deselected = []

    for item in items:
        normalized_nodeid = item.nodeid.replace(
            "\\\\",
            "/",
        )

        if (
            normalized_nodeid
            in PHASE155_AUDIT_ONLY_NODEIDS
        ):
            deselected.append(
                item
            )
        else:
            retained.append(
                item
            )

    if deselected:
        config.hook.pytest_deselected(
            items=deselected
        )

    items[:] = retained

# PHASE155_AUDIT_BOUNDARY_END
'''.strip()


BOUNDARY_TEST = r'''from pathlib import Path


TESTS_DIR = Path(
  __file__
).resolve().parent


def _phase155_audit_nodeids():
  path = (
    TESTS_DIR
    / "phase155_audit_only_nodeids.txt"
  )

  return tuple(
    line.strip()
    for line in path.read_text(
      encoding="utf-8",
    ).splitlines()
    if line.strip()
  )


def test_phase155_audit_boundary_has_23_unique_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert len(
    nodeids
  ) == 23
  assert len(
    set(
      nodeids
    )
  ) == 23


def test_phase155_audit_boundary_contains_only_phase144_tests():
  nodeids = _phase155_audit_nodeids()

  assert all(
    nodeid.startswith(
      "tests/test_phase144_"
    )
    for nodeid in nodeids
  )


def test_phase155_audit_boundary_keeps_function_level_nodeids():
  nodeids = _phase155_audit_nodeids()

  assert all(
    "::test_"
    in nodeid
    for nodeid in nodeids
  )
'''


def _read_lane(
    path: Path,
) -> tuple[str, ...]:
    if not path.exists():
        raise SystemExit(
            "Required R2B lane file not found: "
            + str(
                path
            )
        )

    return tuple(
        line.strip()
        for line in path.read_text(
            encoding="utf-8",
        ).splitlines()
        if line.strip()
    )


def _install_block(
    conftest_path: Path,
) -> None:
    source = conftest_path.read_text(
        encoding="utf-8-sig"
    )

    if START in source:
        before, rest = source.split(
            START,
            1,
        )
        if END not in rest:
            raise SystemExit(
                "Existing Phase155 audit boundary "
                "start marker has no end marker."
            )
        _old, after = rest.split(
            END,
            1,
        )
        source = (
            before.rstrip()
            + "\n\n"
            + after.lstrip(
                "\r\n"
            )
        )

    updated = (
        source.rstrip()
        + "\n\n"
        + BLOCK
        + "\n"
    )

    conftest_path.write_text(
        updated,
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    tests_dir = repo_root / "tests"

    r2b_dir = (
        repo_root
        / "phase155_closure_r2b_output"
    )

    audit_only = _read_lane(
        r2b_dir
        / "lane_audit_only.txt"
    )
    split_or_cache = _read_lane(
        r2b_dir
        / "lane_split_or_cache.txt"
    )

    if len(
        audit_only
    ) != 22:
        raise SystemExit(
            "Expected 22 AUDIT_ONLY nodeids; "
            f"found {len(audit_only)}"
        )

    if len(
        split_or_cache
    ) != 1:
        raise SystemExit(
            "Expected 1 SPLIT_OR_CACHE nodeid; "
            f"found {len(split_or_cache)}"
        )

    combined = tuple(
        dict.fromkeys(
            (
                *audit_only,
                *split_or_cache,
            )
        )
    )

    if len(
        combined
    ) != 23:
        raise SystemExit(
            "Expected 23 unique historical heavy "
            f"nodeids; found {len(combined)}"
        )

    if not all(
        nodeid.startswith(
            "tests/test_phase144_"
        )
        for nodeid in combined
    ):
        raise SystemExit(
            "Audit boundary contains non-Phase144 nodeid."
        )

    manifest_path = (
        tests_dir
        / "phase155_audit_only_nodeids.txt"
    )
    manifest_path.write_text(
        "".join(
            nodeid
            + "\n"
            for nodeid in combined
        ),
        encoding="utf-8",
    )

    conftest_path = tests_dir / "conftest.py"
    _install_block(
        conftest_path
    )

    boundary_test_path = (
        tests_dir
        / "test_phase155_audit_boundary.py"
    )
    boundary_test_path.write_text(
        BOUNDARY_TEST,
        encoding="utf-8",
    )

    print(
        "Phase 155 audit-only boundary installed."
    )
    print(
        "AUDIT_ONLY source nodeids:",
        len(
            audit_only
        ),
    )
    print(
        "SPLIT_OR_CACHE promoted to audit-only:",
        len(
            split_or_cache
        ),
    )
    print(
        "Default-deselected nodeids:",
        len(
            combined
        ),
    )
    print(
        "Production changes: none"
    )
    print(
        "Existing Phase144 test bodies changed: none"
    )
    print(
        "Import changes: none"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
