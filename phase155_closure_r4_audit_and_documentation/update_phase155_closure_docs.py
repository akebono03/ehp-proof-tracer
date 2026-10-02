from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


README_MARKER_START = "<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_START -->"
README_MARKER_END = "<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_END -->"

DESIGN_MARKER_START = "<!-- PHASE155_TEST_CONSOLIDATION_DESIGN_START -->"
DESIGN_MARKER_END = "<!-- PHASE155_TEST_CONSOLIDATION_DESIGN_END -->"

DEVELOPMENT_MARKER_START = "<!-- PHASE155_CLOSURE_START -->"
DEVELOPMENT_MARKER_END = "<!-- PHASE155_CLOSURE_END -->"

ROADMAP_MARKER_START = "<!-- PHASE155_CLOSURE_ROADMAP_START -->"
ROADMAP_MARKER_END = "<!-- PHASE155_CLOSURE_ROADMAP_END -->"

PROOF_MARKER_START = "<!-- PHASE155_TEST_PROVENANCE_START -->"
PROOF_MARKER_END = "<!-- PHASE155_TEST_PROVENANCE_END -->"


def _replace_marked_section(
  text: str,
  start_marker: str,
  end_marker: str,
  section: str,
) -> str:
  payload = (
    start_marker
    + "\n"
    + section.rstrip()
    + "\n"
    + end_marker
  )

  start = text.find(
    start_marker
  )

  if start < 0:
    return (
      text.rstrip()
      + "\n\n"
      + payload
      + "\n"
    )

  end = text.find(
    end_marker,
    start,
  )

  if end < 0:
    raise ValueError(
      "Found start marker without end marker: "
      + start_marker
    )

  end += len(
    end_marker
  )

  return (
    text[:start]
    + payload
    + text[end:]
  )


def _replace_between(
  text: str,
  start_heading: str,
  end_heading: str,
  replacement: str,
) -> str:
  start = text.find(
    start_heading
  )

  if start < 0:
    raise ValueError(
      "Start heading not found: "
      + start_heading
    )

  end = text.find(
    end_heading,
    start,
  )

  if end < 0:
    raise ValueError(
      "End heading not found: "
      + end_heading
    )

  return (
    text[:start]
    + replacement.rstrip()
    + "\n\n"
    + text[end:]
  )


def _audit_lines(
  audit_result: dict,
) -> str:
  lines = []

  for index in range(
    1,
    6,
  ):
    row = audit_result[
      "audits"
    ][
      str(
        index
      )
    ]
    lines.append(
      "audit "
      + str(
        index
      )
      + ": "
      + row[
        "status"
      ]
      + " ("
      + str(
        row[
          "elapsed_seconds"
        ]
      )
      + "s)"
    )

  return "\n".join(
    lines
  )


def _read(
  path: Path,
) -> str:
  return path.read_text(
    encoding="utf-8-sig"
  )


def _write(
  path: Path,
  text: str,
) -> None:
  path.write_text(
    text.rstrip()
    + "\n",
    encoding="utf-8",
  )


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
    required=True,
  )
  args = parser.parse_args()

  repo_root = args.repo_root.resolve()
  output_dir = args.output_dir.resolve()

  audit_result_path = (
    output_dir
    / "audit_result.json"
  )

  if not audit_result_path.exists():
    raise SystemExit(
      "Audit result not found: "
      + str(
        audit_result_path
      )
    )

  audit_result = json.loads(
    audit_result_path.read_text(
      encoding="utf-8"
    )
  )

  if not audit_result.get(
    "all_audit_only_pass"
  ):
    raise SystemExit(
      "Documentation update is blocked until all five audit-only tests PASS."
    )

  collected = int(
    audit_result[
      "current_collected_tests"
    ]
  )
  routine = int(
    audit_result[
      "routine_test_count"
    ]
  )
  audit_summary = _audit_lines(
    audit_result
  )

  readme_path = (
    repo_root
    / "README.md"
  )
  design_path = (
    repo_root
    / "docs"
    / "design.md"
  )
  development_path = (
    repo_root
    / "docs"
    / "development_log.md"
  )
  roadmap_path = (
    repo_root
    / "docs"
    / "roadmap.md"
  )
  proof_path = (
    repo_root
    / "docs"
    / "proof_records.md"
  )

  readme = _read(
    readme_path
  )
  design = _read(
    design_path
  )
  development = _read(
    development_path
  )
  roadmap = _read(
    roadmap_path
  )
  proof = _read(
    proof_path
  )

  test_hygiene = f"""## Test and backup hygiene

Phase 155 replaced the former monolithic-regression-first maintenance pattern with an explicit test boundary.

The current collection contains:

```text
{collected} tests total
{routine} routine tests
5 audit-only tests
```

Routine regression is executed in file-based shards with checkpoint/resume semantics. A shard that has already passed is not rerun after an unrelated repair. The working target is about five minutes per shard; a ten-minute shard is treated as a split/review boundary rather than as a normal unit of feedback.

The five audit-only tests are listed explicitly in:

```text
tests/phase155_audit_only_nodeids.txt
```

They are not ordinary per-change regression tests. They are run explicitly at Phase closure or another major integration boundary because they perform whole-population or historical completion audits.

The Phase 155 closure evidence is therefore:

```text
routine sharded regression: PASS
audit-only explicit closure run: 5/5 PASS
monolithic repository-wide pytest: not run
```

This is an intentional evidence composition, not a claim that one monolithic pytest process produced an all-green result.

During implementation, prefer focused tests for the changed contract. At Phase closure, run the routine sharded regression and then the explicit audit-only set. A complete monolithic historical run is reserved for a release or another integration milestone where that specific evidence is useful.

Temporary backup directories containing copied `test_*.py` files must not be created inside the repository root because pytest may collect them and produce duplicate-module import mismatches. Backup artifacts should be stored outside the repository, for example under the user's Downloads directory."""

  readme = _replace_between(
    readme,
    "## Test and backup hygiene",
    "## Project principle",
    test_hygiene,
  )

  readme_closure = f"""## Phase 155 closure — Test Suite Consolidation

Phase 155 changed test maintenance, not Toda mathematics, proof search, stored provenance, or the public proof APIs.

The phase classified the historical test population into current contract coverage, historical compatibility, audit-only coverage, duplicate/superseded coverage, and performance-heavy integration coverage.

The largest historical runtime outliers were replaced with lightweight contract tests where the expensive mathematical reconstruction was not the contract under test:

```text
508.30s
281.49s
276.88s
```

Reference/provenance integration tests were similarly reduced when the same contract was already protected at a lower or clearer API boundary.

The final Phase 155 test boundary is:

```text
current collection: {collected}
routine: {routine}
audit-only: 5
```

Routine closure uses sharded regression with checkpoint/resume. The five audit-only nodeids remain explicit and are executed only at Phase closure or another major integration boundary.

Phase 155 deliberately does not implement Reference-statement relevance or minimal Reference display. That work begins in Phase 156."""

  readme = _replace_marked_section(
    readme,
    README_MARKER_START,
    README_MARKER_END,
    readme_closure,
  )

  design_section = f"""# Phase 155 Test Suite Consolidation 設計

Phase 155 は test architecture（テスト構成）の整理を行う maintenance Phase であり、Toda の theorem fact、`ProofStep`、proof search、Narrative の数学的意味を変更しない。

## test boundary

現行 collection:

```text
total: {collected}
routine: {routine}
audit-only: 5
```

通常 regression と audit-only を明示的に分離する。

```text
routine test
→ 日常の regression / Phase-final sharded regression

audit-only test
→ whole-population / historical completion audit
→ Phase closure または major integration で明示実行
```

audit-only の境界は function-level nodeid を `tests/phase155_audit_only_nodeids.txt` に列挙して固定する。

## sharded regression

routine regression は test file を単位に shard へ分割する。

```text
file-based shard
→ pytest
→ PASS checkpoint
→ PASS shard は再実行しない
```

目安:

```text
target: 約5分 / shard
10分超: split / review candidate
```

sharding は test semantics を変更しない。単に実行単位と再実行境界を変える。

## stale / duplicate test の扱い

削除・軽量化の対象は、現在の contract を守らず過去の implementation shape だけを固定する test とする。

代表例:

```text
historical fixed contribution count
historical connector placement snapshot
source-code branch shape
obsolete exact Reference locator
同一 provenance contract の多層重複
```

削除時は current contract を別 test が保持することを確認する。

```text
test deletion
!= contract deletion
```

## audit-only 5件

5件は routine regression から除外するが削除しない。

対象は:

```text
Phase144 final completion audit x2
Phase153 all-group Reference population audit
Phase153 112-group Reference-body ownership audit
Phase97 representative cross-layer provenance audit
```

これらは whole-population / integration evidence として Phase closure で明示実行する。

## Phase boundary

Phase 155:

```text
test classification
stale / duplicate repair
lightweight contract replacement
audit-only boundary
sharded closure regression
```

Phase 156:

```text
Reference statement relevance
minimal Reference display
```

Phase 155 では Phase156 の presentation rule を先取りしない。"""

  design = _replace_marked_section(
    design,
    DESIGN_MARKER_START,
    DESIGN_MARKER_END,
    design_section,
  )

  development_section = f"""# Phase 155 Test Suite Consolidation 完了

Phase 155 は test suite の feedback loop を短縮し、現在の contract と historical test を分離する maintenance Phase とした。

production の数学的ロジック、proof graph、proof search、public API は変更していない。

## baseline

Phase 155 開始時監査:

```text
test files: 843
test functions: 10292
```

初回 monolithic closure run:

```text
10421 collected
98 failed
10323 passed
2380.08s (0:39:40)
```

最大 runtime:

```text
508.30s
281.49s
276.88s
```

これら3件は provenance / ordering contract を維持しつつ lightweight test へ置換した。

## consolidation

実施内容:

```text
stale expectation audit
duplicate / superseded audit
canonical regression boundary audit
routine / historical / audit / performance-heavy classification
contract-sensitive 24件の再分類
heavy provenance test の lightweight replacement
112-group population audit の統合
representative provenance matrix の統合
obsolete Phase144 intermediate-shape test の削除
```

audit-only manifest は最終的に5件とした。

## sharded regression

R3 では monolithic pytest を使わず、routine regression を shard 化した。

初回 plan:

```text
10392 routine tests
837 files
8 shards
5 audit-only excluded
```

PASS 済み shard を checkpoint し、timeout / failure のある shard だけを分割・修復して再実行した。

最終 routine evidence:

```text
original PASS shards: 1, 2, 6, 7
R3-R2 repair jobs 2-8: PASS
R3-R3 focused repaired job1 contracts: PASS
Closure-R3 routine result: PASS
```

R3 中に stale test をさらに削除したため、R4 collection は:

```text
total: {collected}
routine: {routine}
audit-only: 5
```

となった。

## explicit audit-only closure

Phase-final R4 で audit-only 5件を1件ずつ明示実行した。

```text
{audit_summary}
```

結果:

```text
5/5 PASS
```

したがって Phase155 の closure evidence は:

```text
routine sharded regression PASS
+
audit-only 5/5 PASS
```

である。

monolithic repository-wide pytest は再実行していない。この点は意図的であり、単一 process の all-green を claim しない。

## test policy after Phase155

```text
implementation
→ focused tests

Phase closure
→ routine sharded regression
→ explicit audit-only closure

major release / integration
→ 必要なら complete monolithic historical regression
```

1 shard は約5分を目安とし、10分を超える場合は split / review candidate とする。

## 次 Phase

Phase156 は test consolidation ではなく、Reference statement relevance / minimal display を扱う。

```text
Reference title
→ 維持

Reference statement lines
→ proof body / consumer が必要とするものだけか監査
```

Phase155 ではこの presentation rule を先取りしていない。"""

  development = _replace_marked_section(
    development,
    DEVELOPMENT_MARKER_START,
    DEVELOPMENT_MARKER_END,
    development_section,
  )

  old_roadmap_start = (
    "### Phase 155 — Reference statement relevance / minimal display"
  )
  old_roadmap_end = (
    "## 今後も先取りしないもの"
  )

  roadmap_replacement = f"""### Phase 155 — Test Suite Consolidation — 完了

Phase 155 は保留していた Test Suite Consolidation を独立 Phase として実施した。

完了内容:

```text
stale expectation inventory
duplicate / superseded coverage audit
current contract boundary
audit-only boundary
performance-heavy test review
lightweight contract replacement
sharded regression
checkpoint / resume
```

closure 時点:

```text
total tests: {collected}
routine tests: {routine}
audit-only tests: 5
routine sharded regression: PASS
audit-only explicit closure: 5/5 PASS
monolithic repository-wide pytest: NOT run
```

通常 regression と whole-population audit を分離し、Phase closure では両方を組み合わせて completion evidence とする。

### Phase 156 — Reference statement relevance / minimal display

Phase 153 で Reference selection / granularity、Phase154 で prose generation を整理した。

Phase156 では Reference selection 自体を作り直さず、Reference section に表示する statement の必要性と粒度を監査する。

主な問い:

```text
Reference title は必要
↓
statement lines は proof body が実際に必要とするものだけか

group-result statement は本文の論証で使われているか
aggregate statement の余分な component が表示されていないか
同じ Reference 内で statement を過剰表示していないか
stable / unstable の provenance を混同していないか
```

方針:

```text
Proof graph / consumer usage
→ necessary Reference statement set
→ minimal display
```

群別 special case や theorem fact の削除ではなく、presentation relevance の一般規則として扱う。

先取りしないもの:

```text
Reference selection の全面再設計
new theorem facts
proof search
theorem ranking
automatic best proof selection
dedicated renderer retirement
stable-range mathematical expansion
```"""

  if old_roadmap_start in roadmap:
    roadmap = _replace_between(
      roadmap,
      old_roadmap_start,
      old_roadmap_end,
      roadmap_replacement,
    )
  else:
    roadmap = _replace_marked_section(
      roadmap,
      ROADMAP_MARKER_START,
      ROADMAP_MARKER_END,
      roadmap_replacement,
    )

  roadmap_closure = f"""# Phase 155 closure / Phase 156 current plan

Phase155 Test Suite Consolidation は完了。

```text
current collection: {collected}
routine: {routine}
audit-only: 5

routine sharded regression: PASS
audit-only explicit closure: 5/5 PASS
```

次は Phase156 `Reference statement relevance / minimal display`。

Phase156 は非安定群の proof Narrative を中心に、Reference statement が consumer に対して本当に必要かを一般規則で監査する。stable range の表示は維持するが、Phase156 の目的を stable computation 拡張へ広げない。"""

  roadmap = _replace_marked_section(
    roadmap,
    ROADMAP_MARKER_START,
    ROADMAP_MARKER_END,
    roadmap_closure,
  )

  proof_section = f"""# Phase 155 test-suite provenance record

Phase 155 は数学的 theorem fact や proof provenance を追加・変更する Phase ではない。

対象は test evidence の provenance、すなわち「どの test が current contract を保証し、どの test が historical / audit-only / duplicate / performance-heavy なのか」という verification boundary である。

## proof provenance boundary

Phase155 で変更していないもの:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
LiteratureReference
existing recursive provenance
Toda theorem facts
group-result proof roots
```

したがって:

```text
test deletion
!= proof deletion

stale expectation repair
!= theorem change

lightweight contract replacement
!= provenance reduction
```

## audit-only provenance

audit-only 5件は routine regression から外すが、completion evidence から削除しない。

```text
routine regression
→ local/current contract feedback

audit-only
→ whole-population / historical completion evidence
```

Phase-final explicit audit:

```text
{audit_summary}
```

すべて PASS。

## current collection boundary

```text
total: {collected}
routine: {routine}
audit-only: 5
```

Phase155 closure は単一 monolithic pytest の all-green ではなく、

```text
routine sharded regression PASS
+
audit-only explicit closure 5/5 PASS
```

を verification provenance とする。

## stale historical expectation boundary

Phase144 由来の一部 test は、現在の generic renderer の意味ではなく次の historical implementation shape を固定していた。

```text
fixed contribution count
fixed connector count / position
source-code branch shape
Reference statement absence
old exact source metadata
```

これらは current contract が別 test で保持されることを確認して削除または更新した。

## next provenance boundary

Phase156 は verification architecture ではなく Reference statement relevance / minimal display を扱う。

```text
stored proof provenance
→ unchanged

Reference selection / granularity
→ Phase153

proof prose generation
→ Phase154

test verification boundary
→ Phase155

Reference statement necessity / minimal display
→ Phase156
```"""

  proof = _replace_marked_section(
    proof,
    PROOF_MARKER_START,
    PROOF_MARKER_END,
    proof_section,
  )

  _write(
    readme_path,
    readme,
  )
  _write(
    design_path,
    design,
  )
  _write(
    development_path,
    development,
  )
  _write(
    roadmap_path,
    roadmap,
  )
  _write(
    proof_path,
    proof,
  )

  docs_output = (
    output_dir
    / "documentation"
  )
  docs_output.mkdir(
    parents=True,
    exist_ok=True,
  )

  output_map = {
    readme_path: (
      docs_output
      / "README.md"
    ),
    design_path: (
      docs_output
      / "design.md"
    ),
    development_path: (
      docs_output
      / "development_log.md"
    ),
    roadmap_path: (
      docs_output
      / "roadmap.md"
    ),
    proof_path: (
      docs_output
      / "proof_records.md"
    ),
  }

  for source, destination in (
    output_map.items()
  ):
    shutil.copyfile(
      source,
      destination,
    )

  print(
    "Phase155 closure documentation updated."
  )
  print(
    "README language: English"
  )
  print(
    "design/development_log/roadmap/proof_records: Japanese"
  )
  print(
    "Full updated documents copied to:"
  )
  print(
    docs_output
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
