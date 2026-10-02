from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def _read(path: Path) -> str:
  return path.read_text(encoding="utf-8-sig")


def _write(path: Path, text: str) -> None:
  path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _marked(
  text: str,
  start: str,
  end: str,
  section: str,
) -> str:
  payload = start + "\n" + section.rstrip() + "\n" + end
  first = text.find(start)

  if first < 0:
    return text.rstrip() + "\n\n" + payload + "\n"

  last = text.find(end, first)

  if last < 0:
    raise ValueError("Missing end marker: " + end)

  last += len(end)
  return text[:first] + payload + text[last:]


def _between(
  text: str,
  start: str,
  end: str,
  section: str,
) -> str:
  first = text.find(start)
  last = text.find(end, first)

  if first < 0 or last < 0:
    raise ValueError("Roadmap replacement boundary not found.")

  return text[:first] + section.rstrip() + "\n\n" + text[last:]


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", type=Path, default=Path.cwd())
  parser.add_argument("--output-dir", type=Path, required=True)
  args = parser.parse_args()

  root = args.repo_root.resolve()
  output = args.output_dir.resolve()

  result = json.loads(
    (output / "audit_result.json").read_text(encoding="utf-8")
  )

  if not result["all_audit_only_pass"]:
    raise SystemExit(
      "Documentation blocked until 2/2 final audits PASS."
    )

  readme_path = root / "README.md"
  design_path = root / "docs" / "design.md"
  dev_path = root / "docs" / "development_log.md"
  roadmap_path = root / "docs" / "roadmap.md"
  proof_path = root / "docs" / "proof_records.md"

  readme = _read(readme_path)
  design = _read(design_path)
  dev = _read(dev_path)
  roadmap = _read(roadmap_path)
  proof = _read(proof_path)

  readme_section = """## Phase 155 closure — Test Suite Consolidation

Phase 155 reorganized test evidence without changing Toda mathematics, proof search, stored provenance, or public proof APIs.

The final collection is:

```text
10384 tests total
10382 routine tests
2 audit-only tests
```

Routine regression is executed in file-based shards with checkpoint/resume semantics. Passed shards are not rerun after unrelated repairs. The working target is about five minutes per shard; ten minutes is a split/review boundary rather than a normal feedback unit.

The final two audit-only tests are explicit Phase-closure integration audits:

```text
Phase153 all-group public Reference structural audit
Phase97 representative cross-layer provenance audit
```

Three earlier audit-only candidates were removed from the Phase155 closure boundary. Two Phase144 audits fixed historical renderer implementation shape. The Phase153 exact Reference/body duplicate audit measured 117 duplicate candidates; that observation is retained as Phase156 input because Reference statement relevance and minimal display belong to Phase156.

Final Phase155 evidence:

```text
routine sharded regression: PASS
final audit-only explicit closure: 2/2 PASS
monolithic repository-wide pytest: not run
```"""

  readme = _marked(
    readme,
    "<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_START -->",
    "<!-- PHASE155_TEST_CONSOLIDATION_CLOSURE_END -->",
    readme_section,
  )

  design_section = """# Phase 155 Test Suite Consolidation 設計

Phase155 は test architecture の maintenance Phase であり、Toda theorem fact、`ProofStep`、proof search、Narrative の数学的意味を変更しない。

最終 boundary:

```text
total: 10384
routine: 10382
audit-only: 2
```

routine regression は file-based shard + checkpoint/resume とする。

final audit-only:

```text
Phase153 all-group public Reference structural audit
Phase97 representative cross-layer provenance audit
```

Phase144 の historical completion/source-shape audit は current contract ではないため削除した。

Phase153 の exact selected-statement/body duplicate audit は 117件を観測した。ただしこれは test-suite defect ではなく Phase156 の Reference statement relevance / minimal display の pressure である。

```text
117 duplicate observations
→ Phase156 input
!= Phase155 production defect
```"""

  design = _marked(
    design,
    "<!-- PHASE155_TEST_CONSOLIDATION_DESIGN_START -->",
    "<!-- PHASE155_TEST_CONSOLIDATION_DESIGN_END -->",
    design_section,
  )

  dev_section = """# Phase 155 Test Suite Consolidation 完了

Phase155 は test suite の feedback loop を短縮し、current contract と historical test を分離した。

開始時:

```text
test files: 843
test functions: 10292
```

初回 monolithic closure run:

```text
10421 collected
98 failed
10323 passed
2380.08s
```

最大 runtime:

```text
508.30s
281.49s
276.88s
```

重い provenance / ordering test は lightweight contract へ置換した。

Closure-R3 では routine regression を shard 化し、PASS shard を checkpoint で保持した。

```text
Closure-R3 routine result: PASS
```

R4 で当初の audit-only 5件を実行すると、historical implementation-shape assumption と Phase156 相当の Reference duplicate pressure が混在していることが判明した。

最終 audit-only は2件に再分類した。

```text
1. Phase153 all-group public Reference structural audit
2. Phase97 representative cross-layer provenance audit
```

Phase153 の exact selected-statement/body duplicate audit は 117件を観測した。この observation は削除せず Phase156 の開始 pressure として保存する。

最終 collection:

```text
10384 total
10382 routine
2 audit-only
```

closure evidence:

```text
routine sharded regression PASS
+
final audit-only 2/2 PASS
```

monolithic repository-wide pytest は再実行していない。

次 Phase は Phase156 `Reference statement relevance / minimal display`。"""

  dev = _marked(
    dev,
    "<!-- PHASE155_CLOSURE_START -->",
    "<!-- PHASE155_CLOSURE_END -->",
    dev_section,
  )

  roadmap_replacement = """### Phase 155 — Test Suite Consolidation — 完了

Phase155 は保留していた Test Suite Consolidation を独立 Phase として実施した。

```text
10384 total
10382 routine
2 audit-only
routine sharded regression: PASS
final audit-only: 2/2 PASS
monolithic repository-wide pytest: NOT run
```

### Phase 156 — Reference statement relevance / minimal display

Phase156 は Reference selection 自体を作り直さず、Reference section に表示する statement の必要性と粒度を監査する。

開始 pressure:

```text
Phase155 R4 で観測:
117 exact selected-statement/body duplicates
```

主な問い:

```text
Reference title は必要
↓
statement lines は proof body が実際に必要とするものだけか

group-result statement は本文で利用されているか
aggregate statement の余分な component が表示されていないか
Reference section と本文で同じ statement を不必要に重複していないか
```

方針:

```text
Proof graph / consumer usage
→ necessary Reference statement set
→ minimal display
```

stable range の表示は維持するが、Phase156 を stable computation 拡張へ広げない。"""

  old_start = (
    "### Phase 155 — Reference statement relevance / minimal display"
  )
  old_end = "## 今後も先取りしないもの"

  if old_start in roadmap:
    roadmap = _between(
      roadmap,
      old_start,
      old_end,
      roadmap_replacement,
    )
  else:
    roadmap = _marked(
      roadmap,
      "<!-- PHASE155_CLOSURE_ROADMAP_START -->",
      "<!-- PHASE155_CLOSURE_ROADMAP_END -->",
      roadmap_replacement,
    )

  proof_section = """# Phase 155 test-suite provenance record

Phase155 は数学的 proof provenance を変更していない。

最終 collection:

```text
10384 total
10382 routine
2 audit-only
```

completion evidence:

```text
routine sharded regression PASS
+
explicit closure audit 2/2 PASS
```

Phase144 completion/source-shape audit は historical implementation shape を current failure と誤認するため closure boundary から削除した。

Phase153 exact selected-statement/body duplicate audit は 117件を観測した。

```text
117 observations
→ Phase156 audit input
!= Phase155 production defect
```

Phase97 closure audit は `goal_source` を常に要求しない。

```text
direct result
→ goal_source=None を許容

aggregate result
→ goal_source identity / repository metadata を保持
```

次の provenance boundary:

```text
Phase153: Reference selection / granularity
Phase154: proof prose generation
Phase155: test verification boundary
Phase156: Reference statement necessity / minimal display
```"""

  proof = _marked(
    proof,
    "<!-- PHASE155_TEST_PROVENANCE_START -->",
    "<!-- PHASE155_TEST_PROVENANCE_END -->",
    proof_section,
  )

  _write(readme_path, readme)
  _write(design_path, design)
  _write(dev_path, dev)
  _write(roadmap_path, roadmap)
  _write(proof_path, proof)

  docs_out = output / "documentation"
  docs_out.mkdir(parents=True, exist_ok=True)

  for source, name in (
    (readme_path, "README.md"),
    (design_path, "design.md"),
    (dev_path, "development_log.md"),
    (roadmap_path, "roadmap.md"),
    (proof_path, "proof_records.md"),
  ):
    shutil.copyfile(source, docs_out / name)

  print("Phase155 R4-R2 documentation updated.")
  print("Full document copies:", docs_out)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
