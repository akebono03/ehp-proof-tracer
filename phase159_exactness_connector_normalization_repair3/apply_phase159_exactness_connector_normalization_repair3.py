from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = (
    ROOT
    / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
    ROOT
    / "tests"
    / "test_phase159_exactness_connector_normalization.py"
)


NEW_FUNCTION = r'''def normalize_toda_group_proof_narrative_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  retained = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      stripped == "以上より,"
      and index + 1 < len(
        paragraphs
      )
      and paragraphs[
        index + 1
      ].strip().startswith(
        "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
      )
    ):
      continue

    retained.append(
      paragraph
    )

  normalized_paragraphs = retained
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  exactness_reason_prefixes = (
    "この完全性と ",
    "完全性より,",
  )
  index = 0

  while index < len(
    normalized_paragraphs
  ) - 1:
    stripped = normalized_paragraphs[
      index
    ].strip()

    if stripped not in standalone_connectors:
      index += 1
      continue

    next_paragraph = normalized_paragraphs[
      index + 1
    ]
    next_stripped = next_paragraph.lstrip()

    if (
      stripped == "これより,"
      and next_stripped.startswith(
        exactness_reason_prefixes
      )
    ):
      normalized_paragraphs.pop(
        index
      )
      continue

    separator = (
      "\n"
      if next_stripped.startswith(
        r"\["
      )
      else " "
    )

    normalized_paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  for index, paragraph in enumerate(
    normalized_paragraphs
  ):
    stripped = paragraph.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "次に, "
    ):
      normalized_paragraphs[
        index
      ] = paragraph.replace(
        "次に, ",
        "まず, ",
        1,
      )

    break

  return "\n\n".join(
    normalized_paragraphs
  )
'''


TEST_SOURCE = r'''from toda_group_proof_narrative_contribution_renderer import (
  normalize_toda_group_proof_narrative_connectors,
)


def test_phase159_exactness_connector_normalization_drops_redundant_koreyori():
  markdown = (
    "$\\pi_{4}^{5}=0$.\n\n"
    "これより,\n\n"
    "この完全性と $\\pi_{4}^{5}=0$ より, "
    "$\\operatorname{Im}E=\\ker H=\\pi_{4}^{3}$.\n\n"
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ は全射."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, この完全性と "
    not in rendered
  )
  assert (
    "この完全性と $\\pi_{4}^{5}=0$ より, "
    "$\\operatorname{Im}E=\\ker H=\\pi_{4}^{3}$."
    in rendered
  )


def test_phase159_exactness_connector_normalization_keeps_ordinary_koreyori():
  markdown = (
    "$\\Delta(\\iota_{5})=\\pm2\\eta_{2}$.\n\n"
    "これより,\n\n"
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, "
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
    in rendered
  )


def test_phase159_exactness_connector_normalization_drops_before_kanzensei_yori():
  markdown = (
    "$\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$.\n\n"
    "これより,\n\n"
    "完全性より, "
    "$\\ker E=\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
  )

  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      markdown
    )
  )

  assert (
    "これより, 完全性より,"
    not in rendered
  )
  assert (
    "完全性より, "
    "$\\ker E=\\operatorname{Im}\\Delta="
    "\\mathbb{Z}\\{2\\eta_{2}\\}$."
    in rendered
  )
'''


def replace_function(
    text: str,
    function_name: str,
    replacement: str,
) -> str:
    marker = f"def {function_name}("
    start = text.find(marker)

    if start < 0:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    next_def = text.find(
        "\ndef ",
        start + len(marker),
    )
    if next_def < 0:
        raise RuntimeError(
            f"next function not found after: {function_name}"
        )

    return (
        text[:start]
        + replacement
        + "\n\n"
        + text[next_def + 1:]
    )


def main() -> None:
    if not RENDERER.exists():
        raise FileNotFoundError(
            f"renderer not found: {RENDERER}"
        )

    text = RENDERER.read_text(
        encoding="utf-8"
    )
    text = replace_function(
        text,
        "normalize_toda_group_proof_narrative_connectors",
        NEW_FUNCTION,
    )
    RENDERER.write_text(
        text,
        encoding="utf-8",
    )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 exactness connector "
        "normalization repair3 applied."
    )


if __name__ == "__main__":
    main()
