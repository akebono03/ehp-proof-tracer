# Phase 165 R52-R23 Existing Rule Adapter

This package adds a narrow reverse-search adapter for four existing Toda pi4^3 inference rules. It does not invent literature premises or complete the proof.

The fifth (Delta-image) rule remains intentionally unresolved because a sourced typed Whitehead-square premise is needed.

Run `run.ps1` from the extracted package folder. The installer makes a backup of the locally installed shared provider before adding the adapter. It is idempotent and refuses an unexpected insertion anchor.

Only focused tests run, not the full suite.
