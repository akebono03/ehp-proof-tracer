# Phase 175 R4R4 — 実装・テストコード全文

## 対象ファイル、クラス、関数

- `phase175_r4r4_pi95_premise_frontier/audit.py`：`latest_prior_report()`、`validate_prior_report()`、`validate_prior_lineage()`、`verify_code_and_source_pins()`、`read_printed_source_evidence()`、`verify_ehp_shape()`、`premise_frontier()`、`report_folder()`、`run()`、`main()` をすべて新規ファイル内に追加。
- `phase175_r4r4_pi95_premise_frontier/tests/test_audit.py`：全テスト関数とテスト用補助関数を新規追加。
- `phase175_r4r4_pi95_premise_frontier/run.ps1`：DryRun／本実行のスクリプトを新規追加。
- `phase175_r4r4_pi95_premise_frontier/__init__.py`：新規パッケージ初期化。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、本書（日本語）：新規全文。

**既存ファイル・import・クラス・関数は一切変更しない。** 以下にすべての新規 import、関数、テストおよび実行コードを、そのまま置き換えられるファイル全体として掲載する。コードの省略なし。

## `audit.py` 全文

```python
"""Phase 175 R4R4: source-first inventory of the six pi_9^5 quotient premises.

This is an audit, not a proof provider. A cited equation, a well-typed
statement and an actual verified ProofStep remain distinct categories.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4_pi95_audit.audit import git, preflight


PACKAGE = "phase175_r4r4_pi95_premise_frontier"
PRIOR_PACKAGE = "phase175_r4r3_two_summand_quotient"
PRIOR_GATE = "PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC"
REVIEWED_RULE_SHA256 = "eea4a60ba01df182ceea475cdbd97d03cc783548981e9766856ffc889c4f087f"
EXPECTED_HEAD_AT_PRIOR_AUDIT = "20622a303b8c4558fe297eed070b43ca2f322831"
DRY_GATE = "PASS_R4R4_PREMISE_FRONTIER_DRYRUN"
FINAL_GATE = "PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC"
EXTRA_SOURCE_PINS = {
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase171_r2j_r3_ehp_exactness/source.py": "f87ce6dc8278661a56bc0024c3a06645c509934d",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
}


def latest_prior_report(explicit: Path | None = None) -> Path:
    """Select a successful real isolated R4R3 report, not a DryRun result."""
    if explicit is not None:
        result = explicit.resolve()
        if not result.is_file():
            raise RuntimeError("R4R4_R4R3_REPORT_MISSING: " + str(result))
        return result
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            continue
        if isinstance(data, dict) and data.get("gate") == PRIOR_GATE:
            return candidate
    raise RuntimeError("R4R4_NO_SUCCESSFUL_R4R3_REAL_REPORT")


def validate_prior_report(report: object) -> dict[str, object]:
    """Read the real R4R3 observation without upgrading it to proof evidence."""
    if not isinstance(report, dict):
        raise RuntimeError("R4R4_PRIOR_NOT_OBJECT")
    expected = {
        "phase": "175-R4R3",
        "mode": "ISOLATED_GENERIC_INFERENCE",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 1,
        "rule_connected_to_public": False,
        "complete_proof": False,
        "full_pytest_executed": False,
    }
    if any(report.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R4_PRIOR_GATE_OR_SCOPE_INVALID")
    pre = report.get("preflight")
    observed = report.get("r4_observation")
    if (not isinstance(pre, dict)
            or not isinstance(pre.get("head"), str)
            or len(pre["head"]) != 40
            or pre.get("pinned_source_count") != 18
            or not isinstance(observed, dict)
            or observed.get("target_group") != "pi_9^5"
            or observed.get("prior_group") != "pi_8^4"
            or observed.get("open_goals_count") != 3
            or observed.get("target_proven_steps") != 0
            or observed.get("prior_verified") is not True
            or observed.get("proof_complete") is not False):
        raise RuntimeError("R4R4_PRIOR_OBSERVATION_CHANGED")
    return {
        "head": pre["head"],
        "target_group": observed["target_group"],
        "prior_group": observed["prior_group"],
        "open_goals_count": observed["open_goals_count"],
        "target_proven_steps": observed["target_proven_steps"],
        "prior_verified": observed["prior_verified"],
        "proof_complete": False,
    }


def validate_prior_lineage(root: Path, prior_head: str, current_head: str) -> dict[str, object]:
    """Accept commits only when changes are confined to the isolated R4R3 package.

    The actual R4 and R4R3 source pins are also checked separately. This is
    not a blanket descendant-HEAD waiver: unrelated tracked edits fail.
    """
    if prior_head != EXPECTED_HEAD_AT_PRIOR_AUDIT:
        raise RuntimeError("R4R4_UNREVIEWED_PRIOR_HEAD")
    _, resolved_head = git(root, "rev-parse", "HEAD")
    if resolved_head != current_head:
        raise RuntimeError("R4R4_CURRENT_HEAD_MISMATCH")
    ancestor, _ = git(
        root, "merge-base", "--is-ancestor", prior_head, current_head,
        allow_failure=True,
    )
    if ancestor:
        raise RuntimeError("R4R4_PRIOR_HEAD_NOT_ANCESTOR")
    _, changed = git(root, "diff", "--name-only", prior_head, current_head)
    paths = sorted({part.strip() for part in changed.splitlines() if part.strip()})
    unexpected = [path for path in paths if not (
        path.startswith(PRIOR_PACKAGE + "/")
        or path == ".pytest_cache/v/cache/nodeids"
    )]
    if unexpected:
        raise RuntimeError("R4R4_UNREVIEWED_INTERVENING_FILES: " + repr(unexpected))
    return {"prior_head": prior_head, "current_head": current_head,
            "reviewed_intervening_paths": paths}


def verify_code_and_source_pins(root: Path) -> dict[str, str]:
    """Require the exact reviewed current files, never a guessed source."""
    for path, expected in EXTRA_SOURCE_PINS.items():
        if not (root / path).is_file():
            raise RuntimeError("R4R4_SOURCE_MISSING: " + path)
        _, actual = git(root, "rev-parse", "HEAD:" + path)
        if actual != expected:
            raise RuntimeError("R4R4_EXTRA_SOURCE_PIN_DRIFT: " + path)
    rule_file = root / PRIOR_PACKAGE / "rule.py"
    if not rule_file.is_file():
        raise RuntimeError("R4R4_R4R3_RULE_FILE_MISSING")
    actual_sha = sha256(rule_file.read_bytes()).hexdigest()
    if actual_sha != REVIEWED_RULE_SHA256:
        raise RuntimeError("R4R4_R4R3_RULE_CONTENT_CHANGED")
    return dict(EXTRA_SOURCE_PINS)


def read_printed_source_evidence(chapter_two: str, chapter_five: str) -> dict[str, bool]:
    """Check actual printed premises and their ordering, NOT proof validity."""
    start_25 = chapter_two.find(r"\begin{proposition}\label{prop:2.5}")
    if start_25 < 0:
        raise RuntimeError("R4R4_PROPOSITION25_MISSING")
    end_25 = chapter_two.find(r"\end{proposition}", start_25)
    if end_25 < start_25:
        raise RuntimeError("R4R4_PROPOSITION25_UNTERMINATED")
    p25 = chapter_two[start_25:end_25]
    if not all(key in p25 for key in (r"\Delta\alpha", r"\subset", r"\ni", "等号")):
        raise RuntimeError("R4R4_PROPOSITION25_HYPOTHESES_MISSING")
    start_58 = chapter_five.find(r"\begin{equation}\label{eq:5.8}")
    prop_58 = chapter_five.find(r"\begin{proposition}\label{prop:5.8}")
    prop_59 = chapter_five.find(r"\begin{equation}\label{eq:5.9}")
    if not (0 <= start_58 < prop_58 < prop_59):
        raise RuntimeError("R4R4_TODA58_ORDER_CHANGED")
    eq58_text = chapter_five[start_58:prop_58]
    proof = chapter_five[prop_58:prop_59]
    if r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" not in eq58_text:
        raise RuntimeError("R4R4_TODA58_IOTA_FORMULA_MISSING")
    required_proof = (
        r"\Delta(\eta_9)",
        r"\Delta(\iota_9)\circ \eta_7",
        r"\Delta:\pi_9^9\to\pi_7^4",
        r"\pi_9^5=E\pi_8^4",
        r"\pi^{5}_{9}=\mathbb Z_2",
        r"\pi^{4}_{8}=\mathbb Z_2",
    )
    if not all(text in proof for text in required_proof):
        raise RuntimeError("R4R4_TODA58_PROOF_CLAUSE_MISSING")
    return {
        "proposition25_inclusion_and_equality_conditions_printed": True,
        "equation58_iota_image_printed": True,
        "proposition58_delta_eta9_formula_printed": True,
        "proposition58_delta_right_injective_claim_printed": True,
        "proposition58_e_surjective_claim_printed": True,
        "proposition58_pi84_and_pi95_printed": True,
        "printed_text_counts_as_verified_inference_step": False,
    }


def verify_ehp_shape() -> dict[str, object]:
    """Construct the valid EHP Delta-to-E window, not a ProofStep."""
    from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from toda_rules import TodaProp42ExactnessStatement

    window = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(10, 9),
        middle_term=TodaPrimaryGroup(8, 4),
        target_term=TodaPrimaryGroup(9, 5),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(window) != (4, 9, "delta_e"):
        raise RuntimeError("R4R4_EHP_WINDOW_TYPE_MISMATCH")
    return {"source": "pi_10^9", "middle": "pi_8^4", "target": "pi_9^5",
            "exactness_indices": [4, 9, "delta_e"],
            "valid_window_is_a_verified_proof_step": False}


def premise_frontier(prior: dict[str, object], printed: dict[str, bool],
                     ehp: dict[str, object]) -> list[dict[str, object]]:
    """No fabricated parent ProofSteps; inventory is explicitly NOT replay."""
    if (prior.get("prior_verified") is not True
            or prior.get("target_proven_steps") != 0
            or printed.get("printed_text_counts_as_verified_inference_step") is not False
            or ehp.get("valid_window_is_a_verified_proof_step") is not False):
        raise RuntimeError("R4R4_PREMISE_EVIDENCE_BOUNDARY_CHANGED")
    return [
        {"index": 1, "premise": "pi_8^4 direct sum of two Z/2 summands",
         "evidence": "prior pi_8^4 complete and trust verified in R4",
         "status": "PRIOR_VERIFIED_TYPED_PRESENTATION_NOT_REPLAYED_HERE", "verified_parent_step_in_r4r4": False},
        {"index": 2, "premise": "pi_10^9 = Z/2{eta_9}",
         "evidence": "eta family and previous group data require a cited replay",
         "status": "SOURCE_FIRST_PROOF_NOT_REPLAYED", "verified_parent_step_in_r4r4": False},
        {"index": 3, "premise": "Delta(eta_9) = E nu-prime eta_7",
         "evidence": "Proposition 2.5 and (5.8) in Toda Chapter II/V",
         "status": "PRINTED_FORMULA_TYPED_INFERENCE_PENDING", "verified_parent_step_in_r4r4": False},
        {"index": 4, "premise": "Delta->E exactness, im Delta = ker E",
         "evidence": "typed Proposition 4.2 Delta-E window is valid",
         "status": "SCHEMA_VALID_PROOF_STEP_PENDING", "verified_parent_step_in_r4r4": False},
        {"index": 5, "premise": "E:pi_8^4 -> pi_9^5 surjective",
         "evidence": "Toda Proposition 5.8 derives it from right Delta injectivity and EHP exactness",
         "status": "PRINTED_ARGUMENT_TYPED_INFERENCE_PENDING", "verified_parent_step_in_r4r4": False},
        {"index": 6, "premise": "E(nu_4 eta_7) = nu_5 eta_8",
         "evidence": "general composite-suspension inference exists, factor image ProofSteps not replayed",
         "status": "GENERIC_RULE_PRESENT_FACTOR_PROOFS_PENDING", "verified_parent_step_in_r4r4": False},
    ]


def report_folder() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    output = root / "EHPProofTracerAudit" / PACKAGE / stamp
    output.mkdir(parents=True, exist_ok=False)
    return output


def run(root: Path, dry_run: bool, prior_path: Path | None = None) -> int:
    output = report_folder()
    result: dict[str, object] = {
        "phase": "175-R4R4", "mode": "SOURCE_FIRST_PREMISE_FRONTIER_AUDIT",
        "dry_run": dry_run, "gate": "FAIL_R4R4_PREMISE_AUDIT",
        "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": [], "rule_connected_to_public": False,
        "public_proof_complete": False, "full_pytest_executed": False,
    }
    try:
        pre = preflight(root)
        result["preflight"] = pre
        prior_file = latest_prior_report(prior_path)
        prior_report = json.loads(prior_file.read_text(encoding="utf-8"))
        prior = validate_prior_report(prior_report)
        result["prior_report"] = str(prior_file)
        result["prior_observation"] = prior
        result["prior_head_lineage"] = validate_prior_lineage(root, prior["head"], pre["head"])
        result["extra_pinned_sources"] = verify_code_and_source_pins(root)
        result["r4r3_rule_sha256"] = REVIEWED_RULE_SHA256
        printed = read_printed_source_evidence(
            (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
            (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
        )
        result["printed_evidence"] = printed
        ehp = verify_ehp_shape()
        result["ehp_schema"] = ehp
        rows = premise_frontier(prior, printed, ehp)
        result["premises"] = rows
        result["premise_count"] = len(rows)
        result["verified_parent_steps_replayed_here"] = 0
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        result["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    text_lines = [
        "# Phase 175 R4R4 — $\\pi_9^5$ 6前提 Source-first 監査", "",
        "Gate: `" + str(result["gate"]) + "`", "",
        "文献上の記載、型の妥当性、検証済み ProofStep は異なる。", "",
        "新規 GIVEN = 0、数学規則 = 0、公開接続 = なし。", "",
        "## R4R3 の商群規則に必要な6前提", "",
    ]
    for row in result.get("premises", []):
        text_lines.append(f"{row['index']}. {row['premise']} — {row['status']}")
    text_lines.extend(["", "監査だけでは群の完成証明を生成しない。", ""])
    (output / "report.md").write_text("\n".join(text_lines), encoding="utf-8")
    print("PHASE175_R4R4_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R4_PINNED_R4_SOURCES=" + str(result.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4R4_EXTRA_PINNED_SOURCES=" + str(len(result.get("extra_pinned_sources", {}))))
    print("PHASE175_R4R4_PREMISES=" + str(result.get("premise_count", 0)))
    print("PHASE175_R4R4_NEW_GIVEN=0")
    print("PHASE175_R4R4_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R4_PUBLIC_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R4_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R4_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R4_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R4_ERROR=" + str(result["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r3-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run, args.r4r3_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_audit.py` 全文

```python
"""Focused R4R4 fail-closed contracts; all report and source fixtures are synthetic."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

import pytest

from phase175_r4r4_pi95_premise_frontier import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R3",
        "mode": "ISOLATED_GENERIC_INFERENCE",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "production_changes": [],
        "new_given": 0,
        "new_mathematical_rules": 1,
        "rule_connected_to_public": False,
        "complete_proof": False,
        "full_pytest_executed": False,
        "preflight": {
            "head": audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
            "pinned_source_count": 18,
        },
        "r4_observation": {
            "target_group": "pi_9^5",
            "prior_group": "pi_8^4",
            "open_goals_count": 3,
            "target_proven_steps": 0,
            "prior_verified": True,
            "proof_complete": False,
        },
    }


def printed_fixture() -> tuple[str, str]:
    chapter_two = (
        r"\begin{proposition}\label{prop:2.5}" + "\n"
        + r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)." + "\n"
        + r"\Delta(E^2\gamma)\ \ni\ \pm\,[\iota_m,\iota_m]\circ\gamma" + "\n"
        + "等号の条件: 2-primary" + "\n"
        + r"\end{proposition}"
    )
    chapter_five = (
        r"\begin{equation}\label{eq:5.8}" + "\n"
        + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" + "\n"
        + r"\end{equation}" + "\n"
        + r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{4}_{8}=\mathbb Z_2" + "\n"
        + r"\pi^{5}_{9}=\mathbb Z_2" + "\n"
        + r"\end{proposition}" + "\n"
        + r"\Delta:\pi_9^9\to\pi_7^4" + "\n"
        + r"\Delta(\eta_9)" + "\n"
        + r"\Delta(\iota_9)\circ \eta_7" + "\n"
        + r"\pi_9^5=E\pi_8^4" + "\n"
        + r"\begin{equation}\label{eq:5.9}"
    )
    return chapter_two, chapter_five


def test_prior_success_is_not_promoted_to_public_proof() -> None:
    found = audit.validate_prior_report(prior_fixture())
    assert found["open_goals_count"] == 3
    assert found["target_proven_steps"] == 0
    assert found["proof_complete"] is False
    assert found["prior_verified"] is True


@pytest.mark.parametrize("key,value", [
    ("phase", "175-R4R2"),
    ("mode", "PUBLIC_PROOF"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("production_changes", ["proof.py"]),
    ("new_given", 1),
    ("new_mathematical_rules", 2),
    ("rule_connected_to_public", True),
    ("complete_proof", True),
    ("full_pytest_executed", True),
])
def test_prior_scope_tampering_rejected(key: str, value: object) -> None:
    report = prior_fixture()
    report[key] = value
    with pytest.raises(RuntimeError, match="R4R4_PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior_report(report)


@pytest.mark.parametrize("section,key,value", [
    ("preflight", "head", "bad"),
    ("preflight", "pinned_source_count", 17),
    ("r4_observation", "target_group", "pi_10^6"),
    ("r4_observation", "open_goals_count", 2),
    ("r4_observation", "target_proven_steps", 1),
    ("r4_observation", "prior_verified", False),
    ("r4_observation", "proof_complete", True),
])
def test_prior_evidence_tampering_rejected(
    section: str, key: str, value: object,
) -> None:
    report = deepcopy(prior_fixture())
    report[section][key] = value
    with pytest.raises(RuntimeError, match="R4R4_PRIOR_OBSERVATION_CHANGED"):
        audit.validate_prior_report(report)


def test_latest_passed_real_report_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    passed = folder / "20261117T051200Z"
    later = folder / "20261117T053000Z"
    passed.mkdir(parents=True)
    later.mkdir(parents=True)
    (passed / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    failure = prior_fixture()
    failure["gate"] = "FAIL_R4R3_ISOLATED_RULE"
    (later / "report.json").write_text(json.dumps(failure), encoding="utf-8")
    assert audit.latest_prior_report() == passed / "report.json"
    assert audit.latest_prior_report(passed / "report.json") == (passed / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R4_R4R3_REPORT_MISSING"):
        audit.latest_prior_report(folder / "missing.json")


def fake_git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    if args == ("rev-parse", "HEAD"):
        return 0, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT
    if args[:2] == ("merge-base", "--is-ancestor"):
        return 0, ""
    if args[:2] == ("diff", "--name-only"):
        return 0, ""
    raise AssertionError(f"unexpected git args: {args}")


def test_lineage_accepts_same_reviewed_head(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(audit, "git", fake_git)
    found = audit.validate_prior_lineage(
        tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
        audit.EXPECTED_HEAD_AT_PRIOR_AUDIT,
    )
    assert found["reviewed_intervening_paths"] == []


def test_lineage_accepts_only_isolated_package_descendant(tmp_path: Path, monkeypatch) -> None:
    descendant = "4" * 40

    def git_approved(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, descendant
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase175_r4r3_two_summand_quotient/README.md\n.pytest_cache/v/cache/nodeids"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", git_approved)
    found = audit.validate_prior_lineage(tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, descendant)
    assert len(found["reviewed_intervening_paths"]) == 2


def test_lineage_rejects_unaudited_production_change(tmp_path: Path, monkeypatch) -> None:
    descendant = "4" * 40

    def git_dirty(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, descendant
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase165_r52_r9_shared_math.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", git_dirty)
    with pytest.raises(RuntimeError, match="R4R4_UNREVIEWED_INTERVENING_FILES"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, descendant)


@pytest.mark.parametrize("prior,current,code", [
    ("f" * 40, audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, "R4R4_UNREVIEWED_PRIOR_HEAD"),
    (audit.EXPECTED_HEAD_AT_PRIOR_AUDIT, "a" * 40, "R4R4_CURRENT_HEAD_MISMATCH"),
])
def test_lineage_rejects_wrong_ref(
    tmp_path: Path, monkeypatch, prior: str, current: str, code: str,
) -> None:
    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match=code):
        audit.validate_prior_lineage(tmp_path, prior, current)


def test_reviewed_source_and_printed_evidence() -> None:
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    assert evidence["proposition58_delta_eta9_formula_printed"] is True
    assert evidence["printed_text_counts_as_verified_inference_step"] is False


@pytest.mark.parametrize("marker", [
    r"\Delta\alpha", r"\subset", r"\ni", "等号",
])
def test_prop25_conditions_fail_closed(marker: str) -> None:
    chapter_two, chapter_five = printed_fixture()
    with pytest.raises(RuntimeError, match="R4R4_PROPOSITION25_HYPOTHESES_MISSING"):
        audit.read_printed_source_evidence(chapter_two.replace(marker, "REMOVED"), chapter_five)


@pytest.mark.parametrize("marker", [
    r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')",
    r"\Delta(\eta_9)",
    r"\Delta(\iota_9)\circ \eta_7",
    r"\Delta:\pi_9^9\to\pi_7^4",
    r"\pi_9^5=E\pi_8^4",
    r"\pi^{5}_{9}=\mathbb Z_2",
    r"\pi^{4}_{8}=\mathbb Z_2",
])
def test_prop58_source_clause_fail_closed(marker: str) -> None:
    chapter_two, chapter_five = printed_fixture()
    with pytest.raises(RuntimeError, match="R4R4_TODA58"):
        audit.read_printed_source_evidence(chapter_two, chapter_five.replace(marker, "REMOVED"))


def test_exact_six_premises_never_claim_verified_parents() -> None:
    prior = audit.validate_prior_report(prior_fixture())
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    window = {"valid_window_is_a_verified_proof_step": False}
    rows = audit.premise_frontier(prior, evidence, window)
    assert [r["index"] for r in rows] == list(range(1, 7))
    assert all(r["verified_parent_step_in_r4r4"] is False for r in rows)
    assert rows[2]["status"] == "PRINTED_FORMULA_TYPED_INFERENCE_PENDING"
    assert rows[4]["status"] == "PRINTED_ARGUMENT_TYPED_INFERENCE_PENDING"


@pytest.mark.parametrize("which", ["prior", "evidence", "window"])
def test_premise_boundary_fails_closed(which: str) -> None:
    prior = audit.validate_prior_report(prior_fixture())
    evidence = audit.read_printed_source_evidence(*printed_fixture())
    window = {"valid_window_is_a_verified_proof_step": False}
    if which == "prior":
        prior["target_proven_steps"] = 1
    elif which == "evidence":
        evidence["printed_text_counts_as_verified_inference_step"] = True
    else:
        window["valid_window_is_a_verified_proof_step"] = True
    with pytest.raises(RuntimeError, match="R4R4_PREMISE_EVIDENCE_BOUNDARY_CHANGED"):
        audit.premise_frontier(prior, evidence, window)


def test_rule_file_sha_is_pinned(tmp_path: Path, monkeypatch) -> None:
    rule = tmp_path / audit.PRIOR_PACKAGE / "rule.py"
    rule.parent.mkdir()
    rule.write_bytes(b"synthetic rule content")
    for path in audit.EXTRA_SOURCE_PINS:
        current = tmp_path / path
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text("synthetic test source", encoding="utf-8")

    def git_expected(root, *args, allow_failure=False):
        assert args[0] == "rev-parse" and args[1].startswith("HEAD:")
        path = args[1][5:]
        return 0, audit.EXTRA_SOURCE_PINS[path]

    monkeypatch.setattr(audit, "git", git_expected)
    with pytest.raises(RuntimeError, match="R4R4_R4R3_RULE_CONTENT_CHANGED"):
        audit.verify_code_and_source_pins(tmp_path)


def test_changed_extra_source_pin_rejected(tmp_path: Path, monkeypatch) -> None:
    for path in audit.EXTRA_SOURCE_PINS:
        current = tmp_path / path
        current.parent.mkdir(parents=True, exist_ok=True)
        current.write_text("synthetic test source", encoding="utf-8")

    def git_bad(root, *args, allow_failure=False):
        return 0, "0" * 40

    monkeypatch.setattr(audit, "git", git_bad)
    with pytest.raises(RuntimeError, match="R4R4_EXTRA_SOURCE_PIN_DRIFT"):
        audit.verify_code_and_source_pins(tmp_path)


def test_real_typed_delta_e_window_is_schema_only() -> None:
    """When the actual project types are installed, exercise them directly."""
    pytest.importorskip("homotopy_groups")
    found = audit.verify_ehp_shape()
    assert found["exactness_indices"] == [4, 9, "delta_e"]
    assert found["valid_window_is_a_verified_proof_step"] is False
```

## `run.ps1` 全文

```powershell
param(
    [switch] $DryRun,
    [string] $R4R3Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        phase175_r4r4_pi95_premise_frontier/tests/test_audit.py `
        phase175_r4r3_two_summand_quotient/tests/test_rule.py `
        phase175_r4r3_two_summand_quotient/tests/test_audit.py `
        phase175_r4_pi95_audit/tests/test_audit.py

    if ($LASTEXITCODE -ne 0) { throw 'R4R4 focused pytest failed' }
    Write-Output 'PHASE175_R4R4_FOCUSED_PYTEST=PASS'

    $cmd = @('-B', '-m', 'phase175_r4r4_pi95_premise_frontier.audit', '--root', $root)
    if ($DryRun) { $cmd += '--dry-run' }
    if ($R4R3Report -ne '') { $cmd += @('--r4r3-report', $R4R3Report) }

    & python @cmd
    $auditExitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R4_EXIT_CODE=$auditExitCode"
    if ($auditExitCode -ne 0) { exit $auditExitCode }
    exit 0
} finally {
    Pop-Location
}
```

## `__init__.py` 全文

```python
"""Read-only Phase 175 R4R4 evidence inventory; not a proof provider."""
```

