Phase157 R11-R14 repair1 — partial apply recovery

前回の R11-R14 は途中まで適用済み。

適用済み:
- generic ORDER dependency ordering
- map-property support before short-exact derivation
- ORDER ordering pipeline call

未適用:
- fixed Reference ancestry-only pruning
- presentation argument at restore call
- R11-R14 regression tests

失敗原因:
`toda_group_proof_narrative_references.py` 内で
`used_step_ids: frozenset[int]` で終わる signature pattern が2箇所あり、
global replace が曖昧だった。

repair1:
- `restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()`
  の関数 slice の中だけを変更。
- contribution renderer の restore call に presentation を渡す。
- R11-R14 regression tests を追加。
- すでに適用済み production ordering は触らない。

Focused pytest only.
Full repository pytest remains deferred until Phase157 closure.
