Phase 147 RC1-3 Repair R1

Repairs only the three issues observed in the first RC1-3 run:
1. Make the apply script tolerant of the current multi-renderer import state.
2. Reuse method-evidence validation before indexing arguments.
3. Compare independently rebuilt exactness components by value, not identity.

The runner stops immediately on failure and runs focused tests only.
