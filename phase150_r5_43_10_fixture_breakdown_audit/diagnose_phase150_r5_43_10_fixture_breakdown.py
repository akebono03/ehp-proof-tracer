from __future__ import annotations

import gc
import time
from pathlib import Path

from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
    TARGETS,
    _context,
)
from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_ordering import (
    build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_contribution_renderer import (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)


OUTPUT = Path("phase150_r5_43_10_fixture_breakdown_audit.txt")


def write(line: str) -> None:
    print(line, flush=True)
    with OUTPUT.open("a", encoding="utf-8", buffering=1) as handle:
        handle.write(line + "\n")
        handle.flush()


def measure(label, function):
    write(f"START {label}")
    started = time.perf_counter()
    value = function()
    elapsed = time.perf_counter() - started
    write(f"END   {label} elapsed={elapsed:.2f}s")
    return value, elapsed


def main() -> int:
    OUTPUT.write_text(
        "Phase 150 R5-43-10 Fixture Breakdown Audit\n"
        "Production changes: none\n"
        "Existing test changes: none\n"
        "Full regression: NOT run\n"
        + "=" * 100
        + "\n",
        encoding="utf-8",
    )

    totals = {
        "context": 0.0,
        "base": 0.0,
        "ordered": 0.0,
        "connected": 0.0,
    }

    for n, k in TARGETS:
        target = f"pi_{n + k}^{n}"
        write("=" * 100)
        write(f"TARGET n={n} k={k} {target}")

        context, elapsed = measure(
            f"{target} context",
            lambda n=n, k=k: _context(n, k),
        )
        totals["context"] += elapsed

        (
            presentation,
            semantic_sidecar,
            blocks,
            arguments,
            aggregate_semantic_sidecar,
            proof_chains,
        ) = context

        base, elapsed = measure(
            f"{target} base",
            lambda: render_toda_group_proof_narrative_multi_argument_markdown(
                presentation,
                blocks,
                semantic_sidecar,
                arguments,
            ),
        )
        totals["base"] += elapsed
        write(f"INFO  {target} base_chars={len(base)}")

        ordered, elapsed = measure(
            f"{target} ordered",
            lambda: build_toda_group_proof_narrative_ordered_contributions(
                presentation,
                blocks,
                semantic_sidecar,
                arguments,
                proof_chains,
                current_markdown=base,
            ),
        )
        totals["ordered"] += elapsed
        contribution_count = sum(len(rows) for rows in ordered)
        write(
            f"INFO  {target} ordered_arguments={len(ordered)} "
            f"contributions={contribution_count}"
        )

        connected, elapsed = measure(
            f"{target} connected",
            lambda: render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
                presentation,
                blocks,
                semantic_sidecar,
                arguments,
            ),
        )
        totals["connected"] += elapsed
        write(f"INFO  {target} connected_chars={len(connected)}")

        del connected
        del ordered
        del base
        del context
        gc.collect()

    write("=" * 100)
    write("TOTALS")
    for name in ("context", "base", "ordered", "connected"):
        write(f"{name}={totals[name]:.2f}s")
    write(f"all={sum(totals.values()):.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
