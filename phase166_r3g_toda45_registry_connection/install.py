"""Phase 166 R3-G minimal checked installation against current production sources."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
LIT = ROOT / 'phase165_r52_r27_r5_literature.py'
SPEC = ROOT / 'phase165_r57_r20_general_specialization.py'
TEST = ROOT / 'phase165_r52_r27_r5_typed_references' / 'test_r5_typed_references.py'
PKG = Path(__file__).resolve().parent


def insert_once(source: str, needle: str, replacement: str, path: Path) -> str:
    if source.count(needle) != 1:
        raise RuntimeError(f'Unexpected production version or already modified: {path} / {needle[:60]}')
    return source.replace(needle, replacement, 1)


def install() -> None:
    if not all(p.is_file() for p in (LIT, SPEC, TEST)):
        raise RuntimeError('Run this package from the repository root; expected source/test files absent.')
    originals = {p: p.read_text(encoding='utf-8') for p in (LIT, SPEC, TEST)}
    altered = dict(originals)
    lit = altered[LIT]
    lit = insert_once(lit, 'from hashlib import sha256\n', 'from hashlib import sha256\n\nfrom expression import ScalarProduct, ScalarSum, ScalarSymbol\nfrom homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup\nfrom toda_rules import Toda45IsomorphismStatement\n', LIT)
    insertion = '''\n\ndef _toda45_universal_statement() -> Toda45IsomorphismStatement:\n    """The whole (4.5) map schema; numerical domain is validated on use."""\n    n, k, m = ScalarSymbol("n"), ScalarSymbol("k"), ScalarSymbol("m")\n    return Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(\n        exponent=ScalarSum(left=m, right=ScalarProduct(left=-1, right=n)),\n        source_group=TodaPrimaryGroup(\n            group_dimension=ScalarSum(left=n, right=k), sphere_dimension=n,\n        ),\n        target_group=TodaPrimaryGroup(\n            group_dimension=ScalarSum(left=m, right=k), sphere_dimension=m,\n        ),\n    ))\n\n\ndef _register_toda45(registry, links, records, source_bridge) -> None:\n    source_id = "toda:tex:ch4:0006"\n    candidates = [\n        a for a in source_bridge.registry._assertions.values()\n        if a.origin is AssertionOrigin.SOURCE_ARCHIVE\n        and isinstance(a.content, dict)\n        and a.content.get("source_statement_id") == source_id\n    ]\n    if len(candidates) != 1:\n        raise ValueError("unique source archive entry required: (4.5)")\n    archive = candidates[0].content\n    source_text = archive.get("source_text")\n    if (not isinstance(source_text, str)\n            or archive.get("source_sha256") != sha256(source_text.encode("utf-8")).hexdigest()\n            or "E" not in source_text):\n        raise ValueError("source content does not match reviewed scope: (4.5)")\n    ref_id = f"typed_literature:{source_id}"\n    assertion_id = f"typed_literature:assertion:{source_id}"\n    statement = _toda45_universal_statement()\n    registry.add_reference(LiteratureEntry(\n        ref_id, ReferenceKind.EQUATION, "(4.5)", source_id=source_id,\n    ))\n    registry.add_assertion(AssertionEntry(\n        assertion_id, ref_id, AssertionKind.STATEMENT, statement,\n        origin=AssertionOrigin.FIXED_STATEMENT,\n        scope=("n>=k+2", "m>=n", "k>=0"),\n    ))\n    links.append(ProofStepLink(\n        assertion_id, step=ProofStep(\n            conclusion=statement, premises=(), rule=ProofRule.GIVEN,\n        ),\n    ))\n    records.append(MigrationRecord(\n        "phase166_r3g", "(4.5)", assertion_id,\n        MigrationStatus.STRUCTURED,\n        "typed universal suspension map with explicit numerical domain",\n    ))\n'''
    lit = insert_once(lit, '\n_SOURCES = (', insertion + '\n_SOURCES = (', LIT)
    lit = insert_once(lit, '    return RegistryBridgeResult(registry, tuple(records), tuple(links))', '    _register_toda45(registry, links, records, source_bridge)\n    return RegistryBridgeResult(registry, tuple(records), tuple(links))', LIT)
    ast.parse(lit)
    altered[LIT] = lit

    spec = altered[SPEC]
    needle = 'def specialize_typed_statement(source: object, goal: object) -> tuple[tuple[str, int], ...] | None:'
    # Replace only existing generic matching function; no new math inference rule.
    pos = spec.index(needle)
    after = spec.index('\n\ndef _specialization_rule(', pos)
    new_func = '''def specialize_typed_statement(source: object, goal: object) -> tuple[tuple[str, int], ...] | None:\n    """Bind general numeric schemas, checking (4.5) stable-range conditions."""\n    if not _contains_symbol(source):\n        return None\n    bindings: dict[str, int] = {}\n    from toda_rules import Toda45IsomorphismStatement\n    matching = (_bind_symbolic_constraints(source, goal, bindings)\n                if isinstance(source, Toda45IsomorphismStatement)\n                else _bind(source, goal, bindings))\n    if not matching:\n        return None\n    try:\n        instantiated = _instantiate(source, bindings)\n    except (ValueError, TypeError):\n        return None\n    if instantiated != goal:\n        return None\n    from phase165_prop51_range_guard import allows_typed_specialization\n    if not allows_typed_specialization(source, bindings):\n        return None\n    from toda_rules import Toda45IsomorphismStatement\n    if isinstance(source, Toda45IsomorphismStatement):\n        n, k, m = (bindings.get(name) for name in ("n", "k", "m"))\n        if (any(type(x) is not int for x in (n, k, m))\n                or k < 0 or n < k + 2 or m < n):\n            return None\n    return tuple(sorted(bindings.items()))\n'''
    spec = spec[:pos] + new_func + spec[after:]
    pre = '''def _bind_symbolic_constraints(pattern: object, concrete: object, bindings: dict[str, int]) -> bool:\n    """Solve typed scalar equalities in dependency order, not field order."""\n    constraints = []\n\n    def flatten(p, c):\n        if type(p) is not type(c) and not isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)):\n            return False\n        if isinstance(p, tuple):\n            if len(p) != len(c):\n                return False\n            return all(flatten(x, y) for x, y in zip(p, c))\n        if is_dataclass(p) and not isinstance(p, type) and not isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)):\n            return all(flatten(getattr(p, field.name), getattr(c, field.name)) for field in fields(p))\n        constraints.append((p, c))\n        return True\n\n    if not flatten(pattern, concrete):\n        return False\n    pending = list(constraints)\n    for _ in range(len(pending) + 1):\n        if not pending:\n            return True\n        next_pending = []\n        advanced = False\n        for p, c in pending:\n            if isinstance(p, (ScalarSymbol, ScalarSum, ScalarProduct)) and type(c) is int:\n                expr = _linear_scalar_expression(p)\n                if expr is None:\n                    return False\n                coefficients, constant = expr\n                remaining = {v: a for v, a in coefficients.items() if v not in bindings and a}\n                known = constant + sum(a * bindings[v] for v, a in coefficients.items() if v in bindings)\n                if not remaining:\n                    if known != c:\n                        return False\n                    advanced = True\n                elif len(remaining) == 1:\n                    name, a = next(iter(remaining.items()))\n                    if (c - known) % a:\n                        return False\n                    bindings[name] = (c - known) // a\n                    advanced = True\n                else:\n                    next_pending.append((p, c))\n            elif _bind(p, c, bindings):\n                advanced = True\n            else:\n                return False\n        if not advanced:\n            return False\n        pending = next_pending\n    return not pending\n\n\ndef _linear_scalar_expression(value: object):\n    """Represent an affine scalar expression as (coefficients, constant)."""\n    if type(value) is int:\n        return ({}, value)\n    if isinstance(value, ScalarSymbol):\n        return ({value.name: 1}, 0)\n    if isinstance(value, ScalarSum):\n        left, right = _linear_scalar_expression(value.left), _linear_scalar_expression(value.right)\n        if left is None or right is None:\n            return None\n        coeff = dict(left[0])\n        for name, amount in right[0].items():\n            coeff[name] = coeff.get(name, 0) + amount\n        return (coeff, left[1] + right[1])\n    if isinstance(value, ScalarProduct):\n        if type(value.left) is int:\n            factor, inner = value.left, _linear_scalar_expression(value.right)\n        elif type(value.right) is int:\n            factor, inner = value.right, _linear_scalar_expression(value.left)\n        else:\n            return None\n        if inner is None:\n            return None\n        return ({name: factor * amount for name, amount in inner[0].items()}, factor * inner[1])\n    return None\n\n\n'''
    spec = insert_once(spec, needle, pre + needle, SPEC)
    ast.parse(spec)
    altered[SPEC] = spec

    tst = altered[TEST]
    tst = tst.replace('assert len(bridge.proof_links) == 2', 'assert len(bridge.proof_links) == 3')
    tst = tst.replace('assert len(old.proof_links) == 2', 'assert len(old.proof_links) == 3')
    tst = tst.replace('        TodaProp44UniversalStatement, Toda52UniversalStatement,', '        TodaProp44UniversalStatement, Toda52UniversalStatement,\n        Toda45IsomorphismStatement,')
    tst = tst.replace('from proof import ProofRule', 'from proof import ProofRule\nfrom toda_rules import Toda45IsomorphismStatement')
    ast.parse(tst)
    altered[TEST] = tst

    backup = PKG / 'backup' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True)
    for path in originals:
        backup_path = backup / path.relative_to(ROOT)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        backup_path.write_text(originals[path], encoding='utf-8')
    for path, body in altered.items():
        path.write_text(body, encoding='utf-8')
    lines = ['# R3-G modified source units', '']
    selected = {
        LIT: {'_toda45_universal_statement', '_register_toda45', 'build_typed_literature_bridge'},
        SPEC: {'_linear_scalar_expression', '_bind_symbolic_constraints', 'specialize_typed_statement'},
        TEST: {node.name for node in ast.parse(altered[TEST]).body
               if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')},
    }
    for path, names in selected.items():
        content = altered[path]
        tree = ast.parse(content)
        nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and node.name in names]
        lines += [f'## {path.relative_to(ROOT)}', '', '```python']
        if path == LIT or path == SPEC:
            top_imports = [node for node in tree.body
                           if isinstance(node, (ast.Import, ast.ImportFrom))]
            lines += ['\n'.join(content.splitlines()[node.lineno-1:node.end_lineno])
                      for node in top_imports]
        for node in nodes:
            lines.append('\n'.join(content.splitlines()[node.lineno-1:node.end_lineno]))
            lines.append('')
        lines += ['```', '']
    (PKG / 'MODIFIED_FUNCTIONS.md').write_text('\n'.join(lines), encoding='utf-8')
    print('R3-G modified:', *(str(p.relative_to(ROOT)) for p in altered), sep='\n  ')
    print('BACKUP:', backup)
    print('Full pytest: NOT RUN')


if __name__ == '__main__':
    install()
