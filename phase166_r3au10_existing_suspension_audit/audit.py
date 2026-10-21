"""R3-AU-10: read-only audit of the existing suspension completion."""
from __future__ import annotations
import argparse
import csv
import inspect
import json
from collections import Counter
from pathlib import Path

def inspect_code(root: Path) -> dict:
    import sys
    sys.path.insert(0, str(root))
    import phase166_r3aj_structured_generator as module
    from expression import Composition, IteratedSuspension, Multiple, Sum
    source = inspect.getsource(module.structured_generator_from_ids)
    base_source = inspect.getsource(module._base_element)
    goal_source = inspect.getsource(module.database_structured_group_goal_candidates)
    return {
        "module": str(Path(module.__file__).resolve()),
        "structured_generator_from_ids_present": callable(module.structured_generator_from_ids),
        "base_element_present": callable(module._base_element),
        "goal_candidates_present": callable(module.database_structured_group_goal_candidates),
        "current_dimension_advanced_by_k": "current_dimension += int(row[\"k\"])" in source,
        "base_element_uses_dimension_minus_initial_n": "dimension - initial_n" in base_source,
        "base_element_uses_iterated_suspension": "IteratedSuspension" in base_source,
        "goal_uses_gen_coe": "component.gen_coe" in goal_source,
        "goal_constructs_multiple": "Multiple(coefficient, representative)" in goal_source,
        "goal_constructs_sum": "Sum(generator, term)" in goal_source,
        "typed_node_names": [x.__name__ for x in (Composition, IteratedSuspension, Multiple, Sum)],
    }

def inspect_data(root: Path, limit: int | None = None) -> tuple[dict, list[dict]]:
    import sys
    sys.path.insert(0, str(root))
    from phase166_r3aj_structured_generator import structured_generator_from_ids
    source = root / "data" / "sphere.csv"
    master = root / "data" / "HyoujiGen.csv"
    if not source.is_file() or not master.is_file():
        raise FileNotFoundError("data/sphere.csv and data/HyoujiGen.csv are required")
    with source.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    results = []
    counts = Counter()
    for line, row in enumerate(rows, 2):
        if not row.get("n", "").strip() or not row.get("Element", "").strip():
            counts["SEPARATOR_OR_EMPTY"] += 1
            continue
        try:
            n = int(row["n"])
            ids = [int(x) for x in row["Element"].split()]
        except ValueError:
            counts["INVALID_INPUT"] += 1
            continue
        try:
            expression = structured_generator_from_ids(ids=ids, start_dimension=n, generator_csv=master)
            state = "BUILT" if expression is not None else "NOT_BUILT"
            name = type(expression).__name__ if expression is not None else ""
        except (ValueError, TypeError, KeyError, IndexError) as exc:
            state = "ERROR"
            name = type(exc).__name__
        counts[state] += 1
        results.append({"csv_line":line,"n":row.get("n",""),"k":row.get("k",""),"id":row.get("id",""),"Element":row.get("Element",""),"state":state,"result_node":name})
        if limit is not None and len(results) >= limit:
            break
    return {"data_rows_checked":len(results),"counts":dict(counts),"latex_mathematically_certified":0},results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",type=Path,default=Path.cwd())
    p.add_argument("--limit",type=int,default=None)
    a=p.parse_args()
    repo=a.repo.resolve()
    result=inspect_code(repo)
    data,rows=inspect_data(repo,a.limit)
    result.update({"phase":"166 R3-AU-10","data":data,"production_code_modified":False,"full_pytest_run":False})
    out=Path(__file__).resolve().parent/"results"
    out.mkdir(exist_ok=True)
    (out/"summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with (out/"construction_rows.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["csv_line","n","k","id","Element","state","result_node"])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
