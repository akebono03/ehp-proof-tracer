from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


ROOT = Path.cwd()
PACKAGE = ROOT / "phase150_finalization"
OUT = PACKAGE / "updated_full_documents"

DOCS = (
    Path("README.md"),
    Path("docs/design.md"),
    Path("docs/development_log.md"),
    Path("docs/roadmap.md"),
    Path("docs/proof_records.md"),
)


README_SECTION = r"""
<!-- PHASE150_CLOSURE -->
## Phase 150 closure — generic provenance / reason prose and strategy boundary

Phase 150 closes the representative-proof phase of the generic Narrative migration.
No additional theorem fact, proof edge, proof search rule, or group-specific Narrative
special case is added by this finalization step.

The phase established that evaluating Narrative quality while several renderer
generations coexist can make a presentation defect appear group-specific even when
the underlying pressure belongs to a general semantic or rendering rule. In
particular, staged migration can leave representative groups on generic, dedicated,
and legacy recursive routes at the same time.

The development strategy therefore changes at the Phase 150 / Phase 151 boundary:

```text
representative-group staged migration
→ all-target generic observation
→ cross-group defect classification
→ one general-rule repair
→ regenerate all targets
```

Phase 151 starts by making the target population observable through the same generic
renderer under the same replay/presentation conditions. This is an audit baseline,
not an immediate public-route switch. Dedicated renderers and legacy fallbacks remain
available as comparison baselines until generic output is sufficiently validated.

The new rule for subsequent Narrative work is:

```text
group identity is not the repair criterion
semantic role / proof structure is the repair criterion
```

The Phase 150 finalization itself changes documentation only. Production behavior
and canonical tests are unchanged by the closure package.

Final repository-wide regression:

```text
{pytest_summary}
```

Phase 151 will re-plan the remaining Narrative work from the all-group generic
baseline rather than continuing representative-group-by-group route migration.
""".strip()


DESIGN_SECTION = r"""
# Phase 150 終了時の Narrative 一般化戦略境界

Phase 150 終了時点で、Narrative の一般化を評価する単位を代表群から対象群全体へ変更する。

これまでの段階的移行では、同一時点に

```text
generic renderer
dedicated renderer
legacy recursive fallback
```

が共存し得る。この状態では、群ごとの表示差に renderer route の差と一般規則の差が混在する。

Phase 151 以降の設計原則は次とする。

```text
全対象群を同一 generic 条件で観測
→ 問題を群名ではなく semantic category で分類
→ 一般規則を1件だけ修正
→ 全対象群を再生成して影響を確認
```

ここで「全対象群を generic 化する」とは、Phase 151 開始時点で public route を一括変更することを意味しない。
まず audit path（監査経路）で同一 generic renderer を強制適用し、比較可能な baseline を作る。

dedicated renderer と legacy fallback は、generic output の品質比較および regression の基準として当面保持する。

以後の Narrative 修正では、原則として

```text
特定の群
特定の (n, k)
特定 generator 名
```

そのものを条件に prose を変更しない。

修正条件は、

```text
semantic role
argument purpose
proof dependency
ownership
exposure
placement
statement category
```

など、proof structure（証明構造）から一般的に導出できる情報に置く。

Phase 150 Finalization はこの戦略境界を文書化するだけであり、production code、proof graph、theorem fact、既存 test を変更しない。
""".strip()


DEV_SECTION = r"""
# Phase 150 — Generic provenance / reason prose 終了と開発戦略の切替

Phase 150 はここで終了する。

Phase 146 以降は $\pi_6^3$ の旧高品質 Narrative を基準として、一般化不足を root cause ごとに整理し、
RC1〜RC4 の順に改善してきた。

Phase 150 の作業を通じて、段階的な generic route 移行を続けながら代表群ごとに文章を修正すると、

```text
generic route
dedicated renderer
legacy recursive fallback
```

という複数世代の表示経路の差が、群固有の問題のように見えることが確認された。

このため Phase 150 では、代表群単位の追加 Narrative 修正をこれ以上進めず、
Phase 151 から評価戦略を変更することを決定した。

新しい開発サイクルは次とする。

```text
全対象群 generic baseline
↓
横断監査
↓
問題を semantic category ごとに集計
↓
一般規則を1件修正
↓
全対象群を再生成
↓
次の一般規則へ
```

これは「全対象群を一度に綺麗にする」という意味ではない。
入力母集団を最初から全対象群とし、修正自体は従来どおり一課題ずつ行う。

Phase 150 Finalization では production code と既存 test を変更しない。
Phase の最後として repository-wide regression を実施した。

```text
{pytest_summary}
```

Phase 151 では public route の一括切替や dedicated renderer の削除を先に行わない。
最初に全対象群を同一 generic renderer・同一 depth・同一規則で生成できる監査 baseline を確立する。
""".strip()


PROOF_SECTION = r"""
# Phase 150 closure / provenance strategy boundary

Phase 150 Finalization は数学的 theorem fact や proof provenance を変更しない。

```text
new theorem fact: none
new ProofStep edge: none
proof search change: none
production renderer change in finalization: none
canonical test change in finalization: none
```

Phase 150 までの監査から、群間の Narrative 差を評価するときは、proof provenance の差だけでなく
renderer route の世代差を分離する必要があることを記録する。

Phase 151 以降は、全対象群について同一 generic renderer を監査経路から適用し、

```text
semantic blocks
Narrative arguments
ownership
exposure
placement
fallback
statement category
```

を横断的に観測する。

dedicated renderer / legacy fallback は直ちに削除せず、generic Narrative の比較基準として保持する。

一般規則の修正は群名を根拠にせず、stored proof provenance と semantic structure から導出できる条件に限定する。

Phase 150 final repository-wide regression:

```text
{pytest_summary}
```

この記録を Phase 150 の provenance boundary とする。
""".strip()


ROADMAP_SECTION = r"""
## Phase 150 — 完了: Generic provenance / reason prose と戦略境界

Phase 150 では generic provenance / reason prose の改善を進める過程で、
段階的 generic route 移行そのものが群間の Narrative 表示差を生む要因になることを確認した。

代表群ごとの追加修正を続ける方式はここで終了する。

Phase 150 Finalization は production code / canonical tests を変更せず、
Phase 151 以降の評価戦略を次へ切り替える。

```text
代表群ごとの段階的切替
→ 全対象群を同一 generic 条件で観測
→ 横断的に一般規則の不足を分類
→ 一般規則を1件ずつ修正
```

final repository-wide regression:

```text
{pytest_summary}
```

---

## Phase 151 — All-group generic baseline / cross-group audit

目的:

- 全対象群を同一 generic renderer、同一 depth、同一規則で生成できる監査経路を確立する。
- public route の現行挙動はまだ一括変更しない。
- dedicated renderer / legacy fallback を比較基準として保持する。
- 群ごとの表示差と renderer route の差を分離する。

主な監査項目:

```text
generic generation success / failure
semantic block categories
Narrative argument roles
raw / structured fallback
OTHER
reason ownership
definition placement
exactness exposure
contribution ordering
final-result derivation
recursive expansion
```

完了条件:

- 対象母集団を同一 generic 条件で再現可能に生成できる。
- failure / fallback / category inventory を群横断で取得できる。
- production public route を変更せず baseline を保存できる。
- 次 Phase で直すべき問題を「群」ではなく「一般規則カテゴリ」で選べる。

---

## Phase 152 — Generic defect classification / repair ordering

Phase 151 の全群 baseline をもとに、残る問題を semantic / presentation category ごとに分類する。

この Phase では将来の修正順を、出現数だけでなく依存関係と downstream impact を見て決定する。

候補カテゴリには次を含む。

```text
reason ownership
definition ownership / placement
calculation / derivation ordering
exactness presentation
final-result derivation
raw rule-name fallback
OTHER block
duplicate contribution
recursive result reuse
```

Phase 152 の結果に基づき、Phase 153 以降は一つの Phase で一種類の一般規則を修正する。

---

## Phase 153 以降 — one general rule per Phase

Phase 153 以降の具体的な番号と対象は Phase 152 の監査結果で確定する。

各 Phase の基本サイクル:

```text
1 general defect category
→ minimum general repair
→ focused regression
→ all-target regeneration / audit
→ no target-specific branch
```

public route の generic 統一は、全対象群の generic baseline と主要一般規則が十分安定した後に独立した Phase として行う。

dedicated renderer / legacy fallback の削除は public route 統一と regression 確認より後に行う。
""".strip()


def read(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    target = ROOT / path
    target.write_text(text.rstrip() + "\n", encoding="utf-8")


def append_once(text: str, marker: str, section: str) -> str:
    if marker in text:
        raise RuntimeError(f"closure marker already exists: {marker}")
    return text.rstrip() + "\n\n---\n\n" + section.rstrip() + "\n"


def replace_roadmap_future(text: str, section: str) -> str:
    # Phase 150 is the intentional replanning boundary. Replace the old Phase 150+
    # plan rather than preserving obsolete RC5/RC6 scheduling.
    m = re.search(r"(?m)^## Phase 150\b", text)
    if not m:
        raise RuntimeError("docs/roadmap.md: Phase 150 heading not found")
    return text[:m.start()].rstrip() + "\n\n---\n\n" + section.rstrip() + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: apply_phase150_finalization.py <pytest-summary-file>")
        return 2

    summary_path = Path(sys.argv[1])
    summary = summary_path.read_text(encoding="utf-8", errors="replace").strip()
    if not summary:
        raise RuntimeError("pytest summary is empty")

    for path in DOCS:
        if not (ROOT / path).is_file():
            raise RuntimeError(f"missing canonical document: {path}")

    originals = {path: read(path) for path in DOCS}

    updated = dict(originals)
    updated[Path("README.md")] = append_once(
        originals[Path("README.md")],
        "<!-- PHASE150_CLOSURE -->",
        README_SECTION.format(pytest_summary=summary),
    )
    updated[Path("docs/design.md")] = append_once(
        originals[Path("docs/design.md")],
        "# Phase 150 終了時の Narrative 一般化戦略境界",
        DESIGN_SECTION,
    )
    updated[Path("docs/development_log.md")] = append_once(
        originals[Path("docs/development_log.md")],
        "# Phase 150 — Generic provenance / reason prose 終了と開発戦略の切替",
        DEV_SECTION.format(pytest_summary=summary),
    )
    updated[Path("docs/proof_records.md")] = append_once(
        originals[Path("docs/proof_records.md")],
        "# Phase 150 closure / provenance strategy boundary",
        PROOF_SECTION.format(pytest_summary=summary),
    )
    updated[Path("docs/roadmap.md")] = replace_roadmap_future(
        originals[Path("docs/roadmap.md")],
        ROADMAP_SECTION.format(pytest_summary=summary),
    )

    OUT.mkdir(parents=True, exist_ok=True)
    for path, content in updated.items():
        out_path = OUT / path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content.rstrip() + "\n", encoding="utf-8")

    # Only after all five full documents have been generated successfully,
    # replace the canonical copies.
    for path, content in updated.items():
        write(path, content)

    print("Phase 150 documentation closure applied.")
    print("Full updated documents:")
    for path in DOCS:
        print(f"  {OUT / path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
