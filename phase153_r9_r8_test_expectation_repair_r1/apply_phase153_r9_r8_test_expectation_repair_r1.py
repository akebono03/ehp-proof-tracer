from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent

def find_repository_root() -> Path:
  for candidate in (PACKAGE_DIR.parent, Path.cwd()):
    if (
      (candidate / 'tests' / 'test_phase153_r8_reference_use_prose_normalization.py').is_file()
      and (candidate / 'tests' / 'test_phase153_r9_reference_reuse_derivation_suppression.py').is_file()
    ):
      return candidate.resolve()
  raise SystemExit('EHP Proof Tracer repository root was not found.')

def main() -> None:
  repo = find_repository_root()
  path = repo / 'tests' / 'test_phase153_r8_reference_use_prose_normalization.py'
  text = path.read_text(encoding='utf-8')

  old = """def test_phase153_r8_pi6_2_keeps_non_reference_derivation_and_conclusion():
  body = _pi6_2_body()

  assert (
    r\"このことから、$γ \\mapsto \\eta_{2}γ$を得る。\"
    in body
  )
  assert (
    r\"\\pi_{6}^{2} = \\mathbb{Z}/4\\{\\eta_{2}\\nu'\\}\"
    in body
  )
"""

  new = """def test_phase153_r8_pi6_2_keeps_final_conclusion():
  body = _pi6_2_body()

  assert (
    r\"\\pi_{6}^{2} = \\mathbb{Z}/4\\{\\eta_{2}\\nu'\\}\"
    in body
  )
"""

  count = text.count(old)
  if count != 1:
    raise SystemExit(f'R8 integration-test replacement target expected once, found {count}.')

  backup_dir = repo / 'phase153_r9_r8_test_expectation_repair_r1_backup'
  backup_dir.mkdir(exist_ok=True)
  backup = backup_dir / path.name
  if not backup.exists():
    shutil.copy2(path, backup)

  path.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')
  print('Phase 153-R9 R8 test-expectation repair R1 applied.')
  print('Production changes: none')
  print('Changed test:')
  print('  tests/test_phase153_r8_reference_use_prose_normalization.py')

if __name__ == '__main__':
  main()
