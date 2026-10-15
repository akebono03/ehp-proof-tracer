"""Roll back all R4 changes from saved originals."""
from pathlib import Path
from install import restore

if __name__ == "__main__":
    restore(Path(__file__).resolve().parent.parent)
    print("R4 files and alias restored")
