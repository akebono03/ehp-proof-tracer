"""Install only the two general map-property rules; fail closed on unexpected source."""
from pathlib import Path
import ast
import shutil

APPEND = Path(__file__).with_name("new_rules.txt").read_text(encoding="utf-8")
MARKER = "def kernel_zero_implies_injective_inference_rule():"
OTHER = "def whole_image_implies_surjective_inference_rule():"


def install(root: Path) -> str:
    path = root / "map_property_rules.py"
    if not path.is_file():
        raise FileNotFoundError(path)
    source = path.read_text(encoding="utf-8-sig")
    if MARKER in source and OTHER in source:
        return "ALREADY_INSTALLED"
    if MARKER in source or OTHER in source:
        raise RuntimeError("partial R4-4 stage2 installation; refusing change")
    tree = ast.parse(source)
    names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    if not {"InjectiveMapStatement", "IsomorphismStatement", "isomorphism_implies_injective_inference_rule"}.issubset(names):
        raise RuntimeError("unexpected map_property_rules.py API")
    for name in ("KernelZeroStatement", "ImageWholeStatement", "SurjectiveMapStatement"):
        if name in names:
            raise RuntimeError("existing symbol collision: " + name)
    new = source.rstrip() + "\n" + APPEND
    ast.parse(new)
    backup = path.with_name("map_property_rules.py.r4_r4_stage2_before.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(new, encoding="utf-8")
    return "INSTALLED"


if __name__ == "__main__":
    print(install(Path.cwd()))
