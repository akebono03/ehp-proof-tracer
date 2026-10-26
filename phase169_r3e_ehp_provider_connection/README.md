# Phase 169 R3E — Connect existing typed EHP subgoal rules

This package makes **one production change**: replaces the complete `shared_expansion_provider()` function in `phase165_r52_r9_shared_math.py`. The change registers the existing `expand_registered_ehp_goal` callable with the shared provider registry. All existing candidate routes and citation screening remain unchanged.

The registered callable only proposes typed backward dependencies for its previously supported EHP cases. It creates no `GIVEN`, proof step, stored completed proof, new source claim, theorem, or group-specific narrative. Its existing n=3 support does **not** establish a general isomorphism theorem for every suspension map.

The supplied `run.ps1` first applies an exact-blob-guarded function replacement, executes focused pytest, then audits a live citation-screened pi4^2 / pi5^3 search. If a test or the live audit fails, it attempts guarded restoration using the saved backup. No full test suite is run.

The full replacement function is under `full_functions/`. The full updated production file is written under `output/` at installation time because the installation preserves the other original production functions verbatim. The original unmodified full file is saved as `output/phase165_r52_r9_shared_math.py.before`.

Expected: pi4^2 stays complete; pi5^3 remains incomplete; the existing EHP root and its typed branches become available as proposals; all four Proposition 4.2 exactness windows retain their candidates; both literature terminal dependencies remain unproved.

Restore manually with `python -B phase169_r3e_ehp_provider_connection/apply.py restore` if desired. The restore operation refuses to overwrite subsequent modifications.
