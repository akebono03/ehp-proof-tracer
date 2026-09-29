Phase 143-75AP R11-R5

R11-R4 stopped before production-file writes because the patcher still
depended on an exact multiline import string. The local audit showed the
semantic import content was correct, so R11-R5 removes newline-format
dependence.

変更対象
========
- toda_group_proof_narrative_argument_multi_renderer.py
- toda_group_proof_narrative_argument_body_renderer.py

変更関数
========
- render_toda_group_proof_narrative_multi_argument_markdown()
- render_toda_group_proof_narrative_argument_body_markdown()

import
======
The transitions import is located by AST ImportFrom node, not by raw text.

After change:

from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)

Implementation boundary
=======================
Only existing argument-level DERIVATION source blocks are connected to the
existing generic semantic renderer. No pi_15^8-specific rule, inference
rule, statement type, Web behavior, or future-phase feature is added.

Focused tests only
==================
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase143_51b_aggregate_statement_prose.py
- tests/test_phase134_24_pi15_8_narrative.py
