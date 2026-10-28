"""Verify that R10EJ-R1 delegates to exactly the reviewed R10EJ runner.

This helper never writes a source file, tracked report, or Git object.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

REVIEWED_ORIGINAL_RUNNER_SHA256 = "6ebff8e59f4ad262ce8d78f96adec48efb5c857de94a7213da6dbda7f07eb34a"
ORIGINAL_RUNNER = Path("phase169_r10ej_cyclic_verified_projection") / "run.ps1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_reviewed_runner(root: Path) -> None:
    """Refuse an unreviewed script without modifying it."""
    path = root / ORIGINAL_RUNNER
    if not path.is_file():
        raise RuntimeError(f"R10EJ original run.ps1 missing: {path}")
    data = path.read_bytes()
    if sha256_bytes(data) != REVIEWED_ORIGINAL_RUNNER_SHA256:
        raise RuntimeError("R10EJ original run.ps1 differs from the reviewed ZIP")
    text = data.decode("utf-8")
    if text.count("python -B -m pytest") != 2:
        raise RuntimeError("R10EJ original runner no longer has exactly two focused pytest invocations")
    if "phase169_r10ej_cyclic_verified_projection.apply restore" not in text:
        raise RuntimeError("R10EJ original runner's rollback guard missing")


def compose_addopts(previous: str | None) -> str:
    """Preserve existing pytest options, disable the cache plugin in child pytest."""
    return " ".join(value for value in ((previous or "").strip(), "-p no:cacheprovider") if value)


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        print("Usage: python -B -m phase169_r10ejr1_pytest_cache_isolation.verify check REPO_PATH", file=sys.stderr)
        return 2
    verify_reviewed_runner(Path(sys.argv[2]))
    print("R10EJR1_REVIEWED_ORIGINAL_RUNNER=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
