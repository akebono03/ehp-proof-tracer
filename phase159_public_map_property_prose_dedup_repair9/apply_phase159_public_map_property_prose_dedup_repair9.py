from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = (
  ROOT
  / "tests"
  / "test_phase159_public_map_property_prose_normalization.py"
)


NEW_FUNCTION = r'''def _phase159_r1_7c_r4_normalize_public_map_property_prose(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  replacements = (
    (
      "は単射である.",
      "は単射.",
    ),
    (
      "は全射である.",
      "は全射.",
    ),
    (
      "は同型写像である.",
      "は同型.",
    ),
    (
      "は同型である.",
      "は同型.",
    ),
    (
      "は零写像である.",
      "は零写像.",
    ),
  )

  normalized = rendered

  for old, new in replacements:
    normalized = normalized.replace(
      old,
      new,
    )

  outer_connector_prefixes = (
    "以上より, ",
    "したがって, ",
    "これより, ",
    "これらより, ",
  )

  paragraphs = normalized.split(
    "\n\n"
  )
  normalized_paragraphs = []

  for paragraph in paragraphs:
    stripped = paragraph.strip()
    replacement = paragraph

    for prefix in outer_connector_prefixes:
      combined_prefix = (
        prefix
        + "完全性より, "
      )

      if stripped.startswith(
        combined_prefix
      ):
        leading_length = (
          len(
            paragraph
          )
          - len(
            paragraph.lstrip()
          )
        )
        leading = paragraph[
          :leading_length
        ]
        replacement = (
          leading
          + stripped[
            len(
              prefix
            ):
          ]
        )
        break

    normalized_paragraphs.append(
      replacement
    )

  normalized = "\n\n".join(
    normalized_paragraphs
  )

  def map_property_key(
    paragraph: str,
  ) -> str | None:
    stripped = paragraph.strip()

    if stripped.startswith(
      "完全性より, "
    ):
      stripped = stripped[
        len(
          "完全性より, "
        ):
      ]

    for suffix in (
      " は単射.",
      " は全射.",
    ):
      if stripped.endswith(
        suffix
      ):
        return stripped

    return None

  exactness_map_property_keys = {
    key
    for paragraph in normalized.split(
      "\n\n"
    )
    if paragraph.strip().startswith(
      "完全性より, "
    )
    for key in (
      map_property_key(
        paragraph
      ),
    )
    if key is not None
  }

  if not exactness_map_property_keys:
    return normalized

  retained = []

  for paragraph in normalized.split(
    "\n\n"
  ):
    stripped = paragraph.strip()
    key = map_property_key(
      paragraph
    )

    if (
      key in exactness_map_property_keys
      and not stripped.startswith(
        "完全性より, "
      )
    ):
      continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


'''


TEST_SOURCE = r'''from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_normalize_public_map_property_prose,
)


def test_phase159_public_map_property_prose_keeps_exactness_injective_once():
  rendered = (
    "## 証明\n\n"
    "以上より, 完全性より, "
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
    "\n\n"
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  sentence = (
    "完全性より, "
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )

  assert normalized.count(
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  ) == 1
  assert normalized.count(
    sentence
  ) == 1
  assert (
    "以上より, 完全性より,"
    not in normalized
  )


def test_phase159_public_map_property_prose_keeps_exactness_surjective_once():
  rendered = (
    "## 証明\n\n"
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
    "\n\n"
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  sentence = (
    "完全性より, "
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )

  assert normalized.count(
    r"$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  ) == 1
  assert normalized.count(
    sentence
  ) == 1


def test_phase159_public_map_property_prose_keeps_standalone_without_exactness_reason():
  rendered = (
    "## 証明\n\n"
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射である."
    "\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射."
    in normalized
  )
  assert (
    "は全射である."
    not in normalized
  )
'''


def replace_function(
  text: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = text.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      f"function not found: {function_name}"
    )

  next_def = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    raise RuntimeError(
      "next function not found after "
      f"{function_name}"
    )

  return (
    text[
      :start
    ]
    + replacement
    + text[
      next_def + 1:
    ]
  )


def main() -> None:
  text = RENDERER.read_text(
    encoding="utf-8"
  )

  text = replace_function(
    text,
    "_phase159_r1_7c_r4_normalize_public_map_property_prose",
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
    "Phase 159 public map-property prose "
    "dedup repair9 applied."
  )


if __name__ == "__main__":
  main()
