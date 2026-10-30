# Phase 171 R2J-R2 — Cited Cyclic-Generator Hopf Surjectivity

This package adds a narrowly scoped, reusable typed backward-inference path for a Hopf homomorphism whose image contains a generator of a cited finite cyclic codomain. The development target is H: pi_7^3 -> pi_7^5, needed in the later proof of pi_6^3.

The logic has two independent proof obligations. First, specialize an earlier, source-positioned Proposition 5.3 general cyclic-group assertion to the concrete pi_7^5 presentation as an INFERENCE. Second, reconstruct the R2I Hopf equation H(nu' o eta_6) = eta_5 o eta_6 from the original screened Proposition 2.2, Toda (5.3), and eta Definition. A general map rule then derives surjectivity from those two INFERENCE premises.

The exact typed presentation of the generator or its previously registered HyoujiGen ID correspondence is required; the database does not establish the group theorem or the Hopf equation. The adopted Proposition 5.3 transcription is checked again. Historical SOURCE_UNVERIFIED metadata is left untouched, and independent verification of the original printed edition is not claimed.

## Changed files

Production: `phase165_r52_r9_shared_math.py`, `shared_expansion_provider()` only, adding one provider hook. No top-level import changes. New module `source.py`, read-only proof audit, tests, installer, and PowerShell runner are contained in `phase171_r2j_r2_cyclic_hopf_surjective/`.

The installer confirms the `develop` branch and the R2I-reviewed baseline HEAD, refuses an unexpected tracked diff, checks the exact insertion anchor, and preserves LF or CRLF line endings. DryRun does not patch. On initial installation, the original file is backed up under `output/`. During application, complete replacement code, the entire modified production file, and a SHA-256 state file are saved. If the test or audit fails during that installation, the runner restores the original file only if the patched hash still matches. An already-installed package may be rerun without reapplying a patch.

## Scope and limitations

- No new fixed literature assertions or GIVEN proofs are added.
- No previously completed pi_7^5 proof tree is loaded into the target as a leaf.
- Existing unrelated group-root search behavior remains untouched by the new specialization provider.
- Delta=0, E injectivity, and the final pi_6^3 group structure are **not** concluded.
- Only focused pytest is executed. Full pytest belongs to Phase 171 closeout.

Run `run.ps1 -DryRun` first, then `run.ps1` from the repository root. Inspect `output/audit.json` for the reconstructed proof and its cited leaves.
