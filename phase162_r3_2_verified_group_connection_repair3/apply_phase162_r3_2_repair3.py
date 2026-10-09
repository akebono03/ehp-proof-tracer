"""R3-2 repair3: patch only the verified proof generator and its import."""
from pathlib import Path
import ast
import shutil

bundle = Path(__file__).resolve().parent
repo = bundle.parent
integration = repo / "phase162_web_narrative_integration.py"
web = repo / "web_group_proof.py"
if not integration.is_file() or not web.is_file():
    raise SystemExit("Missing existing Web integration files")
current = integration.read_text(encoding="utf-8-sig")
web_text = web.read_text(encoding="utf-8-sig")
if "## 群構造の検証済み証明" not in web_text:
    raise SystemExit("The R3-2 lower-panel heading update has not been applied")
if "build_phase162_web_validated_isomorphism_markdown" not in web_text:
    raise SystemExit("Existing lower-panel hook not found")

old_import = chr(10).join((
    "from toda_rules import (",
    "    toda_52_pi4_2_finite_cyclic_transport_inference_rule,",
    "    toda_eta_family_definition_statement,",
    ")",
))
new_import = chr(10).join((
    "from toda_rules import (",
    "    toda_52_pi4_2_finite_cyclic_transport_inference_rule,",
    "    toda_eta_family_definition_statement,",
    "    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,",
    ")",
))
if current.count(old_import) == 1:
    next_text = current.replace(old_import, new_import, 1)
elif current.count(new_import) == 1:
    next_text = current
else:
    raise SystemExit("Unexpected Toda imports; refusing patch")

def function_range(source: str, name: str) -> tuple[int, int]:
    module = ast.parse(source)
    matches = [node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(matches) != 1:
        raise ValueError("Expected exactly one named function")
    lines = source.splitlines(keepends=True)
    node = matches[0]
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))

name = "_build_phase162_existing_group_connection"
replacement_source = (bundle / "phase162_web_narrative_integration.py").read_text(encoding="utf-8")
a, b = function_range(next_text, name)
c, d = function_range(replacement_source, name)
replacement = replacement_source[c:d]
next_text = next_text[:a] + replacement + next_text[b:]
ast.parse(next_text)
if next_text == current:
    print("R3-2 repair3 already applied")
else:
    backups = bundle / "backup_before_apply"
    backups.mkdir(exist_ok=True)
    shutil.copy2(integration, backups / integration.name)
    integration.write_text(next_text, encoding="utf-8")
    print("Updated only the R3-2 goal assembly and its import")
print("Upper Group proof unchanged. Full suite not run.")
