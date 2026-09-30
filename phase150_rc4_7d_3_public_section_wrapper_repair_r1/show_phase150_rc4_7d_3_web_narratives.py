from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _text(view):
  parts = []
  for line in view.rendered_lines:
    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )
  return "\n".join(parts)


for label, n, k in (
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_16^9", 9, 7),
):
  print("=" * 96)
  print(label)
  print("=" * 96)
  print(
    _text(
      build_standard_web_group_proof_view(
        n,
        k,
        max_depth=2,
        mode="narrative",
      )
    )
  )
  print()
