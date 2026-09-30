from pathlib import Path
import shutil

repo = Path.cwd()
source = Path(__file__).resolve().parent / "replacement" / "test_phase144_6_r5_43_10_transport_chain_compression_production.py"
target = repo / "tests" / source.name
backup = repo / "phase150_r5_43_10_fixture_performance_repair_r1_backup" / target.name

if not target.exists():
    raise SystemExit(f"Target test file not found: {target}")

backup.parent.mkdir(parents=True, exist_ok=True)
if not backup.exists():
    shutil.copy2(target, backup)

shutil.copy2(source, target)
print(f"Replaced: {target}")
print(f"Backup:   {backup}")
