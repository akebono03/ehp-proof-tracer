"""R27-R22-R1: syntax-aware guarded installation of Group Query migration."""
import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
TARGET = ROOT / "web_group_query.py"
PACKAGE = Path(__file__).resolve().parent
REQUIRED = {
    "phase165_r52_partial_proof": ("GroupStructureStatus", "ProofSearchStatus"),
    "phase165_r52_r5_auto_search": ("search_group_structure_automatically",),
    "proof": ("Relation", "RelationType"),
    "toda_presentation": ("build_toda_group_structure_presentation",),
    "toda_human_readable_renderer": ("render_toda_group_structure_latex",),
}
REMOVE = {
    "toda_calculation_facade": {"build_standard_toda_report"},
    "toda_human_readable_renderer": {"render_toda_group_result_latex"},
}
NEW_FUNCTION = '''def build_standard_web_group_query_view(
  n: int,
  k: int,
) -> WebGroupQueryView:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = classify_toda_group_query_domain(
    query
  )

  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    return WebGroupQueryView(
      n=n,
      k=k,
      status=TodaCalculationStatus.FOUND,
      result_latex=render_toda_group_query_domain_latex(domain),
      proof_available=False,
    )

  result = search_group_structure_automatically(n=n, k=k)
  conclusion = result.conclusion
  if (
    result.status is ProofSearchStatus.COMPLETE
    and result.structure_status is GroupStructureStatus.KNOWN
    and isinstance(conclusion, Relation)
    and conclusion.relation_type is RelationType.EQUALITY
    and conclusion.lhs == query.target
  ):
    structure_latex = render_toda_group_structure_latex(
      build_toda_group_structure_presentation(conclusion.rhs)
    )
    return WebGroupQueryView(
      n=n,
      k=k,
      status=TodaCalculationStatus.FOUND,
      result_latex=structure_latex,
      proof_available=True,
    )

  return WebGroupQueryView(
    n=n,
    k=k,
    status=TodaCalculationStatus.NOT_FOUND,
    result_latex=None,
    proof_available=False,
  )
'''


def node_span(source, node):
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))


def patch_source(source):
    tree = ast.parse(source)
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "build_standard_web_group_query_view"]
    if len(funcs) != 1:
        raise RuntimeError("Expected exactly one Group Query function")
    fn = funcs[0]
    calls = {n.func.id for n in ast.walk(fn) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    if "build_standard_toda_report" not in calls:
        if "search_group_structure_automatically" in calls:
            return source, False
        raise RuntimeError("Unrecognized Group Query implementation; no changes made")
    if "search_group_structure_automatically" in calls:
        raise RuntimeError("Mixed old/new Group Query implementation; no changes made")
    changes = [( *node_span(source, fn), NEW_FUNCTION)]
    found = {m: set() for m in REQUIRED}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.level or node.module is None:
            continue
        module = node.module
        if module in REQUIRED:
            found[module].update(alias.name for alias in node.names)
        unwanted = REMOVE.get(module, set())
        if not unwanted or not any(alias.name in unwanted for alias in node.names):
            continue
        if any(alias.name in unwanted and alias.asname for alias in node.names):
            raise RuntimeError("Aliased legacy import needs manual review")
        remaining = [a for a in node.names if a.name not in unwanted]
        replacement = "" if not remaining else "from " + module + " import " + ", ".join(a.name + (" as " + a.asname if a.asname else "") for a in remaining) + "\n"
        changes.append((*node_span(source, node), replacement))
        found.setdefault(module, set()).difference_update(unwanted)
    absent = [(module, name) for module, names in REQUIRED.items() for name in names if name not in found[module]]
    if absent:
        position = node_span(source, fn)[0]
        insertion = "".join(f"from {module} import {name}\n" for module, name in absent) + "\n"
        changes.append((position, position, insertion))
    patched = source
    for start, end, replacement in sorted(changes, key=lambda change: (change[0], change[1]), reverse=True):
        patched = patched[:start] + replacement + patched[end:]
    ast.parse(patched)
    if "build_standard_toda_report" in patched or "render_toda_group_result_latex" in patched:
        raise RuntimeError("Legacy Group Query symbols remain; no changes made")
    return patched, True


def main():
    original = TARGET.read_text(encoding="utf-8")
    updated, changed = patch_source(original)
    if not changed:
        print("R27-R22 already installed")
        return
    backup = PACKAGE / "web_group_query.before_r22_r1.py"
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding="utf-8")
    print("R27-R22-R1 installed: syntax-aware import repair and common Backward Search wiring")


if __name__ == "__main__":
    main()
