# Phase 169 R3F1: Rebase terminal EHP candidates on committed R3E1

This is a guarded repair of the **R3F installation baseline only**. The R3F package aborted before modifying production files because its installer still expected the pre-R3E1 blob of `phase165_r52_r9_shared_math.py`. The current `develop` revision is `2e0b466e...` and contains the committed R3E1 EHP provider.

Extract this ZIP at the repository root. Run in Windows PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3f1_committed_ehp_baseline_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3f1_committed_ehp_baseline_fix\run.ps1"
```

## Scope and safety

The production changes are exactly those intended by R3F: add `expand_registered_ehp_terminal_goal` to `phase165_r14_r5_ehp_connection.py` and replace the complete `shared_expansion_provider` in `phase165_r52_r9_shared_math.py`. The R3E1 registered EHP expansion remains connected. No other production module or existing test is touched.

The installer checks both committed Git blob identities, compares each working file against the committed content (ignoring only a possible UTF-8 BOM/CRLF difference), parses the full resulting modules, prepares both backups and full output files, then writes the two modules. It refuses partial upgrades or unknown local edits. The `restore` command refuses restoration if either file changed after installation.

Focused pytest runs against the new tests and the related established EHP/search tests. A live audit compares actual citation-screened terminal options; it never certifies a completed proof. Any failed focused test or audit triggers guarded restoration. **The full pytest suite is deliberately not run during Phase 169 R3F1.**

The post-install full-module replacement files are saved at `phase169_r3f1_committed_ehp_baseline_fix/output/*.full.py`; the complete replaced functions are included in `full_functions/`. A detailed Japanese implementation note is in `IMPLEMENTATION_NOTES.md`.
