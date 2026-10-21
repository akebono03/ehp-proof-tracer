"""Replace one complete R3-V regression test function, guarding the original text."""
from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path

PATH = Path("phase166_r3v_test_repair/test_r3v.py")
NAME = "test_r3v_registered_prior_and_shared_search_connection"
OLD = '    # Do not assert object equality: source and eta-definition names may differ.\n    # The proof search must still establish any needed representation identity.\n    options = shared_expansion_provider(screened,proof_target=named)(named)\n    assert any(option.subgoals == (transported, witness) for option in options)\n'
NEW = '    # The prior generator is the exact registered one (η_3), not the\n    # differently spelled η₃ element returned by the definition factory.\n    options = shared_expansion_provider(screened, proof_target=named)(named)\n    candidates = [\n        option for option in options\n        if option.rule.name == "proved generator suspension normalizes transported cyclic group"\n        and len(option.subgoals) == 2\n        and option.subgoals[1] == witness\n    ]\n    assert candidates, "registered prior did not produce the R3-V normalization"\n    assert any(\n        isinstance(option.subgoals[0], Relation)\n        and option.subgoals[0].lhs == named.lhs\n        and isinstance(option.subgoals[0].rhs, FiniteCyclicGroup)\n        and option.subgoals[0].rhs.order == 2\n        and any(\n            option.subgoals[0].rhs.generator == IteratedSuspension(item.rhs.generator, 1)\n            for item in prior\n        )\n        for option in candidates\n    ), "R3-V transport must use the registered generator without inventing a source"\n    assert all(\n        option.rule.match_guard(\n            (\n                ProofStep(option.subgoals[0], (), ProofRule.GIVEN),\n                ProofStep(option.subgoals[1], (), ProofRule.GIVEN),\n            ),\n            {},\n        )\n        for option in candidates\n    ), "R3-V inference rule must accept the actual typed premises"\n'


def main():
    if not PATH.is_file():
        raise SystemExit("STOP: R3-V test file missing; no changes")
    source = PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == NAME]
    if len(matches) != 1:
        raise SystemExit("STOP: R3-V test function not unique")
    lines = source.splitlines(keepends=True)
    fn = matches[0]
    start, end = fn.lineno - 1, fn.end_lineno
    existing = "".join(lines[start:end])
    if OLD not in existing:
        if NEW in existing:
            print("ALREADY_PATCHED:", PATH)
            return
        raise SystemExit("STOP: R3-V test body differs from reviewed GitHub version")
    changed = existing.replace(OLD, NEW, 1)
    replacement = "".join(lines[:start]) + changed + "".join(lines[end:])
    ast.parse(replacement)
    backup = Path("phase166_r3ac_r3v_test_backups") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup.mkdir(parents=True, exist_ok=False)
    (backup / PATH.name).write_text(source, encoding="utf-8")
    PATH.write_text(replacement, encoding="utf-8")
    Path("phase166_r3ac_r3v_test_alignment/modified_test_function.txt").write_text(changed,encoding="utf-8")
    print("PATCHED:", PATH, "FUNCTION:", NAME)
    print("BACKUP:", backup)
    print("PRODUCTION_CODE_MODIFIED: false")


if __name__ == "__main__":
    main()
