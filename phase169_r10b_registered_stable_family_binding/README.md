# Phase 169 R10B — Registered Stable-Family Binding

## Scope

The existing R7 arbitrary-fold cyclic transport checks a chain of proved `GeneratorImage` statements and an independently proved Toda (4.5) isomorphism. R10B makes the *candidate* named generator chain depend on a real row of `data/HyoujiGen.csv`, instead of trusting arbitrary indexed names.

- `kinds=0`: suspension-family notation metadata.
- `id`: stable identity used to match source and target.
- `n`: minimum permitted degree for a family name; **not** the beginning of Freudenthal's stable range.
- `k`: the element's stem, checked against its concrete typed source and target degrees.
- `latex` and `display`: existing canonical symbol and displayed indexed name.

The registry has 40 `kinds=0` rows, including ID 0 (zero). The latter is not a generator: exactly 39 nonzero family records are eligible for typed candidate binding.

The database is **not proof evidence**. This phase does not create any `ProofStep`, `GIVEN`, generator-image equality, Toda isomorphism, or proof-backed group result from metadata. The existing source publication ordering, stable-range guard, and inferred image obligations are unchanged. No new references are inserted.

## Changed Production Function

Only `phase169_r7_general_stable_transport/rule.py::_intermediate_typed_generator` is replaced in full. Its imports and all other functions remain unchanged. It now requires the same registered family ID on both endpoints, with exact typed degrees and a nondecreasing indexed chain; the candidate's intermediate name is reconstructed from the DB's `display` instead of a hard-coded set of families.

The new package's `family_registry.py` provides the complete new dataclass and functions. See `CHANGED_CODE_JA.md` for the complete code of the modified function, the new module, and all new test functions.

## Installation and Limited Verification

From the repository root, in Windows PowerShell:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r10b_registered_stable_family_binding.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r10b_registered_stable_family_binding\run.ps1"
```

The runner validates branch `develop` and R7 function anchors, backs up the existing R7 module, exports the entire replacement function and entire modified file, executes only R10B, R7, R10A, and R10A2 focused pytest, and audits canonical 1- and 2-stem proof/search/Web results. On a failed limited test/audit, it restores the R7 module. No full pytest is executed.

## Phase Boundary

- R10B: metadata identity binding for typed candidates and existing proof obligations.
- Later: connect additional non-eta family definitions to independently verified, publication-positioned proof evidence. In particular, a registered `nu` family does not automatically prove `pi_8^5`, `pi_9^6`, or `pi_10^7`.
