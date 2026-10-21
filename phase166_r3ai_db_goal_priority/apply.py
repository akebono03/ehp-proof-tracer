from pathlib import Path
import ast
import shutil
import sys

ROOT = Path.cwd()
ADAPTER = ROOT / 'phase166_r3af_goal_adapter.py'
SELECTOR = ROOT / 'phase165_r55_nk_only_goal.py'
BACKUP = ROOT / 'phase166_r3ai_db_goal_priority_backup'

NEW_ADAPTER = '''def database_group_goal_candidates(*, n: int, k: int, csv_path=None):
    """Convert unambiguous CSV structures to proof goals, never evidence.

    Direct nonstable rows are eligible. Stable targets use the stable base
    when no direct row exists. Unsupported labels and zero groups remain
    explicitly unconverted in this phase.
    """
    if type(n) is not int or type(k) is not int or n <= 0 or k < 0:
        return ()
    path = Path(csv_path) if csv_path is not None else Path(__file__).resolve().parent / "data" / "sphere.csv"
    if not path.is_file():
        return ()
    repo = SphereRepository(path)
    rows = repo.df[(repo.df["n"] == n) & (repo.df["k"] == k)]
    if not rows.empty:
        base_n = n
    elif n >= k + 2:
        base_n = k + 2
    else:
        return ()
    source = repo.get_group(base_n, k)
    if not source.components:
        return ()
    pieces = []
    for component in source.components:
        generator = _generator_for_target(component.generator, base_n, n, k)
        if generator is None:
            return ()
        if component.order == inf:
            pieces.append(FreeCyclicGroup(generator))
        elif type(component.order) is int and component.order > 1:
            pieces.append(FiniteCyclicGroup(component.order, generator))
        else:
            return ()
    structure = pieces[0] if len(pieces) == 1 else DirectSumGroup(tuple(pieces))
    return (Relation(TodaPrimaryGroup(n+k, n), structure, RelationType.EQUALITY),)
'''

NEW_SELECTOR = '''def registered_group_goal_candidates(bridge, *, n: int, k: int):
    """Prefer typed DB targets; retain registry fallback for unsupported rows.

    DB data define the goal only, and are never inserted as ProofSteps or
    GIVEN evidence. The registry remains the source of proof premises.
    """
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r57_r8_eta_specialization import specialized_eta_group_goal_candidates
    from phase166_r3af_goal_adapter import database_group_goal_candidates

    database = database_group_goal_candidates(n=n, k=k)
    if database:
        return database
    existing = _phase165_r57_r8_previous_registered_group_goal_candidates(
        bridge=bridge, n=n, k=k,
    )
    if not isinstance(existing, tuple):
        raise TypeError("R55 selector must return a tuple")
    group = TodaPrimaryGroup(group_dimension=n+k, sphere_dimension=n)
    symbolic = specialized_eta_group_goal_candidates(group, bridge)
    output = list(existing)
    for candidate in symbolic:
        if not any(type(candidate) is type(old) and candidate == old for old in output):
            output.append(candidate)
    return tuple(output)
'''

def replace_last_function(source, name, replacement):
    tree = ast.parse(source)
    nodes = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == name]
    if not nodes:
        raise RuntimeError(f'Missing function {name}')
    node = nodes[-1]
    lines = source.splitlines(keepends=True)
    return ''.join(lines[:node.lineno-1]) + replacement + '\n' + ''.join(lines[node.end_lineno:])

def main():
    if not ADAPTER.is_file() or not SELECTOR.is_file():
        raise RuntimeError('Run from ehp-proof-tracer repository root')
    a, s = ADAPTER.read_text(encoding='utf-8-sig'), SELECTOR.read_text(encoding='utf-8-sig')
    if 'Direct nonstable rows are eligible.' in a and 'Prefer typed DB targets;' in s:
        print('ALREADY_APPLIED')
        return
    for term in ('def database_group_goal_candidates(', 'repo.get_group(base_n, k)'):
        if term not in a:
            raise RuntimeError('Adapter differs from inspected baseline: ' + term)
    for term in ('_phase165_r57_r8_previous_registered_group_goal_candidates', 'def registered_group_goal_candidates('):
        if term not in s:
            raise RuntimeError('Selector differs from inspected baseline: ' + term)
    new_a = replace_last_function(a, 'database_group_goal_candidates', NEW_ADAPTER)
    new_s = replace_last_function(s, 'registered_group_goal_candidates', NEW_SELECTOR)
    ast.parse(new_a); ast.parse(new_s)
    BACKUP.mkdir(exist_ok=True)
    shutil.copy2(ADAPTER, BACKUP / ADAPTER.name)
    shutil.copy2(SELECTOR, BACKUP / SELECTOR.name)
    ADAPTER.write_text(new_a, encoding='utf-8')
    SELECTOR.write_text(new_s, encoding='utf-8')
    print('PATCHED:', ADAPTER.name, SELECTOR.name)
    print('BACKUP:', BACKUP)

if __name__ == '__main__':
    main()
