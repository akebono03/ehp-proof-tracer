# EHP Proof Tracer — Phase 175 R3R12R3

R3R12R2 completed its read-only DryRun, then failed two focused public
narrative assertions (47 passed, 2 failed) and restored the patched file.
This release corrects the actual fail-closed presentation mismatch: the
old projector searched for `H:` immediately adjacent to the TeX domain,
while the shared typed renderer prints `H: ` with a space and may prefix
its sentence with the verified exactness explanation.

The replacement now checks the full sentence emitted by
`typed_sentence(injective_step.conclusion, injective_step)`, requiring it to
occur exactly once in the displayed proof. It never constructs an
injectivity claim from a string and never changes an underlying ProofStep.
Every original source, generator-image, group-relation and order check
remains. If the typed sentence cannot be found, the entire proof display is
left unchanged.

## Changed files and API

- Existing `phase175_r3r11_cited_hopf_narrative/projection.py`:
  only the complete `project_verified_source_and_hopf_summary()` hook is
  replaced with the already reviewed R3R12 connection. No imports change.
- New Phase 175 package `projection.py`: add the existing `typed_sentence`
  import and replace the complete `project_verified_hopf_lift_conclusion()`.
  All helper functions, classes, and other imports remain unchanged.
- `tests/test_projection.py`: add two tests checking the actual typed
  injectivity sentence and fail-closed behavior when it is missing.
- `audit.py`, `run.ps1` and four package documents: update the R3R12R3
  labels and source-bound acceptance contract.
- The EHP mathematical code, published source references, group database,
  and inference rules are unchanged.

The installer only accepts the Git blob
`258d22589f92fbebdb9c4516dbe72c1f94a98afd` for the previous R3R11R4
projector (LF/CRLF normalized). Its DryRun is read-only and its live run
restores the original projector if any focused test or public audit fails.

## Windows execution

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R12R3.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r12_hopf_conclusion\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R12R3 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R12R3 audit failed" }
git diff --check
git diff --stat
git status -sb
```

## Acceptance gate

DryRun: `PASS_R3R12R3_READ_ONLY_DRYRUN`.

Real run: `PASS_R3R12R3_VERIFIED_HOPF_ISOMORPHISM_SINGLE_CONCLUSION`.

The source-verified proof of pi_7^3 remains complete with seven references;
the display contains one concluding group relation, and the derivation explains
Hopf surjectivity and isomorphism without introducing new mathematical claims.
The existing pi_6^3 Phase 172 rendering must remain unchanged.

Only the focused pytest paths in `audit.py` are executed. The full
repository suite remains reserved for the end of Phase 175; the next
mathematical search (R4) is outside this package.
