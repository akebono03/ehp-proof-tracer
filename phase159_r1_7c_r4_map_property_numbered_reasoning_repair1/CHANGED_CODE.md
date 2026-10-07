# Phase 159 R1-7c R4 numbered map-property reasoning repair1

## 変更対象

### production

`toda_group_proof_narrative_renderer.py`

新規関数追加位置:
`render_toda_group_proof_narrative_markdown()` の直前。

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
    r"^\[R\d+\]より,\s*"
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
        []
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
        []
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
        []
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

  def ensure_tag(
    line_index: int,
    number: int,
  ) -> None:
    line = lines[
      line_index
    ]

    if tag_pattern.search(
      line
    ):
      return

    suffix_index = max(
      line.rfind(
        " は単射."
      ),
      line.rfind(
        " は全射."
      ),
    )

    if suffix_index < 0:
      return

    closing = line.rfind(
      "$",
      0,
      suffix_index,
    )

    if closing < 0:
      return

    lines[
      line_index
    ] = (
      line[
        :closing
      ]
      + r"\tag{"
      + str(
        number
      )
      + "}"
      + line[
        closing:
      ]
    )

  for map_text in tuple(
    isomorphism_by_map
  ):
    injective_rows = injective_by_map.get(
      map_text,
      ()
    )
    surjective_rows = surjective_by_map.get(
      map_text,
      ()
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
      ensure_tag(
        injective_index,
        injective_number,
      )

    if surjective_number is None:
      surjective_number = next_number
      next_number += 1
      ensure_tag(
        surjective_index,
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

  return (
    prefix
    + "\n".join(
      lines
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

変更関数全体:

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )
```

import の変更はありません。

### test

新規:
`tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`

必要な import とテスト関数全文:

```python
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


def _public_narrative(
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
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{1}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{2}$ は全射."
    in rendered
  )
  assert (
    r"(1), (2) より, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型写像である."
    not in rendered
  )


def test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning():
  rendered = _public_narrative(
    2,
    1,
  )

  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{1}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{2}$ は全射."
    in rendered
  )
  assert (
    r"(1), (2) より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    in rendered
  )


def test_phase159_r1_7c_r4_delta_pairs_without_isomorphism_are_not_numbered():
  for n, k, map_text in (
    (
      3,
      6,
      r"\Delta: \pi_{9}^{5} \to \pi_{7}^{2}",
    ),
    (
      3,
      7,
      r"\Delta: \pi_{10}^{5} \to \pi_{8}^{2}",
    ),
  ):
    rendered = _public_narrative(
      n,
      k,
    )

    assert (
      "$"
      + map_text
      + "$ は単射."
      in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は全射."
      in rendered
    )
    assert (
      "$"
      + map_text
      + r"\tag{"
      not in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は同型."
      not in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は同型写像である."
      not in rendered
    )


def test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded():
  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  )

  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "---\n\n"
    "## 証明\n\n"
    "$F: A \\to B$ は単射.\n"
    "$F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型写像である.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert (
    r"$F: A \to B\tag{1}$ は単射."
    in normalized
  )
  assert (
    r"$F: A \to B\tag{2}$ は全射."
    in normalized
  )
  assert (
    r"(1), (2) より, $F: A \to B$ は同型."
    in normalized
  )
```

## 変更理由

audit2 で同一写像の単射・全射ペアは6件。

- 3件は既に番号付き + 同型結論
- 2件（$\pi_9^3$, $\pi_{10}^3$ の $\Delta$）は同型 step / 同型文なし
- 1件（$\pi_{11}^6$ の $H$）は単射・全射・同型文があるが未番号

audit3/audit4 により、$\pi_{11}^6$ の同型文は
`TodaHopfInvariantIsomorphismStatement`
かつ
`Toda Hopf invariant injective and surjective implies isomorphism`
由来の synthetic step であることを確認した。

よって semantic inference は追加せず、
既に public に存在する「同一写像の単射・全射・同型」の3文だけを
final public normalization で番号付き推論へ整形する。

## 実行する pytest

- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
- `tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py`
- `tests/test_phase159_r1_7c_r4_exact_sequence_subsequence_suppression_repair1.py`
- `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`
- `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

## 完了条件

- $\pi_{11}^6$ の $H$ が単射・全射とも番号付き
- 同型結論が `(n), (m) より, H は同型.` になる
- $\pi_3^2$ の既存番号付き推論を維持
- $\pi_9^3$, $\pi_{10}^3$ の $\Delta$ に同型を追加しない
- map-property `である` repair を維持
- exact-sequence / generator canonicalization に回帰なし
- full pytest は実行しない

## 次 Phase との境界

この repair は既存 public isomorphism conclusion の番号付き説明への接続だけを扱う。

$\Delta$ に新しい同型 inference rule を追加しない。
証明木の semantic content、Reference、$\eta_2$ 文言、stable 判定には触れない。
