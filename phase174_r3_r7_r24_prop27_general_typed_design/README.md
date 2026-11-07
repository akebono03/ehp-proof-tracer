# Phase 174 R3-R7-R24: Proposition 2.7 typed-rule design audit

This package validates the source and mathematical signature of Toda Proposition 2.7 without modifying production search rules, installing a GIVEN, or creating a verified proof step. The project root must be on `develop` with the reviewed HEAD `5349f850428085a162f5b286deebfaa0bdcfb9d0`. The script never checks out or resets Git state.

Run `run.ps1 -DryRun`, then `run.ps1`. The full test suite is deliberately not run.

The signature specializes the **even** integer `n` to the sequence `pi_(2n+1)^(2n+1) --Delta--> pi_(2n-1)^n --H--> pi_(2n-1)^(2n-1)`. It retains the unsigned assertion `H(Delta(iota_(2n+1))) = +/- 2 iota_(2n-1)` and does not select a sign.

The chapter V margin summary contains a different target index `2m-1`; the chapter II full proposition is the normative source. This audit neither corrects that historical source nor certifies a production proof.
