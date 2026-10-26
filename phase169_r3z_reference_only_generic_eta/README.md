# Phase 169 R3Z — Reference-only general higher-eta statements

This patch changes only the shared, model-backed narrative display. It leaves the
backward search, Proof Tree, proposition registry, typed inferences, cited source
identities, and the six Reference entries unchanged.

A registered symbolic higher-eta source appears only under Reference when a
directly dependent, certified numeric specialization is retained in the proof
body. That derived instance stays citation-linked. No source or proof step is
removed from the narrative model.

## Execute

Unzip the archive at the repository root, then run
`powershell -ExecutionPolicy Bypass -File .\phase169_r3z_reference_only_generic_eta\run.ps1`.

A guarded, AST-verified replacement writes the **complete revised renderer
function and complete module** under `output/`. It backs up exact original bytes
and safely restores them if any focused test or live audit fails. No full test
suite is executed.
