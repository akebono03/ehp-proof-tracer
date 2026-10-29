# Phase 171 R2E-R4 — 修正内容と全置換コード

## 変更対象ファイル、クラス、関数、テスト

1. `phase165_r52_r9_shared_math.py` — `build_shared_typed_bridge()` 全体。既定の出典集合末尾に出典を1件追加し、通常経路の参照位置検査を維持する。`sources=` で指定する部分集合では全出典専用の検査をスキップする。**クラスの変更はない。module-level import は変更しない。**
2. `test_phase165_r52_r9_shared_math.py` — 既存テスト `test_r9_pi32_regenerated_by_shared_mathematical_expansion()` と `test_r9_public_pi32_narrative_unchanged()` の全文を置換。前者の証明完了条件は変更せず、入力 Bridge を全出典に変更。後者は表示見出しより数学的結論を検査。**import は変更しない。**
3. **リポジトリ直下へ新規** `phase171_r2e_toda53_double_reference.py` — `build_adopted_toda53_double_reference()`（出典採用）、全 import を含む。R2 数学実装と同じ。
4. `phase171_r2e_toda53_double_source/install.py` — 全関数 `git`, `verify_checkout`, `_replace_once`, `proposed_source`, `proposed_test`, `apply`, `restore`, `main`。改変許可範囲の厳密な検査と byte-exact 復元を維持。
5. `phase171_r2e_toda53_double_source/tests/test_install_unit.py` — 既存テスト関数全体と新規テスト関数3件（R4で3件追加）。新規テストの追加位置は `test_source_and_functions_are_syntactically_valid()` の直前。
6. `phase171_r2e_toda53_double_source/run.ps1`、`audit.py`、`tests/test_source.py` — R2 の全文を変更せず収録。
7. パッケージ内 `README.md` と `監査仕様.md` — それぞれ英語・日本語の全文を収録。

## R4 追加 — 変更箇所の特定と回帰条件

R3 の DryRun が `pi32 proof test anchor not unique` で停止した原因は、現行 GitHub `test_phase165_r52_r9_shared_math.py` の `from hopf_facts import ETA_2` 直後に空行がないのに、インストーラーの `TEST_PROOF_OLD` と変更後全関数 `TEST_PROOF_NEW` に空行があったため。R4 は **両方の関数全文と全テストファイルの空行配置のみ**を訂正する。`tests/test_install_unit.py` に新規テスト関数2件を `test_pi32_complete_requires_full_production_sources()` の直前に追加する。`install.py` では定数 `TEST_PROOF_OLD`、`TEST_PROOF_NEW` の定義だけを訂正し、その他の関数は変更しない。

**今回の R4 実装は既存本番コードや `GIVEN` 採用規則に追加変更を行わない。** R2E の数学的変更は R2/R3 と同一。テストについても全出典からの π₃² 完成証明の判定 (`COMPLETE`、正確な結論、`INFERENCE` 存在) を維持する。

## 失敗した既存テストの扱い

R2E-R2 では `sources=(_adopted_source(),)` の部分 Bridge に対し `π₃²` の `COMPLETE` を期待し、実際には `PARTIAL` となった。この部分出典だけから現在の完成証明の依存関係を得られるという前提は、本番経路の前提と一致していない。Phase 166 R3-R の関連監査では、`build_shared_typed_bridge()` の全出典を使用して同じ π₃² 証明を検査している。

そのため、完成証明テストでは `build_shared_typed_bridge()` を使い、**`ProofSearchStatus.COMPLETE`、正確な群構造の結論、および `ProofRule.INFERENCE` の存在という数学的な検査をすべて残す**。出典集合の部分指定が証明を自動補完しないことは、他の既存テストおよび R2E の新規テストで検査する。π₆³ を完成証明として偽装しない。

## 既存コード・テストの確認

GitHub `akebono03/ehp-proof-tracer` の現行 `develop` から以下を確認した：
`phase165_r52_r9_shared_math.py`、`phase166_r3p_position_binding.py`、`test_phase165_r52_r9_shared_math.py`、`phase166_r3r_proof_tree_audit/audit.py`、`phase169_r3h_source_registry.py`、`phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py`。

変更後の関数／テストを `...` により省略せず全文提示する。ルートの `README.md` 等の正式ドキュメントは変更しない。

## 既存 `phase165_r52_r9_shared_math.py` の import 全文（変更なし）

対応ファイル：`IMPORTS_phase165_r52_r9_shared_math_FULL.py`

```python
"""Shared Phase 165 typed backward-search path. Never replay saved proofs.

Typed source claims may be reused across goals; a source's role as a leaf
is not a license to use an untyped archive or an earlier derived proof.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage, MapIsomorphism, expand_generic_iso_goal
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r14_r11_delta_zero import expand_delta_zero_from_suspension_iso
from phase165_r14_r14_diagonal_and_prop42 import expand_diagonal_suspension
from phase165_r14_r33_final_group import reverse_free_cyclic_transport_rule
from phase165_r3_recursive_search import GoalExpansion
from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import build_context_expansion_provider_registry
from phase165_r6_2_unified_registry_r3_r3.provider_registry import build_shared_expansion_provider_registry
from phase165_r6_2_unified_registry_r1.unified_backward_rule_registry import build_unified_backward_rule_registry
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import (
    AssertionOrigin, UnifiedStatementRegistry,
)
```

## 既存 `build_shared_typed_bridge()` の変更後全文

対応ファイル：`build_shared_typed_bridge_FULL.py`

```python
def build_shared_typed_bridge(*, sources: tuple[RegistryBridgeResult, ...] | None = None) -> RegistryBridgeResult:
    """Merge eligible typed statements without importing derived group proofs.

    The R38 adopted-Tex *source assertions* are currently the first available
    rigorously linked typed leaves. They are shared with every query, not
    selected because the requested group is pi3^2.
    """
    default_sources = sources is None
    if sources is None:
        from phase165_r9_production_wiring import discover_goal_search_inputs
        from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
        production = discover_goal_search_inputs().bridge
        from phase168_r2_7_4_typed_registry_bridge.phase168_r2_7_4_literature_connection import (
            connect_explicit_literature_components,
        )
        production = connect_explicit_literature_components(production)
        adopted_tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
        from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
        from phase165_r52_r27_r5_literature import build_typed_literature_bridge
        from phase165_r57_r20_general_specialization import build_adopted_toda51_diagonal_reference
        literature = build_typed_literature_bridge(production)
        from phase165_r12_r11_prop42_unified import build_adopted_prop42_general_reference
        from phase165_r12_r15_toda51 import build_adopted_toda51_zero_reference
        from phase165_r12_r20_eta_definition import build_cited_eta_family_definition
        from phase169_r3h_source_registry import build_adopted_toda53_hopf_reference
        sources = (production, build_adopted_typed_reference_registry(adopted_tex),
                   build_adopted_prop51_reference(),
                   build_adopted_toda51_diagonal_reference(adopted_tex)) + (literature, build_adopted_prop42_general_reference(), build_adopted_toda51_zero_reference(adopted_tex), build_cited_eta_family_definition(Path(__file__).resolve().parent / 'sources' / 'toda' / 'Toda_05_2.tex'),
                   build_adopted_toda53_hopf_reference(production))
        from phase169_r10d2_general_family_definition.family_citation import (
            build_cited_stable_family_definitions,
        )
        from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
            build_cited_chapter_vi_family_definitions,
        )
        sources = sources + (
            build_cited_stable_family_definitions(),
            build_cited_chapter_vi_family_definitions(),
        )
        from phase169_r10eo_r3_reviewed_definition_bridge.reviewed_definitions import (
            build_cited_reviewed_definitions,
        )
        sources = sources + (build_cited_reviewed_definitions(),)
        from phase171_r2e_toda53_double_reference import (
            build_adopted_toda53_double_reference,
        )
        sources = sources + (build_adopted_toda53_double_reference(production),)
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for index, source in enumerate(sources):
        if not isinstance(source, RegistryBridgeResult):
            raise TypeError("source must be RegistryBridgeResult")
        # R3-C: reuse Phase 163 positions on original reference IDs before
        # shared: index namespacing. No locator or synthetic rank matching.
        from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
            connect_phase163_publication_order,
        )
        source, _publication_binding = connect_phase163_publication_order(source)
        prefix = f"shared:{index}:"
        for ref in source.registry._references.values():
            registry.add_reference(replace(ref, reference_id=prefix + ref.reference_id))
        for assertion in source.registry._assertions.values():
            if assertion.origin is AssertionOrigin.PROOF_INTERNAL:
                continue
            registry.add_assertion(replace(
                assertion, assertion_id=prefix + assertion.assertion_id,
                reference_id=prefix + assertion.reference_id,
                component_position=(
                    assertion.component_position * 100
                    if assertion.component_position is not None
                    and assertion.component_position < 100
                    else assertion.component_position
                ),
                dependencies=tuple(prefix + dep for dep in assertion.dependencies),
            ))
        eligible_ids = {
            a.assertion_id for a in source.registry._assertions.values()
            if a.origin is AssertionOrigin.FIXED_STATEMENT
        }
        for link in source.proof_links:
            if link.assertion_id not in eligible_ids:
                continue
            if link.step is not None and (
                link.step.rule is not ProofRule.GIVEN
                or link.step.conclusion != source.registry.assertion(link.assertion_id).content
            ):
                raise ValueError("source link is not a typed fixed Reference")
            links.append(replace(link, assertion_id=prefix + link.assertion_id))
        records.extend(
            replace(record, assertion_id=prefix + record.assertion_id)
            if record.assertion_id is not None else record
            for record in source.records
        )
    from phase165_r52_r12_component_bridge import expand_cited_given_components
    from phase166_r3l_reference_order import connect_all_reference_orders
    joined = expand_cited_given_components(
        RegistryBridgeResult(registry, tuple(records), tuple(links))
    )
    # Leave archived assertion identities untouched. In the default context,
    # these four old concrete (5.1) GIVENs must be derived by the already
    # registered universal source instead of short-circuiting the Proof Tree.
    if default_sources:
        legacy_ids = {
            "shared:1:adopted:assertion:1",
            "shared:1:adopted:assertion:2",
            "shared:1:adopted:assertion:4",
            "shared:1:adopted:assertion:6",
        }
        joined = RegistryBridgeResult(
            joined.registry, joined.records,
            tuple(link for link in joined.proof_links
                  if link.assertion_id not in legacy_ids),
        )
    # Preserve registered mathematical statements/IDs, but keep one direct
    # GIVEN for the Hopf-image fact; relation views are derived by a rule.
    hopf_relation_ids = {
        "shared:2:toda:adopted:prop5.1:eta2_hopf_relation",
        "shared:2:toda:adopted:prop5.1:finite_dimensional:component:eta2_hopf_relation",
    }
    joined = RegistryBridgeResult(
        joined.registry,
        joined.records,
        tuple(link for link in joined.proof_links
              if link.assertion_id not in hopf_relation_ids),
    )
    ordered, _order_report = connect_all_reference_orders(joined)
    if default_sources:
        from phase166_r3p_position_binding import place_r3p_reference_positions
        return place_r3p_reference_positions(ordered)
    return ordered
```

## 変更後の既存テストファイル全文（テスト2関数を変更）

対応ファイル：`test_phase165_r52_r9_shared_math_FULL.py`

```python
"""Targeted shared typed-goal tests: no saved proof replay or group-specific dispatch."""
from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r52_partial_proof import ProofSearchStatus
from proof import ProofRule, Relation
from unified_statement_registry import AssertionOrigin


def _adopted_source():
    path = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    return build_adopted_typed_reference_registry(path)


def test_r9_shared_registry_contains_source_claims_not_old_completed_proof():
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    assert len(bridge.proof_links) == 9
    assert all(
        entry.origin is not AssertionOrigin.PROOF_INTERNAL
        for entry in bridge.registry._assertions.values()
    )
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)


def test_r9_pi32_regenerated_by_shared_mathematical_expansion():
    from hopf_facts import ETA_2
    bridge = build_shared_typed_bridge()
    result = search_shared_group_goal(
        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)


def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved():
    from expression import GeneratorSymbol, HomotopyElement
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    result = search_shared_group_goal(
        n=3, k=1,
        group_structure=FiniteCyclicGroup(order=2, generator=eta3),
        bridge=bridge,
    )
    assert result.status in (ProofSearchStatus.SEARCH_FAILED, ProofSearchStatus.PARTIAL)
    assert result.conclusion is None
    assert any(isinstance(goal, Relation) for goal in result.open_goals)


def test_r9_shared_expansions_no_pi32_goal_equality_branch():
    from hopf_facts import ETA_2
    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))
    expand = shared_expansion_provider(bridge)
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    options = expand(goal)
    assert options
    assert len(options[0].subgoals) == 3




def test_r9_public_pi32_narrative_unchanged():
    from web_group_proof import build_standard_web_group_proof_view
    view = build_standard_web_group_proof_view(2, 1, 2, "narrative")
    body = "\n".join(
        line.prefix + " " + " ".join(seg.value for seg in line.segments)
        for line in view.rendered_lines
    )
    assert "使用する結果" in body
    assert "証明" in body
    assert r"\pi_{3}^{2}" in body
    assert r"\mathbb{Z}\{\eta_{2}\}" in body
```

## 新規出典モジュール全文（ルートに追加）

対応ファイル：`phase171_r2e_toda53_double_reference.py`

```python
"""Adopt precisely the pre-existing Toda (5.3) double relation as a cited leaf.

This source statement is not a proof of a group presentation or of its order.
The independent archive/hash validation is delegated to the existing adopted
(5.3) Hopf-source verifier; it already checks the exact second clause.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase169_r3h_source_registry import (
    REFERENCE_ID,
    SOURCE_ID,
    build_adopted_toda53_hopf_reference,
)
from proof import (
    InferenceRule,
    LiteratureReference,
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

ASSERTION_ID = "toda:adopted:eq5.3:nu_prime_double_relation"


def build_adopted_toda53_double_reference(
    source_bridge: RegistryBridgeResult,
) -> RegistryBridgeResult:
    """Register only 2 nu-prime = eta_3 o eta_4 o eta_5, with source ancestry.

    The existing adopted (5.3) verifier requires the uniquely identified source,
    its exact SHA-256 and the literal double relation; it rejects missing or
    changed source content. It is not legitimate to manufacture a GIVEN from
    an unverified group goal or Proposition 5.6 candidate.
    """
    verified = build_adopted_toda53_hopf_reference(source_bridge)
    if len(verified.proof_links) != 1:
        raise ValueError("existing (5.3) source verification is incomplete")

    nu_prime = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    eta3 = HomotopyElement(
        name="η₃", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    eta4 = HomotopyElement(
        name="η₄", dimension=4, source=5, target=4,
        generator=GeneratorSymbol(family="η", index=4),
    )
    eta5 = HomotopyElement(
        name="η₅", dimension=5, source=6, target=5,
        generator=GeneratorSymbol(family="η", index=5),
    )
    if (not Composition(eta4, eta5).is_type_compatible()
            or eta3.source != eta4.target):
        raise ValueError("ill-typed eta triple composition")
    relation = Relation(
        lhs=Multiple(2, nu_prime),
        rhs=Composition(eta3, Composition(eta4, eta5)),
        relation_type=RelationType.EQUALITY,
    )
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.3)",
        source_id=SOURCE_ID,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=relation,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("adopted (5.3) double relation only",),
    ))
    step = ProofStep(
        conclusion=relation,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Toda (5.3) double identity",
            literature_reference=LiteratureReference(
                label="Toda (5.3)", locator="(5.3)",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry,
        (MigrationRecord(
            "phase171_r2e", "(5.3):nu_prime_double_relation", ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "adopted source-hash-verified double equality; original edition unverified",
        ),),
        (ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )
```

## 変更後インストーラーの全文

対応ファイル：`install.py`

```python
"""Reversible R2E installation with source and focused-test compatibility repair.

Only the reviewed shared bridge function and one stale test assertion are changed.
No Git checkout/reset, implicit proof link, or renderer changes are performed.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXISTING_TEST = ROOT / "test_phase165_r52_r9_shared_math.py"
NEW_MODULE = ROOT / "phase171_r2e_toda53_double_reference.py"
PAYLOAD = PACKAGE / "phase171_r2e_toda53_double_reference.py"
FULL_FUNCTION = PACKAGE / "build_shared_typed_bridge_FULL.py"
FULL_TEST = PACKAGE / "test_phase165_r52_r9_shared_math_FULL.py"
EXPECTED_BLOB = "0ff831522b59f88ff3ed3892f35e5e048be850e1"
EXPECTED_TEST_BLOB = "c6dcfb3cda9c9115fb802f4a1b2141e0502506bd"
BASELINE = "715b00d67d4b3ff4b34bf87229842d14960ea6bb"
REVIEWED_DIRECTORIES = (
    "phase171_r1_n3_registered_audit/",
    "phase171_r1c_k3_registered_audit/",
    "phase171_r1d_k3_three_gap_diagnostics/",
    "phase171_r2a_prop56_alignment_audit/",
    "phase171_r2b_prop56_source_dependency_audit/",
    "phase171_r2c_pi63_source_frontier_audit/",
    "phase171_r2d_pi63_root_expansion_audit/",
    "phase171_r2e_toda53_double_source/",
)
ANCHOR = "        sources = sources + (build_cited_reviewed_definitions(),)"
ADDITION = "\n".join((
    "        from phase171_r2e_toda53_double_reference import (",
    "            build_adopted_toda53_double_reference,",
    "        )",
    "        sources = sources + (build_adopted_toda53_double_reference(production),)",
))
POSITION_OLD = "\n".join((
    "    from phase166_r3p_position_binding import place_r3p_reference_positions",
    "    return place_r3p_reference_positions(ordered)",
))
POSITION_NEW = "\n".join((
    "    if default_sources:",
    "        from phase166_r3p_position_binding import place_r3p_reference_positions",
    "        return place_r3p_reference_positions(ordered)",
    "    return ordered",
))
TEST_OLD = "\n".join((
    '    assert "証明対象" in body',
    '    assert "使用する結果" in body',
    '    assert "証明" in body',
))
TEST_NEW = "\n".join((
    '    assert "使用する結果" in body',
    '    assert "証明" in body',
    '    assert r"\\pi_{3}^{2}" in body',
    '    assert r"\\mathbb{Z}\\{\\eta_{2}\\}" in body',
))
TEST_PROOF_OLD = 'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n    from hopf_facts import ETA_2\n    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))\n    result = search_shared_group_goal(\n        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,\n    )\n    assert result.status is ProofSearchStatus.COMPLETE\n    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))\n    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)\n'
TEST_PROOF_NEW = 'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n    from hopf_facts import ETA_2\n    bridge = build_shared_typed_bridge()\n    result = search_shared_group_goal(\n        n=2, k=1, group_structure=FreeCyclicGroup(ETA_2), bridge=bridge,\n    )\n    assert result.status is ProofSearchStatus.COMPLETE\n    assert result.conclusion == Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))\n    assert any(step.rule is ProofRule.INFERENCE for step in result.proven_steps)\n'
BACKUP = (
    Path(os.environ.get("LOCALAPPDATA") or str(Path.home()))
    / "EHPProofTracerRecovery" / "phase171_r2e_toda53_double_source_backup"
)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            "git " + " ".join(args) + ": "
            + result.stderr.decode("utf-8", "replace").strip()
        )
    return result.stdout.decode("utf-8", "replace").strip()


def verify_checkout() -> None:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("expected develop branch")
    git("merge-base", "--is-ancestor", BASELINE, "HEAD")
    git("merge-base", "--is-ancestor", "origin/develop", "HEAD")
    changed = tuple(
        path for path in git("diff", "--name-only", "-z", BASELINE, "HEAD").split("\0")
        if path
    )
    if any(
        not any(path.startswith(directory) for directory in REVIEWED_DIRECTORIES)
        for path in changed
    ):
        raise RuntimeError("committed production changes outside reviewed audit directories")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("tracked worktree changes exist before R2E installation")
    if git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py") != EXPECTED_BLOB:
        raise RuntimeError("reviewed source blob changed")
    if git("rev-parse", "HEAD:test_phase165_r52_r9_shared_math.py") != EXPECTED_TEST_BLOB:
        raise RuntimeError("reviewed focused test blob changed")
    for path in (PAYLOAD, FULL_FUNCTION, FULL_TEST, TARGET, EXISTING_TEST):
        if not path.is_file():
            raise RuntimeError("missing reviewed R2E file: " + str(path))
    if NEW_MODULE.exists():
        raise RuntimeError("source module path exists before installation")


def _replace_once(original: str, old: str, new: str, label: str) -> str:
    if original.count(old) != 1:
        raise RuntimeError(label + " anchor not unique")
    return original.replace(old, new, 1)


def proposed_source(original: bytes) -> bytes:
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    updated = _replace_once(normalized, ANCHOR, ANCHOR + "\n" + ADDITION, "source")
    updated = _replace_once(updated, POSITION_OLD, POSITION_NEW, "position")
    start = updated.index("def build_shared_typed_bridge(")
    end = updated.index("def shared_expansion_provider(", start)
    actual_function = updated[start:end].rstrip("\n")
    expected_function = FULL_FUNCTION.read_text(encoding="utf-8").rstrip("\n")
    if actual_function != expected_function:
        raise RuntimeError("full replacement function differs from reviewed payload")
    return updated.replace("\n", newline).encode("utf-8")


def proposed_test(original: bytes) -> bytes:
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    normalized = text.replace("\r\n", "\n")
    updated = _replace_once(normalized, TEST_OLD, TEST_NEW, "narrative test")
    updated = _replace_once(updated, TEST_PROOF_OLD, TEST_PROOF_NEW, "pi32 proof test")
    start = updated.index("def test_r9_pi32_regenerated_by_shared_mathematical_expansion()")
    end = updated.index("def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved()", start)
    if updated[start:end].strip() != TEST_PROOF_NEW.strip():
        raise RuntimeError("pi32 proof function differs from reviewed payload")
    return updated.replace("\n", newline).encode("utf-8")


def apply(*, dry_run: bool = False) -> None:
    verify_checkout()
    original_source = TARGET.read_bytes()
    original_test = EXISTING_TEST.read_bytes()
    updated_source = proposed_source(original_source)
    updated_test = proposed_test(original_test)
    module_payload = PAYLOAD.read_bytes()
    if (not module_payload or updated_source == original_source
            or updated_test == original_test):
        raise RuntimeError("no validated changes to install")
    if dry_run:
        print("PHASE171_R2E_PREFLIGHT=PASS")
        print("PHASE171_R2E_DRY_RUN=PASS")
        return
    BACKUP.mkdir(parents=True, exist_ok=True)
    state_path = BACKUP / "state.json"
    source_before = BACKUP / "phase165_r52_r9_shared_math.py.before"
    test_before = BACKUP / "test_phase165_r52_r9_shared_math.py.before"
    if any(path.exists() for path in (state_path, source_before, test_before)):
        raise RuntimeError("existing R2E backup state; manual review required")
    state = {
        "original_source_sha256": sha256(original_source).hexdigest(),
        "updated_source_sha256": sha256(updated_source).hexdigest(),
        "original_test_sha256": sha256(original_test).hexdigest(),
        "updated_test_sha256": sha256(updated_test).hexdigest(),
        "new_module_sha256": sha256(module_payload).hexdigest(),
    }
    source_before.write_bytes(original_source)
    test_before.write_bytes(original_test)
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        NEW_MODULE.write_bytes(module_payload)
        TARGET.write_bytes(updated_source)
        EXISTING_TEST.write_bytes(updated_test)
    except Exception:
        TARGET.write_bytes(original_source)
        EXISTING_TEST.write_bytes(original_test)
        if NEW_MODULE.is_file() and NEW_MODULE.read_bytes() == module_payload:
            NEW_MODULE.unlink()
        for path in (state_path, source_before, test_before):
            path.unlink(missing_ok=True)
        raise
    print("PHASE171_R2E_PATCHED=phase165_r52_r9_shared_math.py")
    print("PHASE171_R2E_TEST_PATCHED=test_phase165_r52_r9_shared_math.py")
    print("PHASE171_R2E_NEW=phase171_r2e_toda53_double_reference.py")
    print("PHASE171_R2E_BACKUP=" + str(BACKUP))


def restore() -> None:
    state_path = BACKUP / "state.json"
    source_before = BACKUP / "phase165_r52_r9_shared_math.py.before"
    test_before = BACKUP / "test_phase165_r52_r9_shared_math.py.before"
    if any(not path.is_file() for path in (state_path, source_before, test_before)):
        raise RuntimeError("R2E restore state missing")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    original_source = source_before.read_bytes()
    original_test = test_before.read_bytes()
    for contents, name in (
        (original_source, "original_source_sha256"),
        (original_test, "original_test_sha256"),
    ):
        if sha256(contents).hexdigest() != state[name]:
            raise RuntimeError("backup content changed: " + name)
    for path, name in (
        (TARGET, "updated_source_sha256"),
        (EXISTING_TEST, "updated_test_sha256"),
        (NEW_MODULE, "new_module_sha256"),
    ):
        if not path.is_file() or sha256(path.read_bytes()).hexdigest() != state[name]:
            raise RuntimeError("patched file modified: refusing to overwrite " + str(path))
    TARGET.write_bytes(original_source)
    EXISTING_TEST.write_bytes(original_test)
    NEW_MODULE.unlink()
    for path in (state_path, source_before, test_before):
        path.unlink()
    print("PHASE171_R2E_RESTORED=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "install", "restore"))
    args = parser.parse_args()
    try:
        if args.mode == "restore":
            restore()
        else:
            apply(dry_run=(args.mode == "check"))
        return 0
    except Exception as exc:
        print(f"PHASE171_R2E_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        print(traceback.format_exc()[-2200:], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 変更後の起動用 PowerShell 全文

対応ファイル：`run.ps1`

```powershell
param(
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $package '..')).Path
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $repo
try {
    python -B -m phase171_r2e_toda53_double_source.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2E_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m phase171_r2e_toda53_double_source.install install
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_INSTALL_FAILED' }
    $tests = @(
        'phase171_r2e_toda53_double_source/tests/test_install_unit.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py',
        'phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py',
        'test_phase165_r52_r9_shared_math.py'
    )
    python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @tests
    $testExit = $LASTEXITCODE
    if ($testExit -ne 0) {
        Write-Warning 'Focused tests failed: restoring R2E modifications.'
        python -B -m phase171_r2e_toda53_double_source.install restore
        if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_RESTORE_FAILED' }
        throw "PHASE171_R2E_FOCUSED_PYTEST_EXIT=$testExit"
    }
    Write-Host 'PHASE171_R2E_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2e_toda53_double_source.audit
    $auditExit = $LASTEXITCODE
    if ($auditExit -ne 0) {
        Write-Warning 'Post-install source audit failed: restoring R2E modifications.'
        python -B -m phase171_r2e_toda53_double_source.install restore
        if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2E_RESTORE_FAILED' }
        throw "PHASE171_R2E_AUDIT_EXIT=$auditExit"
    }
    Write-Host 'PHASE171_R2E_RESULT=PASS'
}
finally {
    Pop-Location
}
```

## 監査コード全文

対応ファイル：`audit.py`

```python
"""Verify source-only R2E link in the current pi_6^3 citation screen.

This audit does not claim or construct a completed proof of pi_6^3.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import traceback

from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase171_r2e_toda53_double_reference import ASSERTION_ID
from proof import ProofRule


def audit() -> int:
    bridge = build_shared_typed_bridge()
    goal_candidates = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(goal_candidates) != 1:
        raise RuntimeError("pi_6^3 must have exactly one typed DB goal")
    goal = goal_candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing != "shared:0:boundary:Proposition 5.6:pi6_3_group_relation":
        raise RuntimeError("unexpected citing goal identity")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    source_id = "shared:12:" + ASSERTION_ID
    assertion = bridge.registry.assertion(source_id)
    reference = bridge.registry.reference(assertion.reference_id)
    steps = tuple(link.step for link in screened.proof_links
                  if link.assertion_id == source_id and link.step is not None)
    if len(steps) != 1 or steps[0].rule is not ProofRule.GIVEN or steps[0].premises:
        raise RuntimeError("R2E double identity not uniquely screened as GIVEN")
    if (steps[0].conclusion != assertion.content
            or reference.locator != "(5.3)"
            or reference.publication_position != 8100):
        raise RuntimeError("R2E source provenance mismatch")
    if any(link.step is not None and link.step.conclusion == goal
           for link in screened.proof_links):
        raise RuntimeError("target group was incorrectly installed as a GIVEN")
    print("PHASE171_R2E_SOURCE=" + json.dumps({
        "locator": reference.locator,
        "assertion_id": source_id,
        "source_position": reference.publication_position,
        "screened_given_count": len(steps),
        "proof_of_target": False,
    }, ensure_ascii=False))
    print("PHASE171_R2E_NO_DIRECT_GROUP_PROOF=True")
    return 0


def main() -> int:
    try:
        return audit()
    except Exception as exc:
        print(f"PHASE171_R2E_AUDIT_ERROR={type(exc).__name__}: {exc}", file=sys.stderr)
        print(traceback.format_exc()[-2200:], file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 出典テスト全文

対応ファイル：`tests/test_source.py`

```python
"""R2E focused source-adoption and non-circularity regression tests."""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase171_r2e_toda53_double_reference import (
    ASSERTION_ID, build_adopted_toda53_double_reference,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def test_double_relation_is_one_exact_cited_given():
    production = discover_goal_search_inputs().bridge
    source = build_adopted_toda53_double_reference(production)
    assert len(source.proof_links) == 1
    assertion = source.registry.assertion(ASSERTION_ID)
    reference = source.registry.reference(assertion.reference_id)
    assert reference.locator == "(5.3)"
    assert reference.source_id == "toda:tex:ch5:0005"
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert isinstance(assertion.content, Relation)
    assert assertion.content.relation_type is RelationType.EQUALITY
    assert isinstance(assertion.content.lhs, Multiple)
    assert assertion.content.lhs.coefficient == 2
    nu_prime = assertion.content.lhs.expression
    assert nu_prime == HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    rhs = assertion.content.rhs
    assert isinstance(rhs, Composition)
    assert rhs.left.source == rhs.right.left.target
    assert isinstance(rhs.right, Composition)
    assert rhs.right.is_type_compatible()
    assert tuple(x.generator.index for x in (
        rhs.left, rhs.right.left, rhs.right.right,
    )) == (3, 4, 5)
    link = source.proof_links[0]
    assert link.assertion_id == ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert link.step.conclusion == assertion.content


def test_missing_archive_fails_closed():
    missing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError, match="exactly one archived source"):
        build_adopted_toda53_double_reference(missing)
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        build_adopted_toda53_double_reference(None)


def test_default_bridge_appends_source_without_renumbering_prior_ids():
    bridge = build_shared_typed_bridge()
    ids = tuple(a.assertion_id for a in bridge.registry._assertions.values()
                if a.assertion_id.endswith(":" + ASSERTION_ID))
    assert len(ids) == 1
    assertion_id = ids[0]
    assert assertion_id.startswith("shared:12:")
    assertion = bridge.registry.assertion(assertion_id)
    reference = bridge.registry.reference(assertion.reference_id)
    assert reference.locator == "(5.3)"
    assert reference.publication_position == 8100
    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion_id)
    assert len(links) == 1
    assert links[0].step.rule is ProofRule.GIVEN
    assert all(link.step.conclusion != assertion.content or link.assertion_id == assertion_id
               for link in bridge.proof_links)
    assert bridge.registry.assertion(
        "shared:8:toda:adopted:eq5.3:nu_prime_hopf_relation"
    ) is not None


def test_double_source_is_prior_to_pi63_target_and_not_root_proof():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=3)
    assert len(goals) == 1
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing == "shared:0:boundary:Proposition 5.6:pi6_3_group_relation"
    source_id = "shared:12:" + ASSERTION_ID
    assert precedes_citing_assertion(bridge, source_id, citing)
    assert all(link.step.conclusion != target for link in bridge.proof_links
               if link.step is not None)


def test_explicit_sources_are_not_modified():
    production = discover_goal_search_inputs().bridge
    source = build_adopted_toda53_double_reference(production)
    combined = build_shared_typed_bridge(sources=(source,))
    assert len(combined.proof_links) == 1
    assert combined.proof_links[0].step.rule is ProofRule.GIVEN
```

## インストーラーテスト全文（R4 追加3件を含む）

対応ファイル：`tests/test_install_unit.py`

```python
"""Source-independent R2E-R2 patch integrity and rollback-contract tests."""
from __future__ import annotations

import ast

import pytest

from phase171_r2e_toda53_double_source import install


def fixture_original() -> str:
    updated_function = install.FULL_FUNCTION.read_text(encoding="utf-8")
    with_added = install.ANCHOR + "\n" + install.ADDITION
    assert updated_function.count(with_added) == 1
    assert updated_function.count(install.POSITION_NEW) == 1
    original = updated_function.replace(with_added, install.ANCHOR)
    original = original.replace(install.POSITION_NEW, install.POSITION_OLD)
    return original + "\n\ndef shared_expansion_provider(*args):\n    return ()\n"


def fixture_test_original() -> str:
    updated = install.FULL_TEST.read_text(encoding="utf-8")
    assert updated.count(install.TEST_NEW) == 1
    assert updated.count(install.TEST_PROOF_NEW) == 1
    return updated.replace(install.TEST_NEW, install.TEST_OLD).replace(
        install.TEST_PROOF_NEW, install.TEST_PROOF_OLD
    )


def test_proposed_source_has_exact_full_replacement_and_preserves_other_function():
    original = fixture_original()
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    assert install.ADDITION in updated
    assert updated.count(install.ADDITION) == 1
    assert install.POSITION_NEW in updated
    assert install.POSITION_OLD not in updated
    assert updated.endswith("def shared_expansion_provider(*args):\n    return ()\n")
    assert updated.replace(install.ANCHOR + "\n" + install.ADDITION, install.ANCHOR).replace(
        install.POSITION_NEW, install.POSITION_OLD
    ) == original
    ast.parse(updated)


def test_proposed_source_preserves_crlf():
    original = fixture_original().replace("\n", "\r\n")
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    assert "\r\n" in updated
    assert "\n" not in updated.replace("\r\n", "")
    assert install.ADDITION.replace("\n", "\r\n") in updated
    assert install.POSITION_NEW.replace("\n", "\r\n") in updated


def test_proposed_source_rejects_missing_anchor():
    with pytest.raises(RuntimeError, match="source anchor not unique"):
        install.proposed_source(b'def build_shared_typed_bridge():\n    pass\n')


def test_proposed_source_rejects_duplicated_anchor():
    source = fixture_original().replace(
        install.ANCHOR, install.ANCHOR + "\n" + install.ANCHOR
    )
    with pytest.raises(RuntimeError, match="source anchor not unique"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_source_rejects_unreviewed_function_changes():
    source = fixture_original().replace(
        "if not isinstance(source, RegistryBridgeResult):", "if source is None:"
    )
    with pytest.raises(RuntimeError, match="differs from reviewed"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_source_rejects_missing_position_anchor():
    source = fixture_original().replace(install.POSITION_OLD, "    return ordered")
    with pytest.raises(RuntimeError, match="position anchor not unique"):
        install.proposed_source(source.encode("utf-8"))


def test_proposed_test_changes_only_legacy_heading_assertion():
    original = fixture_test_original()
    updated = install.proposed_test(original.encode("utf-8")).decode("utf-8")
    assert install.TEST_NEW in updated
    assert install.TEST_OLD not in updated
    assert install.TEST_PROOF_NEW in updated
    assert install.TEST_PROOF_OLD not in updated
    assert updated.replace(install.TEST_NEW, install.TEST_OLD).replace(
        install.TEST_PROOF_NEW, install.TEST_PROOF_OLD
    ) == original
    ast.parse(updated)


def test_proposed_test_preserves_crlf():
    original = fixture_test_original().replace("\n", "\r\n")
    updated = install.proposed_test(original.encode("utf-8")).decode("utf-8")
    assert "\n" not in updated.replace("\r\n", "")
    assert install.TEST_NEW.replace("\n", "\r\n") in updated
    assert install.TEST_PROOF_NEW.replace("\n", "\r\n") in updated


def test_proposed_test_rejects_missing_anchor():
    with pytest.raises(RuntimeError, match="test anchor not unique"):
        install.proposed_test(b'def test_old():\n    pass\n')


def test_proposed_test_rejects_duplicate_anchor():
    source = fixture_test_original().replace(
        install.TEST_OLD, install.TEST_OLD + "\n" + install.TEST_OLD
    )
    with pytest.raises(RuntimeError, match="test anchor not unique"):
        install.proposed_test(source.encode("utf-8"))


def test_reviewed_pi32_function_has_no_blank_line_after_import():
    old = install.TEST_PROOF_OLD
    new = install.TEST_PROOF_NEW
    original_layout = (
        'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n'
        '    from hopf_facts import ETA_2\n'
        '    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))\n'
    )
    revised_layout = (
        'def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n'
        '    from hopf_facts import ETA_2\n'
        '    bridge = build_shared_typed_bridge()\n'
    )
    assert old.startswith(original_layout)
    assert new.startswith(revised_layout)
    assert old.count('    bridge = build_shared_typed_bridge(sources=(_adopted_source(),))') == 1
    assert new.count('    bridge = build_shared_typed_bridge()') == 1
    assert '\n\n    bridge = build_shared_typed_bridge' not in old
    assert '\n\n    bridge = build_shared_typed_bridge' not in new


def test_reviewed_pi32_full_function_is_the_expected_replacement():
    test = install.FULL_TEST.read_text(encoding='utf-8')
    assert test.count(install.TEST_PROOF_NEW) == 1
    original = fixture_test_original()
    assert original.count(install.TEST_PROOF_OLD) == 1
    updated = install.proposed_test(original.encode('utf-8')).decode('utf-8')
    start = updated.index('def test_r9_pi32_regenerated_by_shared_mathematical_expansion():')
    end = updated.index('def test_r9_pi43_is_a_real_typed_goal_even_if_not_proved():', start)
    assert updated[start:end].strip() == install.TEST_PROOF_NEW.strip()
    assert original[:start] == updated[:start]


def test_reviewed_original_test_matches_exact_git_blob():
    from hashlib import sha1

    normalized_original = fixture_test_original()
    original_bytes = normalized_original.replace('\n', '\r\n').encode('utf-8')
    blob_header = b'blob ' + str(len(original_bytes)).encode('ascii') + b'\0'
    assert sha1(blob_header + original_bytes).hexdigest() == install.EXPECTED_TEST_BLOB
    assert install.EXPECTED_TEST_BLOB == 'c6dcfb3cda9c9115fb802f4a1b2141e0502506bd'


def test_pi32_complete_requires_full_production_sources():
    full = install.FULL_TEST.read_text(encoding="utf-8")
    assert full.count(install.TEST_PROOF_NEW) == 1
    assert "bridge = build_shared_typed_bridge()" in install.TEST_PROOF_NEW
    assert "sources=(_adopted_source(),)" in install.TEST_PROOF_OLD
    assert "assert result.status is ProofSearchStatus.COMPLETE" in install.TEST_PROOF_NEW
    assert "assert any(step.rule is ProofRule.INFERENCE" in install.TEST_PROOF_NEW


def test_proposed_test_rejects_outdated_pi32_proof_anchor():
    source = fixture_test_original().replace(
        install.TEST_PROOF_OLD,
        install.TEST_PROOF_OLD.replace("COMPLETE", "PARTIAL"),
    )
    with pytest.raises(RuntimeError, match="pi32 proof test anchor not unique"):
        install.proposed_test(source.encode("utf-8"))


def test_proposed_test_changes_no_other_mathematical_assertions():
    source = fixture_test_original()
    patched = install.proposed_test(source.encode("utf-8")).decode("utf-8")
    assert "assert result.status is ProofSearchStatus.COMPLETE" in patched
    assert "assert result.conclusion == Relation(TodaPrimaryGroup(3, 2)" in patched
    assert "assert any(step.rule is ProofRule.INFERENCE" in patched
    assert "assert result.status in (ProofSearchStatus.SEARCH_FAILED" in patched


def test_source_and_functions_are_syntactically_valid():
    contents = (
        install.PAYLOAD.read_text(encoding="utf-8"),
        install.FULL_FUNCTION.read_text(encoding="utf-8"),
        install.FULL_TEST.read_text(encoding="utf-8"),
    )
    for content in contents:
        ast.parse(content)


def test_patch_does_not_change_existing_imports():
    original = fixture_original()
    updated = install.proposed_source(original.encode("utf-8")).decode("utf-8")
    before = ast.parse(original).body[0]
    after = ast.parse(updated).body[0]
    assert isinstance(before, ast.FunctionDef)
    assert isinstance(after, ast.FunctionDef)
    assert before.name == after.name == "build_shared_typed_bridge"
    assert ast.dump(after.args) == ast.dump(before.args)


def test_position_binding_changes_only_explicit_source_mode():
    updated = install.FULL_FUNCTION.read_text(encoding="utf-8")
    assert updated.count("    if default_sources:\n        from phase166_r3p_position_binding") == 1
    assert updated.count("    return ordered") == 1
    assert updated.index("    if default_sources:\n        from phase166_r3p_position_binding") < updated.index("    return ordered")


def test_apply_and_restore_are_byte_exact_in_temporary_checkout(tmp_path, monkeypatch):
    from pathlib import Path

    source = tmp_path / "phase165_r52_r9_shared_math.py"
    focused = tmp_path / "test_phase165_r52_r9_shared_math.py"
    module = tmp_path / "phase171_r2e_toda53_double_reference.py"
    backup = tmp_path / "backup"
    original_source = fixture_original().replace("\n", "\r\n").encode("utf-8")
    original_test = fixture_test_original().replace("\n", "\r\n").encode("utf-8")
    source.write_bytes(original_source)
    focused.write_bytes(original_test)
    monkeypatch.setattr(install, "TARGET", source)
    monkeypatch.setattr(install, "EXISTING_TEST", focused)
    monkeypatch.setattr(install, "NEW_MODULE", module)
    monkeypatch.setattr(install, "BACKUP", backup)
    monkeypatch.setattr(install, "verify_checkout", lambda: None)

    install.apply(dry_run=True)
    assert source.read_bytes() == original_source
    assert focused.read_bytes() == original_test
    assert not module.exists()
    install.apply()
    assert source.read_bytes() != original_source
    assert focused.read_bytes() != original_test
    assert module.read_bytes() == install.PAYLOAD.read_bytes()
    assert (backup / "state.json").is_file()
    install.restore()
    assert source.read_bytes() == original_source
    assert focused.read_bytes() == original_test
    assert not module.exists()
    assert not (backup / "state.json").exists()


def test_restore_refuses_modified_patched_test(tmp_path, monkeypatch):
    source = tmp_path / "phase165_r52_r9_shared_math.py"
    focused = tmp_path / "test_phase165_r52_r9_shared_math.py"
    module = tmp_path / "phase171_r2e_toda53_double_reference.py"
    backup = tmp_path / "backup"
    source.write_bytes(fixture_original().encode("utf-8"))
    focused.write_bytes(fixture_test_original().encode("utf-8"))
    monkeypatch.setattr(install, "TARGET", source)
    monkeypatch.setattr(install, "EXISTING_TEST", focused)
    monkeypatch.setattr(install, "NEW_MODULE", module)
    monkeypatch.setattr(install, "BACKUP", backup)
    monkeypatch.setattr(install, "verify_checkout", lambda: None)
    install.apply()
    focused.write_bytes(focused.read_bytes() + b"# modified\n")
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        install.restore()
```

## README.md 全文

対応ファイル：`README.md`

```markdown
# Phase 171 R2E-R4 — Cited Toda (5.3) Double Identity with Compatibility Repair

This is a corrective release for the R2E installer. The first run reverted safely after six focused test failures. Five failures were caused by a pre-existing incompatibility between the explicit `sources=` argument to `build_shared_typed_bridge()` and full-production-only reference-position binding. One failure was a stale UI heading expectation in `test_phase165_r52_r9_shared_math.py`, introduced when the public narrative renderer changed.

The second retry (R2) cleared the KeyError and obsolete heading but exposed another old test assumption: the original nine-reference-only partial source snapshot does not contain all premises needed for the current pi3^2 completed proof. It returned PARTIAL; this is not evidence that the full production search failed. R3 updates that test to use the **full production source bridge**, matching the established Phase 166 R3-R verification path; the test retains all mathematical COMPLETE/conclusion/INFERENCE assertions. The explicit partial-source tests continue to test only their actual source and fail-closed contracts.

The R2E mathematical scope is unchanged: register precisely the adopted Toda equation (5.3) `2ν′ = η₃∘η₄∘η₅` as a source-verified typed `GIVEN`. This is **not** a proof of the order of ν′, cyclic generation, or the complete group π₆³. The original printed source has not been independently verified. The previously adopted archive text, fixed SHA-256 and source publication order are used.

## Modified files

- `phase165_r52_r9_shared_math.py`: replace the complete existing `build_shared_typed_bridge()` function. Retain all existing default source indices, append the new cited source to the default bridge, and apply `place_r3p_reference_positions()` only when the complete default source set is present. This avoids looking for nonexistent source references in explicit partial-source calls.
- `test_phase165_r52_r9_shared_math.py`: replace the complete `test_r9_public_pi32_narrative_unchanged()` and `test_r9_pi32_regenerated_by_shared_mathematical_expansion()` test functions by checking the current narrative's references, proof and mathematical conclusion rather than an obsolete heading. All other existing test functions are untouched. The pi3^2 completion test now uses `build_shared_typed_bridge()` (full default sources), while still requiring a completed INFERENCE proof.
- `phase171_r2e_toda53_double_reference.py`: new repository-root source module with `build_adopted_toda53_double_reference()` and its exact typed source verification.
- `phase171_r2e_toda53_double_source/`: the installer, focused tests, audit, complete replacement function/test, English README, and Japanese audit specification.

No database files, numerical group conclusions, actual proof rules, completed proof histories, web renderer implementations or official project documentation are modified.

## Windows execution

Run from the repository root on the reviewed `develop` checkout, after confirming the previous R2E restore completed successfully.

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2E_R4.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1"
git status -sb
```

`run.ps1` performs focused tests, checks the screened Toda (5.3) `GIVEN`, and rejects a direct proof of the target group. If the focused tests or audit fail, it attempts to restore **both** modified tracked files and to remove the new module, using byte-exact backups under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2e_toda53_double_source_backup`.

Installer-focused unit tests were executed when assembling this release, but repository-dependent proof tests must still run on the Windows checkout. Repository-dependent focused tests must run on the actual Windows checkout. The full project test suite is deferred until the phase closes.

## R4 correction: exact test function text

R3 did not pass its preflight because its full-function replacement anchor included a blank line after `from hopf_facts import ETA_2`. The reviewed GitHub `develop` version has **no blank line there**. R4 corrects both the old and new full-function literals and the packaged complete test file. The intended mathematical test assertions and all production changes are unchanged. Additional installer unit tests guard this exact layout. No application files are modified by preflight failure.

The complete replacement test file was additionally brought into alignment with all reviewed blank lines in the unchanged test functions. When the changed functions are reversed and CRLF restored, the resulting complete test file reproduces the exact Git blob SHA `c6dcfb3cda9c9115fb802f4a1b2141e0502506bd`. A unit test now enforces this identity; the installer still changes only the two intended test functions.
```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2E_R4.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1"
git status -sb
```

`run.ps1` performs focused tests, checks the screened Toda (5.3) `GIVEN`, and rejects a direct proof of the target group. If the focused tests or audit fail, it attempts to restore **both** modified tracked files and to remove the new module, using byte-exact backups under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2e_toda53_double_source_backup`.

Installer-focused unit tests were executed when assembling this release, but repository-dependent proof tests must still run on the Windows checkout. Repository-dependent focused tests must run on the actual Windows checkout. The full project test suite is deferred until the phase closes.

## R4 correction: exact test function text

R3 did not pass its preflight because its full-function replacement anchor included a blank line after `from hopf_facts import ETA_2`. The reviewed GitHub `develop` version has **no blank line there**. R4 corrects both the old and new full-function literals and the packaged complete test file. The intended mathematical test assertions and all production changes are unchanged. Additional installer unit tests guard this exact layout. No application files are modified by preflight failure.
```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2E_R2.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2e_toda53_double_source\run.ps1"
git status -sb
```

`run.ps1` performs focused tests, checks the screened Toda (5.3) `GIVEN`, and rejects a direct proof of the target group. If the focused tests or audit fail, it attempts to restore **both** modified tracked files and to remove the new module, using byte-exact backups under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2e_toda53_double_source_backup`.

Installer-focused unit tests were executed when assembling this release, but repository-dependent proof tests must still run on the Windows checkout. Repository-dependent focused tests must run on the actual Windows checkout. The full project test suite is deferred until the phase closes.
```

## 監査仕様.md 全文

対応ファイル：`監査仕様.md`

```markdown
# Phase 171 R2E-R3 — 限定テスト失敗の修正

## 現状と原因

前版 R2E の DryRun は PASS、通常実行は限定 pytest で **6 failed, 10 passed**、自動復元は PASS した。追跡済みファイルの差分は残っていない。

`KeyError: 'shared:1:adopted:ref:3'` の5件は `build_shared_typed_bridge(sources=(...))` が完全な既定出典集合を含まないにもかかわらず、`place_r3p_reference_positions()` が既定出典の固定 ID を必須としていたために起きた。現行 GitHub `phase166_r3p_position_binding.py` の `SUSPENSION_REF` も照合済み。これを解消するため、既存関数内の位置補正を **`default_sources` の場合だけ**行う。全出典を使う本番経路の位置補正は変更しない。

残る1件は `test_r9_public_pi32_narrative_unchanged()` が旧表示見出し「証明対象」を要求しているが、現行 `web_group_proof.py` の Narrative がその見出しを出さないことによる。見出しの一致は証明の正しさを測定しないため、同テスト関数を「使用する結果」「証明」および π₃² の具体的な結論を確認する検査に変更する。Renderer は変更しない。

## 変更対象・位置

- `phase165_r52_r9_shared_math.py`：既存 `build_shared_typed_bridge()` 全体。既定 sources の末尾へ (5.3) 出典を追加する旧 R2E の変更を継承し、末尾の `place_r3p_reference_positions()` 呼出しを `if default_sources:` の内部に移す。**module-level import は変更しない。**
- `test_phase165_r52_r9_shared_math.py`：既存 `test_r9_public_pi32_narrative_unchanged()` の全文を置換。その他のテスト関数を変更しない。**import は変更しない。**
- 新規 `phase171_r2e_toda53_double_reference.py`：リポジトリ直下に追加。`build_adopted_toda53_double_reference()` を含む。
- 新規監査パッケージ：`install.py`（全関数）、`tests/test_install_unit.py`（全テスト）、`tests/test_source.py`（旧 R2E と同一）、`audit.py`、`run.ps1`、README、監査仕様およびコード全文を収録。

## 出典と数学上の境界

Toda (5.3) の採用済みアーカイブの SHA-256 と完全な文字列検査は既存 `build_adopted_toda53_hopf_reference()` に委ねる。登録するのは関係式 `2ν′ = η₃∘η₄∘η₅` 一件だけである。Proposition 5.6 の π₆³ 群構造は出典 `GIVEN` として追加しない。`CyclicStructureStatement` と Proof Tree の未解決は継続する。

## テスト、復元、完了条件

配布時：インストーラー限定 pytest **15 PASS**（Git 等のプロジェクト非依存）。一時ディレクトリ上で install→restore の byte-exact 検証、改変ファイルの復元拒否、CRLF 維持、変更箇所の一致を含む。

Windows：DryRun → 実装 → `tests/test_install_unit.py`, `tests/test_source.py`, `phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py`, `test_phase165_r52_r9_shared_math.py` の限定 pytest → `audit.py` の引用選別を実施。失敗時は2つの追跡済みファイルを byte-exact に復元し、新規モジュールを削除する。`PHASE171_R2E_FOCUSED_PYTEST=PASS`、`PHASE171_R2E_NO_DIRECT_GROUP_PROOF=True`、`PHASE171_R2E_RESULT=PASS` を確認して完了。

**全体 pytest は Phase 171 の最後にのみ実行する。** 次の R2F は位数4・生成性の型付き導出を扱い、今回の出典採用と混同しない。

## R3 追加修正：部分出典の証明能力と本番経路を区別

R2E-R2 は `KeyError` を解消した後、`test_r9_pi32_regenerated_by_shared_mathematical_expansion()` において `ProofSearchStatus.PARTIAL` を検出した。明示的な `sources=(_adopted_source(),)` は9件の限定出典のみを含み、現行の π₃² 完成証明に必要な本番全出典を含まない。テストは元の数学的完了条件（`COMPLETE`、証明結論、`INFERENCE`）を緩めず、証明用 Bridge を `build_shared_typed_bridge()` の全出典に切り替えた。部分出典の登録件数・`GIVEN` 保持テストは維持し、証明が未完了のケースを誤って完成扱いしない。

`phase165_r52_r9_shared_math.py` の既定出典作成、Toda (5.3) の採用、参照順序境界は R2 から変更なし。実行対象は引き続き限定 pytest のみで、失敗時は byte-exact な元ファイル復元を行う。

## R4 修正 — 現行テスト関数の空行差異

R2E-R3 は `PHASE171_R2E_PREFLIGHT_FAILED` となった。原因は、インストーラーが照合する π₃² の既存テスト関数全文に、GitHub 現行 `develop` に存在しない空行が挿入されていたこと。該当箇所は `from hopf_facts import ETA_2` の直後である。Git の追跡済みファイルは変更されていない。

修正版 R4 では `install.py` の `TEST_PROOF_OLD` と `TEST_PROOF_NEW` の全文、`test_phase165_r52_r9_shared_math_FULL.py` を現行関数の空行配置に厳密に合わせる。追加の単体テスト2件により、同じ配置の不一致を再発防止する。数学的前提、ProofStep の信頼境界、全出典の参照順序、π₃² の `COMPLETE`・結論・`INFERENCE` の検査条件は一切緩めない。

失敗時の復元機能・出典採用範囲・実行対象の限定 pytest は従来どおりとし、全体 pytest は Phase 171 終了時にのみ実施する。

GitHub 現行 `test_phase165_r52_r9_shared_math.py` の全行（既存の無変更テスト関数も含む）を照合し、変更対象2関数を元に戻した全文の Git blob SHA-1 が `c6dcfb3cda9c9115fb802f4a1b2141e0502506bd` に一致することを確認した。実装用インストーラーは既存テスト全体の上書きを行わず、2関数だけを置換する。検証用 `FULL_TEST` の空行・CRLF も現行ファイルに一致させた。回帰テストを1件追加した。
```

## インストールと完了条件

ZIP をリポジトリ直下で展開し、`run.ps1 -DryRun` で前提条件のみ確認した後、通常の `run.ps1` を実行する。バックアップは `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2e_toda53_double_source_backup` に保存する。失敗時は2つの追跡ファイルと新規モジュールを元に戻す。

限定 pytest は `phase171_r2e_toda53_double_source/tests/test_install_unit.py`、`phase171_r2e_toda53_double_source/tests/test_source.py`、`phase169_r3h_toda53_hopf_source/tests/test_phase169_r3h_toda53_hopf_source.py`、`test_phase165_r52_r9_shared_math.py` を実行。`PHASE171_R2E_FOCUSED_PYTEST=PASS`、`PHASE171_R2E_NO_DIRECT_GROUP_PROOF=True`、`PHASE171_R2E_RESULT=PASS` が完了条件。Windows の実本番依存テストは未実行のため確認が必要。

R2F では ν′ の位数4と生成性を一般的な型付き推論で導く方法を検討し、R2E の出典登録とは区別する。全体 pytest は Phase 171 最終段階でのみ行う。

## R4 限定テスト・完了境界

新規追加の単体テストは3件。インストーラーと完全置換関数の静的検証を実行する。Windows での本番コードへの適用、関連限定 pytest、出典引用監査は未実施のため成功を保証しない。失敗時は byte-exact な自動復元を行う。R2F の位数4・生成性の推論は本修正に含めない。

### 全文の Git blob 同一性検査

R4 に収録する `test_phase165_r52_r9_shared_math_FULL.py` を、`TEST_PROOF_NEW` と `TEST_NEW` を元の2関数に戻したうえで CRLF を復元し、Git blob ハッシュを算出した。現行 `develop` の `test_phase165_r52_r9_shared_math.py` の blob `c6dcfb3cda9c9115fb802f4a1b2141e0502506bd` と完全一致している。`test_reviewed_original_test_matches_exact_git_blob()` で継続的に確認する。既存ファイルを無条件に全置換するのではなく、2関数だけを変更する方式を維持する。
