# Phase 175 R4R8 — 追加コード全文

新規ディレクトリ `phase175_r4r8_signed_delta_kernel_frontier/` のみ追加。既存クラス・関数・import の変更はありません。

## __init__.py（全文）

```python
"""Phase 175 R4R8: read-only signed Delta image/kernel frontier audit."""
```

## audit.py（全文）

```python
"""Phase 175 R4R8: source-first, read-only signed Delta image frontier.

No GIVEN, rule, certificate, saved proof, narrative or public provider is added.
The algebraic kernel calculation is an audit observation, not a ProofStep.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback


PACKAGE = "phase175_r4r8_signed_delta_kernel_frontier"
PRIOR_PACKAGE = "phase175_r4r7_prop25_typed_composition"
PRIOR_GATE = "PASS_R4R7_PROP25_TYPED_INFERENCE_ISOLATED_NOT_PUBLIC"
DRY_GATE = "PASS_R4R8_SIGNED_DELTA_KERNEL_FRONTIER_DRYRUN"
FINAL_GATE = "PASS_R4R8_SIGNED_DELTA_KERNEL_FRONTIER_RECORDED_NOT_PUBLIC"
BASE_HEAD = "11968d23724cee147520b5fa3fd5a6e89989003e"
REVIEWED_R4R7_HEAD = "51f9907ac3116c78778d75864775d30d095efa5c"
REVIEWED_R4R7_RULE_BLOB = "e957752baf93f75352d106e53205730af9a02b4d"
REVIEWED_R4R7_AUDIT_BLOB = "c77e744339beef327854de74df73840d2bfb5569"
PINNED_BLOBS = {
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "df4e0f834e9bc321f338ec10b363c79d82623457",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase175_r4r7_prop25_typed_composition/rule.py": REVIEWED_R4R7_RULE_BLOB,
    "phase175_r4r7_prop25_typed_composition/audit.py": REVIEWED_R4R7_AUDIT_BLOB,
}
ALLOWED_COMMITTED_PREFIX = PRIOR_PACKAGE + "/"


def git(root: Path, *arguments: str, allowed_failure: bool = False) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode and not allowed_failure:
        raise RuntimeError("R4R8_GIT_ERROR: " + " ".join(arguments) + " " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def reviewed_lineage(root: Path, head: str) -> dict[str, object]:
    """Permit only a descendant of the audited baseline changing R4R7 paths.

    Both old HEAD and later R4R7-only commits are accepted. The actual rule,
    audit and underlying mathematical source blobs remain independently pinned.
    """
    code, _ = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head,
                  allowed_failure=True)
    if code != 0:
        raise RuntimeError("R4R8_BASE_HEAD_NOT_ANCESTOR")
    _, changed = git(root, "diff", "--name-only", BASE_HEAD, head)
    changed_paths = sorted(set(line.strip() for line in changed.splitlines() if line.strip()))
    invalid = [path for path in changed_paths if not (
        path.startswith(ALLOWED_COMMITTED_PREFIX)
        or path == ".pytest_cache/v/cache/nodeids"
    )]
    if invalid:
        raise RuntimeError("R4R8_UNREVIEWED_COMMITTED_CHANGE: " + repr(invalid))
    if head == REVIEWED_R4R7_HEAD and not changed_paths:
        raise RuntimeError("R4R8_R4R7_COMMIT_CONTENT_MISSING")
    return {
        "reviewed_base_head": BASE_HEAD,
        "reviewed_r4r7_head": REVIEWED_R4R7_HEAD,
        "head": head,
        "reviewed_intervening_paths": changed_paths,
    }


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R8_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R8_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    lineage = reviewed_lineage(root, head)
    dirty = sorted(set(
        git(root, "diff", "--name-only")[1].splitlines()
        + git(root, "diff", "--cached", "--name-only")[1].splitlines()
    ))
    if [x for x in dirty if x != ".pytest_cache/v/cache/nodeids"]:
        raise RuntimeError("R4R8_UNREVIEWED_TRACKED_CHANGES: " + repr(dirty))
    for path, expected in PINNED_BLOBS.items():
        if not (root / path).is_file():
            raise RuntimeError("R4R8_PINNED_SOURCE_MISSING: " + path)
        # R4R7 can still be untracked at the reviewed R4R6 HEAD; verify
        # its working-file Git blob rather than pretending it is committed.
        # All earlier source files must remain committed and match the pin.
        is_r4r7_file = path.startswith(ALLOWED_COMMITTED_PREFIX)
        if is_r4r7_file and head == BASE_HEAD:
            actual = git(root, "hash-object", "--", path)[1]
        else:
            actual = git(root, "rev-parse", "HEAD:" + path)[1]
        if actual != expected:
            raise RuntimeError("R4R8_PINNED_SOURCE_BLOB_DRIFT: " + path)
    shared_source = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    if "phase175_r4r7_prop25_typed_composition" in shared_source:
        raise RuntimeError("R4R8_PREMATURE_PROP25_PUBLIC_CONNECTION")
    return {
        **lineage,
        "pinned_source_blobs": len(PINNED_BLOBS),
        "tracked_dirty": dirty,
        "new_given": 0,
        "new_mathematical_rules": 0,
    }


def validate_prior(data: object) -> dict[str, object]:
    """An actual R4R7 non-DryRun PASS is audit provenance, never a ProofStep."""
    if not isinstance(data, dict):
        raise RuntimeError("R4R8_PRIOR_REPORT_INVALID")
    expected = {
        "phase": "175-R4R7",
        "mode": "ISOLATED_TYPED_CONDITIONAL_INFERENCE",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    differences = [key for key, value in expected.items() if data.get(key) != value]
    if differences:
        raise RuntimeError("R4R8_PRIOR_SCOPE_INVALID: " + repr(differences))
    pre, source, isolated = (
        data.get("preflight"), data.get("source_and_boundary"), data.get("isolated"),
    )
    if not isinstance(pre, dict) or pre.get("head") != BASE_HEAD:
        raise RuntimeError("R4R8_PRIOR_HISTORICAL_HEAD_INVALID")
    if (not isinstance(source, dict)
            or source.get("source_rechecked") is not True
            or source.get("sign_retained") is not True
            or source.get("public_search_unchanged") is not True
            or source.get("source_is_proof") is not False):
        raise RuntimeError("R4R8_PRIOR_SOURCE_BOUNDARY_INVALID")
    if (not isinstance(isolated, dict)
            or isolated.get("isolated_backward_proposals") != 1
            or isolated.get("unproved_parent_obligations") != 2
            or isolated.get("signed_goal_retained") is not True
            or isolated.get("verified_parent_proof_steps_created") != 0
            or isolated.get("previous_proof_search_executed") is not False
            or isolated.get("public_provider_connected") is not False
            or isolated.get("pi95_completed") is not False):
        raise RuntimeError("R4R8_PRIOR_ISOLATED_EVIDENCE_INVALID")
    return {
        "historical_r4r7_head": pre["head"],
        "signed_obligation_remained_unproved": True,
        "prior_is_not_proof_certificate": True,
    }


def find_prior(explicit: Path | None = None) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    if explicit is not None:
        candidate = explicit.expanduser().resolve()
        if not candidate.is_file():
            raise RuntimeError("R4R8_PRIOR_REPORT_NOT_FOUND: " + str(candidate))
        return candidate
    rejected: list[str] = []
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            rejected.append(str(path) + ": " + str(exc))
            continue
        return path
    raise RuntimeError(
        "R4R8_VALID_R4R7_REPORT_MISSING: " + str(folder)
        + " rejected=" + repr(rejected[:5])
    )


def section(source: str, start: str, end: str) -> str:
    pos = source.find(start)
    if pos < 0:
        raise RuntimeError("R4R8_SOURCE_SECTION_MISSING: " + start)
    last = source.find(end, pos + len(start))
    if last < 0:
        raise RuntimeError("R4R8_SOURCE_END_MISSING: " + end)
    return source[pos:last]


def source_frontier(chapter_two: str, chapter_five: str) -> dict[str, object]:
    """Check authored Toda clauses without upgrading printed text into proof."""
    prop25 = section(chapter_two, r"\begin{proposition}\label{prop:2.5}", r"\end{proposition}")
    eq58 = section(chapter_five, r"\begin{equation}\label{eq:5.8}", r"\end{equation}")
    prop58 = section(chapter_five, r"\begin{proposition}\label{prop:5.8}", r"\end{proposition}")
    if any(token not in prop25 for token in (r"\Delta\alpha", r"\subset", r"j<3m-1", "等号")):
        raise RuntimeError("R4R8_PROP25_SOURCE_DRIFT")
    if r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" not in eq58:
        raise RuntimeError("R4R8_EQ58_SIGN_OR_GENERATOR_DRIFT")
    if r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}" not in prop58:
        raise RuntimeError("R4R8_TARGET_SOURCE_DRIFT")
    if "\\Delta(\\eta_9)" not in chapter_five:
        raise RuntimeError("R4R8_PROP58_ARGUMENT_MISSING")
    return {
        "prop25_equality_condition_m4_j9": 9 < 3 * 4 - 1,
        "equation58_signed_literal_present": True,
        "positive_generator_representation": "2nu_4-E_nu_prime",
        "source_sign": "±",
        "source_not_a_verified_proof_step": True,
        "target_group_is_not_adopted": True,
    }


def cyclic_kernel_arithmetic(target_order: int, torsion_order: int) -> dict[str, object]:
    """Audit Z{x} + Z/m{y} -> Z/N with x|->1, y|->N/m.

    For N>0 and 0<m|N, every kernel pair (u,v mod m) has
    u=(N/m)t, v=-t mod m; hence Ker=Z{(N/m,-1)}.
    This does not assert that the needed E-map facts are proven in this project.
    """
    if (type(target_order) is not int or type(torsion_order) is not int
            or target_order <= 1 or torsion_order <= 1
            or target_order % torsion_order != 0):
        raise ValueError("R4R8_INVALID_CYCLIC_KERNEL_PARAMETERS")
    b = target_order // torsion_order
    return {
        "domain_form": "Z{x} + Z/m{y}",
        "codomain_order": target_order,
        "torsion_order": torsion_order,
        "e_x_image_coefficient": 1,
        "e_y_image_coefficient": b,
        "kernel_generator_free_coefficient": b,
        "kernel_generator_torsion_coefficient": -1,
        "e_of_kernel_generator_mod_N": (b - b) % target_order,
        "kernel_rank": 1,
        "arithmetic_checked_not_a_proof_step": True,
    }


def typed_ehp_window() -> dict[str, object]:
    """Check shape of Delta:pi_9^9 -> pi_7^4 -> pi_8^5; not proof."""
    from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from toda_rules import TodaProp42ExactnessStatement

    window = TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(9, 9),
        middle_term=TodaPrimaryGroup(7, 4),
        target_term=TodaPrimaryGroup(8, 5),
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    )
    indices = prop42_exactness_indices(TodaProp42ExactnessStatement(window))
    if indices != (4, 8, "delta_e"):
        raise RuntimeError("R4R8_EHP_DELTA_E_WINDOW_TYPE_MISMATCH: " + repr(indices))
    return {
        "source": "pi_9^9", "middle": "pi_7^4", "target": "pi_8^5",
        "indices": list(indices),
        "schema_valid_not_a_verified_proof_step": True,
    }


def prior_group_shapes() -> dict[str, object]:
    """Check only earlier-group *presentations*; no previous proof replay."""
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from proof import Relation, RelationType

    left = exact_prior_database_result(4, 3)
    right = exact_prior_database_result(5, 3)
    if (not isinstance(left, Relation) or left.relation_type is not RelationType.EQUALITY
            or not isinstance(left.rhs, DirectSumGroup)
            or len(left.rhs.summands) != 2
            or not isinstance(left.rhs.summands[0], FreeCyclicGroup)
            or not isinstance(left.rhs.summands[1], FiniteCyclicGroup)
            or left.rhs.summands[1].order != 4
            or not isinstance(right, Relation) or right.relation_type is not RelationType.EQUALITY
            or not isinstance(right.rhs, FiniteCyclicGroup)
            or right.rhs.order != 8):
        raise RuntimeError("R4R8_EARLIER_DB_PRIOR_GROUP_SHAPE_DRIFT")
    return {
        "pi7_4_structure": "Z + Z/4",
        "pi8_5_structure": "Z/8",
        "prior_presentations_identified": 2,
        "previous_proof_search_executed": False,
        "group_presentations_do_not_certify_E_actions": True,
    }


def unresolved_obligations() -> list[dict[str, object]]:
    """Typed mathematical work for later phases, never fabricated steps."""
    rows = [
        (1, "Group pi_9^9 = Z{iota_9} with verified generator witness"),
        (2, "Certified E(nu_4)=nu_5 and E(E nu-prime)=2nu_5"),
        (3, "Certified EHP exactness Im Delta=Ker E at pi_7^4"),
        (4, "Typed general inference Ker E=Z{2nu_4-E nu-prime} from proved map data"),
        (5, "Typed generator-surjection inference Delta(iota_9)=+/-(2nu_4-E nu-prime)"),
        (6, "Typed iota_9 o E^2 eta_7=eta_9 inference for R4R7 premise"),
    ]
    return [
        {"index": index, "obligation": description, "verified_proof_step_in_r4r8": False}
        for index, description in rows
    ]


def report_dir() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    path = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    path.mkdir(parents=True, exist_ok=False)
    return path


def run(root: Path, *, dry_run: bool, prior_file: Path | None = None) -> int:
    output = report_dir()
    report: dict[str, object] = {
        "phase": "175-R4R8", "mode": "READ_ONLY_SIGNED_DELTA_KERNEL_FRONTIER",
        "dry_run": dry_run, "gate": "FAIL_R4R8_SIGNED_DELTA_KERNEL_FRONTIER",
        "new_given": 0, "new_mathematical_rules": 0,
        "production_changes": [], "rule_connected_to_public": False,
        "pi95_proof_complete": False, "full_pytest_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        prior_path = find_prior(prior_file)
        report["prior_report"] = str(prior_path)
        report["prior"] = validate_prior(json.loads(prior_path.read_text(encoding="utf-8")))
        report["printed"] = source_frontier(
            (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
            (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
        )
        report["groups"] = prior_group_shapes()
        report["ehp_window"] = typed_ehp_window()
        report["kernel_arithmetic"] = cyclic_kernel_arithmetic(8, 4)
        report["unresolved_obligations"] = unresolved_obligations()
        report["prior_proof_search_executed"] = False
        report["verified_parent_proof_steps_created"] = 0
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "report.md").write_text(
        "# Phase 175 R4R8 — 符号付き Delta 像の source-first 監査\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "Toda (5.8) の記載は証明済み ProofStep ではない。\n\n"
        + "群構造と仮定した E の生成元像から導く核の代数計算は、条件付きの監査情報。\n\n"
        + "符号 ± を維持し、未解決の証明義務を列挙する。\n\n"
        + "先行完成証明の再探索なし。公開 Provider 接続なし。π₉⁵ は未完成。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R8_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R8_NEW_GIVEN=0")
    print("PHASE175_R4R8_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R8_PRODUCTION_CHANGES=0")
    print("PHASE175_R4R8_PRIOR_PROOF_SEARCH=NOT_EXECUTED")
    print("PHASE175_R4R8_UNRESOLVED_OBLIGATIONS=" + str(len(report.get("unresolved_obligations", []))))
    print("PHASE175_R4R8_PUBLIC_RULE=NOT_CONNECTED")
    print("PHASE175_R4R8_PI95=NOT_COMPLETE")
    print("PHASE175_R4R8_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R8_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R8_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R8_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r7-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r7_report)


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_audit.py（全文）

```python
"""R4R8 standalone, source-first, fail-closed tests (synthetic evidence)."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from phase175_r4r8_signed_delta_kernel_frontier import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R7",
        "mode": "ISOLATED_TYPED_CONDITIONAL_INFERENCE",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.BASE_HEAD},
        "source_and_boundary": {
            "source_rechecked": True,
            "sign_retained": True,
            "public_search_unchanged": True,
            "source_is_proof": False,
        },
        "isolated": {
            "isolated_backward_proposals": 1,
            "unproved_parent_obligations": 2,
            "signed_goal_retained": True,
            "verified_parent_proof_steps_created": 0,
            "previous_proof_search_executed": False,
            "public_provider_connected": False,
            "pi95_completed": False,
        },
    }


def text_fixture() -> tuple[str, str]:
    chapter_two = (
        r"\begin{proposition}\label{prop:2.5}" + "\n"
        + r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)" + "\n"
        + r"j<3m-1" + " とき等号\n"
        + r"\end{proposition}"
    )
    chapter_five = (
        r"\begin{equation}\label{eq:5.8}" + "\n"
        + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" + "\n"
        + r"\end{equation}" + "\n"
        + r"\begin{proposition}\label{prop:5.8}" + "\n"
        + r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}" + "\n"
        + r"\end{proposition}" + "\n"
        + r"\Delta(\eta_9)"
    )
    return chapter_two, chapter_five


def test_success_prior_is_not_a_proof_certificate() -> None:
    result = audit.validate_prior(prior_fixture())
    assert result["prior_is_not_proof_certificate"] is True
    assert result["historical_r4r7_head"] == audit.BASE_HEAD


@pytest.mark.parametrize("key,invalid", (
    ("gate", "PASS_UNRELATED"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 0),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
))
def test_prior_scope_tampering_rejected(key: str, invalid: object) -> None:
    record = prior_fixture()
    record[key] = invalid
    with pytest.raises(RuntimeError, match="R4R8_PRIOR_SCOPE_INVALID"):
        audit.validate_prior(record)


@pytest.mark.parametrize("field,invalid", (
    ("head", "0" * 40),
))
def test_prior_historical_head_fail_closed(field: str, invalid: object) -> None:
    data = prior_fixture()
    data["preflight"][field] = invalid
    with pytest.raises(RuntimeError, match="HISTORICAL_HEAD_INVALID"):
        audit.validate_prior(data)


@pytest.mark.parametrize("section,key,invalid", (
    ("source_and_boundary", "source_rechecked", False),
    ("source_and_boundary", "sign_retained", False),
    ("source_and_boundary", "source_is_proof", True),
    ("isolated", "unproved_parent_obligations", 1),
    ("isolated", "verified_parent_proof_steps_created", 1),
    ("isolated", "previous_proof_search_executed", True),
    ("isolated", "public_provider_connected", True),
))
def test_prior_evidence_tampering_rejected(section: str, key: str, invalid: object) -> None:
    data = deepcopy(prior_fixture())
    data[section][key] = invalid
    with pytest.raises(RuntimeError, match="R4R8_PRIOR_"):
        audit.validate_prior(data)


def test_latest_prior_finds_real_pass_and_ignores_dryrun(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    earlier = folder / "20261117T085531_456222Z"
    newer = folder / "20261117T085540_456222Z"
    earlier.mkdir(parents=True)
    newer.mkdir(parents=True)
    (earlier / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    wrong = prior_fixture()
    wrong["dry_run"] = True
    (newer / "report.json").write_text(json.dumps(wrong), encoding="utf-8")
    assert audit.find_prior() == earlier / "report.json"
    assert audit.find_prior(earlier / "report.json") == (earlier / "report.json").resolve()
    with pytest.raises(RuntimeError, match="PRIOR_REPORT_NOT_FOUND"):
        audit.find_prior(folder / "missing.json")


def test_source_preserves_sign_and_is_not_a_step() -> None:
    result = audit.source_frontier(*text_fixture())
    assert result["source_sign"] == "±"
    assert result["source_not_a_verified_proof_step"] is True
    assert result["prop25_equality_condition_m4_j9"] is True


@pytest.mark.parametrize("part,token", (
    (0, r"\Delta\alpha"),
    (0, r"j<3m-1"),
    (1, r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')"),
    (1, r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"),
    (1, r"\Delta(\eta_9)"),
))
def test_malformed_source_rejected(part: int, token: str) -> None:
    sources = list(text_fixture())
    sources[part] = sources[part].replace(token, "REMOVED")
    with pytest.raises(RuntimeError, match="R4R8_"):
        audit.source_frontier(*sources)


@pytest.mark.parametrize("N,m", ((8, 4), (8, 2), (12, 3), (16, 8), (6, 2)))
def test_general_kernel_formula_and_enumeration(N: int, m: int) -> None:
    result = audit.cyclic_kernel_arithmetic(N, m)
    b = N // m
    assert result["kernel_generator_free_coefficient"] == b
    assert result["kernel_generator_torsion_coefficient"] == -1
    assert result["arithmetic_checked_not_a_proof_step"] is True
    for u in range(-2 * N, 2 * N + 1):
        for v in range(m):
            kernel_member = ((u + b * v) % N) == 0
            generated_member = (u % b == 0 and (v + u // b) % m == 0)
            assert kernel_member == generated_member


@pytest.mark.parametrize("N,m", ((0, 4), (8, 0), (8, 3), (4, 8), (True, 4), (8, False)))
def test_invalid_kernel_domain_fails_closed(N: object, m: object) -> None:
    with pytest.raises(ValueError, match="R4R8_INVALID_CYCLIC_KERNEL_PARAMETERS"):
        audit.cyclic_kernel_arithmetic(N, m)


def test_unresolved_evidence_is_never_labeled_proved() -> None:
    rows = audit.unresolved_obligations()
    assert len(rows) == 6
    assert [x["index"] for x in rows] == list(range(1, 7))
    assert all(x["verified_proof_step_in_r4r8"] is False for x in rows)
    assert any("surjection" in x["obligation"] for x in rows)


def g(root: Path, *parts: str) -> str:
    return subprocess.run(["git", *parts], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def commit(root: Path, message: str) -> None:
    g(root, "add", ".")
    g(root, "-c", "user.name=Test", "-c", "user.email=t@example.com",
      "commit", "-qm", message)


def init_repo(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    g(root, "init", "-q")
    (root / "baseline.txt").write_text("baseline", encoding="utf-8")
    commit(root, "baseline")
    base = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "BASE_HEAD", base)
    return root, base


def test_reviewed_lineage_accepts_baseline_and_r4r7_commit(tmp_path: Path, monkeypatch) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    assert audit.reviewed_lineage(root, base)["reviewed_intervening_paths"] == []
    changed = root / audit.PRIOR_PACKAGE / "rule.py"
    changed.parent.mkdir(parents=True)
    changed.write_text("isolated rule", encoding="utf-8")
    commit(root, "r4r7")
    result = audit.reviewed_lineage(root, g(root, "rev-parse", "HEAD"))
    assert result["reviewed_intervening_paths"] == [audit.PRIOR_PACKAGE + "/rule.py"]


def test_reviewed_lineage_rejects_unrelated_change(tmp_path: Path, monkeypatch) -> None:
    root, _ = init_repo(tmp_path, monkeypatch)
    (root / "proof.py").write_text("unreviewed", encoding="utf-8")
    commit(root, "unauthorized")
    with pytest.raises(RuntimeError, match="R4R8_UNREVIEWED_COMMITTED_CHANGE"):
        audit.reviewed_lineage(root, g(root, "rev-parse", "HEAD"))


def test_reviewed_lineage_rejects_non_descendant(tmp_path: Path, monkeypatch) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(audit, "BASE_HEAD", "0" * 40)
    with pytest.raises(RuntimeError, match="R4R8_BASE_HEAD_NOT_ANCESTOR"):
        audit.reviewed_lineage(root, base)


def test_reviewed_lineage_rejects_false_exact_r4r7_successor(tmp_path: Path, monkeypatch) -> None:
    root, _ = init_repo(tmp_path, monkeypatch)
    fake_head = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "REVIEWED_R4R7_HEAD", fake_head)
    with pytest.raises(RuntimeError, match="R4R8_R4R7_COMMIT_CONTENT_MISSING"):
        audit.reviewed_lineage(root, fake_head)


def test_preflight_accepts_source_pinned_untracked_r4r7_at_base_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    g(root, "checkout", "-qb", "develop")
    fake_source = root / "phase165_r52_r9_shared_math.py"
    fake_source.write_text("def shared_expansion_provider():\n    return ()\n", encoding="utf-8")
    commit(root, "committed source")
    base = g(root, "rev-parse", "HEAD")
    monkeypatch.setattr(audit, "BASE_HEAD", base)
    p = root / audit.PRIOR_PACKAGE / "rule.py"
    p.parent.mkdir(parents=True)
    p.write_text("uncommitted, reviewed prior rule\n", encoding="utf-8")
    committed_blob = g(root, "rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    untracked_blob = g(root, "hash-object", "--", p.relative_to(root).as_posix())
    monkeypatch.setattr(audit, "PINNED_BLOBS", {
        "phase165_r52_r9_shared_math.py": committed_blob,
        audit.PRIOR_PACKAGE + "/rule.py": untracked_blob,
    })
    checked = audit.preflight(root)
    assert checked["head"] == base
    assert checked["pinned_source_blobs"] == 2
    assert checked["reviewed_intervening_paths"] == []


def test_preflight_rejects_untracked_r4r7_byte_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, base = init_repo(tmp_path, monkeypatch)
    g(root, "checkout", "-qb", "develop")
    fake_source = root / "phase165_r52_r9_shared_math.py"
    fake_source.write_text("no public R4R7 provider", encoding="utf-8")
    commit(root, "committed source")
    monkeypatch.setattr(audit, "BASE_HEAD", g(root, "rev-parse", "HEAD"))
    p = root / audit.PRIOR_PACKAGE / "rule.py"
    p.parent.mkdir(parents=True)
    p.write_text("tampered code", encoding="utf-8")
    monkeypatch.setattr(audit, "PINNED_BLOBS", {
        "phase165_r52_r9_shared_math.py": g(root, "rev-parse", "HEAD:phase165_r52_r9_shared_math.py"),
        audit.PRIOR_PACKAGE + "/rule.py": "0" * 40,
    })
    with pytest.raises(RuntimeError, match="R4R8_PINNED_SOURCE_BLOB_DRIFT"):
        audit.preflight(root)
```

## run.ps1（全文）

```powershell
param(
    [switch] $DryRun,
    [string] $R4R7Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $tests = @(
        'phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_audit.py',
        'phase175_r4r6_prop25_eq58_source_frontier/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R8 focused pytest failed' }
    Write-Output 'PHASE175_R4R8_FOCUSED_PYTEST=PASS'

    $command = @('-B', '-m', 'phase175_r4r8_signed_delta_kernel_frontier.audit', '--root', $root)
    if ($DryRun) { $command += '--dry-run' }
    if ($R4R7Report -ne '') { $command += @('--r4r7-report', $R4R7Report) }
    & python @command
    $exitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R8_EXIT_CODE=$exitCode"
    if ($exitCode -ne 0) { exit $exitCode }
    exit 0
} finally {
    Pop-Location
}
```

