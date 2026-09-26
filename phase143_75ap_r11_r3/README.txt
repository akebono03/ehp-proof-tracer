Phase 143-75AP R11-R3

R11-R2 stopped before writing production files because the current local
body renderer file begins with a UTF-8 BOM (U+FEFF), which ast.parse()
does not accept when passed as an already-decoded Python string.

R11-R3:
- reads production files as bytes;
- decodes with utf-8-sig before AST parsing;
- remembers whether each source file originally had a BOM;
- preserves that BOM state when writing;
- otherwise keeps the R11-R2 implementation unchanged.

変更対象:
- toda_group_proof_narrative_argument_multi_renderer.py
- toda_group_proof_narrative_argument_body_renderer.py

変更する関数:
- render_toda_group_proof_narrative_multi_argument_markdown()
- render_toda_group_proof_narrative_argument_body_markdown()

import変更:
- toda_group_proof_narrative_argument_multi_renderer.py に
  TodaGroupProofNarrativeTransitionRole を追加。

新規クラス・新規関数:
- なし。

テスト変更:
- なし。

Docs変更:
- なし。

Focused tests only:
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase143_51b_aggregate_statement_prose.py
- tests/test_phase134_24_pi15_8_narrative.py

Do not run the full suite yet.
