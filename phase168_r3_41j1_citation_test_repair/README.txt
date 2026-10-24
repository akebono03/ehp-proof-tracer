Phase 168 R3-41J1 — focused correction of the R3-41J test failures

Previous R3-41J log: 4 failed, 15 passed, with successful source rollback.

Causes and targeted remedies:
1. The new exactness-chain sentence changed the existing substring
   '次の完全列を考える', violating two older focused tests.
   Keep that exact wording and insert the certified [R...] source just before it.
2. The new fixture linked its Proof Narrative Model to the unscreened input
   bridge. Unlike the public Web route, this could omit statement bodies from
   registered citations. Construct the model with the same context_sink-screened
   bridge returned by backward search; preserve the all-reference-body assertion.

Production file changed: phase168_r3_5_model_renderer.py only.
Changed function: render_model_backed_narrative_markdown() (full text provided).
Test added (only within this package): tests/test_phase168_r3_41j1_citation_provenance.py

Existing source and test files in the repository are not edited except for the
single renderer function. No new ProofStep, rules, citations or legacy paths.

Run at repository root:
  Expand-Archive -Path "$HOME\Downloads\phase168_r3_41j1_citation_test_repair.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41j1_citation_test_repair\run.ps1"

The installer checks the pre-R3-41J renderer SHA256 (from R3-41I) and stops if
R3-41J was not rolled back or other changes intervened. It saves a backup and
rolls back on focused-test or audit failure.

Scoped pytest only, no repository-wide suite until Phase 168 closure.
The R3-41I audit reports frozen-text quality gaps without modifying baselines.
The resulting output/review_bundle.zip is for review, not an automatic closure.
