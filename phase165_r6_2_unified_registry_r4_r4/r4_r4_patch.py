"""Apply the minimal general reverse pattern while preserving the forward builder."""
from __future__ import annotations

import ast
from pathlib import Path

EXPECTED_IMPORT = 'from dataclasses import dataclass\n\nfrom expression import (\n  MapApplication,\n  MapSymbol,\n)\nfrom proof import (\n  InferenceRule,\n  PatternVariable,\n  PremisePattern,\n  Relation,\n  RelationType,\n)\n'
NEW_FUNCTION = 'def isomorphism_implies_injective_inference_rule():\n  map_variable = PatternVariable(name="map")\n\n  def build_conclusion(\n    premises,\n  ):\n    isomorphism_statement = (\n      premises[0].conclusion\n    )\n\n    return InjectiveMapStatement(\n      map=isomorphism_statement.map,\n    )\n\n  return InferenceRule(\n    name="isomorphism implies injectivity",\n    description=(\n      "An isomorphism is injective."\n    ),\n    premise_patterns=(\n      PremisePattern(\n        statement_type=(\n          IsomorphismStatement\n        ),\n        statement_pattern=IsomorphismStatement(\n          map=map_variable,\n        ),\n      ),\n    ),\n    conclusion_pattern=InjectiveMapStatement(\n      map=map_variable,\n    ),\n    conclusion_builder=(\n      build_conclusion\n    ),\n  )\n'
TARGET = "isomorphism_implies_injective_inference_rule"


def replace_function(source: str) -> str:
    if "from phase165_r52_r23_existing_rule_adapter import" in source:
        raise ValueError("unexpected legacy adapter reference")
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == TARGET]
    if len(candidates) != 1:
        raise ValueError("expected exactly one isomorphism rule function")
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    existing = "".join(lines[node.lineno - 1:node.end_lineno]).replace("\r\n", "\n")
    if "conclusion_pattern=InjectiveMapStatement(" in existing:
        if "statement_pattern=IsomorphismStatement(" in existing:
            return source
        raise ValueError("partial or unexpected installation")
    if "def build_conclusion(" not in existing or "conclusion_builder=" not in existing:
        raise ValueError("existing forward builder differs; refusing edit")
    replaced = "".join(lines[:node.lineno - 1]) + NEW_FUNCTION + "".join(lines[node.end_lineno:])
    if "  PatternVariable," not in replaced:
        old = "  InferenceRule,"
        if replaced.count(old) != 1:
            raise ValueError("cannot locate proof import")
        replaced = replaced.replace(old, old + "\n  PatternVariable,", 1)
    ast.parse(replaced)
    return replaced


def install(directory: Path) -> str:
    target = directory / "map_property_rules.py"
    if not target.is_file():
        raise FileNotFoundError(target)
    raw = target.read_bytes()
    source = raw.decode("utf-8")
    patched = replace_function(source)
    if patched == source:
        return "ALREADY_INSTALLED"
    backup = target.with_name(target.name + ".r4_r4_before.bak")
    if backup.exists():
        raise FileExistsError("backup exists but patch is not installed; manual review required")
    backup.write_bytes(raw)
    try:
        target.write_bytes(patched.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in raw else patched.encode("utf-8"))
    except Exception:
        target.write_bytes(raw)
        raise
    return "INSTALLED"


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(install(args.root.resolve()))


if __name__ == "__main__":
    main()
