from __future__ import annotations

import sys
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

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
