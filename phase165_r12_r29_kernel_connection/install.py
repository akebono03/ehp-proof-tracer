"""Install a shared backward provider with strict anchor checks."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    folder = Path(__file__).resolve().parent
    project = folder.parent
    source = folder / "phase165_r12_r29_kernel_connection.py"
    destination = project / source.name
    shared = project / "phase165_r52_r9_shared_math.py"
    code = shared.read_text(encoding="utf8")
    anchor = "    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)"
    addition = ("    from phase165_r12_r29_kernel_connection import expand_kernel_multiple_from_suspension\n"
                "    extra_providers = (expand_kernel_multiple_from_suspension,) + tuple(extra_providers)\n")
    if addition not in code:
        if code.count(anchor) != 1:
            raise RuntimeError("shared provider anchor not unique")
        code = code.replace(anchor, addition + anchor, 1)
    ast.parse(code)
    ast.parse(source.read_text(encoding="utf8"))
    if destination.exists() and destination.read_bytes() != source.read_bytes():
        raise RuntimeError("existing R29 module conflicts with ZIP")
    if not destination.exists():
        shutil.copy2(source, destination)
    previous = shared.read_text(encoding="utf8")
    if code != previous:
        shutil.copy2(shared, shared.with_name(shared.name + ".r12_r29_backup"))
        shared.write_text(code, encoding="utf8")
    print("R12-R29 kernel backward provider: CONNECTED")


if __name__ == "__main__":
    main()
