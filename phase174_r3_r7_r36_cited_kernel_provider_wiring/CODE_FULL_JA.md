# R36 変更・追加コード全文

## 変更対象

既存 `phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py::build_context_expansion_provider_registry` のみを関数全体で置換。トップレベル import は変更なし。既存テスト変更なし。

## 変更後のファイル全文（関数全体を含む）

### `replacement/context_provider_registry.py`

```python
"""Register context-bound shared expansion providers without altering their mathematical rules."""
from __future__ import annotations

from typing import Callable

from phase165_r6_2_unified_registry_r3_r3.provider_registry import UnifiedExpansionProviderRegistry


def build_context_expansion_provider_registry(
    *, available: tuple[object, ...], prior_conclusions: tuple[object, ...],
    expand_registered_toda45_finite_cyclic_goal: Callable,
    expand_registered_eta_specialization: Callable,
    expand_registered_delta_image_goal: Callable,
    expand_cited_general_specialization: Callable,
) -> UnifiedExpansionProviderRegistry:
    """Keep four historical providers; append R35 only for cited Delta witnesses."""
    if not isinstance(available, tuple) or not isinstance(prior_conclusions, tuple):
        raise TypeError("context statements must be tuples")
    registry = UnifiedExpansionProviderRegistry()
    specifications = (
        ("phase165_r57_r7_stable_expansion.expand_registered_toda45_finite_cyclic_goal",
         expand_registered_toda45_finite_cyclic_goal, available + prior_conclusions),
        ("phase165_r57_r8_eta_specialization.expand_registered_eta_specialization",
         expand_registered_eta_specialization, available),
        ("phase165_r57_r19_delta_image_backward.expand_registered_delta_image_goal",
         expand_registered_delta_image_goal, available),
        ("phase165_r57_r20_general_specialization.expand_cited_general_specialization",
         expand_cited_general_specialization, available),
    )
    # Only an already-screened cited source context can enable the R35 rule.
    # This does not certify a kernel or turn any premise into a proof step.
    from homotopy_groups import FiniteCyclicGroup
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement
    signed_images = tuple(
        statement for statement in available
        if type(statement) is TodaDeltaImageUpToSignStatement
    )
    if any(
        type(statement) is Relation
        and statement.relation_type is RelationType.EQUALITY
        and statement.lhs == getattr(getattr(image, "map", None), "target_group", None)
        and type(statement.rhs) is FiniteCyclicGroup
        and type(statement.rhs.order) is int
        and statement.rhs.order >= 1
        and statement.rhs.generator == image.positive_value
        for image in signed_images for statement in available
    ):
        from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
            expand_cyclic_delta_kernel,
        )
        specifications = specifications + ((
            "phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule.expand_cyclic_delta_kernel",
            expand_cyclic_delta_kernel, available,
        ),)
    for provider_id, function, statements in specifications:
        if not callable(function):
            raise TypeError("context expansion provider must be callable")
        def bound(goal: object, *, _function=function, _statements=statements):
            return _function(goal, _statements)
        registry.register(provider_id, bound, origin="SHARED_CITED_CONTEXT")
    return registry
```

### `install.py`

```python
"""Guarded, idempotent installation of one reviewed shared provider function."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py"
REVIEWED_HEAD = "4200211563834028ed6c4e2eeb01004646b92ba9"
REVIEWED_SUCCESSOR_PREFIX = "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/"
GIT_PINS = {
    TARGET: "34b9cd021f768b404bbcbc8fe9d3cc7fe91b287f",
    "phase165_r52_r9_shared_math.py": "6b965aa49db2ad8707c75dcc953d3c78cdd3e458",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py":
        "b90fe1fee5db04228ed986083b5214709045a7ea",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
}
R35_PATH = "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py"
R35_SHA256 = "f8eb16242ea91c6c8c1c3a991650e2708add16c06b9d4ac0741cae148b4e2847"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def canonical(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def reviewed_blob_matches(data: bytes, expected: str) -> bool:
    normalized = canonical(data)
    return any(
        git_blob_sha(candidate) == expected
        for candidate in (data, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def baseline_source() -> str:
    return (PACKAGE / "baseline" / "context_provider_registry.py").read_text(
        encoding="utf-8-sig"
    ).replace("\r\n", "\n")


def replacement_source() -> str:
    return (PACKAGE / "replacement" / "context_provider_registry.py").read_text(
        encoding="utf-8-sig"
    ).replace("\r\n", "\n")


def patch_source(source: str) -> str:
    """Replace exactly the reviewed whole function; reject unreviewed changes."""
    if not isinstance(source, str):
        raise TypeError("source must be text")
    original = baseline_source()
    replacement = replacement_source()
    if source.replace("\r\n", "\n") == replacement:
        return replacement
    if source.replace("\r\n", "\n") != original:
        raise ValueError("Context provider code changed outside reviewed R36 scope")
    if not reviewed_blob_matches(original.encode("utf-8"), GIT_PINS[TARGET]):
        raise ValueError("R36 baseline does not match the reviewed GitHub code")
    compile(replacement, TARGET, "exec")
    return replacement


def verify_checkout() -> dict[str, object]:
    """Allow only the reviewed R34 HEAD and a R35-only merge successor."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R36 directly into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R36 requires develop")
    local = git("rev-parse", "HEAD")
    raw_remote = git("ls-remote", "origin", "refs/heads/develop")
    remote = raw_remote.split()[0] if raw_remote else ""
    if not remote:
        raise RuntimeError("Cannot verify current GitHub develop")
    reviewed_additions: tuple[str, ...] = ()
    if remote != REVIEWED_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote HEAD changed during source review")
        descendant = subprocess.run(
            ("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, remote),
            cwd=ROOT, capture_output=True,
        )
        if descendant.returncode != 0:
            raise RuntimeError("Remote HEAD has unreviewed lineage")
        reviewed_additions = tuple(
            git("diff", "--name-only", REVIEWED_HEAD, remote).splitlines()
        )
        if not reviewed_additions or any(
            not path.startswith(REVIEWED_SUCCESSOR_PREFIX)
            for path in reviewed_additions
        ):
            raise RuntimeError("Remote changed files beyond the reviewed R35 handoff")
    if local not in (REVIEWED_HEAD, remote):
        raise RuntimeError("Local HEAD requires review before R36 installation")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    changed = git("diff", "--name-only").splitlines()
    if changed not in ([], [TARGET]):
        raise RuntimeError("Unexpected tracked edits; no reset performed: " + repr(changed))
    for path, expected in GIT_PINS.items():
        if path == TARGET:
            data = baseline_source().encode("utf-8")
        else:
            file = ROOT / path
            if not file.is_file():
                raise RuntimeError("Reviewed file missing: " + path)
            data = file.read_bytes()
        if not reviewed_blob_matches(data, expected):
            raise RuntimeError("Reviewed GitHub blob mismatch: " + path)
    r35 = ROOT / R35_PATH
    if not r35.is_file() or hashlib.sha256(canonical(r35.read_bytes())).hexdigest() != R35_SHA256:
        raise RuntimeError("R35 isolated general rule missing or unreviewed")
    if not (PACKAGE / "baseline/context_provider_registry.py").is_file():
        raise RuntimeError("R36 replacement baseline missing")
    actual = (ROOT / TARGET).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    if actual not in (baseline_source(), replacement_source()):
        raise RuntimeError("Tracked context provider differs from both reviewed states")
    if (actual == baseline_source() and changed) or (actual == replacement_source() and changed != [TARGET]):
        raise RuntimeError("Tracked file state disagrees with reviewed R36 installation")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r35_rule_preserved": True,
        "r34_sources_preserved": True,
        "tracked_mode": "INSTALLED" if actual == replacement_source() else "BASELINE",
        "reviewed_successor_files": len(reviewed_additions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    prefix = "PHASE174_R3R7R36_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if args.dry_run:
        print(prefix + "GATE=PASS_R36_REVIEWED_SOURCE_PREFLIGHT")
        print("(END)")
        return 0
    file = ROOT / TARGET
    updated = patch_source(file.read_text(encoding="utf-8-sig"))
    if state["tracked_mode"] == "BASELINE":
        original_bytes = file.read_bytes()
        separator = "\r\n" if b"\r\n" in original_bytes else "\n"
        bom = b"\xef\xbb\xbf" if original_bytes.startswith(b"\xef\xbb\xbf") else b""
        file.write_bytes(bom + updated.replace("\n", separator).encode("utf-8"))
    verify_checkout()
    print(prefix + "MODE=INSTALLED")
    print(prefix + "GATE=PASS_R36_MINIMAL_CONTEXT_PROVIDER_INSTALLED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `audit.py`

```python
"""Audit actual R34 cited steps, R35 rule and R36 shared provider integration."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r36_cited_kernel_provider_wiring.install import verify_checkout

ROOT = Path(__file__).resolve().parents[1]


def audit_public_connection() -> dict[str, object]:
    """Require real screened source facts and reconstruct only cited inferences."""
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    cited_steps = tuple(
        link.step for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )
    codomain, signed_image = checked_prior_statements(ROOT)
    codomain_step = next((step for step in cited_steps if step.conclusion == codomain), None)
    image_step = next((step for step in cited_steps if step.conclusion == signed_image), None)
    if codomain_step is None or image_step is None or codomain_step is image_step:
        raise RuntimeError("R34 cited codomain / signed image must be two distinct steps")
    for step, locator in ((codomain_step, "Proposition 5.8"), (image_step, "(5.10)")):
        parent = step.inference_rule
        if (parent is None or parent.literature_reference is None
                or parent.literature_reference.locator != locator):
            raise RuntimeError("Missing independently cited source: " + locator)
    domain = signed_image.map.source_group
    diagonal = Relation(
        domain, FreeCyclicGroup(signed_image.element), RelationType.EQUALITY,
    )
    kernel_goal = KernelMultipleStatement(signed_image.map, domain, signed_image.element, 2)
    provider = shared_expansion_provider(screened, proof_target=root)
    proposals = tuple(
        item for item in provider(kernel_goal)
        if item.rule.name == RULE_NAME
        and item.subgoals == (diagonal, codomain, signed_image)
    )
    if not proposals:
        raise RuntimeError("R35 kernel rule not reached through the shared provider")
    diagonal_proposals = tuple(
        item for item in provider(diagonal)
        if item.rule.name == "generic cited typed scalar specialization"
        and len(item.subgoals) == 1
    )
    diagonal_step = None
    for proposal in diagonal_proposals:
        source_step = next(
            (step for step in cited_steps if step.conclusion == proposal.subgoals[0]),
            None,
        )
        if source_step is None or source_step.inference_rule is None:
            continue
        if source_step.inference_rule.literature_reference is None:
            continue
        matches = find_inference_matches_for_rule(proposal.rule, (source_step,))
        if not matches:
            continue
        candidate = apply_inference_match(matches[0])
        if candidate.rule is ProofRule.INFERENCE and candidate.conclusion == diagonal:
            diagonal_step = candidate
            break
    if diagonal_step is None:
        raise RuntimeError("Diagonal group cannot be inferred from a cited general source")
    matches = find_inference_matches_for_rule(
        proposals[0].rule, (diagonal_step, codomain_step, image_step),
    )
    if not matches:
        raise RuntimeError("Cited three-premise kernel inference did not match")
    inferred_kernel = apply_inference_match(matches[0])
    if (inferred_kernel.rule is not ProofRule.INFERENCE
            or inferred_kernel.conclusion != kernel_goal
            or inferred_kernel.premises != (diagonal_step, codomain_step, image_step)):
        raise RuntimeError("Kernel proof ancestry differs from the actual cited premises")
    if any(step.conclusion == kernel_goal or step.conclusion == root for step in cited_steps):
        raise RuntimeError("Forbidden kernel/root direct GIVEN was introduced")
    return {
        "screened_cited_codomain": 1,
        "screened_cited_generator_image": 1,
        "shared_kernel_proposals": len(proposals),
        "diagonal_source_inferred": True,
        "three_real_cited_premises_form_inference": True,
        "kernel_inference_in_audit": True,
        "kernel_inference_inserted_as_given": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def report(dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if not dry_run and state["tracked_mode"] != "INSTALLED":
        raise RuntimeError("Install R36 provider before running public audit")
    observations = None if dry_run else audit_public_connection()
    return {
        "phase": "174-R3-R7-R36",
        "git_state": state,
        "observations": observations,
        "new_givens": 0,
        "new_direct_kernel_givens": 0,
        "new_direct_root_givens": 0,
        "new_general_rules": 0,
        "shared_provider_connections": 1 if observations is not None else 0,
        "root_complete": False,
        "full_pytest": False,
        "gate": (
            "PASS_R36_SOURCE_PREFLIGHT_ONLY" if dry_run else
            "PASS_R36_CITED_CYCLIC_KERNEL_PUBLIC_PROVIDER_CONNECTED_ROOT_PENDING"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(args.dry_run)
    outdir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r36"
    )
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / ("preflight.json" if args.dry_run else "public_kernel_provider.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R36_"
    for key, value in result["git_state"].items():
        if key != "reviewed_successor_files":
            print(p + key.upper() + "=" + str(value))
    if result["observations"] is not None:
        for key, value in result["observations"].items():
            print(p + key.upper() + "=" + str(value))
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_MATH_RULES=0")
    print(p + "ROOT_COMPLETE=False")
    print(p + "FULL_PYTEST=False")
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `tests/test_static.py`

```python
"""R36 guarded replacement and scope tests, requiring no project imports."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r36_cited_kernel_provider_wiring.install import (
    GIT_PINS, TARGET, baseline_source, git_blob_sha,
    patch_source, replacement_source,
)


def test_baseline_matches_reviewed_github_blob() -> None:
    assert git_blob_sha(baseline_source().encode("utf-8")) == GIT_PINS[TARGET]


def test_whole_function_replacement_is_idempotent() -> None:
    expected = replacement_source()
    assert patch_source(baseline_source()) == expected
    assert patch_source(expected) == expected
    ast.parse(expected)


def test_top_level_imports_and_function_signature_unchanged() -> None:
    old, new = ast.parse(baseline_source()), ast.parse(replacement_source())
    assert [ast.dump(item) for item in old.body[:4]] == [
        ast.dump(item) for item in new.body[:4]
    ]
    old_functions = [item for item in old.body if isinstance(item, ast.FunctionDef)]
    new_functions = [item for item in new.body if isinstance(item, ast.FunctionDef)]
    assert len(old_functions) == len(new_functions) == 1
    assert ast.dump(old_functions[0].args) == ast.dump(new_functions[0].args)
    assert new_functions[0].name == "build_context_expansion_provider_registry"


def test_unreviewed_changes_rejected() -> None:
    with pytest.raises(ValueError):
        patch_source(baseline_source().replace("context statements must be tuples", "changed"))
```

### `tests/test_context.py`

```python
"""Historical four-provider contract and conditional R35 registration."""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r6_2_unified_registry_r3_r4.context_provider_registry import (
    build_context_expansion_provider_registry,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def _noop(goal: object, available: tuple[object, ...]) -> tuple:
    return ()


def _registry(available: tuple[object, ...]):
    return build_context_expansion_provider_registry(
        available=available, prior_conclusions=(),
        expand_registered_toda45_finite_cyclic_goal=_noop,
        expand_registered_eta_specialization=_noop,
        expand_registered_delta_image_goal=_noop,
        expand_cited_general_specialization=_noop,
    )


def _typed_witnesses():
    delta = TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))
    iota = HomotopyElement("iota_11", 11, 11, 11, GeneratorSymbol("ι", 11))
    nu = HomotopyElement("nu5", 5, 8, 5, GeneratorSymbol("ν", 5))
    eta = HomotopyElement("eta8", 8, 9, 8, GeneratorSymbol("η", 8))
    generator = Composition(nu, eta)
    group = Relation(delta.target_group, FiniteCyclicGroup(2, generator), RelationType.EQUALITY)
    image = TodaDeltaImageUpToSignStatement(delta, iota, generator)
    return group, image


def test_original_four_context_providers_unchanged_without_cited_witness() -> None:
    registry = _registry(("non-cited",))
    assert len(registry.entries()) == 4
    assert all(entry.origin == "SHARED_CITED_CONTEXT" for entry in registry.entries())


def test_one_missing_source_does_not_register_extra_provider() -> None:
    group, image = _typed_witnesses()
    assert len(_registry((group,)).entries()) == 4
    assert len(_registry((image,)).entries()) == 4


def test_mismatched_generator_rejects_registration() -> None:
    group, image = _typed_witnesses()
    wrong = TodaDeltaImageUpToSignStatement(image.map, image.element, image.element)
    assert len(_registry((group, wrong)).entries()) == 4


def test_real_cited_shape_adds_only_one_provider_in_original_order() -> None:
    group, image = _typed_witnesses()
    registry = _registry((group, image))
    entries = registry.entries()
    assert len(entries) == 5
    assert entries[-1].provider_id == (
        "phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule.expand_cyclic_delta_kernel"
    )
    assert [entry.provider_id.split(".")[-1] for entry in entries[:4]] == [
        "expand_registered_toda45_finite_cyclic_goal",
        "expand_registered_eta_specialization",
        "expand_registered_delta_image_goal",
        "expand_cited_general_specialization",
    ]
    assert all(entry.origin == "SHARED_CITED_CONTEXT" for entry in entries)


def test_extra_provider_returns_no_proof_for_unrelated_goal() -> None:
    group, image = _typed_witnesses()
    extra = _registry((group, image)).providers()[-1]
    assert extra("not a typed kernel goal") == ()
```

### `tests/test_public.py`

```python
"""Public source-first R36 connection and exact verified ancestry checks."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME
from phase174_r3_r7_r36_cited_kernel_provider_wiring.audit import audit_public_connection
from proof import ProofRule


def test_shared_provider_offers_real_cited_kernel_expansion() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    group, image = checked_prior_statements()
    goal = KernelMultipleStatement(image.map, image.map.source_group, image.element, 2)
    proposals = shared_expansion_provider(bridge, proof_target=root)(goal)
    matches = tuple(item for item in proposals if item.rule.name == RULE_NAME)
    assert matches
    assert matches[0].subgoals[1:] == (group, image)


def test_cited_diagonal_and_real_priors_form_inference_only() -> None:
    outcome = audit_public_connection()
    assert outcome["diagonal_source_inferred"] is True
    assert outcome["three_real_cited_premises_form_inference"] is True
    assert outcome["kernel_inference_in_audit"] is True
    assert outcome["kernel_inference_inserted_as_given"] is False
    assert outcome["root_complete"] is False


def test_source_bridge_has_no_direct_kernel_or_root_given() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    _, image = checked_prior_statements()
    matches = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and (link.step.conclusion == root
             or (type(link.step.conclusion) is KernelMultipleStatement
                 and link.step.conclusion.map == image.map))
    )
    assert matches == ()
```

### `__init__.py`

```python
"""Phase 174 R3-R7-R36: cited R35 kernel provider public connection."""
```
