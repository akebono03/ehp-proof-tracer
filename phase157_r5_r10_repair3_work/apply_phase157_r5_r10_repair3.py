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
        raise RuntimeError(
            f"missing expected file: {path}"
        )
    backup(path)

old_helper = r'''def _finalize_toda_group_proof_narrative_markdown(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.rstrip().splitlines()

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  if (
    reference_header in lines
    and proof_header in lines
  ):
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )

    if reference_index < proof_index:
      separator_index = proof_index

      while (
        separator_index > 0
        and not lines[
          separator_index - 1
        ].strip()
      ):
        separator_index -= 1

      if (
        separator_index == 0
        or lines[
          separator_index - 1
        ].strip() != "---"
      ):
        lines[
          separator_index:separator_index
        ] = [
          "",
          "---",
          "",
        ]

  while (
    lines
    and not lines[-1].strip()
  ):
    lines.pop()

  if (
    not lines
    or lines[-1].strip()
    != r"$\square$"
  ):
    lines.extend(
      (
        "",
        r"$\square$",
      )
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


'''

new_helper = r'''def _finalize_toda_group_proof_narrative_markdown(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.rstrip().splitlines()

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  if (
    reference_header in lines
    and proof_header in lines
  ):
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )

    if reference_index < proof_index:
      before_proof = lines[
        :proof_index
      ]
      proof_and_after = lines[
        proof_index:
      ]

      while (
        before_proof
        and not before_proof[-1].strip()
      ):
        before_proof.pop()

      if (
        before_proof
        and before_proof[-1].strip()
        == "---"
      ):
        before_proof.pop()

        while (
          before_proof
          and not before_proof[-1].strip()
        ):
          before_proof.pop()

      lines = [
        *before_proof,
        "",
        "---",
        "",
        *proof_and_after,
      ]

  while (
    lines
    and not lines[-1].strip()
  ):
    lines.pop()

  if (
    not lines
    or lines[-1].strip()
    != r"$\square$"
  ):
    lines.extend(
      (
        "",
        r"$\square$",
      )
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


'''

replace_once(
    renderer,
    old_helper,
    new_helper,
    "normalize exact Reference/Proof separator block",
)

old_generic_return = r'''    if _is_phase150_rc4_generic_route_target(
      presentation
    ):
      return (
        _finalize_toda_group_proof_narrative_markdown(
          _wrap_phase150_rc4_generic_public_narrative(
            presentation,
            rendered,
          )
        )
      )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        rendered
      )
    )
'''

new_generic_return = r'''    public_rendered = (
      _wrap_phase150_rc4_generic_public_narrative(
        presentation,
        rendered,
      )
    )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        public_rendered
      )
    )
'''

replace_once(
    renderer,
    old_generic_return,
    new_generic_return,
    "use shared public wrapper for pi6_3 and generic routes",
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


def test_phase157_r5_r10_pi6_3_has_explicit_reference_and_proof_sections():
  rendered = _rendered_group_proof(
    3,
    3,
  )

  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered
  _assert_reference_proof_boundary(
    rendered
  )


@pytest.mark.parametrize(
  ("n", "k"),
  (
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
    "Written: "
    "tests/test_phase157_r5_r10_reference_proof_boundary_qed.py"
)

print("")
print(
    "Phase157 R5-R10 repair3 patch applied successfully."
)
print(
    "Changed: toda_group_proof_narrative_renderer.py"
)
print(
    "Changed: "
    "tests/test_phase157_r5_r10_reference_proof_boundary_qed.py"
)
