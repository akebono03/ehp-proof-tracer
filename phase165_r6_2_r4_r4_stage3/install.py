"""Install strictly the two exactness bridges; fail closed on unfamiliar states."""
import ast
from pathlib import Path
import shutil

NAMES = (
    "ImageZeroStatement", "KernelWholeStatement",
    "exactness_and_zero_image_implies_zero_kernel_inference_rule",
    "exactness_and_whole_kernel_implies_whole_image_inference_rule",
)
REQUIRES = (
    "KernelZeroStatement", "ImageWholeStatement", "SurjectiveMapStatement",
    "kernel_zero_implies_injective_inference_rule",
    "whole_image_implies_surjective_inference_rule",
)


def install(root: Path) -> str:
    path = root / "map_property_rules.py"
    if not path.is_file():
        raise FileNotFoundError(path)
    old = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(old)
    names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    if not set(REQUIRES).issubset(names):
        raise RuntimeError("R4-4 stage2 prerequisite missing")
    present = set(NAMES) & names
    if present == set(NAMES):
        return "ALREADY_INSTALLED"
    if present:
        raise RuntimeError("partial stage3 installation; no changes applied")
    addition = Path(__file__).with_name("new_rules.txt").read_text(encoding="utf-8")
    updated = old.rstrip() + "\n" + addition
    ast.parse(updated)
    backup = path.with_name("map_property_rules.py.r4_r4_stage3_before.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(updated, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    print(install(Path.cwd()))
