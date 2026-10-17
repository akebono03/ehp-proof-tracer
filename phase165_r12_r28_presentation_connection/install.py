"""Connect one common presentation provider; never alter the mathematical inference rules."""
from pathlib import Path
import ast
import shutil


def main() -> None:
    here = Path(__file__).resolve().parent
    project = here.parent
    shared = project / "phase165_r52_r9_shared_math.py"
    target = project / "phase165_r12_r28_presentation_connection.py"
    source = here / target.name
    code = shared.read_text(encoding="utf8")
    anchor = "    extra_providers = (build_concrete_kernel_provider(bridge),) + tuple(extra_providers)"
    addition = ("    from phase165_r12_r28_presentation_connection import expand_eta_presentation\n"
                "    extra_providers = (expand_eta_presentation,) + tuple(extra_providers)\n")
    if addition.strip() not in code:
        if code.count(anchor) != 1:
            raise ValueError("shared provider anchor changed")
        code = code.replace(anchor, addition + anchor, 1)
    ast.parse(code)
    ast.parse(source.read_text(encoding="utf8"))
    if target.exists() and target.read_bytes() != source.read_bytes():
        raise ValueError("conflicting R12-R28 module")
    if not target.exists():
        shutil.copy2(source, target)
    if code != shared.read_text(encoding="utf8"):
        shutil.copy2(shared, shared.with_name(shared.name + ".r12_r28_backup"))
        shared.write_text(code, encoding="utf8")
    print("R12-R28 presentation provider: CONNECTED")


if __name__ == "__main__":
    main()
