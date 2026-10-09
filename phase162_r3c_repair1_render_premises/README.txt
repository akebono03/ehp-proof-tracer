Phase 162 R3-C Repair 1: use the existing primary-group LaTeX renderer
for TodaSuspensionIsomorphismStatement, preserving the three-premise proof.

Replaces ONLY toda_group_structure_transport_reason.py and the R3-C focused
tests. No inference rules or public renderer entry function change.

Unzip at repository root and run:
  powershell -ExecutionPolicy Bypass -File .\phase162_r3c_repair1_render_premises\run_phase162_r3c_repair1.ps1

Runs only focused tests, then the existing R3-B rendering audit.
