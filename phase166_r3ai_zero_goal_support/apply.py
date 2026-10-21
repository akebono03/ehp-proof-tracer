"""Install narrowly scoped typed zero-group Goal discovery."""
from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "phase166_r3af_goal_adapter.py"
BACKUP = ROOT / "phase166_r3ai_zero_goal_support_backup"

NEW_FUNCTION = '''
def database_zero_group_goal_candidates(*, n: int, k: int, csv_path=None):
    """Construct zero-group Goals from explicit DB zero rows; never evidence.

    For an unlisted stable target, reuse its stable-base row, as in
    SphereRepository. A missing or mixed row is not a zero-group assertion.
    """
    if type(n) is not int or type(k) is not int or n < 2 or k < 0:
        return ()
    path = (
        Path(csv_path)
        if csv_path is not None
        else Path(__file__).resolve().parent / "data" / "sphere.csv"
    )
    if not path.is_file():
        return ()
    repo = SphereRepository(path)
    direct = repo.df[(repo.df["n"] == n) & (repo.df["k"] == k)]
    if not direct.empty:
        source_n = n
    elif n >= k + 2:
        source_n = k + 2
    else:
        return ()
    components = repo.get_group(source_n, k).components
    if (
        len(components) != 1
        or components[0].order != 0
        or components[0].generator.strip() != "0"
    ):
        return ()
    return (
        TodaPrimaryGroupZeroStatement(
            TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n)
        ),
    )
'''

def main():
    if not TARGET.is_file():
        raise RuntimeError("Run from the EHP Proof Tracer repository root")
    source = TARGET.read_text(encoding="utf-8-sig")
    if "def database_zero_group_goal_candidates(" in source:
        print("ALREADY_APPLIED:", TARGET)
        return
    if "def database_group_goal_candidates(" not in source:
        raise RuntimeError("Phase 166 R3-AF adapter is missing")
    tree = ast.parse(source)
    if not any(isinstance(node, ast.ImportFrom)
               and node.module == "repository"
               for node in tree.body):
        raise RuntimeError("Unexpected source layout")
    old = "from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup"
    new = "from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement"
    if old not in source:
        raise RuntimeError("Unknown homotopy_groups import; refusing to patch")
    updated = source.replace(old, new, 1).rstrip() + "\n\n" + NEW_FUNCTION.strip() + "\n"
    ast.parse(updated)
    BACKUP.mkdir(exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    TARGET.write_text(updated, encoding="utf-8")
    print("PATCHED:", TARGET)
    print("BACKUP:", BACKUP)

if __name__ == "__main__":
    main()
