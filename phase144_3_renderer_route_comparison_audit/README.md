# Phase 144-3 Renderer Route Comparison Audit

Audit only. No production code or tests are modified.

## Purpose

Compare the renderer currently used by CLI/Web with the generalized multi-Argument renderer developed through Phase 143.

Representative targets:

- pi_6^3
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

For every target the audit writes a side-by-side text report containing:

1. legacy/current CLI-Web Narrative;
2. generic multi-Argument Narrative;
3. extracted display-math lines.

This is intended to establish how much of the visible inconsistency comes from legacy target-specific renderer routes rather than from the generalized semantic/Argument machinery itself.

No pytest or full regression is run.
