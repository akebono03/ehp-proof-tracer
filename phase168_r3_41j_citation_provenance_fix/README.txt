Phase 168 R3-41J — proof-linked citation display repair

Scope: one existing function in phase168_r3_5_model_renderer.py.
No new inference, model, source, Reference or Web APIs.

Modification:
- A merged exactness chain retrieves its citation numbers ONLY from its
  existing typed ProofSteps and cited Proposition 4.2 general GIVEN ancestors.
- A typed GeneratorSuspension satisfying the existing eta pairing condition
  retrieves citation numbers ONLY from its cited eta-family general GIVEN
  ancestors. Unrelated generator suspensions are not assigned eta citations.
- The proof narrative retains existing order, mathematics and all steps.
- Unfinished Proof Tree and explicit legacy paths are unchanged.

The full replacement function is modified_function_full.py.
The full replacement module is written to output/full_file.py by install.py.
The only changed production file is phase168_r3_5_model_renderer.py.

Install from repository root via PowerShell:
  Expand-Archive -Path "$HOME\Downloads\phase168_r3_41j_citation_provenance_fix.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41j_citation_provenance_fix\run.ps1"

The installer refuses a changed R3-41I repository source snapshot.
It saves a byte-for-byte backup before writing and restores it if the scoped
pytest or audit fails. Re-running after a rollback is permitted if the backup equals the restored file.

Review the output/review_bundle.zip audit and output/audit.md before closure.
The R3-41I benchmark audit is not a complete proof validity oracle. Narrative
text differences are not automatically mathematical errors, and closure does
NOT mean frozen reference text has been reproduced byte-for-byte.

No repository-wide pytest is invoked. Run the full suite only at the end of Phase 168.
