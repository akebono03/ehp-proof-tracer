from __future__ import annotations

import gc
import importlib
import sys
import time
import traceback
from pathlib import Path

ROOT = Path.cwd()
TESTS = ROOT / "tests"
OUT = ROOT / "phase150_performance_diagnostic_r2_output"
OUT.mkdir(exist_ok=True)
REPORT = OUT / "REPORT.txt"
DETAIL = OUT / "timing_detail.txt"

# The Phase 144-6 audit modules intentionally import helper modules from tests/
# by their top-level module names. pytest makes that import layout available
# during test execution. This standalone diagnostic must reproduce it.
for path in (ROOT, TESTS):
    path_text = str(path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

TARGETS = (
    ("r5_37", "audit_phase144_6_r5_37", "build_semantic_equivalence_and_rendering_inventory"),
    ("r5_38_occurrences", "audit_phase144_6_r5_38", "build_visibility_occurrences"),
    ("r5_38_groups", "audit_phase144_6_r5_38", "build_explanatory_contribution_groups"),
    ("r5_39", "audit_phase144_6_r5_39", "build_narrative_necessity_inventory"),
    ("r5_40", "audit_phase144_6_r5_40", "build_placement_inventory"),
    ("r5_41", "audit_phase144_6_r5_41", "build_topological_order_audit"),
)


def timed(label, func):
    gc.collect()
    started = time.perf_counter()
    value = func()
    elapsed = time.perf_counter() - started
    try:
        size = len(value)
    except TypeError:
        size = None
    return label, elapsed, size


def load_targets():
    loaded = []
    for label, module_name, function_name in TARGETS:
        module = importlib.import_module(module_name)
        loaded.append((label, getattr(module, function_name)))
    return loaded


def main() -> int:
    lines = []
    lines.append("Phase 150 Performance Diagnostic R2 Repair")
    lines.append("=" * 72)
    lines.append("Production changes: none")
    lines.append("Existing test changes: none")
    lines.append("Documentation changes: none")
    lines.append("Full regression: NOT run")
    lines.append(f"Repository root: {ROOT}")
    lines.append(f"Tests import path: {TESTS}")
    lines.append("")

    try:
        targets = load_targets()
    except Exception:
        REPORT.write_text(
            "\n".join(lines) + "\nIMPORT FAILURE\n" + traceback.format_exc(),
            encoding="utf-8",
        )
        print(REPORT.read_text(encoding="utf-8"))
        return 2

    results = []

    lines.append("A. First sequential pass")
    lines.append("-" * 72)
    for label, func in targets:
        try:
            row = timed(label, func)
        except Exception:
            lines.append(f"{label}: ERROR")
            lines.append(traceback.format_exc())
            REPORT.write_text("\n".join(lines), encoding="utf-8")
            print("\n".join(lines))
            return 3
        results.append(("pass1",) + row)
        lines.append(f"{label}: {row[1]:.3f}s size={row[2]}")

    lines.append("")
    lines.append("B. Immediate second pass in the same Python process")
    lines.append("-" * 72)
    for label, func in targets:
        try:
            row = timed(label, func)
        except Exception:
            lines.append(f"{label}: ERROR")
            lines.append(traceback.format_exc())
            REPORT.write_text("\n".join(lines), encoding="utf-8")
            print("\n".join(lines))
            return 4
        results.append(("pass2",) + row)
        lines.append(f"{label}: {row[1]:.3f}s size={row[2]}")

    first = {label: elapsed for phase, label, elapsed, _ in results if phase == "pass1"}
    second = {label: elapsed for phase, label, elapsed, _ in results if phase == "pass2"}

    lines.append("")
    lines.append("C. Repeated-builder ratios")
    lines.append("-" * 72)
    for label, _, _ in TARGETS:
        a = first[label]
        b = second[label]
        ratio = (b / a) if a else 0.0
        lines.append(
            f"{label}: pass1={a:.3f}s pass2={b:.3f}s "
            f"pass2/pass1={ratio:.3f}"
        )

    lines.append("")
    lines.append("D. Structural findings from current source")
    lines.append("-" * 72)
    lines.append(
        "r5_37 tests call build_semantic_equivalence_and_rendering_inventory() "
        "independently in each test; there is no module-scoped fixture in that test file."
    )
    lines.append(
        "r5_38-r5_41 use module-scoped pytest fixtures, but their audit builders "
        "form a dependency chain that independently rebuilds visibility occurrences "
        "and/or six-group _context() data."
    )
    lines.append(
        "This diagnostic intentionally does not cache or patch any builder. "
        "It measures the current behavior only."
    )

    DETAIL.write_text(
        "\n".join(
            f"{phase}\t{label}\t{elapsed:.6f}\t{size}"
            for phase, label, elapsed, size in results
        ) + "\n",
        encoding="utf-8",
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT.read_text(encoding="utf-8"))
    print(f"Detail: {DETAIL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
