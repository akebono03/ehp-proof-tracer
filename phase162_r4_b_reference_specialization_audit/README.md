# Phase 162 R4-B Reference and Specialization Audit

This is a read-only diagnostic package for the existing EHP Proof Tracer checkout. It compares pi_5^4 and pi_6^5, recording recursive ProofStep ancestry, explicit versus inferred reference origins, presentation reference candidates, and a separately built canonical Toda (4.5) specialization. The separately built comparison step is **not** treated as evidence that it occurs in the root proof tree.

Run `run_phase162_r4_b_reference_specialization_audit.ps1` from the extracted package directory. Results are written to `audit_output/comparison.md` and `audit_output/audit.json`. Only focused tests are executed. No production code or documentation is changed.

A present conclusion or matching string is not a proof that specialization or reference attribution is mathematically justified. Review the recorded ancestry and fixed-statement boundaries before changing rendering behavior.
