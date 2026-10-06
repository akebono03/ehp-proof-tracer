Phase 159-R1-7b repair10

Uses the existing canonical `render_toda_proof_statement_latex()` renderer
for `TodaProp42ExactnessStatement` instead of concatenating raw map-symbol
names such as Unicode Delta.

This preserves canonical LaTeX map labels such as `\Delta`.

No new production import and no group-specific branch.
Focused tests only; no repository-wide pytest.
