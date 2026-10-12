"""R7-R1: guarded test-only repair. No production files are touched."""
import hashlib
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "tests/test_phase164_r7_statement_resolution.py"
SOURCE = PACKAGE / "files/tests/test_phase164_r7_statement_resolution.py"
OLD_SHA256 = "dbef4ea0bc010ca64665670fb2d7d19379d9dd88aa22191a5a8d4792c64f9b62"
NEW_SHA256 = "29bcb588cf0795e7c2c6967f6bfb81e3c7e84dbd796af1a09868dccbef389966"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if not TARGET.is_file():
        raise RuntimeError("R7 test is missing; install original R7 package first")
    if sha256(SOURCE) != NEW_SHA256:
        raise RuntimeError("Repair source checksum mismatch")
    actual = sha256(TARGET)
    if actual == NEW_SHA256:
        print("R7-R1 test already repaired")
        return
    if actual != OLD_SHA256:
        raise RuntimeError("Local test differs from original R7; refusing overwrite")
    backup = ROOT / "tests/test_phase164_r7_statement_resolution.phase164_r7_r1_backup.py"
    if backup.exists() and backup.read_bytes() != TARGET.read_bytes():
        raise RuntimeError("Existing backup differs; refusing overwrite")
    shutil.copyfile(TARGET, backup)
    shutil.copyfile(SOURCE, TARGET)
    print("Repaired R7 test fixture document identity and ProofStep premises; production unchanged")

if __name__ == "__main__":
    main()
