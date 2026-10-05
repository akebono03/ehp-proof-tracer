# Phase 159-R1-4 repair1

## 変更対象

- `toda_group_proof_narrative_renderer.py`

## 追加位置

`_phase159_project_generic_semantics_to_public_proof()` の直前に追加:

```python
def _phase159_public_exactness_latex(
  line: str,
) -> str | None:
  stripped = line.strip()

  if (
    not stripped.startswith("$")
    or r"\xrightarrow{" not in stripped
  ):
    return None

  closing_math = stripped.rfind(
    "$"
  )

  if closing_math <= 0:
    return None

  latex = stripped[
    1:closing_math
  ]

  return latex.replace(
    "Δ",
    r"\Delta",
  )


def _phase159_consolidate_public_exactness_lines(
  lines: list[str],
) -> list[str]:
  exactness_by_index = {
    index: latex
    for index, line in enumerate(
      lines
    )
    if (
      latex := _phase159_public_exactness_latex(
        line
      )
    )
    is not None
  }

  if not exactness_by_index:
    return lines

  maximal_indices = []

  for index, latex in exactness_by_index.items():
    is_strict_subsequence = any(
      (
        latex != other_latex
        and latex in other_latex
      )
      for (
        other_index,
        other_latex,
      ) in exactness_by_index.items()
      if other_index != index
    )

    if not is_strict_subsequence:
      maximal_indices.append(
        index
      )

  canonical_index_by_latex = {}

  for index in maximal_indices:
    latex = exactness_by_index[
      index
    ]
    canonical_index_by_latex.setdefault(
      latex,
      index,
    )

  canonical_latex_by_index = {
    index: latex
    for (
      latex,
      index,
    ) in canonical_index_by_latex.items()
  }

  result = []

  for index, line in enumerate(
    lines
  ):
    latex = exactness_by_index.get(
      index
    )

    if latex is None:
      result.append(
        line
      )
      continue

    owner_index = next(
      (
        canonical_index
        for (
          canonical_index,
          canonical_latex,
        ) in canonical_latex_by_index.items()
        if latex in canonical_latex
      ),
      None,
    )

    if owner_index is None:
      result.append(
        line
      )
      continue

    if index != owner_index:
      continue

    result.append(
      "$"
      + canonical_latex_by_index[
        owner_index
      ]
      + "$ は完全である."
    )

  return result
```

## `_phase159_project_generic_semantics_to_public_proof()` の変更

既存 punctuation 処理の直前に次を追加:

```python
  lines = (
    _phase159_consolidate_public_exactness_lines(
      lines
    )
  )
```

## import 変更

なし。

## テスト変更

なし。

## 完了条件

- $\pi_3^2$ の exactness line が1本だけ。
- `Δ` / `\Delta` の差で重複しない。
- 最大の完全列だけが `は完全である.` を伴って残る。
- 包含関係のない別 component は残る。
- focused / related regression / `git diff --check` が PASS。

## 次 Phase との境界

Reference attribution、数学規則、stable range は変更しない。
