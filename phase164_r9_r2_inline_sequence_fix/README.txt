Phase 164 R9-R2 (inline TeX full-sequence duplication)

Files changed in existing project:
  phase164_r9_narrative_contract.py: replaces the complete helper module.
No production class or proof tree is modified; public renderer already calls helper.

New tests/probe in extracted patch folder:
  test_phase164_r9_r2.py
  probe_web_narrative.py

Guarded by SHA256 of the known R9 helper and the renderer connection.
On failed focused pytest or live Web proof probe, restore helper from backup.

Expected outputs:
  phase164_r9_r2_output/audit.json
  phase164_r9_r2_output/web_probe.json
  phase164_r9_r2_output/pi5_3_narrative.md
  phase164_r9_r2_output/CHANGED_CODE.md

Only targeted pytest; full suite is deferred until final Phase 164 closure.
