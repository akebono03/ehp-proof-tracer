# EHP Proof Tracer — Phase 173 R4-R15R7

## Source-first abstract Proposition 4.4 certificate

This package adds an **isolated, source-screened proof path for abstract group
invariants** in the n=4 case. It consumes the `TodaProp44AbstractGroupResult`
type introduced in R4-R15R6. It does **not** replace the public group query,
change any existing production file, or certify any generator names.

For all eligible integers k >= 3 with two separately admitted predecessor
groups, Proposition 4.4 gives an abstract decomposition

    pi_(k+4)^4 ~= pi_(k+3)^3 (+) pi_(k+4)^7.

For k=31 the registered predecessor invariant lists jointly describe eight
order-two cyclic summands. This is **not** a named-generator proof for the
registered presentation of pi_35^4.

## Source and proof trust boundaries

1. Read the existing original Chapter V transcription and verify the precise
   Lemma 5.4 archive using the already reviewed source validator.
2. Register the previously verified typed lemma in an **isolated, temporary
   source context**; source-screen the real Proposition 4.4 claim and lemma.
3. Keep the database target out of all GIVEN leaves. Remove any directly cited
   predecessor that would replace the required explicitly adopted DB prior.
4. Resolve the theorem and the typed Hopf identity with the existing registered
   backward proof search. Admit the two preceding group results with the
   existing `admitted_db_step` and independently revalidate them.
5. Run the ordinary inference matcher and proof-step constructor to produce
   exactly one abstract inference certificate. A failure remains unresolved.
6. Never equate a formal suspension expression with a separately named database
   generator and never declare the original public group proof complete.

The abstract certificate is a separate typed result. Current
`search_registered_partial_proof` expects the exact named group relation and
therefore is **not** overridden by this package.

## Install and execute

Extract the ZIP into the EHP Proof Tracer repository root. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r7_source_first_abstract_certificate\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r7_source_first_abstract_certificate\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R15R7 failed" }
```

The script verifies the `develop` branch, the remote/local commit, reviewed
upstream source blobs, and the exact previous R15R6 package content. It permits
an R15R6-only follow-up commit and the known tracked pytest cache change. It
runs focused tests only and never resets, checks out, or patches production
sources.

## Expected outputs

The audit writes `abstract_certificate_report.json` and prints:

    PHASE173_R4_R15R7_HEAD_LINEAGE=PASS
    PHASE173_R4_R15R7_SOURCE_GUARD=PASS
    PHASE173_R4_R15R7_FOCUSED_PYTEST=PASS
    PHASE173_R4_R15R7_K31_SOURCE_FIRST_ABSTRACT=PASS
    PHASE173_R4_R15R7_PUBLIC_COMPLETION=False
    PHASE173_R4_R15R7_AUDIT=PASS

An expected line is not an assertion that the command has already been run on
the user's repository. The source-backed integration result must be measured.

## Files and phase boundary

- `source.py`: source screening, using existing reviewed citation policy.
- `search.py`: separate typed abstract certificate, verified source and DB leaves.
- `audit.py`: inspection and JSON report for k=4,7,8,31.
- `preflight.py`, `run.ps1`: portable reviewed-source guard and focused tests.
- `tests/`: standalone/static and repository-backed regression tests.
- `SOURCE_CODE.md`: complete source and test listing.
- `design.md`: Japanese design and trust-boundary document.

R15R7 establishes the isolated abstract proof step. A later phase may expose
that separately in the public interface without misrepresenting the named
presentation. A full test suite is reserved for the Phase closeout.
