# Phase 174 R3-R6-R2R1 — 変更・追加コード全文

旧監査を新しい数学的証明へ合わせるために変更する2関数を、変更後の全文で掲載する。
既存ファイルの先頭 import は変更しない。新しい import は変更した関数の中に全文掲載している。
以下の関数は本実行後に `output/` にも実ファイルから抽出して保存される。

## 既存関数 `phase174_r3_r4_public_delta_connection/audit.py: inspect_public_provider`

```python
def inspect_public_provider() -> dict[str, object]:
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prefer_universal_prop42_derivation,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r3_recursive_search import reconstruct_registered_goal
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        attach_earlier_verified_lemma54,
    )
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase174_r3_r3_injective_delta_zero.audit import proof_has_cited_leaf
    from phase174_r3_r3_injective_delta_zero.rule import delta_e_injectivity_inputs
    from proof import ProofRule
    from toda_rules import TodaDeltaZeroStatement

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Expected a single registered typed pi_8^5 target")
    target = goals[0]
    citation = resolve_specialized_goal_citing_id(bridge, target)
    if citation is None:
        raise ValueError("No actual pi_8^5 publication position")
    amended = attach_earlier_verified_lemma54(bridge, citation)
    if amended is bridge:
        raise ValueError("Verified Lemma 5.4 must precede this proof target")
    bridge = amended
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citation,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    zero_delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    if zero_delta in available:
        raise ValueError("Zero Delta has been promoted to a source GIVEN")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposals = provider(zero_delta)
    integrated = tuple(p for p in proposals if getattr(p.rule,"name",None) == RULE_NAME)
    if len(integrated) != 1:
        raise ValueError("The general Delta rule is not uniquely connected to the public provider")
    if integrated[0].subgoals != delta_e_injectivity_inputs(zero_delta):
        raise ValueError("Public subgoals diverge from the reviewed EHP inference")
    # Preserve First Successful Proof Search. An older valid route can win
    # before the new proposal; verify the new rule with a diagnostic root filter.
    # Subsidiary goals still use the actual citation-screened public provider.
    def new_rule_for_root(query: object):
        options = provider(query)
        if query != zero_delta:
            return options
        return tuple(
            proposal for proposal in options
            if getattr(proposal.rule, "name", None) == RULE_NAME
        )

    step = reconstruct_registered_goal(
        zero_delta, screened, citation, new_rule_for_root,
        lookup_mode="typed_reference",
    )
    if (
        step.rule is not ProofRule.INFERENCE or step.conclusion != zero_delta
        or getattr(step.inference_rule, "name", None) != RULE_NAME
        or len(step.premises) != 2
        or any(prior.rule is not ProofRule.INFERENCE for prior in step.premises)
        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())
        or not proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())
        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())
    ):
        raise ValueError("Connected rule lacks real public source ancestry")

    selected = reconstruct_registered_goal(
        zero_delta, screened, citation, provider, lookup_mode="typed_reference",
    )
    if selected.rule is not ProofRule.INFERENCE or selected.conclusion != zero_delta:
        raise ValueError("Ordinary public provider cannot reconstruct Delta zero")
    return {
        "root_goal_type": type(target).__name__,
        "zero_delta_goal_type": type(zero_delta).__name__,
        "publication_citing_assertion_id": citation,
        "screened_source_count": len(available),
        "new_public_provider_proposals": len(integrated),
        "new_rule_name": RULE_NAME,
        "ordinary_first_success_rule": getattr(selected.inference_rule, "name", None),
        "premise_types": [type(x.conclusion).__name__ for x in step.premises],
        "premises_both_inferred": True,
        "source_ancestry_checked": True,
        "delta_zero_publicly_reconstructed": True,
        "named_group_goal_complete": False,
        "new_given": 0,
    }
```

## 既存テスト関数 `phase174_r3_r4_public_delta_connection/tests/test_connection.py: test_r3r4_real_production_file_has_only_reviewed_wiring`

```python
def test_r3r4_real_production_file_has_only_reviewed_wiring():
    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared
    from phase174_r3_r6_source_extension.patch import connect_shared
    from phase174_r3_r6_r2_prop44_lemma54.patch import normalize, patch_shared
    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')
    current = Path('phase165_r52_r9_shared_math.py').read_bytes()
    r3r4 = replace_provider_call(old)
    r3r5 = insert_shared(r3r4)
    r3r6 = connect_shared(r3r5)
    new_source = patch_shared(normalize(r3r6.decode('utf-8'))).encode('utf-8')
    assert normalize(current.decode('utf-8')) in tuple(
        normalize(candidate.decode('utf-8'))
        for candidate in (r3r4, r3r5, r3r6, new_source)
    )
    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1
```

## 新規ファイル（すべて本パッケージディレクトリ直下、テストだけ `tests/`）

### patch.py

```python
"""Fail-closed two-file follow-up to the reviewed R3-R6-R2 implementation.

Only the old R3-R4 audit and its cumulative test are updated. Both are
checked against the R3-R6-R2 revision and the exact reviewed Git blobs.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import subprocess
from pathlib import Path

from phase174_r3_r6_r2_prop44_lemma54.patch import (
    BLOBS as PREVIOUS_BLOBS,
    HEAD,
    TRANSFORM as PREVIOUS_TRANSFORM,
    normalize,
    replace_one,
    full_unit,
)

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
AUDIT = "phase174_r3_r4_public_delta_connection/audit.py"
AUDIT_BLOB = "d78cb903a236f210f05be05a198fd9b17055924e"


def git_bytes(*args: str) -> bytes:
    return subprocess.run(("git", *args), cwd=ROOT, check=True,
                          capture_output=True).stdout


def blob_hash(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content
    ).hexdigest()


def patch_cumulative_test(text: str) -> str:
    """Preserve byte-exact lineage checks; normalize only checkout line endings."""
    text = replace_one(
        text,
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n",
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import normalize, patch_shared\n",
        label="R3-R4 cumulative test's reviewed import",
    )
    before = (
        "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
        "    assert current in (r3r4, r3r5, r3r6, new_source)\n"
    )
    after = (
        "    new_source = patch_shared(normalize(r3r6.decode('utf-8'))).encode('utf-8')\n"
        "    assert normalize(current.decode('utf-8')) in tuple(\n"
        "        normalize(candidate.decode('utf-8'))\n"
        "        for candidate in (r3r4, r3r5, r3r6, new_source)\n"
        "    )\n"
    )
    text = replace_one(text, before, after, label="R3-R4 reviewed LF/CRLF replay")
    ast.parse(text, filename=TEST)
    return text


def patch_delta_audit(text: str) -> str:
    """Use the same earlier verified Lemma 5.4 source as the completed root."""
    text = replace_one(
        text,
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n",
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
        "    from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.source import (\n"
        "        attach_earlier_verified_lemma54,\n"
        "    )\n",
        label="R3-R4 delta audit independently cited lemma imports",
    )
    before = (
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    screened = screen_shared_proof_context(\n"
    )
    after = (
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    amended = attach_earlier_verified_lemma54(bridge, citation)\n"
        "    if amended is bridge:\n"
        "        raise ValueError(\"Verified Lemma 5.4 must precede this proof target\")\n"
        "    bridge = amended\n"
        "    screened = screen_shared_proof_context(\n"
    )
    text = replace_one(text, before, after, label="R3-R4 source-first public context")
    text = replace_one(
        text,
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n",
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n",
        label="R3-R4 independently inferred lemma ancestry",
    )
    ast.parse(text, filename=AUDIT)
    return text


def reviewed_changes() -> dict[str, tuple[bytes, bytes]]:
    """Check the previous 9-file patch was installed and no tracked changes are staged.

    This supports re-running this follow-up but refuses arbitrary edits to
    other R3-R6-R2 outputs and refuses unexpected edits in its own two files.
    """
    branch = git_bytes("branch", "--show-current").decode("utf-8").strip()
    local = git_bytes("rev-parse", "HEAD").decode("ascii").strip()
    remote = git_bytes("ls-remote", "origin", "refs/heads/develop").decode("ascii").split()
    if branch != "develop" or local != HEAD or remote != [HEAD, "refs/heads/develop"]:
        raise ValueError("Unreviewed R3-R6-R2 HEAD or remote develop")
    if git_bytes("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes must be reviewed")

    for path, transform in PREVIOUS_TRANSFORM.items():
        committed = git_bytes("show", "HEAD:" + path)
        if blob_hash(committed) != PREVIOUS_BLOBS[path]:
            raise ValueError("Reviewed R3-R6-R2 Git blob changed: " + path)
        expected = transform(normalize(committed.decode("utf-8-sig")))
        actual = normalize((ROOT / path).read_text(encoding="utf-8-sig"))
        if path == TEST:
            authorized = (expected, patch_cumulative_test(expected))
        else:
            authorized = (expected,)
        if actual not in authorized:
            raise ValueError("Unreviewed R3-R6-R2 working file: " + path)

    committed = git_bytes("show", "HEAD:" + AUDIT)
    if blob_hash(committed) != AUDIT_BLOB:
        raise ValueError("Reviewed historical Delta audit Git blob changed")
    old_audit = normalize(committed.decode("utf-8-sig"))
    new_audit = patch_delta_audit(old_audit)

    original_test = git_bytes("show", "HEAD:" + TEST)
    old_test = PREVIOUS_TRANSFORM[TEST](normalize(original_test.decode("utf-8-sig")))
    new_test = patch_cumulative_test(old_test)
    current_audit = normalize((ROOT / AUDIT).read_text(encoding="utf-8-sig"))
    current_test = normalize((ROOT / TEST).read_text(encoding="utf-8-sig"))
    if current_audit not in (old_audit, new_audit):
        raise ValueError("Unreviewed R3-R4 audit changes")
    if current_test not in (old_test, new_test):
        raise ValueError("Unreviewed R3-R4 cumulative test changes")
    return {
        AUDIT: ((ROOT / AUDIT).read_bytes(), new_audit.encode("utf-8")),
        TEST: ((ROOT / TEST).read_bytes(), new_test.encode("utf-8")),
    }


def apply(*, dry_run: bool) -> None:
    changes = reviewed_changes()
    print("PHASE174_R3R6R2R1_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R2R1_REVIEWED_HEAD=" + HEAD)
    print("PHASE174_R3R6R2R1_REVIEWED_PRIOR_FILES=" + str(len(PREVIOUS_BLOBS)))
    print("PHASE174_R3R6R2R1_TARGET_FILES=" + str(len(changes)))
    if dry_run:
        print("PHASE174_R3R6R2R1_DRY_RUN_GATE=PASS")
        return
    snapshots = {path: prior for path, (prior, _) in changes.items()}
    try:
        for path, (_, new) in changes.items():
            (ROOT / path).write_bytes(new)
        output = PACKAGE / "output"
        output.mkdir(parents=True, exist_ok=True)
        for path, (_, new) in changes.items():
            text = new.decode("utf-8")
            (output / (path.replace("/", "__") + ".FULL.py")).write_text(
                text, encoding="utf-8",
            )
            fn = "inspect_public_provider" if path == AUDIT else "test_r3r4_real_production_file_has_only_reviewed_wiring"
            (output / (fn + "_FULL.py")).write_text(full_unit(text, fn), encoding="utf-8")
        print("PHASE174_R3R6R2R1_PATCH=PASS")
        print("PHASE174_R3R6R2R1_FULL_REPLACEMENTS=" + str(output))
    except BaseException:
        for path, old in snapshots.items():
            (ROOT / path).write_bytes(old)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apply(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### audit.py

```python
"""Run the historical Delta proof and new completed group proof on the same source path."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r4_public_delta_connection.audit import inspect_public_provider
from phase174_r3_r6_r2_prop44_lemma54.audit import inspect as inspect_group_root
from phase174_r3_r6_r2r1_regression_fix.patch import reviewed_changes


def main() -> int:
    reviewed_changes()
    delta = inspect_public_provider()
    if (delta.get("delta_zero_publicly_reconstructed") is not True
            or delta.get("source_ancestry_checked") is not True
            or delta.get("premises_both_inferred") is not True
            or delta.get("new_given") != 0):
        raise ValueError("EHP Delta source and inferred ancestry were not retained")
    root = inspect_group_root()
    if (root.get("root_status") != "complete"
            or root.get("hopf_invariant_condition_inferred") is not True
            or root.get("lemma54_is_root_ancestor") is not True
            or root.get("preprop44_is_root_ancestor") is not False
            or root.get("previous_pi6_4_still_complete") is not True
            or root.get("new_group_given") != 0):
        raise ValueError("The corrected public pi_8^5 proof regressed")
    output = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    output = output / "EHPProofTracerAudit" / "phase174_r3_r6_r2r1"
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "174-R3-R6-R2R1",
        "historical_delta": delta,
        "root_status": root["root_status"],
        "root_steps": root["root_proven_steps"],
        "lemma54_root_ancestor": root["lemma54_is_root_ancestor"],
        "prelude_not_root_ancestor": not root["preprop44_is_root_ancestor"],
        "previous_pi6_4_still_complete": root["previous_pi6_4_still_complete"],
        "full_pytest_performed": False,
    }
    destination = output / "audit.json"
    destination.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PHASE174_R3R6R2R1_DELTA_RECONSTRUCTED=True")
    print("PHASE174_R3R6R2R1_LEMMA54_DELTA_ANCESTRY=True")
    print("PHASE174_R3R6R2R1_PI85_COMPLETE=True")
    print("PHASE174_R3R6R2R1_PI64_PRESERVED=True")
    print("PHASE174_R3R6R2R1_PROVEN_STEPS=" + str(root["root_proven_steps"]))
    print("PHASE174_R3R6R2R1_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6R2R1_REPORT=" + str(destination))
    print("PHASE174_R3R6R2R1_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### run.ps1

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

if (-not (Test-Path '.\phase174_r3_r6_r2_prop44_lemma54\source.py')) {
    throw 'Phase 174 R3-R6-R2 must be extracted and installed before this correction'
}

python -m phase174_r3_r6_r2r1_regression_fix.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2R1 source/HEAD guard failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R3R6R2R1_DRY_RUN_GATE=PASS'
    exit 0
}

python -m phase174_r3_r6_r2r1_regression_fix.patch
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2R1 minimal patch failed' }

python -m phase174_r3_r6_r2r1_regression_fix.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2R1 source ancestry audit failed' }

python -m pytest -q -p no:cacheprovider `
    phase174_r3_r6_r2r1_regression_fix/tests/test_patch.py `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_patch.py `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
    phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py `
    phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py `
    phase173_r4_r1_lemma54_source_bridge/tests/test_source.py `
    phase174_r3_r6_source_extension/tests/test_source.py `
    phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
    phase174_r3_r5_preflight/tests/test_audit.py `
    phase174_r3_r4_public_delta_connection/tests/test_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2R1 focused pytest failed' }

Write-Output 'PHASE174_R3R6R2R1_FOCUSED_PYTEST=PASS'
Write-Output 'PHASE174_R3R6R2R1_FULL_PYTEST_NOT_RUN=True'
Write-Output 'PHASE174_R3R6R2R1_GATE=PASS'
```

### tests/test_patch.py

```python
"""Pure tests for the two reviewed replacements, without a repository checkout."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_r2r1_regression_fix.patch import (
    normalize,
    patch_cumulative_test,
    patch_delta_audit,
)


def test_cumulative_lineage_replay_accepts_crlf_and_preserves_git_blob_guard() -> None:
    original = (
        "from pathlib import Path\n\n"
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
        "    old = b'old'\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = old\n"
        "    r3r5 = old\n"
        "    r3r6 = old\n"
        "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
        "    assert current in (r3r4, r3r5, r3r6, new_source)\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
    )
    updated = patch_cumulative_test(original)
    assert "patch_shared(normalize(r3r6.decode('utf-8')))" in updated
    assert "normalize(current.decode('utf-8'))" in updated
    assert "git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'" in updated
    ast.parse(updated)
    assert normalize(updated.replace("\n", "\r\n")) == updated


def test_delta_audit_screen_reuses_verified_lemma_and_checks_both_ancestors() -> None:
    source = (
        "def inspect_public_provider():\n"
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
        "    citation = 8800\n"
        "    bridge = original_bridge\n"
        "    if citation is None:\n"
        "        raise ValueError(\"No actual pi_8^5 publication position\")\n"
        "    screened = screen_shared_proof_context(\n"
        "        bridge, goal=target, citing_assertion_id=citation,\n"
        "    )\n"
        "    if (\n"
        "        step.rule is not ProofRule.INFERENCE\n"
        "        or not proof_has_cited_leaf(step.premises[0], TodaProp44UniversalStatement())\n"
        "        or not proof_has_cited_leaf(step.premises[1], TodaProp42GeneralExactnessStatement())\n"
        "    ):\n"
        "        raise ValueError('missing')\n"
    )
    updated = patch_delta_audit(source)
    assert "attach_earlier_verified_lemma54(bridge, citation)" in updated
    assert "proof_has_cited_leaf(step.premises[0], TodaLemma54TypedSource())" in updated
    assert "if amended is bridge:" in updated
    ast.parse(updated)


def test_changed_ancestry_guard_rejects_missing_expected_line() -> None:
    source = (
        "def inspect_public_provider():\n"
        "    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement\n"
    )
    with pytest.raises(ValueError, match="public context"):
        patch_delta_audit(source)


def test_lineage_test_rejects_unreviewed_prior_replay() -> None:
    source = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
        "    return None\n"
    )
    with pytest.raises(ValueError, match="replay"):
        patch_cumulative_test(source)
```

### __init__.py

```python
"""Two-file historical audit and CRLF regression correction for Phase 174."""
```

### tests/__init__.py

```python
"""Focused pure patch regression checks."""
```
