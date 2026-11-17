# Phase 175 R3R12R4 — 変更コード全文

## 変更対象と追加位置

1. `phase175_r3r12_hopf_conclusion/projection.py`：既存の `project_verified_hopf_lift_conclusion()` を関数全文で置換。import は `map_symbol_tex` を追加するため、変更後の import 全文を下記に掲載する。その他の関数・クラスは変更しない。
2. `phase175_r3r12_hopf_conclusion/tests/test_projection.py`：`test_pi73_single_final_conclusion_and_hopf_isomorphism()`、`test_internal_cyclic_latex_is_not_a_second_proof_requirement()`、`test_injectivity_line_matches_the_real_typed_renderer()`、`test_pi63_old_narrative_remains_unchanged()` の文言期待値のみ更新。新規 `test_concise_consequences_follow_typed_hopf_map()` を `test_partial_or_missing_source_citations_are_unchanged()` の直前に追加。テスト用 import は以下に全文を掲載する。
3. `phase175_r3r12_hopf_conclusion/audit.py`：`GATE` 定数、`_public_gate()`、`run()`、`main()` を更新。変更後の import 全文・関数全文を下記に掲載する。
4. `phase175_r3r12_hopf_conclusion/run.ps1`：ファイル全文を下記に掲載する。
5. README.md（英語）、AUDIT_PLAN_JA.md、TEST_RESULTS_JA.md、CODE_FULL_JA.md（日本語）は全文更新して同梱。

既存の `phase175_r3r11_cited_hopf_narrative/projection.py` は今回変更しない（R3R12R3 の接続済み関数を引き続き使用）。数学的推論規則、出典 GIVEN、ProofStep、プロジェクト基幹5文書に変更なし。

## `projection.py` — import 全文

```python
"""Shared certified finite-cyclic Hopf-lift conclusion presentation.

This module reads a completed, verified Proof Tree and already rendered lines.
It never performs a search, registers a mathematical rule or adds a ProofStep.
It refuses presentation changes if any source, image or displayed anchor is
ambiguous. It is intentionally independent of concrete sphere dimensions.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import group_tex, map_symbol_tex, typed_sentence
from phase175_r3_pi73_hopf_lift.rule import RULE_NAME, hopf_lift_inputs
from proof import ProofRule, Relation, RelationType
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from web_group_proof_common import _group_proof_statement_latex
```

## `projection.py` — `project_verified_hopf_lift_conclusion()` 全文

```python
def project_verified_hopf_lift_conclusion(lines: list[str], model) -> list[str]:
    """Explain generator-surjectivity/isomorphism and hide one duplicate.

    The isomorphism is the direct verbal consequence of the *existing* typed
    general lift's proved injectivity + proved finite cyclic target + proved
    generator image. This function creates neither MapSurjective nor a theorem.
    """
    original = list(lines)
    if original.count("証明") != 1 or original.count("□") != 1:
        return original
    certificate = _certified_hopf_lift(model)
    if certificate is None:
        return original
    scope, root, cyclic_step, positions = certificate
    injective_step, codomain_step, image_step = cyclic_step.premises
    group_relation = root.conclusion
    codomain_relation = codomain_step.conclusion
    image_relation = image_step.conclusion
    # The existing lift's typed generator identity is already checked by
    # hopf_lift_inputs().  Its internal CyclicStructureStatement may use a
    # different generator spelling from the published root Relation.  Match
    # the two *displayed* copies of the root's certified conclusion instead.
    root_latex, root_fallback = _group_proof_statement_latex(group_relation)
    codomain_latex, codomain_fallback = _group_proof_statement_latex(codomain_relation)
    if (root_fallback is not None or codomain_fallback is not None
            or not root_latex or not codomain_latex):
        return original
    source_group = group_tex(group_relation.lhs)
    target_group = group_tex(codomain_relation.lhs)
    if not source_group or not target_group:
        return original
    # The general Hopf-lift premise already certifies the *typed* generator
    # identity. A source generator can have a different internal spelling from
    # the canonical public group generator; do not compare their TeX strings.
    # Use the same public generator renderer as the cited codomain equation.
    try:
        generator_tex = render_toda_public_group_generator_latex(
            codomain_relation.rhs.generator,
        )
    except (TypeError, ValueError, AttributeError):
        return original
    if not generator_tex:
        return original
    boundary = original.index("証明")
    final = f"以上より, ${root_latex}$."
    intermediate = f"${root_latex}$."
    intermediate_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == intermediate
    ]
    final_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == final
    ]
    # R3R11 has already certified every equality in its compact Hopf chain.
    # Match the source numbers of the actual proved image step, not a guessed
    # generator-name spelling or a narrative line from an unrelated proof.
    image_sources = _source_numbers(model, positions[2], scope)
    image_prefix = (
        ", ".join(f"[R{number}]" for number in image_sources)
        + "より, $H("
    )
    image_indices = [
        i for i in range(boundary + 1, len(original))
        if len(image_sources) >= 2
        and original[i].startswith(image_prefix)
        and original[i].endswith(f"={generator_tex}$.")
        and original[i].count("$") == 2
    ]
    # The common renderer inserts spacing after "H:" and decorates the
    # sentence using the proved exactness premises. Reuse that same typed
    # sentence instead of guessing its textual punctuation or whitespace.
    # The certificate has already identified this exact MapInjective step.
    injectivity_sentence = typed_sentence(
        injective_step.conclusion, injective_step,
    )
    if (not isinstance(injectivity_sentence, str)
            or not injectivity_sentence.endswith("は単射.")):
        return original
    injection_indices = [
        i for i in range(boundary + 1, len(original))
        if original[i] == injectivity_sentence
    ]
    if (len(intermediate_indices) != 1 or len(final_indices) != 1
            or len(image_indices) != 1 or len(injection_indices) != 1):
        return original
    duplicate_at = intermediate_indices[0]
    final_at = final_indices[0]
    if not (injection_indices[0] < image_indices[0] < duplicate_at < final_at):
        return original
    source_numbers = _source_numbers(model, positions[1], scope)
    # The target group structure must already be displayed with its real
    # unique source. Without that source binding, leave all text untouched.
    if len(source_numbers) != 1:
        return original
    expected = f"[R{source_numbers[0]}]より, ${codomain_latex}$."
    if original.count(expected) != 1:
        return original
    # Existing typed premises certify surjectivity and, together with
    # injectivity, an isomorphism.  Render only their short common
    # consequences; do not manufacture MapSurjective/MapIsomorphism steps.
    symbol = map_symbol_tex(injective_step.conclusion.map)
    if not symbol:
        return original
    surjective = f"よって, ${symbol}$ は全射."
    isomorphism = f"よって, ${symbol}$ は同型."
    changed = []
    for index, line in enumerate(original):
        if index == duplicate_at:
            changed.extend((surjective, "", isomorphism))
        else:
            changed.append(line)
    return changed
```

## `tests/test_projection.py` — import 全文

```python
"""Live public model and fail-closed cyclic Hopf-lift narrative contracts."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase175_r3r12_hopf_conclusion.projection import (
    _certified_hopf_lift,
    project_verified_hopf_lift_conclusion,
)
```

## テスト `test_pi73_single_final_conclusion_and_hopf_isomorphism` 全文

```python
def test_pi73_single_final_conclusion_and_hopf_isomorphism(pi73_verified) -> None:
    result, model = pi73_verified
    before = tuple(id(step) for step in model.steps)
    assert _certified_hopf_lift(model) is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    references, body = markdown.split("\n証明\n", 1)
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(summary) == 1
    assert body.count(conclusion) == 1, (
        "Duplicated root conclusion; root and cyclic generator renderers may differ",
        body,
    )
    assert "以上より, " + conclusion in body
    assert "\n" + conclusion + "\n" not in body
    assert body.count("よって, $H$ は全射.") == 1
    assert body.count("よって, $H$ は同型.") == 1
    assert "の生成元であり" not in body
    assert "すでに $H$ は単射なので" not in body
    assert (body.index(summary) < body.index("よって, $H$ は全射.")
            < body.index("よって, $H$ は同型.")
            < body.index("以上より, " + conclusion))
    assert "**[R2] Lemma 5.7.**" in references
    assert "**[R6] Proposition 2.2.**" in references
    assert len(model.citations) == 7
    assert before == tuple(id(step) for step in model.steps)
```

## テスト `test_concise_consequences_follow_typed_hopf_map` 全文

```python
def test_concise_consequences_follow_typed_hopf_map(pi73_verified) -> None:
    """The same certified map symbol owns both short consequences."""
    from phase168_r3_27_typed_statement_projection import map_symbol_tex

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    _, _, cyclic_step, _ = certificate
    map_symbol = map_symbol_tex(cyclic_step.premises[0].conclusion.map)
    assert map_symbol == "H"
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    sentences = body.splitlines()
    assert sentences.count(f"よって, ${map_symbol}$ は全射.") == 1
    assert sentences.count(f"よって, ${map_symbol}$ は同型.") == 1
    assert all("生成元であり" not in sentence for sentence in sentences)
```

## テスト `test_internal_cyclic_latex_is_not_a_second_proof_requirement` 全文

```python
def test_internal_cyclic_latex_is_not_a_second_proof_requirement(
    pi73_verified, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Typed Hopf-lift certificate, not an internal string, owns generator identity."""
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase175_r3r12_hopf_conclusion import projection

    result, model = pi73_verified
    original_renderer = projection._group_proof_statement_latex

    def internal_cyclic_unrenderable(statement):
        if isinstance(statement, CyclicStructureStatement):
            return None, "internal cyclic spelling intentionally unavailable"
        return original_renderer(statement)

    monkeypatch.setattr(
        projection, "_group_proof_statement_latex", internal_cyclic_unrenderable,
    )
    content = render_model_backed_narrative_markdown(result, model)
    _, body = content.split("\n証明\n", 1)
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    assert body.count(conclusion) == 1, body
    assert "よって, $H$ は同型." in body
```

## テスト `test_injectivity_line_matches_the_real_typed_renderer` 全文

```python
def test_injectivity_line_matches_the_real_typed_renderer(pi73_verified) -> None:
    """The actual renderer emits a space after H:, unlike an old hand-coded guard."""
    from phase168_r3_27_typed_statement_projection import typed_sentence

    result, model = pi73_verified
    certificate = _certified_hopf_lift(model)
    assert certificate is not None
    _, _, cyclic_step, _ = certificate
    injective_step = cyclic_step.premises[0]
    sentence = typed_sentence(injective_step.conclusion, injective_step)
    assert sentence is not None
    assert r"$H: \pi_{7}^{3}\to \pi_{7}^{5}$ は単射." in sentence
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert sentence in body.splitlines()
    assert "よって, $H$ は同型." in body
```

## テスト `test_pi63_old_narrative_remains_unchanged` 全文

```python
def test_pi63_old_narrative_remains_unchanged() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing_id is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing_id,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    _, body = markdown.split("\n証明\n", 1)
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert "よって, $H$ は同型." not in body
```

## `audit.py` — import 全文と変更した定数

```python
"""R3R12 read-only preflight, focused tests and public source-bound gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r12_hopf_conclusion import install

GATE = "PASS_R3R12R4_CONCISE_VERIFIED_HOPF_CONSEQUENCES"
```

## `audit.py` — `_public_gate` 全文

```python
def _public_gate() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    recorded = inspect_one_group(3, 4)
    previous = verify_public_result(recorded)
    markdown = recorded.get("markdown")
    if not isinstance(markdown, str) or markdown.count("\n証明\n") != 1:
        raise RuntimeError("R3R12_PUBLIC_MARKDOWN_MISSING")
    references, body = markdown.split("\n証明\n", 1)
    if (recorded.get("web_key") != "generic-complete-proof"
            or recorded.get("trust_verified") is not True
            or recorded.get("reference_count") != 7
            or previous["search_status"] != "complete"
            or previous["lemma54_used"] is not False):
        raise RuntimeError("R3R12_PROOF_OR_TRUST_CHANGED")
    summary = (
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    conclusion = r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$."
    surjective = "よって, $H$ は全射."
    isomorphism = "よって, $H$ は同型."
    if (body.count(summary) != 1 or body.count(conclusion) != 1
            or body.count("以上より, " + conclusion) != 1
            or body.count(surjective) != 1 or body.count(isomorphism) != 1
            or "の生成元であり" in body or "すでに $H$ は単射なので" in body
            or not (body.index(summary) < body.index(surjective)
                    < body.index(isomorphism)
                    < body.index("以上より, " + conclusion))):
        raise RuntimeError("R3R12_SINGLE_CONCLUSION_OR_HOPF_EXPLANATION_FAILED")
    if (r"$E(\eta_2\nu')=0$." not in references
            or r"$H(\alpha E\beta)=H(\alpha) E\beta$." not in references
            or "特に, " in references or "右合成公式: " in references):
        raise RuntimeError("R3R12_OLDER_REFERENCE_BODIES_CHANGED")
    return {
        "search": previous["search_status"],
        "web": recorded["web_key"],
        "trust": recorded["trust_verified"],
        "reference_count": recorded["reference_count"],
        "lemma54_used": previous["lemma54_used"],
        "hopf_summary": summary,
        "hopf_surjective": surjective,
        "hopf_isomorphism": isomorphism,
        "final_conclusion": "以上より, " + conclusion,
        "final_conclusion_count": body.count(conclusion),
        "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
    }
```

## `audit.py` — `run` 全文

```python
def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = root.resolve()
    checked = preflight(root)
    plan = checked["plan"]
    label = "PHASE175_R3R12R4_"
    print(label + "BRANCH=develop")
    print(label + "HEAD=" + checked["head"])
    print(label + "REVIEWED_BLOB=" + checked["reviewed_blob"])
    print(label + "PATCH_STATUS=" + plan.status)
    print(label + "NEW_GIVEN=0")
    print(label + "NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print(label + "GATE=PASS_R3R12R4_READ_ONLY_DRYRUN")
        return 0

    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / "phase175_r3r12r4_hopf_conclusion")
    folder.mkdir(parents=True, exist_ok=True)
    target = root / install.TARGET
    if plan.status == "PATCH_REQUIRED":
        (folder / "r3r11_projection_backup.py").write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        environment = dict(os.environ)
        environment.update(
            PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
        )
        command = [
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
            *TEST_PATHS,
        ]
        result = subprocess.run(
            command, cwd=root, env=environment, capture_output=True,
            text=True, encoding="utf-8", errors="replace",
            timeout=timeout_seconds, check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            result.stdout + "\n" + result.stderr, encoding="utf-8",
        )
        print(result.stdout[-6000:])
        if result.returncode:
            raise RuntimeError("R3R12_FOCUSED_PYTEST_FAILED")
        print(label + "FOCUSED_PYTEST=PASS")
        public = _public_gate()
        (folder / "report.json").write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "head": checked["head"],
            "before_sha256": sha256(plan.old_bytes).hexdigest(),
            "after_sha256": sha256(target.read_bytes()).hexdigest(),
            "public": public,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        for key, value in public.items():
            print(label + key.upper() + "=" + str(value))
        print(label + "GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print(label + "ROLLBACK=RESTORED")
            else:
                print(label + "ROLLBACK=MANUAL_INSPECTION_REQUIRED")
        raise
```

## `audit.py` — `main` 全文

```python
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        return run(args.root, args.dry_run, args.timeout_seconds)
    except Exception:
        traceback.print_exc()
        print("PHASE175_R3R12R4_GATE=FAIL")
        return 1
```

## `run.ps1` — 全文

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    & python -B -m phase175_r3r12_hopf_conclusion.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R12R4_EXIT_CODE=$code"
    exit $code
}

& python -B -m phase175_r3r12_hopf_conclusion.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R12R4_EXIT_CODE=$code"
exit $code
```
