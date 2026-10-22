# Phase 168 R2-8(4): Checked Higher-Stem Citation Specialization

This package connects the already registered symbolic Proposition 5.3 eta-squared clause and Proposition 5.6 nu clause to their concrete group goals, using the existing `HyoujiGen.csv` structured-generator builder. It does not register new theorems, create proof steps, or modify publication positions.

Extract the ZIP at the repository root and run `powershell -ExecutionPolicy Bypass -File ".\phase168_r2_8_4_generic_specialization\run.ps1"`.

The patch replaces the complete `resolve_specialized_goal_citing_id()` function in `phase166_r3t_goal_source_binding/goal_source.py`. No imports are changed. The complete replacement is in `replacement_function.py`. The new `specialization.py` module is self-contained. The runner backs up the original resolver, executes focused tests, and reruns the nine-case citation audit. The complete test suite is not executed.

Expected outcomes: nine of nine citation targets resolve, with the previously resolved seven preserved. This remains a citation lookup result, not proof completion.
