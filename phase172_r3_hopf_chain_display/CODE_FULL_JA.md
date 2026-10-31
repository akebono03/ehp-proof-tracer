# Phase 172 R3 — 変更コード全文

## 変更対象

既存の `phase168_r3_5_model_renderer.py` は関数 `render_model_backed_narrative_markdown()` **全体**を変更する。トップレベル import は変更せず、既存関数内の局所 import のみ増える。`install.py` はソースの固定部分を照合して、完全な新関数を生成・出力する。

**既存関数全文の出力先**：`-DryRun` が作成する `%LOCALAPPDATA%\EHPProofTracerRecovery\phase172_r3_...\render_model_backed_narrative_markdown_FULL.py`。`phase168_r3_5_model_renderer_FULL.py` にはその import を含むファイル全文を出力する。出力される関数には省略記号を挿入しない。

新規クラス・関数・テストは `phase172_r3_hopf_chain_display/` 配下の各ファイルの先頭または末尾に、以下の全文のとおり追加する。

## `projection.py` — 新規 Projection のクラス・関数・import 全文

```python
"""Source-bound shortening of a verified right-Hopf composition derivation.

This module neither performs inference nor constructs ProofSteps. It recognizes
one already proven premise graph and returns only display indices/citation IDs.
Unrecognized graphs are left unchanged, without deducing equivalence from TeX.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import Composition, MapApplication
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, Relation, RelationType


@dataclass(frozen=True)
class VerifiedHopfDisplay:
    """Locations of retained mathematics and omitted intermediate prose."""

    image_index: int
    formula_index: int
    hidden_indices: frozenset[int]
    formula_citations: tuple[int, ...]
    image_citations: tuple[int, ...]


def project_verified_hopf_chain(
    model: object,
    display_order: tuple[int, ...],
    already_hidden: set[int] | frozenset[int],
) -> VerifiedHopfDisplay | None:
    """Compress only the exact cited, inferred, right-Hopf equality chain.

    Requires the original suspension witness to be visible, its derived
    equality and symmetry already hidden by R2, a cited right-Hopf formula,
    a cited generator-image GIVEN, and an inferred H-image used by surjectivity.
    Other branches and all ProofSteps/citations remain untouched.
    """
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return None
    steps = getattr(model, "steps", None)
    citations = getattr(model, "step_citation_numbers", None)
    root = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(citations, tuple)
            or len(steps) != len(citations) or type(root) is not int):
        return None
    try:
        root_scope = root_ancestor_step_indices(steps, root)
    except ValueError:
        return None
    order = tuple(display_order)
    if (any(type(i) is not int or i not in root_scope for i in order)
            or len(order) != len(set(order))):
        return None
    visible = set(order).difference(already_hidden)
    lookup = {id(step): i for i, step in enumerate(steps)}
    if len(lookup) != len(steps):
        return None

    def index(node: object) -> int | None:
        by_identity = lookup.get(id(node))
        if by_identity is not None:
            return by_identity
        matching = [i for i, step in enumerate(steps) if step == node]
        return matching[0] if len(matching) == 1 else None

    def premise_indices(node: object, count: int) -> tuple[int, ...] | None:
        parents = getattr(node, "premises", ())
        if len(parents) != count:
            return None
        indices = tuple(index(parent) for parent in parents)
        if (any(i is None or i not in root_scope for i in indices)
                or len(indices) != len(set(indices))):
            return None
        return indices

    def inferred_relation(i: int) -> bool:
        statement = steps[i].conclusion
        return (steps[i].rule is ProofRule.INFERENCE
                and isinstance(statement, Relation)
                and statement.relation_type is RelationType.EQUALITY)

    def consumers_of(i: int) -> set[int]:
        return {
            j for j in root_scope
            if any(index(parent) == i for parent in steps[j].premises)
        }

    def source_numbers(i: int) -> tuple[int, ...] | None:
        try:
            scope = root_ancestor_step_indices(steps, i)
        except ValueError:
            return None
        numbers = tuple(dict.fromkeys(
            n for j in sorted(scope) for n in citations[j]
        ))
        return numbers if numbers else None

    for surj_index in order:
        surj = steps[surj_index]
        if (surj.rule is not ProofRule.INFERENCE
                or not isinstance(surj.conclusion, MapSurjective)):
            continue
        for image_node in surj.premises:
            image_idx = index(image_node)
            if (image_idx is None or image_idx not in visible
                    or not inferred_relation(image_idx)):
                continue
            image = steps[image_idx].conclusion
            if (not isinstance(image.lhs, MapApplication)
                    or image.lhs.map != EHP_H_MAP
                    or not isinstance(image.lhs.expression, Composition)):
                continue
            pair = premise_indices(image_node, 2)
            if pair is None:
                continue
            join_idx, normalize_idx = pair
            if not inferred_relation(join_idx) or not inferred_relation(normalize_idx):
                continue
            join, normalized = steps[join_idx].conclusion, steps[normalize_idx].conclusion
            if (join.lhs != image.lhs or normalized.lhs != join.rhs
                    or normalized.rhs != image.rhs):
                continue
            join_parents = premise_indices(steps[join_idx], 2)
            if join_parents is None:
                continue
            hopf_equality_idx, substitution_idx = join_parents
            if (not inferred_relation(hopf_equality_idx)
                    or not inferred_relation(substitution_idx)):
                continue
            hopf_equality = steps[hopf_equality_idx].conclusion
            substitution = steps[substitution_idx].conclusion
            if (hopf_equality.lhs != join.lhs
                    or hopf_equality.rhs != substitution.lhs
                    or substitution.rhs != join.rhs):
                continue
            substitution_parents = premise_indices(steps[substitution_idx], 2)
            hopf_parent = premise_indices(steps[hopf_equality_idx], 1)
            normalize_parent = premise_indices(steps[normalize_idx], 1)
            if (substitution_parents is None or hopf_parent is None
                    or normalize_parent is None):
                continue
            formula_idx, cited_image_idx = substitution_parents
            composition_idx = hopf_parent[0]
            direct_idx = normalize_parent[0]
            if (not inferred_relation(formula_idx)
                    or not inferred_relation(composition_idx)
                    or not inferred_relation(direct_idx)):
                continue
            formula = steps[formula_idx].conclusion
            composition = steps[composition_idx].conclusion
            if (substitution.lhs != formula.lhs or not isinstance(formula.lhs, MapApplication)
                    or formula.lhs.map != EHP_H_MAP
                    or composition.lhs != image.lhs.expression
                    or composition.rhs != hopf_equality.rhs.expression
                    or not isinstance(hopf_equality.rhs, MapApplication)
                    or hopf_equality.rhs.map != EHP_H_MAP
                    or hopf_equality.lhs != image.lhs):
                continue
            formula_parent = premise_indices(steps[formula_idx], 1)
            composition_parent = premise_indices(steps[composition_idx], 1)
            direct_parent = premise_indices(steps[direct_idx], 1)
            if (formula_parent is None or composition_parent is None
                    or direct_parent is None):
                continue
            formula_source_idx = formula_parent[0]
            symmetry_idx = composition_parent[0]
            witness_idx = direct_parent[0]
            symmetry_parent = premise_indices(steps[symmetry_idx], 1)
            if (symmetry_parent is None or symmetry_parent[0] != direct_idx
                    or not inferred_relation(symmetry_idx)):
                continue
            if (steps[symmetry_idx].conclusion.lhs != steps[direct_idx].conclusion.rhs
                    or steps[symmetry_idx].conclusion.rhs != steps[direct_idx].conclusion.lhs):
                continue
            witness = steps[witness_idx]
            formula_source = steps[formula_source_idx]
            cited_image = steps[cited_image_idx]
            if (witness_idx not in visible or formula_idx not in visible
                    or cited_image_idx not in visible or image_idx not in visible
                    or direct_idx not in already_hidden or symmetry_idx not in already_hidden
                    or witness.rule is not ProofRule.INFERENCE
                    or not isinstance(witness.conclusion, GeneratorSuspension)
                    or typed_sentence(witness.conclusion, witness) is None
                    or formula_source.rule is not ProofRule.GIVEN
                    or cited_image.rule is not ProofRule.GIVEN
                    or not citations[formula_source_idx] or not citations[cited_image_idx]
                    or not isinstance(cited_image.conclusion, Relation)
                    or cited_image.conclusion.relation_type is not RelationType.EQUALITY
                    or not isinstance(cited_image.conclusion.lhs, MapApplication)
                    or cited_image.conclusion.lhs.map != EHP_H_MAP):
                continue
            hidden = frozenset((composition_idx, hopf_equality_idx, substitution_idx,
                                join_idx, normalize_idx))
            if (not hidden.issubset(visible) or image_idx in hidden
                    or formula_idx in hidden or cited_image_idx in hidden
                    or any(not inferred_relation(i) or citations[i] for i in hidden)):
                continue
            expected_consumers = {
                composition_idx: {hopf_equality_idx},
                hopf_equality_idx: {join_idx},
                substitution_idx: {join_idx},
                join_idx: {image_idx},
                normalize_idx: {image_idx},
            }
            if any(consumers_of(i) != expected for i, expected in expected_consumers.items()):
                continue
            formula_citations = tuple(citations[formula_source_idx])
            chain_citations = source_numbers(image_idx)
            if chain_citations is None:
                continue
            # Citation for the source suspension must be reachable through its
            # own actual premise graph, rather than a renderer-generated label.
            suspension_citations = source_numbers(witness_idx)
            if (suspension_citations is None
                    or not set(suspension_citations).issubset(chain_citations)
                    or not set(formula_citations).issubset(chain_citations)
                    or not set(citations[cited_image_idx]).issubset(chain_citations)):
                continue
            return VerifiedHopfDisplay(
                image_index=image_idx,
                formula_index=formula_idx,
                hidden_indices=hidden,
                formula_citations=formula_citations,
                image_citations=chain_citations,
            )
    return None
```

## `tests/test_projection.py` — 新規テストの fixture・関数・import 全文

```python
"""Live canonical proof tests and fail-closed Hopf narration checks."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase168_r3_26_exactness_projection import project_exactness_chains
from phase168_r3_29_order_projection import project_narrative_order
from phase172_r2_suspension_relation_display.projection import redundant_suspension_relation_indices
from phase172_r3_hopf_chain_display.projection import project_verified_hopf_chain
from proof import ProofRule


@pytest.fixture(scope="module")
def verified_pi63():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    chains = tuple(
        chain for chain in project_exactness_chains(model)
        if all(i in scope for i in chain.step_indices)
    )
    suppressed = {i for chain in chains for i in chain.step_indices}
    order = tuple(
        entry.step_index
        for entry in project_narrative_order(model, suppressed)
        if entry.step_index in scope
    )
    r2_hidden = redundant_suspension_relation_indices(model, order, suppressed)
    assert len(r2_hidden) == 2
    return result, model, order, set(suppressed).union(r2_hidden)


def test_real_hopf_chain_preserves_verified_citations_and_premises(verified_pi63):
    result, model, order, hidden = verified_pi63
    display = project_verified_hopf_chain(model, order, hidden)
    assert display is not None
    assert len(display.hidden_indices) == 5
    assert display.hidden_indices.isdisjoint(hidden)
    assert display.formula_index not in display.hidden_indices
    assert display.image_index not in display.hidden_indices
    assert display.formula_citations
    assert len(display.image_citations) == 3
    assert set(display.formula_citations).issubset(display.image_citations)
    assert all(model.steps[i].rule is ProofRule.INFERENCE for i in display.hidden_indices)
    assert all(not model.step_citation_numbers[i] for i in display.hidden_indices)
    assert result.proven_steps == model.steps
    assert len(model.citations) == 8


def test_real_public_narrative_shortens_hopf_chain_only(verified_pi63):
    result, model, order, hidden = verified_pi63
    display = project_verified_hopf_chain(model, order, hidden)
    assert display is not None
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    assert "[R3] Chapter V, i)." in reference
    assert "[R4] Proposition 2.2." in reference
    assert "[R5] (5.3)." in reference
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert r"$E\eta_{5} = \eta_{6}$." not in body
    assert r"$\eta_{6} = E\eta_{5}$." not in body
    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." not in body
    assert r"$H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert r"\operatorname{ord}(\nu')=4" in body
    assert r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}" in body
    assert len(model.citations) == 8


def test_missing_reference_prevents_hopf_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    reference_source = model.steps[verified.formula_index].premises[0]
    source_index = next(i for i, step in enumerate(model.steps) if step is reference_source)
    changed = list(model.step_citation_numbers)
    changed[source_index] = ()
    assert project_verified_hopf_chain(
        replace(model, step_citation_numbers=tuple(changed)), order, hidden,
    ) is None


def test_hidden_source_or_missing_r2_guards_prevents_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    assert project_verified_hopf_chain(model, order, set()) is None
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    assert project_verified_hopf_chain(
        replace(model, root_index=None), order, hidden,
    ) is None
    assert project_verified_hopf_chain(
        replace(model, status=ProofSearchStatus.PARTIAL), order, hidden,
    ) is None
    assert project_verified_hopf_chain(
        replace(model, open_goals=("unresolved",)), order, hidden,
    ) is None


def test_direct_citation_on_intermediate_prevents_shortening(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    changed = list(model.step_citation_numbers)
    selected = next(iter(verified.hidden_indices))
    changed[selected] = verified.formula_citations
    assert project_verified_hopf_chain(
        replace(model, step_citation_numbers=tuple(changed)), order, hidden,
    ) is None


def test_unrelated_or_invalid_display_order_is_unchanged(verified_pi63):
    _, model, order, hidden = verified_pi63
    verified = project_verified_hopf_chain(model, order, hidden)
    assert verified is not None
    assert project_verified_hopf_chain(model, order + (order[0],), hidden) is None
    assert project_verified_hopf_chain(
        model, tuple(i for i in order if i != verified.formula_index), hidden,
    ) is None
```

## `install.py` — インストーラーの関数・import 全文

```python
"""Phase 172 R3: guarded, reversible single-function presentation update."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = Path('phase168_r3_5_model_renderer.py')
PROJECTION = Path('phase172_r3_hopf_chain_display/projection.py')
TEST = Path('phase172_r3_hopf_chain_display/tests/test_projection.py')
REVIEWED_GIT_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
R2_GIT_BLOB = 'bba6280a36ca1c094be1b2a65d94ba0d2582c7a1'
REVIEWED_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
REVIEWED_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
OLD_BEFORE_LOOP = (
    '    if not incomplete:\n'
    '        from phase172_r2_suspension_relation_display.projection import (\n'
    '            redundant_suspension_relation_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_suspension_relation_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    for index in order:\n'
)
NEW_BEFORE_LOOP = (
    '    if not incomplete:\n'
    '        from phase172_r2_suspension_relation_display.projection import (\n'
    '            redundant_suspension_relation_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_suspension_relation_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    hopf_display = None\n'
    '    if not incomplete:\n'
    '        from phase172_r3_hopf_chain_display.projection import (\n'
    '            project_verified_hopf_chain,\n'
    '        )\n'
    '        hopf_display = project_verified_hopf_chain(\n'
    '            model, order, suppressed_body_indices,\n'
    '        )\n'
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    for index in order:\n'
)
OLD_IN_LOOP = (
    '        if index in suppressed_body_indices:\n'
    '            continue\n'
    '        step = model.steps[index]\n'
)
NEW_IN_LOOP = (
    '        if index in suppressed_body_indices:\n'
    '            continue\n'
    '        if hopf_display is not None and index in (\n'
    '            hopf_display.formula_index, hopf_display.image_index,\n'
    '        ):\n'
    '            latex, fallback = _group_proof_statement_latex(\n'
    '                model.steps[index].conclusion,\n'
    '            )\n'
    '            if latex is None or fallback is not None:\n'
    '                raise ValueError("verified Hopf line cannot be rendered")\n'
    '            numbers = (\n'
    '                hopf_display.formula_citations\n'
    '                if index == hopf_display.formula_index\n'
    '                else hopf_display.image_citations\n'
    '            )\n'
    '            source_tags = ", ".join(f"[R{number}]" for number in numbers)\n'
    '            lines.extend((f"{source_tags}より, ${latex}$.", ""))\n'
    '            continue\n'
    '        step = model.steps[index]\n'
)
TEST_GROUPS = (
    ('phase172_r3_hopf_chain_display/tests/test_projection.py',),
    ('phase172_r2_suspension_relation_display/tests/test_projection.py',),
    ('phase171_r20r13_eta_sentence_layout/tests/test_projection.py',),
    ('phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py',),
    ('phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py',),
)


def command(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
        errors='replace', check=False, timeout=timeout,
    )


def checked(args: list[str]) -> str:
    result = command(args)
    if result.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ' ' + result.stderr[-900:])
    return result.stdout.strip()


def normalized(raw: bytes) -> str:
    data = raw.decode('utf-8-sig')
    if '\r' in data.replace('\r\n', ''):
        raise RuntimeError('mixed newlines are unsupported')
    return data.replace('\r\n', '\n')


def git_blob(raw: bytes) -> str:
    header = b'blob ' + str(len(raw)).encode('ascii') + b'\0'
    return hashlib.sha1(header + raw).hexdigest()


def transformed(raw: bytes) -> bytes:
    source = normalized(raw)
    if (source.count(OLD_BEFORE_LOOP) != 1
            or source.count(OLD_IN_LOOP) != 1
            or NEW_BEFORE_LOOP in source
            or NEW_IN_LOOP in source):
        raise RuntimeError('reviewed R2 Renderer anchors are not unique')
    replaced = source.replace(OLD_BEFORE_LOOP, NEW_BEFORE_LOOP, 1)
    replaced = replaced.replace(OLD_IN_LOOP, NEW_IN_LOOP, 1)
    tree = ast.parse(replaced)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == 'render_model_backed_narrative_markdown']
    if len(functions) != 1:
        raise RuntimeError('expected exactly one Renderer function')
    ending = '\r\n' if b'\r\n' in raw else '\n'
    return replaced.replace('\n', ending).encode('utf-8')


def full_function(raw: bytes) -> str:
    source = normalized(raw)
    tree = ast.parse(source)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == 'render_model_backed_narrative_markdown']
    if len(functions) != 1:
        raise RuntimeError('Renderer function missing/ambiguous')
    node = functions[0]
    return '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    branch = checked(['git', 'branch', '--show-current'])
    head = checked(['git', 'rev-parse', 'HEAD'])
    if branch != 'develop':
        raise RuntimeError('R3 requires develop')
    blob = checked(['git', 'rev-parse', 'HEAD:' + TARGET.as_posix()])
    if blob != REVIEWED_GIT_BLOB:
        raise RuntimeError('committed Renderer differs from reviewed R2 source')
    r2_blob = checked(['git', 'rev-parse', 'HEAD:phase172_r2_suspension_relation_display/projection.py'])
    if r2_blob != R2_GIT_BLOB:
        raise RuntimeError('committed R2 typed comparison differs from reviewed source')
    work_status = checked(['git', 'status', '--porcelain=v1', '--', TARGET.as_posix()])
    if work_status:
        raise RuntimeError('Renderer has local changes; not overwriting')
    tracked = subprocess.run(
        ['git', 'show', 'HEAD:' + TARGET.as_posix()], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout
    actual = (ROOT / TARGET).read_bytes()
    if normalized(tracked) != normalized(actual):
        raise RuntimeError('worktree Renderer differs from HEAD')
    for path, expected_sha in (
        (PROJECTION, REVIEWED_PROJECTION_SHA256),
        (TEST, REVIEWED_TEST_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('R3 package file missing: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected_sha:
            raise RuntimeError('R3 package payload differs from reviewed content: ' + str(path))
    remote = command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop changed; review updated HEAD first')
    transformed(actual)
    return {
        'branch': branch, 'head': head, 'remote_develop': remote_head,
        'head_renderer_blob': blob, 'r2_projection_blob': r2_blob,
        'worktree_renderer_sha256': hashlib.sha256(actual).hexdigest(),
    }


def report_dir() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    path = base / ('phase172_r3_' + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def run_focused(output: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    tested = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        run = subprocess.run(
            [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short',
             '-p', 'no:cacheprovider', *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', errors='replace', check=False, timeout=200,
        )
        log = run.stdout + '\n' + run.stderr
        (output / f'focused_{number}.log').write_text(log, encoding='utf-8')
        tested.append({'number': number, 'paths': list(paths),
                       'exit_code': run.returncode,
                       'last_lines': log.splitlines()[-15:]})
        print(f'PHASE172_R3_FOCUSED_{number}=' +
              ('PASS' if run.returncode == 0 else 'FAIL'), flush=True)
        if run.returncode:
            raise RuntimeError('focused pytest failed: ' + str(number) + '\n' + log[-2200:])
    return tested


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    state = preflight()
    print('PHASE172_R3_BRANCH=' + str(state['branch']), flush=True)
    print('PHASE172_R3_HEAD=' + str(state['head']), flush=True)
    print('PHASE172_R3_REVIEWED_SOURCE=PASS', flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = transformed(before)
    output = report_dir()
    (output / 'render_model_backed_narrative_markdown_FULL.py').write_text(
        full_function(after), encoding='utf-8',
    )
    (output / 'phase168_r3_5_model_renderer_FULL.py').write_bytes(after)
    if args.dry_run:
        print('PHASE172_R3_DRY_RUN=PASS', flush=True)
        print('PHASE172_R3_FULL_FUNCTION=' + str(output), flush=True)
        print('PHASE172_R3_SOURCE_CHANGES=0', flush=True)
        return 0
    (output / 'renderer_before.py').write_bytes(before)
    report: dict[str, object] = {
        'phase': '172-R3', 'mode': 'GUARDED_PRESENTATION_ONLY',
        'state': state, 'full_pytest_executed': False,
        'proof_tree_modified': False, 'mathematical_rules_modified': False,
        'focused': [],
    }
    try:
        (ROOT / TARGET).write_bytes(after)
        if args.run_focused_tests:
            report['focused'] = run_focused(output)
        report['result'] = 'PASS_R3_HOPF_DISPLAY_ONLY'
    except BaseException as error:
        (ROOT / TARGET).write_bytes(before)
        report['result'] = 'FAILED_RESTORED_SOURCE'
        report['diagnostic'] = repr(error)
        (output / 'result.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
        print('PHASE172_R3_RESTORED=PASS', flush=True)
        print('PHASE172_R3_REPORT=' + str(output), flush=True)
        raise
    (output / 'result.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print('PHASE172_R3_REPORT=' + str(output), flush=True)
    print('PHASE172_R3_SOURCE_CHANGES=1', flush=True)
    print('PHASE172_R3_RESULT=PASS_R3_HOPF_DISPLAY_ONLY', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## `run.ps1` — PowerShell Runner 全文

```powershell
param(
    [switch]$DryRun,
    [switch]$RunFocusedTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldLocation = (Get-Location).Path
$OldPath = $env:PYTHONPATH
$OldUtf8 = $env:PYTHONUTF8
$OldEncoding = $env:PYTHONIOENCODING
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    Set-Location $Root
    $env:PYTHONPATH = "$Root;$OldPath"
    $env:PYTHONUTF8 = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $Arguments = @('-B', '-m', 'phase172_r3_hopf_chain_display.install')
    if ($DryRun) {
        $Arguments += '--dry-run'
    }
    if ($RunFocusedTests) {
        $Arguments += '--run-focused-tests'
    }
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 172 R3 failed with exit code $LASTEXITCODE"
    }
}
finally {
    Set-Location $OldLocation
    $env:PYTHONPATH = $OldPath
    $env:PYTHONUTF8 = $OldUtf8
    $env:PYTHONIOENCODING = $OldEncoding
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
}
```

