Phase 162 exactness-window source fix

Only production change:
  toda_group_proof_narrative_exactness_display_contributions.py
  function _exactness_window_latex

Cause: generic renderer returns "$...$ は完全である." but the old
extractor removed dollars only if the string ended in "$". The entire
prose was then wrapped as LaTeX a second time.

This fix extracts only the math part for the exact known suffix, keeps
existing handling for math-only input, and leaves other inputs unchanged.

Focused tests: this package's 4 cases + earlier repair's 4 cases.
No full suite. No proof rules, derivations, or docs changed.
