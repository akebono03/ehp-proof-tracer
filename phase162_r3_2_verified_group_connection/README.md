# Phase 162 R3-2 — Verified Group Proof Web Connection

Changes only the lower verified-proof narrative displayed for n=3, k=2 in Web narrative mode. The upper Group proof rendering, its presentation, and other (n,k) cases are preserved.

The original public Web function name is preserved for compatibility. It now constructs a group-structure root via the existing Phase 162 R2 proof reconstruction, and renders it using the Phase 162 R3 narrative generator. The former isomorphism narrative is used only as the source of its existing Reference section, pending R3-3 reference attribution work.

Implementation: complete replacement `phase162_web_narrative_integration.py`, plus the exact heading change in `web_group_proof.py` applied by a guarded installer with backups.

Run `run_phase162_r3_2.ps1` after extracting in the repository root. Focused tests only.
