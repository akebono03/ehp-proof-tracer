# R12-R23 self-contained runtime repair

Run `run.ps1` from the repository root after extraction. This revision removes the runtime dependency on the R12-R22 `audit.py` file. Instead, it reconstructs the four verified typed proofs using existing common search and inference rules, verifies the final ancestry, and invokes the common renderer. It adds no mathematical axioms and changes no existing renderer or rule file.

The script executes only the focused R12-R23 tests and never executes repository-wide pytest. It writes `audit_result.json` and, on successful rendering, `public_narrative.md` in this package directory. Narrative content requires separate human review.
