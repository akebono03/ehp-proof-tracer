# Phase 161-R4-R5 repair1 changed code

## 変更対象

### `toda_prop56_zero_bootstrap.py`

変更 import:

- `LiteratureReference` を `from proof import (...)` に追加。

変更後 import 全文:

- `output/proof_import_after.py.txt`

変更関数:

- `_build_pi4_3_prop51_specialization_link_step()`

関数全文:

- `output/_build_pi4_3_prop51_specialization_link_step.py.txt`

### `toda_literature_statement_boundary.py`

追加 mapping:

```python
"Toda Proposition 5.1 higher eta group relation": "higher_eta_group_relation",
```

これは既存の Proposition 5.1 component

```text
higher_eta_group_relation
```

を fixed statement として認識させるための最小追加。

### test

変更:

- `tests/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py`

テスト全文:

- `output/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py.txt`

## 完了条件

Reference:

$$
\pi_{n+1}^{n}=\mathbb Z/2\{\eta_n\},\qquad n\ge3
$$

が Proposition 5.1 として表示される。

具体形

$$
\pi_4^3=\mathbb Z/2\{\eta_3\}
$$

は Reference ではなく本文にだけ表示され、Proposition 5.1 の `[Rk]` marker
と接続される。

Toda (5.2) の Reference と $\pi_4^2$ の結論は維持する。

全体 pytest は Phase161 終了時まで実行しない。
