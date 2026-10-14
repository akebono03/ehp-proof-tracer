# Phase 165 R52-R15-R1

This is a test-fixture correction only. The established citation checker requires matching, non-empty document `source_id` values to establish intra-document order. R15's new test omitted this required input in both references, so approved citations correctly returned UNKNOWN.

The source reference is now explicitly `Toda`; the citing reference defaults to `Toda`, and a separate test verifies rejection of a different document. No production API, policy, search, or renderer is modified.

Run `run.ps1` from the extracted package. It backs up the previous test file before replacement and executes only focused tests.
