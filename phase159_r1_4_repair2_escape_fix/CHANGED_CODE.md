# Phase 159-R1-4 repair2

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_public_exactness_latex()`

## import 変更

なし。

## 変更後関数全体

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
```

## 修正理由

repair1 生成時の escaping により、実コードが以下になっていた。

```python
r"\\xrightarrow{"
r"\\Delta"
```

そのため実際の LaTeX 文字列

```text
\xrightarrow{
\Delta
```

と一致しなかった。

診断では5本すべて `normalized=None` となり、
consolidation helper が一度も対象行を認識できていなかった。

## テスト変更

なし。

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py"
```

```powershell
python -m pytest -q `
  ".\tests\test_phase143_32_exactness_component_latex.py" `
  ".\tests\test_phase143_42_argument_body_contribution_renderer.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
```

## 完了条件

- Phase 159 focused tests 全 PASS。
- exactness related regressions 全 PASS。
- `git diff --check` PASS。
- pi_3^2 public Narrative で完全列が1本だけになる。
- その完全列が `は完全である.` を伴う。

## 次 Phase との境界

Reference attribution、数学規則、stable range、Freudenthal は変更しない。
