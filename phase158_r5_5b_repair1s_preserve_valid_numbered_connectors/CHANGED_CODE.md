# Phase 158-R5-5b repair1s changed code

## Production

`toda_group_proof_narrative_contribution_renderer.py`

import 変更なし。

変更関数全文:

```python
def suppress_toda_group_proof_narrative_dangling_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  def numbered_connector_numbers(
    line: str,
  ) -> tuple[
    int,
    ...,
  ] | None:
    stripped = line.strip()

    if (
      not stripped.startswith(
        "("
      )
      or not stripped.endswith(
        "より,"
      )
      or "$" in stripped
      or "[R" in stripped
    ):
      return None

    relation_text = stripped[
      : -len(
        "より,"
      )
    ].strip()
    parts = tuple(
      part.strip()
      for part in relation_text.split(
        " と "
      )
    )

    if not parts:
      return None

    numbers = []

    for part in parts:
      if (
        len(
          part
        ) < 3
        or not part.startswith(
          "("
        )
        or not part.endswith(
          ")"
        )
      ):
        return None

      number_text = part[
        1:-1
      ]

      if not number_text.isdigit():
        return None

      numbers.append(
        int(
          number_text
        )
      )

    return tuple(
      numbers
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  retained_paragraphs = []

  for paragraph_index, paragraph in enumerate(
    paragraphs
  ):
    lines = paragraph.splitlines()

    while lines:
      stripped = lines[
        -1
      ].strip()

      if stripped in standalone_connectors:
        lines.pop()
        continue

      connector_numbers = (
        numbered_connector_numbers(
          stripped
        )
      )

      if connector_numbers is None:
        break

      previous_text = "\n\n".join(
        paragraphs[
          :paragraph_index
        ]
      )
      referenced_tags_exist = all(
        (
          r"\tag{"
          + str(
            number
          )
          + "}"
        )
        in previous_text
        for number in connector_numbers
      )

      next_paragraph = next(
        (
          candidate.strip()
          for candidate in paragraphs[
            paragraph_index + 1:
          ]
          if candidate.strip()
        ),
        "",
      )
      has_following_derivation = (
        "$" in next_paragraph
      )

      if (
        referenced_tags_exist
        and has_following_derivation
      ):
        break

      lines.pop()

    if not lines:
      continue

    normalized = "\n".join(
      lines
    )
    stripped = normalized.lstrip()

    for connector in standalone_connectors:
      prefix = (
        connector
        + " "
      )

      if (
        stripped.startswith(
          prefix
          + "[R"
        )
      ):
        leading = len(
          normalized
        ) - len(
          stripped
        )
        normalized = (
          normalized[
            :leading
          ]
          + stripped[
            len(
              prefix
            ):
          ]
        )
        break

    if normalized.strip():
      retained_paragraphs.append(
        normalized
      )

  return "\n\n".join(
    retained_paragraphs
  )
```

## Test

`tests/test_phase157_r20_repair43_dangling_connector_cleanup.py`

変更後 import 全文:

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_dangling_connectors,
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
```

変更・追加テスト関数全文:

```python
def test_phase157_r20_repair43_has_no_dangling_connector_paragraphs_or_lines():
  body = _body_pi6_3_repair43()
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  for paragraph in body.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    assert stripped not in standalone_connectors

    lines = tuple(
      line.strip()
      for line in paragraph.splitlines()
      if line.strip()
    )

    if not lines:
      continue

    assert lines[
      -1
    ] not in standalone_connectors


def test_phase157_r20_repair43_keeps_valid_numbered_derivation_connector():
  markdown = "\n\n".join(
    (
      r"$a=b\tag{4}$",
      r"$b=c\tag{7}$",
      "(4) と (7) より,",
      r"$a=c$",
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      markdown
    )
  )

  assert "(4) と (7) より," in rendered


def test_phase157_r20_repair43_removes_unreferenced_numbered_connector():
  markdown = "\n\n".join(
    (
      r"$a=b$",
      "(4) と (7) より,",
      r"$a=c$",
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      markdown
    )
  )

  assert "(4) と (7) より," not in rendered
```

既存の以下2テストは変更しない:
- test_phase157_r20_repair43_reference_marker_does_not_keep_redundant_connector_prefix
- test_phase157_r20_repair43_required_reason_sentences_remain

## 完了条件

1. 有効な番号付き connector が残る。
2. 参照 tag のない connector は削除される。
3. Phase 157 standalone dangling cleanup を維持する。
4. tag(1), tag(2) が public normalization 後も残る。
5. group-specific rule を追加しない。
6. eq3 tag(3) が残課題なら次 repair に分離する。
7. repository-wide pytest は実行しない。
