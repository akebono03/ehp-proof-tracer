# Phase 169 R10EQ-R1 — Universal stable representative definition

This patch adds one common definitional inference for a typed stable element rather than one source attestation or mathematical rule per generator. It does not invent group structures, Toda isomorphisms, or citations.

**Repository baseline:** `akebono03/ehp-proof-tracer`, `develop`, commit `3e102f43b5d378d511391e0b3eb5a175f07ac2dc`.

Changes are intentionally limited to a new `phase169_r10eq_r1_universal_stable_definition` package and the whole `shared_expansion_provider` function in `phase165_r52_r9_shared_math.py`. Imports at module level and all existing classes and other functions are unchanged. The runner writes the full new function and replacement full file to its timestamped output directory.

Run in repository root after extraction:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10eq_r1_universal_stable_definition.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10eq_r1_universal_stable_definition\run.ps1"
git status -sb
```

The runner checks the branch and exact HEAD, refuses pre-existing changes to the edited tracked file, makes a byte-exact backup, runs **focused** pytest with cache disabled, searches and replays the 11-stem and 14-stem proof trees, and restores the modified tracked file on failure. No full test suite is run.

The rule's interpretation of `kinds=0` is an **explicit project naming convention**: registered indexed names designate successive representatives of a chosen stable element in the stable range. This is a definitional agreement, not an independent theorem inferred from the CSV. For any unregistered element, an explicit `IteratedSuspension` expression is required. Independent proof of group structure and Toda (4.5) remains mandatory.
