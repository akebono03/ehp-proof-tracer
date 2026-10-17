"""Install R12-R27 name matching by replacing only the R12-R26 provider module."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    package = Path(__file__).resolve().parent
    project = package.parent
    source = package / "phase165_r12_r26_map_candidates.py"
    destination = project / source.name
    if not destination.exists():
        raise FileNotFoundError("R12-R26 must be installed before R12-R27")
    current = destination.read_text(encoding="utf-8")
    updated = source.read_text(encoding="utf-8")
    ast.parse(updated)
    if "_same_eta_generator_name" in current:
        if current != updated:
            raise ValueError("R12-R27 already modified differently; refusing overwrite")
        print("R12-R27 name matching: ALREADY_INSTALLED")
        return
    if current.count("if goal.generator != target_eta:") != 1:
        raise ValueError("R12-R26 candidate guard changed; refusing overwrite")
    shutil.copy2(destination, project / (destination.name + ".r12_r27_backup"))
    destination.write_text(updated, encoding="utf-8")
    print("R12-R27 name matching: INSTALLED")


if __name__ == "__main__":
    main()
