"""Fail-closed R57-R8 installer; emit complete installed replacement units."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _replace_shared_provider(root: Path, package: Path):
    path = root / "phase165_r52_r9_shared_math.py"
    source = path.read_text(encoding="utf-8")
    desired = (package / "shared_expansion_provider.py.txt").read_text(encoding="utf-8").rstrip("\n")
    matches = [x for x in ast.parse(source).body if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider"]
    if len(matches) != 1:
        raise RuntimeError("R57-R8 expects exactly one shared_expansion_provider")
    f = matches[0]
    lines = source.splitlines(keepends=True)
    old = "".join(lines[f.lineno-1:f.end_lineno]).rstrip("\n")
    if old == desired:
        return None
    if "expand_registered_eta_specialization" in old:
        raise RuntimeError("existing specialization provider differs; stop")
    if "expand_registered_toda45_finite_cyclic_goal" not in old or "expand_existing_pi43_rules" not in old:
        raise RuntimeError("R57-R7 predecessor missing from shared provider")
    updated = "".join(lines[:f.lineno-1]) + desired + "\n" + "".join(lines[f.end_lineno:])
    ast.parse(updated)
    return path, updated, "phase165_r52_r9_shared_math.py", desired


def _replace_selector(root: Path):
    """Append a strictly compatible wrapper with the original signature.

    The historical R55 source is not on GitHub HEAD. Inspect the actual local
    function and fail if its signature or call contract cannot be preserved.
    """
    path = root / "phase165_r55_nk_only_goal.py"
    source = path.read_text(encoding="utf-8")
    sentinel = "# R57-R8 REGISTERED GENERIC GOAL SPECIALIZATION"
    if sentinel in source:
        if "specialized_eta_group_goal_candidates" not in source:
            raise RuntimeError("R57-R8 selector marker exists without hook")
        return None
    tree = ast.parse(source)
    matches = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "registered_group_goal_candidates"]
    if len(matches) != 1:
        raise RuntimeError("R55 goal selector not found exactly once")
    fn = matches[0]
    if fn.args.posonlyargs or fn.args.vararg or fn.args.kwarg:
        raise RuntimeError("unsupported selector signature; leave code unchanged")
    params = [x.arg for x in fn.args.args] + [x.arg for x in fn.args.kwonlyargs]
    if len(params) != len(set(params)) or not ({"n", "k"} <= set(params)):
        raise RuntimeError("selector must expose n and k to specialize a requested group")
    bridge_param = next((x for x in ("bridge", "registry_bridge") if x in params), None)
    original_signature = ast.unparse(fn.args)
    original_call = ", ".join(x+"="+x for x in params)
    # When R55 builds its own shared bridge, repeat that construction for
    # selecting candidates. It is the same source registry, not new evidence.
    bridge_line = ("    typed_bridge = " + bridge_param + "\n" if bridge_param else
                   "    from phase165_r52_r9_shared_math import build_shared_typed_bridge\n    typed_bridge = build_shared_typed_bridge()\n")
    patch = (
        "\n\n"+sentinel+"\n"
        "_phase165_r57_r8_previous_registered_group_goal_candidates = registered_group_goal_candidates\n\n"
        "def registered_group_goal_candidates(" + original_signature + "):\n"
        "    \"\"\"Extend the previous R55 selection with derived symbolic-reference goals.\"\"\"\n"
        "    from homotopy_groups import TodaPrimaryGroup\n"
        "    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates\n"
        "    existing = _phase165_r57_r8_previous_registered_group_goal_candidates("+original_call+")\n"
        "    if not isinstance(existing, tuple):\n"
        "        raise TypeError(\"R55 selector must return a tuple\")\n"
        "    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)\n"
        + bridge_line +
        "    candidates = specialized_eta_group_goal_candidates(group, typed_bridge)\n"
        "    output = list(existing)\n"
        "    for candidate in candidates:\n"
        "        if not any(type(candidate) is type(old) and candidate == old for old in output):\n"
        "            output.append(candidate)\n"
        "    return tuple(output)\n"
    )
    ast.parse(patch)
    final=source.rstrip("\n")+patch
    ast.parse(final)
    return path, final, "phase165_r55_nk_only_goal.py", patch


def install(root: Path, package: Path) -> str:
    expected_helper = package / "phase165_r57_r8_eta_specialization.py"
    existing_helper = root / expected_helper.name
    if existing_helper.exists() and existing_helper.read_bytes() != expected_helper.read_bytes():
        raise RuntimeError("existing specialization module differs; stop")
    changes = [x for x in (_replace_shared_provider(root,package), _replace_selector(root)) if x]
    for path, result, _, _ in changes:
        ast.parse(result)
    for path, result, _, _ in changes:
        backup = path.with_suffix(".r57_r8_before.py.bak")
        if not backup.exists():
            shutil.copy2(path,backup)
    if not existing_helper.exists():
        shutil.copy2(expected_helper,existing_helper)
    for path, result, _, _ in changes:
        path.write_text(result,encoding="utf-8")
    readme = ["# R57-R8 installed code", "", "## Modified complete functions", ""]
    for path, result, label, content in changes:
        readme.extend(["### "+label,"", "```python",content.rstrip("\n"),"```", ""])
    if changes:
        (package/"INSTALLED_FUNCTIONS.md").write_text("\n".join(readme),encoding="utf-8")
    return "INSTALLED" if changes else "ALREADY_INSTALLED"


if __name__ == "__main__":
    package=Path(__file__).resolve().parent
    print("R57-R8:",install(package.parent,package))
    print("Only typed reference specialization added; no GIVEN or old replay")
    print("Full pytest NOT run")
