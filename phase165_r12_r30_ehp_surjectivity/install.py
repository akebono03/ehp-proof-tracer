"""Install only the R30 shared EHP whole-image backward provider."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil


def main() -> None:
    folder = Path(__file__).resolve().parent
    project = folder.parent
    source = folder / "phase165_r12_r30_ehp_surjectivity.py"
    destination = project / source.name
    shared = project / "phase165_r52_r9_shared_math.py"
    code = shared.read_text(encoding="utf-8")
    anchor = "    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)"
    addition = ("    from phase165_r12_r30_ehp_surjectivity import expand_ehp_whole_image\n"
                "    extra_providers = (expand_ehp_whole_image,) + tuple(extra_providers)\n")
    if addition not in code:
        if code.count(anchor) != 1:
            raise RuntimeError("shared provider anchor absent or ambiguous")
        code = code.replace(anchor, addition + anchor, 1)
    ast.parse(code)
    ast.parse(source.read_text(encoding="utf-8"))
    if destination.exists() and destination.read_bytes() != source.read_bytes():
        raise RuntimeError("existing R30 module conflicts with ZIP")
    if not destination.exists():
        shutil.copy2(source, destination)
    if code != shared.read_text(encoding="utf-8"):
        shutil.copy2(shared, shared.with_name(shared.name + ".r12_r30_backup"))
        shared.write_text(code, encoding="utf-8")
    print("R12-R30 EHP whole-image provider: CONNECTED")


if __name__ == "__main__":
    main()
