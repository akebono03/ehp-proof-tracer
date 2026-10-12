# Phase 163 R4-R81 — Live Boundary Bridge Duplicate Audit

This read-only package compares four R80 fixed-statement reference candidates against the actual existing Toda literature component catalog and the existing registry bridge. It reports exact locator matches, preserves component order, and flags equation (4.4) as an alias requiring reconciliation with Proposition 4.2.

Run `run.ps1` from the repository root in Windows PowerShell. The script requires the R80 output JSON and the current repository modules; it runs only focused tests and writes `phase163_r4_r81_output/duplicate_audit.json` and `report.md`.

An absent exact locator does not establish semantic uniqueness across all existing rules, references, or proof steps. No formal mathematical validation, permanent identifier allocation, production registry edits, proof search integration, or full test suite is performed.
