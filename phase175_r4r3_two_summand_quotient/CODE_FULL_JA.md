# Phase 175 R4R3R2 — 実装・テストのコード全文

## 今回の変更対象（最初に列挙）

- `phase175_r4r3_two_summand_quotient/audit.py`：`phase175_r4_pi95_audit.audit` の import を完全列挙して更新（`git` と `preflight`）。定数 `REVIEWED_R4_REPORT_HEAD`、`REVIEWED_R4_COMMIT`、`REVIEWED_R4_COMMIT_CHANGES` を `FINAL_GATE` の直後に新規追加。`validate_r4_report()` の直前に `validate_r4_lineage()` を新規追加。`run()` を関数全文で置き換え。
- `phase175_r4r3_two_summand_quotient/tests/test_audit.py`：ファイル末尾に7個の新規テスト関数と `reviewed_git_result()` helper を追加。import 変更なし。テスト関数はすべて全文記載。
- `phase175_r4r3_two_summand_quotient/README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、本書（日本語）：ファイル全文更新。
- `rule.py`、`tests/test_rule.py`、`run.ps1`、`__init__.py` は**変更なし**。今回クラス追加・変更なし。本番 Proof Search と共通 Renderer も変更なし。

以下は ZIP 内の同名コードファイルと一字一句同じ内容。`...` によるコード省略は行わず、import を含む完全なファイルを掲載する。既存の `validate_r4_report()` は変更していないが、全体コードにも含める。

## `audit.py`（全文）

```python
"""Phase 175 R4R3: review an isolated generic EHP two-summand quotient rule.

The previous R4 observation must exist and remain unchanged. Nothing in this
module edits production code, creates GIVENs, or runs the whole test suite.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4_pi95_audit.audit import git, preflight
from phase175_r4r3_two_summand_quotient.rule import RULE_NAME


PACKAGE = "phase175_r4r3_two_summand_quotient"
REVIEWED_R4_GATE = "PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE"
R4_REPORT_FOLDER = "phase175_r4_pi95_audit"
DRY_GATE = "PASS_R4R3_ISOLATED_RULE_DRYRUN"
FINAL_GATE = "PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC"
REVIEWED_R4_REPORT_HEAD = "c77a26fdebe0eead67f1f7dad3a469aa446b134f"
REVIEWED_R4_COMMIT = "20622a303b8c4558fe297eed070b43ca2f322831"
REVIEWED_R4_COMMIT_CHANGES = {
    ".pytest_cache/v/cache/nodeids": "M",
    "phase175_r4_pi95_audit/AUDIT_PLAN_JA.md": "A",
    "phase175_r4_pi95_audit/CODE_FULL_JA.md": "A",
    "phase175_r4_pi95_audit/README.md": "A",
    "phase175_r4_pi95_audit/TEST_RESULTS_JA.md": "A",
    "phase175_r4_pi95_audit/__init__.py": "A",
    "phase175_r4_pi95_audit/audit.py": "A",
    "phase175_r4_pi95_audit/run.ps1": "A",
    "phase175_r4_pi95_audit/tests/test_audit.py": "A",
}


def r4_report_path(explicit: Path | None = None) -> Path:
    """Choose the last successful full R4 observation, never a DryRun."""
    if explicit is not None:
        path = explicit.resolve()
        if not path.is_file():
            raise RuntimeError("R4R3_R4_REPORT_NOT_FOUND: " + str(path))
        return path
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    report_root = root / "EHPProofTracerAudit" / R4_REPORT_FOLDER
    choices = sorted(report_root.glob("*/report.json"), reverse=True)
    for path in choices:
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if result.get("gate") == REVIEWED_R4_GATE:
            return path
    raise RuntimeError("R4R3_NO_PASSED_R4_REAL_REPORT")


def validate_r4_lineage(root: Path, report_head: object, current_head: object) -> dict[str, object]:
    """Accept only an unchanged HEAD or the exact reviewed R4 audit commit.

    The R4 real report was recorded just before its audit-only package was
    committed. The reviewed commit adds no mathematical/production sources;
    its only changed pre-existing file is pytest's nodeids cache. Do not
    accept an arbitrary descendant or a change to the R4 audit after that
    commit. Actual Git objects, parentage and file statuses are checked.
    """
    if not isinstance(report_head, str) or not isinstance(current_head, str):
        raise RuntimeError("R4R3_R4_HEAD_OR_PINS_CHANGED")
    if report_head == current_head:
        return {
            "report_head": report_head,
            "current_head": current_head,
            "status": "SAME_HEAD",
            "reviewed_changes": [],
        }
    if (report_head, current_head) != (
        REVIEWED_R4_REPORT_HEAD, REVIEWED_R4_COMMIT,
    ):
        raise RuntimeError("R4R3_R4_UNREVIEWED_HEAD_TRANSITION")
    _, actual_head = git(root, "rev-parse", "HEAD")
    if actual_head != current_head:
        raise RuntimeError("R4R3_R4_CURRENT_HEAD_MISMATCH")
    _, actual_parent = git(root, "rev-parse", current_head + "^1")
    if actual_parent != report_head:
        raise RuntimeError("R4R3_R4_UNREVIEWED_PARENT")
    _, changed = git(
        root, "diff", "--name-status", "--no-renames",
        report_head, current_head,
    )
    actual_changes: dict[str, str] = {}
    for line in changed.splitlines():
        fields = line.split("\t")
        if len(fields) != 2 or fields[0] not in {"A", "M"}:
            raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
        status, path = fields
        if path in actual_changes:
            raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
        actual_changes[path] = status
    if actual_changes != REVIEWED_R4_COMMIT_CHANGES:
        raise RuntimeError("R4R3_R4_UNREVIEWED_COMMIT_DIFF")
    return {
        "report_head": report_head,
        "current_head": current_head,
        "status": "REVIEWED_R4_AUDIT_ONLY_COMMIT",
        "reviewed_changes": sorted(actual_changes),
    }


def validate_r4_report(report: object, current_head: str) -> dict[str, object]:
    """Never infer target proof or trust from an unchecked prior report."""
    if not isinstance(report, dict):
        raise RuntimeError("R4R3_REPORT_NOT_OBJECT")
    if (report.get("phase") != "175-R4"
            or report.get("mode") != "READ_ONLY_AUDIT"
            or report.get("dry_run") is not False
            or report.get("gate") != REVIEWED_R4_GATE
            or report.get("new_given") != 0
            or report.get("new_mathematical_rules") != 0
            or report.get("full_pytest_executed") is not False
            or report.get("production_changes") != []):
        raise RuntimeError("R4R3_R4_GATE_OR_POLICY_MISMATCH")

    r4_preflight = report.get("preflight")
    if (not isinstance(r4_preflight, dict)
            or r4_preflight.get("head") != current_head
            or r4_preflight.get("pinned_source_count") != 18):
        raise RuntimeError("R4R3_R4_HEAD_OR_PINS_CHANGED")

    observed = report.get("observations")
    rows = report.get("actual_rows")
    source = report.get("source")
    if (not isinstance(observed, dict)
            or observed.get("target_group") != "pi_9^5"
            or observed.get("prior_group") != "pi_8^4"
            or observed.get("open_goals_count") != 3
            or observed.get("target_status") != "INCOMPLETE_AND_WEB_CONFIRMED"
            or observed.get("prior_status") != "COMPLETE_AND_WEB_VERIFIED"
            or observed.get("proof_complete") is not False
            or not isinstance(observed.get("open_goals"), list)
            or len(observed["open_goals"]) != 3
            or not isinstance(rows, dict)
            or not isinstance(rows.get("target"), dict)
            or rows["target"].get("search_proven_count") != 0
            or not isinstance(rows.get("prior_pi84"), dict)
            or rows["prior_pi84"].get("trust_verified") is not True
            or not isinstance(source, dict)
            or source.get("prior_pi84_printed") is not True
            or source.get("source_proposition25") is not True
            or source.get("source_ehp_delta_eta9") is not True
            or source.get("source_ehp_delta_iota9") is not True
            or source.get("source_pi95_quotient") is not True
            or source.get("source_is_derived_goal_proof") is not False):
        raise RuntimeError("R4R3_R4_OPEN_GOAL_OR_SOURCE_EVIDENCE_CHANGED")

    return {
        "target_group": observed["target_group"],
        "prior_group": observed["prior_group"],
        "open_goals_count": observed["open_goals_count"],
        "target_proven_steps": rows["target"]["search_proven_count"],
        "prior_verified": rows["prior_pi84"]["trust_verified"],
        "source_prop25_seen": source["source_proposition25"],
        "proof_complete": False,
    }


def make_report_path() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    path = root / "EHPProofTracerAudit" / PACKAGE / stamp
    path.mkdir(parents=True, exist_ok=False)
    return path


def run(root: Path, dry_run: bool, r4_report: Path | None = None) -> int:
    output = make_report_path()
    result: dict[str, object] = {
        "phase": "175-R4R3",
        "mode": "ISOLATED_GENERIC_INFERENCE",
        "gate": "FAIL_R4R3_ISOLATED_RULE",
        "dry_run": dry_run,
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 1,
        "rule_connected_to_public": False,
        "complete_proof": False,
        "full_pytest_executed": False,
    }
    try:
        examined = preflight(root)
        result["preflight"] = examined
        report_file = r4_report_path(r4_report)
        loaded = json.loads(report_file.read_text(encoding="utf-8"))
        result["r4_report"] = str(report_file)
        r4_preflight = loaded.get("preflight") if isinstance(loaded, dict) else None
        r4_head = r4_preflight.get("head") if isinstance(r4_preflight, dict) else None
        lineage = validate_r4_lineage(root, r4_head, examined["head"])
        result["r4_lineage"] = lineage
        result["r4_observation"] = validate_r4_report(loaded, lineage["report_head"])
        result["mathematical_rule"] = RULE_NAME
        result["unproven_public_premises"] = [
            "verified pi_8^4 direct-sum presentation in the search context",
            "proved pi_10^9 = (Z/2){eta_9} presentation",
            "inferred Delta(eta_9) is a chosen pi_8^4 summand generator",
            "inferred Proposition 4.2 Delta-to-E exactness window",
            "inferred E:pi_8^4 -> pi_9^5 surjective",
            "inferred E(nu_4 eta_7) = nu_5 eta_8",
        ]
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["traceback"] = traceback.format_exc()[-4000:]

    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    report_md = "\n".join([
        "# Phase 175 R4R3 — 一般商群推論の隔離監査", "",
        "Gate: `" + str(result["gate"]) + "`", "",
        "新規 GIVEN: 0。新規一般推論規則: 1。", "",
        "対象群の完成証明・公開 Proof Tree・Narrative は変更しない。", "",
        "R4 report: `" + str(result.get("r4_report", "UNVERIFIED")) + "`", "",
        "## 必要な証明義務", "",
        *["- " + x for x in result.get("unproven_public_premises", [])],
        "", "次段階で、実際に検証された前提と出典を公開 Provider へ接続する。", "",
    ])
    (output / "report.md").write_text(report_md, encoding="utf-8")
    print("PHASE175_R4R3_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R3_PINNED_SOURCES=" + str(result.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4R3_NEW_GIVEN=0")
    print("PHASE175_R4R3_NEW_GENERAL_RULES=1")
    print("PHASE175_R4R3_PUBLIC_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R3_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R3_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R3_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R3_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4-report", type=Path, default=None)
    options = parser.parse_args(argv)
    return run(options.root.resolve(), options.dry_run, options.r4_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_audit.py`（全文）

```python
"""Isolated R4 observation-policy tests; fixtures are intentionally synthetic."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase175_r4r3_two_summand_quotient import audit


HEAD = "synthetic-verified-head"


def fixture_r4():
    return {
        "phase": "175-R4",
        "mode": "READ_ONLY_AUDIT",
        "gate": audit.REVIEWED_R4_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest_executed": False,
        "production_changes": [],
        "preflight": {"head": HEAD, "pinned_source_count": 18},
        "observations": {
            "target_group": "pi_9^5",
            "prior_group": "pi_8^4",
            "open_goals_count": 3,
            "open_goals": ["CyclicStructureStatement(goal)", "Relation(a,b)", "Relation(b,a)"],
            "target_status": "INCOMPLETE_AND_WEB_CONFIRMED",
            "prior_status": "COMPLETE_AND_WEB_VERIFIED",
            "proof_complete": False,
        },
        "actual_rows": {
            "target": {"search_proven_count": 0},
            "prior_pi84": {"trust_verified": True},
        },
        "source": {
            "prior_pi84_printed": True,
            "source_proposition25": True,
            "source_ehp_delta_eta9": True,
            "source_ehp_delta_iota9": True,
            "source_pi95_quotient": True,
            "source_is_derived_goal_proof": False,
        },
    }


def test_passed_real_r4_report_is_still_unfinished() -> None:
    result = audit.validate_r4_report(fixture_r4(), HEAD)
    assert result == {
        "target_group": "pi_9^5",
        "prior_group": "pi_8^4",
        "open_goals_count": 3,
        "target_proven_steps": 0,
        "prior_verified": True,
        "source_prop25_seen": True,
        "proof_complete": False,
    }


@pytest.mark.parametrize("field,value", [
    ("phase", "175-R3"),
    ("mode", "PUBLIC_PROOF"),
    ("gate", "PASS_R4_AUDIT_ONLY_DRYRUN"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("full_pytest_executed", True),
    ("production_changes", ["phase165_r52_r9_shared_math.py"]),
])
def test_rejects_wrong_r4_policy(field: str, value: object) -> None:
    data = fixture_r4()
    data[field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_GATE_OR_POLICY_MISMATCH"):
        audit.validate_r4_report(data, HEAD)


@pytest.mark.parametrize("field,value", [
    ("head", "different-commit"),
    ("pinned_source_count", 17),
])
def test_rejects_r4_head_or_pins(field: str, value: object) -> None:
    data = fixture_r4()
    data["preflight"][field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_HEAD_OR_PINS_CHANGED"):
        audit.validate_r4_report(data, HEAD)


@pytest.mark.parametrize("section,field,value", [
    ("observations", "open_goals_count", 2),
    ("observations", "proof_complete", True),
    ("observations", "target_status", "COMPLETE_AND_WEB_VERIFIED"),
    ("observations", "prior_status", "INCOMPLETE_AND_WEB_CONFIRMED"),
    ("actual_rows.target", "search_proven_count", 1),
    ("actual_rows.prior_pi84", "trust_verified", False),
    ("source", "source_pi95_quotient", False),
    ("source", "source_is_derived_goal_proof", True),
])
def test_rejects_changed_mathematical_observation(
    section: str, field: str, value: object,
) -> None:
    data = deepcopy(fixture_r4())
    node = data
    for part in section.split("."):
        node = node[part]
    node[field] = value
    with pytest.raises(RuntimeError, match="R4R3_R4_OPEN_GOAL_OR_SOURCE_EVIDENCE_CHANGED"):
        audit.validate_r4_report(data, HEAD)


def test_latest_passed_r4_report_is_chosen(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    root = tmp_path / "EHPProofTracerAudit" / audit.R4_REPORT_FOLDER
    oldest = root / "20261117T020000Z"
    newest = root / "20261117T040000Z"
    oldest.mkdir(parents=True)
    newest.mkdir(parents=True)
    (oldest / "report.json").write_text(json.dumps(fixture_r4()), encoding="utf-8")
    failed = deepcopy(fixture_r4())
    failed["gate"] = "FAIL_R4_AUDIT_NOT_COMPLETED"
    (newest / "report.json").write_text(json.dumps(failed), encoding="utf-8")
    assert audit.r4_report_path() == oldest / "report.json"


def test_no_successful_r4_report_is_rejected(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    with pytest.raises(RuntimeError, match="R4R3_NO_PASSED_R4_REAL_REPORT"):
        audit.r4_report_path()


def test_explicit_report_path_is_not_silently_replaced(tmp_path: Path) -> None:
    expected = tmp_path / "report.json"
    expected.write_text(json.dumps(fixture_r4()), encoding="utf-8")
    assert audit.r4_report_path(expected) == expected.resolve()
    with pytest.raises(RuntimeError, match="R4R3_R4_REPORT_NOT_FOUND"):
        audit.r4_report_path(tmp_path / "missing.json")


def test_r4_same_head_lineage_needs_no_exception(monkeypatch, tmp_path: Path) -> None:
    def reject_git_calls(root, *args):
        raise AssertionError("same-HEAD report does not need Git transition")

    monkeypatch.setattr(audit, "git", reject_git_calls)
    found = audit.validate_r4_lineage(tmp_path, HEAD, HEAD)
    assert found["status"] == "SAME_HEAD"
    assert found["report_head"] == HEAD
    assert found["reviewed_changes"] == []


def reviewed_git_result(root: Path, *args: str) -> tuple[int, str]:
    if args == ("rev-parse", "HEAD"):
        return 0, audit.REVIEWED_R4_COMMIT
    if args == ("rev-parse", audit.REVIEWED_R4_COMMIT + "^1"):
        return 0, audit.REVIEWED_R4_REPORT_HEAD
    if args == (
        "diff", "--name-status", "--no-renames",
        audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
    ):
        return 0, "\n".join(
            "\t".join((status, path))
            for path, status in audit.REVIEWED_R4_COMMIT_CHANGES.items()
        )
    raise AssertionError(f"unexpected Git command: {args!r}")


def test_r4_reviewed_one_commit_is_accepted(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    found = audit.validate_r4_lineage(
        tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
    )
    assert found["status"] == "REVIEWED_R4_AUDIT_ONLY_COMMIT"
    assert found["current_head"] == audit.REVIEWED_R4_COMMIT
    assert len(found["reviewed_changes"]) == 9
    sample = fixture_r4()
    sample["preflight"]["head"] = found["report_head"]
    assert audit.validate_r4_report(sample, found["report_head"])["proof_complete"] is False


@pytest.mark.parametrize("reported,current", [
    ("unreviewed-report", audit.REVIEWED_R4_COMMIT),
    (audit.REVIEWED_R4_REPORT_HEAD, "unreviewed-next-commit"),
    (audit.REVIEWED_R4_COMMIT, audit.REVIEWED_R4_REPORT_HEAD),
])
def test_r4_unreviewed_head_transitions_are_rejected(
    monkeypatch, tmp_path: Path, reported: str, current: str,
) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD_TRANSITION"):
        audit.validate_r4_lineage(tmp_path, reported, current)


def test_r4_commit_with_wrong_parent_is_rejected(monkeypatch, tmp_path: Path) -> None:
    def wrong_parent(root, *args):
        if args == ("rev-parse", audit.REVIEWED_R4_COMMIT + "^1"):
            return 0, "different-parent"
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", wrong_parent)
    with pytest.raises(RuntimeError, match="UNREVIEWED_PARENT"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


def test_r4_commit_with_wrong_live_head_is_rejected(monkeypatch, tmp_path: Path) -> None:
    def wrong_head(root, *args):
        if args == ("rev-parse", "HEAD"):
            return 0, "different-head"
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", wrong_head)
    with pytest.raises(RuntimeError, match="CURRENT_HEAD_MISMATCH"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


@pytest.mark.parametrize("changed", [
    {"phase165_r52_r9_shared_math.py": "M"},
    {"phase175_r4_pi95_audit/audit.py": "M"},
    {"phase175_r4_pi95_audit/README.md": "D"},
    {"phase175_r4_pi95_audit/audit.py": "A", "extra.py": "A"},
    {},
])
def test_r4_commit_with_unreviewed_diff_is_rejected(
    monkeypatch, tmp_path: Path, changed: dict[str, str],
) -> None:
    def altered_diff(root, *args):
        if args and args[0] == "diff":
            return 0, "\n".join(f"{status}\t{path}" for path, status in changed.items())
        return reviewed_git_result(root, *args)

    monkeypatch.setattr(audit, "git", altered_diff)
    with pytest.raises(RuntimeError, match="UNREVIEWED_COMMIT_DIFF"):
        audit.validate_r4_lineage(
            tmp_path, audit.REVIEWED_R4_REPORT_HEAD, audit.REVIEWED_R4_COMMIT,
        )


def test_r4_lineage_rejects_missing_head(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", reviewed_git_result)
    with pytest.raises(RuntimeError, match="HEAD_OR_PINS_CHANGED"):
        audit.validate_r4_lineage(tmp_path, None, audit.REVIEWED_R4_COMMIT)
```

## `rule.py`（全文）

```python
"""General EHP quotient rule for an elementary rank-two 2-group.

A = (Z/2){a} + (Z/2){b}, C = (Z/2){z},
C --Delta--> A --E--> B is exact, E onto, Delta(z) is one
of a,b, and E(the other) = y. Then B = (Z/2){y}.

The rule consumes only explicit typed proof goals. It registers no literature
claims, never treats a printed target theorem as a proof, and has no special
sphere-dimension branches. It is NOT wired to public search in R4R3.
"""
from __future__ import annotations

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import (
    InferenceRule,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact rank-two elementary 2-group quotient by a generated summand"


def two_summand_quotient_inputs(
    goal: object,
    domain_relation: object,
    delta_source_relation: object,
    delta_image: object,
    suspension_image: object,
) -> tuple[object, ...] | None:
    """Check all source, target, generator and consecutive-EHP map types.

    No input is trusted merely because it is constructed as a statement.
    The returned six statements must each be independently proved before the
    inference may be applied. The selected surviving summand is not assumed.
    """
    if (type(goal) is not CyclicStructureStatement
            or type(goal.group) is not TodaPrimaryGroup
            or goal.order != 2
            or type(domain_relation) is not Relation
            or domain_relation.relation_type is not RelationType.EQUALITY
            or type(domain_relation.lhs) is not TodaPrimaryGroup
            or type(domain_relation.rhs) is not DirectSumGroup
            or type(delta_source_relation) is not Relation
            or delta_source_relation.relation_type is not RelationType.EQUALITY
            or type(delta_source_relation.lhs) is not TodaPrimaryGroup
            or type(delta_source_relation.rhs) is not FiniteCyclicGroup
            or delta_source_relation.rhs.order != 2
            or type(delta_image) is not GeneratorImage
            or type(suspension_image) is not GeneratorImage):
        return None

    parts = domain_relation.rhs.summands
    if (type(parts) is not tuple
            or len(parts) != 2
            or any(type(x) is not FiniteCyclicGroup or x.order != 2 for x in parts)):
        return None

    first = parts[0].generator
    second = parts[1].generator
    if first == second:
        return None

    source = delta_source_relation.lhs
    middle = domain_relation.lhs
    target = goal.group
    delta = TodaDeltaMap(source, middle)
    suspension = TodaSuspensionMap(middle, target)
    if (delta_image.map != delta
            or suspension_image.map != suspension
            or delta_image.source_generator != delta_source_relation.rhs.generator
            or suspension_image.target_generator != goal.generator):
        return None

    killed = delta_image.target_generator
    survivor = suspension_image.source_generator
    if not ((killed == first and survivor == second)
            or (killed == second and survivor == first)):
        return None

    # An expression's printed name alone does not type it as a generator.
    if (_endpoints(first) != (middle.group_dimension, middle.sphere_dimension)
            or _endpoints(second) != (middle.group_dimension, middle.sphere_dimension)
            or _endpoints(delta_image.source_generator)
            != (source.group_dimension, source.sphere_dimension)
            or _endpoints(goal.generator)
            != (target.group_dimension, target.sphere_dimension)):
        return None

    exactness = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=source,
        middle_term=middle,
        target_term=target,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(exactness) is None:
        return None

    return (
        domain_relation,
        delta_source_relation,
        delta_image,
        exactness,
        MapSurjective(suspension),
        suspension_image,
    )


def two_summand_quotient_rule(
    goal: CyclicStructureStatement,
    domain_relation: Relation,
    delta_source_relation: Relation,
    delta_image: GeneratorImage,
    suspension_image: GeneratorImage,
) -> InferenceRule:
    """Apply the quotient only after all six exact premises are proved.

    Earlier group relations may be admitted prior results; the four map and
    exactness facts must be INFERENCE ProofSteps. Provenance/trust for prior
    relations is checked separately by the existing proof-search boundary.
    """
    required = two_summand_quotient_inputs(
        goal, domain_relation, delta_source_relation, delta_image, suspension_image,
    )
    if required is None:
        raise ValueError("not a typed rank-two EHP quotient goal")

    def guard(premises, bindings):
        return (
            len(premises) == 6
            and tuple(step.conclusion for step in premises) == required
            and all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
                    for step in premises[:2])
            and all(step.rule is ProofRule.INFERENCE for step in premises[2:])
            and two_summand_quotient_inputs(
                goal, domain_relation, delta_source_relation, delta_image,
                suspension_image,
            ) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "If Delta from a proved order-two cyclic group maps its generator "
            "to one direct-sum generator of a proved (Z/2)^2, EHP exactness "
            "identifies the E-kernel with that summand. With independently "
            "proved E surjective and E of the other generator equal to y, "
            "the target is (Z/2){y}."
        ),
        premise_patterns=tuple(
            PremisePattern(
                statement_type=type(statement),
                statement_pattern=statement,
                relation_type=RelationType.EQUALITY
                if isinstance(statement, Relation) else None,
            )
            for statement in required
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_two_summand_quotient(
    goal: object,
    domain_relation: object,
    delta_source_relation: object,
    delta_image: object,
    suspension_image: object,
) -> tuple[GoalExpansion, ...]:
    """Isolated backward proposal: no proof leaf or production registration."""
    required = two_summand_quotient_inputs(
        goal, domain_relation, delta_source_relation, delta_image, suspension_image,
    )
    if required is None:
        return ()
    return (GoalExpansion(
        two_summand_quotient_rule(
            goal, domain_relation, delta_source_relation,
            delta_image, suspension_image,
        ),
        required,
    ),)
```

## `tests/test_rule.py`（全文）

```python
"""Isolated algebraic inference contracts; every fixture premise is synthetic.

Only the actual ProofStep matcher may infer the root. These test fixtures are
not registered references and are not a proof of pi_9^5 in production.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from phase165_r14_r6_generic_iso import GeneratorImage
from phase175_r4r3_two_summand_quotient.rule import (
    RULE_NAME, expand_two_summand_quotient,
    two_summand_quotient_inputs, two_summand_quotient_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def fixture():
    """Typed pi8^4/pi9^5 example, with no asserted source truth."""
    a_group = TodaPrimaryGroup(8, 4)
    c_group = TodaPrimaryGroup(10, 9)
    b_group = TodaPrimaryGroup(9, 5)
    nu4 = HomotopyElement(
        "ν₄", 4, source=7, target=4,
        generator=GeneratorSymbol("ν", 4),
    )
    nuprime_e = HomotopyElement(
        "Eν′", 4, source=7, target=4,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    eta7 = HomotopyElement(
        "η₇", 7, source=8, target=7,
        generator=GeneratorSymbol("η", 7),
    )
    nu5 = HomotopyElement(
        "ν₅", 5, source=8, target=5,
        generator=GeneratorSymbol("ν", 5),
    )
    eta8 = HomotopyElement(
        "η₈", 8, source=9, target=8,
        generator=GeneratorSymbol("η", 8),
    )
    eta9 = HomotopyElement(
        "η₉", 9, source=10, target=9,
        generator=GeneratorSymbol("η", 9),
    )
    a = Composition(nu4, eta7)
    killed = Composition(nuprime_e, eta7)
    y = Composition(nu5, eta8)
    source = Relation(
        a_group,
        DirectSumGroup((FiniteCyclicGroup(2, a), FiniteCyclicGroup(2, killed))),
        RelationType.EQUALITY,
    )
    delta_source = Relation(
        c_group, FiniteCyclicGroup(2, eta9), RelationType.EQUALITY,
    )
    delta = GeneratorImage(TodaDeltaMap(c_group, a_group), eta9, killed)
    suspension = GeneratorImage(TodaSuspensionMap(a_group, b_group), a, y)
    goal = CyclicStructureStatement(b_group, y, 2)
    return goal, source, delta_source, delta, suspension


def synthetic(value: object, kind: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(
        value, (), kind,
        inference_rule=InferenceRule("synthetic fixture only: not a cited proof"),
    )


def inferred_parent_steps():
    values = two_summand_quotient_inputs(*fixture())
    assert values is not None
    return tuple(synthetic(value) for value in values)


def test_proved_six_premise_rule_and_group_relation() -> None:
    goal, prior, source, delta, suspension = fixture()
    required = two_summand_quotient_inputs(goal, prior, source, delta, suspension)
    assert required is not None and len(required) == 6
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    assert rule.name == RULE_NAME
    parents = inferred_parent_steps()
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    cyclic = apply_inference_match(matches[0])
    assert cyclic.rule is ProofRule.INFERENCE
    assert cyclic.conclusion == goal
    assert cyclic.premises == parents
    bridge = finite_cyclic_structure_as_relation_inference_rule()
    relations = find_inference_matches_for_rule(bridge, (cyclic,))
    assert len(relations) == 1
    final = apply_inference_match(relations[0])
    assert final.conclusion == Relation(
        goal.group, FiniteCyclicGroup(2, goal.generator), RelationType.EQUALITY,
    )
    assert final.premises == (cyclic,)


def test_exposure_is_only_a_backward_proposal() -> None:
    goal, prior, source, delta, suspension = fixture()
    results = expand_two_summand_quotient(goal, prior, source, delta, suspension)
    assert len(results) == 1
    assert results[0].subgoals == two_summand_quotient_inputs(*fixture())
    assert all(not isinstance(item, ProofStep) for item in results[0].subgoals)


@pytest.mark.parametrize("index", range(6))
def test_missing_any_one_proof_rejects_conclusion(index: int) -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = inferred_parent_steps()
    absent = parents[:index] + parents[index + 1:]
    assert not find_inference_matches_for_rule(rule, absent)


@pytest.mark.parametrize("index", (2, 3, 4, 5))
def test_cannot_substitute_a_given_for_derived_map_or_exactness(index: int) -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = list(inferred_parent_steps())
    parents[index] = synthetic(parents[index].conclusion, ProofRule.GIVEN)
    assert not find_inference_matches_for_rule(rule, tuple(parents))


def test_prior_relations_can_be_previous_admitted_results() -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = list(inferred_parent_steps())
    parents[0] = synthetic(prior, ProofRule.GIVEN)
    parents[1] = synthetic(source, ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, tuple(parents))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal


@pytest.mark.parametrize("where", ("prior", "source", "delta", "suspension", "goal"))
def test_rejects_wrong_group_dimensions(where: str) -> None:
    goal, prior, source, delta, suspension = fixture()
    if where == "prior":
        prior = replace(prior, lhs=TodaPrimaryGroup(8, 5))
    elif where == "source":
        source = replace(source, lhs=TodaPrimaryGroup(10, 10))
    elif where == "delta":
        delta = replace(delta, map=TodaDeltaMap(source.lhs, goal.group))
    elif where == "suspension":
        suspension = replace(
            suspension, map=TodaSuspensionMap(source.lhs, goal.group),
        )
    else:
        goal = replace(goal, group=TodaPrimaryGroup(10, 6))
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None
    assert not expand_two_summand_quotient(goal, prior, source, delta, suspension)


@pytest.mark.parametrize("where", ("prior", "source", "goal"))
def test_rejects_wrong_order(where: str) -> None:
    goal, prior, source, delta, suspension = fixture()
    if where == "prior":
        original = prior.rhs.summands
        prior = replace(prior, rhs=DirectSumGroup(
            (FiniteCyclicGroup(4, original[0].generator), original[1]),
        ))
    elif where == "source":
        source = replace(source, rhs=FiniteCyclicGroup(4, source.rhs.generator))
    else:
        goal = replace(goal, order=4)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_same_killed_and_surviving_summand() -> None:
    goal, prior, source, delta, suspension = fixture()
    suspension = replace(suspension, source_generator=delta.target_generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_non_independent_basis_generators() -> None:
    goal, prior, source, delta, suspension = fixture()
    a = prior.rhs.summands[0]
    prior = replace(prior, rhs=DirectSumGroup((a, a)))
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_wrong_delta_image_or_generator() -> None:
    goal, prior, source, delta, suspension = fixture()
    delta = replace(delta, target_generator=goal.generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None
    goal, prior, source, delta, suspension = fixture()
    suspension = replace(suspension, target_generator=delta.target_generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_fake_generator_types_with_only_matching_names() -> None:
    goal, prior, source, delta, suspension = fixture()
    malformed = HomotopyElement(
        "ν₅η₈", 5, source=9, target=4,
        generator=GeneratorSymbol("faked-name"),
    )
    bad = replace(goal, generator=malformed)
    image = replace(suspension, target_generator=malformed)
    assert two_summand_quotient_inputs(bad, prior, source, delta, image) is None


def test_no_assumed_target_as_premise() -> None:
    goal, prior, source, delta, suspension = fixture()
    values = two_summand_quotient_inputs(goal, prior, source, delta, suspension)
    assert values is not None
    assert all(statement != goal for statement in values)
    assert all(statement != Relation(
        goal.group, FiniteCyclicGroup(2, goal.generator), RelationType.EQUALITY,
    ) for statement in values)
```

## `run.ps1`（全文）

```powershell
param(
    [switch] $DryRun,
    [string] $R4Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        phase175_r4r3_two_summand_quotient/tests/test_rule.py `
        phase175_r4r3_two_summand_quotient/tests/test_audit.py `
        phase175_r4_pi95_audit/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R4R3 focused pytest failed' }
    Write-Output 'PHASE175_R4R3_FOCUSED_PYTEST=PASS'

    $cmd = @('-B', '-m', 'phase175_r4r3_two_summand_quotient.audit', '--root', $root)
    if ($DryRun) { $cmd += '--dry-run' }
    if ($R4Report -ne '') { $cmd += @('--r4-report', $R4Report) }
    & python @cmd
    $auditExitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R3_EXIT_CODE=$auditExitCode"
    if ($auditExitCode -ne 0) { exit $auditExitCode }
    exit 0
} finally {
    Pop-Location
}
```

## `__init__.py`（全文）

```python
"""Phase 175 R4R3: isolated typed rank-two EHP quotient inference."""
```

