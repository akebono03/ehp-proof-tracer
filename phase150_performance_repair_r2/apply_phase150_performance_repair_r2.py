from __future__ import annotations

from pathlib import Path


TARGETS = {
    "tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py": (
        ("_context", "_uncached_context", "maxsize=None"),
        ("_render_pair", "_uncached_render_pair", "maxsize=None"),
    ),
    "tests/test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py": (
        ("build_parity_audit", "_uncached_build_parity_audit", "maxsize=1"),
    ),
    "tests/test_phase144_6_r5_21_missing_7_facts_generic_provider_audit.py": (
        ("build_missing_fact_traces", "_uncached_build_missing_fact_traces", "maxsize=1"),
    ),
    "tests/test_phase144_6_r5_22_missing_4_facts_statement_structure_audit.py": (
        ("build_statement_structure_traces", "_uncached_build_statement_structure_traces", "maxsize=1"),
    ),
    "tests/test_phase144_6_r5_23_missing_7_facts_generic_visibility_path_audit.py": (
        ("build_visibility_path_traces", "_uncached_build_visibility_path_traces", "maxsize=1"),
    ),
    "tests/test_phase144_6_r5_24_generic_visibility_policy_correction_design_audit.py": (
        ("build_group_protection_impacts", "_uncached_build_group_protection_impacts", "maxsize=1"),
        ("build_visible_fact_body_traces", "_uncached_build_visible_fact_body_traces", "maxsize=1"),
    ),
    "tests/test_phase144_6_r5_25_multi_argument_suppression_selective_frontier_relevance_audit.py": (
        ("build_multi_suppression_traces", "_uncached_build_multi_suppression_traces", "maxsize=1"),
        ("build_frontier_candidate_signatures", "_uncached_build_frontier_candidate_signatures", "maxsize=1"),
    ),
}


def ensure_lru_cache_import(text: str) -> str:
    line = "from functools import lru_cache\n"
    if line in text:
        return text
    if text.startswith("import "):
        first_break = text.find("\n")
        return text[: first_break + 1] + line + text[first_break + 1 :]
    return line + text


def insert_wrapper_after_import_block(
    text: str,
    public_name: str,
    uncached_name: str,
    decorator_args: str,
) -> str:
    marker = f"{uncached_name} = {public_name}\n"
    if marker in text:
        return text

    # Put wrappers immediately before the first top-level function/class/decorator.
    candidates = []
    for token in ("\ndef ", "\nclass ", "\n@pytest.", "\n@"):
        pos = text.find(token)
        if pos >= 0:
            candidates.append(pos + 1)
    if not candidates:
        raise RuntimeError(f"Could not locate insertion point for {public_name}")

    insert_at = min(candidates)
    wrapper = (
        f"{uncached_name} = {public_name}\n\n"
        f"@lru_cache({decorator_args})\n"
        f"def {public_name}(*args, **kwargs):\n"
        f"  return {uncached_name}(*args, **kwargs)\n\n\n"
    )
    return text[:insert_at] + wrapper + text[insert_at:]


def patch_r5_19(text: str) -> str:
    text = ensure_lru_cache_import(text)

    # _context is imported; cache it before any test/helper uses it.
    if "_uncached_context = _context\n" not in text:
        insertion = text.find("\ndef _render_pair")
        if insertion < 0:
            raise RuntimeError("R5-19: _render_pair not found")
        wrapper = (
            "\n_uncached_context = _context\n\n"
            "@lru_cache(maxsize=None)\n"
            "def _context(n, k):\n"
            "  return _uncached_context(n, k)\n"
        )
        text = text[:insertion] + wrapper + text[insertion:]

    # Cache the complete rendered pair too. Rename the existing complete helper,
    # then add a same-signature cached wrapper after its body.
    if "_uncached_render_pair" not in text:
        old = "def _render_pair(n, k):\n"
        if old not in text:
            raise RuntimeError("R5-19: original _render_pair definition not found")
        text = text.replace(old, "def _uncached_render_pair(n, k):\n", 1)

        next_test = text.find("\ndef test_phase144_6_r5_19_")
        if next_test < 0:
            raise RuntimeError("R5-19: first test function not found")
        wrapper = (
            "\n@lru_cache(maxsize=None)\n"
            "def _render_pair(n, k):\n"
            "  return _uncached_render_pair(n, k)\n"
        )
        text = text[:next_test] + wrapper + text[next_test:]

    return text


def patch_builder_file(text: str, wrappers) -> str:
    text = ensure_lru_cache_import(text)
    # Insert all wrappers after imports but before the first test.
    first_test = text.find("\ndef test_")
    if first_test < 0:
        raise RuntimeError("First test function not found")

    blocks = []
    for public_name, uncached_name, decorator_args in wrappers:
        if f"{uncached_name} = {public_name}\n" in text:
            continue
        blocks.append(
            f"{uncached_name} = {public_name}\n\n"
            f"@lru_cache({decorator_args})\n"
            f"def {public_name}():\n"
            f"  return {uncached_name}()\n"
        )

    if blocks:
        text = text[:first_test] + "\n" + "\n\n".join(blocks) + "\n" + text[first_test:]
    return text


def main() -> int:
    repo = Path.cwd()
    changed = []

    for relative, wrappers in TARGETS.items():
        path = repo / relative
        if not path.exists():
            raise FileNotFoundError(path)

        original = path.read_text(encoding="utf-8-sig")
        if relative.endswith("r5_19_proof_chain_narrative_integration.py"):
            updated = patch_r5_19(original)
        else:
            updated = patch_builder_file(original, wrappers)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(relative)

    print("Phase 150 Performance Repair R2 applied.")
    print("Production changes: none.")
    print("Audit builder changes: none.")
    print("Mathematical assertions changed: none.")
    print("Changed test files:")
    for relative in changed:
        print(f"  - {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
