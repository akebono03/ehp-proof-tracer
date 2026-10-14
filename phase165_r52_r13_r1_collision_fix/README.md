# Phase 165 R52-R13-R1 — Direct Reference Collision Fix

This patch resolves a duplicate-result collision introduced when Proposition 5.1 was registered as a fixed typed reference. A unique `GIVEN` reference is preferred to reconstructing the same statement by backward inference. A goal without a matching registered reference still expands normally. Existing APIs are preserved.

## Changed files and functions

- `phase165_r3_recursive_search.py`: `reconstruct_registered_goal()`; no import changes. The full replacement function is provided in `CHANGED_CODE.md`.
- `test_phase165_r52_r13_r1_collision_fix.py`: four new test functions, including all imports. Add at repository root.
- `install.py`, `run.ps1`: install and targeted regression runner.

## Usage

Run `run.ps1` from the repository root. This package expects R52-R13 to be installed. No full pytest run is requested. No further mathematical rule expansion is included in this patch.
