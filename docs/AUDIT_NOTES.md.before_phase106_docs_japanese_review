# Documentation audit summary — 2026-08-25

## Main corrections

1. The uploaded long-form documentation had detailed current-history text only
   through approximately Phase 5-36, while the code/tests had progressed to
   Phase 5-65.

2. Historical statements such as:
   - greedy premise matching,
   - no pattern variables,
   - no shared bindings,
   - no substitution,
   - only type-based premise combinations,
   were correct at earlier phases but are no longer current limitations.

3. Current implementation includes:
   - exhaustive deterministic backtracking,
   - PatternVariable / VariableBinding,
   - relation-pattern matching,
   - repeated-variable consistency,
   - shared bindings across premises,
   - bindings stored in InferenceMatch,
   - conclusion_pattern substitution,
   - multiple binding assignments producing distinct conclusions,
   - multiple-rule multi-round propagation,
   - branch / merge fixed-point inference.

4. Phase 5-65 is now explicitly treated as:
   `generic inference engine foundation completed`.

5. Phase 6 is defined as:
   `EHP domain inference rules`.

6. Current limitations were rewritten to include only limitations that remain
   true at Phase 5-65:
   - ordinary Python conclusion equality,
   - no first-class alternative-proof collection in the knowledge state,
   - no fully general recursive unification language,
   - unbound conclusion variables substitute to None,
   - combinatorial exhaustive search without indexing/pruning,
   - max_rounds is not semantic cycle detection.

7. The uploaded current inference-rule suite was re-run:
   `423 passed`.
   This is not claimed to be the complete project test-suite count.

## Documentation roles after revision

- README.md: current capabilities and status
- design.md: current architecture and design rules
- development_log.md: chronological history
