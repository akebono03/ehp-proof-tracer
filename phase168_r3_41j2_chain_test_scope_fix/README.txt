Phase 168 R3-41J2 — Separate Reference EHP formula from proof-chain assertion

Root cause of R3-41J1 1 FAIL / 18 PASS:
  The original R3-26a test counted "\\xrightarrow{\\Delta}" across the
  entire narrative. The Proposition 4.2 reference statement legitimately
  contains an EHP sequence with Delta, alongside exactly one rendered
  concrete EHP sequence in the proof. The test should count the proof only.

Production change: REAPPLY the unchanged R3-41J1 renderer function
  phase168_r3_5_model_renderer.py:
  render_model_backed_narrative_markdown() (full function in package).

Existing test correction:
  phase168_r3_26a_after_r3_25a/tests/test_phase168_r3_26_projection.py:
  test_pi32_three_windows_project_one_chain() (complete function in package).
  The original import section and the other existing test are unchanged.

The package has preflight checks, byte-for-byte backups, full resulting
file copies, 20 limited tests, and rollback of BOTH changed files if any
step fails. No mathematical rule, citation registry, proof model,
publication order, legacy implementation, frozen text or unrelated test is
modified. No whole-repository pytest is run.

Windows PowerShell from repository root:
  Expand-Archive -Path "$HOME\Downloads\phase168_r3_41j2_chain_test_scope_fix.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41j2_chain_test_scope_fix\run.ps1"

After success upload:
  phase168_r3_41j2_chain_test_scope_fix/output/review_bundle.zip

A successful limited audit does not imply the frozen original is
verbatim identical to the current narrative; manual review remains required.
