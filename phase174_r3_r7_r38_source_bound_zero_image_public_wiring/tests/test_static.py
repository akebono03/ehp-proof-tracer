"""R38 static contracts, runnable before the project dependency imports."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.install import (
    PACKAGE, reviewed_patch_bytes,
)


def test_full_context_replacement_preserves_existing_function() -> None:
    baseline, replacement = reviewed_patch_bytes()
    assert replacement != baseline
    old_tree = ast.parse(baseline.decode('utf-8'))
    new_tree = ast.parse(replacement.decode('utf-8'))
    old = next(x for x in old_tree.body if isinstance(x, ast.FunctionDef))
    new = next(x for x in new_tree.body if isinstance(x, ast.FunctionDef))
    assert old.name == new.name == 'build_context_expansion_provider_registry'
    assert len(old.args.kwonlyargs) == len(new.args.kwonlyargs)
    assert len(old.body) < len(new.body)


def test_no_proof_leaf_or_target_group_literal_installed() -> None:
    code = (PACKAGE / 'provider.py').read_text(encoding='utf-8')
    tree = ast.parse(code)
    identifiers = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert 'ProofStep' not in identifiers
    assert 'AssertionEntry' not in identifiers
    assert 'LiteratureEntry' not in identifiers
    assert 'ProofRule' not in identifiers
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == 'TodaPrimaryGroup'
        and any(isinstance(arg, ast.Constant) and isinstance(arg.value, int)
                for arg in node.args)
        for node in ast.walk(tree)
    )


def test_only_reviewed_context_function_is_replaced() -> None:
    before = (PACKAGE / 'baseline/context_provider_registry.py').read_text(encoding='utf-8')
    after = (PACKAGE / 'replacement/context_provider_registry.py').read_text(encoding='utf-8')
    anchor = '    for provider_id, function, statements in specifications:\n'
    assert before.count(anchor) == after.count(anchor) == 1
    assert after.endswith(before.split(anchor)[1])
    assert before.split(anchor)[0] in after
    assert 'PROVIDER_ID, expand_source_bound_zero_image_chain' in after


def test_complete_code_and_import_sections_present() -> None:
    full = (PACKAGE / 'CHANGED_FUNCTION_FULL.py').read_text(encoding='utf-8')
    imports = (PACKAGE / 'IMPORTS_FULL.txt').read_text(encoding='utf-8')
    assert full.startswith('def build_context_expansion_provider_registry(')
    assert full.strip().endswith('return registry')
    assert 'from __future__ import annotations' in imports
    assert 'UnifiedExpansionProviderRegistry' in imports
    ast.parse(imports + '\n' + full)
