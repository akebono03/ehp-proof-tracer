# Phase 159-R1-6b repair1

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - 新規 `_phase159_normalize_public_reference_map_property_wording()`
  - `render_toda_group_proof_narrative_markdown()`

import:
- 変更なし

test:
- 変更なし

## 新規関数

`_phase159_number_public_map_property_statement()` の直前に追加。

```python
def _phase159_normalize_public_reference_map_property_wording(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]

  pattern = re.compile(
    r"^(?P<prefix>\$.*\$\s+は)"
    r"(?P<property>"
    r"単射である"
    r"|全射である"
    r"|同型写像である"
    r"|零写像である"
    r")\.$"
  )

  normalized_lines = []

  replacement_by_property = {
    "単射である": "単射",
    "全射である": "全射",
    "同型写像である": "同型",
    "零写像である": "零写像",
  }

  for line in reference_body.splitlines():
    match = pattern.match(
      line.strip()
    )

    if match is None:
      normalized_lines.append(
        line
      )
      continue

    leading = line[
      :len(
        line
      )
      - len(
        line.lstrip()
      )
    ]

    normalized_lines.append(
      leading
      + match.group(
        "prefix"
      )
      + replacement_by_property[
        match.group(
          "property"
        )
      ]
      + "."
    )

  normalized_reference = "\n".join(
    normalized_lines
  )

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )
```

## 変更後 `render_toda_group_proof_narrative_markdown()` 全体

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
    _phase159_normalize_public_map_property_wording(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_reference_map_property_wording(
      rendered
    )
  )
  rendered = (
    _phase159_number_public_map_property_statement(
      rendered
    )
  )

  return (
    _phase159_inject_foundational_reference_section(
      presentation,
      rendered,
    )
  )
```

## 変更理由

R1-6b の `(5.1)` attribution 自体は成功している。
失敗しているのは Reference statement の wording だけ。

proof body の既存 public normalizer は Reference section を意図的に対象外としているため、
Reference に残った low-level prose

`は同型写像である.`

を public Reference の formula-style 規則

`は同型.`

へ正規化する。

## pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_6a_foundational_reference_identity.py" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase157_r2_literature_statement_boundary.py" `
  ".\tests\test_phase157_r5_r3_boundary_catalog_expansion.py" `
  ".\tests\test_phase49_low_dimensional_facts.py" `
  ".\tests\test_phase49_generator_transport.py"
```

## 完了条件

- `[R1] (5.1)` attribution を維持。
- `[F...]` は復活しない。
- Reference の E 同型表示が `は同型.`。
- proof body の `(1)`, `(2)` statement numbering を維持。
- focused / related tests PASS。
- `git diff --check` PASS。

## 次 Phase との境界

- 今回は Reference wording のみ。
- `[R1] より` / `完全性より` の body linkage はまだ追加しない。
- full pytest は Phase 159 最後のみ。
