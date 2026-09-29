from pathlib import Path
import runpy
import shutil


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

shutil.copyfile(
    HERE / "test_phase144_2_sigma_triple_prime_definition.py",
    ROOT / "tests" / "test_phase144_2_sigma_triple_prime_definition.py",
)

runpy.run_path(
    str(HERE / "apply_phase144_2.py"),
    run_name="__main__",
)
