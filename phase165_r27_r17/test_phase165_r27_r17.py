import ast
from pathlib import Path
import pytest

from repository_element_facade import explore_standard_repository_generator_input
from generator_facts import NU_PRIME_GENERATOR


def test_r27_r17_generator_alias_preserved():
    for alias in ('nu_prime', "nu'", 'ν′'):
        result = explore_standard_repository_generator_input(alias)
        assert result.exploration.generator == NU_PRIME_GENERATOR


def test_r27_r17_no_legacy_proof_promoted():
    result = explore_standard_repository_generator_input('nu_prime')
    assert result.exploration.occurrences == ()
    assert result.presentation.occurrences == ()
    assert 'Occurrences: 0' in result.markdown


def test_r27_r17_unknown_generator_is_empty():
    result = explore_standard_repository_generator_input('eta_999')
    assert result.exploration.occurrences == ()


def test_r27_r17_invalid_input_validation():
    for value in ('', 'eta_0', 'not_a_generator'):
        with pytest.raises(ValueError):
            explore_standard_repository_generator_input(value)


def test_r27_r17_source_has_no_legacy_generator_builder():
    source = Path('repository_element_facade.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    assert 'build_standard_production_proof_repository' not in source
    assert any(isinstance(node, ast.FunctionDef) and node.name == 'explore_standard_repository_generator_input' for node in tree.body)
