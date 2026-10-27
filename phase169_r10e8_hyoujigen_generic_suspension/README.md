# Phase 169 R10E8 — HyoujiGen-driven generic suspension definitions

This is a narrowly scoped implementation package for Toda Chapter VI stable-family citations. The inference rule is **not** changed: `expand_cited_stable_family` remains the sole family-independent derivation engine. Typed family identity, stem, minimum sphere dimension, and canonical naming come from `data/HyoujiGen.csv`.

## Modified production files

- `phase169_r10d2_general_family_definition/family_citation.py`: import the Chapter VI source records and extend the two existing, source-gated family-ID checks in the **entire** `canonical_member` and `cited_family_reference_sentence` functions. The historical Chapter V source registration API and tests remain intact.
- `phase165_r52_r9_shared_math.py`: in the **entire** `build_shared_typed_bridge` function, append the independently registered Chapter VI citation bridge after the existing Chapter V bridge.

## New files and placement

At repository root, unpack the `phase169_r10e8_hyoujigen_generic_suspension/` directory. It contains complete new modules `source_records.py` and `chapter_vi_reference.py`, a complete `patch.py`, a focused `audit.py`, and tests in `tests/test_r10e8_hyoujigen_generic_suspension.py`.

`source_records.py` only stores the three reviewed Chapter VI source clauses and their paragraph boundaries. `chapter_vi_reference.py` validates the source verbatim against the HyoujiGen family identity and the previously reviewed Chapter V order manifest. The resulting source registrations carry checked publication positions **relative to the adopted transcription**, not independently verified original-edition positions.

The fixed source definitions are `GIVEN` leaves. The two member instances and their concrete `GeneratorImage` are `INFERENCE`, using the already-installed rule. CSV identity alone never proves an image.

## Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e8_hyoujigen_generic_suspension.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e8_hyoujigen_generic_suspension\run.ps1"
```

The runner demands the reviewed `develop` HEAD, matching reviewed Git source blobs, and no existing changes to the two modified production files. On pytest or audit failure, it restores both production files byte-for-byte. It runs **only** the R10E8, R10D2, R10E5 and R10E4 targeted tests, then audits the two direct-sum goals. It does **not** run the whole test suite.

## Full replacement units

Following execution, `output/` contains the **complete** updated modules, the **complete** updated import section, and the **complete** revised functions `canonical_member`, `cited_family_reference_sentence`, and `build_shared_typed_bridge`; no code is abbreviated. `run.ps1` performs identical source-guarded replacement in the live repository.

## Completion gate and next phase

R10E8 is locally validated when its three source clauses have unique checked boundaries and fixed-source provenance, each family supports a real three-step cited-to-inferred-to-image proof, existing focused tests pass, and the two group-search statuses are reported without falsely promoting partial results. A full pytest remains reserved for the end of Phase 169. The next step is a Trust Boundary and Narrative verification of any newly completed groups, not additional family-specific rules.
