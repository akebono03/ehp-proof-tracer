# Phase 165 R52-R12: cited component bridge

This package connects searchable components of source-backed composite statements to the shared backward proof search.

## Changes

- New `phase165_r52_r12_component_bridge.py`: `expand_cited_given_components`.
- New `test_phase165_r52_r12_component_bridge.py`: four targeted tests.
- Existing `phase165_r52_r9_shared_math.py`: one guarded full-function return-site replacement, retaining all other behavior.
- Existing `phase165_typed_component_lookup.py`: unchanged, required from R52-R11.

The installer preserves a backup of the shared module. An `INFERENCE` parent is not silently promoted to a `GIVEN` literature reference. In particular, the older Proposition 5.1 aggregate INFERENCE link remains blocked pending a properly source-backed GIVEN registration. The new mechanism becomes immediately active for any eligible source-backed composite already present in the shared registry.

## Run

Run `run.ps1` at the repository root. It executes only relevant targeted pytest modules. No full pytest run is performed.
