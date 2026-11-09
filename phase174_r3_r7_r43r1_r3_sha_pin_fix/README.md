# EHP Proof Tracer Phase 174 R3-R7-R43R1

This patch corrects a single mistaken Git blob SHA pin in the pre-existing R43 source guard.

- File changed: `phase174_r3_r7_r43_public_ehp_map_property_wiring/source_guard.py`.
- Incorrect 35-digit value: `8834cbefbfca18dc01f072c9738a05f7bdc`.
- Correct 40-digit value: `8834cbefbfca5bcca18dc01f072c9738a05f7bdc`.
- No production Python modules, mathematical rules, or proof APIs are modified.
- Source validation, repository ancestry validation, and the previous R43 focused test suite remain intact.
- This patch is safe to rerun: it checks the complete known original or corrected file contents.

## Windows execution

Unzip `R43R1.zip` in the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r43r1_r3_sha_pin_fix\run.ps1"
```

The full run repeats the *existing* R43 guarded installation, audit, and focused regressions; it does not run the full pytest suite. The project root-zero proof is not asserted by this fix.
