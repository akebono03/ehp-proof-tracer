import ast
from pathlib import Path

from apply import FILES, transform

ROOT = Path(__file__).resolve().parent.parent


def test_r25_transform_idempotent():
    for name in FILES:
        first=transform((ROOT/name).read_text(encoding='utf-8'),name)
        assert transform(first,name)==first


def test_r25_transform_retains_explicit_repository_functions():
    for name, direct in (
        ('repository_proof_scope_facade.py','explore_repository_generator_proof_scope'),
        ('repository_generator_known_group_identity_lookup.py','find_repository_generator_known_group_identity_nodes'),
    ):
        source=(ROOT/name).read_text(encoding='utf-8')
        before=ast.parse(source)
        after=ast.parse(transform(source,name))
        old=next(x for x in before.body if isinstance(x,ast.FunctionDef) and x.name==direct)
        new=next(x for x in after.body if isinstance(x,ast.FunctionDef) and x.name==direct)
        assert ast.dump(old)==ast.dump(new)
