Phase 161-R4-R4 resume after pycache access denied

Observed failure
================
The R4-R4 apply step completed successfully.

The next command failed in `py_compile` because Windows denied replacing:

  __pycache__/toda_group_proof_narrative_contribution_renderer.cpython-310.pyc

This is a bytecode-cache filesystem problem, not evidence of a Python syntax
error in the modified production file.

This package
============
- does NOT re-apply R4-R4
- does NOT modify production code
- does NOT modify tests
- validates syntax with ast.parse, which does not write .pyc
- sets PYTHONDONTWRITEBYTECODE=1
- resumes steps 3 through 6
- runs focused/regression tests only
- does NOT run the full suite

The known stale Phase156 repair8 assertion
`definition_reason.conclusion_step.inference_rule is None`
is excluded from the regression gate.
