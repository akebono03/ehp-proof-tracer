from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)


def backup(path: Path) -> None:
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


def replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"Already applied: {label}")
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one match for {label} in {path}, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"Applied: {label}")


contribution_renderer = (
    ROOT
    / "toda_group_proof_narrative_contribution_renderer.py"
)

public_tests = (
    ROOT / "tests" / "test_phase132_7_group_proof_cli_modes.py",
    ROOT / "tests" / "test_phase150_rc4_7a_cross_group_reference_normalization.py",
    ROOT / "tests" / "test_phase144_6_r3_production_references.py",
    ROOT / "tests" / "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py",
    ROOT / "tests" / "test_phase153_r11_generic_reference_attribution_filtering.py",
)

for path in (contribution_renderer, *public_tests):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)

old_block = '''  legacy_intro = (
    "使用する結果を先にまとめる.\\n\\n"
  )

  if rendered.startswith(
    legacy_intro
  ):
    rendered = rendered[
      len(
        legacy_intro
      ):
    ]

  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + rendered
  )
'''

new_block = '''  legacy_intro = (
    "使用する結果を先にまとめる.\\n\\n"
  )

  public_reference_section = (
    reference_section
  )

  if public_reference_section.startswith(
    legacy_intro
  ):
    public_reference_section = (
      public_reference_section[
        len(
          legacy_intro
        ):
      ]
    )

  if rendered.startswith(
    legacy_intro
  ):
    rendered = rendered[
      len(
        legacy_intro
      ):
    ]

  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + public_reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + rendered
  )
'''

replace_once(
    contribution_renderer,
    old_block,
    new_block,
    "strip legacy intro only from public reference section",
)

# Public-output tests whose old contract explicitly required the legacy intro.
replacements = {
    public_tests[0]: (
        '"使用する結果を先にまとめる." in captured.out',
        '"## 使用する結果" in captured.out',
    ),
    public_tests[1]: (
        '"使用する結果を先にまとめる." in rendered',
        '"## 使用する結果" in rendered',
    ),
    public_tests[2]: (
        '"使用する結果を先にまとめる." in rendered',
        '"## 使用する結果" in rendered',
    ),
    public_tests[4]: (
        '"使用する結果を先にまとめる." in reference_part',
        '"## 使用する結果" in reference_part',
    ),
}

for path, (old, new) in replacements.items():
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            print(f"Already applied test contract: {path.name}")
            continue
        raise RuntimeError(
            f"expected public-output assertion not found in {path}"
        )
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"Updated public-output test contract: {path.name}")

phase156 = public_tests[3]
phase156_text = phase156.read_text(encoding="utf-8")
old_phase156 = '''  assert rendered.startswith(
    "使用する結果を先にまとめる."
  )
'''
new_phase156 = '''  assert rendered.startswith(
    "# Group proof narrative"
  )
  assert "## 使用する結果" in rendered
  assert "\\n## 証明\\n" in rendered
  assert (
    "使用する結果を先にまとめる."
    not in rendered
  )
'''
if new_phase156 not in phase156_text:
    count = phase156_text.count(old_phase156)
    if count != 1:
        raise RuntimeError(
            "expected exactly one Phase156 legacy public-output "
            f"assertion, found {count}"
        )
    phase156_text = phase156_text.replace(
        old_phase156,
        new_phase156,
        1,
    )
    phase156.write_text(
        phase156_text,
        encoding="utf-8",
    )
    print(
        "Updated public-output test contract: "
        "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
    )
else:
    print(
        "Already applied test contract: "
        "test_phase156_r5_repair9_test_contract_after_boundary_collapse.py"
    )

print("")
print("Phase157 R5-R10 repair7 patch applied successfully.")
print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
)
for path in public_tests:
    print(f"Changed: {path.relative_to(ROOT)}")
