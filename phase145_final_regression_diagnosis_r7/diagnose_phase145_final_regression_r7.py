from __future__ import annotations

import ast
from collections import Counter, defaultdict
from pathlib import Path


TESTS = Path("tests")


def parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))


def main() -> int:
    if not TESTS.is_dir():
        raise RuntimeError("tests directory not found")

    test_files = sorted(TESTS.glob("test_*.py"))
    package_imports: list[tuple[Path, int, str]] = []
    bare_imports: list[tuple[Path, int, str]] = []
    relative_imports: list[tuple[Path, int, str]] = []
    bare_by_module: dict[str, list[tuple[Path, int]]] = defaultdict(list)

    for path in test_files:
        tree = parse(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if node.level:
                    relative_imports.append((path, node.lineno, "." * node.level + module))
                elif module.startswith("tests.test_"):
                    package_imports.append((path, node.lineno, module))
                elif module.startswith("test_"):
                    bare_imports.append((path, node.lineno, module))
                    bare_by_module[module].append((path, node.lineno))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name
                    if module.startswith("tests.test_"):
                        package_imports.append((path, node.lineno, module))
                    elif module.startswith("test_"):
                        bare_imports.append((path, node.lineno, module))
                        bare_by_module[module].append((path, node.lineno))

    print("=" * 78)
    print("Phase 145 Final Regression Diagnosis R7")
    print("Canonical test import-style audit")
    print("=" * 78)
    print(f"canonical test files: {len(test_files)}")
    print(f"tests.test_* package imports: {len(package_imports)}")
    print(f"bare test_* imports: {len(bare_imports)}")
    print(f"relative imports: {len(relative_imports)}")
    print(f"unique bare test_* modules: {len(bare_by_module)}")
    print()

    print("A. Bare test-module dependency inventory")
    print("-" * 78)
    missing = []
    existing = []
    for module in sorted(bare_by_module):
        target = TESTS / f"{module}.py"
        refs = bare_by_module[module]
        state = "EXISTS" if target.is_file() else "MISSING"
        print(f"{module}: {state}; references={len(refs)}; target={target.as_posix()}")
        for path, lineno in refs:
            print(f"  {path.as_posix()}:{lineno}")
        if target.is_file():
            existing.append(module)
        else:
            missing.append(module)

    print()
    print("B. Summary")
    print("-" * 78)
    print(f"bare modules with canonical target: {len(existing)}")
    print(f"bare modules without canonical target: {len(missing)}")
    if missing:
        print("missing bare targets:")
        for module in missing:
            print(f"  {module}")

    print()
    print("C. Package marker")
    print("-" * 78)
    marker = TESTS / "__init__.py"
    print(f"tests/__init__.py exists: {marker.exists()}")
    if marker.exists():
        print(f"tests/__init__.py size: {marker.stat().st_size} bytes")

    print()
    print("D. Interpretation gate")
    print("-" * 78)
    if bare_imports:
        print(
            "Mixed import styles confirmed: canonical tests contain both "
            "'tests.test_*' package imports and bare 'test_*' imports."
        )
    else:
        print("No bare test-module imports found.")

    print()
    print("=" * 78)
    print("Phase 145 Final Regression Diagnosis R7: COMPLETE")
    print("Repository changes: none")
    print("Repository-wide pytest: NOT RUN")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
