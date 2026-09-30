from pathlib import Path
import shutil

ROOT = Path.cwd()
DOCS = ROOT / "docs"
PACKAGE = ROOT / "phase147_documentation_closure"
OUTPUT = PACKAGE / "updated_full_documents"

DEVELOPMENT = DOCS / "development_log.md"
ROADMAP = DOCS / "roadmap.md"
PROOF = DOCS / "proof_records.md"

DEVELOPMENT_APPEND = r"""

---

# Phase 147 — RC1 Argument-method ownership 完了

Phase 147 は Phase 146 で分類した6 root causes のうち、RC1
`Argument-method ownership` のみを扱った。

対象は、Narrative argument が「何を示すために、どの exactness method を主要な証明手段として
使うか」という ownership（所有関係）である。

Phase 147 では RC2 以降の evidence exposure、contribution ordering、provenance prose、
EHP naming、equation numbering を先取りしていない。

## RC1-1 — ownership boundary audit

現行 generic Narrative の method selection 経路を監査した。

確認した既存構造:

```text
NarrativeArgument
→ relevant groups
→ method evidence
→ exactness method components
→ primary exactness selection
→ renderer
```

重要な確認:

```text
Argument.supporting_blocks
!= Argument method ownership
```

`supporting_blocks` に `EXACTNESS` block がなくても、
`extract_toda_group_proof_narrative_argument_method_evidence()` は recursive provenance から
method evidence を取得できる。

したがって RC1 の問題は method discovery failure ではなく、renderer に入る前の
`Argument → primary exactness method` 関係が独立した semantic API として表現されていないこと
だった。

## RC1-2 — minimal ownership API design

`TodaGroupProofNarrativeArgument` 自体には method field を追加しない方針を採用した。

既存の低水準 selection API:

```text
relevant groups
+
exactness components
→ primary exactness component
```

を維持し、その上に argument 単位の ownership API を置く設計とした。

```text
presentation
blocks
semantic sidecar
arguments
argument index
→ argument-owned primary exactness component | None
```

RC1 では新しい ownership dataclass を追加せず、既存 semantic data から導出できる関係として扱う。

## RC1-3 — minimal ownership API implementation

`select_toda_group_proof_narrative_argument_primary_exactness_component()`
を追加し、既存処理を組み合わせて argument-owned primary method を取得できるようにした。

既存 primitive API は維持した。

multi-argument renderer の primary-method selection は、新 ownership API を使用する経路へ変更した。

一方、body / evidence handling が引き続き必要とする method evidence extraction は残した。

```text
primary-method ownership selection
→ RC1 API

body / evidence handling
→ existing method evidence

RC1 ownership
!= RC2 evidence exposure
```

RC1-3 Repair R1 後:

```text
Phase 147 ownership tests:
8 passed in 7.07s

focused existing regression:
46 passed in 15.96s
```

## RC1-4 — ownership integration audit

6代表群を横断して ownership integration を監査した。

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

確認結果:

```text
multi renderer:
  ownership API call present
  old inline primary selector absent
  method evidence extraction preserved
```

$\pi_6^3$ では、

```text
establish_order
→ primary exactness method owned

establish_group_structure
→ a different primary exactness method owned
```

となることを確認した。

generic header は次の proof-purpose / method relation を生成する。

```text
次に、$\nu'$ の位数を決定するために、次の完全列を考える.
```

および

```text
最後に、$\pi_{6}^{3}$ の群構造を決定するために、次の完全列を考える.
```

RC1-4 regression:

```text
15 passed in 4.28s
```

## RC1-5 — Phase 147 final regression

Phase 147 の最後にのみ repository-wide regression を実行した。

focused:

```text
RC1 ownership:
54 passed in 17.54s

Generic Narrative:
24 passed in 6.66s

Web group-proof Narrative:
20 passed in 10.72s
```

boundary verification:

```text
Argument -> primary exactness ownership API: present
Multi renderer old inline primary selection: absent
Method evidence for body handling: preserved
RC2 evidence exposure behavior: intentionally unchanged
RC3 contribution ordering behavior: intentionally unchanged
```

repository-wide final:

```text
10314 passed in 2942.66s (0:49:02)
```

Phase 147 完了。

## Phase 147 完了境界

Phase 147 で解決したもの:

```text
Narrative Argument
→ owned primary exactness method
```

Phase 147 で意図的に解決していないもの:

```text
recursive auxiliary exactness evidence の過剰表示
exactness contribution duplication の RC2 部分
contribution insertion ordering
short exact sequence と final conclusion の配置順
generic Reference / reason prose
EHP semantic naming
final equation numbering / prose formatting
```

したがって次は Phase 148 / RC2 `Recursive exactness evidence exposure` とする。
"""

PROOF_APPEND = r"""

---

# Phase 147 Argument-method ownership provenance record

Phase 147 は新しい Toda の数学的 theorem fact を追加した Phase ではない。

対象は Phase 146 で RC1 と分類した Narrative presentation 上の
`Argument-method ownership` である。

## ownership provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 147 で追加した ownership API は、既存 proof provenance から取得できる

```text
argument relevant groups
method evidence
exactness method components
```

を組み合わせ、

```text
Narrative Argument
→ primary exactness method component | None
```

という presentation 上の関係を導出する。

したがって:

```text
Argument-method ownership
!= theorem ownership

primary exactness ownership
!= new exactness fact

ownership selection
!= new proof search

ownership selection
!= proof edge creation

ownership API
!= EHP evaluator
```

## supporting blocks と method ownership の分離

Phase 147 の audit では、

```text
Argument.supporting_blocks
```

と

```text
Argument method ownership
```

を同一視しないことを確認した。

`supporting_blocks` に exactness block が直接含まれなくても、既存 recursive provenance から
method evidence が得られる場合がある。

したがって ownership は `NarrativeArgument` の stored field として追加せず、
既存 semantic structure から導出する API とした。

## pi_6^3 ownership record

対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

Phase 147 RC1-4 では `establish_order` と `establish_group_structure` が、それぞれ異なる
primary exactness method を所有することを確認した。

```text
establish_order
→ $\nu'$ の位数決定の primary exactness method

establish_group_structure
→ $\pi_6^3$ の群構造決定の primary exactness method
```

これにより generic Narrative は proof purpose と method introduction を

```text
$\nu'$ の位数を決定するために、次の完全列を考える.
```

のように結び付けられる。

これは historical $\pi_6^3$ 専用文字列を埋め込んだものではない。

## RC1 / RC2 boundary

multi-argument renderer では primary-method selection を ownership API へ移した。

一方、body / evidence handling に必要な

```text
extract_toda_group_proof_narrative_argument_method_evidence()
```

は維持した。

したがって Phase 147 は、

```text
どの argument がどの primary method を所有するか
```

を扱うが、

```text
recursive exactness evidence を本文にどこまで表示するか
```

は変更しない。

後者は Phase 148 / RC2 の責務である。

同様に、

```text
short exact sequence
→ final group conclusion
```

などの contribution placement / ordering は Phase 149 / RC3 の責務として残す。

## final verification record

focused:

```text
RC1 ownership:
54 passed in 17.54s

Generic Narrative:
24 passed in 6.66s

Web group-proof Narrative:
20 passed in 10.72s
```

repository-wide final:

```text
10314 passed in 2942.66s (0:49:02)
```

この結果を Phase 147 / RC1 の final regression boundary とする。

```text
RC1 complete
!= historical pi_6^3 Narrative fully restored

RC1 complete
!= auxiliary exactness exposure solved

RC1 complete
!= contribution ordering solved
```

次の provenance / presentation pressure は Phase 148 / RC2
`Recursive exactness evidence exposure` とする。
"""

OLD_ROADMAP = r"""## Phase 147 — RC1: Argument-method ownership

目的:

historical proof-purpose と current argument-method ownership の差を、target-specific special
case ではなく一般規則で解消する。

主対象:

```text
order argument と主要 exactness method の ownership
argument purpose と method introduction の対応
```

Phase 147 では RC2 以降を先取りしない。

完了条件:

```text
RC1 の concrete blocker が一般 ownership rule で解消
+
existing proof preservation
+
focused regression
```

---

## Phase 148 — RC2: Recursive exactness evidence exposure
"""

NEW_ROADMAP = r"""## Phase 147 — 完了: RC1 Argument-method ownership

Phase 147 は historical proof-purpose と current argument-method ownership の差を、
target-specific special case ではなく一般 ownership API で整理した。

完了内容:

```text
RC1-1 ownership boundary audit
RC1-2 minimal ownership API design
RC1-3 minimal ownership API implementation
RC1-4 ownership integration audit
RC1-5 final regression
```

確定した経路:

```text
Narrative Argument
→ existing method evidence
→ exactness method components
→ argument-owned primary exactness method
→ renderer
```

multi renderer は primary-method selection に ownership API を使用する。

旧 inline primary selector は multi renderer から除去した。

body / evidence handling 用の method evidence extraction は維持し、RC2 を先取りしていない。

$\pi_6^3$ では、

```text
establish_order
→ primary exactness method

establish_group_structure
→ a different primary exactness method
```

を確認した。

final regression:

```text
10314 passed in 2942.66s (0:49:02)
```

Phase 147 完了。

---

## 現在地: Phase 148 — RC2 Recursive exactness evidence exposure

## Phase 148 — RC2: Recursive exactness evidence exposure
"""


def append_once(path: Path, marker: str, text: str) -> None:
    source = path.read_text(encoding="utf-8")
    if marker in source:
        raise SystemExit(
            f"{path}: Phase 147 documentation marker already exists"
        )
    path.write_text(
        source.rstrip() + text + "\n",
        encoding="utf-8",
    )


def replace_once(path: Path, old: str, new: str) -> None:
    source = path.read_text(encoding="utf-8")
    count = source.count(old)
    if count != 1:
        raise SystemExit(
            f"{path}: expected roadmap block exactly once, found {count}"
        )
    path.write_text(
        source.replace(old, new, 1),
        encoding="utf-8",
    )


def main() -> int:
    for path in (DEVELOPMENT, ROADMAP, PROOF):
        if not path.exists():
            raise SystemExit(f"missing required file: {path}")

    append_once(
        DEVELOPMENT,
        "# Phase 147 — RC1 Argument-method ownership 完了",
        DEVELOPMENT_APPEND,
    )
    replace_once(
        ROADMAP,
        OLD_ROADMAP,
        NEW_ROADMAP,
    )
    append_once(
        PROOF,
        "# Phase 147 Argument-method ownership provenance record",
        PROOF_APPEND,
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        DEVELOPMENT,
        OUTPUT / "development_log.md",
    )
    shutil.copy2(
        ROADMAP,
        OUTPUT / "roadmap.md",
    )
    shutil.copy2(
        PROOF,
        OUTPUT / "proof_records.md",
    )

    print("Phase 147 documentation closure applied.")
    print("Changed:")
    print("  docs/development_log.md")
    print("  docs/roadmap.md")
    print("  docs/proof_records.md")
    print("Unchanged:")
    print("  README.md")
    print("  docs/design.md")
    print("Full updated files copied to:")
    print("  phase147_documentation_closure/updated_full_documents/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
