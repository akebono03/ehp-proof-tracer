# Phase 169 R3M — Prior Database Result Catalog

This package defines a read-only catalog API for group structures that does not query, replay, or require completed proofs. Its inputs are existing typed database results and the project's established literature-position metadata.

This is the first, intentionally isolated step of separating **known group results** from **completed proofs**. It does not wire the catalog into production Backward Search and does not convert an unpositioned CSV row into a fictitious literary reference.

From the repository root, extract the ZIP and run `powershell -ExecutionPolicy Bypass -File .\phase169_r3m_prior_result_catalog\run.ps1`. The script runs only the six focused tests and a read-only audit of three adjacent 2-stem result dependencies. No full pytest suite is run.
