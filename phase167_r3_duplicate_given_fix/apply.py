from __future__ import annotations
import ast
import json
import shutil
from pathlib import Path

folder = Path(__file__).resolve().parent
repo = folder.parent
target = repo / "phase165_r52_r16_web_citation_gate.py"
source = target.read_text(encoding="utf-8")
tree = ast.parse(source)
functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "screen_shared_proof_context"]
if len(functions) != 1:
    raise RuntimeError("Cannot locate unique citation screening function")
node = functions[0]
lines = source.splitlines(keepends=True)
start = sum(map(len, lines[:node.lineno - 1]))
end = sum(map(len, lines[:node.end_lineno]))
function = source[start:end]
old = '''        return RegistryBridgeResult(bridge.registry, bridge.records, tuple(accepted))'''
new = '''        # Equivalent copies from the same printed position are one GIVEN,
        # not competing independent mathematical derivations. Preserve a
        # previously linked source when possible, including its provenance.
        unique = []
        for candidate in accepted:
            assertion = bridge.registry.assertion(candidate.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            identical_index = None
            for index, existing in enumerate(unique):
                other = bridge.registry.assertion(existing.assertion_id)
                other_reference = bridge.registry.reference(other.reference_id)
                if (
                    candidate.step.conclusion == existing.step.conclusion
                    and reference.publication_position == other_reference.publication_position
                    and assertion.component_position == other.component_position
                ):
                    identical_index = index
                    break
            original_links = tuple(
                link for link in bridge.proof_links
                if link.assertion_id == candidate.assertion_id
                and link.step is not None
                and link.step.rule is ProofRule.GIVEN
                and link.step.conclusion == candidate.step.conclusion
            )
            if len(original_links) == 1:
                candidate = original_links[0]
            if identical_index is None:
                unique.append(candidate)
            else:
                existing = unique[identical_index]
                existing_linked = any(
                    link.assertion_id == existing.assertion_id
                    and link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and link.step.conclusion == existing.step.conclusion
                    for link in bridge.proof_links
                )
                if len(original_links) == 1 and not existing_linked:
                    unique[identical_index] = candidate
        return RegistryBridgeResult(bridge.registry, bridge.records, tuple(unique))'''
if function.count(old) != 1 or 'explicit_publication_target' not in function:
    raise RuntimeError("Unexpected citation screen layout; refusing patch")
updated_function = function.replace(old,new,1)
updated_source = source[:start] + updated_function + source[end:]
ast.parse(updated_source)
backup = folder / 'backup' / target.name
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(target,backup)
target.write_text(updated_source,encoding='utf-8')
(folder / 'modified_function_full.py').write_text(updated_function,encoding='utf-8')
print(json.dumps({'status':'PATCHED','target':str(target),'backup':str(backup),'full_function':str(folder/'modified_function_full.py')},ensure_ascii=False,indent=2))
