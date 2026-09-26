from pathlib import Path
import ast

FILES = [
    Path("toda_group_proof_narrative_argument_body_renderer.py"),
    Path("toda_group_proof_narrative_argument_multi_renderer.py"),
    Path("toda_group_proof_narrative_renderer.py"),
]

KEYWORDS = (
    "duplicate", "redundant", "relocat", "supporting_blocks",
    "local_body_blocks", "preserve_provenance", "direct_derivation",
    "aggregate",
)

def read_text(path):
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")

def segment(text, node):
    lines = text.splitlines()
    return "\n".join(lines[node.lineno - 1:node.end_lineno])

for path in FILES:
    print("=" * 78)
    print(path)
    print("=" * 78)
    if not path.exists():
        print("MISSING")
        continue
    text = read_text(path)
    tree = ast.parse(text)
    print("Imports")
    print("-" * 78)
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            print(segment(text, node))
    print("\nRelevant functions")
    print("-" * 78)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            source = segment(text, node)
            if any(k in node.name + "\n" + source for k in KEYWORDS):
                print(f"\n### {node.name} (lines {node.lineno}-{node.end_lineno})")
                print(source)

print("\n" + "=" * 78)
print("RELATED TEST INVENTORY")
print("=" * 78)

for path in [
    Path("tests/test_phase143_51a_r_provenance_semantic_catalog.py"),
    Path("tests/test_phase143_51b_aggregate_statement_prose.py"),
    Path("tests/test_phase143_59b_group_structure_duplicate_suppression.py"),
    Path("tests/test_phase143_61b_direct_premise_narrative.py"),
    Path("tests/test_phase143_61b_r_semantic_suppression_priority.py"),
    Path("tests/test_phase134_24_pi15_8_narrative.py"),
]:
    print("\n" + "-" * 78)
    print(path)
    print("-" * 78)
    if not path.exists():
        print("MISSING")
        continue
    text = read_text(path)
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            print(f"\n### {node.name} (lines {node.lineno}-{node.end_lineno})")
            print(segment(text, node))
