from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  candidates = (
    PACKAGE_DIR.parent,
    Path.cwd(),
  )

  for candidate in candidates:
    if (
      (
        candidate
        / "toda_group_proof_narrative_contribution_renderer.py"
      ).is_file()
      and (
        candidate
        / "tests"
      ).is_dir()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, found {count}."
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_file(
  repo: Path,
) -> None:
  path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  old_import = """from proof import (
  ProofStep,
  Relation,
  RelationType,
)
"""

  new_import = """from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
"""

  text = replace_once(
    text,
    old_import,
    new_import,
    "scalar import",
  )

  old_import = """from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
"""

  new_import = """from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
)
"""

  text = replace_once(
    text,
    old_import,
    new_import,
    "scalar latex import",
  )

  old = """        rendered = (
          _render_generic_narrative_step(
            premise_step
          )
        )

        if rendered:
          suppressed_fragments.add(
            rendered
          )
"""

  new = """        if isinstance(
          premise_step.conclusion,
          ScalarGreaterEqualStatement,
        ):
          rendered = (
            "$"
            + _render_scalar_latex(
              premise_step.conclusion.left
            )
            + r" \\ge "
            + _render_scalar_latex(
              premise_step.conclusion.right
            )
            + "$"
          )
        else:
          rendered = (
            _render_generic_narrative_step(
              premise_step
            )
          )

        if rendered:
          suppressed_fragments.add(
            rendered
          )
"""

  text = replace_once(
    text,
    old,
    new,
    "suppression render key",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )


def install_test(
  repo: Path,
) -> None:
  shutil.copy2(
    (
      PACKAGE_DIR
      / "tests"
      / "test_phase153_r7_scalar_suppression_key.py"
    ),
    (
      repo
      / "tests"
      / "test_phase153_r7_scalar_suppression_key.py"
    ),
  )


def main() -> None:
  repo = find_repository_root()

  backup_dir = (
    repo
    / "phase153_r7_scalar_suppression_key_repair_r6_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )

  production_path = (
    repo
    / "toda_group_proof_narrative_contribution_renderer.py"
  )
  backup_path = (
    backup_dir
    / production_path.name
  )

  if not backup_path.exists():
    shutil.copy2(
      production_path,
      backup_path,
    )

  patch_file(
    repo
  )
  install_test(
    repo
  )

  print(
    "Phase 153-R7 scalar suppression-key repair R6 applied."
  )
  print(
    "Changed:"
  )
  print(
    "  toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Added:"
  )
  print(
    "  tests/test_phase153_r7_scalar_suppression_key.py"
  )


if __name__ == "__main__":
  main()
