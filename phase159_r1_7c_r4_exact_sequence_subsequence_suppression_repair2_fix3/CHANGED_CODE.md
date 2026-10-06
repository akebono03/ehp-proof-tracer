# Phase 159 R1-7c R4 exact-sequence suppression repair2 fix3

## 変更対象

production code の変更はありません。

### `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`

import の変更はありません。

変更テスト関数:

```python
def test_phase157_r20_repair32_full_exactness_uses_intro_sequence_anchor():
  body = _body_pi6_3_repair32()

  exact_sequence_core = (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}"
  )
  eta6_definition = (
    r"$\eta_{6}=E\eta_{5}$."
  )

  assert (
    "次の完全列を考える."
    in body
  )
  assert exact_sequence_core in body
  assert body.index(
    exact_sequence_core
  ) < body.index(
    eta6_definition
  )
```

```python
def test_phase157_r20_repair32_bare_duplicate_full_sequence_is_removed():
  body = _body_pi6_3_repair32()

  duplicate_bare_sequence = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$."
  )
  stale_inline_exactness = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  exact_sequence_core = (
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}"
  )

  assert duplicate_bare_sequence not in body
  assert stale_inline_exactness not in body
  assert body.count(
    exact_sequence_core
  ) == 1
```

## 修正理由

Phase157 の旧 expectation は

```text
$...$ は完全である.
```

という inline math（行内数式）形式を要求していた。

現在の public Narrative は

```text
次の完全列を考える.

\[
...
\]
```

という display math（別行立て数式）形式が正規契約。

repair2 fix2 後の出力では必要な完全列自体は復帰しているため、
production を変更せず stale expectation のみ修正する。

## 完了条件

- Phase157 exactness display regression: PASS
- $\pi_3^2$ focused regression: PASS
- late-prefix helper regression: PASS
- generator canonicalization regression: PASS
- full pytest は実行しない

## 次 Phase との境界

exact-sequence duplication / display contract の整合だけを扱う。
$\eta_2$ 文言、Reference、stable 判定、generator 表記は変更しない。
