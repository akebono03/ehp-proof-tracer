"""R53: guarded, minimal public-zero-group provider integration.

Replaces one complete existing function with a checked copy that wraps its
already screened provider. The independent R35 mathematical rule is unchanged.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    ROOT, TARGET, git_bytes, normalized, verify_checkout,
)

PACKAGE = Path(__file__).resolve().parent
OLD_ANCHOR = (
    "        if context_sink is not None:\n"
    "            context_sink(screened)\n"
    "        return search_registered_partial_proof(\n"
)
NEW_ANCHOR = (
    "        if context_sink is not None:\n"
    "            context_sink(screened)\n"
    "        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (\n"
    "            build_public_source_bound_kernel_provider,\n"
    "        )\n"
    "        provider = build_public_source_bound_kernel_provider(provider, screened)\n"
    "        return search_registered_partial_proof(\n"
)


def function_source(source: str, function: str) -> str:
    """Extract a whole top-level definition, not a few patch lines."""
    parsed = ast.parse(source)
    matches = tuple(
        item for item in parsed.body
        if isinstance(item, ast.FunctionDef) and item.name == function
    )
    if len(matches) != 1:
        raise RuntimeError("Expected one callable to replace: " + function)
    lines = source.splitlines(keepends=True)
    return "".join(lines[matches[0].lineno - 1:matches[0].end_lineno])


def patched_source(original: str) -> str:
    """Only change the exact public zero-group search branch, once."""
    current_function = function_source(original, "search_group_from_registered_goal")
    if OLD_ANCHOR in current_function and NEW_ANCHOR not in current_function:
        if current_function.count(OLD_ANCHOR) != 1:
            raise RuntimeError("R53 public zero-branch anchor was repeated")
        replacement = current_function.replace(OLD_ANCHOR, NEW_ANCHOR)
        if original.count(current_function) != 1:
            raise RuntimeError("R53 source has a nonunique function")
        updated = original.replace(current_function, replacement, 1)
    elif NEW_ANCHOR in current_function and OLD_ANCHOR not in current_function:
        updated = original
    else:
        raise RuntimeError("Unreviewed public search hook shape")
    # The ZIP carries the entire expected replacement, not an abbreviated diff.
    expected = (PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8")
    observed = function_source(updated, "search_group_from_registered_goal")
    if ast.dump(ast.parse(observed), include_attributes=False) != ast.dump(
        ast.parse(expected), include_attributes=False
    ):
        raise RuntimeError("R53 complete function differs from the reviewed replacement")
    if updated.count("build_public_source_bound_kernel_provider(provider, screened)") != 1:
        raise RuntimeError("R53 wrapper was not inserted exactly once")
    return updated


def prepare() -> tuple[bytes, str, str]:
    """Check the exact committed file and one safe idempotent replacement."""
    baseline = git_bytes("show", "HEAD:" + TARGET)
    old = normalized(baseline).decode("utf-8-sig")
    updated = patched_source(old)
    working_bytes = (ROOT / TARGET).read_bytes()
    working = normalized(working_bytes).decode("utf-8-sig")
    if working not in (old, updated):
        raise RuntimeError("Unreviewed public group search working source")
    return working_bytes, old, updated


def apply(*, dry_run: bool) -> dict[str, object]:
    """Preserve Windows EOL when replacing the complete reviewed function."""
    state = verify_checkout()
    current, old, updated = prepare()
    mode = "ALREADY_INSTALLED" if normalized(current).decode("utf-8-sig") == updated else "INSTALL"
    if not dry_run and mode == "INSTALL":
        line_ending = b"\r\n" if b"\r\n" in current else b"\n"
        replacement = updated.encode("utf-8").replace(b"\n", line_ending)
        (ROOT / TARGET).write_bytes(replacement)
        if normalized((ROOT / TARGET).read_bytes()).decode("utf-8-sig") != updated:
            raise RuntimeError("R53 public function replacement was not applied")
    return {
        **state,
        "target": TARGET,
        "install_mode": mode,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "changed_production_files": 0 if dry_run else 1,
        "full_pytest": False,
        "gate": (
            "PASS_R53_GENERIC_PROVIDER_PREFLIGHT" if dry_run else
            "PASS_R53_GENERIC_PROVIDER_WIRING_INSTALLED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    details = apply(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R53_"
    for name, value in details.items():
        print(prefix + name.upper() + "=" + str(value))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
