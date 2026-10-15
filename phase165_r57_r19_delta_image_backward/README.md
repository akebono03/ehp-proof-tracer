# Phase 165 R57-R19: Typed Delta-Image Backward Expansion

This package connects the existing `free_cyclic_generator_delta_image_inference_rule()` to shared backward proof search. It does not create new mathematical axioms, group results, or `GIVEN` steps. The signed Delta statement must be present in the screened typed Reference context; the source free-cyclic group relation remains a subgoal that must be proved independently.

Run `run.ps1` from the extracted package. It installs the adapter and runs only R57-R19 and R57-R18 targeted tests, then writes `delta_image_goals.json`. The complete test suite is not run.

The installer requires the R57-R12 shared provider to be unchanged, except for this package's changes, and fails without modifying the project otherwise.
