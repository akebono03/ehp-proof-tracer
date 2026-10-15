# Phase 165 R57-R14: On-demand Recursive Proof Search

This patch adds opt-in recursive reconstruction of ordered earlier group proofs within one query. It never persists completed `ProofStep` objects or synthesizes literature assumptions. A registered order is not proof evidence. Unfinished earlier results are not reusable. No full pytest is run.

Install using `run.ps1` in a checkout with R57-R13 already installed. The existing `ProofOrderCatalog` retains its earlier compatibility interface. The new entry option is `recursive_proof_order_catalog=...`.

This is a prerequisite mechanism, not full automatic selection of order metadata and not a completed Toda (4.5) proof for `pi_5^4`. It does not change the Web entry by default.
