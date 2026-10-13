"""R52-R3 repair: install the previously omitted targeted test only."""
from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
NAME = "test_phase165_r52_r3_web_adapter.py"


def main() -> None:
    for required in (
        "web_group_proof.py",
        "phase165_r52_partial_proof.py",
        "phase165_r52_r2_search_adapter.py",
        "phase165_r52_r3_web_adapter.py",
    ):
        if not (ROOT / required).is_file():
            raise FileNotFoundError(f"Missing installed R52 dependency: {required}")
    content = (BUNDLE / NAME).read_text(encoding="utf-8")
    ast.parse(content)
    destination = ROOT / NAME
    if destination.is_file():
        existing = destination.read_text(encoding="utf-8-sig")
        if existing != content:
            raise RuntimeError(
                "Existing targeted test differs; refusing to overwrite: " + NAME
            )
        print("R52-R3 targeted test already installed")
        return
    shutil.copy2(BUNDLE / NAME, destination)
    print("Installed " + NAME)


if __name__ == "__main__":
    main()
