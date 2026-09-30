from pathlib import Path
import re
import shutil
import sys

SUMMARY_PATH = Path(
  "phase149_rc3_5_final_regression_documentation_closure"
) / "repository_regression_summary.txt"

FILES = {
  "README.md": "en",
  "docs/design.md": "ja",
  "docs/development_log.md": "ja",
  "docs/roadmap.md": "ja",
  "docs/proof_records.md": "ja",
}

MARKER = "PHASE149_RC3_CLOSURE"


def _read_summary():
  if not SUMMARY_PATH.exists():
    raise RuntimeError(
      "repository_regression_summary.txt is missing"
    )

  summary = SUMMARY_PATH.read_text(
    encoding="utf-8",
  ).strip()

  if not summary:
    raise RuntimeError(
      "repository regression summary is empty"
    )

  return summary


def _section_for(
  path,
  summary,
):
  if path == "README.md":
    return f"""
<!-- {MARKER} -->
## Phase 149 closure — Narrative contribution ordering

Phase 149 completed RC3, Narrative contribution ordering, without adding new Toda theorem facts or changing the stored proof graph.

Phase 147 established which Narrative Argument owns a primary exactness method. Phase 148 established which exactness evidence is exposed. Phase 149 adds the corresponding placement rule:

```text
RC1: Argument -> method ownership
RC2: method -> visible evidence
RC3: visible evidence -> Narrative placement
```

For visible `OWNED_PRIMARY` exactness evidence, the Narrative body now collects the existing RC2 display contributions and places them before the owning Argument conclusion. This placement is independent of the global Narrative block order.

For the representative proof

$$
\\pi_6^3=\\mathbb{{Z}}/4\\{{\\nu'\\}},
$$

the group-structure explanation now presents the EHP exactness method and the derived short exact sequence

$$
0
\\longrightarrow
\\pi_5^2
\\xrightarrow{{E}}
\\pi_6^3
\\xrightarrow{{H}}
\\pi_6^5
\\longrightarrow
0
$$

before the final group-structure conclusion.

The RC3-4 cross-group audit covered

$$
\\pi_6^3,\\quad
\\pi_8^5,\\quad
\\pi_{{10}}^4,\\quad
\\pi_{{12}}^5,\\quad
\\pi_{{15}}^8,\\quad
\\pi_{{16}}^9.
$$

Audit result:

```text
pi_6^3:  owned_primary_visible=1, ordering_ok=True
pi_8^5:  owned_primary_visible=1, ordering_ok=True
pi_10^4: owned_primary_visible=0, ordering_ok=True
pi_12^5: owned_primary_visible=0, ordering_ok=True
pi_15^8: owned_primary_visible=0, ordering_ok=True
pi_16^9: owned_primary_visible=0, ordering_ok=True

failures=[]
AUDIT_RESULT=PASS
```

Focused RC3-4 / RC3-3 / RC2 regression:

```text
57 passed in 10.85s
```

Final repository-wide regression:

```text
{summary}
```

Phase 149 changes presentation ordering only:

```text
Narrative contribution placement
!= ProofStep ordering
!= proof edge mutation
!= theorem inference
!= exactness exposure classification
```

The observed placement of the derived calculation

$$
2\\nu'=\\eta_3^3
$$

inside the order Argument remains a separate calculation/derivation-ordering pressure. It is not treated as an RC3 exactness-placement failure and is not changed in Phase 149.

The next planned pressure is Phase 150 / RC4, generic provenance / reason prose.
"""
  if path == "docs/design.md":
    return f"""
<!-- {MARKER} -->
# Phase 149 RC3 Narrative contribution ordering

Phase 149 は Phase 146 で RC3 と分類した Narrative contribution ordering（Narrative 寄与の配置順）を扱う。

責務の分離は次のとおり。

```text
RC1:
Narrative Argument
→ primary method ownership

RC2:
primary / recursive method evidence
→ exposure classification

RC3:
visible owned evidence
→ Narrative placement
```

RC3 の一般順序は次を目標とする。

```text
method
→ evidence
→ derivation
→ conclusion
```

`OWNED_PRIMARY` exactness evidence は、RC2 の既存 contribution 抽出・filter をそのまま利用し、owner Argument の conclusion より前へ配置する。

重要なのは、global Narrative block order を proof の説明順そのものと見なさないことである。

```text
global block order
!= Argument-local explanatory order
```

Phase 149 RC3-3 では、`OWNED_PRIMARY` exactness contribution を body loop の前に収集し、元 exactness block 位置での重複表示を抑止し、owner conclusion block の直前へ挿入する。

この処理は presentation-only である。

```text
exactness placement
!= exactness exposure reclassification
!= ProofStep relocation
!= proof edge mutation
!= theorem fact creation
```

6代表群

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9
$$

の RC3-4 audit では全 Argument で ordering invariant が成立した。

```text
failures=[]
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

repository-wide final regression:

```text
{summary}
```

なお、$\pi_6^3$ の order Argument 内で

$$
2\nu'=\eta_3^3
$$

という derived calculation の表示位置をさらに自然にできる余地はある。しかしこれは RC3 の exactness evidence placement とは異なる calculation / derivation internal ordering の問題であり、Phase 149 では変更しない。
"""
  if path == "docs/development_log.md":
    return f"""
<!-- {MARKER} -->
# Phase 149 — RC3 Narrative contribution ordering

## RC3-1 Ordering audit

$\pi_6^3$ の current Narrative を監査した。

RC2 の exposure / ownership は正しく、問題は short exact sequence が final group conclusion より後に表示される placement に限定された。

既存 hidden contribution ordering には provider anchor / dependent contribution / argument conclusion という一般 placement model が存在する一方、RC2 の derived short exact sequence は local exactness block 位置で直接 render されていた。

## RC3-2 General ordering rule design

一般的な Narrative 順序を

```text
method
→ evidence
→ derivation
→ conclusion
```

とした。

$\pi_6^3$、dimension、$\nu'$、short exact sequence type に依存する special case は採用しない。

RC2 の display-derived contribution を無理に `ProofStep` contribution 型へ変換せず、既存 RC2 display path 上で owner conclusion より前へ配置する最小方針とした。

## RC3-3 Minimal implementation

変更対象:

```text
toda_group_proof_narrative_argument_body_renderer.py
render_toda_group_proof_narrative_argument_body_markdown()
```

初回実装では exactness block に到達後に contribution を defer したが、multi-Argument renderer が local body と method evidence を global block order へ再構成するため、$\pi_6^3$ の conclusion が先に処理され、末尾 fallback へ流れた。

初回 focused result:

```text
49 passed
1 failed
```

Repair R1 では `OWNED_PRIMARY` exactness contribution を loop 前に precollect し、owner conclusion 直前へ挿入する方式へ修正した。

Repair R1 focused result:

```text
50 passed in 10.84s
```

## RC3-4 Cross-group ordering audit

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

結果:

```text
pi_6^3: owned_primary_visible=1, ordering_ok=True
pi_8^5: owned_primary_visible=1, ordering_ok=True
pi_10^4: owned_primary_visible=0, ordering_ok=True
pi_12^5: owned_primary_visible=0, ordering_ok=True
pi_15^8: owned_primary_visible=0, ordering_ok=True
pi_16^9: owned_primary_visible=0, ordering_ok=True

failures=[]
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

production change は RC3-3 の1関数のみで、RC3-4 は audit/test のみ。

## RC3-5 Final regression / documentation closure

Phase 149 の最終 repository-wide regression:

```text
{summary}
```

Phase 149 完了。

完了境界:

```text
visible OWNED_PRIMARY exactness evidence
→ owner Argument conclusion より前へ配置

RC2 exposure classification
→ unchanged

ProofStep / proof graph / theorem facts
→ unchanged
```

$\pi_6^3$ の order Argument 内の derived calculation `(3)` の位置は、RC3 exactness placement とは別の改善候補として残す。

次は Phase 150 / RC4 `Generic provenance / reason prose`。
"""
  if path == "docs/roadmap.md":
    return f"""
<!-- {MARKER} -->
# Phase 149 完了 — RC3 Narrative contribution ordering

Phase 149 / RC3 は完了。

目的:

```text
RC2 で表示対象になった evidence を
owner Argument の論証順に配置する
```

達成した一般規則:

```text
method
→ evidence
→ derivation
→ conclusion
```

代表6群の cross-group audit:

```text
pi_6^3:  ordering_ok=True
pi_8^5:  ordering_ok=True
pi_10^4: ordering_ok=True
pi_12^5: ordering_ok=True
pi_15^8: ordering_ok=True
pi_16^9: ordering_ok=True
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

repository-wide final:

```text
{summary}
```

## 次の順序

Phase 146 で整理した残課題は引き続き次の依存順で扱う。

```text
Phase 150 / RC4
Generic provenance / reason prose

Phase 151 / RC5
EHP semantic naming

Phase 152 / RC6
Final equation numbering / prose formatting
```

Phase 150 では RC3 の ordering を再設計しない。表示された fact に対して、一般的な provenance / reason prose をどのように付与するかを対象とする。

$\pi_6^3$ の order Argument 内にある derived calculation

$$
2\nu'=\eta_3^3
$$

の局所的な表示順改善候補は記録するが、Phase 150 の RC4 を先取りして Phase 149 に追加実装しない。
"""
  if path == "docs/proof_records.md":
    return f"""
<!-- {MARKER} -->
# Phase 149 RC3 Narrative ordering / provenance record

Phase 149 は新しい Toda theorem fact を追加していない。

対象は Phase 146 の RC3:

```text
Contribution ownership / insertion ordering
```

である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 149 の placement rule は RC2 で表示可能と判定された existing contribution の Narrative 上の位置だけを変更する。

```text
Narrative placement
!= ProofStep placement

Narrative placement
!= proof edge creation

Narrative placement
!= theorem inference

Narrative placement
!= exactness exposure classification
```

## pi_6^3 record

対象:

$$
\pi_6^3=\mathbb{{Z}}/4\{{\nu'\}}.
$$

Phase 149 RC3-1 では final group conclusion より後に derived short exact sequence が表示されていた。

RC3-3 Repair R1 後は、

$$
0
\longrightarrow
\pi_5^2
\xrightarrow{{E}}
\pi_6^3
\xrightarrow{{H}}
\pi_6^5
\longrightarrow
0
$$

が owner `establish_group_structure` Argument の final conclusion より前に表示される。

この配置は $\pi_6^3$ 専用条件ではなく `OWNED_PRIMARY` exposure と owner conclusion の関係から決まる。

## six-group ordering record

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{{10}}^4,\quad
\pi_{{12}}^5,\quad
\pi_{{15}}^8,\quad
\pi_{{16}}^9.
$$

RC3-4:

```text
pi_6^3: owned_primary_visible=1, ordering_ok=True
pi_8^5: owned_primary_visible=1, ordering_ok=True
pi_10^4: owned_primary_visible=0, ordering_ok=True
pi_12^5: owned_primary_visible=0, ordering_ok=True
pi_15^8: owned_primary_visible=0, ordering_ok=True
pi_16^9: owned_primary_visible=0, ordering_ok=True

failures=[]
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

## remaining boundary

$\pi_6^3$ の order Argument では、式 (1), (2) から得る

$$
2\nu'=\eta_3^3
$$

をさらに早い位置へ置く方が文章上自然である可能性がある。

ただしこれは exactness contribution placement ではなく calculation / derivation internal ordering である。

したがって:

```text
observed prose-order improvement
!= RC3 failure
```

として Phase 149 では production change を追加しない。

## final verification record

repository-wide final regression:

```text
{summary}
```

Phase 149 / RC3 完了。

次の provenance pressure は Phase 150 / RC4 `Generic provenance / reason prose` とする。
"""
  raise AssertionError(
    path
  )


def main():
  summary = _read_summary()

  for path in FILES:
    target = Path(
      path
    )

    if not target.exists():
      raise RuntimeError(
        f"missing documentation file: {path}"
      )

    text = target.read_text(
      encoding="utf-8",
    )

    if MARKER in text:
      raise RuntimeError(
        f"Phase 149 closure already present in {path}"
      )

    section = _section_for(
      path,
      summary,
    )

    updated = (
      text.rstrip()
      + "\n\n---\n\n"
      + section.strip()
      + "\n"
    )

    target.write_text(
      updated,
      encoding="utf-8",
    )

  output_dir = (
    Path(
      "phase149_rc3_5_final_regression_documentation_closure"
    )
    / "updated_full_documents"
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  for path in FILES:
    source = Path(
      path
    )
    destination = (
      output_dir
      / source.name
    )
    shutil.copyfile(
      source,
      destination,
    )

  print(
    "Phase 149 RC3-5 documentation closure applied."
  )
  print(
    "Updated full documents:"
  )
  for path in FILES:
    print(
      f"  {path}"
    )


if __name__ == "__main__":
  main()
