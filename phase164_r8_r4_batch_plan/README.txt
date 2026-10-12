Phase 164 R8-R4 — read-only batch migration planning

Files added only inside this package:
 audit.py: classifies all root production AST ProofStep constructors/inference calls and replacement candidates.
 test_audit.py: complete tests including CP932 Windows UTF-8 handling.
 run.ps1: targeted pytest then read-only inventory report.

Outputs: phase164_r8_r4_output/audit.json and report.md.
No existing project files or APIs changed. This is a classification stage; NOT a claim that R8 is complete.
R8-R5: batch migrate verified categories to common factory; preserve GIVEN origins and replay object identity.
