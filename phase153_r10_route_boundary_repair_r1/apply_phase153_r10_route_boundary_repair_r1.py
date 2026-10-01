from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent

def find_repository_root() -> Path:
  for candidate in (PACKAGE_DIR.parent, Path.cwd()):
    if (
      (candidate / "toda_group_proof_narrative_references.py").is_file()
      and (candidate / "toda_group_proof_narrative_renderer.py").is_file()
      and (candidate / "tests" / "test_phase153_r9_reference_reuse_derivation_suppression.py").is_file()
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

  old = '''  used_entries = tuple(
    entry
    for entry in entries
    if (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )
    in body_markdown
  )

  number_map = {
'''

  new = '''  body_reference_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\\[R([0-9]+)\\]",
      body_markdown,
    )
  )

  if not body_reference_numbers:
    return (
      entries,
      statement_lines_by_reference_number,
      body_markdown,
    )

  used_reference_numbers = set(
    body_reference_numbers
  )
  used_entries = tuple(
    entry
    for entry in entries
    if entry.number in used_reference_numbers
  )

  number_map = {
'''

  text = replace_once(
    text,
    old,
    new,
    "R10 marker-route boundary",
  )
  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def patch_renderer(repo: Path) -> None:
  path = repo / "toda_group_proof_narrative_renderer.py"
  text = path.read_text(encoding="utf-8")

  old = '''      rendered = (
        "\\n".join(
          prefix_lines
        )
        + suppressed_body
        + "\\n"
      )
'''

  new = '''      rendered = (
        "\\n".join(
          prefix_lines
        )
        + "\\n"
        + suppressed_body
        + "\\n"
      )
'''

  text = replace_once(
    text,
    old,
    new,
    "R10 proof heading spacing",
  )
  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def patch_r9_test(repo: Path) -> None:
  path = (
    repo
    / "tests"
    / "test_phase153_r9_reference_reuse_derivation_suppression.py"
  )
  text = path.read_text(encoding="utf-8")

  old = '''def test_phase153_r9_pi6_2_reuses_r3_without_rederiving_its_ancestry():
  body = _pi6_2_body()

  assert "[R2]を用いる。" in body
  assert "[R3]を用いる。" in body

  for forbidden in (
    r"\\pi_{i - 1}^{1} = 0",
    "[R4]を用いる。",
    r"γ \\mapsto \\eta_{2}γ",
    "Toda (5.2) の η₂ 合成同型を得る。",
  ):
    assert forbidden not in body
'''

  new = '''def test_phase153_r9_pi6_2_reuses_selected_references_without_rederiving_ancestry():
  body = _pi6_2_body()

  assert "[R1]を用いる。" in body
  assert "[R2]を用いる。" in body

  for forbidden in (
    r"\\pi_{i - 1}^{1} = 0",
    "Proposition 4.4",
    r"γ \\mapsto \\eta_{2}γ",
    "Toda (5.2) の η₂ 合成同型を得る。",
  ):
    assert forbidden not in body
'''

  text = replace_once(
    text,
    old,
    new,
    "R9 rendered-reference numbering expectation",
  )
  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

def main() -> None:
  repo = find_repository_root()
  backup_dir = repo / "phase153_r10_route_boundary_repair_r1_backup"
  backup_dir.mkdir(exist_ok=True)

  for relative in (
    "toda_group_proof_narrative_references.py",
    "toda_group_proof_narrative_renderer.py",
    "tests/test_phase153_r9_reference_reuse_derivation_suppression.py",
  ):
    source = repo / relative
    backup = backup_dir / relative.replace("/", "__")
    if not backup.exists():
      shutil.copy2(source, backup)

  patch_references(repo)
  patch_renderer(repo)
  patch_r9_test(repo)

  shutil.copy2(
    PACKAGE_DIR / "audit_phase153_r10_route_boundary_repair_r1.py",
    repo / "audit_phase153_r10_route_boundary_repair_r1.py",
  )

  print("Phase 153-R10 route-boundary repair R1 applied.")
  print("Changed production:")
  print("  toda_group_proof_narrative_references.py")
  print("  toda_group_proof_narrative_renderer.py")
  print("Changed test:")
  print("  tests/test_phase153_r9_reference_reuse_derivation_suppression.py")
  print("Added audit:")
  print("  audit_phase153_r10_route_boundary_repair_r1.py")

if __name__ == "__main__":
  main()
