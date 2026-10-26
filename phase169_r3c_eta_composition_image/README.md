# Phase 169 R3C — Composite Eta Suspension Image

This package connects a two-factor eta composition to the already registered, individually proved eta suspensions. It adds one typed backward proposal for a `GeneratorImage` goal: if $E(\alpha)=\alpha'$ and $E(\beta)=\beta'$ are independently proved, then $E(\alpha\circ\beta)=\alpha'\circ\beta'$. At this phase, this rule is restricted to typed consecutive eta-family suspensions, with checked source and target dimensions.

This is **not** proof of the EHP isomorphism $E:\pi_4^2\to\pi_5^3$ and does not finish the $\pi_5^3$ group computation. The existing `ProofStep` search, citation eligibility, and phase R3B group-transport rule are unchanged.

## Scope and files

- Only production file changed: `phase165_r12_r21_eta_generator_chain.py`.
- New functions immediately before `expand_cited_eta_generator`: `_composition_eta_suspensions`, `composition_eta_suspension_image_rule`.
- Existing function replaced as a whole: `expand_cited_eta_generator`.
- Full imports, full updated production file and all complete functions are in `full_files/` and `full_functions/`.
- New full test functions and imports are in `tests/test_phase169_r3c_eta_composition_image.py`.
- `audit.py` reconstructs the generator-image Goal using the actual screened citation context. No fabricated `GIVEN` evidence is installed.
- `apply.py` refuses changes to an unexpected source; `restore.py` restores only when the installed patch remains unchanged.

## Run on Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3c_eta_composition_image.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3c_eta_composition_image\run.ps1"
```

The runner executes only focused pytest, followed by the image-frontier audit. The full test suite is reserved for the end of Phase 169.

## Exit criteria

1. Old single-eta suspension behavior and R3B finite-cyclic transport still work.
2. A two-factor eta composition image yields exactly two separately provable generator-suspension Goals.
3. A checked inference can derive the composite image from two proven suspensions, but not from missing or bare `GIVEN` component steps.
4. Actual source-approved `GeneratorImage` search is recorded in `output/composite_image.json` as `proved` or an explicit unresolved diagnostic.
5. The EHP suspension-isomorphism premise is not supplied as an unverified fact. R3D will address this separately.
