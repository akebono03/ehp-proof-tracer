# Phase 166 R3 recovery

This package reverts only the order-only common-search patch and its modified integration test, using the exact backups created by that patch. It checks both backup files before making any change, makes safety copies of the current files, verifies restored SHA-256 hashes, and runs targeted pytest only.

Extract at the project root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r3_recovery\run.ps1
```

The rollback temporarily restores the earlier lookup behavior, which may allow unordered typed references or enforce legacy independent-review checks. It is a recovery step, **not** completion of the agreed order-only policy. Check the actual Web pi_3^2 proof after execution. The next change must diagnose and populate genuine publication/component order metadata before enforcing the order-only gate in production.
