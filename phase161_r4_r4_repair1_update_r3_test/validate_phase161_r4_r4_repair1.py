from pathlib import Path
import ast


REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = (
  REPO_ROOT / "toda_group_proof_narrative_contribution_renderer.py",
  REPO_ROOT / "tests" / "test_phase161_r4_r3_fixed_frontier_internal_ancestry.py",
  REPO_ROOT / "tests" / "test_phase161_r4_r4_restore_global_frontier.py",
)


def main():
  for target in TARGETS:
    source = target.read_text(
      encoding="utf-8"
    )
    ast.parse(
      source,
      filename=str(
        target
      ),
    )
    print(
      "AST OK:",
      target,
    )


if __name__ == "__main__":
  main()
