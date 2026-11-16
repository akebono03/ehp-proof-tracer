# EHP Proof Tracer — Phase 175 R3R11R1

This is the corrected package for Phase 175 R3R11. It fixes three focused
regressions observed on Windows after a successful read-only DryRun: the
Proposition 2.2 source body was absent, the certified Hopf composition chain
was not compressed, and one old Phase 174 R70 **installer pin** test rejected
the already committed and legitimate R3R10 renderer change.

The production change remains **only one complete function replacement**:
`phase171_r20r13_eta_sentence_layout/projection.py::format_complete_proof_sentences`.
The shared presentation helpers live in
`phase175_r3r11_cited_hopf_narrative/projection.py`. No mathematical GIVEN,
inference rule, ProofStep, proof-search path, registry entry, or existing
external API is changed.

## What changed in R3R11R1

* Proposition 2.2 can be recognized by its exactly typed cited GIVEN and
  attached, source-specific LiteratureReference when its citation metadata
  omits the registered assertion IDs. A matching locator without the actual
  cited source ProofStep is insufficient.
* The right-composition formula's display normalizes whitespace while keeping
  its verified mathematical meaning.
* The Hopf chain projector tests the final typed conclusion and its actual
  proof ancestors rather than requiring one specific intermediate expansion
  layout. It hides only its own uncited, explicitly witnessed intermediate
  equalities. The source steps, final equality, and citation numbers remain.
* The focused pytest selection retains the functional R70 regression tests,
  but does not re-run R70's historical installer-baseline pin test, whose
  baseline predates R3R10. R70's production guard and tests are **unchanged**.

## Windows PowerShell

Run from the repository root on `develop`, after the successful R3R10 commit.
Extract this archive with overwrite to replace the failed R3R11 package:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\R3R11R1.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r11_cited_hopf_narrative\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
Write-Output "DRYRUN_EXIT_CODE=$LASTEXITCODE"
```

If that exits with 0, run the focused application and actual public-search
checks:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File $script
Write-Output "R3R11R1_EXIT_CODE=$LASTEXITCODE"
git diff --check
git diff --stat
git status -sb
```

The DryRun is read-only. The full run backs up the original function file,
applies an EOL-preserving exact replacement, executes only listed focused
tests and checks the actual completed public proof and Web outcome. On failure,
the original bytes are restored unless another process modified the file.
Recovery logs are written outside the repository under
`%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r11_cited_hopf_narrative`.

Expected success gate:
`PASS_R3R11R1_CITED_REFERENCES_AND_HOPF_CHAIN_COMPACT`.
The full pytest suite remains reserved for the end of Phase 175.
