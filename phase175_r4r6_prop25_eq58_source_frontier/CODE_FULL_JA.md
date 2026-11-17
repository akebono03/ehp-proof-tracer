# Phase 175 R4R6R2 — 変更コード全文

以下はすべて追加・置換単位を省略せず示す。変更していない関数・クラスは ZIP 内の既存ソースに保持する。

## 1. audit.py の変更後 import 全文

```python
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
```

## 2. 監査定数（配置位置：既存 PACKAGE/PRIOR_GATE 付近）

```python
PACKAGE = "phase175_r4r6_prop25_eq58_source_frontier"
PRIOR_PACKAGE = "phase175_r4r5r3_public_order_zero"
PRIOR_GATE = "PASS_R4R5R3_SHARED_PROVIDER_CONNECTED_NOT_COMPLETE"
# These describe the *historical R4R5R3 source guard*, not the later R4R6 HEAD.
PRIOR_REVIEWED_BASE_HEAD = "2789fb6297efaa35962695b95300063feb6e2ea2"
PRIOR_CHANGED_PREFIX = "phase175_r4r5_eta7_annihilator_isolated/"
PRIOR_PRODUCTION_BLOB = "ee1efa2d91df479168b7b964d24e814e0f516449"
PRIOR_RULE_SHA256 = "228a856bb4aa535edf4243885dee8472b8789c7d85c3507fc5eb1aace8a42bcd"
DRY_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_DRYRUN"
FINAL_GATE = "PASS_R4R6_PROP25_EQ58_SOURCE_FRONTIER_RECORDED_NOT_PUBLIC"
REVIEWED_HEADS = (
    "8d8c1eaaeffed2bc798c2ed19c8fe97c8e2ca5fc",
    "c48fdc307ba67a5e21b0ef49d57953468f7b47e2",
)
PINNED_BLOBS = {
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "df4e0f834e9bc321f338ec10b363c79d82623457",
    "phase175_r4r4_pi95_premise_frontier/audit.py": "0a9fbbd1c3262dfc46ec8f6e8a819eb5876742fc",
    "phase175_r4r5r3_public_order_zero/provider.py": "9a736418a2f191cfe485e3777c8bbb2143f2a9f3",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
}
```

## 3. validate_prior() 全文および新規 validate_prior_history() 全文

配置位置：`find_real_prior()` の直後、既存 `section()` の直前。

```python
def validate_prior(data: object) -> dict[str, object]:
    """Validate the real R4R5R3 report against its historical producer.

    R4R5R3 ran *before* the public-provider change was committed, so its
    reviewed_head must not be compared to the later R4R6 checkout HEADs.
    The independent Git history and blob checks run in validate_prior_history.
    """
    if not isinstance(data, dict):
        raise RuntimeError("R4R6_PRIOR_INVALID")
    expected = {
        "phase": "175-R4R5R3",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "connected_previously_isolated_general_rules": 1,
        "public_pi95_complete": False,
        "full_pytest_executed": False,
    }
    if any(data.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R6_PRIOR_GATE_OR_SCOPE_INVALID")

    source_guard = data.get("source_guard")
    general = data.get("general_rule")
    integration = data.get("real_integration_pytest")
    if not isinstance(source_guard, dict):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: source_guard not a dict")
    reviewed_head = source_guard.get("reviewed_head")
    paths = source_guard.get("reviewed_intervening_paths")
    if (not isinstance(reviewed_head, str)
            or len(reviewed_head) != 40
            or reviewed_head == "0" * 40
            or any(c not in "0123456789abcdef" for c in reviewed_head)
            or source_guard.get("reviewed_base_head") != PRIOR_REVIEWED_BASE_HEAD
            or source_guard.get("production_blob") != PRIOR_PRODUCTION_BLOB
            or source_guard.get("isolated_rule_sha256") != PRIOR_RULE_SHA256
            or not isinstance(paths, list)
            or any(not isinstance(path, str)
                   or not path.startswith(PRIOR_CHANGED_PREFIX)
                   or ".." in path.split("/")
                   or path == PRIOR_CHANGED_PREFIX
                   for path in paths)
            or paths != sorted(set(paths))):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: historical source guard")
    if (not isinstance(general, dict)
            or general.get("public_provider_proposals_with_verified_parent") != 3
            or general.get("source_groups") != ["pi_8^7", "pi_8^4", "pi_8^4"]
            or general.get("new_given") != 0
            or general.get("previous_proof_search_executed") is not False
            or general.get("target_pi95_completed") is not False
            or not isinstance(integration, dict)
            or integration.get("exit_code") != 0):
        raise RuntimeError("R4R6_PRIOR_EVIDENCE_INVALID: proof/provider replay boundary")
    return {
        "r4r5r3_head": reviewed_head,
        "r4r5r3_base_head": PRIOR_REVIEWED_BASE_HEAD,
        "verified_provider_examples": 3,
        "earlier_proof_search_rerun": False,
        "prior_report_is_not_mathematical_proof": True,
    }


def validate_prior_history(root: Path, source_guard: dict[str, object]) -> dict[str, object]:
    """Revalidate the exact earlier Git range recorded by R4R5R3.

    This cannot be replaced by a check against the present R4R6 HEAD:
    its full provider-wiring commit was created *after* the prior report.
    """
    reviewed_head = str(source_guard["reviewed_head"])
    current_head = git(root, "rev-parse", "HEAD")
    for ancestor, descendant in (
        (PRIOR_REVIEWED_BASE_HEAD, reviewed_head),
        (reviewed_head, current_head),
    ):
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=root, capture_output=True, text=True, check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "R4R6_PRIOR_HISTORY_INVALID: unreviewed ancestor "
                + ancestor + " -> " + descendant
            )
    actual_changed_paths = sorted(set(git(
        root, "diff", "--name-only", PRIOR_REVIEWED_BASE_HEAD, reviewed_head,
    ).splitlines()))
    recorded_changed_paths = source_guard["reviewed_intervening_paths"]
    if actual_changed_paths != recorded_changed_paths:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: changed paths differ")
    if any(not path.startswith(PRIOR_CHANGED_PREFIX)
           for path in actual_changed_paths):
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: unexpected changed file")
    if git(root, "rev-parse", reviewed_head + ":phase165_r52_r9_shared_math.py") != PRIOR_PRODUCTION_BLOB:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: prior production blob drift")
    rule_path = root / PRIOR_CHANGED_PREFIX / "rule.py"
    if not rule_path.is_file() or hashlib.sha256(rule_path.read_bytes()).hexdigest() != PRIOR_RULE_SHA256:
        raise RuntimeError("R4R6_PRIOR_HISTORY_INVALID: isolated inference rule drift")
    return {
        "historical_reviewed_head": reviewed_head,
        "historical_reviewed_base_head": PRIOR_REVIEWED_BASE_HEAD,
        "current_head": current_head,
        "changed_paths": actual_changed_paths,
        "historical_production_blob_checked": True,
        "historical_rule_sha256_checked": True,
    }
```

## 4. run() 全文

配置位置は既存 `report_folder()` の直後、`main()` の直前（置換）。

```python
def run(root: Path, *, dry_run: bool, prior_path: Path | None) -> int:
    output = report_folder()
    result: dict[str, object] = {
        "phase": "175-R4R6",
        "mode": "READ_ONLY_SOURCE_TYPE_BOUNDARY_AUDIT",
        "dry_run": dry_run,
        "gate": "FAIL_R4R6_PROP25_EQ58_SOURCE_FRONTIER",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    try:
        result["preflight"] = preflight(root)
        found = find_real_prior(prior_path)
        result["prior_report"] = str(found)
        prior_data = json.loads(found.read_text(encoding="utf-8"))
        result["prior_evidence"] = validate_prior(prior_data)
        result["prior_history"] = validate_prior_history(root, prior_data["source_guard"])
        result["source_evidence"] = source_evidence(
            (root / "sources/toda/Toda_02_2.tex").read_text(encoding="utf-8"),
            (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8"),
        )
        result["typed_frontier"] = typed_frontier()
        result["order_and_implementation_boundary"] = order_two_and_boundaries(root)
        result["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R4R6 — Proposition 2.5 / (5.8) 出典・型・境界監査",
        "", "Gate: `" + str(result["gate"]) + "`", "",
        "Toda Proposition 2.5 の m=4, i=8, j=9 は j < 3m−1 を満たす。",
        "符号 ± を保存し、2η₇=0 と π₈⁴ の位数2成分を用いる整理を記録する。",
        "ここでは ProofStep を生成せず、(5.8) の直接 GIVEN 化もしない。",
        "π₉⁵ は generic-partial-proof のまま。", "",
        "新規 GIVEN: 0 / 新規数学規則: 0 / 全体 pytest: 未実施", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("PHASE175_R4R6_HEAD=" + str(result.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R6_PRIOR_HISTORICAL_HEAD=" + str(result.get("prior_history", {}).get("historical_reviewed_head", "UNVERIFIED")))
    print("PHASE175_R4R6_NEW_GIVEN=0")
    print("PHASE175_R4R6_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R6_PRODUCTION_CHANGES=0")
    print("PHASE175_R4R6_PI95=NOT_COMPLETE")
    print("PHASE175_R4R6_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R6_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R6_GATE=" + str(result["gate"]))
    if "error" in result:
        print("PHASE175_R4R6_ERROR=" + str(result["error"]))
        return 1
    return 0
```

## 5. tests/test_audit.py の変更後 import 全文

```python
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import subprocess

import pytest

from phase175_r4r6_prop25_eq58_source_frontier import audit
```

## 6. テスト fixture 関数 prior_fixture() 全文

配置位置：既存同名関数を置換。

```python
def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R5R3", "gate": audit.PRIOR_GATE,
        "dry_run": False, "new_given": 0, "new_mathematical_rules": 0,
        "public_pi95_complete": False, "full_pytest_executed": False,
        "connected_previously_isolated_general_rules": 1,
        "source_guard": {
            "reviewed_head": audit.PRIOR_REVIEWED_BASE_HEAD,
            "reviewed_base_head": audit.PRIOR_REVIEWED_BASE_HEAD,
            "reviewed_intervening_paths": [],
            "production_blob": audit.PRIOR_PRODUCTION_BLOB,
            "isolated_rule_sha256": audit.PRIOR_RULE_SHA256,
        },
        "general_rule": {
            "public_provider_proposals_with_verified_parent": 3,
            "source_groups": ["pi_8^7", "pi_8^4", "pi_8^4"],
            "new_given": 0, "previous_proof_search_executed": False,
            "target_pi95_completed": False,
        },
        "real_integration_pytest": {"exit_code": 0},
    }
```

## 7. テスト関数の追加（全文）

配置位置：`tests/test_audit.py` の末尾。

```python
def test_historical_source_head_not_forced_to_later_checkout_head() -> None:
    record = prior_fixture()
    assert record["source_guard"]["reviewed_head"] not in audit.REVIEWED_HEADS
    assert audit.validate_prior(record)["r4r5r3_head"] == audit.PRIOR_REVIEWED_BASE_HEAD


@pytest.mark.parametrize("field,bad", [
    ("reviewed_base_head", "0" * 40),
    ("production_blob", "0" * 40),
    ("isolated_rule_sha256", "0" * 64),
    ("reviewed_intervening_paths", ["proof.py"]),
    ("reviewed_intervening_paths", ["phase175_r4r5_eta7_annihilator_isolated/../../proof.py"]),
])
def test_historical_source_guard_tampering_rejected(field: str, bad: object) -> None:
    record = prior_fixture()
    record["source_guard"][field] = bad
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_EVIDENCE_INVALID"):
        audit.validate_prior(record)


def test_historical_genuine_commit_range_is_accepted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=tmp_path, text=True,
                              capture_output=True, check=True).stdout.strip()

    def commit(message: str) -> str:
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", message)
        return git("rev-parse", "HEAD")

    git("init", "-q")
    source_file = tmp_path / "phase165_r52_r9_shared_math.py"
    source_file.write_text("original shared provider\n", encoding="utf-8")
    base = commit("pre R4R5R2")
    monkeypatch.setattr(audit, "PRIOR_REVIEWED_BASE_HEAD", base)
    original_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    monkeypatch.setattr(audit, "PRIOR_PRODUCTION_BLOB", original_blob)

    rule_path = tmp_path / "phase175_r4r5_eta7_annihilator_isolated" / "rule.py"
    rule_path.parent.mkdir(parents=True)
    rule_path.write_bytes(b"source guarded order zero inference\n")
    import hashlib
    rule_hash = hashlib.sha256(rule_path.read_bytes()).hexdigest()
    monkeypatch.setattr(audit, "PRIOR_RULE_SHA256", rule_hash)
    historical_head = commit("R4R5R2 committed")
    source_file.write_text("new shared provider\n", encoding="utf-8")
    commit("R4R5R3 production wiring committed")
    record = prior_fixture()
    record["source_guard"].update({
        "reviewed_head": historical_head,
        "reviewed_base_head": base,
        "reviewed_intervening_paths": ["phase175_r4r5_eta7_annihilator_isolated/rule.py"],
        "production_blob": original_blob,
        "isolated_rule_sha256": rule_hash,
    })
    assert audit.validate_prior(record)["r4r5r3_head"] == historical_head
    checked = audit.validate_prior_history(tmp_path, record["source_guard"])
    assert checked["historical_reviewed_head"] == historical_head
    assert checked["historical_production_blob_checked"] is True

    forged = deepcopy(record)
    forged["source_guard"]["reviewed_intervening_paths"] = []
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, forged["source_guard"])

    # The actual rule bytes are a separately verified source of the prior audit.
    rule_path.write_bytes(b"tampered source\n")
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, record["source_guard"])


def test_historical_unrelated_commit_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=tmp_path, text=True,
                              capture_output=True, check=True).stdout.strip()
    def commit(message: str) -> str:
        git("add", ".")
        git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", message)
        return git("rev-parse", "HEAD")

    git("init", "-q")
    source = tmp_path / "phase165_r52_r9_shared_math.py"
    source.write_text("original\n", encoding="utf-8")
    base = commit("original")
    monkeypatch.setattr(audit, "PRIOR_REVIEWED_BASE_HEAD", base)
    monkeypatch.setattr(audit, "PRIOR_PRODUCTION_BLOB", git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py"))
    (tmp_path / "proof.py").write_text("unrelated change\n", encoding="utf-8")
    unreviewed_head = commit("unrelated")
    record = prior_fixture()
    record["source_guard"].update({
        "reviewed_head": unreviewed_head,
        "reviewed_base_head": base,
        "reviewed_intervening_paths": [],
    })
    assert audit.validate_prior(record)["verified_provider_examples"] == 3
    with pytest.raises(RuntimeError, match="R4R6_PRIOR_HISTORY_INVALID"):
        audit.validate_prior_history(tmp_path, record["source_guard"])
```

## 8. 変更のない箇所

- `run.ps1` の内容は従来版と同一。
- `find_real_prior()` の R4R6R1 診断処理はそのまま。
- `source_evidence()`、`typed_frontier()`、`order_two_and_boundaries()` は変更しない。
- 本番コード、共有 Proof Search、GIVEN / ProofStep / Renderer は変更しない。
