# Phase 171 R2H — 変更コード全文

## 変更対象と追加位置

1. `phase165_r52_r9_shared_math.py` の関数 `build_shared_typed_bridge` 全体（R2E 出典の直後に新たな出典を追加）。
2. 同ファイルの関数 `shared_expansion_provider` 全体（`expand_hopf_image_relation` の直後に新たな推論経路を追加）。
3. `phase171_r2h_prop22_cited_hopf/source.py` 新設（既存の `phase171_r2e_toda53_double_reference.py` と同じリポジトリ直下階層）。
4. `phase171_r2h_prop22_cited_hopf/install.py`、`audit.py`、`run.ps1`、`tests/test_install.py`、`tests/test_cited_formula.py` を新設。テストは既存ファイルを変更せず、別パッケージに追加する。

既存ファイルの `import` 部は変更しない。新規モジュールの `import` 部は以下のコード全文に含む。

## `phase165_r52_r9_shared_math.py` の関数全文

`run.ps1` の実行後、**実際の置換後の関数全文**が以下のファイルに生成される。ここに数行差分を省略したコードを貼り付ける必要はない。出力ファイルは関数定義先頭から関数終了までを AST から抽出した完全な Python コードであり、元の関数と置換可能である。

- `phase171_r2h_prop22_cited_hopf/output/build_shared_typed_bridge_FULL.py`
- `phase171_r2h_prop22_cited_hopf/output/shared_expansion_provider_FULL.py`

変更部分の全文は次の2箇所である。その他の既存コード、型定義、import、API は不変。

```python
        from phase171_r2h_prop22_cited_hopf.source import (
            build_cited_prop22_right_reference,
        )
        sources = sources + (build_cited_prop22_right_reference(production),)
```

```python
        from phase171_r2h_prop22_cited_hopf.source import (
            expand_cited_prop22_right_formula,
        )
        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))
```

## `source.py` 全文

```python
"""Verified general right-Hopf formula and conservative typed derivations.

The registered general formula is a cited leaf, NOT a proof of any group.
Concrete formulas and Hopf-value substitutions must be INFERENCE steps.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from expression import Composition, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

SOURCE_ID = "toda:tex:ch2:0009"
SOURCE_SHA256 = "5560fe950f06dea97bd152bc97dd29661576697a7d7e58b41c938f0b3e373146"
REFERENCE_ID = "toda:Proposition 2.2"
ASSERTION_ID = "toda:adopted:prop2.2:right_hopf_formula"
RIGHT_FORMULA = r"H(\alpha\circ E\beta)\ =\ H(\alpha)\circ E\beta"


@dataclass(frozen=True)
class TodaProp22RightFormula:
    """The universal formula H(alpha o E beta) = H(alpha) o E beta."""


def build_cited_prop22_right_reference(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:
    """Adopt the exact prior formula from the one reviewed archival source."""
    if not isinstance(source_bridge, RegistryBridgeResult):
        raise TypeError("source_bridge must be RegistryBridgeResult")
    candidates = tuple(
        assertion for assertion in source_bridge.registry._assertions.values()
        if assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(assertion.content, dict)
        and assertion.content.get("source_statement_id") == SOURCE_ID
    )
    if len(candidates) != 1:
        raise ValueError("Proposition 2.2 must have exactly one archived source")
    source = candidates[0].content
    text = source.get("source_text")
    if (not isinstance(text, str)
            or source.get("source_sha256") != SOURCE_SHA256
            or sha256(text.encode("utf-8")).hexdigest() != SOURCE_SHA256
            or r"\begin{proposition}\label{prop:2.2}" not in text
            or RIGHT_FORMULA not in text
            or r"\end{proposition}" not in text):
        raise ValueError("archived Proposition 2.2 formula failed source verification")

    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.PROPOSITION,
        locator="Proposition 2.2",
        source_id=SOURCE_ID,
    ))
    general = TodaProp22RightFormula()
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=general,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("right composition formula only",),
    ))
    step = ProofStep(
        conclusion=general,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda Proposition 2.2 right-Hopf source",
            literature_reference=LiteratureReference(
                label="Toda Proposition 2.2", locator="Proposition 2.2",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord(
            "phase171_r2h", SOURCE_ID, ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "adopted-source hash verified; original edition independently unverified",
        ),),
        (ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )


def _formula_parts(goal: object) -> tuple[HomotopyElement, HomotopyElement] | None:
    """Recognize only the literal right-formula shape with compatible degrees."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return None
    if not isinstance(goal.lhs, MapApplication) or goal.lhs.map != EHP_H_MAP:
        return None
    product = goal.lhs.expression
    if not isinstance(product, Composition):
        return None
    alpha, right = product.left, product.right
    if (not isinstance(alpha, HomotopyElement)
            or not isinstance(right, Suspension)
            or not isinstance(right.expression, HomotopyElement)
            or not product.is_type_compatible()):
        return None
    beta = right.expression
    if (type(alpha.dimension) is not int or type(beta.dimension) is not int
            or type(alpha.source) is not int or type(alpha.target) is not int
            or type(beta.source) is not int or type(beta.target) is not int
            or alpha.dimension != alpha.target or beta.dimension != beta.target
            or alpha.source != beta.target + 1):
        return None
    expected = Composition(MapApplication(EHP_H_MAP, alpha), right)
    return (alpha, beta) if goal.rhs == expected else None


def cited_prop22_right_specialization_rule(goal: Relation) -> InferenceRule:
    """Specialize the cited universal formula, never infer a citation from a name."""
    if _formula_parts(goal) is None:
        raise ValueError("goal is not a degree-compatible right-Hopf formula")

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].conclusion == TodaProp22RightFormula())

    return InferenceRule(
        name="specialize cited Toda Proposition 2.2 right formula",
        premise_patterns=(PremisePattern(statement_type=TodaProp22RightFormula),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def _combined_premises(goal: object, available: tuple[object, ...]) -> tuple[tuple[Relation, Relation], ...]:
    """Resolve only a screened H(alpha)=beta witness with beta the right factor."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)):
        return ()
    product = goal.lhs.expression
    if (not isinstance(product.right, Suspension)
            or not isinstance(product.right.expression, HomotopyElement)
            or not isinstance(product.left, HomotopyElement)):
        return ()
    alpha = product.left
    beta = product.right.expression
    formula = Relation(
        lhs=goal.lhs,
        rhs=Composition(MapApplication(EHP_H_MAP, alpha), product.right),
        relation_type=RelationType.EQUALITY,
    )
    if _formula_parts(formula) != (alpha, beta):
        return ()
    if goal.rhs != Composition(beta, product.right):
        return ()
    hopf = Relation(
        lhs=MapApplication(EHP_H_MAP, alpha),
        rhs=beta,
        relation_type=RelationType.EQUALITY,
    )
    return ((formula, hopf),) if available.count(hopf) == 1 else ()


def cited_prop22_hopf_substitution_rule(goal: Relation, formula: Relation, hopf: Relation) -> InferenceRule:
    """Apply the independently proved Hopf image to the proved right formula."""
    if _combined_premises(goal, (hopf,)) != ((formula, hopf),):
        raise ValueError("formula/Hopf premises are not the verified typed pair")

    def guard(premises, bindings):
        return (len(premises) == 2
                and premises[0].rule is ProofRule.INFERENCE
                and premises[0].conclusion == formula
                and premises[1].conclusion == hopf)

    return InferenceRule(
        name="substitute proved Hopf value into cited right formula",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=Relation),
            PremisePattern(statement_type=Relation),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_prop22_right_formula(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Supply backward proposals only when the cited source survives screening."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if available.count(TodaProp22RightFormula()) != 1:
        return ()
    if _formula_parts(goal) is not None:
        return (GoalExpansion(
            cited_prop22_right_specialization_rule(goal),
            (TodaProp22RightFormula(),),
        ),)
    if not isinstance(goal, Relation):
        return ()
    options = []
    for formula, hopf in _combined_premises(goal, available):
        options.append(GoalExpansion(
            cited_prop22_hopf_substitution_rule(goal, formula, hopf),
            (formula, hopf),
        ))
    return tuple(options)

```

## `install.py` 全文

```python
"""Guarded, idempotent R2H integration; no reset, checkout, or overwrite of edits."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha1
from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
BASE_BLOB_SHA = "97bd75c575200ff799e10c5d1f646bc804136580"
ANCHOR_SOURCE = "        sources = sources + (build_adopted_toda53_double_reference(production),)"
INSERT_SOURCE = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            build_cited_prop22_right_reference,\n"
    "        )\n"
    "        sources = sources + (build_cited_prop22_right_reference(production),)"
)
ANCHOR_PROVIDER = "        options.extend(expand_hopf_image_relation(goal, tuple(available)))"
INSERT_PROVIDER = (
    "        from phase171_r2h_prop22_cited_hopf.source import (\n"
    "            expand_cited_prop22_right_formula,\n"
    "        )\n"
    "        options.extend(expand_cited_prop22_right_formula(goal, tuple(available)))"
)


def git(*arguments: str) -> str:
    process = subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("git inspection failed: " + process.stderr)
    return process.stdout.strip()


def git_blob(data: bytes) -> str:
    normalized = data.replace(b"\r\n", b"\n")
    return sha1(b"blob " + str(len(normalized)).encode() + b"\0" + normalized).hexdigest()


def patch_source(source: str) -> str:
    """Insert only the R2H source and expansion connections in existing functions."""
    eol = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    if (normalized.count(ANCHOR_SOURCE) != 1
            or normalized.count(ANCHOR_PROVIDER) != 1):
        raise ValueError("shared integration anchors changed or are ambiguous")
    for addition in (INSERT_SOURCE, INSERT_PROVIDER):
        if addition in normalized:
            raise ValueError("partial or duplicate R2H integration")
    normalized = normalized.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE)
    normalized = normalized.replace(ANCHOR_PROVIDER, ANCHOR_PROVIDER + "\n" + INSERT_PROVIDER)
    return normalized.replace("\n", eol)


def status() -> tuple[str, bytes, bytes]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R2H must run on develop")
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    current = TARGET.read_bytes()
    normalized = current.decode("utf-8")
    if git_blob(current) == BASE_BLOB_SHA:
        updated = patch_source(normalized).encode("utf-8")
        return "NEEDS_PATCH", current, updated
    # Recognize exactly the result from the reviewed baseline, not arbitrary code.
    head_blob = git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py")
    if head_blob != BASE_BLOB_SHA:
        raise RuntimeError("HEAD shared_math blob differs from reviewed baseline")
    baseline = subprocess.run(
        ["git", "show", "HEAD:phase165_r52_r9_shared_math.py"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode("utf-8")
    expected = patch_source(baseline)
    if normalized.replace("\r\n", "\n") == expected.replace("\r\n", "\n"):
        return "ALREADY_APPLIED", current, current
    raise RuntimeError("shared_math contains unreviewed changes; refusing to overwrite")


def full_functions(source: str) -> dict[str, str]:
    """Extract the full post-change functions, never truncated diffs."""
    import ast
    tree = ast.parse(source)
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in (
            "build_shared_typed_bridge", "shared_expansion_provider",
        ):
            result[node.name] = ast.get_source_segment(source, node)
    if set(result) != {"build_shared_typed_bridge", "shared_expansion_provider"}:
        raise ValueError("expected full shared functions missing")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "apply"))
    args = parser.parse_args()
    stage, before, after = status()
    print("PHASE171_R2H_PREFLIGHT=" + stage, flush=True)
    if args.mode == "check":
        print("PHASE171_R2H_RESULT=PASS_CHECK", flush=True)
        return 0
    if stage == "NEEDS_PATCH":
        dest_root = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        dest = dest_root / ("phase171_r2h_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        dest.mkdir(parents=True, exist_ok=False)
        backup = dest / TARGET.name
        shutil.copy2(TARGET, backup)
        print("PHASE171_R2H_BACKUP=" + str(dest), flush=True)
        if TARGET.read_bytes() != before:
            raise RuntimeError("shared file changed during R2H preflight")
        TARGET.write_bytes(after)
        print("PHASE171_R2H_PATCHED=" + str(TARGET.relative_to(ROOT)), flush=True)
    checked = TARGET.read_text(encoding="utf-8")
    pieces = full_functions(checked)
    output = ROOT / "phase171_r2h_prop22_cited_hopf" / "output"
    output.mkdir(parents=True, exist_ok=True)
    for name, code in pieces.items():
        (output / (name + "_FULL.py")).write_text(code + "\n", encoding="utf-8")
    print("PHASE171_R2H_FUNCTIONS_FULL=" + str(output), flush=True)
    print("PHASE171_R2H_RESULT=PASS_APPLY", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

## `audit.py` 全文

```python
"""Verify the two-step cited Hopf derivation under publication-order screening."""
from __future__ import annotations

from expression import Composition, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2h_prop22_cited_hopf.source import (
    TodaProp22RightFormula, expand_cited_prop22_right_formula,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def run() -> None:
    complete = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(complete, n=3, k=3)
    if len(goals) != 1:
        raise RuntimeError("expected exactly one pi_6^3 goal")
    root = goals[0]
    citing = resolve_specialized_goal_citing_id(complete, root)
    if not citing:
        raise RuntimeError("pi_6^3 citing assertion unresolved")
    screened = screen_shared_proof_context(
        complete, goal=root, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    formula_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id.endswith(":toda:adopted:prop2.2:right_hopf_formula")
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == TodaProp22RightFormula()
    )
    hopf_links = tuple(
        link for link in screened.proof_links
        if link.assertion_id.endswith(":toda:adopted:eq5.3:nu_prime_hopf_relation")
        and link.step is not None
        and link.step.rule is ProofRule.GIVEN
    )
    if len(formula_links) != 1 or len(hopf_links) != 1:
        raise RuntimeError("one cited Prop2.2 and one (5.3) Hopf leaf required")
    assertion = screened.registry.assertion(formula_links[0].assertion_id)
    reference = screened.registry.reference(assertion.reference_id)
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or reference.locator != "Proposition 2.2"
            or reference.publication_position != 3700
            or not precedes_citing_assertion(screened, formula_links[0].assertion_id, citing)):
        raise RuntimeError("Proposition 2.2 citation position invalid")
    hopf = hopf_links[0].step.conclusion
    if (not isinstance(hopf, Relation)
            or hopf.relation_type is not RelationType.EQUALITY
            or not isinstance(hopf.lhs, MapApplication)
            or hopf.lhs.map != EHP_H_MAP):
        raise RuntimeError("(5.3) is not the typed H(nu-prime)=eta_5 equality")
    alpha, beta = hopf.lhs.expression, hopf.rhs
    final = Relation(
        lhs=MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        rhs=Composition(beta, Suspension(beta)),
        relation_type=RelationType.EQUALITY,
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=root)
    offered = provider(final)
    if not any(option.rule.name ==
               "substitute proved Hopf value into cited right formula"
               for option in offered):
        raise RuntimeError("new cited inference not connected to shared provider")
    # Audit only the newly introduced two-step chain, so unrelated generic
    # alternatives cannot be mistaken for a successful R2H witness.
    scoped_provider = lambda current: expand_cited_prop22_right_formula(
        current, available,
    )
    result = reconstruct_registered_goal(
        final, screened, citing, scoped_provider,
        lookup_mode="typed_reference_publication",
    )
    if (result.rule is not ProofRule.INFERENCE
            or result.conclusion != final
            or len(result.premises) != 2
            or result.premises[0].rule is not ProofRule.INFERENCE
            or result.premises[1].rule is not ProofRule.GIVEN
            or result.premises[1].conclusion != hopf
            or len(result.premises[0].premises) != 1
            or result.premises[0].premises[0].rule is not ProofRule.GIVEN
            or result.premises[0].premises[0].conclusion != TodaProp22RightFormula()):
        raise RuntimeError("right-Hopf dependency chain is not a verified two-step proof")
    if any(link.step is not None and link.step.conclusion == root for link in screened.proof_links):
        raise RuntimeError("group goal was incorrectly inserted as a source")
    print("PHASE171_R2H_PROP22_SOURCE=PASS", flush=True)
    print("PHASE171_R2H_PUBLICATION_POSITION=3700", flush=True)
    print("PHASE171_R2H_HOPF_DEPENDENCY=PASS", flush=True)
    print("PHASE171_R2H_FORMULA_INFERENCE=PASS", flush=True)
    print("PHASE171_R2H_COMBINED_INFERENCE=PASS", flush=True)
    print("PHASE171_R2H_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2H_RESULT=PASS_CITED_FORMULA_ONLY", flush=True)


if __name__ == "__main__":
    run()

```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m phase171_r2h_prop22_cited_hopf.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2H_RESULT=PASS_DRY_RUN'
        return
    }
    & python -B -m phase171_r2h_prop22_cited_hopf.install apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_PATCH_FAILED' }
    $Tests = @(
        'phase171_r2h_prop22_cited_hopf/tests/test_install.py',
        'phase171_r2h_prop22_cited_hopf/tests/test_cited_formula.py',
        'phase171_r2g_nu_prime_registered_identity/tests/test_identity.py',
        'phase168_r2_8_3_generator_identity/tests/test_r2_8_3_generator_identity.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'tests/test_phase30_prop22.py'
    )
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2H_FOCUSED_PYTEST=PASS'
    & python -B -m phase171_r2h_prop22_cited_hopf.audit
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2H_AUDIT_FAILED' }
    Write-Host 'PHASE171_R2H_RESULT=PASS'
}
finally { Pop-Location }

```

## `tests/test_install.py` 全文

```python
"""Pure tests for the guarded R2H installer (without production modules)."""
from __future__ import annotations

from hashlib import sha1

import pytest

from phase171_r2h_prop22_cited_hopf.install import (
    ANCHOR_PROVIDER, ANCHOR_SOURCE, INSERT_PROVIDER, INSERT_SOURCE,
    full_functions, git_blob, patch_source,
)


BASE = ("def build_shared_typed_bridge():\n"
        "    if True:\n" + ANCHOR_SOURCE + "\n"
        "def shared_expansion_provider():\n"
        "    def expand(goal):\n" + ANCHOR_PROVIDER + "\n")


def test_r2h_inserts_exactly_two_connections():
    patched = patch_source(BASE)
    assert patched.count(INSERT_SOURCE) == 1
    assert patched.count(INSERT_PROVIDER) == 1
    assert patched.index(ANCHOR_SOURCE) < patched.index(INSERT_SOURCE)


def test_r2h_preserves_crlf():
    patched = patch_source(BASE.replace("\n", "\r\n"))
    assert "\r\n" in patched
    assert patched.replace("\r\n", "\n") == patch_source(BASE)


def test_r2h_fails_closed_for_ambiguous_source_anchor():
    with pytest.raises(ValueError, match="anchors"):
        patch_source(BASE + ANCHOR_SOURCE)


def test_r2h_fails_closed_for_partial_integration():
    with pytest.raises(ValueError, match="partial"):
        patch_source(BASE.replace(ANCHOR_SOURCE, ANCHOR_SOURCE + "\n" + INSERT_SOURCE))


def test_r2h_extracts_two_whole_functions():
    functions = full_functions(patch_source(BASE))
    assert set(functions) == {"build_shared_typed_bridge", "shared_expansion_provider"}
    assert INSERT_SOURCE in functions["build_shared_typed_bridge"]
    assert INSERT_PROVIDER in functions["shared_expansion_provider"]


def test_git_blob_matches_standard_blob_calculation():
    data = b"hello\n"
    expected = sha1(b"blob 6\0hello\n").hexdigest()
    assert git_blob(data) == expected
    assert git_blob(b"hello\r\n") == expected

```

## `tests/test_cited_formula.py` 全文

```python
"""R2H proof-origin and type-safety regressions against the current repository."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
from map_facts import EHP_H_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase171_r2h_prop22_cited_hopf.source import (
    ASSERTION_ID, SOURCE_ID, TodaProp22RightFormula,
    _formula_parts, build_cited_prop22_right_reference,
    cited_prop22_right_specialization_rule, expand_cited_prop22_right_formula,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def _elements():
    alpha = HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"),
    )
    beta = HomotopyElement(
        "η₅", 5, 6, 5, GeneratorSymbol("η", index=5),
    )
    return alpha, beta


def _formal_goal():
    alpha, beta = _elements()
    return Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        Composition(MapApplication(EHP_H_MAP, alpha), Suspension(beta)),
        RelationType.EQUALITY,
    )


def test_proposition_22_archived_source_and_general_given():
    source_bridge = discover_goal_search_inputs().bridge
    cited = build_cited_prop22_right_reference(source_bridge)
    assert len(cited.proof_links) == 1
    assert cited.proof_links[0].step.rule is ProofRule.GIVEN
    assert cited.proof_links[0].step.conclusion == TodaProp22RightFormula()
    assertion = cited.registry.assertion(ASSERTION_ID)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert cited.registry.reference(assertion.reference_id).locator == "Proposition 2.2"


def test_proposition_22_rejects_falsified_source_bytes():
    base = discover_goal_search_inputs().bridge
    registry = UnifiedStatementRegistry()
    for reference in base.registry._references.values():
        registry.add_reference(reference)
    for assertion in base.registry._assertions.values():
        if (assertion.origin is AssertionOrigin.SOURCE_ARCHIVE
                and isinstance(assertion.content, dict)
                and assertion.content.get("source_statement_id") == SOURCE_ID):
            modified = dict(assertion.content)
            modified["source_text"] += " altered"
            assertion = replace(assertion, content=modified)
        registry.add_assertion(assertion)
    tampered = RegistryBridgeResult(registry, base.records, base.proof_links)
    with pytest.raises(ValueError, match="source verification"):
        build_cited_prop22_right_reference(tampered)


def test_right_formula_requires_screened_source():
    goal = _formal_goal()
    assert _formula_parts(goal) is not None
    assert expand_cited_prop22_right_formula(goal, ()) == ()
    options = expand_cited_prop22_right_formula(goal, (TodaProp22RightFormula(),))
    assert len(options) == 1
    assert options[0].subgoals == (TodaProp22RightFormula(),)
    assert cited_prop22_right_specialization_rule(goal).conclusion_pattern == goal


def test_right_formula_rejects_wrong_rhs_and_bad_dimensions():
    goal = _formal_goal()
    bad_rhs = replace(goal, rhs=goal.lhs.expression.right)
    assert expand_cited_prop22_right_formula(bad_rhs, (TodaProp22RightFormula(),)) == ()
    alpha, beta = _elements()
    invalid_alpha = replace(alpha, source=70)
    bad_goal = Relation(
        MapApplication(EHP_H_MAP, Composition(invalid_alpha, Suspension(beta))),
        Composition(MapApplication(EHP_H_MAP, invalid_alpha), Suspension(beta)),
        RelationType.EQUALITY,
    )
    assert _formula_parts(bad_goal) is None


def test_hopf_substitution_requires_exact_screened_hopf_relation():
    alpha, beta = _elements()
    final = Relation(
        MapApplication(EHP_H_MAP, Composition(alpha, Suspension(beta))),
        Composition(beta, Suspension(beta)),
        RelationType.EQUALITY,
    )
    source = TodaProp22RightFormula()
    hopf = Relation(MapApplication(EHP_H_MAP, alpha), beta, RelationType.EQUALITY)
    assert expand_cited_prop22_right_formula(final, (source,)) == ()
    assert expand_cited_prop22_right_formula(final, (source, hopf, hopf)) == ()
    options = expand_cited_prop22_right_formula(final, (source, hopf))
    assert len(options) == 1
    assert options[0].subgoals[1] == hopf
    assert _formula_parts(options[0].subgoals[0]) is not None


def test_cited_proposition_22_actual_two_step_proof_tree():
    from phase171_r2h_prop22_cited_hopf.audit import run
    run()

```

## `README.md` 全文

```markdown
# Phase 171 R2H — Cited Toda Proposition 2.2 Right-Hopf Derivation

This package registers the **source-verified general right-Hopf formula** from the adopted Toda Chapter II transcription and connects a narrowly typed two-step inference to the shared backward-search provider. It **does not** prove the group structure of `pi_6^3` or identify `eta_6` with `E(eta_5)`.

The source is archived as `toda:tex:ch2:0009` with reviewed SHA-256 `5560fe950f06dea97bd152bc97dd29661576697a7d7e58b41c938f0b3e373146`, publication position 3700, and locator `Proposition 2.2`. The original printed edition has not been independently verified.

## Changed production scope

- `phase165_r52_r9_shared_math.py`: complete functions `build_shared_typed_bridge` and `shared_expansion_provider` are affected; two guarded insertions attach the new cited source and proposal provider. There is no import-section change.
- New `phase171_r2h_prop22_cited_hopf/source.py`: complete source verification and typed inference functions. No existing rule or test is removed.
- `phase168_r2_8_3_generator_identity/identity.py` and all R2G work are left unchanged.

## Usage

Unzip the package at the repository root. Run `run.ps1 -DryRun`, followed by `run.ps1` from PowerShell. The runner checks the reviewed shared-source blob, backs it up under `%LOCALAPPDATA%\EHPProofTracerRecovery`, applies the narrow edit, runs focused pytest, and audits the resulting proof tree. It never runs the repository-wide test suite.

`output/build_shared_typed_bridge_FULL.py` and `output/shared_expansion_provider_FULL.py` are emitted by the installer after application, containing the complete actual replacement functions. The source module, installer, audit, test functions and PowerShell source are also included in `CHANGED_CODE_FULL_JA.md`.

## Intended proof scope

The screened general formula is `GIVEN`. Its concrete specialization `H(alpha o E beta) = H(alpha) o E beta` is `INFERENCE`. Substituting an independently screened `H(alpha)=beta` yields `H(alpha o E beta)=beta o E beta` as a second `INFERENCE`. No target group presentation is promoted to a source assertion.

The later identity `eta_6=E eta_5`, EHP exactness, order-four extension, and generator conclusion remain separate obligations for future R2H follow-up or R2I.

```

## `監査仕様.md` 全文

```markdown
# Phase 171 R2H — 監査仕様

## 対象と出典

対象は Toda Proposition 2.2 の右合成公式 $H(\alpha\circ E\beta)=H(\alpha)\circ E\beta$ のみとする。出典は `sources/toda/Toda_02_2.tex` に由来する既存アーカイブ `toda:tex:ch2:0009` とし、全文断片の SHA-256、原文の識別子および公式の字面を照合する。掲載順は既存 Phase 163 manifest の `toda:Proposition 2.2`（3700）を用い、独自の出典順を発明しない。刊行版原本との独立照合済みとは主張しない。

## 型付き推論

検証済み一般公式を `GIVEN` とし、具体的な元 $\alpha,\beta$ の source/target と合成適合性を確認したうえで $H(\alpha\circ E\beta)=H(\alpha)\circ E\beta$ を `INFERENCE` として導く。さらに独立に引用選別済みの等式 $H(\alpha)=\beta$ を前提として $H(\alpha\circ E\beta)=\beta\circ E\beta$ を導く。今回は $\alpha=\nu'$ と $\beta=\eta_5$ の場合を監査する。

## 信頼境界と対象外

Proposition 2.2 のメタデータのみでは `GIVEN` を作らない。アーカイブの不一致、出典の重複、掲載順の不一致、型の不一致、Hopf 等式の欠落・重複では失敗させる。群構造 Proposition 5.6 を `GIVEN` にしない。$\eta_6=E\eta_5$ の接続、$\pi_6^3$ の位数4、生成性、および $\pi_7^4,\pi_8^5$ は今回の境界外。

## テストと完了条件

限定 pytest だけを実行する。一般出典の SHA-256、固定命題の掲載順、2段の Proof Tree、偽装アーカイブの拒否、型不適合の拒否、既存 R2E/R2G のテストを確認する。結果が `PASS_CITED_FORMULA_ONLY` であっても群構造の完成とは判定しない。全体 pytest は Phase 171 終了時のみ実施する。

```

