# Phase 175 R4R14R4 — Generic zero-value transport

This package adds an **isolated, unregistered inference** for transporting a verified equality `c = 0` across a separately proved generator image `E(g) = c`. The composition `c` may have any number of factors, from two upwards. This is not a Toda-specific theorem and does not claim proof completion.

The implementation has no changes to production search, source registries, or renderers. `run.ps1 -DryRun` checks pinned Git blobs, and `run.ps1` runs only focused tests. A subsequent Phase step is required to connect the rule to the shared backward proof provider and to evaluate the remaining EHP exactness obligations.
