Phase 153-R2 Public Narrative Repair Fixed1
===========================================

原因
----
production repair 自体は成功している。

- existing R2 semantic regression: 2 passed
- existing reference normalization regression: 5 passed
- new public Narrative test の1本目: passed

失敗した2本目は、provenance-only [R1] が compact reference のままであることを
確認する目的だったが、

  "まず、[R1]を用いる。"

という premise lead まで固定していた。

premise ordering により lead は「まず」「また」「さらに」のいずれにもなり得るため、
これは必要以上に強い test contract だった。

Fixed1
------
production code は変更しない。

tests/test_phase153_r2_public_reference_semantic_fact.py のみ変更し、

  assert "まず、[R1]を用いる。" in rendered

を

  assert "[R1]を用いる。" in rendered

へ変更する。

これにより確認する意味は維持される。

- R1 reference marker が本文で使われる。
- provenance-only result は semantic fact に展開されない。
- premise ordering / lead wording は固定しない。

Phase境界
---------
- production renderer は変更しない。
- Toda45 専用処理は追加しない。
- unresolved rendering 2件は扱わない。
- whole repository pytest は Phase 153 終了時まで実行しない。
