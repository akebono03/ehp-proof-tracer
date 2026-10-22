# Phase 168 R3-5: Opt-in Model-backed Web Boundary

This is a narrowly scoped transition step, **not** a replacement of the public default narrative renderer. `build_partial_web_group_proof_view` accepts an optional `narrative_model` argument. The model-backed path renders only references and proof statements already present in the supplied Proof Narrative Model. It does not search a registry or infer citations from names or prose.

The default Web route remains unchanged until the search path can supply its exact screened bridge to the model builder. The model-backed renderer is deliberately concise and does not reproduce the previous long-form proof exposition.

Run `run.ps1` from the repository root on Windows PowerShell. It saves a backup of the modified production Web adapter in `backup/`, installs the two Python modules, runs only focused tests, and then performs a real-search diagnostic of pi_4^2. The full suite is not executed.
