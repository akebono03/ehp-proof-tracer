from pathlib import Path
import ast

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r55_nk_only_goal import search_group_from_registered_goal

def test_current_search_entry_is_callable():
    assert callable(search_group_from_registered_goal)

def test_incomplete_result_does_not_claim_conclusion():
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
        diagnostics=("missing typed inference",), open_goals=("remaining",),
    )
    assert result.conclusion is None
    assert result.open_goals

def test_no_historical_probe_import_in_shared_search():
    source = (Path(__file__).resolve().parents[1] / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
    assert not any(module and module.startswith("probes.probe_phase") for module in modules)
