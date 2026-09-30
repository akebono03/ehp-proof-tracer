from pathlib import Path
import shutil

FILES = (
  Path("README.md"),
  Path("docs/design.md"),
  Path("docs/development_log.md"),
  Path("docs/roadmap.md"),
  Path("docs/proof_records.md"),
)

README_APPEND = r"""

## Phase 148 closure — recursive exactness evidence exposure

Phase 148 completed RC2, `Recursive exactness evidence exposure`, without adding new Toda theorem facts or changing the stored proof graph.

The Narrative pipeline now distinguishes exactness method evidence as:

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

For an `OWNED_PRIMARY` exactness component, raw exactness-window prose is suppressed while the owned higher-level method contribution, including an appropriate derived short exact sequence, may remain visible.

For `UNOWNED_RECURSIVE` evidence, recursive exactness body contributions are not automatically expanded into the Narrative. The proof provenance remains available; the suppression is presentation-only.

`AMBIGUOUS_RELEVANT` remains conservative and preserves the existing display behavior rather than guessing an owner.

The Web Narrative path now respects the selected bounded replay depth instead of replacing it with complete replay. Semantic closure remains presentation-side and adds only the narrowly required existing provenance for Narrative rendering. At depth 0, semantic closure is the identity. For positive depth, the Phase 148 calculation closure is limited to the equality-premise chain needed beneath an existing order relation, while the previously registered definition closure remains available.

The Phase 148 boundary is therefore:

```text
proof provenance
→ RC1 argument-method ownership
→ RC2 exactness evidence exposure
→ Narrative body
```

It does not include contribution ordering. In particular, ordering pressure such as a final group conclusion appearing before its explanatory short exact sequence is deferred to Phase 149 / RC3.

Final verification evidence:

```text
focused RC2 regression:
92 passed in 36.15s

canonical repository regression:
10398 passed, 3 failed in 1316.54s (0:21:56)

failure classification:
the three failures were confined to
tests/test_phase144_6_pi6_generic_production_route.py
and were stale expectations introduced by earlier Phase 148 repair work.

restored Phase 144-6 contract:
4 passed in 1.71s
```

The repository-wide suite was not rerun after restoring those three stale expectations, in accordance with the Phase-final test policy. The final record therefore preserves the measured whole-suite result and the focused restoration result separately rather than inventing an inferred all-pass count.
"""

DESIGN_APPEND = r"""

---

# Phase 148 設計完了記録 — Recursive exactness evidence exposure

Phase 148 / RC2 の責務は、既存 proof provenance に含まれる recursive exactness evidence
（再帰的な完全性証拠）を Narrative 本文へどこまで展開するかを一般規則として決定することである。

## exposure pipeline

```text
ProofStep / provenance
→ method evidence
→ RC1: Argument-method ownership
→ RC2: exactness exposure classification
→ Narrative body
```

Phase 148 では exactness method component を次の3分類で扱う。

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

### OWNED_PRIMARY

Argument が primary method として所有する component。

```text
raw EXACTNESS_WINDOW
→ 本文では抑制

DERIVED_SHORT_EXACT_SEQUENCE / higher-level method contribution
→ ownership と contribution rule に従って保持可能

provenance
→ 保持
```

### UNOWNED_RECURSIVE

recursive provenance から到達するが、その Argument の primary method として所有されない component。

```text
body contribution
→ 自動展開しない

raw exactness
→ 自動展開しない

derived short exact sequence
→ 自動展開しない

provenance
→ 保持
```

### AMBIGUOUS_RELEVANT

複数 component が直接 relevant で一意な owner を決定できない場合。

```text
conservative fallback
→ 既存表示を維持
→ renderer が ownership を推測しない
```

## semantic closure boundary

Web Narrative は selected depth の bounded replay を入力とする。

```text
selected bounded replay
→ semantic closure
→ Narrative renderer
```

complete replay を Web Narrative の入力として常用しない。

depth 0 では semantic closure は identity とする。

positive depth では、既存 provenance のうち Narrative に必要な最小 dependency のみを補う。
Phase 148 で追加した calculation closure は、

```text
ORDER relation
→ direct EQUALITY premise
→ その equality の direct EQUALITY premises
```

という graph-level relation に限定する。

これにより $\pi_6^3$ の位数計算に必要な equality chain は補う一方、
group-structure context や Hopf chain の無関係な equality を一括で展開しない。

既存の registered definition semantic closure は維持する。

```text
semantic closure
!= new proof search
!= new theorem fact
!= proof edge creation
```

## Phase 149 との境界

Phase 148 は exposure を扱い、ordering は扱わない。

```text
RC2:
どの exactness evidence を本文に出すか

RC3:
表示対象 contribution をどの順序に置くか
```

したがって、

```text
short exact sequence
→ final group conclusion
```

のような数学書としての説明順序は Phase 149 / RC3 の責務とする。
"""

DEVLOG_APPEND = r"""

---

# Phase 148 完了 — RC2 Recursive exactness evidence exposure

Phase 146 で分類した root cause のうち RC2
`Recursive exactness evidence exposure` を実装・監査した。

## 実施内容

1. recursive exactness evidence の現行経路を監査。
2. exposure class を
   `OWNED_PRIMARY` / `UNOWNED_RECURSIVE` / `AMBIGUOUS_RELEVANT`
   に整理。
3. `UNOWNED_RECURSIVE` の body contribution を自動展開しない一般規則を追加。
4. relocated direct premise 経路から raw exactness が再挿入される bypass を抑制。
5. `OWNED_PRIMARY` でも raw exactness window 自体は本文へ再挿入しないよう統一。
6. Web Narrative が complete replay を常用していた経路を bounded replay へ戻した。
7. bounded depth で必要な計算式を失わないため semantic closure を監査。
8. broad equality closure を撤回し、
   `ORDER → direct EQUALITY → equality premises`
   に限定した graph-level closure へ修正。
9. depth 0 は semantic closure identity とした。
10. 6代表群
    $\pi_6^3,\pi_8^5,\pi_{10}^4,\pi_{12}^5,\pi_{15}^8,\pi_{16}^9$
    を横断監査した。

## 代表監査結果

RC2-4 最終6群監査では、

```text
all bounded below complete = True
all closure-added exactness = 0
all visible raw exactness = 0
all ambiguous exposure = 0
```

を確認した。

$\pi_6^3$ depth 2 では broad closure の +7 nodes を監査し、
必要な order calculation equality 2件と definition endpoint だけを残す方向へ限定した。

## 最終修正

Phase 148 RC2-5 の途中で過去 test contract を広い文字列置換で誤変更したため、
stale expectation を個別に復元した。

最終 focused regression:

```text
92 passed in 36.15s
```

canonical repository regression:

```text
pytest -q tests

10398 passed
3 failed
1316.54s (0:21:56)
```

3 failures はすべて

```text
tests/test_phase144_6_pi6_generic_production_route.py
```

の誤変更された Phase 144-6 contract に限定された。

GitHub `develop` の現行 contract へ復元後:

```text
4 passed in 1.71s
```

全体 suite は Phase-final 方針に従い再実行していない。
したがって `10401 passed` のような推定値は記録せず、
whole-suite 実測と focused restoration 実測を分けて保存する。

## Phase 148 完了条件

```text
RC2 exposure general rule
→ 完了

raw recursive exactness overexposure
→ 解消

Web selected-depth bounded replay
→ 復元

depth-0 no-premise boundary
→ 復元

order calculation semantic closure scope
→ 最小化

proof provenance
→ 不変

RC3 ordering
→ 未着手
```

次は Phase 149 / RC3 `Narrative ordering`。
"""

ROADMAP_APPEND = r"""

---

# Phase 148 完了後ロードマップ

## Phase 148 — 完了

RC2 `Recursive exactness evidence exposure` を完了した。

```text
RC1 Argument-method ownership
→ Phase 147 完了

RC2 Recursive exactness evidence exposure
→ Phase 148 完了
```

Phase 148 では proof provenance を削除せず、Narrative 本文への exactness evidence の
表示範囲だけを一般規則で制御した。

## Phase 149 — RC3 Narrative ordering

次 Phase は contribution ownership / insertion ordering
（寄与の所有と挿入順序）を扱う。

主要 pressure は、数学的説明の順序として

```text
method / short exact sequence
→ derivation
→ final group conclusion
```

と読むべき箇所で、final conclusion が method contribution より先に現れる場合があること。

Phase 149 では次を守る。

```text
RC2 exposure classification
→ 変更しない

proof graph
→ 変更しない

theorem facts
→ 追加しない

depth semantics
→ 変更しない

ordering / placement
→ 必要最小限の一般規則だけを追加
```

$\pi_6^3$ の historical prose を直接 special case として復元するのではなく、
Argument、transition、contribution ownership から導ける ordering rule を監査する。

## その後

Phase 146 の root-cause 順序を維持する。

```text
RC3 → RC4 → RC5 → RC6
```

- RC3: Contribution ownership / insertion ordering
- RC4: Generic provenance / reason prose
- RC5: EHP semantic naming
- RC6: Final equation numbering / prose formatting

下流の formatting を先に固定せず、selection / ownership / ordering の意味構造を先に確定する。
"""

PROOF_APPEND = r"""

---

# Phase 148 recursive exactness exposure / provenance record

Phase 148 は新しい Toda の数学的 theorem fact を追加した Phase ではない。

対象は Phase 146 で RC2 と分類した

```text
Recursive exactness evidence exposure
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

Phase 148 の exposure classification は、既存 provenance を Narrative 本文へ表示するかを
決める presentation rule である。

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

したがって:

```text
Narrative suppression
!= ProofStep deletion

body contribution suppression
!= provenance deletion

exactness exposure class
!= theorem classification

semantic closure
!= new theorem inference
```

## OWNED_PRIMARY provenance

Argument が primary method として所有する exactness component では、
raw exactness window の反復表示を抑制しつつ、所有された method の説明に必要な
higher-level contribution を利用できる。

```text
raw window suppression
!= exactness fact deletion
```

## UNOWNED_RECURSIVE provenance

recursive dependency として存在するだけの exactness evidence は、
Narrative body へ自動展開しない。

この規則は raw exactness window だけでなく、その component から生成される
derived short exact sequence contribution にも適用する。

```text
UNOWNED_RECURSIVE
→ body contributions = ()

provenance
→ preserved
```

## Web bounded replay provenance

Phase 148 の監査で、Web Narrative が selected depth より complete replay を利用し、
深い recursive exactness evidence を本文へ持ち込んでいたことを確認した。

修正後:

```text
selected bounded replay
→ semantic closure
→ Narrative
```

とする。

semantic closure は既存 proof ancestry から表示に必要な dependency を補うだけである。

depth 0:

```text
closure = identity
```

positive depth の order calculation:

```text
ORDER relation
→ direct EQUALITY premise
→ direct EQUALITY premises of that equality
```

既存 registered definition closure は維持する。

## six-group audit record

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

最終 RC2-4 audit:

```text
all bounded below complete = True
all closure-added exactness = 0
all visible raw exactness = 0
all ambiguous exposure = 0
```

これは raw exactness が proof graph から消えたことを意味しない。
Narrative body への exposure が抑制されたことを意味する。

## final regression record

focused:

```text
92 passed in 36.15s
```

canonical repository regression:

```text
pytest -q tests

10398 passed
3 failed
1316.54s (0:21:56)
```

3 failures は Phase 148 repair 中に誤変更された
`tests/test_phase144_6_pi6_generic_production_route.py`
の historical generic-route contract に限定された。

GitHub `develop` の現行 contract へ復元後:

```text
4 passed in 1.71s
```

repository-wide suite は再実行していない。

したがって final provenance record は、

```text
whole-suite measured evidence
+
focused stale-contract restoration evidence
```

として保持する。

## next-phase boundary

Phase 149 / RC3 は Narrative ordering を扱う。

```text
RC2:
what exactness evidence is exposed

RC3:
where exposed contributions are placed
```

Phase 148 では ordering rule を先取りしない。
"""

APPENDS = {
  Path("README.md"): README_APPEND,
  Path("docs/design.md"): DESIGN_APPEND,
  Path("docs/development_log.md"): DEVLOG_APPEND,
  Path("docs/roadmap.md"): ROADMAP_APPEND,
  Path("docs/proof_records.md"): PROOF_APPEND,
}


def main() -> int:
  missing = [
    str(path)
    for path in FILES
    if not path.exists()
  ]
  if missing:
    raise FileNotFoundError(
      "missing documentation files: "
      + ", ".join(missing)
    )

  output_root = Path(
    "phase148_rc2_5_documentation_closure"
  ) / "updated_full_documents"

  for path in FILES:
    text = path.read_text(encoding="utf-8")
    marker = APPENDS[path].strip().splitlines()[0]

    if marker in text:
      print(
        f"Already updated: {path}"
      )
    else:
      text = text.rstrip() + APPENDS[path] + "\n"
      path.write_text(
        text,
        encoding="utf-8",
      )
      print(
        f"Updated: {path}"
      )

    destination = output_root / path
    destination.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      path,
      destination,
    )

  print("")
  print(
    "Full updated documentation copied to:"
  )
  print(
    output_root
  )
  print(
    "Production changes: none."
  )
  print(
    "Test changes: none."
  )
  print(
    "Repository-wide pytest: NOT rerun."
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
