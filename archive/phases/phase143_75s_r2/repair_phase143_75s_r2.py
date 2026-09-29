from pathlib import Path
import shutil


SOURCE = Path(
  "phase143_75s"
) / (
  "test_phase143_75s_"
  "toda58_whitehead_square_"
  "semantic_rendering.py"
)

TARGET = Path(
  "tests"
) / (
  "test_phase143_75s_"
  "toda58_whitehead_square_"
  "semantic_rendering.py"
)


def main():
  if not SOURCE.exists():
    raise FileNotFoundError(
      "Phase 143-75S source test file "
      "was not found: "
      + str(SOURCE)
    )

  TARGET.parent.mkdir(
    parents=True,
    exist_ok=True,
  )

  shutil.copyfile(
    SOURCE,
    TARGET,
  )

  print(
    "Phase 143-75S-R2 test placement "
    "repair complete."
  )
  print(
    "Placed:",
    TARGET,
  )


if __name__ == "__main__":
  main()
