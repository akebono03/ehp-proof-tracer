# Phase 164 R4-R8 Test Expectation Repair

This minimal patch updates one regression test to expect the already-existing rejection message for a forged source Statement ID. It does not modify production code, Registry, proof rules, or the renderer.

Extract this archive into the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase164_r4_r8_test_message_repair\run.ps1`.

The runner copies the complete updated test module, performs targeted tests only, then runs the existing registry-backed reconstruction. The full pytest suite is not run.
