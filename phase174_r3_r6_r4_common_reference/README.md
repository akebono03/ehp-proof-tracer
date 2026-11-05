# EHP Proof Tracer — Phase 174 R3-R6-R4 Common Reference Body

This package adds source-bound *Reference* prose for the already-registered universal Toda (4.8) and (5.5) statements. It does not alter mathematical proof search, existing proof trees, citations, or registered GIVEN assertions.

## Reviewed baseline

- Repository: `akebono03/ehp-proof-tracer`, branch `develop`.
- Reviewed remote HEAD: `f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9`.
- Accepted local HEADs: that HEAD or its reviewed predecessor `ecbb2fea225c5b88000629d9c025934fcc2d7075`, provided the target file matches the pinned Git blob.
- Target file: `phase168_r3_37c_reference_projection.py`.
- Reviewed target blob: `754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2`.

## Scope

Only the existing `project_reference_bodies()` function is modified. The new `phase174_r3_r6_r4_common_reference/projection.py` contains `project_cited_universal_toda_reference_body()` and verifies that an already-cited source assertion is the exact registered, source-screened universal statement with the expected provenance metadata.

The (4.8) presentation **retains** the conditional hypothesis `Delta(iota_(2n-1))=0` and identifies the double suspension as injective with quotient of order two. The (5.5) presentation retains `n >= 5` and the universal doubled nu-family equation. These are source statements, not assertions that a specific group has already been proved.

No proof engine or family-specific narrative branch is changed. An unrelated reference or a wrong locator has no new body. The previous R3 renderer remains unchanged, including cyclic-group order reasoning and the single displayed proof conclusion.

## Run on Windows PowerShell

From the repository root after extracting the ZIP into `.`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r4_common_reference\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r4_common_reference\run.ps1"
```

The DryRun checks the pinned remote/local HEAD, the reviewed file blob, and the local file contents, and regenerates the bundled complete replacement code in `output/` without writing the production file. The ZIP already contains the full reviewed replacement module and changed function. The real run installs the one guarded change, runs the focused pytest selection with `--import-mode=importlib`, and audits the completed public proof narrative.

A mismatch aborts without overwriting local changes. No full-suite pytest is run; Phase 174 has not closed.
