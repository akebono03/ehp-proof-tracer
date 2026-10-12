# Phase 164 R5 — Web Registry-backed Group Proof

This package connects the confirmed, typed Toda Proposition 5.1 and Equation (5.3) bindings to the `n=3, k=2` group-proof narrative in the Flask Web UI.

Run `run.ps1` from PowerShell after extracting this folder into the project root. The script makes a backup of `web_group_proof.py`, replaces only the full `build_standard_web_group_proof_view` function, adds the new proof bridge, and runs focused tests.

The Phase 162 group source/eta bridge remains an inference-backed subtree. The Phase 164 R4-R8 registry-backed isomorphism is supplied as an actual proof premise to the existing finite-cyclic transport inference, producing a new group conclusion. Other `n,k` pairs, trace, and outline remain on the previous paths.

This package performs no full test suite. It requires the existing R4-R8 modules and Phase 163 manifest. The Web proof explicitly fails if they are missing.
