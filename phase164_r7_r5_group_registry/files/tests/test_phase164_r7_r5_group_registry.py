"""R7-R5: Group facade shares internal proof-root resolution."""
from unittest.mock import patch

import pytest

from phase164_r7_repository_root_resolution import validate_repository_internal_proof_roots
from proof import ProofRule, ProofStep
from proof_repository import ProofRepository, ProofRepositoryEntry
from toda_calculation_facade import build_standard_toda_report
from toda_calculation_report_result import TodaCalculationReportResult


def _repository():
    repository = ProofRepository()
    step = ProofStep(conclusion="group fixture", premises=(), rule=ProofRule.GIVEN)
    repository.register(ProofRepositoryEntry(key="fixture.group", step=step))
    return repository


def test_r7_r5_group_facade_validates_before_reporting():
    repository = _repository()
    sentinel = object()
    with (
        patch("toda_calculation_facade.build_standard_production_proof_repository", return_value=repository),
        patch("toda_calculation_facade.validate_repository_internal_proof_roots", wraps=validate_repository_internal_proof_roots) as guard,
        patch("toda_calculation_facade.build_toda_report", return_value=sentinel) as report,
    ):
        actual = build_standard_toda_report(3, 2)
    assert actual is sentinel
    guard.assert_called_once_with(repository)
    report.assert_called_once_with(repository, n=3, k=2)


def test_r7_r5_group_guard_failure_prevents_calculation():
    repository = _repository()
    with (
        patch("toda_calculation_facade.build_standard_production_proof_repository", return_value=repository),
        patch("toda_calculation_facade.validate_repository_internal_proof_roots", side_effect=ValueError("registry mismatch")),
        patch("toda_calculation_facade.build_toda_report") as report,
    ):
        with pytest.raises(ValueError, match="registry mismatch"):
            build_standard_toda_report(3, 2)
    report.assert_not_called()


def test_r7_r5_common_guard_keeps_existing_root_identity():
    repository = _repository()
    original = repository.entries()[0]
    assert validate_repository_internal_proof_roots(repository) is repository
    assert repository.entries()[0] is original
    assert repository.entries()[0].step is original.step


def test_r7_r5_guard_rejects_non_repository():
    with pytest.raises(TypeError, match="repository must be a ProofRepository"):
        validate_repository_internal_proof_roots(None)
