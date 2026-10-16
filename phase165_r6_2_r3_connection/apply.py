"""Install bounded verified-witness candidate generation in shared search."""
from __future__ import annotations
import ast
import shutil
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
R2 = ROOT / "phase165_r6_2_r2_verified_inverse.py"

MARKER = "    # R6-2 R3: use only cited GIVEN witnesses for verified inverse proposals."
INJECT = '    # R6-2 R3: use only cited GIVEN witnesses for verified inverse proposals.\n    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses\n    from phase165_r8_rule_provider import discover_inference_rules\n    witness_rules, _witness_report = discover_inference_rules()\n    cited_witnesses = tuple(\n        link.step for link in bridge.proof_links\n        if link.step is not None\n        and link.step.rule is ProofRule.GIVEN\n        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT\n        and link.step.conclusion == bridge.registry.assertion(link.assertion_id).content\n    )\n'
MERGE_OLD = "        merged = merge_backward_expansions(tuple(options), generic_provider(goal))"
MERGE_NEW = '        # R2 returns candidate Goals only; the recursive search still verifies ProofSteps.\n        # Exhaustion is not equivalent to proof; preserve the older search proposals.\n        try:\n            witness_options = reverse_rules_from_witnesses(\n                goal, witness_rules, cited_witnesses, max_combinations=2048,\n            )\n        except ValueError as exc:\n            if str(exc) != "generic witness inverse search budget exceeded":\n                raise\n            witness_options = ()\n        merged = merge_backward_expansions(\n            merge_backward_expansions(tuple(options), generic_provider(goal)),\n            witness_options,\n        )'

def main():
    if not TARGET.exists() or not R2.exists():
        raise FileNotFoundError("Shared math or R2 implementation missing")
    old = TARGET.read_text(encoding="utf-8-sig")
    tree = ast.parse(old)
    funcs = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == "shared_expansion_provider"]
    if len(funcs) != 1:
        raise RuntimeError("Unexpected shared expansion provider")
    body = ast.get_source_segment(old, funcs[0])
    if MARKER in body:
        print(json.dumps({"status":"ALREADY_INSTALLED","full_pytest_run":False}))
        return
    if "expand_existing_pi43_rules" not in body:
        raise RuntimeError("Existing shared provider changed; refuse blind replacement")
    if old.count(MERGE_OLD) != 1:
        raise RuntimeError("Expected exactly one merge point")
    anchor = "    generic_provider = build_generic_backward_expansion_provider()"
    if old.count(anchor) != 1:
        raise RuntimeError("Expected exactly one generic provider setup")
    rewritten=old.replace(anchor,anchor+"\n\n"+INJECT.rstrip("\n"))
    rewritten=rewritten.replace(MERGE_OLD,MERGE_NEW)
    ast.parse(rewritten)
    backup=TARGET.with_name(TARGET.name+".r6_2_r3_before.bak")
    if not backup.exists():
        shutil.copy2(TARGET,backup)
    TARGET.write_text(rewritten,encoding="utf-8")
    print(json.dumps({"status":"CONNECTED","modified_file":TARGET.name,
                      "fixed_cited_witnesses_only":True,
                      "pi43_adapter_retained":True,"full_pytest_run":False},indent=2))

if __name__ == "__main__":
    main()
