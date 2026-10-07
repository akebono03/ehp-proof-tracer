# Phase 159 $\pi_3^2$ numbered exactness-prefix repair22

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()`
- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
  - `test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning()`
  - `test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning()`
  - `test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded()`

import の変更はありません。

## `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()` 全文

```python
def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  lines = proof_body.splitlines()

  reference_prefix = re.compile(
    r"^\[R\d+\]\s*より,\s*"
  )
  exactness_prefix = re.compile(
    r"^完全性より,\s*"
  )
  connector_prefix = re.compile(
    r"^\((\d+)\),\s*\((\d+)\)\s+より,\s*"
  )
  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
  )

  def map_property(
    line: str,
    suffix: str,
  ) -> tuple[
    str,
    int | None,
  ] | None:
    stripped = line.strip()
    stripped = reference_prefix.sub(
      "",
      stripped,
    )
    stripped = exactness_prefix.sub(
      "",
      stripped,
    )

    if not stripped.endswith(
      suffix
    ):
      return None

    map_text = stripped[
      :-len(
        suffix
      )
    ].strip()

    tag_match = tag_pattern.search(
      map_text
    )
    tag_number = (
      int(
        tag_match.group(
          1
        )
      )
      if tag_match is not None
      else None
    )
    map_text = tag_pattern.sub(
      "",
      map_text,
    ).strip()

    return (
      map_text,
      tag_number,
    )

  def isomorphism_map(
    line: str,
  ) -> tuple[
    str,
    bool,
  ] | None:
    stripped = line.strip()

    if reference_prefix.match(
      stripped
    ):
      return None

    had_connector = (
      connector_prefix.match(
        stripped
      )
      is not None
    )
    stripped = connector_prefix.sub(
      "",
      stripped,
    )

    for suffix in (
      " は同型.",
      " は同型写像.",
      " は同型である.",
      " は同型写像である.",
    ):
      if stripped.endswith(
        suffix
      ):
        return (
          tag_pattern.sub(
            "",
            stripped[
              :-len(
                suffix
              )
            ].strip(),
          ),
          had_connector,
        )

    return None

  injective_by_map = {}
  surjective_by_map = {}
  isomorphism_by_map = {}

  for index, line in enumerate(
    lines
  ):
    injective = map_property(
      line,
      " は単射.",
    )

    if injective is not None:
      injective_by_map.setdefault(
        injective[0],
        [],
      ).append(
        (
          index,
          injective[1],
        )
      )

    surjective = map_property(
      line,
      " は全射.",
    )

    if surjective is not None:
      surjective_by_map.setdefault(
        surjective[0],
        [],
      ).append(
        (
          index,
          surjective[1],
        )
      )

    isomorphism = isomorphism_map(
      line
    )

    if isomorphism is not None:
      isomorphism_by_map.setdefault(
        isomorphism[0],
        [],
      ).append(
        (
          index,
          isomorphism[1],
        )
      )

  existing_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for line in lines
    for match in tag_pattern.finditer(
      line
    )
  )
  next_number = (
    max(
      existing_numbers,
      default=0,
    )
    + 1
  )

  numbered_map_properties = {}

  for map_text in tuple(
    isomorphism_by_map
  ):
    injective_rows = injective_by_map.get(
      map_text,
      (),
    )
    surjective_rows = surjective_by_map.get(
      map_text,
      (),
    )

    if (
      not injective_rows
      or not surjective_rows
    ):
      continue

    injective_index, injective_number = (
      injective_rows[
        0
      ]
    )
    surjective_index, surjective_number = (
      surjective_rows[
        0
      ]
    )

    if injective_number is None:
      injective_number = next_number
      next_number += 1

    if surjective_number is None:
      surjective_number = next_number
      next_number += 1

    numbered_map_properties[
      injective_index
    ] = (
      map_text,
      "は単射",
      injective_number,
    )
    numbered_map_properties[
      surjective_index
    ] = (
      map_text,
      "は全射",
      surjective_number,
    )

    isomorphism_index, _had_connector = (
      isomorphism_by_map[
        map_text
      ][
        0
      ]
    )
    lines[
      isomorphism_index
    ] = (
      "("
      + str(
        injective_number
      )
      + "), ("
      + str(
        surjective_number
      )
      + ") より, "
      + map_text
      + " は同型."
    )

  output_lines = []

  for index, line in enumerate(
    lines
  ):
    numbered = numbered_map_properties.get(
      index
    )

    if numbered is None:
      output_lines.append(
        line
      )
      continue

    map_text, property_text, number = numbered

    if (
      map_text.startswith(
        "$"
      )
      and map_text.endswith(
        "$"
      )
    ):
      map_text = map_text[
        1:-1
      ]

    output_lines.extend(
      (
        r"\[",
        (
          map_text
          + r"\quad\text{"
          + property_text
          + r"}. \qquad ("
          + str(
            number
          )
          + ")"
        ),
        r"\]",
      )
    )

  return (
    prefix
    + "\n".join(
      output_lines
    )
    + (
      "\n"
      if rendered.endswith(
        "\n"
      )
      else ""
    )
  )
```

## テスト変更の要点

R1-7c の古い inline `\tag{1}` 期待値を、現在の helper と R1-6d が共有している centered contract:

```text
\[
H: ...\quad\text{は単射}. \qquad (1)
\]

\[
H: ...\quad\text{は全射}. \qquad (2)
\]
```

へ更新する。

general helper test には `完全性より, ` を付け、今回の回帰を直接固定する。

## 変更一覧

1. `map_property()` で `完全性より, ` を map identity（写像同一性）から除去する。
2. `[R1]より,` / `[R1] より,` の両 spacing を認識する。
3. Reference / proof linkage / unique-preimage ordering は変更しない。
4. stale inline-tag tests を centered contract へ更新する。

## 実行する pytest

- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests/test_phase159_r1_6d_specialization_reference_linkage_finalization.py`
- `tests/test_phase159_pi3_2_public_definition_premise_locality.py`

full pytest は Phase 159 終了時まで実行しない。

## 完了条件

$\pi_3^2$ 本文が

```text
\[
H: π_3^2 → π_3^3 \quad\text{は単射}. \qquad (1)
\]

...

\[
H: π_3^2 → π_3^3 \quad\text{は全射}. \qquad (2)
\]

(1), (2) より, H: π_3^2 → π_3^3 は同型.
```

となり、Reference linkage と $E(\iota_1)=\iota_2$ 導出も維持されること。

## 次 repair との境界

今回は numbered map-property recognition だけ。
Reference component selection、GIVEN cleanup、proof graph の変更には進まない。
