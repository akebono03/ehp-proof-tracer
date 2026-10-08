# Phase 161-R4-R5 changed code

## 変更対象

### `toda_prop56_zero_bootstrap.py`

import 変更:

`from proof import (...)` に `InferenceRule` を追加する。

変更後 import 全文は:

- `output/proof_import_after.py.txt`

新規関数:

- `_build_pi4_3_prop51_specialization_link_step()`

追加位置:

- `_build_pi4_2_step()` の直前。

変更関数:

- `_build_pi4_2_step()`
- `build_toda_prop56_zero_argument_step()`

各関数全文は `output/` に出力する。

## テスト

新規:

- `tests/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py`

必要 import を含むテストファイル全文は:

- `output/test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py.txt`

## 実装方針

$\pi_4^3=\mathbb Z/2\{\eta_3\}$ の既存 derivation（導出）は保持する。

Proposition 5.1 の一般形 fixed statement を、その concrete $\pi_4^3$ relation
の provenance（由来）として proof graph に接続する。

linkage step 自体には `LiteratureReference` を付与しない。これにより concrete
statement を Reference として誤表示せず、Proposition 5.1 の general statement
を既存 Reference machinery から選択させる。

## pytest

focused tests と directly affected provenance regression のみ実行する。

全体 pytest は Phase161 終了時まで実行しない。

## 次 Phase との境界

R4-R5 では以下を変更しない。

- pi_5^3
- pi_6^4
- stable transport
- Phase157 pi_6^3 Proposition 2.2 / (5.7) regression
- Web Provenance header
- documentation
