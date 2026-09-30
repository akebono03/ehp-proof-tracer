from functools import lru_cache
from audit_phase144_6_r5_20 import (
  ParityKind,
  ParityStatus,
  build_parity_audit,
  parity_requirements,
)


_uncached_build_parity_audit = build_parity_audit

@lru_cache(maxsize=1)
def build_parity_audit():
  return _uncached_build_parity_audit()


def test_phase144_6_r5_20_freezes_dedicated_parity_requirements():
  dedicated, generic, results = build_parity_audit()

  assert dedicated
  assert generic
  assert len(results) == len(parity_requirements())
  assert len(results) >= 20


def test_phase144_6_r5_20_covers_all_required_parity_kinds():
  requirements = parity_requirements()

  assert {
    requirement.kind
    for requirement in requirements
  } == {
    ParityKind.MATHEMATICAL_FACT,
    ParityKind.ORDERING,
    ParityKind.DISCOURSE,
    ParityKind.STRUCTURE,
  }


def test_phase144_6_r5_20_final_group_is_present_in_generic():
  dedicated, generic, results = build_parity_audit()
  result = next(
    result
    for result in results
    if result.requirement.key == "final_group"
  )

  assert result.status is ParityStatus.PRESENT


def test_phase144_6_r5_20_definition_is_present_in_generic():
  dedicated, generic, results = build_parity_audit()
  result = next(
    result
    for result in results
    if result.requirement.key == "nu_prime_bracket_definition"
  )

  assert result.status is ParityStatus.PRESENT


def test_phase144_6_r5_20_short_exact_sequence_is_present_in_generic():
  dedicated, generic, results = build_parity_audit()
  result = next(
    result
    for result in results
    if result.requirement.key == "short_exact_sequence"
  )

  assert result.status is ParityStatus.PRESENT


def test_phase144_6_r5_20_reports_missing_items_instead_of_forcing_parity():
  dedicated, generic, results = build_parity_audit()

  assert all(
    result.status in (
      ParityStatus.PRESENT,
      ParityStatus.MISSING,
    )
    for result in results
  )
