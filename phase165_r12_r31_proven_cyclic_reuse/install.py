"""Minimal, guarded integration into the shared provider."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    folder = Path(__file__).resolve().parent
    project = folder.parent
    source = folder / "phase165_r12_r31_proven_cyclic_reuse.py"
    destination = project / source.name
    shared = project / "phase165_r52_r9_shared_math.py"
    existing = shared.read_text(encoding="utf-8")
    anchor = "    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)"
    addition = (
        "    from phase165_r12_r31_proven_cyclic_reuse import expand_free_cyclic_structure_from_relation\n"
        "    extra_providers = (expand_free_cyclic_structure_from_relation,) + tuple(extra_providers)\n"
    )
    if addition not in existing:
        if existing.count(anchor) != 1:
            raise RuntimeError("shared provider anchor absent or ambiguous")
        updated = existing.replace(anchor, addition + anchor, 1)
    else:
        updated = existing
    ast.parse(source.read_text(encoding="utf-8"))
    ast.parse(updated)
    if destination.exists() and destination.read_bytes() != source.read_bytes():
        raise RuntimeError("existing R31 module differs; refusing overwrite")
    if not destination.exists():
        shutil.copy2(source, destination)
    if updated != existing:
        shutil.copy2(shared, shared.with_name(shared.name + ".r12_r31_backup"))
        shared.write_text(updated, encoding="utf-8")
    print("R12-R31 proved cyclic relation provider: CONNECTED")


if __name__ == "__main__":
    main()
