# Phase 165 R52-R18: proof-use order

This patch adds an opt-in proof-use ordering filter to the shared backward search. It preserves bibliographic publication order, never grants permission to references excluded by R16, and supports explicitly reviewed same-proposition prerequisite relationships without treating printed component order as proof order.

Run `run.ps1` from the repository root after extracting the ZIP. Only targeted pytest is executed. This patch does not automatically extract or certify proof dependencies from Toda's manuscript and does not register completed internal proofs.

The new `proof_use_order` argument defaults to `None` to preserve existing web behavior until a reviewed goal-to-assertion mapping is supplied.
