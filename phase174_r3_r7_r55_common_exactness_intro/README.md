# Phase 174 R3-R7-R55: One shared exactness introduction

This package repairs only introductory prose for multiple verified EHP exactness chains. The existing common renderer emits the identical group-structure introductory sentence once per independent chain. R55 says that sentence once for the first chain and continues with "さらに" for each later chain, retaining every chain and its citation numbers.

## Safety

The installer pins GitHub develop HEAD `40db3a00ca8be58e589e0949e6a70dcedd3b9cf5` and nine related source Git blob IDs. It changes exactly one existing production file, `phase168_r3_5_model_renderer.py`, and leaves the standard proof engine, mathematical rules, citations, verified ProofSteps, and the public search provider unchanged. It rejects unrelated tracked or staged modifications. No special group/dimension narrative branch is introduced.

## Run

Extract the archive into the project root, then run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r55_common_exactness_intro\run.ps1 -DryRun`; if that succeeds, rerun without `-DryRun`.

The installer creates `FULL_CHANGED_FUNCTIONS.md` containing the complete unabridged before/after `render_model_backed_narrative_markdown()` bodies extracted from the exact local reviewed source. This avoids embedding an incomplete fragment of the long renderer function. The audit uses real in-process Flask POSTs for both `group` and `group_proof`. A live deployed server and browser KaTeX are not claimed.
