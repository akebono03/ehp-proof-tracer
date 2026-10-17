Phase 165 R12-R15: Toda (5.1) audit import repair

R12-R15's seven focused tests previously passed, but its audit failed because
phase165_r12_r14_kernel_closure resolved to a namespace directory rather than
the expected Python source module. This package preserves existing modules and
restores the uploaded R12-R14 source file only when the root-level file is missing.
It then runs the original R12-R15 installer, seven focused tests, one import
guard test, and the original audit. No full pytest is run.

From the EHP Proof Tracer project root:
  Expand-Archive -Path "$HOME\Downloads\phase165_r12_r15_toda51_import_repair.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r15_toda51_import_repair\run.ps1"

If another root-level R12-R14 source already exists without the required
function, installation aborts without overwriting it.

Completion: pytest passes AND audit completes. A CERTIFIED result in
surjectivity_proof_certified (plus Toda (5.1) ancestry) is needed to claim
successful surjectivity, independently of successful execution.
