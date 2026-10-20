from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent.parent
TARGET=ROOT / "phase166_r3v_existing_evidence_bridge" / "test_r3v.py"
SOURCE=Path(__file__).with_name("test_r3v.py")

def main():
    before=TARGET.read_text(encoding="utf-8")
    after=SOURCE.read_text(encoding="utf-8")
    if before==after:
        print("ALREADY_APPLIED: test correction")
        return
    if "assert any(link.step and link.step.conclusion == Relation(" not in before:
        raise RuntimeError("Unknown test version: refusing overwrite")
    backup=Path(__file__).parent / "original_test_r3v.py"
    if not backup.exists():
        shutil.copy2(TARGET,backup)
    TARGET.write_text(after,encoding="utf-8")
    print("PATCHED TEST ONLY:",TARGET)
if __name__=="__main__":main()
