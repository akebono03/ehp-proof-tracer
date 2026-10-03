from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)


def backup(path: Path) -> None:
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


web_group_proof = ROOT / "web_group_proof.py"
test_target = ROOT / "tests" / "test_phase157_r5_r10_reference_proof_boundary_qed.py"

for path in (web_group_proof, test_target):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)

web_text = web_group_proof.read_text(encoding="utf-8")

old_separator_block = (
    '    if stripped == "---":\n'
    '      lines.append(\n'
    '        WebGroupProofRenderedLineView(\n'
    '          kind="separator",\n'
    '          indent_level=0,\n'
    '          prefix="",\n'
    '          statement_latex=None,\n'
    '          suffix="",\n'
    '        )\n'
    '      )\n'
    '      continue\n'
    '\n'
)

if old_separator_block in web_text:
    web_text = web_text.replace(
        old_separator_block,
        "",
        1,
    )

loop_anchor = '    if display_math_lines is not None:\n'
separator_block = old_separator_block

if separator_block + loop_anchor not in web_text:
    count = web_text.count(loop_anchor)
    if count != 1:
        raise RuntimeError(
            "expected exactly one display-math loop anchor in "
            f"{web_group_proof}, found {count}"
        )
    web_text = web_text.replace(
        loop_anchor,
        separator_block + loop_anchor,
        1,
    )
    print("Applied: separator parser before display-math state")
else:
    print("Already applied: separator parser before display-math state")

web_group_proof.write_text(
    web_text,
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
def test_phase157_r5_r10_reference_and_proof_have_visible_boundary(
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
print("Written: tests/test_phase157_r5_r10_reference_proof_boundary_qed.py")

print("")
print("Phase157 R5-R10 repair2 patch applied successfully.")
print("Changed: web_group_proof.py")
print("Changed: tests/test_phase157_r5_r10_reference_proof_boundary_qed.py")
