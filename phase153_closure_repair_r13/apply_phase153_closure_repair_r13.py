from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent

def find_repository_root() -> Path:
  for candidate in (PACKAGE_DIR.parent, Path.cwd()):
    if (
      (candidate / "toda_group_proof_narrative_references.py").is_file()
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

  marker = "def build_toda_group_proof_narrative_reference_entries(\n"
  helper = '''def _same_toda_group_proof_literature_reference(
  left: LiteratureReference | None,
  right: LiteratureReference | None,
) -> bool:
  if left is None or right is None:
    return left is right

  if (
    left.locator is not None
    and right.locator is not None
  ):
    return left.locator == right.locator

  return left == right


'''

  if "def _same_toda_group_proof_literature_reference(" not in text:
    if marker not in text:
      raise SystemExit(
        "R13 LiteratureReference identity insertion marker not found."
      )
    text = text.replace(
      marker,
      helper + marker,
      1,
    )

  old_exclude = '''  retained_entries = tuple(
    entry
    for entry in entries
    if entry.reference != root_reference
  )
'''

  new_exclude = '''  retained_entries = tuple(
    entry
    for entry in entries
    if not _same_toda_group_proof_literature_reference(
      entry.reference,
      root_reference,
    )
  )
'''

  text = replace_once(
    text,
    old_exclude,
    new_exclude,
    "R13 canonical root Reference exclusion",
  )

  old_step_usage = '''      entry.reference
      != root_reference
      and any(
'''

  new_step_usage = '''      not _same_toda_group_proof_literature_reference(
        entry.reference,
        root_reference,
      )
      and any(
'''

  text = replace_once(
    text,
    old_step_usage,
    new_step_usage,
    "R13 generic canonical root Reference exclusion",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def patch_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_renderer.py"
  text = path.read_text(encoding="utf-8")

  start = text.find(
    "def _phase153_r3_10_connect_public_reference_section(\n"
  )
  if start < 0:
    raise SystemExit(
      "R13 specialized public Reference connector was not found."
    )

  end = text.find(
    "\ndef _wrap_phase150_rc4_generic_public_narrative(\n",
    start,
  )
  if end < 0:
    raise SystemExit(
      "R13 specialized public Reference connector end marker was not found."
    )

  replacement = '''def _phase153_r3_10_connect_public_reference_section(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  lines = rendered.splitlines()
  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  try:
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )
  except ValueError:
    return rendered

  if reference_index >= proof_index:
    return rendered

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )

  if not reference_entries:
    return rendered

  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )

  proof_body = "\n".join(
    lines[
      proof_index
      + 1:
    ]
  ).lstrip()

  (
    used_reference_entries,
    used_statement_lines,
    filtered_proof_body,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      reference_entries,
      statement_lines_by_reference_number,
      proof_body,
    )
  )

  (
    filtered_reference_entries,
    filtered_statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      used_reference_entries,
      used_statement_lines,
      presentation.root_step,
    )
  )

  if (
    len(
      filtered_reference_entries
    )
    != len(
      used_reference_entries
    )
  ):
    return rendered

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      filtered_reference_entries,
      filtered_statement_lines,
    )
  )

  if not reference_section:
    return rendered

  prefix_lines = lines[
    :reference_index
  ]

  while (
    prefix_lines
    and not prefix_lines[
      -1
    ].strip()
  ):
    prefix_lines.pop()

  return (
    "\n".join(
      (
        *prefix_lines,
        "",
        reference_header,
        "",
        reference_section,
        "",
        proof_header,
        "",
        filtered_proof_body,
      )
    ).rstrip()
    + "\n"
  )


'''

  text = (
    text[:start]
    + replacement
    + text[end + 1:]
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def install_test(repo: Path) -> None:
  shutil.copy2(
    PACKAGE_DIR / "tests" / "test_phase153_closure_repair_r13.py",
    repo / "tests" / "test_phase153_closure_repair_r13.py",
  )

def main() -> None:
  repo = find_repository_root()
  backup_dir = repo / "phase153_closure_repair_r13_backup"
  backup_dir.mkdir(exist_ok=True)

  for relative in (
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_renderer.py",
  ):
    source = repo / relative
    backup = backup_dir / relative
    if not backup.exists():
      shutil.copy2(source, backup)

  patch_references(repo)
  patch_renderer(repo)
  install_test(repo)

  print("Phase 153 closure repair R13 applied.")
  print("Changed:")
  print("  toda_group_proof_narrative_references.py")
  print("  toda_group_proof_narrative_renderer.py")
  print("Added:")
  print("  tests/test_phase153_closure_repair_r13.py")

if __name__ == "__main__":
  main()
