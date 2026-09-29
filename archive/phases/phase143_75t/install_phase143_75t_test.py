from pathlib import Path
import shutil


SOURCE = Path(
  "phase143_75t"
) / (
  "test_phase143_75t_"
  "toda58_equation_aggregate_"
  "semantic_rendering.py"
)

TARGET = Path(
  "tests"
) / SOURCE.name


def main():
  if not SOURCE.exists():
    raise FileNotFoundError(
      str(SOURCE)
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
    "Placed:",
    TARGET,
  )


if __name__ == "__main__":
  main()
