from __future__ import annotations

import ast
import importlib.util
import inspect
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
PHASE148_FILES = (
    ROOT / "tests" / "test_phase148_rc2_4_repair_r5.py",
    ROOT / "tests" / "test_phase148_rc2_4_repair_r5_r2.py",
)
RC45_FILE = ROOT / "tests" / "test_phase150_rc4_5_visible_reasons.py"


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _function_source(module, name: str) -> str:
    value = getattr(module, name, None)
    if value is None:
        return "<missing>"
    return inspect.getsource(value)


def _extract_param_cases(module):
    for name in ("CASES", "TARGETS", "_CASES", "_TARGETS"):
        value = getattr(module, name, None)
        if isinstance(value, tuple):
            return name, value
    return None, ()


def _candidate_reason_collections(module):
    result = {}
    for name, value in vars(module).items():
        if not isinstance(value, (tuple, list)) or not value:
            continue
        if all(isinstance(item, str) for item in value):
            result[name] = tuple(value)
    return result


def _print_counter(label: str, values):
    counter = Counter(values)
    print(label)
    print(f"  total={len(values)} unique={len(counter)}")
    for text, count in counter.items():
        if count > 1:
            print(f"  DUPLICATE x{count}: {text!r}")


def audit_phase148():
    print("=" * 78)
    print("A. Phase 148 exactness contract audit")
    print("=" * 78)
    for path in PHASE148_FILES:
        print()
        print(f"FILE: {path}")
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        module = _load_module(path)
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if "exactness" not in node.name:
                continue
            print("-" * 78)
            print(node.name)
            print(_function_source(module, node.name).rstrip())

    print()
    print("INTERPRETATION CHECK:")
    print(
        "If semantic-presence tests pass while only literal one-visible-phrase tests fail, "
        "exactness evidence remains in the semantic closure and the failure is a rendered-"
        "text contract mismatch rather than evidence loss."
    )


def audit_rc45():
    print()
    print("=" * 78)
    print("B. Phase 150 RC4-5 visible-reason counting audit")
    print("=" * 78)
    if not RC45_FILE.exists():
        raise FileNotFoundError(RC45_FILE)

    module = _load_module(RC45_FILE)
    test_name = "test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count"

    print()
    print(f"FILE: {RC45_FILE}")
    print("-" * 78)
    print("FAILING TEST SOURCE")
    print(_function_source(module, test_name).rstrip())

    case_name, cases = _extract_param_cases(module)
    print()
    print(f"Detected case collection: {case_name!r}")
    print(f"Detected cases: {cases!r}")

    print()
    print("MODULE-LEVEL STRING COLLECTIONS")
    collections = _candidate_reason_collections(module)
    if not collections:
        print("  none")
    for name, values in collections.items():
        _print_counter(f"  {name}", values)

    fn = getattr(module, test_name)
    source = inspect.getsource(fn)
    suspicious = ".count(" in source and "sum(" in source
    print()
    print("STATIC COUNTING CHECK")
    print(f"  contains sum(...count(...)): {suspicious}")
    if suspicious:
        print(
            "  Duplicate reason strings can make the same rendered occurrence count more "
            "than once. This is a test-counting hazard."
        )

    print()
    print("REFERENCED MODULE OBJECTS")
    for name in sorted(set(fn.__code__.co_names)):
        if name in vars(module):
            print(f"  {name}: {type(vars(module)[name]).__name__}")

    print()
    print("No production code, existing test, or documentation is modified.")


def main():
    print("Phase 150 Final Regression 9-Failure Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print("Documentation changes: none")
    print("Full regression: NOT run")
    print()
    audit_phase148()
    audit_rc45()


if __name__ == "__main__":
    main()
