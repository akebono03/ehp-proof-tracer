# Phase 159 R1-7c R4 map-property `である` repair1

## 変更対象

### production

`toda_group_proof_narrative_renderer.py`

新規関数追加位置:
`render_toda_group_proof_narrative_markdown()` の直前。

```python
def _phase159_r1_7c_r4_normalize_public_map_property_prose(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = (
    "## 証明\n\n"
  )
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
  proof_body = rendered[
    proof_start:
  ]
  proof_body = proof_body.replace(
    "は単射である.",
    "は単射.",
  )
  proof_body = proof_body.replace(
    "は全射である.",
    "は全射.",
  )

  return (
    rendered[
      :proof_start
    ]
    + proof_body
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

  return (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
```

import の変更はありません。

### test

新規:
`tests/test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py`

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


def test_phase159_r1_7c_r4_public_map_property_prose_removes_dearu():
  targets = (
    (
      6,
      5,
    ),
    (
      6,
      6,
    ),
    (
      7,
      6,
    ),
    (
      9,
      7,
    ),
  )

  for n, k in targets:
    rendered = _public_narrative(
      n,
      k,
    )
    proof_body = rendered.split(
      "## 証明\n\n",
      1,
    )[
      1
    ]

    assert "は単射である." not in proof_body
    assert "は全射である." not in proof_body


def test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    r"$\Delta: \pi_{10}^{9} \to \pi_{8}^{4}$ は単射."
    in rendered
  )
  assert (
    r"$E: \pi_{9}^{4} \to \pi_{10}^{5}$ は全射."
    in rendered
  )
  assert (
    r"[R1] より, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r4_pi16_9_aggregate_line_is_concise():
  rendered = _public_narrative(
    9,
    7,
  )

  assert (
    r"$|\pi_{16}^{9}| = 16$ であり, "
    r"$E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射."
    in rendered
  )


def test_phase159_r1_7c_r4_reference_section_is_not_normalized():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "Reference map は単射である.\n\n"
    "---\n\n"
    "## 証明\n\n"
    "Proof map は単射である.\n"
  )

  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_map_property_prose,
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  assert (
    "Reference map は単射である."
    in normalized
  )
  assert (
    "Proof map は単射."
    in normalized
  )
  assert (
    "Proof map は単射である."
    not in normalized
  )
```

## 変更理由

Audit1〜4 により public Narrative には
`は単射である.` / `は全射である.` が 8 件残存。

一方で contribution renderer 内では同じ文字列が ordering / trimming /
dependency matching にも使われている。

そのため内部文字列を変更せず、Phase158 public contract 組立後の
`## 証明` 部分だけを正規化する。

## 完了条件

- confirmed 4 outputs の proof body に `は単射である.` がない
- confirmed 4 outputs の proof body に `は全射である.` がない
- concise form `は単射.` / `は全射.` が表示される
- Reference section は変更されない
- exact-sequence focused regressions PASS
- generator canonicalization regression PASS
- full pytest は実行しない

## 次 Phase との境界

この repair は public map-property prose の簡潔化だけを扱う。
`は同型である.` は current audit 0 件なので変更しない。
Reference semantic content、$\eta_2$ 文言、stable 判定には触れない。
