from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


README_MARKER_START = "<!-- PHASE155_CLOSURE_START -->"
README_MARKER_END = "<!-- PHASE155_CLOSURE_END -->"

DOC_MARKER_START = "<!-- PHASE155_CLOSURE_START -->"
DOC_MARKER_END = "<!-- PHASE155_CLOSURE_END -->"


README_SECTION = r"""
<!-- PHASE155_CLOSURE_START -->
## Phase 155 test-suite consolidation

Phase 155 consolidated the test suite without changing production mathematics.

The phase established explicit execution lanes:

```text
canonical_routine
historical_compatibility
audit_only
performance_heavy_integration
residual_retained
```

The final Phase 155 classification before the closure regression is:

```text
canonical_routine: 9069
historical_compatibility: 65
audit_only: 293
performance_heavy_integration: 31
residual_retained: 664
nonroutine total: 1053
```

Phase 155 also removed verified duplicate / superseded test debt, repaired stale
expectations, and separated performance-heavy integration checks from the
routine feedback loop.

The standing test policy is:

- new tests should be lightweight by default,
- prefer local unit / contract tests and representative cases,
- do not add all-group, repository-wide, huge snapshot, or deep recursive scans
  to the routine canonical lane,
- heavy integration or audit tests must be explicitly separated when created,
- long-running audit tools must show progress and support checkpoint / resume,
- repository-wide pytest is reserved for phase closure.

The Phase 155 R6 runtime audit confirmed that the heavy lane contains materially
slower tests, including a representative cross-group Narrative audit that took
about 26.6 seconds and a representative cross-group Reference normalization
test that took about 7.5 seconds.

The repository-wide Phase 155 closure regression result is recorded in
`docs/development_log.md` and `docs/proof_records.md`.

Phase 156 is reserved for Reference statement relevance / minimal display.
In particular, group-result and other Reference statements should be displayed
only when they are actually needed by the proof.
<!-- PHASE155_CLOSURE_END -->
""".strip()


DESIGN_SECTION = r"""
<!-- PHASE155_CLOSURE_START -->
# Phase 155：test-suite consolidation 設計境界

Phase 155 は production mathematics、`ProofStep`、proof graph、Narrative の数学的意味を変更せず、
test suite の実行境界を整理した。

## execution lane

```text
canonical_routine
historical_compatibility
audit_only
performance_heavy_integration
residual_retained
```

`canonical_routine` は通常の開発フィードバック用である。

`historical_compatibility` は過去互換確認時のみ、`audit_only` はその監査目的が必要な場合のみ、
`performance_heavy_integration` は通常の focused / canonical loop から外して実行する。

`residual_retained` は削除候補を意味しない。
current contract との直接 ownership がまだ routine lane として確定していない test を保持する境界である。

## test design policy

今後の test は lightweight を原則とする。

```text
small unit / local contract / representative case
→ routine candidate

all-group / cross-group / population scan
→ audit / heavy lane

repository-wide pytest
→ Phase closure only
```

重い audit / integration runner は、

```text
visible progress
+
checkpoint
+
resume
```

を持つ。

## Phase 155 final boundary

R5 classification:

```text
canonical_routine: 9069
historical_compatibility: 65
audit_only: 293
performance_heavy_integration: 31
residual_retained: 664
nonroutine total: 1053
```

R6 では 21 collection batch がすべて成功し、12 bounded runtime probe も最終的に PASS した。

Phase 155 Closure の repository-wide full pytest は Phase 最後の1回として実行する。
その結果は `docs/development_log.md` と `docs/proof_records.md` に記録する。

## Phase 156 との境界

Phase 155 は Reference の表示内容を新たに最小化しない。

Phase 156 では、

```text
Reference statement relevance
Reference statement minimal display
```

を扱う。

特に群の結果を含む Reference statement は、実際の proof で必要なものだけを表示する一般規則を対象とする。
<!-- PHASE155_CLOSURE_END -->
""".strip()


ROADMAP_SECTION = r"""
<!-- PHASE155_CLOSURE_START -->
# Phase 155：Test Suite Consolidation — COMPLETE

Phase 155 では test suite の整理、重複削減、stale expectation 修正、実行 lane 分離、
collection / runtime audit を完了した。

完了項目:

```text
R1 inventory / classification
R2 stale expectation audit / repair
R3 duplicate / superseded cleanup
R4 canonical regression boundary
R5 heavy / historical boundary
R6 pytest collection / runtime audit
Closure repository-wide full pytest
```

最終 execution lane:

```text
canonical_routine: 9069
historical_compatibility: 65
audit_only: 293
performance_heavy_integration: 31
residual_retained: 664
nonroutine total: 1053
```

standing policy:

```text
new tests are lightweight by default
heavy tests do not enter routine canonical regression
long-running audits show progress
long-running audits support checkpoint / resume
repository-wide pytest is Phase-closure only
```

# Phase 156：Reference statement relevance / minimal display

次 Phase は Reference statement の relevance（関連性）と minimal display（必要最小限表示）を扱う。

主対象:

```text
group-result Reference statements
theorem / lemma Reference statements
used-vs-visible Reference relation
Reference statement granularity
```

目的:

```text
proof で実際に必要な Reference
→ 表示

proof で使用しない Reference
→ 表示しない
```

既存 proof provenance、Reference selection の一般規則、Phase 153 の自己参照除外・使用参照選択を維持し、
特定群専用の Reference list を hard-code しない。

Phase 156 では test-suite consolidation の追加機能を先取りしない。
<!-- PHASE155_CLOSURE_END -->
""".strip()


DEVLOG_SECTION_TEMPLATE = r"""
<!-- PHASE155_CLOSURE_START -->
# Phase 155：Test Suite Consolidation

Phase 155 は test suite の規模・重複・historical expectation・重い integration test の混在を整理した。

## R1 inventory / classification

開始時 inventory:

```text
test files: 843
source test functions: 10292
phase-numbered test files: 820
```

current contract / historical compatibility / audit-only / superseded snapshot /
duplicate coverage / performance-heavy integration の分類を開始した。

## R2 stale expectation audit / repair

high-confidence stale expectation を監査し、production behavior を戻さず test expectation 側を current contract に合わせた。

最終 focused:

```text
61 passed
stale: 0
```

## R3 duplicate / superseded cleanup

exact / superseded candidate を proof 付きで整理し、safe deletion のみ実施した。

最終結果:

```text
safe test IDs removed: 161
whole test files deleted: 5
duplicate test names: 0
unresolved nonhistorical removable pairs: 0
R3 closure: True
```

production code は変更していない。

## R4 canonical regression boundary

current public surface と internal production ownership を使って routine canonical boundary を確立した。

最終:

```text
canonical source test IDs: 9069
canonical files: 768
residual validation lane: 750
R4 canonical boundary validated: True
```

## R5 heavy / historical boundary

R4 の residual を追加監査し、routine / nonroutine の execution lane を確定した。

```text
canonical_routine: 9069
historical_compatibility: 65
audit_only: 293
performance_heavy_integration: 31
residual_retained: 664
nonroutine total: 1053
R5 boundary validated: True
```

test 本体は R5 では実行していない。

## R6 pytest collection / runtime audit

21 batch の collection を checkpoint 付きで実行した。

```text
collection batches: 21
collection failed batches: 0
runtime probes: 12
```

初回 bounded runtime probe では heavy lane の旧 expectation 2件が FAIL した。

修正:

```text
Phase144 old all-selected-rendered expectation
→ current Narrative-participating / DETACHED boundary に修正

Phase150 pi16_9 fixed Reference-name expectation
→ Reference numbering / normalization contract に限定
```

修正後:

```text
runtime 9: PASS 26.55s
runtime 10: PASS 7.51s
R6 audit validated: True
```

production code は変更していない。

## Test policy

Phase 155 以降:

```text
new tests are lightweight by default
small unit / local contract / representative test を優先
all-group / cross-group / population scan は routine canonical に入れない
heavy integration / audit test は作成時から分離
長時間 runner は progress を表示
長時間 runner は checkpoint / resume を持つ
repository-wide pytest は Phase 最後だけ
```

## Closure

repository-wide final regression:

```text
{FULL_RESULT}
```

Phase 155 完了。

次は Phase 156 `Reference statement relevance / minimal display`。
群結果などの Reference statement は proof で実際に必要なものだけを表示する一般規則を扱う。
<!-- PHASE155_CLOSURE_END -->
""".strip()


PROOF_SECTION_TEMPLATE = r"""
<!-- PHASE155_CLOSURE_START -->
# Phase 155 test-suite consolidation / provenance record

Phase 155 は数学的 proof provenance を変更した Phase ではない。

対象は test infrastructure であり、production の

```text
ProofStep
ProofStep.premises
ProofStep.inference_rule
proof repository
Narrative mathematical semantics
Toda theorem facts
```

は Phase 155 の整理対象ではない。

## stale expectation repair boundary

Phase 155 では production behavior を過去 snapshot に戻さず、current contract と矛盾する test expectation を修正した。

特に R6 で確認した2件:

```text
old Phase144:
all selected contributions must be rendered

current:
Narrative-participating contributions are connected
DETACHED contributions may remain outside Narrative
```

および:

```text
old Phase150:
pi16_9 test freezes a specific visible Reference list

current:
old normalization test guards Reference numbering / normalization
exact Reference relevance is deferred to Phase 156
```

したがって:

```text
test expectation repair
!= proof fact change

heavy-lane separation
!= provenance deletion

test deletion after redundancy proof
!= theorem deletion
```

## execution-lane provenance boundary

最終分類:

```text
canonical_routine: 9069
historical_compatibility: 65
audit_only: 293
performance_heavy_integration: 31
residual_retained: 664
nonroutine total: 1053
```

これは test execution policy の分類であり、数学的 theorem importance の ranking ではない。

## R6 measured evidence

```text
21 collection batches
0 failed collection batches
12 bounded runtime probes
all PASS after stale-expectation repair
```

heavy lane representative:

```text
Phase144 cross-group Narrative audit: 26.55s
Phase150 cross-group Reference normalization: 7.51s
```

この実測により、heavy integration test を routine loop から分離する方針を確認した。

## final verification record

repository-wide Phase 155 closure:

```text
{FULL_RESULT}
```

この full regression を Phase 155 の最終 test provenance とする。

## next-phase boundary

Phase 156 は Reference statement relevance / minimal display を扱う。

```text
Phase 155:
test execution / maintenance boundary

Phase 156:
which Reference statements should be visible
```

Phase 155 Closure では Phase 156 の表示規則を実装しない。
<!-- PHASE155_CLOSURE_END -->
""".strip()


def _replace_or_append(
    text: str,
    section: str,
    start_marker: str,
    end_marker: str,
) -> str:
    pattern = re.compile(
        re.escape(start_marker)
        + r".*?"
        + re.escape(end_marker),
        re.DOTALL,
    )

    if pattern.search(text):
        updated = pattern.sub(
            section,
            text,
        )
    else:
        updated = (
            text.rstrip()
            + "\n\n"
            + section
            + "\n"
        )

    return updated


def _extract_full_result(
    log_text: str,
) -> str:
    lines = log_text.splitlines()

    summary_candidates = []

    for line in lines:
        lowered = line.lower()

        if (
            " passed" in lowered
            or " failed" in lowered
            or " error" in lowered
        ):
            if (
                " in "
                in lowered
                and (
                    "=" in line
                    or "passed"
                    in lowered
                )
            ):
                summary_candidates.append(
                    line.strip()
                )

    if not summary_candidates:
        return (
            "pytest exit code 0; "
            "summary line not detected"
        )

    return summary_candidates[-1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_closure_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )

    metadata_path = (
        output_dir
        / "phase155_full_pytest_metadata.json"
    )
    log_path = (
        output_dir
        / "phase155_full_pytest.log"
    )

    if not metadata_path.exists():
        raise SystemExit(
            "full pytest metadata not found"
        )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    if metadata.get(
        "returncode"
    ) != 0:
        raise SystemExit(
            "full pytest did not pass; "
            "documentation will not be updated"
        )

    log_text = log_path.read_text(
        encoding="utf-8"
    )

    full_result = _extract_full_result(
        log_text
    )

    targets = {
        "README.md": README_SECTION,
        "docs/design.md": DESIGN_SECTION,
        "docs/roadmap.md": ROADMAP_SECTION,
        "docs/development_log.md": (
            DEVLOG_SECTION_TEMPLATE.format(
                FULL_RESULT=full_result
            )
        ),
        "docs/proof_records.md": (
            PROOF_SECTION_TEMPLATE.format(
                FULL_RESULT=full_result
            )
        ),
    }

    print(
        "Updating Phase 155 closure documents"
    )

    for relative_path, section in targets.items():
        path = (
            repo_root
            / relative_path
        )

        current = path.read_text(
            encoding="utf-8-sig"
        )

        updated = _replace_or_append(
            current,
            section,
            DOC_MARKER_START,
            DOC_MARKER_END,
        )

        path.write_text(
            updated,
            encoding="utf-8",
        )

        print(
            " updated:",
            relative_path,
        )

    full_documents = (
        output_dir
        / "full_documents"
    )
    full_documents.mkdir(
        parents=True,
        exist_ok=True,
    )

    for relative_path in targets:
        source = (
            repo_root
            / relative_path
        )
        destination = (
            full_documents
            / relative_path
        )
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            source,
            destination,
        )

    summary = [
        "# Phase 155 Closure",
        "",
        "Production changes: none.",
        "Phase 156 functionality: not implemented.",
        "",
        "Final regression:",
        "",
        "```text",
        full_result,
        "```",
        "",
        "R1–R6: COMPLETE",
        "Phase 155: COMPLETE",
        "",
        "Updated full documents are stored under:",
        "`phase155_closure_output/full_documents/`",
    ]

    (
        output_dir
        / "phase155_closure_summary.md"
    ).write_text(
        "\n".join(
            summary
        )
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155 documentation closure completed."
    )
    print(
        "Full result:",
        full_result,
    )
    print(
        "Full documents:",
        full_documents,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
