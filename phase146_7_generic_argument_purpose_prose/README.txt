Phase 146-7 Generic Argument Purpose Prose

Changed production file:
- toda_group_proof_narrative_argument_renderer.py
  - render_toda_group_proof_narrative_argument_header_method_section

Added focused test:
- tests/test_phase146_7_generic_argument_purpose_prose.py

Scope:
Combine an existing NarrativeArgument purpose sentence with its existing
exactness-method transition.

Before:
  $X$ の位数を決定する.そのために、次の完全列を考える.

After:
  $X$ の位数を決定するために、次の完全列を考える.

The rule uses only the existing generic purpose sentence and exactness-method
transition. It contains no pi_6^3, dimension, theorem, or nu-prime routing
condition.

Out of scope:
- Restoring the historical label "EHP 完全列".
- Changing route ownership.
- Changing contribution selection/order.
- Generalizing other historical prose differences.

Full suite:
Not run here. Project policy reserves the full suite for Phase completion.
