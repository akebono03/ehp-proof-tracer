Phase 165 R12-R13: generic image-to-kernel integration.

Run from the project root in PowerShell:
Expand-Archive -Path "$HOME\Downloads\phase165_r12_r13_kernel_image.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r13_kernel_image\run.ps1"

The installer checks installed R11/R12 files and patches only the provider setup
in phase165_r52_r9_shared_math.py (backup: .r12_r13.bak).
It adds phase165_r12_r13_kernel_image.py, seven focused tests, and an audit.
This phase derives the TYPE of a concrete Ker(E) from Im(Delta) and exactness;
it does not assert the kernel is proved until upstream references and recursive
proofs close. It does not run full pytest.
