# Phase 165 R49 — Import Anchor Fix

This replaces the failed R49 installer with a scoped import-block replacement. The original installer accidentally counted occurrences of `TodaSuspensionMap` outside the import block and aborted before writing any production file.

The installer parses both complete patched modules before writing, saves backups, and runs only the R49 targeted pytest through `run.ps1`. It does not change proof rules, Reference selection, or other Phase features. No full pytest.
