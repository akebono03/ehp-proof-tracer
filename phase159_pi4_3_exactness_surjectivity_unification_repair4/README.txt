Phase 159 - pi_4^3 exactness-to-surjectivity repair4

原因
====
surjectivity focused test が public Narrative の conclusion を

  "$E: \pi_3^2 -> \pi_4^3$ は全射."

という特定の文末形式で hard-code していた。

しかし canonical renderer は
  「は全射である.」
を返す契約があり、Phase 159 の後段 prose normalization によって
表面形が変わる場合もある。

今回の変更
==========
test-only。

変更対象:
tests/test_phase159_pi4_3_exactness_surjectivity_unification.py

変更する関数:
test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector()

検証内容:
- E: pi_3^2 -> pi_4^3 の map 表示が存在する
- その paragraph に「全射」が含まれる
- exactness reason body より後に現れる

「である」の有無には依存しない。

実装変更
========
なし。

完了条件
========
- connector normalization focused tests PASS
- surjectivity focused tests PASS
- pi_4^3 kernel exactness prose tests PASS
- Phase 150 exactness-to-map-property regression PASS
- Phase 50 pi_4^3 exactness bridge PASS

Phase 境界
==========
- reason builder は変更しない。
- connector normalizer は今回変更しない。
- Reference selection は変更しない。
- equation numbering は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
