# Phase 169 R10D2 — Generic, Source-Cited Stable Family Definitions

This package replaces the single-family adapter approach proposed in R10D. It integrates **one** checked general-family definition mechanism and **one** inference rule for every supported cited series. New families require source records only, not a new Python statement class or rule. It does not assert that the 39 family names found in `HyoujiGen.csv` are automatically proven.

The initial source-verified records are **nu (family ID 4)** and **sigma (family ID 9)**, drawn from the adopted transcription `sources/toda/Toda_05_2.tex`. Eta's existing cited definition and composition route are preserved to avoid breaking established proofs. No unverified family (including mu) is admitted.

**Scope:** `phase165_r52_r9_shared_math.py`, `phase168_r3_37c_reference_projection.py` and this new module only. The R7 general transport remains unchanged. The source-checked family definitions and their specializations do not manufacture group results or suspension isomorphisms.

**Run:** unzip in the EHP Proof Tracer repository root and execute `powershell -ExecutionPolicy Bypass -File .\phase169_r10d2_general_family_definition\run.ps1` on the `develop` branch. The runner executes only focused pytest cases, followed by a read-only provenance/search audit. It rolls back both production files after a failed test or audit.

**Outputs:** `output/*_FULL.py`, full patched source files, backup copies, and `output/audit.json` / `output/audit.md`. The source-order evidence is tied to the adopted transcription, not a verified original edition.

**Important:** Do **not** apply the earlier R10D zip first. The R10D2 installer checks the reviewed, pre-R10D source versions and safely stops if they differ. Unchanged source and proof rules are not rewritten or refactored.
