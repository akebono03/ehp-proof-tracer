# R17 追加コード全文

既存関数 `web_group_proof_common._group_proof_statement_latex` は Source Guard 検査後、DryRun 時に `MODIFIED_FUNCTION_FULL_JA.md` へ全文出力する。ファイル先頭の import 変更はない。

## `patch.py`

```python
"""Guarded R17 replacement of one common typed statement formatting function.

The proof search, mathematical rules, and shared Narrative model are untouched.
The target is source-checked and the entire replacement function is exported.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("web_group_proof_common.py")
EXPECTED_BLOB = "0126fd71c66257fc2f4f498a5357d44a67a55884"
PACKAGE = ROOT / "phase174_r3_r7_r17_typed_map_open_goal"
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
          / "EHPProofTracerAudit" / "phase174_r3_r7_r17"
          / "web_group_proof_common.original.py")
OUTPUT = PACKAGE / "MODIFIED_FUNCTION_FULL_JA.md"

OLD = (
    "  from proof import Relation, RelationType\n"
    "\n"
    "  if (\n"
    "    isinstance(statement, CyclicStructureStatement)\n"
)
NEW = (
    "  from proof import Relation, RelationType\n"
    "  from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaSuspensionMap\n"
    "  from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective\n"
    "  from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex\n"
    "\n"
    "  # A display projection of the typed map property, never a proof claim.\n"
    "  if isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism)):\n"
    "    mapping = statement.map\n"
    "    if isinstance(mapping, (TodaDeltaMap, TodaSuspensionMap, TodaHopfInvariantMap)):\n"
    "      source = group_tex(mapping.source_group)\n"
    "      target = group_tex(mapping.target_group)\n"
    "      symbol = map_symbol_tex(mapping)\n"
    "      if source is not None and target is not None and symbol is not None:\n"
    "        arrow = (\n"
    "          r'\\hookrightarrow' if isinstance(statement, MapInjective)\n"
    "          else r'\\twoheadrightarrow' if isinstance(statement, MapSurjective)\n"
    "          else r'\\xrightarrow{\\cong}'\n"
    "        )\n"
    "        return (f'{symbol}: {source} {arrow} {target}', None)\n"
    "\n"
    "  if (\n"
    "    isinstance(statement, CyclicStructureStatement)\n"
)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalize_and_style(data: bytes) -> tuple[str, bytes]:
    """Preserve uniform LF/CRLF; refuse BOM, mixed EOL or bare CR."""
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in common formatter")
    remainder = data.replace(b"\r\n", b"")
    if b"\r" in remainder or (b"\r\n" in data and b"\n" in remainder):
        raise RuntimeError("Malformed source line endings")
    return data.replace(b"\r\n", b"\n").decode("utf-8"), (b"\r\n" if b"\r\n" in data else b"\n")


def matches_git_blob(data: bytes, sha: str) -> bool:
    try:
        text, _ = normalize_and_style(data)
    except (UnicodeError, RuntimeError):
        return False
    normalized = text.encode("utf-8")
    return any(blob_sha(x) == sha for x in (data, normalized, normalized.replace(b"\n", b"\r\n")))


def transform_source(source: str) -> str:
    """Alter exactly one current common formatter without a special n/k branch."""
    if source.count(OLD) != 1 or NEW in source:
        raise RuntimeError("Expected one unpatched common map formatter anchor")
    before = ast.parse(source)
    functions = [n for n in before.body if isinstance(n, ast.FunctionDef)]
    if sum(n.name == "_group_proof_statement_latex" for n in functions) != 1:
        raise RuntimeError("Common typed formatter function missing or duplicated")
    replaced = source.replace(OLD, NEW, 1)
    after = ast.parse(replaced)
    before_public = [n.name for n in before.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    after_public = [n.name for n in after.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    if before_public != after_public:
        raise RuntimeError("Unexpected public class/function changes")
    compile(replaced, str(TARGET), "exec")
    return replaced


def expected_patched_bytes(original: bytes) -> bytes:
    source, eol = normalize_and_style(original)
    if not matches_git_blob(original, EXPECTED_BLOB):
        raise RuntimeError("Common formatter differs from pinned GitHub blob")
    return transform_source(source).encode("utf-8").replace(b"\n", eol)


def export_complete_function(source: str, destination: Path = OUTPUT) -> None:
    """Write the entire *actual* modified function extracted from the AST."""
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "_group_proof_statement_latex"]
    if len(nodes) != 1:
        raise RuntimeError("Expected one complete formatter function")
    lines = source.splitlines()
    fn = nodes[0]
    complete = "\n".join(lines[fn.lineno - 1:fn.end_lineno])
    destination.write_text(
        "# R17 変更後の関数全文\n\n"
        "変更対象: `web_group_proof_common.py` の `_group_proof_statement_latex`。\n\n"
        "この関数内の import ブロックも省略せず含みます。"
        "ファイル先頭の import は変更ありません。\n\n"
        "```python\n" + complete + "\n```\n",
        encoding="utf-8",
    )


def guarded_patch(*, dry_run: bool, root: Path = ROOT) -> dict[str, str]:
    """Never overwrite a nonmatching checkout; preserve backup on application."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("Missing common formatter")
    original = path.read_bytes()
    result = expected_patched_bytes(original)
    output_source, _ = normalize_and_style(result)
    export_complete_function(output_source, root / OUTPUT.relative_to(ROOT))
    summary = {
        "before_sha": blob_sha(normalize_and_style(original)[0].encode("utf-8")),
        "after_sha": blob_sha(output_source.encode("utf-8")),
        "full_function": str(root / OUTPUT.relative_to(ROOT)),
    }
    if dry_run:
        return summary
    backup = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / "web_group_proof_common.original.py"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and backup.read_bytes() != original:
        raise RuntimeError("Conflicting existing R17 source backup")
    backup.write_bytes(original)
    path.write_bytes(result)
    if path.read_bytes() != result:
        path.write_bytes(original)
        raise RuntimeError("R17 patched bytes failed verification")
    summary["backup"] = str(backup)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    summary = guarded_patch(dry_run=args.dry_run)
    for label, value in summary.items():
        print("PHASE174_R3R7R17_PATCH_" + label.upper() + "=" + value)
    print("PHASE174_R3R7R17_PATCH_GATE=" + ("PASS_PREFLIGHT" if args.dry_run else "PASS_APPLIED"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `audit.py`

```python
"""R17: reviewed source and public typed pending map-goal display audit.

No map surjectivity or isomorphism is assumed. Audit distinguishes a cyclic
MapIsomorphism candidate from an independent certified proof.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, TARGET, blob_sha, expected_patched_bytes,
    matches_git_blob, normalize_and_style,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R17"
PRE_R16_HEAD = "e7bcd34a526b3f885a8e3be81c4aac362d8834c7"
REVIEWED_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
R16_PREFIX = "phase174_r3_r7_r16_public_ehp_zero_root/"
SHARED_MATH = "phase165_r52_r9_shared_math.py"
R15_SHARED_BLOB = "7f81769776278b46a220fb90771970a9dd7c73c2"
R16_SHARED_BLOB = "d42bb7420cf58f4dd466511d6498c66d9917b29c"
PINS = {
    "phase168_r3_27_typed_statement_projection.py": "26ce3632fe1b32bab7e822e8f701409b26f4f04a",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r16_public_ehp_zero_root/audit.py": "68e7611ede13f17a3358ee0754f5e296686ae042",
}


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
    ).stdout


def reviewed_lineage(local: str, remote: str, committed: tuple[str, ...],
                     modified: tuple[str, ...], patched: bool) -> str:
    """Accept precisely the R16 working-tree handoff or merged state."""
    if remote != REVIEWED_HEAD or local not in (PRE_R16_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed local/remote develop HEAD; no automatic overwrite")
    if not committed or SHARED_MATH not in committed or not any(
        x.startswith(R16_PREFIX) for x in committed
    ) or any(x != SHARED_MATH and not x.startswith(R16_PREFIX) for x in committed):
        raise RuntimeError("Remote R16 lineage contains unexpected paths")
    target = TARGET.as_posix()
    initial = (SHARED_MATH,) if local == PRE_R16_HEAD else ()
    expected = tuple(sorted(initial + ((target,) if patched else ())))
    if tuple(sorted(modified)) != expected:
        raise RuntimeError("Unexpected local tracked changes: " + repr(modified))
    return ("LOCAL_R16_PATCH_UNCOMMITTED" if local == PRE_R16_HEAD
            else "R16_MERGED_CLEAN")


def verify_git_and_sources(*, patched: bool, root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R17 directly below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Expected develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    local = git("rev-parse", "HEAD", root=root)
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged modifications require independent review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    git_bytes("merge-base", "--is-ancestor", PRE_R16_HEAD, REVIEWED_HEAD, root=root)
    commits = git("rev-list", "--reverse", PRE_R16_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines()
    if len(commits) != 1:
        raise RuntimeError("Expected one reviewed R16 merge commit")
    diff_paths = tuple(git("diff", "--name-only", PRE_R16_HEAD, REVIEWED_HEAD, root=root).splitlines())
    lineage = reviewed_lineage(local, remote, diff_paths, changed, patched)
    for name, sha in PINS.items():
        file = root / name
        if not file.is_file() or not matches_git_blob(file.read_bytes(), sha):
            raise RuntimeError("R17 source pin changed: " + name)

    tracked_formatter = git_bytes("show", "HEAD:" + TARGET.as_posix(), root=root)
    if not matches_git_blob(tracked_formatter, EXPECTED_BLOB):
        raise RuntimeError("GitHub common formatter changed since review")
    target = root / TARGET
    source, _ = normalize_and_style(target.read_bytes())
    old, _ = normalize_and_style(tracked_formatter)
    expected = (normalize_and_style(expected_patched_bytes(tracked_formatter))[0]
                if patched else old)
    if source != expected:
        raise RuntimeError("Unreviewed local common formatter; abort")
    head_math = git_bytes("show", "HEAD:" + SHARED_MATH, root=root)
    expected_head = R15_SHARED_BLOB if local == PRE_R16_HEAD else R16_SHARED_BLOB
    if not matches_git_blob(head_math, expected_head):
        raise RuntimeError("R16 Git math baseline mismatch")
    if not matches_git_blob((root / SHARED_MATH).read_bytes(), R16_SHARED_BLOB):
        raise RuntimeError("Applied R16 shared math patch missing or altered")
    return {
        "local_head": local, "remote_head": remote,
        "lineage": lineage, "source_guard": "PASS",
        "pinned_paths": len(PINS) + 2, "modified_paths": changed,
        "r16_math_preserved": True,
    }


def previous_report_path() -> Path:
    home = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return home / "EHPProofTracerAudit" / "phase174_r3_r7_r16" / "public_ehp_root_audit.json"


def validate_r16_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R16"
            or report.get("gate") != "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN"
            or report.get("new_group_given") != 0
            or report.get("new_mathematical_inference_rules") != 0
            or report.get("full_pytest_run") is not False
            or report.get("root_proof_completed_claimed") is not False):
        raise RuntimeError("Prior R16 source-first result is not certified")
    live = report.get("live") or {}
    # R16 report structure is independently audited again in live R17, below.
    return {"gate": report["gate"], "root_was_not_completed": True}


def inspect_public_map_display() -> dict[str, Any]:
    """Compare real goal proof search, public math text, and cyclic iso branch."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import (
        MapInjective, MapIsomorphism, MapSurjective, expand_generic_iso_goal,
    )
    from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs, RULE_NAME
    from proof import ProofRule
    from web_group_proof_common import _group_proof_statement_latex

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    components = ehp_zero_inputs(goal)
    if components is None or len(components) != 4:
        raise RuntimeError("Typed EHP root obligations changed")
    surj = components[0]
    assert isinstance(surj, MapSurjective)
    rendered, fallback = _group_proof_statement_latex(surj)
    expected = r"\Delta: \pi_{13}^{13} \twoheadrightarrow \pi_{11}^{6}"
    if rendered != expected or fallback is not None:
        raise RuntimeError("Generic typed Delta-surjectivity math is not rendered")
    iso = MapIsomorphism(surj.map)
    iso_latex, iso_fallback = _group_proof_statement_latex(iso)
    inj_latex, inj_fallback = _group_proof_statement_latex(MapInjective(surj.map))
    if (iso_latex != r"\Delta: \pi_{13}^{13} \xrightarrow{\cong} \pi_{11}^{6}"
            or iso_fallback is not None
            or inj_latex != r"\Delta: \pi_{13}^{13} \hookrightarrow \pi_{11}^{6}"
            or inj_fallback is not None):
        raise RuntimeError("General typed map-property LaTeX is inconsistent")

    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    provider = shared_expansion_provider(screened, proof_target=goal)
    root_options = tuple(provider(goal))
    surj_options = tuple(provider(surj))
    iso_options = tuple(provider(iso))
    generic_iso = tuple(expand_generic_iso_goal(iso))
    if (len(root_options) != 1 or root_options[0].rule.name != RULE_NAME
            or root_options[0].subgoals != components or surj_options):
        raise RuntimeError("R16 root or unresolved Delta-surjectivity baseline changed")
    cyclic_iso = bool(generic_iso) and surj in generic_iso[0].subgoals
    if not cyclic_iso:
        raise RuntimeError("Generic isomorphism proof dependency was unexpectedly changed")
    if any(link.step is not None and link.step.conclusion in (goal, surj, iso)
           and link.step.rule is ProofRule.GIVEN for link in screened.proof_links):
        raise RuntimeError("Target, Delta surjectivity, or Delta isomorphism was a direct GIVEN")

    result = search_group_from_registered_goal(n=7, k=5, bridge=bridge, goal=goal)
    if (result.status is ProofSearchStatus.COMPLETE or result.conclusion is not None
            or any(step.conclusion == goal for step in result.proven_steps)
            or not any(open_goal == surj for open_goal in result.open_goals)):
        raise RuntimeError("Unexpected claim of completed target proof or lost Delta goal")
    markdown = render_partial_proof_markdown(result)
    if ("$" + expected + "$" not in markdown
            or "MapSurjective（数式表示未対応）" in markdown):
        raise RuntimeError("Public common partial renderer did not display Delta math")
    return {
        "public_root_candidates": len(root_options),
        "public_delta_surjectivity_candidates": len(surj_options),
        "public_delta_isomorphism_candidates": len(iso_options),
        "generic_isomorphism_depends_on_surjectivity": cyclic_iso,
        "direct_given_for_goal_or_delta": False,
        "delta_latex": rendered,
        "search_status": result.status.value,
        "open_goal_types": [type(item).__name__ for item in result.open_goals],
        "proven_steps": len(result.proven_steps),
        "math_rule_changes": 0,
        "new_proof_steps": 0,
        "completion_claimed": False,
    }


def report_path(*, dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    name = "typed_map_preflight.json" if dry_run else "typed_map_public_audit.json"
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r17" / name


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(patched=not dry_run, root=root)
    prior = previous_report_path()
    if not prior.is_file():
        raise RuntimeError("R16 public audit evidence not found: " + str(prior))
    previous = validate_r16_report(json.loads(prior.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_public_map_display()
    return {
        "phase": PHASE, "git_state": state, "previous": previous,
        "mode": "PREFLIGHT" if dry_run else "TYPED_PUBLIC_MAP_GOAL_DISPLAY",
        "live": live,
        "new_group_given": 0, "new_math_rules": 0,
        "production_math_modified": False,
        "full_pytest_run": False, "completion_claimed": False,
        "gate": ("PASS_PREFLIGHT" if dry_run else
                 "PASS_TYPED_DELTA_OPEN_GOAL_SURJECTIVITY_STILL_PENDING"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = report_path(dry_run=args.dry_run)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R17_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["lineage"])
    print(prefix + "SOURCE_GUARD=PASS")
    if report["live"] is not None:
        live = report["live"]
        print(prefix + "ROOT_PROPOSALS=" + str(live["public_root_candidates"]))
        print(prefix + "DELTA_SURJECTIVITY_PROPOSALS=" + str(live["public_delta_surjectivity_candidates"]))
        print(prefix + "ISOMORPHISM_PROPOSALS=" + str(live["public_delta_isomorphism_candidates"]))
        print(prefix + "ISOMORPHISM_CYCLE_GUARD=" + str(live["generic_isomorphism_depends_on_surjectivity"]))
        print(prefix + "PUBLIC_DELTA_LATEX=" + live["delta_latex"])
        print(prefix + "SEARCH_STATUS=" + live["search_status"])
        print(prefix + "SEARCH_PROVEN_STEPS=" + str(live["proven_steps"]))
        print(prefix + "OPEN_GOALS=" + str(len(live["open_goal_types"])))
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_MATH_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_patch.py`

```python
"""R17 guarded exact one-function replacement tests."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r17_typed_map_open_goal.patch import (
    EXPECTED_BLOB, NEW, OLD, blob_sha, matches_git_blob,
    normalize_and_style, transform_source, export_complete_function,
)


def source_fixture() -> str:
    return (
        "def _group_proof_statement_latex(statement):\n"
        "  from expression import Expression\n"
        "  from homotopy_groups import TodaPrimaryGroup\n"
        "  from phase165_r12_r2_quotient_rules import CyclicStructureStatement\n"
        + OLD
        + "  ):\n"
        + "    return None, None\n"
        + "  return None, 'unhandled'\n"
    )


def test_exact_single_common_formatter_replacement_preserves_public_name() -> None:
    patched = transform_source(source_fixture())
    assert patched.count(NEW) == 1
    assert "def _group_proof_statement_latex(statement):" in patched
    assert "isinstance(statement, (MapInjective, MapSurjective, MapIsomorphism))" in patched
    assert "return (f'{symbol}: {source} {arrow} {target}', None)" in patched
    assert "  return None, 'unhandled'" in patched


def test_patch_never_accepts_reapplication_or_unreviewed_anchor() -> None:
    source = source_fixture()
    with pytest.raises(RuntimeError):
        transform_source(transform_source(source))
    with pytest.raises(RuntimeError):
        transform_source(source.replace("_group_proof_statement_latex", "other_formatter"))
    with pytest.raises(RuntimeError):
        transform_source(source + OLD)


@pytest.mark.parametrize("malformed", (
    b"one\r\ntwo\n", b"one\rtwo\r", b"\xef\xbb\xbfone\n",
))
def test_reject_unsafe_end_of_line_or_bom(malformed: bytes) -> None:
    with pytest.raises(RuntimeError):
        normalize_and_style(malformed)


def test_preserve_uniform_line_endings_and_strict_sha() -> None:
    assert normalize_and_style(b"one\ntwo\n") == ("one\ntwo\n", b"\n")
    assert normalize_and_style(b"one\r\ntwo\r\n") == ("one\ntwo\n", b"\r\n")
    assert len(EXPECTED_BLOB) == 40
    sha = blob_sha(b"one\ntwo\n")
    assert matches_git_blob(b"one\ntwo\n", sha)
    assert matches_git_blob(b"one\r\ntwo\r\n", sha)
    assert not matches_git_blob(b"one changed\ntwo\n", sha)
    assert not matches_git_blob(b"one\r\ntwo\n", sha)


def test_complete_replacement_function_is_exported(tmp_path) -> None:
    path = tmp_path / "MODIFIED_FUNCTION_FULL_JA.md"
    export_complete_function(transform_source(source_fixture()), path)
    content = path.read_text(encoding="utf-8")
    assert "def _group_proof_statement_latex(statement):" in content
    assert "from proof import Relation, RelationType" in content
    assert "from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective" in content
    assert "  return None, 'unhandled'" in content
    assert "```python" in content


def test_replacement_contains_no_group_specific_dimension_or_generator() -> None:
    # The only map-specific distinction is the *type*, not a chosen n or k.
    patched = transform_source(source_fixture())
    addition = patched.split("  # A display projection", 1)[1].split("  if (\n    isinstance(statement, CyclicStructureStatement)", 1)[0]
    assert "sphere_dimension ==" not in addition
    assert "group_dimension ==" not in addition
    assert "nu_" not in addition
    assert "eta_" not in addition
```

## `tests/test_audit.py`

```python
"""Guard the R16->R17 remote lineage and non-circular theorem boundary."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r17_typed_map_open_goal.audit import (
    PRE_R16_HEAD, REVIEWED_HEAD, R16_PREFIX, SHARED_MATH,
    reviewed_lineage, validate_r16_report,
)


def committed_paths() -> tuple[str, ...]:
    return (SHARED_MATH, R16_PREFIX + "audit.py")


def test_released_r16_source_and_unchanged_math_handoff_are_accepted() -> None:
    assert reviewed_lineage(PRE_R16_HEAD, REVIEWED_HEAD,
                            committed_paths(), (SHARED_MATH,), False) == "LOCAL_R16_PATCH_UNCOMMITTED"
    assert reviewed_lineage(REVIEWED_HEAD, REVIEWED_HEAD,
                            committed_paths(), (), False) == "R16_MERGED_CLEAN"
    assert reviewed_lineage(PRE_R16_HEAD, REVIEWED_HEAD,
                            committed_paths(), (SHARED_MATH, "web_group_proof_common.py"), True) == "LOCAL_R16_PATCH_UNCOMMITTED"
    assert reviewed_lineage(REVIEWED_HEAD, REVIEWED_HEAD,
                            committed_paths(), ("web_group_proof_common.py",), True) == "R16_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,tracked,patched", (
    (PRE_R16_HEAD, PRE_R16_HEAD, committed_paths(), (SHARED_MATH,), False),
    ("f" * 40, REVIEWED_HEAD, committed_paths(), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, ("proof.py",), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, committed_paths(), ("proof.py",), False),
    (PRE_R16_HEAD, REVIEWED_HEAD, committed_paths(), (), False),
    (REVIEWED_HEAD, REVIEWED_HEAD, committed_paths(), ("web_group_proof_common.py",), False),
))
def test_unreviewed_checkout_or_tracked_change_fails_closed(local, remote, paths, tracked, patched) -> None:
    with pytest.raises(RuntimeError):
        reviewed_lineage(local, remote, paths, tracked, patched)


def valid_r16() -> dict:
    return {
        "phase": "174-R3-R7-R16",
        "gate": "PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN",
        "new_group_given": 0,
        "new_mathematical_inference_rules": 0,
        "full_pytest_run": False,
        "root_proof_completed_claimed": False,
    }


def test_valid_real_r16_report_contract() -> None:
    assert validate_r16_report(valid_r16())["root_was_not_completed"] is True


@pytest.mark.parametrize("field,value", (
    ("phase", "174-R3-R7-R15"),
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_mathematical_inference_rules", 1),
    ("full_pytest_run", True),
    ("root_proof_completed_claimed", True),
))
def test_incorrect_prior_source_or_fabricated_completion_rejected(field, value) -> None:
    item = valid_r16()
    item[field] = value
    with pytest.raises(RuntimeError):
        validate_r16_report(item)
```

## `tests/test_public.py`

```python
"""Production public route test: map display without proof fabrication."""
from __future__ import annotations

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective, MapIsomorphism, MapSurjective
from phase174_r3_r7_r17_typed_map_open_goal.audit import inspect_public_map_display
from web_group_proof_common import _group_proof_statement_latex


def test_generic_typed_map_property_displays_do_not_choose_a_stem() -> None:
    for top, lower, sphere in ((13, 11, 6), (15, 13, 7)):
        mapping = TodaDeltaMap(TodaPrimaryGroup(top, top), TodaPrimaryGroup(lower, sphere))
        source = rf"\pi_{{{top}}}^{{{top}}}"
        target = rf"\pi_{{{lower}}}^{{{sphere}}}"
        assert _group_proof_statement_latex(MapSurjective(mapping)) == (
            rf"\Delta: {source} \twoheadrightarrow {target}", None,
        )
        assert _group_proof_statement_latex(MapInjective(mapping)) == (
            rf"\Delta: {source} \hookrightarrow {target}", None,
        )
        assert _group_proof_statement_latex(MapIsomorphism(mapping)) == (
            rf"\Delta: {source} \xrightarrow{{\cong}} {target}", None,
        )


def test_public_r16_search_still_open_and_map_math_visible() -> None:
    status = inspect_public_map_display()
    assert status["public_root_candidates"] == 1
    assert status["public_delta_surjectivity_candidates"] == 0
    assert status["generic_isomorphism_depends_on_surjectivity"] is True
    assert status["direct_given_for_goal_or_delta"] is False
    assert status["search_status"] != "complete"
    assert status["math_rule_changes"] == 0
    assert status["completion_claimed"] is False
    assert "MapSurjective" in status["open_goal_types"]
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$PatchAttempted = $false
$Backup = Join-Path $env:LOCALAPPDATA 'EHPProofTracerAudit\phase174_r3_r7_r17\web_group_proof_common.original.py'
$Target = Join-Path $RepoRoot 'web_group_proof_common.py'

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Fetch, but never pull/reset/stash/checkout user files.
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "R17 Git fetch failed: $LASTEXITCODE" }

    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R17 source guard/preflight failed: $LASTEXITCODE" }
    & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R17 formatting patch dry-run failed: $LASTEXITCODE" }

    $Groups = @(
        @{ Name = 'R17_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_patch.py',
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_audit.py'
        ) },
        @{ Name = 'R16_ROOT'; Paths = @(
            '.\phase174_r3_r7_r16_public_ehp_zero_root\tests\test_public.py'
        ) },
        @{ Name = 'R3_EHP_RULE'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py'
        ) },
        @{ Name = 'PHASE173_TYPED_DISPLAY'; Paths = @(
            '.\phase173_r4_r15r17r3r3_typed_goal_display\tests\test_open_goals.py'
        ) }
    )
    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "R17 missing focused test: $TestPath"
            }
        }
        Write-Output "PHASE174_R3R7R17_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "R17 focused test failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R17_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R17_GATE=PASS_PREFLIGHT'
    }
    else {
        $PatchAttempted = $true
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.patch
        if ($LASTEXITCODE -ne 0) { throw 'R17 guarded formatting patch failed' }
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r17_typed_map_open_goal\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R17 public typed-map display regression failed' }
        & python -B -m phase174_r3_r7_r17_typed_map_open_goal.audit
        if ($LASTEXITCODE -ne 0) { throw 'R17 public typed-map audit failed' }
    }
    Write-Output '(END)'
}
catch {
    if ($PatchAttempted -and (Test-Path -LiteralPath $Backup)) {
        $Modified = @(git diff --name-only)
        if ($Modified -contains 'web_group_proof_common.py') {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Output 'PHASE174_R3R7R17_ROLLBACK=COMMON_RENDERER_RESTORED'
        }
    }
    throw
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
```
