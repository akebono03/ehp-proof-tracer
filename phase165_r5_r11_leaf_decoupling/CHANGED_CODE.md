# Phase 165 R5-R11 全コード

新規モジュールはプロジェクト直下に追加。既存モジュールの変更は `_phase162_ehp_leaves` の互換 import と Web replay の import 元のみ。

## `phase162_ehp_leaf_inputs.py`（全文）

```python
"""Shared historical EHP leaf construction, independent of Narrative rendering.

This module preserves Phase 162 leaf semantics; it does not certify the
underlying historical GIVEN facts or change the Phase 165 search.
"""

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase162_reference_boundary import cite_verified_fixed_statement
from phase164_r8_proofstep_factory import create_legacy_given_proof_step
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule
from toda_rules import TodaProp42ExactnessStatement


def _phase162_ehp_leaves():
    """Reuse the original independent EHP input leaves, not an iso conclusion."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = cite_verified_fixed_statement(
        build_phase58_representative_result()["final_hopf_step"],
        reference_locator="(5.3)",
        component_key="nu_prime_hopf_relation",
        expected_conclusion=build_phase58_representative_result()["expected_final_hopf"],
    )
    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        create_legacy_given_proof_step(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    return prop51, hopf_eta5, exactness

```

## `install.py`（全文）

```python
"""Guarded, reversible, minimal Phase 165 R5-R11 migration."""
import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OLD = ROOT / "phase162_web_narrative_integration.py"
REPLAY = ROOT / "phase162_pi5_3_web_replay.py"
NEW = ROOT / "phase162_ehp_leaf_inputs.py"
BACKUP = ROOT / ".phase165_r5_r11_backup"
OLD_IMPORT = "from phase162_web_narrative_integration import _phase162_ehp_leaves"
NEW_IMPORT = "from phase162_ehp_leaf_inputs import _phase162_ehp_leaves"


def read_file(path):
    data = path.read_bytes()
    return data.decode("utf-8-sig"), data.startswith(b"\xef\xbb\xbf"), "\r\n" if b"\r\n" in data else "\n"


def write_file(path, content, bom, newline):
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + normalized.replace("\n", newline).encode("utf-8"))


def install():
    if BACKUP.exists():
        raise RuntimeError("Backup exists. Refusing to overwrite: " + str(BACKUP))
    if NEW.exists():
        raise RuntimeError("New leaf module already exists: " + str(NEW))
    for path in (OLD, REPLAY):
        if not path.is_file():
            raise RuntimeError("Required file not found: " + str(path))
    old, old_bom, old_newline = read_file(OLD)
    replay, replay_bom, replay_newline = read_file(REPLAY)
    tree = ast.parse(old)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "_phase162_ehp_leaves"]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one existing EHP leaf function")
    node = matches[0]
    source_lines = old.splitlines(keepends=True)
    function_source = "".join(source_lines[node.lineno - 1:node.end_lineno]).replace("\r\n", "\n")
    template = (PACKAGE / "phase162_ehp_leaf_inputs.py").read_text(encoding="utf-8")
    new_func = template[template.index("def _phase162_ehp_leaves():"):]
    if ast.dump(ast.parse(function_source), include_attributes=False) != ast.dump(ast.parse(new_func), include_attributes=False):
        raise RuntimeError("Local leaf function differs from vetted source: no migration")
    if replay.count(OLD_IMPORT) != 1:
        raise RuntimeError("Expected one replay import, found " + str(replay.count(OLD_IMPORT)))
    # Preserve entire module outside this function. Replace with a compatibility alias.
    source_lines[node.lineno - 1:node.end_lineno] = [NEW_IMPORT + "\n"]
    changed_old = "".join(source_lines)
    changed_replay = replay.replace(OLD_IMPORT, NEW_IMPORT, 1)
    ast.parse(changed_old)
    ast.parse(changed_replay)
    BACKUP.mkdir()
    try:
        shutil.copy2(OLD, BACKUP / OLD.name)
        shutil.copy2(REPLAY, BACKUP / REPLAY.name)
        NEW.write_bytes((PACKAGE / "phase162_ehp_leaf_inputs.py").read_bytes())
        write_file(OLD, changed_old, old_bom, old_newline)
        write_file(REPLAY, changed_replay, replay_bom, replay_newline)
    except BaseException:
        restore()
        raise
    return {"status": "INSTALLED", "modified_files": [OLD.name, REPLAY.name], "added_file": NEW.name, "backup": BACKUP.name, "removed_legacy_renderer": False, "full_pytest_run": False}


def restore():
    for path in (OLD, REPLAY):
        backup = BACKUP / path.name
        if backup.is_file():
            shutil.copy2(backup, path)
    if NEW.exists():
        NEW.unlink()
    return {"status": "RESTORED"}


if __name__ == "__main__":
    print(json.dumps(install(), ensure_ascii=False, indent=2))

```

## `restore.py`（全文）

```python
from install import restore

if __name__ == "__main__":
    print(restore())

```

## `test_r5_r11.py`（全文）

```python
"""Narrow migration guarantees; independent from broken Phase 59 fixture."""

import ast
from pathlib import Path

import phase162_ehp_leaf_inputs as shared
import phase162_web_narrative_integration as historical
import phase162_pi5_3_web_replay as replay


def test_r5_r11_compatibility_alias_is_identical():
    assert historical._phase162_ehp_leaves is shared._phase162_ehp_leaves


def test_r5_r11_replay_uses_shared_leaf_object():
    assert replay._phase162_ehp_leaves is shared._phase162_ehp_leaves


def test_r5_r11_leaf_module_does_not_import_narrative():
    tree = ast.parse(Path(shared.__file__).read_text(encoding="utf-8-sig"))
    imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    assert "phase162_web_narrative_integration" not in imported
    assert "phase162_r3_narrative_connection" not in imported


def test_r5_r11_original_module_has_no_leaf_definition():
    tree = ast.parse(Path(historical.__file__).read_text(encoding="utf-8-sig"))
    assert not [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_phase162_ehp_leaves"]


def test_r5_r11_leaf_window_count_and_order(monkeypatch):
    sentinel = object()
    hopf = object()
    windows = []
    monkeypatch.setattr(shared, "build_phase55_representative_result", lambda: {"prop51_steps": (sentinel,)})
    monkeypatch.setattr(shared, "build_phase58_representative_result", lambda: {"final_hopf_step": hopf, "expected_final_hopf": object()})
    monkeypatch.setattr(shared, "cite_verified_fixed_statement", lambda *args, **kwargs: hopf)
    def record(*, conclusion, premises, rule):
        assert premises == ()
        assert rule is shared.ProofRule.GIVEN
        windows.append(conclusion.window)
        return conclusion
    monkeypatch.setattr(shared, "create_legacy_given_proof_step", record)
    first, second, exactness = shared._phase162_ehp_leaves()
    assert first is sentinel
    assert second is hopf
    assert len(exactness) == len(windows) == 4
    assert [w.middle_term.group_dimension for w in windows] == [5, 5, 6, 4]

```

## `run.ps1`（全文）

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python "$PSScriptRoot\install.py"
if ($LASTEXITCODE -ne 0) { throw 'R5-R11 installation aborted' }
$env:PYTHONPATH = $root
python -m pytest -q "$PSScriptRoot\test_r5_r11.py" "test_phase165_r52_r11_common_renderer.py" "test_phase165_r56_common_renderer.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Regression detected; restoring original modules'
    python "$PSScriptRoot\restore.py"
    throw 'R5-R11 regression; changes restored'
}
Write-Host 'R5-R11 targeted tests PASS; legacy Narrative retained; full pytest NOT run.'

```

## `phase162_pi5_3_web_replay.py`：変更後 import 部分（全文）

```python
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    reconstruct_phase162_pi5_3_group_goal,
)
from phase162_ehp_leaf_inputs import _phase162_ehp_leaves
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_match
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
)
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
```

`build_phase162_pi5_3_web_replay()` 自体は一切変更しない。

## `phase162_web_narrative_integration.py`：変更後 import 部分（全文）

以下が既存ファイル先頭の import 部分。元の関数定義位置は互換 import `from phase162_ehp_leaf_inputs import _phase162_ehp_leaves` に置き換える。

```python
from phase162_reference_boundary import cite_verified_fixed_statement
from phase164_r8_proofstep_factory import (
    create_legacy_given_proof_step,
    derive_inference_proof_step,
)
from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement
from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase162_r2_existing_proof_connection import (
    reconstruct_phase162_r2_from_existing_proofs,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import Relation, RelationType, apply_inference_match, find_inference_match
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
)
```

既存の先頭 import は変更せず、旧関数の位置に以下を追加する。

```python
from phase162_ehp_leaf_inputs import _phase162_ehp_leaves
```

互換 import はファイル途中に置くが、トップレベルで1回だけ実行される。既存関数本体は変更しない。
