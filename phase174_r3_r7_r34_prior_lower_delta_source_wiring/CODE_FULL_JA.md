# R34 変更コード全文・置換単位

## 変更対象

既存ファイル `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge` のみ。トップレベル import は変更なし。関数内にだけ出典登録の import を追加。既存テストは変更しない。新規ソースとテストの追加位置は `phase174_r3_r7_r34_prior_lower_delta_source_wiring/` 以下。

## 本番関数の置換単位全体: `phase165_r52_r9_shared_math.py::build_shared_typed_bridge`

変更後の関数全文です。実行時は同じ変更を単一アンカーで差し込む Installer を利用してください。既存モジュールを手作業で全上書きする必要はありません。

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
        from phase171_r2h_prop22_cited_hopf.source import (
            build_cited_prop22_right_reference,
        )
        sources = sources + (build_cited_prop22_right_reference(production),)
        from phase174_r3_r6_source_extension.source import build_cited_extension_sources
        sources = sources + (build_cited_extension_sources(),)
        from phase174_r3_r6_r2_prop44_lemma54.source import (
            build_cited_preprop44_splitting,
        )
        sources = sources + (build_cited_preprop44_splitting(),)
        from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
            build_isolated_toda59_annihilator_bridge,
        )
        sources = sources + (build_isolated_toda59_annihilator_bridge(),)
        from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
            register_positioned_prop27,
        )
        sources = sources + (register_positioned_prop27(Path(__file__).resolve().parent),)
        from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
            build_cited_lower_delta_sources,
        )
        sources = sources + (
            build_cited_lower_delta_sources(Path(__file__).resolve().parent),
        )
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

## 新規ファイルの完全版

全新規ファイルの全文（import を含む）です。コードの `...` による省略はありません。


### 出典登録（新規）: `source.py`

```python
"""Cite two independently printed prior facts for the lower EHP Delta.

Only Toda Proposition 5.8 and equation (5.10) are added as FIXED_STATEMENT
leaves. Their generator is checked against the real structured DB prior, but
DB data does not independently certify the mathematics. No kernel, top Delta,
or root group is asserted; no proof search or renderer is overridden.
"""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3aj_structured_generator import structured_generator_from_ids
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from proof import (
    InferenceRule,
    LiteratureReference,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "sources/toda/Toda_05_2.tex"
SOURCE_BLOB = "579661138928499ba04a51327f686d9b971b5314"
PROP58 = r"\begin{proposition}\label{prop:5.8}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
EQ510 = r"\begin{equation}\label{eq:5.10}"
CODOMAIN_CLAUSE = r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
IMAGE_CLAUSE = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
MANIFEST_ROWS = (
    ("Proposition 5.8", "toda:Proposition 5.8", "toda:tex:ch5:0016", ReferenceKind.PROPOSITION),
    ("(5.10)", "toda:(5.10)", "toda:tex:ch5:0018", ReferenceKind.EQUATION),
)


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def pinned_source_text(root: Path = ROOT) -> str:
    """Require exact reviewed Toda bytes modulo whole-file CRLF/LF handling."""
    data = (root / SOURCE).read_bytes()
    normalized = data.replace(b"\r\n", b"\n")
    if SOURCE_BLOB not in (
        git_blob_sha(data), git_blob_sha(normalized),
        git_blob_sha(normalized.replace(b"\n", b"\r\n")),
    ):
        raise ValueError("Toda source bytes differ from reviewed GitHub blob")
    text = normalized.decode("utf-8-sig")
    if any(text.count(boundary) != 1 for boundary in (PROP58, EQ510, PROP59)):
        raise ValueError("Prior-source anchors are missing or ambiguous")
    i58, i510, i59 = (text.index(boundary) for boundary in (PROP58, EQ510, PROP59))
    if not (i58 < i510 < i59):
        raise ValueError("Printed prior-source order changed")
    end58 = text.find(r"\end{proposition}", i58)
    end510 = text.find(r"\end{equation}", i510)
    if end58 < 0 or end510 < 0 or not (end58 < i510 < end510 < i59):
        raise ValueError("Printed prior-source boundaries changed")
    if text[i58:end58].count(CODOMAIN_CLAUSE) != 1:
        raise ValueError("Printed finite cyclic codomain clause changed")
    if text[i510:end510].count(IMAGE_CLAUSE) != 1:
        raise ValueError("Printed lower Delta generator image clause changed")
    return text


def reviewed_source_positions(manifest: Path = DEFAULT_MANIFEST) -> tuple[int, int]:
    """Require exact source IDs; no hand-assigned order or new target citation."""
    positions, rows, _manifest = _load_manifest_reference_order(manifest)
    selected: list[int] = []
    for locator, ref_id, source_id, _kind in MANIFEST_ROWS:
        matches = rows.get(ref_id, ())
        if (len(matches) != 1
                or matches[0].get("statement_id") != source_id
                or matches[0].get("locator") != locator):
            raise ValueError("Reviewed prior citation ID changed: " + locator)
        position = positions.get(ref_id)
        if type(position) is not int or position <= 0:
            raise ValueError("Prior-source publication position not reviewed")
        selected.append(position)
    if selected[0] >= selected[1]:
        raise ValueError("Prior-source publication positions reversed")
    return selected[0], selected[1]


def checked_prior_statements(root: Path = ROOT) -> tuple[Relation, TodaDeltaImageUpToSignStatement]:
    """Transcribe printed prior claims with exact, checked structural generator."""
    pinned_source_text(root)
    domain = TodaPrimaryGroup(11, 11)
    codomain = TodaPrimaryGroup(9, 5)
    stored = exact_prior_database_result(
        5, 4, csv_path=root / "data" / "sphere.csv",
        generator_csv=root / "data" / "HyoujiGen.csv",
    )
    if (type(stored) is not Relation
            or stored.relation_type is not RelationType.EQUALITY
            or stored.lhs != codomain
            or type(stored.rhs) is not FiniteCyclicGroup
            or stored.rhs.order != 2
            or type(stored.rhs.generator) is not Composition
            or not stored.rhs.generator.is_type_compatible()):
        raise ValueError("Structured pi_9^5 presentation differs from the printed source")
    expected = structured_generator_from_ids(
        ids=(4, 2), start_dimension=5,
        generator_csv=root / "data" / "HyoujiGen.csv",
    )
    if (expected is None or stored.rhs.generator != expected):
        raise ValueError("Structured nu_5 eta_8 generator mismatches the adopted source")
    generator = HomotopyElement(
        name="ι_11", dimension=11, source=11, target=11,
        generator=GeneratorSymbol(family="ι", index=11),
    )
    lower = TodaDeltaMap(domain, codomain)
    image = TodaDeltaImageUpToSignStatement(
        map=lower, element=generator, positive_value=stored.rhs.generator,
    )
    return stored, image


def build_cited_lower_delta_sources(
    root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    """Register exactly two earlier facts; no generated goal or inference rule."""
    positions = reviewed_source_positions(manifest)
    group, image = checked_prior_statements(root)
    registry = UnifiedStatementRegistry()
    links: list[ProofStepLink] = []
    records: list[MigrationRecord] = []
    for (locator, reference_id, source_id, kind), position, claim in zip(
        MANIFEST_ROWS, positions, (group, image)
    ):
        assertion_id = "toda:174:r3r7r34:prior:" + reference_id
        registry.add_reference(LiteratureEntry(
            reference_id=reference_id,
            kind=kind,
            locator=locator,
            source_id=source_id,
            publication_position=position,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=reference_id,
            kind=AssertionKind.STATEMENT,
            content=claim,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=("prior source only", "not Proposition 5.9 conclusion"),
        ))
        links.append(ProofStepLink(assertion_id=assertion_id, step=ProofStep(
            conclusion=claim,
            premises=(),
            rule=ProofRule.GIVEN,
            note="Adopted Toda transcription; original edition unverified",
            inference_rule=InferenceRule(
                name="Cited prior Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
        records.append(MigrationRecord(
            source="phase174_r3_r7_r34",
            source_key=source_id,
            assertion_id=assertion_id,
            status=MigrationStatus.STRUCTURED,
            detail="Checked earlier source claim; no Proposition 5.9 conclusion admitted",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))
```

### 安全な設置手順（新規）: `install.py`

```python
"""R34 guarded installer for two cited prior-source leaves only.

Refuses unreviewed production edits. Does not reset, stage, or commit the
checkout, and leaves every earlier phase package intact.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    ROOT,
    checked_prior_statements,
    git_blob_sha,
    reviewed_source_positions,
)

BASE_HEAD = "8a1fa3c52264ba8544ad24cd68e24316963e090f"
SINGLE_REVIEWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r33_three_premise_source_frontier/"
PRODUCTION = "phase165_r52_r9_shared_math.py"
BASE_BLOB = "742451ea67ede314f99246afbb470a5e8a7f008f"
ANCHOR = (
    "        sources = sources + "
    "(register_positioned_prop27(Path(__file__).resolve().parent),)"
)
ADDITION = (
    "        from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (\n"
    "            build_cited_lower_delta_sources,\n"
    "        )\n"
    "        sources = sources + (\n"
    "            build_cited_lower_delta_sources(Path(__file__).resolve().parent),\n"
    "        )"
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def reviewed_remote_head() -> str:
    """Allow only an exact HEAD or a successor adding only unchanged R33 files."""
    response = git("ls-remote", "origin", "refs/heads/develop")
    remote = response.split()[0] if response else ""
    if not remote:
        raise RuntimeError("Cannot verify GitHub origin/develop")
    if remote == BASE_HEAD:
        return remote
    git("fetch", "-q", "origin", "develop")
    if git("rev-parse", "FETCH_HEAD") != remote:
        raise RuntimeError("Remote HEAD advanced during source review")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
        cwd=ROOT, capture_output=True,
    )
    if ancestor.returncode:
        raise RuntimeError("GitHub lineage differs from reviewed R33 base")
    additions = git("diff", "--name-status", BASE_HEAD, remote).splitlines()
    if not additions or any(
        not item.startswith("A\t" + SINGLE_REVIEWED_SUCCESSOR_PREFIX)
        for item in additions
    ):
        raise RuntimeError("GitHub advanced outside reviewed R33 package; re-review")
    return remote


def patch_source(original: str) -> str:
    """Insert the exact R34 source builder once into the existing source tuple."""
    if type(original) is not str:
        raise TypeError("R34 installer accepts str source only")
    if original.count(ANCHOR) != 1:
        raise RuntimeError("Shared provider R30 anchor changed or is ambiguous")
    if original.count(ADDITION) == 1:
        return original
    if "build_cited_lower_delta_sources" in original:
        raise RuntimeError("Partial or unreviewed R34 source wiring found")
    return original.replace(ANCHOR, ANCHOR + "\n" + ADDITION, 1)


def expected_source_bytes(original: bytes) -> bytes:
    """Preserve source-file LF/CRLF faithfully rather than rewriting a tree."""
    if git_blob_sha(original) != BASE_BLOB:
        raise RuntimeError("Reviewed original production Git blob differs")
    text = original.decode("utf-8")
    if "\r\n" in text:
        patch = patch_source(text.replace("\r\n", "\n"))
        return patch.replace("\n", "\r\n").encode("utf-8")
    return patch_source(text).encode("utf-8")


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R34 must be extracted in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R34 requires develop branch")
    remote = reviewed_remote_head()
    local = git("rev-parse", "HEAD")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Local HEAD differs from reviewed R33 lineage")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged edits require review")
    changed = git("diff", "--name-only").splitlines()
    if any(filename != PRODUCTION for filename in changed):
        raise RuntimeError("Unexpected tracked edits; no reset performed")
    for directory in (
        "phase174_r3_r7_r30_prop27_public_provider_wiring",
        "phase174_r3_r7_r31_delta_surjectivity_general_audit",
        "phase174_r3_r7_r32_lower_delta_kernel_audit",
        "phase174_r3_r7_r33_three_premise_source_frontier",
    ):
        if not (ROOT / directory).is_dir():
            raise RuntimeError("Earlier phase missing: " + directory)
    base = subprocess.run(
        ("git", "show", local + ":" + PRODUCTION),
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    expected = expected_source_bytes(base)
    actual = (ROOT / PRODUCTION).read_bytes()
    if actual == base:
        mode = "BASELINE"
    elif actual.replace(b"\r\n", b"\n") == base.replace(b"\r\n", b"\n"):
        mode = "BASELINE_EOL_NORMALIZED"
    elif actual == expected:
        mode = "INSTALLED"
    elif actual.replace(b"\r\n", b"\n") == expected.replace(b"\r\n", b"\n"):
        mode = "INSTALLED_EOL_NORMALIZED"
    else:
        raise RuntimeError("Tracked production changes are not the exact R34 patch")
    reviewed_source_positions()
    checked_prior_statements()
    return {
        "local_head": local, "remote_head": remote,
        "source_guard": "PASS", "mode": mode,
        "earlier_phases_preserved": True,
    }


def install() -> dict[str, object]:
    state = preflight()
    if state["mode"].startswith("BASELINE"):
        path = ROOT / PRODUCTION
        data = path.read_bytes()
        text = data.decode("utf-8")
        if "\r\n" in text:
            installed = patch_source(text.replace("\r\n", "\n")).replace("\n", "\r\n")
        else:
            installed = patch_source(text)
        path.write_bytes(installed.encode("utf-8"))
    final = preflight()
    if final["mode"] == "BASELINE":
        raise RuntimeError("R34 installer did not apply the intended patch")
    return final


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = preflight() if args.dry_run else install()
    p = "PHASE174_R3R7R34_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    print(p + "RUN=" + ("DRYRUN_PASS" if args.dry_run else "INSTALL_PASS"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 監査プログラム（新規）: `audit.py`

```python
"""R34 cited lower-Delta prior-source screen and provider audit.

Reports proven source leaves separately from later (unproved) kernel/root
claims. No inference step is fabricated by this audit.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r34_prior_lower_delta_source_wiring.install import preflight
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
    ROOT,
    build_cited_lower_delta_sources,
)


def screen_report() -> dict[str, object]:
    from homotopy_groups import (
        FiniteCyclicGroup,
        FreeCyclicGroup,
        TodaDeltaMap,
        TodaPrimaryGroup,
        TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from proof import ProofRule, ProofStep, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    domain, codomain = TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5)
    delta = TodaDeltaMap(domain, codomain)
    isolated = build_cited_lower_delta_sources(ROOT)
    if len(isolated.proof_links) != 2:
        raise RuntimeError("R34 must register exactly two independent source leaves")
    registered = build_shared_typed_bridge()
    screen = screen_independent_sources_for_derived_goal(registered, goal=root)
    steps = tuple(
        link.step for link in screen.proof_links
        if type(link.step) is ProofStep and link.step.rule is ProofRule.GIVEN
    )
    group_steps = tuple(s for s in steps
                        if type(s.conclusion) is Relation
                        and s.conclusion.relation_type is RelationType.EQUALITY
                        and s.conclusion.lhs == codomain
                        and type(s.conclusion.rhs) is FiniteCyclicGroup
                        and s.conclusion.rhs.order == 2)
    delta_steps = tuple(s for s in steps
                        if type(s.conclusion) is TodaDeltaImageUpToSignStatement
                        and s.conclusion.map == delta)
    diagonal_steps = tuple(s for s in steps
                           if type(s.conclusion) is Relation
                           and s.conclusion.relation_type is RelationType.EQUALITY
                           and s.conclusion.lhs == domain
                           and type(s.conclusion.rhs) is FreeCyclicGroup)
    if len(group_steps) != 1 or len(delta_steps) != 1:
        raise RuntimeError("Two independently cited earlier leaves not publicly screened")
    expected_group = isolated.proof_links[0].step.conclusion
    expected_delta = isolated.proof_links[1].step.conclusion
    if group_steps[0].conclusion != expected_group or delta_steps[0].conclusion != expected_delta:
        raise RuntimeError("Source and public screened claims have different identities")
    if any(s.conclusion == root for s in steps) or any(
        type(s.conclusion) is KernelMultipleStatement and s.conclusion.map == delta
        for s in steps
    ):
        raise RuntimeError("An unproved kernel or root was registered as GIVEN")
    return {
        "screened_prior_codomain_leaves": len(group_steps),
        "screened_prior_delta_generator_leaves": len(delta_steps),
        "screened_concrete_diagonal_leaves": len(diagonal_steps),
        "signed_image_is_conservative_for_exact_equation": True,
        "prior_literature_citations": ["Proposition 5.8", "(5.10)"],
        "db_generator_is_independent_literature_source": False,
        "new_source_givens": 2,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_math_rules": 0,
        "lower_kernel_proved": False,
        "delta_surjectivity_proved": False,
        "root_complete": False,
        "full_pytest": False,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    state = preflight()
    screen = None if dry_run else screen_report()
    return {
        "phase": "174-R3-R7-R34",
        "git_state": state,
        "source": screen,
        "gate": (
            "PASS_R34_PRIOR_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R34_TWO_EARLIER_CITED_LEAVES_SCREENED_DOMAIN_AND_KERNEL_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r34"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "prior_cited_source.json")
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R34_"
    for key in ("local_head", "remote_head", "source_guard", "mode", "earlier_phases_preserved"):
        print(p + key.upper() + "=" + str(result["git_state"][key]))
    if result["source"] is not None:
        for key, value in result["source"].items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 出典テスト（新規）: `tests/test_source.py`

```python
"""R34 source, manifestation, typed generator and forbidden-goal guards."""
from __future__ import annotations

import pytest

from expression import Composition
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase174_r3_r7_r34_prior_lower_delta_source_wiring import source
from proof import ProofRule, Relation
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


def test_real_prior_toda_source_is_pinned_and_ordered():
    text = source.pinned_source_text()
    assert text.index(source.PROP58) < text.index(source.EQ510) < text.index(source.PROP59)
    assert text.count(source.CODOMAIN_CLAUSE) >= 1
    assert text.count(source.IMAGE_CLAUSE) >= 1


def test_manifest_positions_are_exact_and_in_order():
    p58, eq510 = source.reviewed_source_positions()
    assert type(p58) is int and type(eq510) is int
    assert 0 < p58 < eq510


def test_structured_db_generator_is_actual_composition():
    codomain, image = source.checked_prior_statements()
    assert type(codomain) is Relation
    assert codomain.lhs == TodaPrimaryGroup(9, 5)
    assert type(codomain.rhs) is FiniteCyclicGroup
    assert codomain.rhs.order == 2
    assert type(codomain.rhs.generator) is Composition
    assert codomain.rhs.generator.is_type_compatible()
    assert type(image) is TodaDeltaImageUpToSignStatement
    assert image.map == TodaDeltaMap(TodaPrimaryGroup(11, 11), codomain.lhs)
    assert image.positive_value == codomain.rhs.generator
    assert image.element.source == 11 and image.element.target == 11


def test_only_two_earlier_cited_givens_no_kernel_or_root():
    bridge = source.build_cited_lower_delta_sources()
    assert len(bridge.proof_links) == 2
    for link, (_, ref_id, source_id, _) in zip(bridge.proof_links, source.MANIFEST_ROWS):
        step = link.step
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        assert reference.reference_id == ref_id
        assert reference.source_id == source_id
        assert step.rule is ProofRule.GIVEN
        assert not step.premises
        assert step.inference_rule.literature_reference.locator in ("Proposition 5.8", "(5.10)")
        assert bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
    assert all("KernelMultiple" not in type(link.step.conclusion).__name__
               and "ZeroStatement" not in type(link.step.conclusion).__name__
               for link in bridge.proof_links)


def test_missing_printed_clauses_rejected(tmp_path):
    path = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    path.parent.mkdir(parents=True)
    real = source.pinned_source_text()
    path.write_text(real.replace(source.IMAGE_CLAUSE, "NOT_AN_EQUATION"), encoding="utf-8")
    with pytest.raises(ValueError):
        source.pinned_source_text(tmp_path)


def test_manifest_rejection_of_swapped_source_id(monkeypatch):
    current = source._load_manifest_reference_order
    def wrong(path):
        positions, rows, manifest = current(path)
        altered = dict(rows)
        key = "toda:(5.10)"
        altered[key] = (dict(rows[key][0], statement_id="forged:id"),)
        return positions, altered, manifest
    monkeypatch.setattr(source, "_load_manifest_reference_order", wrong)
    with pytest.raises(ValueError):
        source.reviewed_source_positions()


def test_cited_source_steps_do_not_prove_the_derived_kernel():
    bridge = source.build_cited_lower_delta_sources()
    assert all(type(link.step.conclusion).__name__ != "KernelMultipleStatement"
               for link in bridge.proof_links)
    assert all(link.step.rule is not ProofRule.INFERENCE
               for link in bridge.proof_links)
```

### 設置テスト（新規）: `tests/test_install.py`

```python
"""R34 installer is idempotent and changes one reviewed production anchor."""
from __future__ import annotations

import subprocess

import pytest

from phase174_r3_r7_r34_prior_lower_delta_source_wiring import install


def baseline_source() -> str:
    return subprocess.run(
        ("git", "show", "HEAD:" + install.PRODUCTION),
        cwd=install.ROOT, check=True, capture_output=True,
    ).stdout.decode("utf-8")


def test_patch_is_idempotent_and_contains_only_source_builder():
    base = baseline_source()
    patched = install.patch_source(base)
    assert install.patch_source(patched) == patched
    assert patched.count(install.ADDITION) == 1
    assert patched.replace(install.ANCHOR + "\n" + install.ADDITION,
                           install.ANCHOR) == base


def test_patch_rejects_removed_or_ambiguous_anchor():
    base = baseline_source()
    with pytest.raises(RuntimeError):
        install.patch_source(base.replace(install.ANCHOR, "REPLACED"))
    with pytest.raises(RuntimeError):
        install.patch_source(base + "\n" + install.ANCHOR)


def test_expected_git_blob_is_exactly_reviewed():
    baseline = subprocess.run(
        ("git", "show", "HEAD:" + install.PRODUCTION),
        cwd=install.ROOT, check=True, capture_output=True,
    ).stdout
    revised = install.expected_source_bytes(baseline)
    assert revised != baseline
    assert b"build_cited_lower_delta_sources" in revised
    assert b"register_positioned_prop27" in revised


def test_preflight_after_install_preserves_earlier_phases():
    state = install.preflight()
    assert state["source_guard"] == "PASS"
    assert state["mode"].startswith("INSTALLED")
    assert state["earlier_phases_preserved"] is True
```

### 公開接続テスト（新規）: `tests/test_public.py`

```python
"""Proof-use screening and R30 shared-provider regression for R34."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    typed_specialization,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit import screen_report
from proof import ProofRule
from toda_rules import TodaDeltaImageUpToSignStatement


def test_r34_two_prior_cited_leaves_reach_public_screen():
    result = screen_report()
    assert result["screened_prior_codomain_leaves"] == 1
    assert result["screened_prior_delta_generator_leaves"] == 1
    assert result["new_direct_kernel_givens"] == 0
    assert result["new_direct_root_givens"] == 0
    assert result["lower_kernel_proved"] is False
    assert result["root_complete"] is False


def test_shared_bridge_presents_signed_delta_as_only_cited_leaf():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    matches = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and type(link.step.conclusion) is TodaDeltaImageUpToSignStatement
        and link.step.conclusion.map.source_group == TodaPrimaryGroup(11, 11)
        and link.step.conclusion.map.target_group == TodaPrimaryGroup(9, 5)
    )
    assert len(matches) == 1
    assert matches[0].rule is ProofRule.GIVEN
    assert matches[0].inference_rule.literature_reference.locator == "(5.10)"


def test_r30_cited_prop27_shared_provider_remains_operational():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    proposals = provider(typed_specialization(6))
    assert any(proposal.subgoals == (Prop27GeneralTheoremPremise(),)
               for proposal in proposals)
```

### 静的検査テスト（新規）: `tests/test_static_helpers.py`

```python
"""Repository-independent source-static smoke tests for R34 packaging."""
from __future__ import annotations

import ast
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (BASE / path).read_text(encoding="utf-8")


def test_full_changed_function_is_present_and_parseable():
    tree = ast.parse(read("CHANGED_FUNCTION_FULL.py"))
    functions = [x for x in tree.body if isinstance(x, ast.FunctionDef)]
    assert [x.name for x in functions] == ["build_shared_typed_bridge"]
    assert "build_cited_lower_delta_sources" in ast.unparse(functions[0])


def test_only_two_prior_literature_references_are_registered():
    tree = ast.parse(read("source.py"))
    items = [x for x in tree.body if isinstance(x, ast.Assign)
             and any(isinstance(v, ast.Name) and v.id == "MANIFEST_ROWS"
                     for v in x.targets)]
    assert len(items) == 1
    assert len(items[0].value.elts) == 2


def test_checked_prior_sources_exclude_derived_statement():
    source = read("source.py")
    assert "KernelMultipleStatement(" not in source
    assert "TodaPrimaryGroupZeroStatement(" not in source
    assert "TodaDeltaImageUpToSignStatement(" in source
    assert "FiniteCyclicGroup" in source


def test_runner_is_focused_only():
    runner = read("run.ps1")
    assert "-m pytest -q" in runner
    assert "-DryRun" in runner or "$DryRun" in runner
    assert "pytest --maxfail" not in runner
    assert "FULL_PYTEST=False" in runner


def test_complete_replacement_and_installer_use_same_source_call():
    text = read("CHANGED_FUNCTION_FULL.py")
    installer = read("install.py")
    for token in (
        "from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import",
        "build_cited_lower_delta_sources(Path(__file__).resolve().parent)",
    ):
        assert token in text
        if "from phase" in token:
            assert "phase174_r3_r7_r34_prior_lower_delta_source_wiring.source" in installer
        else:
            assert token in installer
```

### PowerShell実行手順（新規）: `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.install --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R34 source preflight failed' }
& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R34 audit preflight failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R34_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.install
if ($LASTEXITCODE -ne 0) { throw 'R34 guarded installation failed' }
& python -B -m phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit
if ($LASTEXITCODE -ne 0) { throw 'R34 public source audit failed' }

$Groups = @(
    @{ Name='R34_STATIC'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_static_helpers.py') },
    @{ Name='R34_SOURCE'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_source.py') },
    @{ Name='R34_INSTALL'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_install.py') },
    @{ Name='R34_PUBLIC'; Files=@('.\phase174_r3_r7_r34_prior_lower_delta_source_wiring\tests\test_public.py') },
    @{ Name='R33_SOURCE_CONTRACT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_source_contract.py') },
    @{ Name='R32_KERNEL_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R34_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R34 focused pytest failed: ' + $Group.Name) }
}
Write-Output 'PHASE174_R3R7R34_RUN=PASS'
Write-Output 'PHASE174_R3R7R34_FULL_PYTEST=False'
Write-Output '(END)'
```
