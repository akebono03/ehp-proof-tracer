# Phase 174 R3-R7-R2R1 — pytest collection and head-lineage repair

This repair addresses a test-collection failure, not a mathematical proof failure. Several historical Phase 165 test directories have the same import name as a root-level Python source module. Under pytest `--import-mode=importlib`, that test-directory namespace may shadow the module. The focused test runner now selects `--import-mode=prepend` and keeps bytecode/cache output disabled. The same focused test files are preserved and an import-mode regression test is added.

## Reviewed Git lineage

The R3-R7-R1 report records commit `992975395195a0e49955617ba1ae772127036dde`. GitHub `develop` advanced to `c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c` solely by adding the R3-R7-R1 audit package. The R2 report guard checks that exact commit ancestry and that all intervening paths belong to that audit package, in addition to checking nine unchanged mathematical source blobs. Both baseline local HEAD values are accepted; no checkout or commit is performed. Newer GitHub commits require a new review and are not silently accepted.

## Scope

Only files within `phase174_r3_r7_r2_ehp_chain_audit/` are replaced or added: `run.ps1`, `audit.py`, `tests/test_contract.py`, `tests/test_runner_import_mode.py`, `README.md`, and `CODE_FULL_JA.md`. Other R2 audit files are preserved identically in the bundled replacement. Existing production modules, historical test files, mathematical rules, literature assertions, and common renderer are not changed.

## Run

Unzip from the repository root, then invoke `run.ps1 -DryRun` followed by `run.ps1`. Both modes run focused pytest before the read-only audit. The saved R3-R7-R1 report is required. The R2 report is written outside the Git repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r2\ehp_chain_audit.json`. No full pytest suite is run.

## Completion

Focused pytest and both audit modes must pass. The live report must list exactness, Delta-map and predecessor proof obligations without claiming candidates are completed proofs or adding target-specific GIVENs. The following R3-R7-R3 phase may consider new general inference only after inspecting the measured evidence and source ancestry.
