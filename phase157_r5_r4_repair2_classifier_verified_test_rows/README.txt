Phase157-R5-R4 repair2 — classifier-verified test rows

変更対象:
- tests/test_phase157_r5_r4_generic_reference_selection.py

production code:
- 変更なし

修正:
- stale classification plan の component_key を信用しない。
- current classify_toda_literature_statement_step() に exact locator/rule pair を通す。
- 実際に
  FIXED_STATEMENT + component_key != None,
  PROOF_INTERNAL,
  FIXED_STATEMENT + component_key == None
  を返す3行を自動選択する。
- rule name を推測しない。

focused pytest のみ。
112群再監査と全体 pytest はまだ実行しない。
