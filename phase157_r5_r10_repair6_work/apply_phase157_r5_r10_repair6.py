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
test_target = (
    ROOT
    / "tests"
    / "test_phase157_r5_r10_reference_proof_boundary_qed.py"
)

for path in (
    contribution_renderer,
    test_target,
):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)

old_return = '''  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + rendered
  )
'''

new_return = '''  legacy_intro = (
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

replace_once(
    contribution_renderer,
    old_return,
    new_return,
    "remove legacy reference intro before public proof body",
)

test_text = test_target.read_text(encoding="utf-8")

extra_test = r'''

def test_phase157_r5_r10_pi6_3_proof_body_does_not_repeat_reference_intro():
  rendered = _rendered_group_proof(
    3,
    3,
  )

  proof_body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  assert (
    "使用する結果を先にまとめる."
    not in proof_body
  )
'''

if (
    "test_phase157_r5_r10_pi6_3_proof_body_does_not_repeat_reference_intro"
    not in test_text
):
    test_target.write_text(
        test_text.rstrip()
        + extra_test
        + "\n",
        encoding="utf-8",
    )
    print(
        "Added: "
        "test_phase157_r5_r10_pi6_3_proof_body_does_not_repeat_reference_intro"
    )
else:
    print(
        "Already present: "
        "test_phase157_r5_r10_pi6_3_proof_body_does_not_repeat_reference_intro"
    )

print("")
print("Phase157 R5-R10 repair6 patch applied successfully.")
print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
)
print(
    "Changed: "
    "tests/test_phase157_r5_r10_reference_proof_boundary_qed.py"
)
