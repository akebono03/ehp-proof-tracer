from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
NODEIDS = (
  PACKAGE_DIR
  / "modified_test_nodeids.txt"
)


def main() -> int:
  if not NODEIDS.exists():
    raise RuntimeError(
      "modified_test_nodeids.txt was not generated"
    )

  nodeids = [
    line.strip()
    for line in NODEIDS.read_text(
      encoding="utf-8",
    ).splitlines()
    if line.strip()
  ]

  if not nodeids:
    print(
      "No stale intro test functions required modification."
    )
    return 0

  command = [
    sys.executable,
    "-m",
    "pytest",
    *nodeids,
    "-q",
  ]

  print(
    "Running "
    + str(
      len(
        nodeids
      )
    )
    + " affected test function(s)."
  )

  result = subprocess.run(
    command,
    cwd=REPO_ROOT,
    check=False,
  )

  return result.returncode


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
