# Phase 163 R4-R7 — 変更コード全文

## 変更対象

- 新規 `phase163_r4_r7_representative_bindings.py`（リポジトリ直下）。
- 新規 `tests/test_phase163_r4_r7_representative_bindings.py`（既存 tests ディレクトリ内）。
- ZIP 内 `run.ps1`（プロジェクトの既存ファイルの書換えなし）。

既存の import・クラス・関数・メソッドは変更しない。新規クラス `WitnessCandidate`、`BindingAttempt`、新規関数 `bind_representative_witnesses`、`representative_candidates`、`run_audit` を独立モジュールに追加する。既存 API の変更はない。

## 目的・完了条件

- Phase 58 の `(5.3)` の Toda bracket、Hopf 値、2 倍関係の実 ProofStep を読み出す。
- Phase 65 の Proposition 5.6 の $\pi_5^2$ の実 ProofStep を読み出す。
- R6 の既存検証経路で真正の引用境界を確認できたものだけを新スナップショットへ接続。
- GIVEN、未登録主張、検証失敗は昇格させず監査表へ残す。
- 全体 pytest と Backward Search 接続は今回実施しない。

注意：`cite_verified_fixed_statement` は既存 ancestry の内部整合性検証であり、文献原本の数学的真正性の独立検証ではない。したがって、構造化できた記録でも外部文献検証が完了したと主張しない。

## 実行する pytest

```powershell
python -m pytest -q tests/test_phase163_r4_r6_structured_binding.py tests/test_phase163_r4_r7_representative_bindings.py
```

## 次 Phase との境界

Definition の独立登録、全 Statement の移行、掲載順と証明完了時点の確定、Backward Search への接続は範囲外。

## 新規本体ファイル全文

```python
"""Phase 163 R4-R7: opt-in binding of real representative proof steps.

No witness is fabricated. Existing Phase 162 citation verification is required.
Unverified sources remain metadata-only. No search or renderer integration.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from phase162_reference_boundary import cite_verified_fixed_statement
from phase163_r4_r6_structured_binding import (
    FixedStatementBinding,
    bind_verified_fixed_statements,
)
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult, build_registry_bridge
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class WitnessCandidate:
    reference_locator: str
    component_key: str
    witness: ProofStep
    expected_conclusion: object
    source_description: str

    def __post_init__(self) -> None:
        if not self.reference_locator or not self.component_key:
            raise ValueError("reference and component must be nonempty")
        if not isinstance(self.witness, ProofStep):
            raise TypeError("witness must be ProofStep")
        if self.expected_conclusion != self.witness.conclusion:
            raise ValueError("expected conclusion and witness must match")


@dataclass(frozen=True)
class BindingAttempt:
    reference_locator: str
    component_key: str
    status: str
    detail: str


def bind_representative_witnesses(
    base: RegistryBridgeResult,
    candidates: tuple[WitnessCandidate, ...],
    *,
    citation_builder: Callable[..., ProofStep] = cite_verified_fixed_statement,
) -> tuple[RegistryBridgeResult, tuple[BindingAttempt, ...]]:
    """Bind individually verified citations; preserve failures without promoting them.

    Passing a builder is only for controlled focused tests. Production defaults to
    Phase 162's verified-ancestry citation constructor.
    """
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    accepted: list[FixedStatementBinding] = []
    attempts: list[BindingAttempt] = []
    seen: set[tuple[str, str]] = set()
    eligible = {
        r.assertion_id for r in base.records
        if r.source == "boundary" and r.status is MigrationStatus.METADATA_ONLY
    }
    for candidate in candidates:
        if not isinstance(candidate, WitnessCandidate):
            raise TypeError("candidates must contain WitnessCandidate")
        locator, component = candidate.reference_locator, candidate.component_key
        key = (locator, component)
        if key in seen:
            raise ValueError(f"duplicate candidate: {key}")
        seen.add(key)
        assertion_id = f"boundary:{locator}:{component}"
        if assertion_id not in eligible:
            attempts.append(BindingAttempt(locator, component, "NOT_REGISTERED", "No metadata-only boundary entry"))
            continue
        if candidate.witness.rule is ProofRule.GIVEN:
            attempts.append(BindingAttempt(locator, component, "GIVEN_UNVERIFIED", "GIVEN is not a derived proof and cannot be promoted"))
            continue
        try:
            citation = citation_builder(
                candidate.witness, locator, component, candidate.expected_conclusion
            )
            binding = FixedStatementBinding(
                reference_locator=locator,
                component_key=component,
                citation_step=citation,
                expected_conclusion=candidate.expected_conclusion,
            )
            # The R6 validation is authoritative even for a custom builder.
            bind_verified_fixed_statements(base, (binding,))
        except (ValueError, TypeError, KeyError) as exc:
            attempts.append(BindingAttempt(locator, component, "VERIFICATION_FAILED", f"{type(exc).__name__}: {exc}"))
            continue
        accepted.append(binding)
        attempts.append(BindingAttempt(locator, component, "STRUCTURED", "Existing citation boundary validated; external literary truth not independently established"))
    result = bind_verified_fixed_statements(base, tuple(accepted))
    return result, tuple(attempts)


def representative_candidates() -> tuple[WitnessCandidate, ...]:
    """Use existing project builders unchanged; do not construct substitute proofs."""
    from probes.probe_phase58_capabilities import build_phase58_representative_result
    from probes.probe_phase65_capabilities import build_phase65_representative_result

    five_three = build_phase58_representative_result()
    five_six = build_phase65_representative_result()
    return (
        WitnessCandidate(
            "(5.3)", "nu_prime_bracket_definition",
            five_three["bracket_membership_step"],
            five_three["bracket_membership_step"].conclusion,
            "Phase58 bracket membership GIVEN: not independently verified",
        ),
        WitnessCandidate(
            "(5.3)", "nu_prime_hopf_relation",
            five_three["final_hopf_step"], five_three["expected_final_hopf"],
            "Phase58 final_hopf_step",
        ),
        WitnessCandidate(
            "(5.3)", "nu_prime_double_relation",
            five_three["final_double_step"], five_three["expected_final_double"],
            "Phase58 final_double_step",
        ),
        WitnessCandidate(
            "Proposition 5.6", "pi5_2_group_relation",
            five_six["pi5_2_step"], five_six["pi5_2_step"].conclusion,
            "Phase65 pi5_2_step",
        ),
    )


def run_audit(output_dir: Path) -> dict[str, object]:
    base = build_registry_bridge()
    candidates = representative_candidates()
    result, attempts = bind_representative_witnesses(base, candidates)
    structured = sum(r.status is MigrationStatus.STRUCTURED for r in result.records)
    counts = {status: sum(a.status == status for a in attempts)
              for status in sorted({a.status for a in attempts})}
    report = {
        "phase": "163 R4-R7",
        "status_counts": counts,
        "total_base_records": len(base.records),
        "structured_records": structured,
        "original_structured_records": sum(r.status is MigrationStatus.STRUCTURED for r in base.records),
        "notes": [
            "Citation ancestry check is not independent literature verification.",
            "Brackets represented by a GIVEN remain unverified unless a legitimate derivation exists.",
            "Nu-prime membership is not inferred from bracket membership automatically.",
            "Any failed candidate remains metadata-only; no invented theorem facts.",
            "No full pytest, no backward search or renderer changes.",
        ],
        "attempts": [
            {"reference_locator": a.reference_locator,
             "component_key": a.component_key,
             "status": a.status, "detail": a.detail}
            for a in attempts
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = ["# Phase 163 R4-R7 — 代表的な実 ProofStep 接続", "",
             "これは選択した4候補の結果であり、全命題数ではありません。", "",
             "| 文献 | component | 状態 | 理由 |", "|---|---|---|---|"]
    for a in attempts:
        lines.append(f"| {a.reference_locator} | `{a.component_key}` | {a.status} | {a.detail.replace('|', '/')} |")
    lines.extend(["", f"- Structured records: {structured}",
                  "- 全体 pytest: 未実施", "- 文献原本に対する数学的同一性の検証: 未完了", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    audit = run_audit(Path("phase163_r4_r7_output"))
    print("Phase 163 R4-R7", audit["status_counts"])
    print("Saved phase163_r4_r7_output/report.md")
    print("Full pytest not run.")

```

## 新規テストファイル全文

```python
from dataclasses import replace

import pytest

from phase163_r4_r7_representative_bindings import (
    WitnessCandidate,
    bind_representative_witnesses,
)
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from proof import (
    FoundationalReferenceIdentity,
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
)


LOCATOR = "(5.3)"
KEY = "nu_prime_hopf_relation"


def _derived():
    given = ProofStep(conclusion="input", premises=(), rule=ProofRule.GIVEN)
    conclusion = Relation(lhs="H(nu_prime)", rhs="eta_5")
    return ProofStep(conclusion=conclusion, premises=(given,), rule=ProofRule.INFERENCE)


def _citation(witness, locator, component, expected):
    identity = FoundationalReferenceIdentity(
        key=f"literature:{locator}:{component}", label=locator
    )
    leaf = ProofStep(
        conclusion=expected, premises=(), rule=ProofRule.GIVEN,
        foundational_reference=identity,
    )
    return ProofStep(
        conclusion=expected, premises=(leaf,), rule=ProofRule.INFERENCE,
        foundational_reference=identity,
        inference_rule=InferenceRule(
            name="phase162_verified_literature_citation",
            literature_reference=LiteratureReference(label="Toda " + locator, locator=locator),
        ),
    )


def _candidate():
    step = _derived()
    return WitnessCandidate(LOCATOR, KEY, step, step.conclusion, "test fixture")


def test_r4_r7_accepted_typed_citation_keeps_original_metadata():
    base = build_registry_bridge()
    result, attempts = bind_representative_witnesses(
        base, (_candidate(),), citation_builder=_citation
    )
    assert attempts[0].status == "STRUCTURED"
    assertion_id = f"boundary:{LOCATOR}:{KEY}"
    assert result.registry.assertion(assertion_id).content == _candidate().expected_conclusion
    assert next(r for r in result.records if r.assertion_id == assertion_id).status is MigrationStatus.STRUCTURED
    assert next(r for r in base.records if r.assertion_id == assertion_id).status is MigrationStatus.METADATA_ONLY


def test_r4_r7_given_is_not_promoted():
    base = build_registry_bridge()
    candidate = _candidate()
    given = ProofStep(conclusion=candidate.expected_conclusion, premises=(), rule=ProofRule.GIVEN)
    result, attempts = bind_representative_witnesses(
        base, (replace(candidate, witness=given),), citation_builder=_citation
    )
    assert attempts[0].status == "GIVEN_UNVERIFIED"
    assert result.records == base.records


def test_r4_r7_rejects_invalid_citation_without_promotion():
    base = build_registry_bridge()
    def invalid(witness, locator, component, expected):
        return witness
    result, attempts = bind_representative_witnesses(
        base, (_candidate(),), citation_builder=invalid
    )
    assert attempts[0].status == "VERIFICATION_FAILED"
    assert result.records == base.records


def test_r4_r7_unregistered_component_is_not_promoted():
    base = build_registry_bridge()
    candidate = replace(_candidate(), component_key="not_in_registry")
    result, attempts = bind_representative_witnesses(
        base, (candidate,), citation_builder=_citation
    )
    assert attempts[0].status == "NOT_REGISTERED"
    assert result.records == base.records


def test_r4_r7_duplicate_rejected():
    base = build_registry_bridge()
    candidate = _candidate()
    with pytest.raises(ValueError, match="duplicate"):
        bind_representative_witnesses(base, (candidate, candidate), citation_builder=_citation)


def test_r4_r7_conclusion_mismatch_rejected():
    with pytest.raises(ValueError, match="must match"):
        WitnessCandidate(LOCATOR, KEY, _derived(), "not a conclusion", "test")

```

## PowerShell 全文

```powershell
$ErrorActionPreference = "Stop"
$project = (Get-Location).Path
$package = $PSScriptRoot
$required = @(
  "unified_statement_registry.py",
  "phase163_r4_registry_bridge.py",
  "phase163_r4_r6_structured_binding.py",
  "phase162_reference_boundary.py",
  "probes\probe_phase58_capabilities.py",
  "probes\probe_phase65_capabilities.py"
)
foreach ($relative in $required) {
  if (-not (Test-Path (Join-Path $project $relative))) {
    throw "Required existing project file missing: $relative"
  }
}
$dest = Join-Path $project "tests"
if (-not (Test-Path $dest)) { throw "Project tests directory missing" }
Copy-Item (Join-Path $package "phase163_r4_r7_representative_bindings.py") (Join-Path $project "phase163_r4_r7_representative_bindings.py") -Force
Copy-Item (Join-Path $package "tests\test_phase163_r4_r7_representative_bindings.py") (Join-Path $dest "test_phase163_r4_r7_representative_bindings.py") -Force
python -m pytest -q tests/test_phase163_r4_r6_structured_binding.py tests/test_phase163_r4_r7_representative_bindings.py
if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $LASTEXITCODE" }
python phase163_r4_r7_representative_bindings.py
if ($LASTEXITCODE -ne 0) { throw "Representative binding audit failed: $LASTEXITCODE" }
Write-Host "Phase 163 R4-R7 focused tests and representative audit finished. Full suite not run."

```
