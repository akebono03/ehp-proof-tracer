from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)


def backup(path: Path) -> None:
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


def replace_if_needed(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"Already applied: {label}")
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one unapplied match for {label} in {path}, found {count}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"Applied: {label}")


def replace_last_if_needed(
    path: Path,
    old: str,
    new: str,
    guard: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if guard in text:
        print(f"Already applied: {label}")
        return
    index = text.rfind(old)
    if index < 0:
        raise RuntimeError(
            f"final renderer return anchor not found for {label} in {path}"
        )
    updated = text[:index] + new + text[index + len(old):]
    path.write_text(updated, encoding="utf-8")
    print(f"Applied: {label}")


renderer = ROOT / "toda_group_proof_narrative_renderer.py"
web_group_proof = ROOT / "web_group_proof.py"
template = ROOT / "templates" / "index.html"
test_target = ROOT / "tests" / "test_phase157_r5_r10_reference_proof_boundary_qed.py"

for path in (renderer, web_group_proof, template):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)

helper_anchor = '''def _is_phase150_rc4_generic_route_target(\n'''
helper = r'''def _finalize_toda_group_proof_narrative_markdown(
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
renderer_text = renderer.read_text(encoding="utf-8")
if "def _finalize_toda_group_proof_narrative_markdown(" not in renderer_text:
    if helper_anchor not in renderer_text:
        raise RuntimeError("renderer helper insertion anchor not found")
    renderer.write_text(
        renderer_text.replace(helper_anchor, helper + helper_anchor, 1),
        encoding="utf-8",
    )
    print("Applied: narrative finalizer helper")
else:
    print("Already applied: narrative finalizer helper")

replace_if_needed(
    renderer,
    '''    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        phase134_24_pi15_8,\n      )\n    )\n''',
    '''    return (\n      _finalize_toda_group_proof_narrative_markdown(\n        _phase153_r3_10_connect_public_reference_section(\n          presentation,\n          phase134_24_pi15_8,\n        )\n      )\n    )\n''',
    "pi15_8 public route finalization",
)

replace_if_needed(
    renderer,
    '''      return _wrap_phase150_rc4_generic_public_narrative(\n        presentation,\n        rendered,\n      )\n\n    return rendered\n''',
    '''      return (\n        _finalize_toda_group_proof_narrative_markdown(\n          _wrap_phase150_rc4_generic_public_narrative(\n            presentation,\n            rendered,\n          )\n        )\n      )\n\n    return (\n      _finalize_toda_group_proof_narrative_markdown(\n        rendered\n      )\n    )\n''',
    "generic public routes finalization",
)

replace_if_needed(
    renderer,
    '''    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        rendered,\n      )\n    )\n''',
    '''    return (\n      _finalize_toda_group_proof_narrative_markdown(\n        _phase153_r3_10_connect_public_reference_section(\n          presentation,\n          rendered,\n        )\n      )\n    )\n''',
    "pi8_5 public route finalization",
)

replace_last_if_needed(
    renderer,
    '''  return rendered\n''',
    '''  return (\n    _finalize_toda_group_proof_narrative_markdown(\n      rendered\n    )\n  )\n''',
    '''  return (\n    _finalize_toda_group_proof_narrative_markdown(\n      rendered\n    )\n  )\n''',
    "fallback public route finalization",
)

replace_if_needed(
    web_group_proof,
    '''    if self.kind not in (\n      "heading",\n      "text",\n    ):\n      raise ValueError(\n        "kind must be heading or text"\n      )\n''',
    '''    if self.kind not in (\n      "heading",\n      "separator",\n      "text",\n    ):\n      raise ValueError(\n        "kind must be heading, separator, or text"\n      )\n''',
    "web rendered-line separator kind",
)

separator_anchor = '''    if stripped.startswith(\n      "## "\n    ):\n'''
separator_block = '''    if stripped == "---":\n      lines.append(\n        WebGroupProofRenderedLineView(\n          kind="separator",\n          indent_level=0,\n          prefix="",\n          statement_latex=None,\n          suffix="",\n        )\n      )\n      continue\n\n'''
web_text = web_group_proof.read_text(encoding="utf-8")
if separator_block.strip() not in web_text:
    if separator_anchor not in web_text:
        raise RuntimeError("web separator insertion anchor not found")
    web_group_proof.write_text(
        web_text.replace(separator_anchor, separator_block + separator_anchor, 1),
        encoding="utf-8",
    )
    print("Applied: web separator parser")
else:
    print("Already applied: web separator parser")

replace_if_needed(
    template,
    '''              {% if line.kind == "heading" %}\n                <h4>\n                  {{ line.prefix }}\n                </h4>\n              {% else %}\n''',
    '''              {% if line.kind == "heading" %}\n                <h4>\n                  {{ line.prefix }}\n                </h4>\n              {% elif line.kind == "separator" %}\n                <hr class="group-proof-section-separator">\n              {% else %}\n''',
    "web template separator rendering",
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
  separator_index = rendered.index(
    "\n---\n",
  )
  proof_index = rendered.index(
    "## 証明"
  )

  assert (
    reference_index
    < separator_index
    < proof_index
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
print("Phase157 R5-R10 repair1 patch applied successfully.")
print("Changed: toda_group_proof_narrative_renderer.py")
print("Changed: web_group_proof.py")
print("Changed: templates/index.html")
print("Added: tests/test_phase157_r5_r10_reference_proof_boundary_qed.py")
