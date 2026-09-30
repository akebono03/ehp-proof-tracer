from __future__ import annotations

import importlib.util
import inspect
from collections import defaultdict
from pathlib import Path

ROOT = Path.cwd()
TEST_FILE = ROOT / "tests" / "test_phase150_rc4_5_visible_reasons.py"


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _positions(text: str, needle: str):
    positions = []
    start = 0
    while True:
        index = text.find(needle, start)
        if index < 0:
            return tuple(positions)
        positions.append(index)
        start = index + max(1, len(needle))


def _line_number(text: str, index: int):
    return text.count("\n", 0, index) + 1


def _safe_value(value):
    if isinstance(value, (str, int, float, bool, type(None))):
        return repr(value)
    if isinstance(value, tuple):
        return f"tuple(len={len(value)})"
    if isinstance(value, list):
        return f"list(len={len(value)})"
    if isinstance(value, dict):
        return f"dict(len={len(value)})"
    return type(value).__name__


def _reason_details(reason):
    result = [f"type={type(reason).__name__}"]
    if hasattr(reason, "__dict__"):
        for key, value in vars(reason).items():
            result.append(f"{key}={_safe_value(value)}")
    return ", ".join(result)


def _print_nearby_lines(rendered: str, sentence: str):
    lines = rendered.splitlines()
    sentence_first_line = sentence.splitlines()[0]
    hits = [
        index
        for index, line in enumerate(lines)
        if sentence_first_line in line
    ]
    for hit in hits:
        lo = max(0, hit - 2)
        hi = min(len(lines), hit + max(3, len(sentence.splitlines()) + 2))
        print(f"    CONTEXT lines {lo + 1}-{hi}:")
        for index in range(lo, hi):
            marker = ">>" if index == hit else "  "
            print(f"    {marker} {index + 1:04d}: {lines[index]}")


def _inspect_object(label, obj):
    print(f"  {label}: type={type(obj).__name__}")
    if hasattr(obj, "__dict__"):
        for key, value in vars(obj).items():
            print(f"    {key}: {_safe_value(value)}")


def main():
    print("=" * 80)
    print("Phase 150 RC4-5 Visible Reason Multiplicity Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print("Documentation changes: none")
    print("Full regression: NOT run")
    print("=" * 80)

    if not TEST_FILE.exists():
        raise SystemExit(f"Missing test file: {TEST_FILE}")

    module = _load_module(TEST_FILE)
    print()
    print("A. Current local RC4-5 source")
    print("-" * 80)
    print(inspect.getsource(module._render_case).rstrip())
    print()
    print(inspect.getsource(
        module.test_phase150_rc4_5_visible_reason_count_matches_typed_reason_count
    ).rstrip())

    print()
    print("B. Per-target typed reason -> sentence -> multiplicity")
    print("-" * 80)

    for label, n, k in module.CASES:
        (
            presentation,
            semantic_sidecar,
            reason_sidecar,
            rendered,
        ) = module._render_case(n, k)

        print()
        print("=" * 80)
        print(f"TARGET {label} n={n} k={k}")
        print(f"rendered_chars={len(rendered)}")
        print(f"typed_reasons={len(reason_sidecar.reasons)}")
        _inspect_object("presentation", presentation)
        _inspect_object("semantic_sidecar", semantic_sidecar)
        _inspect_object("reason_sidecar", reason_sidecar)

        grouped = defaultdict(list)
        none_reasons = []
        for index, reason in enumerate(reason_sidecar.reasons, start=1):
            sentence = module.render_toda_group_proof_narrative_reason_sentence(reason)
            if sentence is None:
                none_reasons.append((index, reason))
                continue
            grouped[sentence].append((index, reason))

        print(f"renderable_reason_instances={sum(len(v) for v in grouped.values())}")
        print(f"distinct_reason_sentences={len(grouped)}")
        print(f"none_reason_instances={len(none_reasons)}")

        if none_reasons:
            print("  NON-RENDERED TYPED REASONS")
            for index, reason in none_reasons:
                print(f"    reason[{index}]: {_reason_details(reason)}")

        for sentence_index, (sentence, reasons) in enumerate(grouped.items(), start=1):
            positions = _positions(rendered, sentence)
            print()
            print(f"  SENTENCE {sentence_index}")
            print(f"    typed_reason_instances={len(reasons)}")
            print(f"    rendered_occurrences={len(positions)}")
            print(f"    rendered_positions={positions}")
            print(
                "    rendered_lines="
                + repr(tuple(_line_number(rendered, pos) for pos in positions))
            )
            print(f"    sentence={sentence!r}")
            for reason_index, reason in reasons:
                print(
                    f"    reason[{reason_index}]: "
                    f"{_reason_details(reason)}"
                )
            _print_nearby_lines(rendered, sentence)

        duplicate_typed = sum(
            max(0, len(reasons) - 1)
            for reasons in grouped.values()
        )
        duplicate_rendered = sum(
            max(0, len(_positions(rendered, sentence)) - 1)
            for sentence in grouped
        )
        print()
        print("  SUMMARY")
        print(f"    duplicate_typed_instances={duplicate_typed}")
        print(f"    duplicate_rendered_occurrences={duplicate_rendered}")
        print(
            "    sentence_multiplicities="
            + repr(
                tuple(
                    (
                        len(reasons),
                        len(_positions(rendered, sentence)),
                    )
                    for sentence, reasons in grouped.items()
                )
            )
        )

    print()
    print("C. Classification guide")
    print("-" * 80)
    print(
        "typed>1 and rendered=1: multiple typed reasons intentionally collapse to one prose sentence."
    )
    print(
        "typed=1 and rendered>1: one typed reason sentence is emitted by more than one narrative path."
    )
    print(
        "typed>1 and rendered>1: both semantic duplication and prose-path duplication are present."
    )
    print(
        "typed=rendered>1: one-to-one multiplicity may be intentional, but ownership/context must be inspected."
    )
    print()
    print("Audit complete. No files in the repository were modified.")


if __name__ == "__main__":
    main()
