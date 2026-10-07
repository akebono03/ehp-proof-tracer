# Phase 159 $\pi_3^2$ repair18 numbered-locality repair23

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_order_public_unique_preimage_definition_premises()`
- `tests/test_phase159_pi3_2_public_definition_premise_locality.py`
  - module-level expected constants only:
    - `H_INJECTIVE`
    - `E_ISOMORPHISM`
    - `H_SURJECTIVE`
    - `H_ISOMORPHISM`

import の変更はありません。

## `_phase159_order_public_unique_preimage_definition_premises()` 全文

```python
def _phase159_order_public_unique_preimage_definition_premises(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

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
  had_trailing_newline = rendered.endswith(
    "\n"
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if (
      stripped.startswith(
        r"\["
      )
      and stripped.endswith(
        r"\]"
      )
    ):
      display_lines = tuple(
        line.strip()
        for line in stripped.splitlines()
        if line.strip()
      )

      if len(
        display_lines
      ) == 3:
        display_body = display_lines[
          1
        ]
        display_match = re.fullmatch(
          (
            r"(?P<map>.+?)"
            r"\\quad\\text\{"
            r"(?P<property>は単射|は全射)"
            r"\}\.\s*"
            r"\\qquad\s*"
            r"\((?P<number>\d+)\)"
          ),
          display_body,
        )

        if display_match is not None:
          stripped = (
            "$"
            + display_match.group(
              "map"
            )
            + "$ "
            + display_match.group(
              "property"
            )
            + "."
          )

    numbered_connector = re.compile(
      (
        r"^(?:\(\d+\)"
        r"(?:,\s*|\s+と\s+)?)"
        r"+\s*より,\s*"
      )
    )
    stripped = numbered_connector.sub(
      "",
      stripped,
    )

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ].lstrip()

        for reference_prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            reference_prefix
          ):
            stripped = suffix[
              len(
                reference_prefix
              ):
            ]
            break

    for prose_prefix in (
      "完全性より, ",
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
    ):
      if stripped.startswith(
        prose_prefix
      ):
        stripped = stripped[
          len(
            prose_prefix
          ):
        ]
        break

    for verbose, concise in (
      (
        " は単射である.",
        " は単射.",
      ),
      (
        " は全射である.",
        " は全射.",
      ),
      (
        " は零写像である.",
        " は零写像.",
      ),
      (
        " は同型写像である.",
        " は同型.",
      ),
    ):
      if stripped.endswith(
        verbose
      ):
        stripped = (
          stripped[
            :-len(
              verbose
            )
          ]
          + concise
        )
        break

    return stripped.rstrip(
      ".,"
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    line = _render_generic_narrative_step(
      proof_step
    )

    if not line:
      return None

    target_key = match_key(
      line
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  for node in presentation.nodes:
    proof_step = node.proof_step
    definition_line = (
      _phase159_unique_preimage_definition_line(
        proof_step
      )
    )

    if definition_line is None:
      continue

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    visible_premise_records = tuple(
      (
        premise_step,
        paragraph_index_for_step(
          premise_step
        ),
      )
      for premise_step in proof_step.premises
    )

    if any(
      premise_index is None
      for (
        _,
        premise_index,
      ) in visible_premise_records
    ):
      continue

    premise_indices = tuple(
      premise_index
      for (
        _,
        premise_index,
      ) in visible_premise_records
      if premise_index is not None
    )

    if len(
      premise_indices
    ) != len(
      proof_step.premises
    ):
      continue

    definition_index = definition_matches[
      0
    ]
    expected_indices = tuple(
      range(
        definition_index
        - len(
          premise_indices
        ),
        definition_index,
      )
    )

    if premise_indices == expected_indices:
      continue

    premise_paragraphs = tuple(
      paragraphs[
        premise_index
      ]
      for premise_index in premise_indices
    )

    for premise_index in sorted(
      premise_indices,
      reverse=True,
    ):
      paragraphs.pop(
        premise_index
      )

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    definition_index = definition_matches[
      0
    ]
    paragraphs[
      definition_index:
      definition_index
    ] = premise_paragraphs

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result
```

## テスト期待値の変更

テスト関数自体は変更しません。module-level constants のみ現行表示契約へ更新します。

```python
H_INJECTIVE = (
  "\\[\n"
  r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
  r"\quad\text{は単射}. \qquad (1)"
  "\n\\]"
)

E_ISOMORPHISM = (
  r"$E(\iota_{1}) = \iota_{2}$ であるから, "
  r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ は同型."
)

H_SURJECTIVE = (
  "\\[\n"
  r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
  r"\quad\text{は全射}. \qquad (2)"
  "\n\\]"
)

H_ISOMORPHISM = (
  r"(1), (2) より, "
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
)
```

## 変更一覧

1. repair18 の `match_key()` が centered numbered map-property を通常の semantic line に正規化する。
2. `(1), (2) より,` を照合キーから除去する。
3. `[R1] より,` の空白を正しく扱う。
4. $\eta_2$ 定義の direct premises を番号付け後でも直前に再配置できるようにする。
5. repair18 の古い表示定数を repair22 の現行表示へ更新する。
6. Reference、numbered-reasoning、E の導出には触れない。

## 実行する pytest

- `tests/test_phase159_pi3_2_public_definition_premise_locality.py`
- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests/test_phase159_r1_6d_specialization_reference_linkage_finalization.py`
- Reference focused 2 tests

full pytest は Phase 159 終了まで実行しない。

## 完了条件

最終順序が概ね

```text
[R1] より, π_2^1 = 0.
H は単射. (1)

[R1] より, π_1^1 = Z{iota_1}, π_2^2 = Z{iota_2}.
E(iota_1)=iota_2 であるから, E は同型.
E は単射.
Δ は零写像.
H は全射. (2)
(1), (2) より, H は同型.
[R1] より, π_3^3 = Z{iota_3}.
この同型写像により, H(eta_2)=iota_3 となる eta_2 が一意に存在する.
```

となり、repair18 locality 3 tests が PASS すること。

## 次 repair との境界

今回は repair18 ordering と current numbered display の整合だけ。
Reference component selection、GIVEN cleanup、proof graph の変更には進まない。
