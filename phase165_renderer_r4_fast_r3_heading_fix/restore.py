from pathlib import Path
from install import restore
if __name__ == "__main__":
    restore(Path(__file__).resolve().parent.parent)
    print("R4 fast rollback: restored original source and compatibility package")
