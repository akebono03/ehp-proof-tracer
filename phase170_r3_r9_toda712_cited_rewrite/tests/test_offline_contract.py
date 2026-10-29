"""Guarded patch and source-registration checks independent of production imports."""
from __future__ import annotations

import ast
from hashlib import sha1
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
ROUTER = HERE / 'replacement/phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py'
TRANSPORT = HERE / 'replacement/phase168_r2_toda52_transport.py'
SOURCE = HERE / 'source712.py'


def _functions(path: Path) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in ast.parse(path.read_text(encoding='utf-8')).body
            if isinstance(node, ast.FunctionDef)}


def test_reviewed_transport_is_a_complete_module():
    names = _functions(TRANSPORT)
    assert {'_toda52_group_presentation_matches',
            '_toda52_cited_generator_equality',
            '_toda52_ordered_db_rule',
            'expand_toda52_finite_cyclic_goal'} <= names.keys()
    assert not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                   and n.value.value is Ellipsis
                   for n in ast.walk(ast.parse(TRANSPORT.read_text(encoding='utf-8'))))


def test_router_existing_source_still_preserved():
    full = ROUTER.read_text(encoding='utf-8')
    assert 'register_source_checked_prop58_pi73' in full
    assert 'register_cited_toda712_generator_equality' in full
    assert len(_functions(ROUTER)) == 1


def test_reviewed_toda_reference_is_not_manufactured_from_csv():
    full = SOURCE.read_text(encoding='utf-8')
    assert 'CHAPTER_VII_BLOB' in full
    assert 'CLAUSE' in full and '(7.12)' in full
    assert 'ids=(10, 4)' in full and 'ids=(3, 11)' in full
    assert 'base.proof_links' in full
    assert 'ProofStep(' not in full


def test_runner_is_conservative_and_reversible():
    runner = (HERE / 'runner.py').read_text(encoding='utf-8')
    assert 'REVIEWED_BASE_HEAD' in runner
    assert 'git(root, "diff", "--cached", "--name-only")' in runner
    assert 'restored' in runner.lower()
    assert 'focused_pytest' in runner and 'active_web' in runner
    assert 'full_pytest": False' in runner
    assert 'if dry_run:' in runner


def test_source_file_and_runner_compiles():
    for name in ('runner.py', 'source712.py', 'verify.py'):
        compile((HERE / name).read_bytes(), name, 'exec')
