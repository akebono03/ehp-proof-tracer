import re

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


DEPENDENCY_LABEL_PATTERN = re.compile(
  r"\[B\d{2}\]"
)
RAW_CLASS_NAME_PATTERN = re.compile(
  r"`[A-Z][A-Za-z0-9_]+`"
)
INTERNAL_RULE_PREFIXES = (
  "Toda ",
)
ENGLISH_FRAGMENTS = (
  r"\text{ is ",
  " integration",
  " specialization",
  " semantics",
  " branch",
  " premises",
  " transported decomposition",
  " finite-dimensional",
  " quotient by ",
  " zero-left ",
  " bridge",
)
CONNECTIVE_FRAGMENTS = (
  "より,",
  "の条件のもとで,",
  "次の完全列を考える.",
  "この完全性と両端の写像の性質より,",
)


def _render_case(
  n: int,
  k: int,
) -> str:
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def _issue_categories(
  line: str,
) -> tuple[
  str,
  ...,
]:
  categories = []

  if DEPENDENCY_LABEL_PATTERN.search(
    line
  ):
    categories.append(
      "DEPENDENCY_LABEL"
    )

  if RAW_CLASS_NAME_PATTERN.search(
    line
  ):
    categories.append(
      "RAW_CLASS_NAME"
    )

  if any(
    line.startswith(
      prefix
    )
    for prefix in INTERNAL_RULE_PREFIXES
  ):
    categories.append(
      "INTERNAL_RULE_NAME"
    )

  if any(
    fragment in line
    for fragment in ENGLISH_FRAGMENTS
  ):
    categories.append(
      "ENGLISH_OR_INTERNAL_PHRASE"
    )

  if any(
    fragment in line
    for fragment in CONNECTIVE_FRAGMENTS
  ):
    categories.append(
      "CONNECTIVE"
    )

  return tuple(
    categories
  )


def audit_case(
  n: int,
  k: int,
) -> None:
  rendered = _render_case(
    n,
    k,
  )
  lines = rendered.splitlines()

  issue_rows = []

  for line_number, line in enumerate(
    lines,
    start=1,
  ):
    categories = _issue_categories(
      line
    )

    if not categories:
      continue

    issue_rows.append(
      (
        line_number,
        categories,
        line,
      )
    )

  print("=" * 78)
  print(
    f"n={n}, k={k}"
  )
  print("=" * 78)

  if not issue_rows:
    print(
      "No prose-audit candidates."
    )
    print()
    return

  counts = {}

  for _line_number, categories, _line in issue_rows:
    for category in categories:
      counts[
        category
      ] = counts.get(
        category,
        0,
      ) + 1

  print("COUNTS")
  for category in (
    "DEPENDENCY_LABEL",
    "RAW_CLASS_NAME",
    "INTERNAL_RULE_NAME",
    "ENGLISH_OR_INTERNAL_PHRASE",
    "CONNECTIVE",
  ):
    print(
      f"  {category}: "
      f"{counts.get(category, 0)}"
    )

  print()
  print("CANDIDATES")

  for line_number, categories, line in issue_rows:
    print(
      f"  L{line_number:03d} "
      f"[{', '.join(categories)}]"
    )
    print(
      f"    {line}"
    )

  print()


def main() -> None:
  for n, k in (
    (3, 3),
    (5, 3),
    (8, 7),
    (9, 7),
  ):
    audit_case(
      n,
      k,
    )


if __name__ == "__main__":
  main()
