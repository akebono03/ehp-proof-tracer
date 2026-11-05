# Phase 174 R3-R6-R2 全コード記録

## 既存ファイル変更対象

- `phase165_r52_r27_r5_literature.py` — HEAD blob `c9bfe2788f4cf043db6dada98a437afea6accf75`
- `phase169_r4b_prop44_injectivity/rule.py` — HEAD blob `aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b`
- `phase165_r52_r9_shared_math.py` — HEAD blob `bf5bc76c842a6fcac65fc88846f96a95917d0624`
- `phase168_r3_37c_reference_projection.py` — HEAD blob `fac793665068c5ae8ac51c413687123a470cfbd8`
- `phase168_r3_5_model_renderer.py` — HEAD blob `eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8`
- `phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py` — HEAD blob `9bcec30bb228126e1e7670a221d447a524219d0c`
- `phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py` — HEAD blob `bd3244471191a6dda4d1deba7c7cf419e896623b`
- `phase174_r3_r5_preflight/audit.py` — HEAD blob `0e00b6514ffd1b7eed79708b48081af8482dac0f`
- `phase174_r3_r4_public_delta_connection/tests/test_connection.py` — HEAD blob `59e0905444f73a656b24a4528edaeeddad2ebda6`

## 既存クラスの変更後全文

```python
@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """Toda Proposition 4.4: a conditional isomorphism, not existence of alpha.

    The hypothesis H(alpha)=+/-iota is proved independently before use.
    The preceding Hopf-fibration paragraph is NOT part of the proposition.
    """
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True
```

## 既存規則関数の変更後全文

```python
def prop44_hopf_four_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """Apply conditional Proposition 4.4 to a proved Lemma 5.4 Hopf witness."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )
    from proof import Relation, RelationType

    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 suspension injectivity")
    hopf = canonical_hopf_relation()
    proposition = TodaProp44UniversalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == proposition
            and premises[1].rule is ProofRule.INFERENCE
            and premises[1].conclusion == hopf
            and len(premises[1].premises) == 1
            and premises[1].premises[0].rule is ProofRule.GIVEN
            and type(premises[1].premises[0].conclusion) is TodaLemma54TypedSource
            and premises[1].premises[0].conclusion == TodaLemma54TypedSource()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 using separately proved Hopf invariant",
        description=(
            "Proposition 4.4 is conditional; independently prove H(nu_4)=iota_7 "
            "from the earlier, screened Lemma 5.4 before specializing it."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=proposition,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose the conditional theorem only when Lemma 5.4 is source-screened."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(proposition) != 1 or available.count(lemma) != 1:
        return ()
    return (GoalExpansion(
        prop44_hopf_four_injectivity_rule(goal),
        (proposition, canonical_hopf_relation()),
    ),)
```

## 既存監査関数の変更後全文

```python
def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Compare against the pinned current HEAD or the exact reviewed new provider."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    import subprocess
    from phase174_r3_r6_r2_prop44_lemma54.patch import git_blob, normalize, patch_shared

    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_FILE),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if git_blob(original) != "bf5bc76c842a6fcac65fc88846f96a95917d0624":
        raise ValueError("Unexpected committed R3-R6 source")
    original_text = normalize(original.decode("utf-8-sig"))
    expected = patch_shared(original_text)
    normalized_current = normalize(source.decode("utf-8-sig"))
    if normalized_current not in (original_text, expected):
        raise ValueError("Unreviewed production source modifications")
    state = "COMMITTED" if normalized_current == original_text else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
```

## 残る既存変更関数の取得方法

既存の大型関数については、9ファイル全体を厳密に照合した後、実行時に各 **変更後ファイル全文** と **変更後関数全文** を `phase174_r3_r6_r2_prop44_lemma54/output/` に出力する。関数内 import を含めて省略はない。変更前原文は Git の同一 HEAD に残る。

## 新規クラス・関数を置く位置

`phase174_r3_r6_r2_prop44_lemma54/source.py` に新設する。既存のクラスを複製したり、将来 Phase の群の特殊化を追加したりしない。

## source.py — 全文

```python
"""Typed, independently cited pre-Proposition-4.4 splitting and Lemma-5.4 access.

The source paragraph asserts E+h_* is an isomorphism; it does NOT assert
H(h)=+/-iota. Lemma 5.4 is preferred whenever its cited source precedes
an actual proof target. No particular group result is imported as GIVEN.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import verify_prop44_hopf_fibration_source
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase169_r4b_prop44_injectivity.rule import _is_hopf_four_suspension
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    SOURCE_ID,
    TodaLemma54TypedSource,
    add_verified_lemma54_source,
)
from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep
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
PRELUDE_REFERENCE_ID = "phase174:r3r6r2:preprop44:reference"
PRELUDE_ASSERTION_ID = "phase174:r3r6r2:preprop44:assertion"
PRELUDE_LOCATOR = "Chapter IV, immediately before Proposition 4.4"


@dataclass(frozen=True)
class TodaPreProp44SplittingStatement:
    """The *printed* E+h_* splitting for n=2,4,8; not a claim about H(h)."""

    dimensions: tuple[int, ...] = (2, 4, 8)
    assertion: str = "E+h_* is an isomorphism for every i"


def verify_prelude_source(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> int:
    """Pin the transcribed prelude and place it strictly before Proposition 4.4."""
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be paths")
    verify_prop44_hopf_fibration_source(root / "sources/toda/Toda_04_2.tex")
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8-sig")
    start = "$n=2,4,8$ のとき, Hopf fibration"
    stop = r"\begin{proposition}\label{prop:4.4}"
    if text.count(start) != 1 or text.count(stop) != 1:
        raise ValueError("Pre-Proposition 4.4 source boundaries changed")
    passage = text.split(start, 1)[1].split(stop, 1)[0]
    if any(part not in passage for part in (
        r"S^n\hookrightarrow S^{2n-1}\xrightarrow{h} S^n",
        r"E+h_*:",
        r"\xrightarrow{\ \cong\ }",
        r"\cite{Steenrod1951}",
    )):
        raise ValueError("The cited pre-Proposition 4.4 splitting was changed")
    positions, _, _ = _load_manifest_reference_order(manifest)
    before = positions.get("toda:(4.7)")
    after = positions.get("toda:Proposition 4.4")
    if (before, after) != (7200, 7300):
        raise ValueError("Reviewed source order around Proposition 4.4 changed")
    return (before + after) // 2


def build_cited_preprop44_splitting() -> RegistryBridgeResult:
    """A separate sourced remark (one GIVEN); no Proposition 4.4 hypothesis."""
    position = verify_prelude_source()
    source = TodaPreProp44SplittingStatement()
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=PRELUDE_REFERENCE_ID,
        kind=ReferenceKind.REMARK,
        locator=PRELUDE_LOCATOR,
        source_id="sources/toda/Toda_04_2.tex (adopted transcription, original edition unverified)",
        publication_position=position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=PRELUDE_ASSERTION_ID,
        reference_id=PRELUDE_REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=source,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("source paragraph E+h_* splitting", "n=2,4,8"),
    ))
    link = ProofStepLink(
        PRELUDE_ASSERTION_ID,
        step=ProofStep(source, (), ProofRule.GIVEN, inference_rule=InferenceRule(
            name="Cited pre-Proposition 4.4 E+h_* splitting",
            literature_reference=LiteratureReference(
                label="Toda Chapter IV prelude", locator=PRELUDE_LOCATOR,
            ),
        )),
    )
    return RegistryBridgeResult(registry, (), (link,))


def prelude_splitting_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """E is a split injection when (E,h_*) is a cited isomorphism."""
    if not _is_hopf_four_suspension(goal):
        raise ValueError("Only the reviewed n=4 suspension is supported")
    source = TodaPreProp44SplittingStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == source
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="cited Hopf-fibration splitting implies suspension injectivity",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaPreProp44SplittingStatement,
            statement_pattern=source,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Chapter IV prelude", locator=PRELUDE_LOCATOR,
        ),
    )


def expand_cited_preprop44_splitting(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use the earlier independent splitting only when Lemma 5.4 is unavailable."""
    if not isinstance(available, tuple):
        raise TypeError("available must be screened citation statements")
    if not _is_hopf_four_suspension(goal):
        return ()
    if any(isinstance(item, TodaLemma54TypedSource) for item in available):
        return ()
    source = TodaPreProp44SplittingStatement()
    if available.count(source) != 1:
        return ()
    return (GoalExpansion(prelude_splitting_injectivity_rule(goal), (source,)),)


def attach_earlier_verified_lemma54(
    bridge: RegistryBridgeResult, citing_assertion_id: str,
) -> RegistryBridgeResult:
    """Adopt Lemma 5.4 only if its existing archive actually precedes the target.

    This is a common citation-screening operation, independent of n, k,
    target generator spelling or the eventual proof outcome.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be a typed registry bridge")
    if ADOPTED_ASSERTION_ID in bridge.registry._assertions:
        return bridge
    citing = bridge.registry.assertion(citing_assertion_id)
    citing_reference = bridge.registry.reference(citing.reference_id)
    archives = tuple(
        item for item in bridge.registry._assertions.values()
        if item.origin is AssertionOrigin.SOURCE_ARCHIVE
        and isinstance(item.content, dict)
        and item.content.get("source_statement_id") == SOURCE_ID
    )
    if len(archives) != 1:
        return bridge
    archive_reference = bridge.registry.reference(archives[0].reference_id)
    source_position = archive_reference.publication_position
    target_position = citing_reference.publication_position
    if (type(source_position) is not int or type(target_position) is not int
            or source_position >= target_position):
        return bridge
    chapter = (ROOT / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    return add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_assertion_id, chapter=chapter,
    )
```

## audit.py — 全文

```python
"""End-to-end proof-ancestry audit of the corrected conditional Proposition 4.4."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    verify_prelude_source,
)
from proof import ProofRule


def cited_leaves(step) -> tuple[object, ...]:
    if step.rule is ProofRule.GIVEN:
        return (step.conclusion,)
    out: list[object] = []
    for premise in step.premises:
        out.extend(cited_leaves(premise))
    return tuple(out)


def inspect() -> dict[str, object]:
    position = verify_prelude_source()
    original = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(original, n=5, k=3)
    if len(roots) != 1:
        raise ValueError("Expected the registered pi_8^5 target")
    target = roots[0]
    citing = resolve_specialized_goal_citing_id(original, target)
    if citing is None:
        raise ValueError("Missing real publication position of target")
    augmented = attach_earlier_verified_lemma54(original, citing)
    if augmented is original:
        raise ValueError("Lemma 5.4 not attached although it precedes Proposition 5.6")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaProp44UniversalStatement()) == 1
    assert available.count(TodaLemma54TypedSource()) == 1
    assert available.count(TodaPreProp44SplittingStatement()) == 1
    provider = shared_expansion_provider(screened, proof_target=target)
    map_goal = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
    ))
    map_step = reconstruct_registered_goal(
        map_goal, screened, citing, provider, lookup_mode="typed_reference",
    )
    if (map_step.rule is not ProofRule.INFERENCE
            or map_step.conclusion != map_goal
            or getattr(map_step.inference_rule, "name", None)
            != "Toda Proposition 4.4 using separately proved Hopf invariant"
            or len(map_step.premises) != 2
            or map_step.premises[1].conclusion != canonical_hopf_relation()
            or map_step.premises[1].rule is not ProofRule.INFERENCE):
        raise ValueError("Proposition 4.4 was used without independently proved Hopf condition")
    ancestry = cited_leaves(map_step)
    if (ancestry.count(TodaProp44UniversalStatement()) != 1
            or ancestry.count(TodaLemma54TypedSource()) != 1
            or TodaPreProp44SplittingStatement() in ancestry):
        raise ValueError("Wrong cited ancestry for conditional Proposition 4.4")
    result = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    if result.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("pi_8^5 completed root regressed: " + result.status.value)
    roots_proved = tuple(step for step in result.proven_steps if step.conclusion == target)
    if len(roots_proved) != 1 or roots_proved[0].rule is not ProofRule.INFERENCE:
        raise ValueError("Completed group root lacks its own inference")
    root_ancestors = cited_leaves(roots_proved[0])
    if (TodaLemma54TypedSource() not in root_ancestors
            or TodaProp44UniversalStatement() not in root_ancestors
            or TodaPreProp44SplittingStatement() in root_ancestors):
        raise ValueError("Public group root did not choose the Lemma 5.4 route")
    model = build_linked_proof_narrative_model(result, screened)
    narrative = render_model_backed_narrative_markdown(result, model)
    if "Lemma 5.4" not in narrative or "Proposition 4.4" not in narrative:
        raise ValueError("Proposition 4.4 or Lemma 5.4 citation not visible")
    if r"$h:S^7\to S^4$" in narrative:
        raise ValueError("Unproved H(h) presentation remains in the narrative")
    # Earlier targets must not cite the later Lemma 5.4.
    previous = search_group_from_registered_goal(n=4, k=2, bridge=original)
    if previous.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("Prior pi_6^4 complete proof regressed")
    return {
        "phase": "174-R3-R6-R2",
        "root": "pi_8^5",
        "root_status": result.status.value,
        "root_proven_steps": len(result.proven_steps),
        "root_verified": True,
        "source_given_lemma54": True,
        "proposition44_conditional": True,
        "hopf_invariant_condition_inferred": True,
        "lemma54_is_root_ancestor": True,
        "preprop44_is_root_ancestor": False,
        "previous_pi6_4_still_complete": True,
        "prelude_source_position": position,
        "new_group_given": 0,
        "narrative_reference_verified": True,
        "narrative": narrative,
        "full_pytest_performed": False,
    }


def main() -> int:
    result = inspect()
    output = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    output = output / "EHPProofTracerAudit" / "phase174_r3_r6_r2"
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (output / "web_narrative.md").write_text(result["narrative"], encoding="utf-8")
    print("PHASE174_R3R6R2_PI85_COMPLETE=True")
    print("PHASE174_R3R6R2_HOPF_CONDITION_INFERRED=True")
    print("PHASE174_R3R6R2_LEMMA54_ROOT_ANCESTRY=True")
    print("PHASE174_R3R6R2_PRELUDE_NOT_IN_ROOT=True")
    print("PHASE174_R3R6R2_PI64_PRESERVED=True")
    print("PHASE174_R3R6R2_ROOT_STEPS=" + str(result["root_proven_steps"]))
    print("PHASE174_R3R6R2_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6R2_AUDIT=" + str(output / "audit.json"))
    print("PHASE174_R3R6R2_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## verify.py — 全文

```python
"""Read-only source check before any production code changes."""
from __future__ import annotations

from phase165_r52_r27_r5_literature import verify_prop44_hopf_fibration_source
from phase174_r3_r6_r2_prop44_lemma54.source import verify_prelude_source
from phase173_r4_r1_lemma54_source_bridge.source import validate_lemma54_text
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    verify_prop44_hopf_fibration_source()
    rank = verify_prelude_source()
    chapter = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    validate_lemma54_text(chapter)
    print("PHASE174_R3R6R2_PRELUDE_POSITION=" + str(rank))
    print("PHASE174_R3R6R2_LEMMA54_SOURCE=PASS")
    print("PHASE174_R3R6R2_SOURCE_TEXT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## patch.py — 全文

```python
"""Exact, fail-closed patch against the reviewed Phase 174 R3-R6 develop baseline."""
from __future__ import annotations

import ast
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
HEAD = "e4a5b73962bb98acb62b5335ffecae4728d98378"
BLOBS = {
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase169_r4b_prop44_injectivity/rule.py": "aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b",
    "phase165_r52_r9_shared_math.py": "bf5bc76c842a6fcac65fc88846f96a95917d0624",
    "phase168_r3_37c_reference_projection.py": "fac793665068c5ae8ac51c413687123a470cfbd8",
    "phase168_r3_5_model_renderer.py": "eb34d6fd4783ca943e07de6e6d9756d0e85ff9b8",
    "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": "9bcec30bb228126e1e7670a221d447a524219d0c",
    "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": "bd3244471191a6dda4d1deba7c7cf419e896623b",
    "phase174_r3_r5_preflight/audit.py": "0e00b6514ffd1b7eed79708b48081af8482dac0f",
    "phase174_r3_r4_public_delta_connection/tests/test_connection.py": "59e0905444f73a656b24a4528edaeeddad2ebda6",
}


def run_git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True, encoding="utf-8").stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n")


def replace_one(text: str, before: str, after: str, *, label: str) -> str:
    if text.count(before) != 1:
        raise ValueError(f"Unreviewed source context: {label}: {text.count(before)}")
    return text.replace(before, after, 1)


def full_unit(text: str, name: str) -> str:
    tree = ast.parse(text)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
               and node.name == name]
    if len(matches) != 1:
        raise ValueError("Expected one complete unit: " + name)
    node = matches[0]
    start = min([node.lineno] + [d.lineno for d in node.decorator_list]) - 1
    return "\n".join(text.split("\n")[start:node.end_lineno]) + "\n"


PROP44_CLASS = '''@dataclass(frozen=True)
class TodaProp44UniversalStatement:
    """Toda Proposition 4.4: a conditional isomorphism, not existence of alpha.

    The hypothesis H(alpha)=+/-iota is proved independently before use.
    The preceding Hopf-fibration paragraph is NOT part of the proposition.
    """
    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"
    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"
    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"
    target_group: str = "pi_i^n"
    quantifiers: tuple[str, ...] = ("n", "i", "alpha")
    includes_suspension_injectivity: bool = True
'''

RULES = '''def prop44_hopf_four_injectivity_rule(goal: MapInjective) -> InferenceRule:
    """Apply conditional Proposition 4.4 to a proved Lemma 5.4 Hopf witness."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )
    from proof import Relation, RelationType

    if not _is_hopf_four_suspension(goal):
        raise ValueError("goal must be an n=4 suspension injectivity")
    hopf = canonical_hopf_relation()
    proposition = TodaProp44UniversalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == proposition
            and premises[1].rule is ProofRule.INFERENCE
            and premises[1].conclusion == hopf
            and len(premises[1].premises) == 1
            and premises[1].premises[0].rule is ProofRule.GIVEN
            and type(premises[1].premises[0].conclusion) is TodaLemma54TypedSource
            and premises[1].premises[0].conclusion == TodaLemma54TypedSource()
            and _is_hopf_four_suspension(goal)
        )

    return InferenceRule(
        name="Toda Proposition 4.4 using separately proved Hopf invariant",
        description=(
            "Proposition 4.4 is conditional; independently prove H(nu_4)=iota_7 "
            "from the earlier, screened Lemma 5.4 before specializing it."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaProp44UniversalStatement,
                statement_pattern=proposition,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=hopf,
            ),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
        literature_reference=LiteratureReference(
            label="Toda Proposition 4.4", locator="Proposition 4.4",
        ),
    )


def expand_cited_prop44_injectivity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose the conditional theorem only when Lemma 5.4 is source-screened."""
    from phase173_r4_r1_lemma54_source_bridge.source import (
        TodaLemma54TypedSource,
        canonical_hopf_relation,
    )

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not _is_hopf_four_suspension(goal):
        return ()
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    if available.count(proposition) != 1 or available.count(lemma) != 1:
        return ()
    return (GoalExpansion(
        prop44_hopf_four_injectivity_rule(goal),
        (proposition, canonical_hopf_relation()),
    ),)
'''


def patch_literature(text: str) -> str:
    text = replace_one(text, full_unit(text, "TodaProp44UniversalStatement"),
                       PROP44_CLASS.rstrip() + "\n", label="conditional proposition class")
    return replace_one(
        text,
        '    verify_prop44_hopf_fibration_source()\n    registry = UnifiedStatementRegistry()\n',
        '    registry = UnifiedStatementRegistry()\n',
        label="decouple conditional proposition source from prelude",
    )


def patch_injectivity(text: str) -> str:
    start = text.index("def prop44_hopf_four_injectivity_rule(")
    end = len(text)
    # These two functions are the final units in the reviewed R4-B module.
    if text.count("def prop44_hopf_four_injectivity_rule(") != 1 or text.count("def expand_cited_prop44_injectivity(") != 1:
        raise ValueError("Unreviewed R4-B rule structure")
    return text[:start] + RULES


def patch_shared(text: str) -> str:
    before = '        sources = sources + (build_cited_extension_sources(),)\n'
    after = (before +
        '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
        '            build_cited_preprop44_splitting,\n'
        '        )\n'
        '        sources = sources + (build_cited_preprop44_splitting(),)\n')
    text = replace_one(text, before, after, label="independent prelude source")
    before = ('        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n'
              '        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))\n')
    after = (
        '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
        '            expand_cited_preprop44_splitting,\n'
        '        )\n'
        '        options.extend(expand_cited_preprop44_splitting(goal, tuple(available)))\n'
        '        from phase173_r4_r1_lemma54_source_bridge.source import (\n'
        '            expand_cited_lemma54_hopf,\n'
        '        )\n'
        '        options.extend(expand_cited_lemma54_hopf(goal, tuple(available)))\n'
        '        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity\n'
        '        conditional_prop44 = expand_cited_prop44_injectivity(goal, tuple(available))\n'
        '        if conditional_prop44:\n'
        '            return conditional_prop44\n'
    )
    text = replace_one(text, before, after, label="general typed proof providers")
    before = ('        if pi74_connection is not None:\n'
              '            bridge, citing_assertion_id, expansion_provider = pi74_connection\n'
              '    assertions = tuple(bridge.registry._assertions.values())\n')
    after = ('        if pi74_connection is not None:\n'
             '            bridge, citing_assertion_id, expansion_provider = pi74_connection\n'
             '    if citing_assertion_id is not None and expansion_provider is None:\n'
             '        from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
             '            attach_earlier_verified_lemma54,\n'
             '        )\n'
             '        bridge = attach_earlier_verified_lemma54(bridge, citing_assertion_id)\n'
             '    assertions = tuple(bridge.registry._assertions.values())\n')
    return replace_one(text, before, after, label="source-first citation admission")


def patch_projection(text: str) -> str:
    old = ('    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement\n')
    new = (old +
           '    from phase174_r3_r6_r2_prop44_lemma54.source import (\n'
           '        TodaPreProp44SplittingStatement,\n'
           '    )\n')
    text = replace_one(text, old, new, label="reference-projector import")
    old = ('            elif (type(statement) is TodaProp44UniversalStatement\n'
           '                  and statement == TodaProp44UniversalStatement()\n'
           '                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):\n')
    new = ('            elif (type(statement) is TodaProp44UniversalStatement\n'
           '                  and statement == TodaProp44UniversalStatement()):\n')
    text = replace_one(text, old, new, label="conditional proposition projection")
    anchor = '            elif isinstance(statement, TodaProp42GeneralExactnessStatement):\n'
    inserted = (
        '            elif (type(statement) is TodaPreProp44SplittingStatement\n'
        '                  and statement == TodaPreProp44SplittingStatement()):\n'
        '                sentence = (\n'
        '                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\\to S^n$ "\n'
        '                    r"が存在し, 任意の $i$ で "\n'
        '                    r"$E+h_*:\\pi_{i-1}^{n-1}\\oplus\\pi_i^{2n-1}"\n'
        '                    r"\\xrightarrow{\\cong}\\pi_i^n$ が成り立つ "\n'
        '                    r"(Steenrod 1951 を引用)."\n'
        '                )\n'
    )
    return replace_one(text, anchor, inserted + anchor, label="independent prelude reference")


def patch_renderer(text: str) -> str:
    start = text.find('                    # R4F: the source paragraph immediately BEFORE Prop. 4.4\n')
    end_anchor = '                        lines.extend((application, ""))\n'
    end = text.find(end_anchor, start)
    if start < 0 or end < start or text.count(end_anchor) != 1:
        raise ValueError("Unreviewed handwritten Hopf fibration narrative")
    return text[:start] + text[end + len(end_anchor):]


PREFLIGHT_FUNCTION = '''def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Compare against the pinned current HEAD or the exact reviewed new provider."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    import subprocess
    from phase174_r3_r6_r2_prop44_lemma54.patch import git_blob, normalize, patch_shared

    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_FILE),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if git_blob(original) != "bf5bc76c842a6fcac65fc88846f96a95917d0624":
        raise ValueError("Unexpected committed R3-R6 source")
    original_text = normalize(original.decode("utf-8-sig"))
    expected = patch_shared(original_text)
    normalized_current = normalize(source.decode("utf-8-sig"))
    if normalized_current not in (original_text, expected):
        raise ValueError("Unreviewed production source modifications")
    state = "COMMITTED" if normalized_current == original_text else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
'''


def patch_preflight(text: str) -> str:
    return replace_one(
        text, full_unit(text, "inspect_source_provider"),
        PREFLIGHT_FUNCTION.rstrip() + "\n", label="strict preflight source guard",
    )


def patch_r3r4_test(text: str) -> str:
    before = ("    from phase174_r3_r6_source_extension.patch import connect_shared\n"
              "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n")
    after = ("    from phase174_r3_r6_source_extension.patch import connect_shared\n"
             "    from phase174_r3_r6_r2_prop44_lemma54.patch import patch_shared\n"
             "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n")
    text = replace_one(text, before, after, label="R3-R4 cumulative test import")
    before = "    assert current in (r3r4, r3r5, connect_shared(r3r5))\n"
    after = ("    r3r6 = connect_shared(r3r5)\n"
             "    new_source = patch_shared(r3r6.decode('utf-8')).encode('utf-8')\n"
             "    assert current in (r3r4, r3r5, r3r6, new_source)\n")
    return replace_one(text, before, after, label="R3-R4 cumulative test guard")


def patch_r4b_tests(text: str) -> str:
    if text.count("def test_r4b_source_bound_dim4_has_one_proposal") != 1:
        raise ValueError("R4-B tests changed")
    return (PACKAGE / "overrides/test_r4b_prop44_injectivity.py").read_text(encoding="utf-8")


def patch_r4g_tests(text: str) -> str:
    if text.count("def test_r4g_typed_prop44_cannot_accept_fake_fibration_metadata") != 1:
        raise ValueError("R4-G tests changed")
    return (PACKAGE / "overrides/test_r4g_hopf_reference.py").read_text(encoding="utf-8")


TRANSFORM = {
    "phase165_r52_r27_r5_literature.py": patch_literature,
    "phase169_r4b_prop44_injectivity/rule.py": patch_injectivity,
    "phase165_r52_r9_shared_math.py": patch_shared,
    "phase168_r3_37c_reference_projection.py": patch_projection,
    "phase168_r3_5_model_renderer.py": patch_renderer,
    "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": patch_r4b_tests,
    "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": patch_r4g_tests,
    "phase174_r3_r5_preflight/audit.py": patch_preflight,
    "phase174_r3_r4_public_delta_connection/tests/test_connection.py": patch_r3r4_test,
}


def verified_changes() -> dict[str, tuple[bytes, bytes]]:
    if run_git("branch", "--show-current") != "develop":
        raise ValueError("Expected develop branch")
    if run_git("rev-parse", "HEAD") != HEAD:
        raise ValueError("Unreviewed local HEAD")
    remote = run_git("ls-remote", "origin", "refs/heads/develop").split()[0]
    if remote != HEAD:
        raise ValueError("Unreviewed remote HEAD")
    if run_git("diff", "--cached", "--name-only"):
        raise ValueError("Staged changes require review")
    result: dict[str, tuple[bytes, bytes]] = {}
    for path, sha in BLOBS.items():
        original = subprocess.run(("git", "show", "HEAD:" + path), cwd=ROOT,
                                  capture_output=True, check=True).stdout
        if git_blob(original) != sha:
            raise ValueError("Reviewed Git blob changed: " + path)
        text = normalize(original.decode("utf-8-sig"))
        updated = TRANSFORM[path](text)
        ast.parse(updated, filename=path)
        modified = updated.encode("utf-8")
        current = (ROOT / path).read_bytes()
        # Only the literal reviewed original or this exact patch is accepted.
        if normalize(current.decode("utf-8-sig")) not in (text, updated):
            raise ValueError("Unreviewed working source: " + path)
        result[path] = (original, modified)
    return result


def execute(dry_run: bool) -> None:
    edits = verified_changes()
    print("PHASE174_R3R6R2_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R2_REVIEWED_HEAD=" + HEAD)
    print("PHASE174_R3R6R2_TARGET_FILES=" + str(len(edits)))
    if dry_run:
        print("PHASE174_R3R6R2_DRY_RUN_GATE=PASS")
        return
    snapshots = {path: (ROOT / path).read_bytes() for path in edits}
    try:
        for path, (before, after) in edits.items():
            (ROOT / path).write_bytes(after)
        output = PACKAGE / "output"
        output.mkdir(exist_ok=True)
        for path in edits:
            content = (ROOT / path).read_text(encoding="utf-8")
            (output / (path.replace("/", "__") + ".FULL.py")).write_text(
                content, encoding="utf-8",
            )
            for name in {
                "phase165_r52_r27_r5_literature.py": ("TodaProp44UniversalStatement", "build_typed_literature_bridge"),
                "phase169_r4b_prop44_injectivity/rule.py": (
                    "prop44_hopf_four_injectivity_rule", "expand_cited_prop44_injectivity"),
                "phase165_r52_r9_shared_math.py": (
                    "build_shared_typed_bridge", "shared_expansion_provider", "search_shared_group_goal"),
                "phase168_r3_37c_reference_projection.py": ("project_reference_bodies",),
                "phase168_r3_5_model_renderer.py": ("render_model_backed_narrative_markdown",),
                "phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py": (),
                "phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py": (),
                "phase174_r3_r5_preflight/audit.py": ("inspect_source_provider",),
                "phase174_r3_r4_public_delta_connection/tests/test_connection.py":
                    ("test_r3r4_real_production_file_has_only_reviewed_wiring",),
            }[path]:
                (output / (name + "_FULL.py")).write_text(full_unit(content, name), encoding="utf-8")
        print("PHASE174_R3R6R2_PATCH=PASS")
        print("PHASE174_R3R6R2_FULL_REPLACEMENTS=" + str(output))
    except BaseException:
        for path, content in snapshots.items():
            (ROOT / path).write_bytes(content)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    execute(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_patch.py — 全文

```python
"""Off-repository guarded-patch tests; no production paths are mutated."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_r2_prop44_lemma54.patch import (
    PROP44_CLASS,
    RULES,
    patch_injectivity,
    patch_literature,
    patch_projection,
    patch_renderer,
    patch_shared,
    replace_one,
)


def test_prop44_has_no_implicit_hopf_fibration_dimensions() -> None:
    ast.parse("from dataclasses import dataclass\n" + PROP44_CLASS)
    assert "preceding_hopf_fibration_dimensions" not in PROP44_CLASS
    assert "source_condition" in PROP44_CLASS
    assert "Lemma 5.4" in RULES
    assert "premises[1].premises[0].rule is ProofRule.GIVEN" in RULES


def test_exact_replacement_is_single_and_fail_closed() -> None:
    assert replace_one("a x b", "x", "Y", label="fixture") == "a Y b"
    with pytest.raises(ValueError):
        replace_one("x x", "x", "Y", label="duplicate")
    with pytest.raises(ValueError):
        replace_one("missing", "x", "Y", label="absent")


def test_old_provider_and_new_lemma_route_are_replaced_together() -> None:
    source = "\n".join((
        "def build_shared_typed_bridge():",
        "    if True:",
        "        sources = sources + (build_cited_extension_sources(),)",
        "def shared_expansion_provider():",
        "    def expand(goal):",
        "        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity",
        "        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))",
        "def search_shared_group_goal():",
        "    if True:",
        "        if pi74_connection is not None:",
        "            bridge, citing_assertion_id, expansion_provider = pi74_connection",
        "    assertions = tuple(bridge.registry._assertions.values())",
        "",
    ))
    updated = patch_shared(source)
    ast.parse(updated)
    assert updated.count("build_cited_preprop44_splitting()") == 1
    assert updated.count("attach_earlier_verified_lemma54") == 2
    assert updated.count("expand_cited_lemma54_hopf(goal, tuple(available))") == 1
    assert updated.count("conditional_prop44 = expand_cited_prop44_injectivity") == 1
    with pytest.raises(ValueError):
        patch_shared(updated)


def test_conditional_rule_full_units_are_parseable() -> None:
    original = """from __future__ import annotations

def _is_hopf_four_suspension(goal):
    return True

def prop44_hopf_four_injectivity_rule(goal):
    return None

def expand_cited_prop44_injectivity(goal, available):
    return ()
"""
    revised = patch_injectivity(original)
    ast.parse(revised)
    assert revised.count("def prop44_hopf_four_injectivity_rule") == 1
    assert revised.count("def expand_cited_prop44_injectivity") == 1
    assert revised.count("premises[1].premises[0].rule is ProofRule.GIVEN") == 1


def test_reference_projection_does_not_mix_proposition_with_prelude() -> None:
    source = "\n".join((
        "def project_reference_bodies():",
        "    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement",
        "    if True:",
        "            elif (type(statement) is TodaProp44UniversalStatement",
        "                  and statement == TodaProp44UniversalStatement()",
        "                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):",
        "                sentence = 'condition'",
        "            elif isinstance(statement, TodaProp42GeneralExactnessStatement):",
        "                sentence = 'exact'",
        "",
    ))
    updated = patch_projection(source)
    assert "statement.preceding_hopf_fibration_dimensions" not in updated
    assert "TodoPreProp44" not in updated
    assert "TodaPreProp44SplittingStatement" in updated
    # This string fixture is not a complete if/elif chain; check unit separately.
    assert updated.count("Chapter IV") == 0


def test_renderer_removes_only_manufactured_hopf_invariant_of_h() -> None:
    source = "\n".join((
        "def render_model_backed_narrative_markdown():",
        "    if True:",
        "                    # R4F: the source paragraph immediately BEFORE Prop. 4.4",
        "                    application = 'unverified Hopf invariant'",
        '                        lines.extend((application, ""))',
        "    return lines",
        "",
    ))
    updated = patch_renderer(source)
    assert "unverified Hopf invariant" not in updated
    assert "return lines" in updated
```

## tests/test_source.py — 全文

```python
"""Source-checking and typed conditional-Proposition-4.4 proof tests."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_37c_reference_projection import project_reference_bodies
from phase169_r4b_prop44_injectivity.rule import (
    expand_cited_prop44_injectivity,
    prop44_hopf_four_injectivity_rule,
)
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_ASSERTION_ID,
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    build_cited_preprop44_splitting,
    expand_cited_preprop44_splitting,
    verify_prelude_source,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def _injection() -> MapInjective:
    return MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
    ))


def test_preprop44_is_an_independent_sourced_remark() -> None:
    assert verify_prelude_source() == 7250
    bridge = build_cited_preprop44_splitting()
    assert tuple(bridge.registry._assertions) == (PRELUDE_ASSERTION_ID,)
    assert len(bridge.proof_links) == 1
    claim = bridge.proof_links[0].step
    assert claim is not None
    assert claim.rule is ProofRule.GIVEN
    assert claim.conclusion == TodaPreProp44SplittingStatement()
    refs = project_reference_bodies(bridge.registry, (PRELUDE_ASSERTION_ID,))
    assert len(refs) == 1
    assert "E+h_*" in refs[0]
    assert "H(h)" not in refs[0]


def test_wrong_source_paragraph_is_refused(tmp_path: Path) -> None:
    original = Path(__file__).resolve().parents[2]
    manuscript = original / "sources/toda/Toda_04_2.tex"
    updated = tmp_path / "sources/toda/Toda_04_2.tex"
    updated.parent.mkdir(parents=True, exist_ok=True)
    updated.write_bytes(manuscript.read_bytes().replace(
        b"Hopf fibration", b"unverified fibration", 1,
    ))
    with pytest.raises(ValueError, match="unverified Toda Chapter IV"):
        verify_prelude_source(root=tmp_path)


def test_conditioned_prop44_refuses_missing_lemma() -> None:
    prop44 = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert not hasattr(prop44, "preceding_hopf_fibration_dimensions")
    assert expand_cited_prop44_injectivity(_injection(), (prop44,)) == ()
    proposals = expand_cited_prop44_injectivity(_injection(), (prop44, lemma))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (prop44, canonical_hopf_relation())
    assert expand_cited_prop44_injectivity(_injection(), (prop44, lemma, lemma)) == ()
    bad = replace(prop44, includes_suspension_injectivity=False)
    assert expand_cited_prop44_injectivity(_injection(), (bad, lemma)) == ()


def test_prop44_guard_requires_actual_lemma54_given_ancestor() -> None:
    rule = prop44_hopf_four_injectivity_rule(_injection())
    given_prop = ProofStep(TodaProp44UniversalStatement(), (), ProofRule.GIVEN)
    given_lemma = ProofStep(TodaLemma54TypedSource(), (), ProofRule.GIVEN)
    inferred_hopf = ProofStep(canonical_hopf_relation(), (given_lemma,), ProofRule.INFERENCE)
    good = find_inference_matches_for_rule(rule, (given_prop, inferred_hopf))
    assert len(good) == 1
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (), ProofRule.GIVEN),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        given_prop, ProofStep(canonical_hopf_relation(), (
            ProofStep(TodaPreProp44SplittingStatement(), (), ProofRule.GIVEN),
        ), ProofRule.INFERENCE),
    )) == ()


def test_preprop44_rule_is_sourced_only_when_later_lemma_unavailable() -> None:
    older = TodaPreProp44SplittingStatement()
    assert len(expand_cited_preprop44_splitting(_injection(), (older,))) == 1
    assert expand_cited_preprop44_splitting(_injection(), ()) == ()
    assert expand_cited_preprop44_splitting(_injection(), (
        older, TodaLemma54TypedSource(),
    )) == ()


def test_live_public_pi85_injection_requires_lemma54() -> None:
    bridge = build_shared_typed_bridge()
    target, = registered_group_goal_candidates(bridge, n=5, k=3)
    citing = resolve_specialized_goal_citing_id(bridge, target)
    assert citing is not None
    new_bridge = attach_earlier_verified_lemma54(bridge, citing)
    screened = screen_shared_proof_context(
        new_bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    assert len(expand_cited_prop44_injectivity(_injection(), (
        TodaProp44UniversalStatement(), TodaLemma54TypedSource(),
    ))) == 1
    actual = reconstruct_registered_goal(
        _injection(), screened, citing, provider, lookup_mode="typed_reference",
    )
    assert actual.rule is ProofRule.INFERENCE
    assert len(actual.premises) == 2
    assert actual.premises[1].conclusion == canonical_hopf_relation()
    assert actual.premises[1].premises[0].conclusion == TodaLemma54TypedSource()


def test_historical_hopf_paragraph_is_not_a_created_relation() -> None:
    source = Path(__file__).resolve().parents[2] / "phase168_r3_5_model_renderer.py"
    text = source.read_text(encoding="utf-8")
    assert r"$h:S^7\to S^4$ により" not in text
    assert "Do not invoke the later Lemma 5.4" not in text
    assert PRELUDE_LOCATOR != "Proposition 4.4"
```

## overrides/test_r4b_prop44_injectivity.py — 全文

```python
"""Conditioned Proposition 4.4: independent Lemma 5.4 and earlier splitting."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource,
    canonical_hopf_relation,
)
from phase174_r3_r6_r2_prop44_lemma54.source import (
    TodaPreProp44SplittingStatement,
    attach_earlier_verified_lemma54,
    expand_cited_preprop44_splitting,
)
from proof import ProofRule


def _goal(n: int = 3, k: int = 2) -> MapInjective:
    return MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(n + k, n), TodaPrimaryGroup(n + k + 1, n + 1),
    ))


def test_r4b_source_bound_dim4_has_two_real_premises():
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    proposals = expand_cited_prop44_injectivity(_goal(), (proposition, lemma))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (proposition, canonical_hopf_relation())
    assert proposals[0].rule.literature_reference.locator == "Proposition 4.4"


def test_r4b_no_unverified_hopf_or_tampered_source():
    proposition = TodaProp44UniversalStatement()
    lemma = TodaLemma54TypedSource()
    assert expand_cited_prop44_injectivity(_goal(), ()) == ()
    assert expand_cited_prop44_injectivity(_goal(), (proposition,)) == ()
    assert expand_cited_prop44_injectivity(_goal(), (proposition, proposition, lemma)) == ()
    fake = replace(proposition, includes_suspension_injectivity=False)
    assert expand_cited_prop44_injectivity(_goal(), (fake, lemma)) == ()


def test_r4b_unrelated_dimensions_and_bad_map_are_rejected():
    citations = (TodaProp44UniversalStatement(), TodaLemma54TypedSource())
    assert expand_cited_prop44_injectivity(_goal(n=4), citations) == ()
    invalid = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(7, 4)))
    assert expand_cited_prop44_injectivity(invalid, citations) == ()


def test_r4b_live_screened_lemma54_hopf_inference():
    bridge = build_shared_typed_bridge()
    candidate, = registered_group_goal_candidates(bridge, n=5, k=3)
    citing = resolve_specialized_goal_citing_id(bridge, candidate)
    assert citing is not None
    bridge = attach_earlier_verified_lemma54(bridge, citing)
    screened = screen_shared_proof_context(
        bridge, goal=candidate, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    provider = shared_expansion_provider(screened, proof_target=candidate)
    wanted = _goal()
    proof = reconstruct_registered_goal(
        wanted, screened, citing, provider, lookup_mode="typed_reference",
    )
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == wanted
    assert len(proof.premises) == 2
    assert proof.premises[0].rule is ProofRule.GIVEN
    assert proof.premises[0].conclusion == TodaProp44UniversalStatement()
    assert proof.premises[1].rule is ProofRule.INFERENCE
    assert proof.premises[1].conclusion == canonical_hopf_relation()
    assert len(proof.premises[1].premises) == 1
    assert proof.premises[1].premises[0].conclusion == TodaLemma54TypedSource()


def test_r4b_earlier_group_still_uses_printed_splitting():
    bridge = build_shared_typed_bridge()
    candidate, = registered_group_goal_candidates(bridge, n=4, k=2)
    citing = resolve_specialized_goal_citing_id(bridge, candidate)
    assert citing is not None
    assert attach_earlier_verified_lemma54(bridge, citing) is bridge
    screened = screen_shared_proof_context(
        bridge, goal=candidate, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaPreProp44SplittingStatement()) == 1
    assert available.count(TodaLemma54TypedSource()) == 0
    assert len(expand_cited_preprop44_splitting(_goal(), available)) == 1
    assert expand_cited_prop44_injectivity(_goal(), available) == ()


def test_r4b_prelude_precedes_proposition_without_hopf_invariant_assumption():
    root = Path(__file__).resolve().parents[2]
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8")
    paragraph = text.split(r"\begin{proposition}\label{prop:4.4}", 1)[0]
    assert "$n=2,4,8$ のとき, Hopf fibration" in paragraph
    assert r"E+h_*:" in paragraph
    assert not hasattr(TodaProp44UniversalStatement(), "preceding_hopf_fibration_dimensions")
```

## overrides/test_r4g_hopf_reference.py — 全文

```python
"""The pre-Proposition-4.4 source is a separately cited remark, not Proposition 4.4."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r27_r5_literature import (
    TodaProp44UniversalStatement,
    verify_prop44_hopf_fibration_source,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase174_r3_r6_r2_prop44_lemma54.source import (
    PRELUDE_LOCATOR,
    TodaPreProp44SplittingStatement,
    build_cited_preprop44_splitting,
    expand_cited_preprop44_splitting,
)
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def pi64():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    assert "\n証明\n" in markdown
    reference, body = markdown.split("\n証明\n", 1)
    return result, model, reference, body


def test_r4g_source_position_and_distinct_prelude():
    verify_prop44_hopf_fibration_source()
    root = Path(__file__).resolve().parents[2]
    text = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8")
    assert text.index("$n=2,4,8$ のとき, Hopf fibration") < text.index(
        r"\begin{proposition}\label{prop:4.4}",
    )
    bridge = build_cited_preprop44_splitting()
    assert len(bridge.proof_links) == 1
    assert bridge.proof_links[0].step.conclusion == TodaPreProp44SplittingStatement()
    reference = next(iter(bridge.registry._references.values()))
    assert reference.publication_position == 7250
    assert reference.locator == PRELUDE_LOCATOR
    assert not hasattr(TodaProp44UniversalStatement(), "preceding_hopf_fibration_dimensions")


def test_r4g_refuses_edited_chapter_iv(tmp_path):
    source = Path(__file__).resolve().parents[2] / "sources/toda/Toda_04_2.tex"
    edited = tmp_path / "Toda_04_2.tex"
    edited.write_bytes(source.read_bytes().replace(b"Hopf fibration", b"changed fibration", 1))
    with pytest.raises(ValueError, match="unverified Toda Chapter IV"):
        verify_prop44_hopf_fibration_source(edited)


def test_r4g_earlier_prelude_is_cited_separately(pi64):
    _, model, reference, body = pi64
    prelude = tuple(c for c in model.citations
                    if (c.reference.locator or c.reference.label) == PRELUDE_LOCATOR)
    assert len(prelude) == 1
    assert len(prelude[0].statement_bodies) == 1
    assert r"$n=2,4,8$" in prelude[0].statement_bodies[0]
    assert "E+h_*" in prelude[0].statement_bodies[0]
    assert PRELUDE_LOCATOR in reference
    assert r"$h:S^7\to S^4$" not in body
    assert "Proposition 4.4 直前の記述" not in reference
    assert body.rstrip().endswith("□")


def test_r4g_conditional_proposition_requires_independent_hopf_witness():
    proposition = TodaProp44UniversalStatement()
    assert not hasattr(proposition, "preceding_hopf_fibration_dimensions")
    goal = MapInjective(TodaSuspensionMap(TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4)))
    assert expand_cited_prop44_injectivity(goal, (proposition,)) == ()
    assert len(expand_cited_prop44_injectivity(
        goal, (proposition, TodaLemma54TypedSource()),
    )) == 1
    assert expand_cited_prop44_injectivity(
        goal, (replace(proposition, includes_suspension_injectivity=False),
               TodaLemma54TypedSource()),
    ) == ()
    assert len(expand_cited_preprop44_splitting(
        goal, (TodaPreProp44SplittingStatement(),),
    )) == 1


def test_r4g_web_and_prior_pi53_still_complete(pi64):
    result, _, reference, body = pi64
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert len(view.steps) == len(result.proven_steps)
    assert "Chapter IV" in reference
    bridge = build_shared_typed_bridge()
    contexts = []
    earlier = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert earlier.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(earlier, contexts[0])
    earlier_narrative = render_model_backed_narrative_markdown(earlier, model)
    assert r"$h:S^7\to S^4$" not in earlier_narrative
```

## run.ps1 — 全文

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) {
    throw 'Run after extracting this package in the EHP Proof Tracer root'
}

python -m phase174_r3_r6_r2_prop44_lemma54.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 source/HEAD guard failed' }

python -m phase174_r3_r6_r2_prop44_lemma54.verify
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 cited source check failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R3R6R2_DRY_RUN_GATE=PASS'
    exit 0
}

python -m phase174_r3_r6_r2_prop44_lemma54.patch
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 guarded patch failed' }

python -m phase174_r3_r6_r2_prop44_lemma54.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 proof ancestry audit failed' }

python -m pytest -q `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_patch.py `
    phase174_r3_r6_r2_prop44_lemma54/tests/test_source.py `
    phase169_r4b_prop44_injectivity/tests/test_r4b_prop44_injectivity.py `
    phase169_r4g_hopf_reference/tests/test_r4g_hopf_reference.py `
    phase173_r4_r1_lemma54_source_bridge/tests/test_source.py `
    phase174_r3_r6_source_extension/tests/test_source.py `
    phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
    phase174_r3_r5_preflight/tests/test_audit.py `
    phase174_r3_r4_public_delta_connection/tests/test_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R3-R6-R2 focused pytest failed' }

Write-Output 'PHASE174_R3R6R2_FOCUSED_PYTEST=PASS'
Write-Output 'PHASE174_R3R6R2_FULL_PYTEST_NOT_RUN=True'
Write-Output 'PHASE174_R3R6R2_GATE=PASS'
```
