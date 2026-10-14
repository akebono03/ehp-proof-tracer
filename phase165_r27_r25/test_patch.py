import ast
from pathlib import Path

import pytest

from generator_facts import NU_PRIME_GENERATOR
from repository_generator_known_group_identity_lookup import (
    find_standard_repository_generator_known_group_identity_nodes,
)
from repository_proof_scope_facade import (
    explore_standard_repository_generator_proof_scope_input,
)

ROOT = Path(__file__).resolve().parent.parent


def test_r25_scope_standard_entry_fails_closed():
    with pytest.raises(RuntimeError, match='retired'):
        explore_standard_repository_generator_proof_scope_input('nu_prime')


def test_r25_scope_invalid_generator_keeps_validation():
    with pytest.raises(ValueError):
        explore_standard_repository_generator_proof_scope_input('not_a_generator')


def test_r25_identity_standard_entry_fails_closed():
    with pytest.raises(RuntimeError, match='retired'):
        find_standard_repository_generator_known_group_identity_nodes(NU_PRIME_GENERATOR)


def test_r25_identity_invalid_type_keeps_validation():
    with pytest.raises(TypeError):
        find_standard_repository_generator_known_group_identity_nodes('nu_prime')


def test_r25_no_builder_import_or_call():
    for name in ('repository_proof_scope_facade.py', 'repository_generator_known_group_identity_lookup.py'):
        tree=ast.parse((ROOT/name).read_text(encoding='utf-8'))
        assert not any(isinstance(n, ast.ImportFrom) and n.module == 'standard_production_repository' for n in ast.walk(tree))
        assert not any(isinstance(n, ast.Name) and n.id == 'build_standard_production_proof_repository' for n in ast.walk(tree))


def test_r25_explicit_repository_functions_preserved():
    scope=ast.parse((ROOT/'repository_proof_scope_facade.py').read_text(encoding='utf-8'))
    identity=ast.parse((ROOT/'repository_generator_known_group_identity_lookup.py').read_text(encoding='utf-8'))
    assert any(isinstance(n, ast.FunctionDef) and n.name == 'explore_repository_generator_proof_scope' for n in scope.body)
    assert any(isinstance(n, ast.FunctionDef) and n.name == 'find_repository_generator_known_group_identity_nodes' for n in identity.body)
