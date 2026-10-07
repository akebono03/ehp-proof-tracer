# Phase 159 R1-7c R4 generator canonicalization repair1 fix1

## 変更対象

production code の追加変更はありません。
最初の repair1 実行で production 側は既に適用済みです。

### `tests/test_phase143_3_generic_eta_normalization.py`

import の変更はありません。

変更テスト関数全体:

```python
def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )

  assert any(
    r"\eta_{3}^{3}"
    in rendered
    for rendered in rendered_steps
  )
  assert any(
    (
      r"\eta_{3}\eta_{4}\eta_{5}"
      in rendered
    )
    and (
      r"\eta_{3}^{3}"
      in rendered
    )
    for rendered in rendered_steps
  )
```

### `tests/test_phase157_r20_generic_dependency_rendering.py`

import の変更はありません。

変更テスト関数全体:

```python
def test_phase157_r20_reference_dependencies_are_recovered_from_graph():
  rendered = _render_pi6_3_r20()

  for reference in (
    "Proposition 5.6",
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.1",
    "(5.7)",
  ):
    assert reference in rendered

  assert (
    rendered.index(
      "[R5]より"
    )
    < rendered.index(
      "[R3]より"
    )
  )
```

```python
def test_phase157_r20_eta_family_is_canonicalized_generically():
  rendered = _render_pi6_3_r20()

  assert r"\eta_{2}^{3}" in rendered
  assert r"\eta_{3}^{3}" in rendered
  assert r"\eta_{5}" in rendered
  assert r"\eta_{5}^{2}" in rendered

  assert (
    r"\eta_{2}\eta_{3}\eta_{4}"
    not in rendered
  )
  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}$."
    not in rendered
  )
  assert (
    r"E^{2}\eta_{3}"
    not in rendered
  )
```

### `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

新規/再生成ファイルです。
import と4つのテスト関数を含む全文は ZIP 内に収録しています。

## 完了条件

- `$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.` が public Narrative に存在
- `$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\eta_{6}\\}$.` が存在しない
- `$\\eta_{3}\\eta_{4}\\eta_{5}=\\eta_{3}^{3}$` に必要な expanded form は維持
- current R5 locator `(5.7)` を regression が期待
- focused pytest がすべて PASS
- full pytest は実行しない
