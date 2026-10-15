# Phase 165 R57-R21-R3 Public Renderer Entry Fix

This targeted patch verifies and updates the public `render_partial_proof_markdown()` entry point so that it delegates to the effective shared Narrative Renderer. It does not change mathematics or proof search. It stops if the actual output still violates the unified narrative contract. Extract at the repository root and run `run.ps1` from PowerShell. Only targeted pytest is executed.
