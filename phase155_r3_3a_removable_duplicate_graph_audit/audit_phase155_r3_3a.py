from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DECISION_REMOVABLE = "removable_duplicate"
DECISION_RETAIN = "retain_independent"
DECISION_HISTORICAL = "historical_keep"
DECISION_REVIEW = "needs_review"


@dataclass(frozen=True)
class ComponentRecord:
    component_id: str
    node_count: int
    edge_count: int
    nodes: str
    protected_historical_nodes: str
    natural_sink_nodes: str
    canonical_survivor: str
    cycle_present: bool
    deletion_candidate_count: int
    deletion_candidates: str
    needs_manual_review: bool
    reason: str


@dataclass(frozen=True)
class NodeRecord:
    component_id: str
    test_id: str
    incoming_removable_edges: int
    outgoing_removable_edges: int
    historical_protected: bool
    natural_sink: bool
    canonical_survivor: bool
    deletion_candidate: bool
    phase_number: int
    reason: str


def _git_head(
    repo_root: Path,
) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        return "unavailable"


def _read_csv(
    path: Path,
) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(
                handle
            )
        )


def _write_csv(
    path: Path,
    rows: Iterable[object],
) -> None:
    rows = list(
        rows
    )

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(
        asdict(
            rows[
                0
            ]
        ).keys()
    )

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(
                asdict(
                    row
                )
            )


def _phase_number(
    test_id: str,
) -> int:
    match = re.search(
        r"test_phase(\d+)",
        test_id,
    )

    if match is None:
        return -1

    return int(
        match.group(
            1
        )
    )


def _canonical_key(
    test_id: str,
) -> tuple[
    int,
    str,
]:
    return (
        _phase_number(
            test_id
        ),
        test_id,
    )


def _component_nodes(
    removable_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> list[
    set[
        str
    ]
]:
    adjacency: dict[
        str,
        set[
            str
        ],
    ] = defaultdict(
        set
    )

    for row in removable_rows:
        older = row[
            "older_test_id"
        ]
        newer = row[
            "newer_test_id"
        ]
        adjacency[
            older
        ].add(
            newer
        )
        adjacency[
            newer
        ].add(
            older
        )

    visited = set()
    result = []

    for start in sorted(
        adjacency
    ):
        if start in visited:
            continue

        queue = deque(
            [
                start
            ]
        )
        component = set()
        visited.add(
            start
        )

        while queue:
            current = (
                queue.popleft()
            )
            component.add(
                current
            )

            for neighbor in adjacency[
                current
            ]:
                if neighbor in visited:
                    continue
                visited.add(
                    neighbor
                )
                queue.append(
                    neighbor
                )

        result.append(
            component
        )

    return result


def _has_directed_cycle(
    nodes: set[
        str
    ],
    outgoing: dict[
        str,
        set[
            str
        ],
    ],
) -> bool:
    state: dict[
        str,
        int
    ] = {}

    def visit(
        node: str,
    ) -> bool:
        node_state = state.get(
            node,
            0,
        )

        if node_state == 1:
            return True

        if node_state == 2:
            return False

        state[
            node
        ] = 1

        for target in outgoing.get(
            node,
            set(),
        ):
            if (
                target in nodes
                and visit(
                    target
                )
            ):
                return True

        state[
            node
        ] = 2
        return False

    return any(
        visit(
            node
        )
        for node in sorted(
            nodes
        )
        if state.get(
            node,
            0,
        )
        == 0
    )


def _reachable_survivor(
    start: str,
    survivors: set[
        str
    ],
    outgoing: dict[
        str,
        set[
            str
        ],
    ],
) -> bool:
    queue = deque(
        [
            start
        ]
    )
    visited = {
        start
    }

    while queue:
        current = (
            queue.popleft()
        )

        for target in outgoing.get(
            current,
            set(),
        ):
            if target in survivors:
                return True

            if target in visited:
                continue

            visited.add(
                target
            )
            queue.append(
                target
            )

    return False


def build_graph_audit(
    rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> tuple[
    list[
        ComponentRecord
    ],
    list[
        NodeRecord
    ],
]:
    review_rows = [
        row
        for row in rows
        if row.get(
            "decision"
        )
        == DECISION_REVIEW
    ]

    if review_rows:
        raise ValueError(
            "R3-3A requires R3-2 closure with needs_review = 0"
        )

    removable_rows = [
        row
        for row in rows
        if (
            row.get(
                "decision"
            )
            == DECISION_REMOVABLE
            and row.get(
                "deletion_authorized",
                "",
            ).lower()
            in (
                "true",
                "1",
                "yes",
            )
        )
    ]

    protected = {
        test_id
        for row in rows
        if row.get(
            "decision"
        )
        == DECISION_HISTORICAL
        for test_id in (
            row[
                "older_test_id"
            ],
            row[
                "newer_test_id"
            ],
        )
    }

    outgoing: dict[
        str,
        set[
            str
        ],
    ] = defaultdict(
        set
    )
    incoming: dict[
        str,
        set[
            str
        ],
    ] = defaultdict(
        set
    )

    for row in removable_rows:
        older = row[
            "older_test_id"
        ]
        newer = row[
            "newer_test_id"
        ]
        outgoing[
            older
        ].add(
            newer
        )
        incoming[
            newer
        ].add(
            older
        )

    components = (
        _component_nodes(
            removable_rows
        )
    )
    component_records = []
    node_records = []

    for index, nodes in enumerate(
        components,
        start=1,
    ):
        component_id = (
            "C"
            + str(
                index
            ).zfill(
                3
            )
        )
        component_edges = [
            row
            for row in removable_rows
            if (
                row[
                    "older_test_id"
                ]
                in nodes
                and row[
                    "newer_test_id"
                ]
                in nodes
            )
        ]
        protected_nodes = (
            nodes
            & protected
        )
        natural_sinks = {
            node
            for node in nodes
            if not (
                outgoing.get(
                    node,
                    set(),
                )
                & nodes
            )
        }
        cycle_present = (
            _has_directed_cycle(
                nodes,
                outgoing,
            )
        )

        preferred_survivors = (
            protected_nodes
            or natural_sinks
        )

        if preferred_survivors:
            canonical = max(
                preferred_survivors,
                key=_canonical_key,
            )
        else:
            canonical = max(
                nodes,
                key=_canonical_key,
            )

        mandatory_survivors = set(
            protected_nodes
        )

        if natural_sinks:
            mandatory_survivors.update(
                natural_sinks
            )

        if not mandatory_survivors:
            mandatory_survivors.add(
                canonical
            )

        deletion_candidates = set()

        for node in nodes:
            if node in mandatory_survivors:
                continue

            if node in protected:
                continue

            if _reachable_survivor(
                node,
                mandatory_survivors,
                outgoing,
            ):
                deletion_candidates.add(
                    node
                )

        unresolved_nodes = (
            nodes
            - mandatory_survivors
            - deletion_candidates
        )

        needs_manual_review = bool(
            unresolved_nodes
        )

        if needs_manual_review:
            reason = (
                "At least one node cannot reach a protected or sink survivor "
                "through authorized older-to-newer removable edges."
            )
        elif cycle_present:
            reason = (
                "Directed cycle exists, but every non-survivor still reaches "
                "an authorized survivor after survivor protection."
            )
        elif protected_nodes:
            reason = (
                "Historical-protected nodes are retained; all other authorized "
                "older nodes reach a retained survivor."
            )
        else:
            reason = (
                "All deletion candidates reach a natural newer-side sink "
                "through authorized removable edges."
            )

        component_records.append(
            ComponentRecord(
                component_id=(
                    component_id
                ),
                node_count=len(
                    nodes
                ),
                edge_count=len(
                    component_edges
                ),
                nodes="\x1f".join(
                    sorted(
                        nodes
                    )
                ),
                protected_historical_nodes=(
                    "\x1f".join(
                        sorted(
                            protected_nodes
                        )
                    )
                ),
                natural_sink_nodes=(
                    "\x1f".join(
                        sorted(
                            natural_sinks
                        )
                    )
                ),
                canonical_survivor=(
                    canonical
                ),
                cycle_present=(
                    cycle_present
                ),
                deletion_candidate_count=len(
                    deletion_candidates
                ),
                deletion_candidates=(
                    "\x1f".join(
                        sorted(
                            deletion_candidates
                        )
                    )
                ),
                needs_manual_review=(
                    needs_manual_review
                ),
                reason=reason,
            )
        )

        for node in sorted(
            nodes
        ):
            is_sink = (
                node in natural_sinks
            )
            is_canonical = (
                node
                == canonical
            )
            is_deletion = (
                node
                in deletion_candidates
            )

            if node in protected:
                node_reason = (
                    "historical_keep protection"
                )
            elif is_sink:
                node_reason = (
                    "natural newer-side survivor"
                )
            elif is_canonical:
                node_reason = (
                    "canonical survivor"
                )
            elif is_deletion:
                node_reason = (
                    "authorized older-side duplicate reaches survivor"
                )
            else:
                node_reason = (
                    "not proven deletable by directed coverage"
                )

            node_records.append(
                NodeRecord(
                    component_id=(
                        component_id
                    ),
                    test_id=node,
                    incoming_removable_edges=len(
                        incoming.get(
                            node,
                            set(),
                        )
                        & nodes
                    ),
                    outgoing_removable_edges=len(
                        outgoing.get(
                            node,
                            set(),
                        )
                        & nodes
                    ),
                    historical_protected=(
                        node
                        in protected
                    ),
                    natural_sink=(
                        is_sink
                    ),
                    canonical_survivor=(
                        is_canonical
                    ),
                    deletion_candidate=(
                        is_deletion
                    ),
                    phase_number=(
                        _phase_number(
                            node
                        )
                    ),
                    reason=(
                        node_reason
                    ),
                )
            )

    return (
        component_records,
        node_records,
    )


def write_summary(
    path: Path,
    repo_root: Path,
    all_rows: list[
        dict[
            str,
            str,
        ]
    ],
    components: list[
        ComponentRecord
    ],
    nodes: list[
        NodeRecord
    ],
) -> None:
    decision_counts = Counter(
        row.get(
            "decision",
            "",
        )
        for row in all_rows
    )
    deletion_nodes = {
        row.test_id
        for row in nodes
        if row.deletion_candidate
    }
    survivor_nodes = {
        row.test_id
        for row in nodes
        if (
            row.natural_sink
            or row.historical_protected
            or row.canonical_survivor
        )
    }
    cycles = sum(
        row.cycle_present
        for row in components
    )
    review_components = sum(
        row.needs_manual_review
        for row in components
    )

    lines = [
        "# Phase 155-R3-3A — removable duplicate graph and canonical survivor audit",
        "",
        "## Input",
        "",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Verified candidate pairs: {len(all_rows)}",
        f"- Removable duplicate pairs: {decision_counts[DECISION_REMOVABLE]}",
        f"- Retain-independent pairs: {decision_counts[DECISION_RETAIN]}",
        f"- Historical-keep pairs: {decision_counts[DECISION_HISTORICAL]}",
        f"- Needs-review pairs: {decision_counts[DECISION_REVIEW]}",
        "",
        "## Graph result",
        "",
        f"- Removable connected components: {len(components)}",
        f"- Unique tests in removable graph: {len(nodes)}",
        f"- Unique deletion candidates: {len(deletion_nodes)}",
        f"- Survivor/protected tests: {len(survivor_nodes)}",
        f"- Components containing directed cycles: {cycles}",
        f"- Components needing manual review: {review_components}",
        "",
        "## Safety rule",
        "",
        "An older-side test becomes a deletion candidate only when it can reach a protected or natural newer-side survivor through one or more R3-2F-r1 `deletion_authorized=true` edges.",
        "",
        "Tests participating in `historical_keep` pairs are protected from deletion.",
        "",
        "R3-3A performs no deletion. File-level helper/import dependencies must still be audited before R3-3B changes existing test files.",
        "",
        "Repository-wide pytest remains deferred until Phase 155 closure.",
    ]

    path.write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--verified-pairs",
        type=Path,
        default=Path(
            "phase155_r3_2f_r1_audit_output/"
            "phase155_r3_2f_r1_verified_pairs.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3a_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = (
        args.repo_root.resolve()
    )

    verified_path = (
        args.verified_pairs
        if args.verified_pairs.is_absolute()
        else repo_root
        / args.verified_pairs
    )

    if not verified_path.exists():
        raise SystemExit(
            "R3-2F-r1 verified-pairs CSV not found: "
            + str(
                verified_path
            )
        )

    rows = _read_csv(
        verified_path
    )

    components, nodes = (
        build_graph_audit(
            rows
        )
    )

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_csv(
        output_dir
        / "phase155_r3_3a_components.csv",
        components,
    )
    _write_csv(
        output_dir
        / "phase155_r3_3a_nodes.csv",
        nodes,
    )

    deletion_candidates = [
        row
        for row in nodes
        if row.deletion_candidate
    ]
    _write_csv(
        output_dir
        / "phase155_r3_3a_deletion_candidates.csv",
        deletion_candidates,
    )

    write_summary(
        output_dir
        / "phase155_r3_3a_summary.md",
        repo_root,
        rows,
        components,
        nodes,
    )

    counts = Counter(
        row.get(
            "decision",
            "",
        )
        for row in rows
    )
    review_components = sum(
        row.needs_manual_review
        for row in components
    )
    cycles = sum(
        row.cycle_present
        for row in components
    )

    metadata = {
        "phase": "155-R3-3A",
        "git_head": _git_head(
            repo_root
        ),
        "verified_candidate_pairs": len(
            rows
        ),
        "removable_pairs": counts[
            DECISION_REMOVABLE
        ],
        "connected_components": len(
            components
        ),
        "unique_graph_tests": len(
            nodes
        ),
        "unique_deletion_candidates": len(
            deletion_candidates
        ),
        "cycle_components": cycles,
        "manual_review_components": (
            review_components
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3a_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-3A removable duplicate graph audit completed."
    )
    print(
        "verified candidate pairs:",
        len(
            rows
        ),
    )
    print(
        "removable pairs:",
        counts[
            DECISION_REMOVABLE
        ],
    )
    print(
        "connected components:",
        len(
            components
        ),
    )
    print(
        "unique tests in removable graph:",
        len(
            nodes
        ),
    )
    print(
        "unique deletion candidates:",
        len(
            deletion_candidates
        ),
    )
    print(
        "cycle components:",
        cycles,
    )
    print(
        "manual-review components:",
        review_components,
    )
    print(
        "output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
