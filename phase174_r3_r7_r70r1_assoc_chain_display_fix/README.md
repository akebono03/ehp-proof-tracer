# Phase 174 R70R1 — Verified Associativity Bridge Display Fix

This package corrects the R70 complete-proof narrative projection. The certified public proof uses a right-associated composite image, followed by a separately proved associativity inference before applying the cited zero-factor law. R70 had incorrectly assumed the left-associated image directly had two factor-image premises.

The patch changes exactly one function in the existing R70 projection file. It does not change proof rules, registered sources, search providers, the common narrative renderer, or historical tests. The installer rejects unreviewed files, accepts entire LF or CRLF sources, and supports a second safe invocation.

Run `run.ps1 -DryRun` before `run.ps1` from the repository root. The focused pytest and existing R70 public proof audit run on the actual repository. The output gate is `PASS_R70R1_FOCUSED_AND_PUBLIC_ASSOCIATIVITY`.
