# Phase 165 — Single Narrative Renderer Implementation Cleanup

This installer removes the duplicate implementation file `toda_group_proof_generic_narrative_renderer.py`, preserves its non-rendering helpers in `toda_group_proof_narrative_shared_components.py`, and moves its partial-proof entry into the established `toda_group_proof_narrative_renderer.py`. A small, lazy compatibility *package* under the old import name is retained so existing imports and tests do not immediately break; it has no narrative implementation of its own.

The canonical completed-proof narrative remains unchanged. Incomplete proofs continue to use the same previously validated partial-proof formatting, now hosted in the primary renderer module. This is a structural cleanup, not a rewrite of prose, inference rules, or search.

## Installation

Extract this ZIP into the project root. In PowerShell:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_renderer_single_implementation_cleanup.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_renderer_single_implementation_cleanup\run.ps1"
```

The runner captures completed and partial Narrative Markdown **before** modification, installs the cleanup, runs five targeted tests, and checks exact equality of both outputs after modification. If tests or output comparison fail, it restores the changed project files automatically. The original files are backed up under `.renderer_single_implementation_backup`.

No full pytest suite is executed. A compatibility import package remains by design; removing the old import namespace entirely requires a separate migration of all consumers and historical tests. No proof-search behavior is changed.

## R1 runner correction

The original runner launched `snapshot.py` from its package subdirectory, which
made Python unable to import project-root modules. The R1 runner prepends the
project root to `PYTHONPATH` before taking the baseline, installing, running
focused tests, and comparing outputs. The installer, mathematical code, and
renderer transformation are unchanged. The initial import failure happened
before the installer, so the original project files were not modified.
