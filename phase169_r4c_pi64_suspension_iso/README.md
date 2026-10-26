# Phase 169 R4C — E-isomorphism proof bridge for π₆⁴

This package adds exactly one backward inference route for the suspension isomorphism `E: π₅³ → π₆⁴`.

It requires **two separately inferred properties of the same map**: injectivity from the previously installed R4B, ultimately citing Toda Proposition 4.4, and surjectivity from previously existing generic EHP rules, citing Proposition 4.2 (4.4) and Toda (5.1). It never inserts an isomorphism, group structure, map property, or source relation as a new GIVEN. It does not relax Toda (4.5)'s stable-range requirement.

## Install and run

From the repository root on the `develop` branch, after successfully installing Phase 169 R4B:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r4c_pi64_suspension_iso.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r4c_pi64_suspension_iso\run.ps1"
```

The script checks the exact GitHub baseline blob and exact R4B worktree change before touching `phase165_r52_r9_shared_math.py`. It makes a byte-for-byte backup and restores the original file if any focused pytest or proof audit fails. No other production files, legacy tests, or project documentation are modified. The test scope is six new R4C tests plus existing R4B and R3O focused tests. The full suite is **not** run.

The output directory contains the original file, complete post-change file, complete modified `shared_expansion_provider` function, `audit.json`, and `audit.md`. Even if the standalone suspension isomorphism is proved, the public group goal may still need separate work; consult the reported search status, not the rule's presence, to determine completion.

## R4C1 compatibility update

The R4C1 runner recognizes both audited R4B predecessor states: the pre-R4B Git commit with the exact R4B worktree insertion, and the current develop commit with R4B already committed. It verifies the actual Git blob and the absence of unrelated edits. Mathematical rules, audit criteria, and prior tests remain unchanged. Six focused tests protect this guard.
