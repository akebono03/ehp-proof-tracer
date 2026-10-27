"""Guarded minimal production patch with complete replacement-function outputs."""
from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"


# No module-level imports change: all additions are local in the full functions.
# Every old anchor has to match EXACTLY once, or the entire patch aborts.
REPLACEMENTS = {
    "phase165_r52_r9_shared_math.py": (
        (
            '''    context_id = citing_assertion_id or assertions[0].assertion_id
    proof_context = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=context_id,
        verified_assertion_ids=verified_assertion_ids,
        explicit_publication_target=citing_assertion_id is not None,
    )''',
            '''    context_id = citing_assertion_id or assertions[0].assertion_id
    if citing_assertion_id is None:
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        proof_context = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
    else:
        proof_context = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=verified_assertion_ids,
            explicit_publication_target=True,
        )''',
        ),
    ),
    "phase168_r3_5_model_renderer.py": (
        (
            '        if locator == "Chapter V, i)":\n            locator = "η 系列の定義（Chapter V, i）"',
            '        # Display the cited locator verbatim; no series-specific alias.',
        ),
    ),
    "phase165_r55_nk_only_goal.py": (
        (
            '''        from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
        from phase165_r52_r2_search_adapter import search_registered_partial_proof''',
            '''        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        from phase165_r52_r2_search_adapter import search_registered_partial_proof''',
        ),
        (
            '''        # DB goals have no publication assertion. Preserve the existing
        # implicit-target citation policy without inventing a citing ID.''',
            '''        # The DB target has no publication position. Cite only independently
        # positioned fixed source statements; invent no target citation ID.''',
        ),
        (
            '''        screened = screen_shared_proof_context(
            bridge, goal=candidate, citing_assertion_id=context_id,
        )''',
            '''        screened = screen_independent_sources_for_derived_goal(
            bridge, goal=candidate,
        )''',
        ),
    ),
    "web_group_proof.py": (
        (
            '''    if citing_id is None:
      raise UnverifiedProofTree("complete proof has no positioned citing assertion")
    # Unsupported origins and invalid inferences are rejected by the existing
    # single proof-tree checker; do not silently skip its invocation here.
    verify_proof_tree_for_narrative(
      result, model_bridge, citing_assertion_id=citing_id,
    )''',
            '''    # A DB goal need not have a publication assertion. For this derived-only
    # route, require an actual typed group target before invoking the gate.
    # Synthetic/untyped completed results retain the previous fail-closed path.
    if citing_id is None:
      from homotopy_groups import TodaPrimaryGroupZeroStatement
      from proof import Relation, RelationType
      valid_derived_group = (
        isinstance(result.conclusion, Relation)
        and result.conclusion.relation_type is RelationType.EQUALITY
        and result.conclusion.lhs == result.target
      ) or (
        isinstance(result.conclusion, TodaPrimaryGroupZeroStatement)
        and result.conclusion.group == result.target
      )
      if not valid_derived_group:
        raise UnverifiedProofTree("complete unpositioned proof lacks a typed group target")
    # Keep the existing positioned-Goal call signature byte-for-byte.
    # The new keyword is passed only to genuinely unpositioned targets.
    if citing_id is None:
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=None,
        derived_target_without_citing_id=True,
      )
    else:
      verify_proof_tree_for_narrative(
        result, model_bridge, citing_assertion_id=citing_id,
      )''',
        ),
    ),
    "phase168_r3_41p13_trust_boundary/verification.py": (
        (
            '''    citing_assertion_id: str,
) -> tuple[int, int]:''',
            '''    citing_assertion_id: str | None,
    derived_target_without_citing_id: bool = False,
) -> tuple[int, int]:''',
        ),
        (
            '''    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise ValueError("citing_assertion_id must identify a positioned goal")
    bridge.registry.assertion(citing_assertion_id)''',
            '''    if derived_target_without_citing_id:
        if citing_assertion_id is not None:
            raise ValueError("derived-target mode requires no citing assertion")
        if result.status is not ProofSearchStatus.COMPLETE:
            raise ValueError("derived-target mode requires a completed proof")
        if not any(
            step.rule is ProofRule.INFERENCE
            and step.conclusion == result.conclusion
            for step in result.proven_steps
        ):
            raise UnverifiedProofTree("an uncited goal must be independently inferred")
    else:
        if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
            raise ValueError("citing_assertion_id must identify a positioned goal")
        bridge.registry.assertion(citing_assertion_id)''',
        ),
        (
            '''                            and precedes_citing_assertion(
                                bridge, link.assertion_id, citing_assertion_id
                            )):''',
            '''                            and (
                                (
                                    derived_target_without_citing_id
                                    and bridge.registry.reference(
                                        assertion.reference_id
                                    ).publication_position is not None
                                    and assertion.content != result.conclusion
                                    and not _same_group_as_derived_target(
                                        assertion.content, result.conclusion
                                    )
                                )
                                or (
                                    not derived_target_without_citing_id
                                    and precedes_citing_assertion(
                                        bridge, link.assertion_id,
                                        citing_assertion_id,
                                    )
                                )
                            )):''',
        ),
        (
            '''    checked: set[int] = set()''',
            '''    def _same_group_as_derived_target(source: object, target: object) -> bool:
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from proof import Relation
        source_group = (
            source.group if isinstance(source, TodaPrimaryGroupZeroStatement)
            else source.lhs if isinstance(source, Relation) else None
        )
        target_group = (
            target.group if isinstance(target, TodaPrimaryGroupZeroStatement)
            else target.lhs if isinstance(target, Relation) else None
        )
        return source_group is not None and source_group == target_group

    checked: set[int] = set()''',
        ),
    ),
}


FUNCTIONS = {
    "phase165_r52_r9_shared_math.py": ("search_shared_group_goal",),
    "phase165_r55_nk_only_goal.py": ("search_group_from_registered_goal",),
    "web_group_proof.py": ("build_standard_web_group_proof_view",),
    "phase168_r3_5_model_renderer.py": (
        "render_model_backed_narrative_markdown",
    ),
    "phase168_r3_41p13_trust_boundary/verification.py": (
        "verify_proof_tree_for_narrative",
    ),
    "phase169_r10e1_general_group_transport/transport.py": (
        "expand_prior_general_group_transport",
    ),
}


def _full_function(source: str, function_name: str) -> str:
    tree = ast.parse(source)
    matches = tuple(
        node for node in tree.body if isinstance(node, ast.FunctionDef)
        and node.name == function_name
    )
    if len(matches) != 1:
        raise RuntimeError("expected one full function: " + function_name)
    node = matches[0]
    return "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def transform(name: str, raw: bytes) -> tuple[bytes, dict[str, str]]:
    crlf = b"\r\n" in raw
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    original = source
    if name == "phase169_r10e1_general_group_transport/transport.py":
        new_function = (HERE / "expand_prior_general_group_transport_FULL.py").read_text(
            encoding="utf-8",
        )
        old_function = _full_function(source, "expand_prior_general_group_transport")
        source = source.replace(old_function, new_function, 1)
    else:
        for old, new in REPLACEMENTS[name]:
            if source.count(old) != 1 or new in source:
                raise RuntimeError("R10E2 source anchor mismatched: " + name)
            source = source.replace(old, new, 1)
    if source == original:
        raise RuntimeError("R10E2 expected changed source: " + name)
    ast.parse(source)
    extracted = {fn: _full_function(source, fn) for fn in FUNCTIONS[name]}
    serialized = source.encode("utf-8")
    if crlf:
        serialized = serialized.replace(b"\n", b"\r\n")
    return serialized, extracted


def main() -> None:
    import sys
    OUTPUT.mkdir(parents=True, exist_ok=True)
    changed = []
    files = list(FUNCTIONS)
    for name in files:
        p = ROOT / name
        if not p.is_file():
            raise RuntimeError("R10E2 required production module missing: " + name)
        original = p.read_bytes()
        new_content, full = transform(name, original)
        changed.append((p, name, original, new_content, full))
    # All files validated before any write.
    for path, name, original, new_content, full in changed:
        destination = OUTPUT / (name.replace("/", "__") + ".before")
        destination.write_bytes(original)
        (OUTPUT / (name.replace("/", "__") + ".FULL")).write_bytes(new_content)
        for fn, code in full.items():
            f = OUTPUT / (fn + "_FULL.py")
            f.write_text(code, encoding="utf-8")
            print("R10E2R1_FULL_FUNCTION=" + str(f))
    try:
        for path, name, original, new_content, full in changed:
            temp = path.with_name(path.name + ".r10e2-tmp")
            temp.write_bytes(new_content)
            os.replace(temp, path)
            print("R10E2R1_PATCHED=" + str(path))
    except Exception:
        for path, name, original, new_content, full in changed:
            path.write_bytes(original)
        raise
    print("R10E2R1_PATCH_COUNT=" + str(len(changed)))


if __name__ == "__main__":
    main()
