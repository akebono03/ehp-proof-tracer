"""Repair R6 registration installer after a nonmatching function-text anchor."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAIM = ROOT / "phase165_prop51_claim_order.py"
REGISTRATION = ROOT / "phase165_r52_r13_reference_registration.py"
IDENTIFIER = "toda:adopted:prop5.1:pi4_3"


def patch_claim(data: str) -> str:
    if 'OrderedProp51Item(4, "pi4_3_group_relation", "LITERATURE", pi4_3_goal())' in data:
        return data
    before = 'OrderedProp51Item(4, "pi4_3_group_goal", "GOAL", pi4_3_goal())'
    after = 'OrderedProp51Item(4, "pi4_3_group_relation", "LITERATURE", pi4_3_goal())'
    if data.count(before) != 1:
        raise ValueError("Unexpected ordered Proposition 5.1 fourth claim")
    return data.replace(before, after)


def patch_registration(data: str) -> str:
    if f'assertion_id="{IDENTIFIER}"' in data:
        return data
    tree = ast.parse(data)
    names = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "build_adopted_prop51_reference"]
    if len(names) != 1:
        raise ValueError("Unique build_adopted_prop51_reference function not found")
    fn = names[0]
    returns = [node for node in fn.body if isinstance(node, ast.Return)]
    if len(returns) != 1 or fn.body[-1] is not returns[0]:
        raise ValueError("Registration function does not end in a unique return")
    ret = returns[0]
    # Must be the existing registration call, not an unrelated return or branch.
    if not isinstance(ret.value, ast.Call) or not isinstance(ret.value.func, ast.Name) or ret.value.func.id != "register_adopted_composite_reference":
        raise ValueError("Registration function return is not the adopted composite registration")
    if not any(k.arg == "assertion_id" and isinstance(k.value, ast.Constant) and k.value.value == "toda:adopted:prop5.1:finite_dimensional" for k in ret.value.keywords):
        raise ValueError("Registration function has an unexpected assertion ID")
    # Existing import must expose all registry classes; do not blindly duplicate it.
    imported = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "unified_statement_registry":
            imported.update(a.name for a in node.names)
    required = {"AssertionEntry", "AssertionKind", "AssertionOrigin"}
    if not required.issubset(imported):
        raise ValueError("Required registry imports missing: " + repr(sorted(required - imported)))
    lines = data.splitlines(keepends=True)
    line = lines[ret.lineno - 1]
    indentation = line[:len(line) - len(line.lstrip())]
    # Preserve the complete original call exactly, including its local formatting.
    prefix = ''.join(lines[:ret.lineno-1])
    ret_source = ''.join(lines[ret.lineno-1:ret.end_lineno])
    expr = ret_source[ret_source.index('return') + len('return'):].strip()
    if not expr.startswith('register_adopted_composite_reference('):
        raise ValueError("Unexpected return source")
    replacement = (
        f"{indentation}bridge = {expr}\n"
        f"{indentation}# This literature assertion has no GIVEN proof link: no self-proof.\n"
        f"{indentation}from phase165_prop51_claim_order import pi4_3_goal\n"
        f"{indentation}bridge.registry.add_assertion(AssertionEntry(\n"
        f"{indentation}    assertion_id=\"{IDENTIFIER}\",\n"
        f"{indentation}    reference_id=\"adopted:toda:adopted:prop5.1:finite_dimensional\",\n"
        f"{indentation}    kind=AssertionKind.STATEMENT,\n"
        f"{indentation}    content=pi4_3_goal(),\n"
        f"{indentation}    origin=AssertionOrigin.FIXED_STATEMENT,\n"
        f"{indentation}    component_position=4,\n"
        f"{indentation}    scope=(\"user_adopted_claim_without_given_proof\",),\n"
        f"{indentation}))\n"
        f"{indentation}return bridge\n"
    )
    result = prefix + replacement + ''.join(lines[ret.end_lineno:])
    ast.parse(result)
    return result


def main() -> None:
    if not CLAIM.is_file() or not REGISTRATION.is_file():
        raise SystemExit("R5 prerequisite missing; no files modified")
    old_claim = CLAIM.read_text(encoding="utf-8-sig")
    old_reg = REGISTRATION.read_text(encoding="utf-8-sig")
    try:
        new_claim = patch_claim(old_claim)
        new_reg = patch_registration(old_reg)
        ast.parse(new_claim)
        ast.parse(new_reg)
    except (ValueError, SyntaxError) as exc:
        raise SystemExit("UNEXPECTED_LOCAL_CODE: " + str(exc) + "; no files modified") from exc
    modified = []
    for path, before, after in ((CLAIM, old_claim, new_claim), (REGISTRATION, old_reg, new_reg)):
        if before != after:
            backup = path.with_name(path.name + ".prop51_literature_r6_fix.bak")
            if not backup.exists():
                shutil.copy2(path, backup)
            path.write_text(after, encoding="utf-8")
            modified.append(path.name)
    print(json.dumps({"status":"INSTALLED" if modified else "ALREADY_INSTALLED", "modified": modified, "ordered_positions":5,"literature_at_position":4,"fourth_claim_given_link":False,"full_pytest_run":False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
