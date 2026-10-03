# Phase157 R5-R10 changed code

## Files / functions

- `toda_group_proof_narrative_renderer.py`
  - add `_finalize_toda_group_proof_narrative_markdown()` immediately before `_is_phase150_rc4_generic_route_target()`
  - change `render_toda_group_proof_narrative_markdown()` so every public Narrative return goes through the finalizer
- `web_group_proof.py`
  - change `WebGroupProofRenderedLineView.__post_init__()`
  - change `_build_group_proof_rendered_lines()`
- `templates/index.html`
  - add rendering branch for `line.kind == "separator"`
- `tests/test_phase157_r5_r10_reference_proof_boundary_qed.py`
  - new focused regression tests

No import changes are required.

## New helper

```python
def _finalize_toda_group_proof_narrative_markdown(
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
```

The complete changed production functions/classes are applied by `apply_phase157_r5_r10.py`, which checks exact current-code anchors before replacing them. No `...` abbreviation is used in the patch or tests.
