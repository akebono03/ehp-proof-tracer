from pathlib import Path
import shutil


SOURCE = Path(
  "phase143_75w"
) / (
  "test_phase143_75w_"
  "toda54_bracket_up_to_sign_"
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
