# Phase 163 R4-R8 — 既存コードとの境界および全文

## 現行コード・関連テスト

- GitHub `proof.py`: `ProofStep` と `ProofRule.GIVEN` の契約を確認。
- `probes/probe_phase58_capabilities.py`: `(5.3)` の `bracket_membership_step` に三成分と index 1 を保持していることを確認。
- ローカルの R2、R4 Bridge、R6、R7 実装と R7 の軽量テストを確認。
- 既存 `toda_literature_statement_boundary.py` の `nu_prime_bracket_definition` を使用。

## 変更対象・追加位置

- **プロジェクトルートに新規追加**: `phase163_r4_r8_choice_registration.py`
  - クラス `LiteratureChoice`, `ChoiceSnapshot`（全文は後述）。
  - 関数 `register_literature_choices`, `nu_prime_bracket_matches`, `build_nu_prime_choice`, `run_audit`（全文は後述）。
- **tests に新規追加**: `tests/test_phase163_r4_r8_choice_registration.py`。すべてのテスト関数・import を全文掲載。
- パッケージ内 `run.ps1`: 配置後の軽量テストと監査を実行。
- **既存ソース／既存 API／既存テストの変更なし**。import の追加も既存ファイルにはなし。

## 意図的な制限

`nu_prime_bracket_definition` は Toda bracket の「元の選択」であり、**通常の推論で導出された証明済み Statement とは別**。
型付きの選択内容は `ChoiceSnapshot` に保持するが、元の Bridge 状態は `metadata_only` のままである。
数式構造が一致しても、文献原本による出典検証・一般的な引用許可は与えない。
`GIVEN` の検証に Phase 162 の導出検証を流用しない。`H(ν′)=η₅`、`2ν′=η₃η₄η₅` の処理は R7 のまま。

## 実行する pytest

```powershell
python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py
```

全体 pytest は Phase 163 の終了時に実行する。R8 の完了条件は、新規8テスト PASS、代表データの Choice が型付きで保存されていること、橋渡しの元の状態が維持されていること。R9 以降で Definition 全体の出典監査を行い、Phase 164 の探索接続は先取りしない。

## 追加ソース：全文

```python
"""Phase 163 R4-R8: retain typed literature choice without asserting proof.

The (5.3) nu-prime bracket membership is a source-claimed selection, not
an inference or a mathematically verified external statement.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from expression import HomotopyElement, Multiple, TodaBracket
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult, build_registry_bridge
from proof import ProofRule, ProofStep
from toda_rules import TodaBracketMembershipStatement


@dataclass(frozen=True)
class LiteratureChoice:
    """Typed selection with explicit, intentionally unverified provenance."""

    assertion_id: str
    reference_locator: str
    component_key: str
    defined_symbol: str
    statement: TodaBracketMembershipStatement
    source_step: ProofStep
    provenance: str = "source_claimed_not_independently_verified"

    def __post_init__(self) -> None:
        if self.provenance != "source_claimed_not_independently_verified":
            raise ValueError("unsupported provenance: verification must not be invented")
        if self.assertion_id != f"boundary:{self.reference_locator}:{self.component_key}":
            raise ValueError("assertion identity mismatch")
        if not isinstance(self.statement, TodaBracketMembershipStatement):
            raise TypeError("statement must be a TodaBracketMembershipStatement")
        if not isinstance(self.source_step, ProofStep):
            raise TypeError("source_step must be ProofStep")
        if self.source_step.rule is not ProofRule.GIVEN or self.source_step.premises:
            raise ValueError("choice must have a leaf GIVEN source; derived facts need R6/R7")
        if self.source_step.conclusion != self.statement:
            raise ValueError("choice statement differs from source step")
        if not self.defined_symbol:
            raise ValueError("defined_symbol required")


@dataclass(frozen=True)
class ChoiceSnapshot:
    """A parallel typed declaration catalog; no citation permission granted."""

    bridge: RegistryBridgeResult
    choices: tuple[LiteratureChoice, ...]

    def find(self, assertion_id: str) -> LiteratureChoice:
        return next(choice for choice in self.choices if choice.assertion_id == assertion_id)


def register_literature_choices(
    base: RegistryBridgeResult,
    choices: tuple[LiteratureChoice, ...],
) -> ChoiceSnapshot:
    """Validate identities and record typed choices without promoting bridge statuses."""
    if not isinstance(base, RegistryBridgeResult):
        raise TypeError("base must be RegistryBridgeResult")
    if not isinstance(choices, tuple):
        raise TypeError("choices must be a tuple")
    allowed = {
        record.assertion_id for record in base.records
        if record.source == "boundary" and record.status is MigrationStatus.METADATA_ONLY
    }
    seen: set[str] = set()
    for choice in choices:
        if not isinstance(choice, LiteratureChoice):
            raise TypeError("choices must contain LiteratureChoice")
        if choice.assertion_id not in allowed:
            raise ValueError(f"not an eligible boundary: {choice.assertion_id}")
        if choice.assertion_id in seen:
            raise ValueError(f"duplicate choice: {choice.assertion_id}")
        seen.add(choice.assertion_id)
        if base.registry.reference(f"toda:{choice.reference_locator}").locator != choice.reference_locator:
            raise ValueError("reference locator mismatch")
    return ChoiceSnapshot(bridge=base, choices=choices)


def nu_prime_bracket_matches(statement: TodaBracketMembershipStatement) -> bool:
    """Check structural fields; never infer truth of the mathematical relation."""
    if not isinstance(statement, TodaBracketMembershipStatement):
        return False
    element = statement.element
    bracket = statement.bracket
    if not isinstance(element, HomotopyElement) or not isinstance(bracket, TodaBracket):
        return False
    if not isinstance(bracket.first, HomotopyElement) or not isinstance(bracket.third, HomotopyElement):
        return False
    second = bracket.second
    if not isinstance(second, Multiple) or not isinstance(second.expression, HomotopyElement):
        return False
    elements = (element, bracket.first, second.expression, bracket.third)
    generators = tuple(x.generator for x in elements)
    return (
        element.name == "ν′"
        and element.source == 6 and element.target == 3
        and generators[0] is not None and generators[0].family == "ν" and generators[0].decoration == "′"
        and generators[1] is not None and generators[1].family == "η" and generators[1].index == 3
        and second.coefficient == 2
        and generators[2] is not None and generators[2].family == "ι" and generators[2].index == 4
        and generators[3] is not None and generators[3].family == "η" and generators[3].index == 4
        and bracket.index == 1
    )


def build_nu_prime_choice(base: RegistryBridgeResult, source_step: ProofStep) -> ChoiceSnapshot:
    """Use the existing bracket GIVEN directly, without replacing it with a proof."""
    if not isinstance(source_step, ProofStep):
        raise TypeError("source_step must be ProofStep")
    if not nu_prime_bracket_matches(source_step.conclusion):
        raise ValueError("source is not nu-prime in {eta_3, 2 iota_4, eta_4}_1")
    choice = LiteratureChoice(
        assertion_id="boundary:(5.3):nu_prime_bracket_definition",
        reference_locator="(5.3)",
        component_key="nu_prime_bracket_definition",
        defined_symbol="ν′",
        statement=source_step.conclusion,
        source_step=source_step,
    )
    return register_literature_choices(base, (choice,))


def run_audit(output_dir: Path) -> dict[str, object]:
    from probes.probe_phase58_capabilities import build_phase58_representative_result

    base = build_registry_bridge()
    representative = build_phase58_representative_result()
    snapshot = build_nu_prime_choice(base, representative["bracket_membership_step"])
    choice = snapshot.choices[0]
    record = next(record for record in base.records if record.assertion_id == choice.assertion_id)
    report = {
        "phase": "163 R4-R8",
        "reference_locator": choice.reference_locator,
        "component_key": choice.component_key,
        "defined_symbol": choice.defined_symbol,
        "expression": "nu_prime in {eta_3, 2 iota_4, eta_4}_1",
        "typed_bracket_index": choice.statement.bracket.index,
        "status": "CHOICE_RECORDED_SOURCE_UNVERIFIED",
        "bridge_status_unchanged": record.status.value,
        "source_rule": choice.source_step.rule.value,
        "choice_count": len(snapshot.choices),
        "notes": [
            "A GIVEN source is a source-claimed selection, not a derived proof.",
            "The typed choice catalog does not grant theorem availability or citation eligibility.",
            "The original bridge remains metadata-only for this component.",
            "No independent verification against the printed literature was performed.",
            "R7 derived Hopf/double relations remain separate assertions.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 163 R4-R8 — (5.3) の元の選択の記録", "",
        r"- 数学的表記: $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$",
        "- 型付きの式の検査: 成功", "- 登録区分: CHOICE_RECORDED_SOURCE_UNVERIFIED",
        "- 元の Bridge の状態: metadata_only（変更なし）",
        "- 既存 ProofStep: GIVEN（変更なし）", "- 原典との独立照合: 未実施", "",
        r"この選択は $H(\nu')=\eta_5$ や $2\nu'=\eta_3\eta_4\eta_5$ と別々に扱う。",
        "探索への候補提供、推論規則の自動生成、Renderer 変更は行わない。",
        "全体 pytest は Phase 163 の最後まで実施しない。", "",
    ]
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return report


if __name__ == "__main__":
    result = run_audit(Path("phase163_r4_r8_output"))
    print("Phase 163 R4-R8:", result["status"], result["bridge_status_unchanged"])
    print("Saved phase163_r4_r8_output/report.md")
    print("Full pytest not run.")

```

## 新規テスト：全文

```python
from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Multiple, TodaBracket
from phase163_r4_r8_choice_registration import (
    LiteratureChoice,
    build_nu_prime_choice,
    nu_prime_bracket_matches,
    register_literature_choices,
)
from phase163_r4_registry_bridge import MigrationStatus, build_registry_bridge
from proof import ProofRule, ProofStep
from toda_rules import TodaBracketMembershipStatement


def _nu_prime_step(index=1):
    nu = HomotopyElement(name="ν′", dimension=3, source=6, target=3,
                         generator=GeneratorSymbol(family="ν", decoration="′"))
    eta3 = HomotopyElement(name="η₃", dimension=3, generator=GeneratorSymbol(family="η", index=3))
    iota4 = HomotopyElement(name="ι_4", dimension=4, generator=GeneratorSymbol(family="ι", index=4))
    eta4 = HomotopyElement(name="η₄", dimension=4, generator=GeneratorSymbol(family="η", index=4))
    statement = TodaBracketMembershipStatement(
        element=nu, bracket=TodaBracket(
            first=eta3, second=Multiple(coefficient=2, expression=iota4),
            third=eta4, index=index,
        )
    )
    return ProofStep(conclusion=statement, premises=(), rule=ProofRule.GIVEN)


def _choice(step):
    return LiteratureChoice(
        assertion_id="boundary:(5.3):nu_prime_bracket_definition",
        reference_locator="(5.3)", component_key="nu_prime_bracket_definition",
        defined_symbol="ν′", statement=step.conclusion, source_step=step,
    )


def test_r4_r8_typed_selection_keeps_full_toda_bracket():
    step = _nu_prime_step()
    assert nu_prime_bracket_matches(step.conclusion)
    assert step.conclusion.bracket.index == 1
    assert step.conclusion.bracket.second.coefficient == 2
    assert step.conclusion.bracket.first.generator.index == 3
    assert step.conclusion.bracket.third.generator.index == 4


def test_r4_r8_selection_keeps_bridge_metadata_only():
    base = build_registry_bridge()
    result = build_nu_prime_choice(base, _nu_prime_step())
    target = "boundary:(5.3):nu_prime_bracket_definition"
    assert result.find(target).statement == _nu_prime_step().conclusion
    assert next(record.status for record in base.records if record.assertion_id == target) is MigrationStatus.METADATA_ONLY
    assert result.bridge is base


def test_r4_r8_wrong_bracket_index_is_rejected():
    with pytest.raises(ValueError, match="not nu-prime"):
        build_nu_prime_choice(build_registry_bridge(), _nu_prime_step(index=2))


def test_r4_r8_given_with_premises_is_rejected():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="leaf GIVEN"):
        _choice(replace(step, premises=(step,)))


def test_r4_r8_derived_proof_is_not_labeled_choice():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="leaf GIVEN"):
        _choice(replace(step, rule=ProofRule.INFERENCE))


def test_r4_r8_duplicate_choice_is_rejected():
    step = _nu_prime_step()
    with pytest.raises(ValueError, match="duplicate"):
        register_literature_choices(build_registry_bridge(), (_choice(step), _choice(step)))


def test_r4_r8_wrong_assertion_identity_is_rejected():
    with pytest.raises(ValueError, match="identity mismatch"):
        replace(_choice(_nu_prime_step()), assertion_id="boundary:(5.3):nu_prime_hopf_relation")


def test_r4_r8_unknown_boundary_is_rejected():
    choice = _choice(_nu_prime_step())
    with pytest.raises(ValueError, match="not an eligible boundary"):
        register_literature_choices(
            build_registry_bridge(),
            (replace(choice, reference_locator="(9.9)", assertion_id="boundary:(9.9):nu_prime_bracket_definition"),),
        )

```

## 実行スクリプト：全文

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'python'

$TargetSource = Join-Path $ProjectRoot 'phase163_r4_r8_choice_registration.py'
$TargetTest = Join-Path $ProjectRoot 'tests\test_phase163_r4_r8_choice_registration.py'
$ExpectedFiles = @(
    'unified_statement_registry.py',
    'phase163_r4_registry_bridge.py',
    'phase163_r4_r6_structured_binding.py',
    'phase163_r4_r7_representative_bindings.py',
    'phase162_reference_boundary.py',
    'toda_literature_statement_boundary.py',
    'proof.py',
    'toda_rules.py'
)
foreach ($Filename in $ExpectedFiles) {
    if (-not (Test-Path (Join-Path $ProjectRoot $Filename))) {
        throw "Required current project file missing: $Filename"
    }
}
if (-not (Test-Path (Join-Path $ProjectRoot 'tests'))) {
    throw 'Expected project tests directory missing.'
}
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r8_choice_registration.py') -Destination $TargetSource -Force
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests\test_phase163_r4_r8_choice_registration.py') -Destination $TargetTest -Force

& $Python -B -m pytest -q tests/test_phase163_r4_r8_choice_registration.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 R4-R8 focused pytest failed; audit not run.' }
& $Python -B phase163_r4_r8_choice_registration.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 163 R4-R8 audit failed.' }
Write-Host 'Phase 163 R4-R8 focused test and choice declaration audit complete. Full suite not run.'

```
