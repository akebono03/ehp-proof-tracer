from pathlib import Path
import shutil
import sys


DOC_PATHS = (
  Path("README.md"),
  Path("docs/design.md"),
  Path("docs/development_log.md"),
  Path("docs/roadmap.md"),
  Path("docs/proof_records.md"),
)


def _read(path):
  return path.read_text(encoding="utf-8")


def _write_preserving_newlines(path, text):
  original = path.read_bytes()
  newline = "\r\n" if b"\r\n" in original else "\n"
  normalized = text.replace("\r\n", "\n").replace("\r", "\n")
  path.write_bytes(normalized.replace("\n", newline).encode("utf-8"))


def _append_once(text, marker, section):
  if marker in text:
    return text
  return text.rstrip() + "\n\n" + section.strip() + "\n"


def _replace_phase148_roadmap(text, regression_summary):
  start_marker = (
    "## 現在地: Phase 148 — "
    "RC2 Recursive exactness evidence exposure"
  )
  phase149_marker = (
    "## Phase 149 — RC3: "
    "Contribution ownership / insertion ordering"
  )
  start = text.find(start_marker)
  phase149 = text.find(phase149_marker)

  if start < 0:
    raise RuntimeError("Phase 148 current-location marker not found")
  if phase149 < 0 or phase149 <= start:
    raise RuntimeError("Phase 149 marker not found after Phase 148")

  replacement = f'''## Phase 148 — 完了: RC2 Recursive exactness evidence exposure

Phase 148 は、primary method に吸収されない recursive exactness evidence の
main Narrative への露出を、proof provenance を削除せず一般規則で制御した。

完了内容:

```text
RC2-1 exposure audit
RC2-2 minimal general exposure rule design
RC2-3 exposure classification / body contribution integration
RC2-4 Web depth parity / semantic closure / six-group cross audit
RC2-5 final regression / documentation closure
```

確定した exposure class:

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

表示境界:

```text
OWNED_PRIMARY
→ raw EXACTNESS_WINDOW は本文で抑制
→ derived short exact sequence / higher-level method presentation は保持

UNOWNED_RECURSIVE
→ recursive raw exactness contribution を本文で抑制
→ proof graph / provenance は保持

AMBIGUOUS_RELEVANT
→ conservative fallback として既存表示を保持
```

Web Narrative は selected depth の bounded replay を入力とし、必要な semantic dependency
だけを semantic closure で補う。complete replay を user-selected depth の代わりに
使用しない。

R4.2 では original bounded presentation の equality conclusion に対する direct equality
premise を1段だけ semantic closure に追加し、$\\pi_6^3$ の numbered calculation chain を
復元した。exactness ProofStep はこの calculation closure では追加しない。

6代表群:

$$
\\pi_6^3,\\quad
\\pi_8^5,\\quad
\\pi_{{10}}^4,\\quad
\\pi_{{12}}^5,\\quad
\\pi_{{15}}^8,\\quad
\\pi_{{16}}^9
$$

の post-repair audit では次を確認した。

```text
bounded semantic closure remains below complete replay
closure-added exactness = 0
visible raw exactness ProofStep = 0
AMBIGUOUS_RELEVANT exposure = 0
```

$\\pi_{{10}}^4$ と $\\pi_{{12}}^5$ に残る generic `is exact` prose は actual
`TodaProp42ExactnessStatement` raw rendering ではないため、raw exactness leakage と
して数えない。判定は文字列件数ではなく actual statement rendering に基づく。

final repository-wide regression:

```text
{regression_summary}
```

Phase 148 完了。

---

## 現在地: Phase 149 — RC3 Contribution ownership / insertion ordering

'''
  return text[:start] + replacement + text[phase149:]


def main():
  if len(sys.argv) != 2:
    raise SystemExit(
      "usage: apply_phase148_rc2_5_documentation.py "
      "<regression-summary-file>"
    )

  summary_path = Path(sys.argv[1])
  regression_summary = summary_path.read_text(
    encoding="utf-8"
  ).strip()

  if not regression_summary:
    raise SystemExit("empty regression summary")

  for path in DOC_PATHS:
    if not path.exists():
      raise SystemExit(f"required document not found: {path}")

  readme = _read(Path("README.md"))
  readme_section = f'''## Phase 148 closure

Phase 148 completed RC2, recursive exactness evidence exposure, without adding
new Toda theorem facts or changing the stored proof graph.

The Narrative layer now classifies exactness method components as
`OWNED_PRIMARY`, `UNOWNED_RECURSIVE`, or `AMBIGUOUS_RELEVANT`. Owned primary
methods keep the higher-level method presentation and derived short exact
sequence while suppressing raw exactness windows. Unowned recursive exactness
evidence remains available in proof provenance but is not automatically
expanded in the main Narrative. Ambiguous directly relevant evidence keeps the
conservative existing-display fallback.

Web Narrative now starts from the user-selected bounded replay depth. Semantic
closure adds only the dependencies required by the Narrative rules instead of
silently replacing depth 2 with complete replay. The Phase 148 calculation
closure adds one level of direct equality premises for original equality
conclusions; it does not add exactness proof steps.

The final six-group audit covered

$$
\\pi_6^3,\\quad
\\pi_8^5,\\quad
\\pi_{{10}}^4,\\quad
\\pi_{{12}}^5,\\quad
\\pi_{{15}}^8,\\quad
\\pi_{{16}}^9.
$$

It confirmed that bounded semantic closure remains below complete replay, no
exactness step is introduced by calculation closure, no raw
`TodaProp42ExactnessStatement` rendering is exposed, and no
`AMBIGUOUS_RELEVANT` component occurs in the audited groups.

The final repository-wide Phase 148 regression is:

```text
{regression_summary}
```

Phase 149 is intentionally separate and addresses RC3 contribution ownership
and insertion ordering. Phase 148 does not change the ordering of the short
exact sequence and final group conclusion.
'''
  readme = _append_once(
    readme,
    "## Phase 148 closure",
    readme_section,
  )

  design = _read(Path("docs/design.md"))
  design_section = f'''# 32. Phase 148 RC2 完了境界

Phase 148 は recursive exactness evidence の main Narrative への露出を制御する
presentation semantics を一般化した。

基本経路:

```text
ProofStep provenance
→ Argument method evidence
→ exactness method component
→ RC1 ownership
→ RC2 exposure classification
→ Narrative body / contribution rendering
```

exposure class:

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

意味:

```text
OWNED_PRIMARY
→ Argument が所有する primary exactness method
→ raw EXACTNESS_WINDOW は本文で抑制
→ derived short exact sequence / higher-level method presentation は保持

UNOWNED_RECURSIVE
→ recursive provenance から到達するが primary method ではない
→ main Narrative body への raw exactness 展開を抑制
→ ProofStep / proof edge / provenance は削除しない

AMBIGUOUS_RELEVANT
→ directly relevant component が複数
→ RC2 では推測して1つへ絞らず conservative fallback
```

重要:

```text
exactness exposure suppression
!= ProofStep deletion
!= proof edge deletion
!= theorem fact deletion
!= new proof search
```

Web Narrative の replay 境界:

```text
selected depth
→ bounded group-result replay
→ semantic closure
→ Narrative
```

user-selected depth 2 を complete replay へ置き換えない。

R4.2 calculation-premise semantic closure は、original bounded presentation に存在する
equality conclusion の direct equality premise を1段だけ追加する。

```text
original equality conclusion
→ one-level direct equality premises

closure-added equality premise
→ 同じ calculation rule では再帰展開しない
```

既存 registered semantic-definition closure は従来どおり維持する。
この calculation closure は `TodaProp42ExactnessStatement` を追加対象にしない。

6代表群の final RC2-4 audit:

```text
bounded below complete: PASS
closure-added exactness zero: PASS
visible raw exactness zero: PASS
ambiguous exposure zero: PASS
```

raw exactness の判定は `"is exact"` / `"は完全である"` の単純文字列件数ではなく、
actual `TodaProp42ExactnessStatement` の normalized rendering が最終 Narrative に
現れるかで判定する。higher-level method prose と raw exactness window を混同しない。

Phase 148 final repository-wide regression:

```text
{regression_summary}
```

Phase 148 / RC2 は exposure selection の責務であり、次は扱わない。

```text
short exact sequence と final conclusion の ordering
contribution insertion ordering
generic provenance / reason prose
EHP semantic naming
final equation numbering / prose formatting
```

ordering / insertion は Phase 149 / RC3 の責務である。
'''
  design = _append_once(
    design,
    "# 32. Phase 148 RC2 完了境界",
    design_section,
  )

  development_log = _read(Path("docs/development_log.md"))
  development_section = f'''# Phase 148 — RC2 Recursive exactness evidence exposure

Phase 148 は Phase 146 で RC2 と分類した recursive exactness evidence exposure を、
target-specific special case ではなく一般 presentation rule で解決する Phase とした。

## RC2-1 — exposure audit

既存 method evidence / exactness component / contribution 経路を監査した。

問題は、primary component が存在しない場合に recursive exactness evidence が
main Narrative へ露出し得ることだった。proof graph / provenance の問題ではなく、
main Narrative exposure の問題として分離した。

## RC2-2 — minimal general exposure rule

3 class を定義した。

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

provenance を保持し、ownership を exposure より先に決定し、unowned recursive evidence は
body へ自動展開しない。ambiguous directly relevant evidence は推測して選ばない。

## RC2-3 — minimal implementation

`TodaGroupProofNarrativeExactnessExposureClass` と一般 classifier を追加し、
exactness contribution filter / Argument body renderer / multi renderer に接続した。

Repair R1 では direct-premise relocation が exposure filter を迂回していた経路を抑制した。

focused result:

```text
38 passed in 13.10s
```

## RC2-4 — Web parity / semantic closure / cross-group audit

Web Narrative が selected depth 2 ではなく complete replay を入力にしていることを確認した。

R3 diagnostic:

```text
pi_6^3:
depth2 input nodes = 18
depth3 nodes = 36
complete nodes = 177
depth2 public exactness count = 0
complete public exactness count = 15
Web exactness count = 15
```

R4 で Web Narrative を bounded replay へ戻した。

その結果、$\\pi_6^3$ の numbered calculation chain に必要な depth-3 equality premises が
presentation から不足することが判明し、R4.2 で semantic closure を最小拡張した。

R4.2-R2:

```text
59 passed in 24.11s
input replay nodes = 18
closure nodes = 25
closure max_depth = 3
closure-added steps = 7
closure-added equality steps = 6
Web exactness phrases = 0
```

6群 audit で $\\pi_{{10}}^4$ と $\\pi_{{12}}^5$ に generic exactness phrase が1件ずつ
残ったが、R5-R1 / R5-R2 で actual exactness ProofStep の raw rendering ではないことを確認した。

R5-R3 final six-group focused regression:

```text
61 passed in 32.20s
```

final invariants:

```text
all bounded below complete = True
all closure-added exactness zero = True
all visible raw exactness zero = True
all ambiguous exposure zero = True
```

## RC2-5 — final regression / documentation closure

Phase 最後に repository-wide regression を1回実行した。

```text
{regression_summary}
```

## Phase 148 完了境界

解決:

```text
recursive exactness evidence exposure classification
owned-primary raw exactness suppression
unowned-recursive raw exactness suppression
relocated direct-premise exactness suppression
Web Narrative bounded-depth parity
minimum calculation-premise semantic closure
statement-based raw exactness audit invariant
```

維持:

```text
ProofStep provenance
proof graph
theorem facts
existing proof search
Trace / Outline explicit selection
Narrative default depth 2
derived short exact sequence
higher-level method presentation
```

未着手:

```text
RC3 contribution ownership / insertion ordering
short exact sequence → final group conclusion ordering
RC4 generic provenance / reason prose
RC5 EHP semantic naming
RC6 final equation numbering / prose formatting
```

Phase 148 完了。次は Phase 149 / RC3。
'''
  development_log = _append_once(
    development_log,
    "# Phase 148 — RC2 Recursive exactness evidence exposure",
    development_section,
  )

  roadmap = _replace_phase148_roadmap(
    _read(Path("docs/roadmap.md")),
    regression_summary,
  )

  proof_records = _read(Path("docs/proof_records.md"))
  proof_section = f'''# Phase 148 recursive exactness exposure provenance record

Phase 148 は新しい Toda theorem fact を追加した Phase ではない。

対象は Phase 146 で RC2 と分類した recursive exactness evidence の Narrative exposure である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

RC2 exposure classification は proof graph を変更せず、

```text
existing exactness ProofStep
→ method evidence
→ exactness component
→ Argument ownership
→ exposure class
```

を presentation layer で導出する。

```text
hidden from main Narrative
!= deleted from proof provenance

UNOWNED_RECURSIVE
!= mathematically irrelevant

OWNED_PRIMARY
!= new theorem ownership
```

## bounded replay / semantic closure provenance

Web Narrative は user-selected bounded replay を入力とする。

```text
depth 2 selection
→ depth-2 bounded replay
→ semantic closure
→ Narrative
```

complete replay は selected depth の代替として main Web Narrative に渡さない。

R4.2 semantic closure は original bounded presentation に存在する equality conclusion の
direct equality premise を1段だけ補う。existing `ProofStep.premises` を再利用するだけで、
新しい equality を生成しない。また calculation rule は exactness ProofStep を追加しない。

## pi_6^3 calculation provenance

depth 2 では

$$
2\\nu'=\\eta_3^3
$$

が存在する一方、その direct equality premises

$$
2\\nu'=\\eta_3E\\eta_3\\eta_5
$$

および

$$
\\eta_3E\\eta_3\\eta_5=\\eta_3^3
$$

は shortest depth 3 にある。

R4.2 はこの existing premise edge を1段だけ closure に含め、Narrative の numbered
calculation chain を復元する。

```text
existing equality premise recovery
!= theorem synthesis
```

## exactness exposure provenance

6代表群:

$$
\\pi_6^3,\\quad
\\pi_8^5,\\quad
\\pi_{{10}}^4,\\quad
\\pi_{{12}}^5,\\quad
\\pi_{{15}}^8,\\quad
\\pi_{{16}}^9
$$

の final audit で:

```text
closure-added exactness = 0
visible raw exactness ProofStep = 0
AMBIGUOUS_RELEVANT = 0
```

を確認した。

$\\pi_{{10}}^4$ と $\\pi_{{12}}^5$ では最終 Narrative に generic `is exact` prose が1行残るが、
actual `TodaProp42ExactnessStatement` の normalized raw rendering とは一致しない。

```text
generic exactness phrase
!= raw exactness ProofStep exposure
```

RC2 completion invariant は actual statement identity / rendering に基づく。

## RC2 / RC3 boundary

Phase 148 は

```text
どの exactness evidence を main Narrative に露出するか
```

を扱う。

次の contribution ownership / insertion ordering と short exact sequence / conclusion ordering は
Phase 149 / RC3 の責務である。

## final verification record

R5-R3 focused:

```text
61 passed in 32.20s
```

repository-wide final:

```text
{regression_summary}
```

この結果を Phase 148 / RC2 の final provenance boundary とする。
'''
  proof_records = _append_once(
    proof_records,
    "# Phase 148 recursive exactness exposure provenance record",
    proof_section,
  )

  updated = {
    Path("README.md"): readme,
    Path("docs/design.md"): design,
    Path("docs/development_log.md"): development_log,
    Path("docs/roadmap.md"): roadmap,
    Path("docs/proof_records.md"): proof_records,
  }

  for path, text in updated.items():
    _write_preserving_newlines(path, text)

  output_root = (
    Path("phase148_rc2_5_final_regression_documentation_closure")
    / "updated_full_documents"
  )
  for path in DOC_PATHS:
    destination = output_root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, destination)

  print("Phase 148 RC2-5 documentation closure applied.")
  print("Full updated documents copied to:")
  print(output_root)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
