Phase 165 R12-R12: generic EHP exactness consequences and provenance.

From the project root, unpack this ZIP to the project root and run:
 powershell -ExecutionPolicy Bypass -File .\phase165_r12_r12_ehp_consequences\run.ps1

Requires the successfully installed R12-R11 precedence fix.
Modified production file: phase165_r52_r9_shared_math.py (one provider registration).
Added production module: phase165_r12_r12_ehp_consequences.py.
No other project files are modified; full pytest is not run.

The typed exactness consequence can be inferred from the cited Proposition 4.2
specialization. Suspension surjectivity remains OPEN until the zero target
is independently proved. The specific kernel subgroup remains OPEN.
