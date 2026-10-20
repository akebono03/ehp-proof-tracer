# Phase 166 R3-H: Uniform Registered Source Steps

This package removes the preference for stored `ProofStepLink` objects from the existing explicit publication-order source selector. It treats the `AssertionEntry` content and its recorded position as authoritative and constructs new source steps consistently. The patch is guarded and saves a backup.

Run `run.ps1` at the repository root after Phase 166 registry_uniform_links has been installed. This package does not alter the implicit-target Web route, transport expansion, or rendering. It performs only targeted tests.
