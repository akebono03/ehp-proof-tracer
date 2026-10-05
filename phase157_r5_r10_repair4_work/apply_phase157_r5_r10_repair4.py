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


renderer = ROOT / "toda_group_proof_narrative_renderer.py"
test_target = (
    ROOT
    / "tests"
    / "test_phase157_r5_r10_reference_proof_boundary_qed.py"
)

for path in (renderer, test_target):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)

text = renderer.read_text(encoding="utf-8")

old_specialized_return = '''  return (
    "\\n".join(
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
    + "\\n"
  )
'''

new_specialized_return = '''  return (
    "\\n".join(
      (
        *prefix_lines,
        "",
        reference_header,
        "",
        reference_section,
        "",
        "---",
        "",
        proof_header,
        "",
        filtered_proof_body,
      )
    ).rstrip()
    + "\\n"
  )
'''

if new_specialized_return not in text:
    count = text.count(old_specialized_return)
    if count != 1:
        raise RuntimeError(
            "could not locate specialized public wrapper return "
            f"(found {count})"
        )
    text = text.replace(
        old_specialized_return,
        new_specialized_return,
        1,
    )
    print("Applied: specialized wrapper emits Reference/Proof separator")
else:
    print("Already applied: specialized wrapper emits Reference/Proof separator")

old_generic_extract = '''  reference_prefix = (
    reference_section
    + "\\n\\n"
  )

  if not rendered.startswith(
    reference_prefix
  ):
    return rendered

  proof = rendered[
    len(
      reference_prefix
    ):
  ].lstrip()
'''

new_generic_extract = '''  reference_prefixes = (
    (
      reference_section
      + "\\n\\n"
    ),
    (
      "使用する結果を先にまとめる.\\n\\n"
      + reference_section
      + "\\n\\n"
    ),
  )
  reference_prefix = next(
    (
      prefix
      for prefix in reference_prefixes
      if rendered.startswith(
        prefix
      )
    ),
    None,
  )

  if reference_prefix is None:
    return rendered

  proof = rendered[
    len(
      reference_prefix
    ):
  ].lstrip()
'''

if new_generic_extract not in text:
    count = text.count(old_generic_extract)
    if count != 1:
        raise RuntimeError(
            "could not locate generic wrapper prefix extraction "
            f"(found {count})"
        )
    text = text.replace(
        old_generic_extract,
        new_generic_extract,
        1,
    )
    print("Applied: generic wrapper accepts pi6_3 legacy reference intro")
else:
    print("Already applied: generic wrapper accepts pi6_3 legacy reference intro")

old_generic_return = '''  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + reference_section
    + "\\n\\n"
    "## 証明\\n\\n"
    + proof.rstrip()
    + "\\n"
  )
'''

new_generic_return = '''  return (
    "# Group proof narrative\\n\\n"
    "## 使用する結果\\n\\n"
    + reference_section
    + "\\n\\n"
    "---\\n\\n"
    "## 証明\\n\\n"
    + proof.rstrip()
    + "\\n"
  )
'''

if new_generic_return not in text:
    count = text.count(old_generic_return)
    if count != 1:
        raise RuntimeError(
            "could not locate generic public wrapper return "
            f"(found {count})"
        )
    text = text.replace(
        old_generic_return,
        new_generic_return,
        1,
    )
    print("Applied: generic wrapper emits Reference/Proof separator")
else:
    print("Already applied: generic wrapper emits Reference/Proof separator")

renderer.write_text(
    text,
    encoding="utf-8",
)

test_source = r'''import pytest

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from web_group_proof import (
  _build_group_proof_rendered_lines,
  build_standard_web_group_proof_view,
)


def _rendered_group_proof(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _assert_reference_proof_boundary(
  rendered: str,
) -> None:
  reference_index = rendered.index(
    "## 使用する結果"
  )
  proof_index = rendered.index(
    "## 証明"
  )
  separator_index = rendered.rfind(
    "\n---\n",
    reference_index,
    proof_index,
  )

  assert separator_index >= 0
  assert (
    reference_index
    < separator_index
    < proof_index
  )
  assert (
    rendered[
      separator_index:
      proof_index
    ].strip()
    == "---"
  )


@pytest.mark.parametrize(
  ("n", "k"),
  (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  ),
)
def test_phase157_r5_r10_public_reference_proof_boundary(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  if "## 使用する結果" not in rendered:
    pytest.skip(
      "this proof has no reference section"
    )

  assert "## 証明" in rendered
  _assert_reference_proof_boundary(
    rendered
  )


def test_phase157_r5_r10_pi6_3_legacy_intro_is_normalized():
  rendered = _rendered_group_proof(
    3,
    3,
  )

  assert rendered.startswith(
    "# Group proof narrative"
  )
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  assert (
    "使用する結果を先にまとめる."
    not in rendered
  )
  _assert_reference_proof_boundary(
    rendered
  )


@pytest.mark.parametrize(
  ("n", "k"),
  (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  ),
)
def test_phase157_r5_r10_narrative_ends_with_qed(
  n,
  k,
):
  rendered = _rendered_group_proof(
    n,
    k,
  )

  assert rendered.rstrip().endswith(
    r"$\square$"
  )


def test_phase157_r5_r10_separator_parser_recognizes_horizontal_rule():
  rendered_lines = (
    _build_group_proof_rendered_lines(
      (
        "## 使用する結果\n"
        "reference\n"
        "\n"
        "---\n"
        "\n"
        "## 証明\n"
        "proof\n"
        "$\\square$\n"
      )
    )
  )

  assert any(
    line.kind == "separator"
    for line in rendered_lines
  )


def test_phase157_r5_r10_web_adapter_exposes_separator_and_qed():
  view = build_standard_web_group_proof_view(
    3,
    3,
    max_depth=2,
    mode="narrative",
  )

  kinds = tuple(
    line.kind
    for line in view.rendered_lines
  )

  assert "separator" in kinds
  assert any(
    line.kind == "heading"
    and line.prefix == "使用する結果"
    for line in view.rendered_lines
  )
  assert any(
    line.kind == "heading"
    and line.prefix == "証明"
    for line in view.rendered_lines
  )
  assert any(
    any(
      segment.kind == "inline_math"
      and segment.value == r"\square"
      for segment in line.segments
    )
    for line in view.rendered_lines
  )
'''

test_target.write_text(
    test_source,
    encoding="utf-8",
)
print(
    "Written: tests/test_phase157_r5_r10_reference_proof_boundary_qed.py"
)

print("")
print("Phase157 R5-R10 repair4 patch applied successfully.")
print("Changed: toda_group_proof_narrative_renderer.py")
print(
    "Changed: tests/test_phase157_r5_r10_reference_proof_boundary_qed.py"
)
