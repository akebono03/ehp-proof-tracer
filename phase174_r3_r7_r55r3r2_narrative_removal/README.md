# EHP Proof Tracer — Phase 174 R55R3R2

This package removes the complete R55R3 bespoke proof-sentence implementation and its obsolete local installer/tests. It retains certified source bodies by moving their existing, source-screened Reference projection to the common reference module. It adds only ordinary typed-statement formatting for `Prop27TypedHopfDeltaStatement`, `KernelMultipleStatement`, and proven zero equalities.

## Scope

- `phase168_r3_37c_reference_projection.py`: move already-certified R2/R7 reference formulas to the common Reference projection.
- `phase168_r3_5_model_renderer.py`: **remove** the R55R3 bespoke narrative hook. No replacement hook is added.
- `phase168_r3_27_typed_statement_projection.py`: format typed conclusions without selecting a proof target or walking an entire proof tree.
- Delete the reviewed, untracked `phase174_r3_r7_r55r3_common_proof_display` directory and, when present, `phase174_r3_r7_r55r3r1_public_sentence_correction` after strict SHA-256 checks. The preceding read-only R55R2 evidence is retained.

All changes are guarded by Git blob identities and local worktree content validation. The installation is idempotent, fails closed on unknown edits, and does not add proof premises, mathematical inference rules, or Group-query-specific narrative rules.

## Usage

Extract the ZIP directly into the project repository root. Run `run.ps1 -DryRun`, then `run.ps1`. Both calls operate on the local `develop` branch. The real execution runs only focused pytest files plus a production proof/HTTP audit. Complete source files, complete changed functions, and updated import sections are saved in this package's `output` folder.

The original signed Toda (5.10) reference is **not algebraically normalized** by a display-only step. A sign reduction, if required, must be a separately checked generic transformation rather than a hidden narrative rewrite.

Full pytest is deferred until Phase 174 closeout. No existing top-level project documentation is overwritten by this package.
