from pathlib import Path

def test_required_premises_argument_present():
    source = (Path(__file__).parent / "test_r4_r4_integration.py").read_text(encoding="utf-8")
    assert "premises=(), rule=ProofRule.GIVEN" in source
    assert "premise = ProofStep(" in source

def test_four_tests_preserved():
    import ast
    source = (Path(__file__).parent / "test_r4_r4_integration.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert len([node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]) == 4
