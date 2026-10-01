from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent

def find_repository_root() -> Path:
  for candidate in (PACKAGE_DIR.parent, Path.cwd()):
    if (
      (candidate / "toda_group_proof_narrative_references.py").is_file()
      and (candidate / "toda_group_proof_narrative_contribution_renderer.py").is_file()
      and (candidate / "toda_group_proof_narrative_renderer.py").is_file()
      and (candidate / "tests").is_dir()
    ):
      return candidate.resolve()
  raise SystemExit("EHP Proof Tracer repository root was not found.")

def replace_once(text: str, old: str, new: str, label: str) -> str:
  count = text.count(old)
  if count != 1:
    raise SystemExit(
      f"{label}: expected exactly one replacement target, found {count}."
    )
  return text.replace(old, new, 1)

def patch_references(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_references.py"
  text = path.read_text(encoding="utf-8")
  marker = "def select_toda_group_proof_narrative_reference_statement_steps(\n"

  helper = '''def exclude_toda_group_proof_narrative_root_reference(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
  root_step: ProofStep,
) -> tuple[
  tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
]:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      root_step
    )
  )

  if root_reference is None:
    return (
      entries,
      statement_lines_by_reference_number,
    )

  retained_entries = tuple(
    entry
    for entry in entries
    if entry.reference != root_reference
  )

  if len(retained_entries) == len(entries):
    return (
      entries,
      statement_lines_by_reference_number,
    )

  number_map = {
    entry.number: new_number
    for new_number, entry in enumerate(
      retained_entries,
      start=1,
    )
  }

  filtered_entries = tuple(
    replace(
      entry,
      number=number_map[
        entry.number
      ],
    )
    for entry in retained_entries
  )

  filtered_statement_lines = {
    number_map[
      entry.number
    ]: statement_lines_by_reference_number[
      entry.number
    ]
    for entry in retained_entries
    if entry.number in statement_lines_by_reference_number
  }

  return (
    filtered_entries,
    filtered_statement_lines,
  )


'''

  if "def exclude_toda_group_proof_narrative_root_reference(" in text:
    raise SystemExit("R12 root Reference helper is already present.")
  if marker not in text:
    raise SystemExit("R12 helper insertion marker not found.")

  path.write_text(
    text.replace(marker, helper + marker, 1),
    encoding="utf-8",
    newline="\n",
  )

def patch_contribution_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_contribution_renderer.py"
  text = path.read_text(encoding="utf-8")

  old_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  new_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    "R12 contribution Reference import",
  )

  old = '''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
'''

  new = '''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
'''

  if old not in text:
    raise SystemExit(
      "R12 contribution Reference statement block not found."
    )

  text = text.replace(old, new, 1)

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def patch_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_renderer.py"
  text = path.read_text(encoding="utf-8")

  old_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''

  new_import = '''from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    "R12 renderer Reference import",
  )

  old = '''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  reference_section = (
'''

  new = '''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  reference_section = (
'''

  text = replace_once(
    text,
    old,
    new,
    "R12 marker-bearing root Reference exclusion",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def install_test(repo: Path) -> None:
  shutil.copy2(
    PACKAGE_DIR / "tests" / "test_phase153_r12_root_reference_exclusion.py",
    repo / "tests" / "test_phase153_r12_root_reference_exclusion.py",
  )

def main() -> None:
  repo = find_repository_root()
  backup_dir = (
    repo
    / "phase153_r12_root_reference_exclusion_across_routes_backup"
  )
  backup_dir.mkdir(exist_ok=True)

  for relative in (
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_contribution_renderer.py",
    "toda_group_proof_narrative_renderer.py",
  ):
    source = repo / relative
    backup = backup_dir / relative
    if not backup.exists():
      shutil.copy2(source, backup)

  patch_references(repo)
  patch_contribution_renderer(repo)
  patch_renderer(repo)
  install_test(repo)

  print(
    "Phase 153-R12 Root Reference exclusion across routes applied."
  )
  print("Changed:")
  print("  toda_group_proof_narrative_references.py")
  print("  toda_group_proof_narrative_contribution_renderer.py")
  print("  toda_group_proof_narrative_renderer.py")
  print("Added:")
  print("  tests/test_phase153_r12_root_reference_exclusion.py")

if __name__ == "__main__":
  main()
