# Phase 161-R4-R5 repair17 changed code

## 変更対象

production code の変更なし。

テストのみ変更:

- `tests/test_phase161_r4_r5_repair13_reference_selection_source_binding.py`
  - `test_phase161_r4_r5_repair13_reference_selection_binds_prop51_component_source()`

必要 import の変更なし。

変更後テストファイル全文:

- `output/test_phase161_r4_r5_repair13_reference_selection_source_binding.py.txt`

## stale expectation の内容

repair13 当時は、Reference entry の `proof_steps` から

`Toda Proposition 5.1 finite-dimensional integration`

が消えることを期待していた。

repair14 以降は同じ locator の Proposition 5.1 を1 entry に統合し、

- `Toda Proposition 5.1 higher eta group relation`
- `Toda Proposition 5.1 finite-dimensional integration`

の両方を provenance として保持する。

表示 statement は一般形 higher-eta component を使い、
本文 linkage は concrete $\pi_4^3$ に接続する。

したがって aggregate provenance step の存在自体は正常。

## 完了条件

focused tests で:

- repair16 boundary tests PASS
- repair14 locator dedup tests PASS
- repair13 revised test PASS
- Phase157 current Reference contracts PASS

最終 public $\pi_4^2$ で:

- `[R1] (5.2)`
- `[R2] Proposition 5.1`
- R2 は一般形
- concrete $\pi_4^3$ は Reference に出ない
- `[R2]` は本文の concrete $\pi_4^3$ に付く
- `(5.2)` の $i=4$ specialization
- generator transport
- target conclusion
- `□`

を確認する。

## 次 Phase との境界

今回変更しない:

- `これより, 以上より,` の prose normalization
- Web Provenance header
- Phase144 stale test の整理
- $\pi_5^3$
- $\pi_6^4$
- 全体 pytest
