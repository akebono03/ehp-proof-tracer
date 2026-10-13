"""Install only the R52-R8 test fixture correction."""
from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
SRC = Path(__file__).resolve().with_name("test_phase165_r52_r8_show_proof_route.py")
DST = ROOT / SRC.name


def main() -> None:
    if not DST.is_file():
        raise FileNotFoundError(f"Existing R52-R8 test not found: {DST}")
    current = DST.read_text(encoding="utf-8-sig")
    updated = SRC.read_text(encoding="utf-8")
    ast.parse(current)
    ast.parse(updated)
    old = "n=2, k=1, status=ProofSearchStatus.SEARCH_FAILED"
    new = 'diagnostics=("Registered proof test fixture",),'
    if new in current and current == updated:
        print("R52-R8 test fixture correction already installed")
        return
    if current.count(old) != 1 or new in current:
        raise RuntimeError("Unexpected test version: no files changed")
    backup = ROOT / "test_phase165_r52_r8_show_proof_route.py.r8_fixture_backup"
    if not backup.exists():
        shutil.copy2(DST, backup)
    DST.write_text(updated, encoding="utf-8")
    print("Corrected: test_phase165_r52_r8_show_proof_route.py")


if __name__ == "__main__":
    main()
