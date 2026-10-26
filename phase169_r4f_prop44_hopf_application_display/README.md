# Phase 169 R4F — Proposition 4.4 Hopf-fibration applicability

## Purpose

Display the correct source-order-safe applicability of Toda Proposition 4.4
when the existing proof derives the suspension injection into sphere dimension four.
The generic statement requires a Hopf invariant ±1 map. The paragraph
immediately preceding Proposition 4.4 establishes the necessary Hopf
fibration for n=4; its projection h:S^7→S^4 is a suitable α.

The later naming of ν₄ in Lemma 5.4 is **not** used to prove Proposition 5.3.
This package changes presentation only and does not create any mathematical
premise or source entry.

## Prerequisites

* Current `develop` checkout of `akebono03/ehp-proof-tracer`.
* Phase 169 R4E has been applied (either uncommitted or committed).
* Previously extracted R4E/R4D/R4C/R3Z focused test packages.
* The reviewed Git blob `324900b180b60e14ce7d310912e4833b1ff89c31` exists locally.

## Run on Windows PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r4f_prop44_hopf_application_display.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4f_prop44_hopf_application_display\run.ps1"
```

The installer patches only `phase168_r3_5_model_renderer.py`, validates the
whole new function, runs focused tests, performs proof-tree/Web projection audit,
then verifies the tracked changes. Failures roll back the production file.
It does not run the full pytest suite.

## Files

* `patch.py`: reviewed R4E baseline and one-function-only patch.
* `audit.py`: proof-tree, publication-screened citation and Web checks.
* `tests/test_r4f_hopf_application.py`: complete source-backed narrative tests.
* `tests/test_r4f_patch_safety.py`: patch safety tests.
* `run.ps1`: safe, repeatable Windows entry point (repeat invocations refuse to double-patch).
* `IMPLEMENTATION_JA.md`: Japanese implementation and phase boundary.

After success the `output/` directory contains:

* `phase168_r3_5_model_renderer.py.before` — pre-change backup.
* `phase168_r3_5_model_renderer.py.FULL` — complete replacement file.
* `render_model_backed_narrative_markdown_FULL.py` — complete replacement function.
* `audit.json`, `audit.md` and `web_narrative.md` — verified results.

## R4F1 regression repair

R4F1 fixes the incorrect exact-string match for the Lemma 5.4 source label
and retains the R4E `"[R2]より, E ... は単射"` rendered sentence.
The Hopf-fibration condition is an additional preceding paragraph, not a
replacement for the verified injection conclusion. Existing R4E tests stay
unchanged. The mathematical inference rules and proof sources are unchanged.
