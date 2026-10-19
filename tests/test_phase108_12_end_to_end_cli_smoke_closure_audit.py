from pathlib import Path
import subprocess
import sys


_REPO_ROOT = (
  Path(
    __file__
  )
  .resolve()
  .parents[
    1
  ]
)


def _run_main(
  *args: str,
) -> subprocess.CompletedProcess:
  return subprocess.run(
    [
      sys.executable,
      "main.py",
      *args,
    ],
    cwd=_REPO_ROOT,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="strict",
    check=False,
  )






