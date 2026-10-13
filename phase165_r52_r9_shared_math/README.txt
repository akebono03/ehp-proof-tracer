Phase 165 R52-R9: shared typed backward proof search

Scope:
- R38's nine linked GIVEN Source Reference statements become reusable typed
  premises, NOT an already-completed pi3^2 proof tree.
- All n,k goal relations from calculation are newly searched, and must be
  derived from references and common inference rules before being PROVED.
- Generic reverse generator transport is built from the exact linked
  GeneratorImage source facts; no if (n == 2 && k == 1) or pi32_goal equality.
- Existing generic isomorphism, EHP exactness, delta-zero, and diagonal
  suspension expansion modules are reused.
- The old R34 goal-specific equality branch is replaced by a source-witness
  approach, preserving the historical R38 public API and its test.
- Main registered Show proof and Group query progress paths use the same
  underlying typed search. The former still employs the common narrative
  renderer for successfully completed derivations.
- No mathematical fact, fixed Reference, or ProofStep is inferred from
  historical completed proof trees or from untyped SOURCE_ARCHIVE text.

Current explicit boundary:
- This is a generalized engine and leaf binding mechanism. It does NOT
  establish pi4^3 automatically unless a certified typed finite-cyclic
  inference rule and requisite typed source facts are present.
- pi4^3 remains a typed unresolved Relation, not a fake proof.
- Existing old RegisteredProofProvider inventory is retained as a legacy
  API used by targeted tests, but the normal default route no longer uses it.

Changed files and function units:
- phase165_r52_r9_shared_math.py: entirely new module; functions
  build_shared_typed_bridge, shared_expansion_provider, search_shared_group_goal.
- phase165_r52_r7_registered_common_proof.py:
  build_registered_common_replay entire function (R7 old APIs retained).
- phase165_r52_r5_auto_search.py:
  search_group_structure_automatically entire function.
- phase165_r14_r34_backward_search.py:
  phase165_r34_expansions entire function, removes pi32_goal() branch.
- test_phase165_r52_r9_shared_math.py: six complete new tests and imports.

All modified functions / imports are preserved in installed source; the
installer is AST-guided, checks source shapes and makes backups.

How to install:
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r9_shared_math.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r9_shared_math\run.ps1"

Targeted pytest only until Phase closure.
Full pytest: NOT run.
