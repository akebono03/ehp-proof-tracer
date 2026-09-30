# Phase 150 / RC4-5D-1-R1

Audit-harness-only repair.

The original RC4-5D-1 audit imported
`extract_toda_recursive_proof_provenance` from a nonexistent module.
The current repository defines that API in `toda_proof_dependency.py`.

This package changes only the RC4-5D-1 audit script import.

Production changes: none.

Existing test changes: none.

Repository-wide tests remain deferred until the end of Phase 150.
