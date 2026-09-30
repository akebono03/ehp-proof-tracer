from pathlib import Path
import shutil

ROOT = Path.cwd()
SOURCE = (
  ROOT
  / "phase150_rc4_5b_3_r1_repair"
  / "payload"
  / "tests"
  / "test_phase150_rc4_5b_3_r1_beta_latex.py"
)
TARGET = ROOT / "tests" / "test_phase150_rc4_5b_3_r1_beta_latex.py"

shutil.copyfile(SOURCE, TARGET)
print("Wrote:", TARGET.relative_to(ROOT))
