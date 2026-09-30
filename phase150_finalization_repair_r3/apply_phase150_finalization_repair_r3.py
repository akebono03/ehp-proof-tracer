from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE = ROOT / "reference_updated_tests"
BACKUP = ROOT / "backup_before_r3"

FILES = (
    "test_phase132_6_group_proof_narrative_renderer.py",
    "test_phase132_7_group_proof_cli_modes.py",
    "test_phase132_8_group_proof_narrative_dedup.py",
    "test_phase132_9_web_group_proof_modes.py",
    "test_phase133_10_sigma_label_wording.py",
    "test_phase133_6_group_proof_narrative_labels.py",
    "test_phase133_9_group_proof_narrative_labels.py",
    "test_phase144_6_r3_production_references.py",
    "test_phase144_6_r3_structured_references.py",
    "test_phase144_6_r4_supporting_fact_filtering.py",
)

def main() -> int:
    BACKUP.mkdir(exist_ok=True)
    for name in FILES:
        target = REPO / "tests" / name
        source = SOURCE / name
        if not target.is_file():
            raise FileNotFoundError(target)
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(target, BACKUP / name)
        data = source.read_bytes()
        data.decode("utf-8")
        target.write_bytes(data)
        print(f"updated UTF-8: tests/{name}")
    print("R3 applied. Production files unchanged.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
