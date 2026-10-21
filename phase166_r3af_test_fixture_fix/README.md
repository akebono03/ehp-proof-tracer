# Phase 166 R3-AF Test Fixture Fix

Run `run.ps1` from the EHP Proof Tracer repository root. This package fixes a malformed CSV test fixture to include the `Element` and `gen_coe` columns required by the existing `SphereRepository.get_group()` API. Only the R3-AF test file changes; no production files are modified. The runner backs up the prior test file and executes the three R3-AF focused tests.
