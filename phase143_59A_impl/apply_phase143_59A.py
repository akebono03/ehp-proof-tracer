from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path(__file__).resolve().parent

FILES = (
  (
    SOURCE_ROOT
    / "toda_group_proof_narrative_group_structure_semantics.py",
    ROOT
    / "toda_group_proof_narrative_group_structure_semantics.py",
  ),
  (
    SOURCE_ROOT
    / "tests"
    / "test_phase143_59a_group_structure_semantic_key.py",
    ROOT
    / "tests"
    / "test_phase143_59a_group_structure_semantic_key.py",
  ),
)


def main() -> None:
  for source, destination in FILES:
    destination.write_text(
      source.read_text(
        encoding="utf-8"
      ),
      encoding="utf-8",
    )
    print(
      f"updated {destination}"
    )


if __name__ == "__main__":
  main()
