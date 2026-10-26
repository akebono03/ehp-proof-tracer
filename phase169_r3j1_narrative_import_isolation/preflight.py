"""Guard the canonical EHP module path before pytest changes import search order."""
from __future__ import annotations

from pathlib import Path
import importlib


def main() -> None:
    repo = Path(__file__).resolve().parent.parent
    if Path.cwd().resolve() != repo:
        raise RuntimeError("Run R3J1 from the repository root")
    canonical = (repo / "phase165_r14_r5_ehp_connection.py").resolve()
    module = importlib.import_module("phase165_r14_r5_ehp_connection")
    actual = Path(module.__file__).resolve()
    if actual != canonical:
        raise RuntimeError(f"Shadow EHP adapter import: {actual} != {canonical}")
    if not callable(module.expand_registered_ehp_terminal_goal):
        raise RuntimeError("Missing R3F terminal adapter")
    if not callable(module.expand_cited_ehp_terminal_goal):
        raise RuntimeError("Missing R3I cited terminal adapter")
    print("R3J1_ROOT_EHP_MODULE_OK=True")


if __name__ == "__main__":
    main()
