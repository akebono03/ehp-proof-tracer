Phase 153-R2 Public Narrative Repair Fixed2
===========================================

原因
----
Fixed1 では provenance-only reference の本文表示を

  "[R1]を用いる。"

まで要求していた。

しかし pi_10^6 の Proposition 5.8 は root theorem であり、
public Narrative では次の2箇所で保持される。

1. 冒頭:
   Toda Proposition 5.8を用いる。

2. reference section:
   **[R1] Proposition 5.8.**

leaf premise として "[R1]を用いる。" を出す構造ではない。

Fixed2
------
production code は変更しない。

test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact()
の契約を次へ修正する。

- **[R1] Proposition 5.8.** が reference section に残る。
- Toda Proposition 5.8を用いる。 が root theorem 宣言として残る。
- Toda Proposition 5.8 finite-dimensional integration という
  provenance-only 内部ラベルは public Narrative に出ない。

Phase境界
---------
- production renderer は変更しない。
- Toda45 専用処理は追加しない。
- unresolved rendering 2件は扱わない。
- whole repository pytest は Phase 153 終了時まで実行しない。
