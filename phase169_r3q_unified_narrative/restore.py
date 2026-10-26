"""Restore exactly the two source files saved by R3Q installation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def main():
    for name in ("phase168_r3_5_model_renderer.py", "phase168_r3_27_typed_statement_projection.py"):
        source = PKG / "output" / (name + ".before")
        target = ROOT / name
        if not source.is_file():
            raise RuntimeError("No backup for " + name)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        print("R3Q_RESTORED=" + name)


if __name__ == "__main__":
    main()
