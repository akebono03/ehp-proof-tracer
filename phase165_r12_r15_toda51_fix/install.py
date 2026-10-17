"""Install R12-R15 using one Toda (5.1) source and common specialization."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def main() -> None:
    root = Path.cwd()
    package = Path(__file__).resolve().parent
    payload = package / "payload" / "phase165_r12_r15_toda51.py"
    target = root / payload.name
    shared_path = root / "phase165_r52_r9_shared_math.py"
    if not shared_path.is_file():
        raise FileNotFoundError(shared_path)
    if target.is_file() and target.read_bytes() != payload.read_bytes():
        raise RuntimeError("Conflicting existing Toda (5.1) specialization module")
    text = shared_path.read_text(encoding="utf8")
    if "build_adopted_prop42_general_reference()" not in text:
        raise RuntimeError("R12-R11 prerequisite not installed")
    if "expand_ehp_exactness_consequences" not in text:
        raise RuntimeError("R12-R12 prerequisite not installed")
    marker = "build_adopted_toda51_zero_reference(adopted_tex)"
    if marker not in text:
        anchor = "        sources = (production, build_adopted_typed_reference_registry(adopted_tex),"
        if text.count(anchor) != 1:
            raise RuntimeError("Cannot locate unique common source registration")
        text = text.replace(
            anchor,
            "        from phase165_r12_r15_toda51 import build_adopted_toda51_zero_reference\n" + anchor,
            1,
        )
        anchor2 = "(literature, build_adopted_prop42_general_reference())"
        if text.count(anchor2) != 1:
            raise RuntimeError("Cannot locate common source tuple")
        text = text.replace(
            anchor2,
            "(literature, build_adopted_prop42_general_reference(), " + marker + ")",
            1,
        )
    provider_import = "from phase165_r12_r15_toda51 import expand_cited_toda51_zero"
    if provider_import not in text:
        anchor3 = "    if not isinstance(prior_conclusions, tuple):"
        if text.count(anchor3) != 1:
            raise RuntimeError("Cannot locate shared provider setup")
        text = text.replace(anchor3, "    " + provider_import + "\n" + anchor3, 1)
    call = "options.extend(expand_cited_toda51_zero(goal, tuple(available)))"
    if call not in text:
        anchor4 = "        options = []"
        if text.count(anchor4) != 1:
            raise RuntimeError("Cannot locate shared provider expansion")
        text = text.replace(anchor4, anchor4 + "\n        " + call, 1)
    # If the superseded R15 standalone connectivity provider was installed,
    # disconnect it. Preserve the existing file for diagnosis, not runtime use.
    text = text.replace(
        "    from phase165_r12_r15_surjectivity import expand_sphere_connectivity_zero\n",
        "",
    )
    text = text.replace(
        "build_exactness_binding_provider(bridge), expand_sphere_connectivity_zero)",
        "build_exactness_binding_provider(bridge))",
    )
    ast.parse(text, filename=str(shared_path))
    ast.parse(payload.read_text(encoding="utf8"), filename=str(target))
    if shared_path.read_text(encoding="utf8") != text:
        backup = shared_path.with_name(shared_path.name + ".r12_r15_toda51.bak")
        if not backup.exists():
            shutil.copy2(shared_path, backup)
        shared_path.write_text(text, encoding="utf8")
        print("Updated:", shared_path.name)
    else:
        print("Already connected:", shared_path.name)
    if not target.exists():
        shutil.copy2(payload, target)
        print("Added:", target.name)
    print("Toda (5.1) universal-zero specialization installed; full pytest NOT run")


if __name__ == "__main__":
    main()
