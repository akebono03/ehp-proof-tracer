"""R17R1: exact historical test-contract correction; never touch production proof logic."""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py")
EXPECTED_BLOB = "b085e0c93878d08245beed6d675cf4531f139234"
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) /
          "EHPProofTracerAudit" / "phase174_r3_r7_r17r1" / "test_open_goals.original.py")
OLD_PARAMS = "@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2), (5, 3, 3)))"
NEW_PARAMS = "@pytest.mark.parametrize('n,k,expected', ((4, 8, 3), (4, 9, 2)))"
NEXT_FUNCTION = "\n\ndef test_same_latex_is_not_sufficient_to_merge_distinct_typed_structures() -> None:\n"
NEW_TEST = '''\n\ndef test_pi8_5_completed_case_is_not_reported_as_an_open_goal() -> None:
    """The formerly partial (n=5,k=3) case must retain its completed proof."""
    typed = exact_prior_database_result(5, 3)
    assert typed is not None
    result = search_group_from_registered_goal(n=5, k=3, goal=typed)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == typed
    assert result.open_goals == ()
    assert any(step.conclusion == typed for step in result.proven_steps)
    model = build_proof_narrative_model(result)
    assert model.steps == result.proven_steps
    assert model.root_index is not None
    assert project_typed_open_goal_displays(result.open_goals) == ()
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "## 未解決 Goal" not in markdown
    view = build_standard_web_group_proof_view(
        n=5, k=3, goal=typed, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert not any(line.kind == "heading" and line.prefix == "未解決 Goal"
                   for line in view.rendered_lines)
'''


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def normalized(raw: bytes) -> tuple[str, bytes]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM")
    remains = raw.replace(b"\r\n", b"")
    if b"\r" in remains or (b"\r\n" in raw and b"\n" in remains):
        raise RuntimeError("Mixed or malformed EOL")
    return raw.replace(b"\r\n", b"\n").decode("utf-8"), (b"\r\n" if b"\r\n" in raw else b"\n")


def original_matches(raw: bytes) -> bool:
    try:
        source, _ = normalized(raw)
    except (UnicodeError, RuntimeError):
        return False
    lf = source.encode("utf-8")
    return any(blob_sha(v) == EXPECTED_BLOB for v in (raw, lf, lf.replace(b"\n", b"\r\n")))


def transform(source: str) -> str:
    """Replace a stale parametrization and add a real completed-case test."""
    before = ast.parse(source)
    functions = [x.name for x in before.body if isinstance(x, ast.FunctionDef)]
    if (source.count(OLD_PARAMS) != 1 or source.count(NEXT_FUNCTION) != 1
            or NEW_PARAMS in source or "test_pi8_5_completed_case_is_not_reported_as_an_open_goal" in source
            or functions.count("test_real_typed_pending_goals_are_grouped_only_in_public_display") != 1):
        raise RuntimeError("Reviewed historical test anchors changed or already patched")
    out = source.replace(OLD_PARAMS, NEW_PARAMS, 1).replace(
        NEXT_FUNCTION, NEW_TEST + NEXT_FUNCTION, 1,
    )
    new_functions = [x.name for x in ast.parse(out).body if isinstance(x, ast.FunctionDef)]
    added = [x for x in new_functions if x not in functions]
    if (added != ["test_pi8_5_completed_case_is_not_reported_as_an_open_goal"]
            or len(new_functions) != len(functions) + 1):
        raise RuntimeError("Unexpected test functions changed")
    compile(out, str(TARGET), "exec")
    return out


def patched_bytes(original: bytes) -> bytes:
    if not original_matches(original):
        raise RuntimeError("Historical test source does not match reviewed GitHub blob")
    source, eol = normalized(original)
    return transform(source).encode("utf-8").replace(b"\n", eol)


def run(*, mode: str, root: Path = ROOT) -> str:
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("Historical typed Goal test is missing")
    if mode in ("dry-run", "apply"):
        original = target.read_bytes()
        expected = patched_bytes(original)
        if mode == "dry-run":
            return "PASS_PREFLIGHT"
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if BACKUP.is_file() and BACKUP.read_bytes() != original:
            raise RuntimeError("Conflicting backup; do not overwrite")
        BACKUP.write_bytes(original)
        target.write_bytes(expected)
        if target.read_bytes() != expected:
            target.write_bytes(original)
            raise RuntimeError("Historical test write verification failed")
        return "PASS_APPLIED"
    if mode == "rollback":
        if not BACKUP.is_file():
            return "NO_BACKUP"
        original = BACKUP.read_bytes()
        candidate = patched_bytes(original)
        current = target.read_bytes()
        if current == original:
            return "ALREADY_ORIGINAL"
        if current != candidate:
            raise RuntimeError("Refusing rollback of unreviewed file content")
        target.write_bytes(original)
        return "RESTORED"
    raise ValueError("Unknown mode")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    mode = "dry-run" if args.dry_run else "apply" if args.apply else "rollback"
    print("PHASE174_R3R7R17R1_TEST_PATCH=" + run(mode=mode))
    print("PHASE174_R3R7R17R1_TEST_PATH=" + str(TARGET))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
