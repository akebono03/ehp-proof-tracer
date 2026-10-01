from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
  "README.md": (
    "## Phase 154 proof-prose generation refinement",
    "44 passed",
    "57 passed",
    "violations: 0",
    "final full regression remains",
  ),
  "docs/design.md": (
    "<!-- PHASE154_DOCUMENTATION_CLOSURE -->",
    "# Phase 154 設計完了記録",
    "transition_repetition: 0",
    "repository-wide final full regression はまだ実行していない",
  ),
  "docs/development_log.md": (
    "<!-- PHASE154_DOCUMENTATION_CLOSURE -->",
    "# Phase 154 — Proof prose generation refinement",
    "44 passed",
    "57 passed",
    "violations: 0",
  ),
  "docs/roadmap.md": (
    "## Phase 154 — Proof prose generation refinement",
    "Phase 154 の implementation / closure audit は完了",
    "### Phase 155 — Reference statement relevance / minimal display",
    "final full regression",
  ),
  "docs/proof_records.md": (
    "<!-- PHASE154_DOCUMENTATION_CLOSURE -->",
    "# Phase 154 Proof prose generation provenance record",
    "Reference-to-consumer connection",
    "repository-wide all-pass",
  ),
}


def main() -> int:
  failures = []

  for relative, fragments in EXPECTED.items():
    path = REPO_ROOT / relative
    text = path.read_text(
      encoding="utf-8",
    )

    for fragment in fragments:
      if fragment not in text:
        failures.append(
          (
            relative,
            fragment,
          )
        )

  roadmap = (
    REPO_ROOT
    / "docs/roadmap.md"
  ).read_text(
    encoding="utf-8",
  )

  if (
    "次 Phase は test-suite 整理ではなく、"
    "現在の Narrative 本文の不自然さを一般規則で改善する。"
    in roadmap
  ):
    failures.append(
      (
        "docs/roadmap.md",
        "stale Phase 154 planned wording remains",
      )
    )

  if failures:
    print(
      "FAIL"
    )
    for failure in failures:
      print(
        "  ",
        failure,
      )
    return 1

  print(
    "PASS: Phase 154 documentation closure content verified."
  )
  print(
    "Full regression status remains explicitly NOT RUN."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
