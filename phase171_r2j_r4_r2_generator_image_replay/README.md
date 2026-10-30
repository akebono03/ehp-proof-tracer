# Phase 171 R2J-R4-R2 — Source-Bound Generator Image Replay (R1 Repair)

This archive repairs the read-only replay's **local rule-precedence error**. In the original R4-R2 audit, both a citation-backed eta-pair inference and a generic composition inference could be offered for the same two-factor generator image. The shared search requires one valid derivation, and duplicate routes can leave that goal unresolved. The actual production shared provider already prefers the eta-pair route. This repair makes the scoped audit provider behave identically.

The replay reconstructs the typed statement `E(eta_2 o eta_3 o eta_4) = eta_3 o eta_4 o eta_5` using only an earlier, publication-screened Chapter V eta definition. A database group candidate and the screened Toda (5.3) double relation are used only to specify the target expression, not to certify its truth.

**Only audit package files change.** No production implementation, existing production tests, Git history, or repository-wide documentation is modified; no additional GIVEN proof premise is added. The replay still reports `INFERRED` or `UNFINISHED`, and it does not prove the cyclic order-four structure of `pi_6^3`.

## Changed files

- `audit.py`: complete replacements for `scoped_provider` and `main`, without import changes.
- `tests/test_audit.py`: entire updated test module with its import list; two new precedence tests, for seven focused tests total.
- `README.md`, `監査仕様.md`, and `CODE_FULL_JA.md`: complete updated documentation.

## Windows PowerShell

Extract the ZIP into the repository root using `Expand-Archive -Force`. The R4-R1 audit package is still needed because this replay reads its typed goal-creation helper.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r2_generator_image_replay\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r2_generator_image_replay\run.ps1"
```

The focused pytest command disables the pytest cache provider. If proof reconstruction is still incomplete, the summary prints `REASON` and concrete `OPEN_GOAL` entries and writes them to `output/audit.json`. Full pytest is reserved for Phase 171 closeout.
