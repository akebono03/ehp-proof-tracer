# Phase157-R5-R6 repair1 changed code

## Changed files

- `toda_upstream_bootstrap.py`
- `toda_literature_statement_boundary.py`
- `tests/test_phase157_r2_literature_statement_boundary.py`
- `tests/test_phase157_r5_r6_53_bracket_definition_reference.py`

## `toda_upstream_bootstrap.py`

### Import change

The complete changed `from proof import (...)` block is emitted after apply to:

`phase157_r5_r6_repair1_output/toda_upstream_bootstrap_import_after.txt`

### Function change

The complete changed:

`build_toda_53_nu_prime_steps()`

is emitted after apply to:

`phase157_r5_r6_repair1_output/build_toda_53_nu_prime_steps_after.txt`

The mathematical construction is unchanged except that
`bracket_membership_step` is now an inference-backed literature source step
with explicit Toda `(5.3)` provenance.

## `toda_literature_statement_boundary.py`

Catalog-only changes:
- keep `nu_prime_bracket_definition`;
- remove the fixed mapping for
  `Toda 5.3 nu-prime Lemma 5.2 bracket specialization`;
- add the fixed mapping for
  `Toda (5.3) nu-prime bracket definition`.

No function body changes.

## `tests/test_phase157_r2_literature_statement_boundary.py`

Changed complete test function:

```python
def test_phase157_r2_equation53_inventory_has_no_group_order_policy():
  components = get_toda_fixed_statement_components(
    "(5.3)"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_bracket_definition",
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )

  assert all(
    component.order is None
    for component in components
  )
```

The existing
`test_phase157_r2_equation53_bracket_specialization_is_proof_internal()`
is intentionally not changed.

## New/rewritten R5-R6 test

The apply script writes the complete
`tests/test_phase157_r5_r6_53_bracket_definition_reference.py`.
