# Phase 162 R4-B2 Generator Normalization Repair 2

## Purpose

Repair one overly strict test contract without modifying a mathematical inference or rewriting the repository root. The previous test compared full `Relation` objects, including the `HomotopyElement.name` display field. The focused test now verifies the group, order, generator symbol, source, target, and dimensions. A separate test records that name metadata may differ without asserting full `ProofStep` equality.

## Files

- `files/tests/test_phase162_r4_b2_generator_normalization.py`: complete replacement test module
- `run_phase162_r4_b2_generator_normalization_repair2.ps1`: installer and focused tests

## Run

Extract this archive in the EHP Proof Tracer project root. Run the PowerShell script from that root. This package requires Repair 1 already installed.

## Boundary

This is a *test contract* repair only. It does not establish structural equality between the new root and repository root, nor connect the normalized proof to the proof replay. Do not switch the public renderer based on these tests. The full test suite remains reserved for the end of Phase 162.
