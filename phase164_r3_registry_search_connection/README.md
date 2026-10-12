# Phase 164 R3 — Registry-to-Backward-Search Connection

This package adds an opt-in, fail-closed adapter for the existing concrete proof of the suspension isomorphism E: pi_4^2 -> pi_5^3. No general proof search algorithm, inferred bibliographic order, trusted mathematical evidence, or new renderer is introduced.

Run PowerShell from the repository root after Phase 164 R2:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase164_r3_registry_search_connection.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase164_r3_registry_search_connection\run.ps1"
```

The runner installs one new production module and one new focused test file, then executes only the named tests. It fails rather than overwriting pre-existing target files. There is no repository-wide test run.

## Trust boundary

- Two existing literature-derived inference ProofSteps must each be explicitly bound to an assertion containing the same *typed conclusion*.
- All assertions must pass Phase 164 R2, including a caller-provided independent verification allowlist and the original position checks. An allowlist alone does not verify the Toda source.
- Four existing EHP exactness GIVEN steps must be supplied independently and their roots must be explicitly trusted by the caller.
- Phase 161 R7 checks inference ancestry before the unchanged Phase 161 reconstruction. The final goal uses seven existing inference rules.
- The tests use synthetic, explicitly positioned registry fixtures solely to verify adapter behavior. They do **not** establish that current Phase 163 production assertions have been mathematically verified or that every actual pi_5^3 source assertion is already eligible.

Production registry eligibility evidence and the final mathematical reference review remain explicit work for R4. Existing API signatures and rendering behavior are unchanged.
