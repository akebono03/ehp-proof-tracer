# Phase 159 R1-7c R4 exact-sequence suppression repair2 fix5

## 変更対象

production code の変更はありません。

### `tests/test_phase157_r20_repair32_exactness_intro_anchor.py`

import の変更はありません。

変更テスト関数:

```python
def test_phase157_r20_repair32_full_exactness_uses_intro_sequence_anchor():
  body = _body_pi6_3_repair32()
  normalized_body = " ".join(
    body.split()
  )

  exact_sequence_block = (
    r"\[ "
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}. "
    r"\]"
  )
  eta6_definition = (
    r"$\eta_{6}=E\eta_{5}$."
  )

  assert (
    "次の完全列を考える."
    in body
  )
  assert exact_sequence_block in normalized_body
  assert normalized_body.index(
    exact_sequence_block
  ) < normalized_body.index(
    eta6_definition
  )
```

```python
def test_phase157_r20_repair32_bare_duplicate_full_sequence_is_removed():
  body = _body_pi6_3_repair32()
  normalized_body = " ".join(
    body.split()
  )

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
  exact_sequence_block = (
    r"\[ "
    r"\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}. "
    r"\]"
  )

  assert duplicate_bare_sequence not in body
  assert stale_inline_exactness not in body
  assert normalized_body.count(
    exact_sequence_block
  ) == 1
```

## Audit3 で確定した現行表示

$$
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3.
$$

これは4項の display math（別行立て数式）である。

続く

$$
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
$$

は別の display block として存在するため、両者を1つの5項列として
テストしてはいけない。

## 完了条件

- Phase157 exactness display regression PASS
- $\pi_3^2$ focused regression PASS
- late-prefix helper regression PASS
- generator canonicalization regression PASS
- production code 変更なし
- full pytest は実行しない

## 次 Phase との境界

exact-sequence display contract の stale test 修正のみ。
$\eta_2$、Reference、stable 判定、generator 表記には触れない。
