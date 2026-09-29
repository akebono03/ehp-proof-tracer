from pathlib import Path
import shutil

README = Path("README.md")
DESIGN = Path("docs/design.md")
DEVLOG = Path("docs/development_log.md")
ROADMAP = Path("docs/roadmap.md")
PROOF = Path("docs/proof_records.md")

for path in (README, DESIGN, DEVLOG, ROADMAP, PROOF):
  if not path.is_file():
    raise RuntimeError(f"Required document not found: {path}")

def read(path):
  raw = path.read_bytes()
  bom = raw.startswith(b"\xef\xbb\xbf")
  newline = "\r\n" if b"\r\n" in raw else "\n"
  text = raw.decode("utf-8-sig").replace("\r\n", "\n")
  return text, bom, newline

def write(path, text, bom, newline):
  if not text.endswith("\n"):
    text += "\n"
  if newline == "\r\n":
    text = text.replace("\n", "\r\n")
  path.write_text(
    text,
    encoding="utf-8-sig" if bom else "utf-8",
    newline="",
  )

def replace_if_present(text, old, new):
  if old in text:
    return text.replace(old, new)
  return text

def append_once(text, marker, section):
  if marker in text:
    return text
  return text.rstrip() + "\n\n" + section.strip() + "\n"

text, bom, nl = read(README)
text = replace_if_present(
  text,
  "- safe rule-name or type-name fallback when no explicit mathematical or presentation label is available,",
  "- semantic Narrative rendering for the audited proof-statement inventory, with no rule-name fallback remaining in the Phase 143 completion audit,",
)
text = replace_if_present(
  text,
  "- safe mathematical rendering with explicit fallback for unsupported aggregate statements.",
  "- semantic mathematical rendering for the audited Narrative statement inventory, while preserving proof provenance and avoiding invented mathematical prose.",
)
text = replace_if_present(
  text,
  "Narrative uses fixed deterministic templates over the same graph. Unsupported statements use safe existing renderers or rule/type fallbacks instead of inventing mathematical prose.",
  "Narrative uses deterministic presentation rules over the same proof graph. Phase 143 moved the audited proof-statement inventory from internal rule-name fallback toward first-class semantic statement rendering. The completion audit found no remaining rule-name fallback in the audited current-entrypoint Narrative output.",
)
text = replace_if_present(
  text,
  "Latest repository-wide regression:\n\n```text\n9517 passed in 575.31s (0:09:35)\n```",
  "Latest repository-wide regression:\n\n```text\n9980 passed in 807.31s (0:13:27)\n```",
)
readme_section = r'''## Phase 143 closure

Phase 143 generalized Narrative presentation away from internal rule-name fallback and toward semantic mathematical rendering backed by stored proof statements.

The phase did not add new Toda theorems, change the proof graph, or introduce a second proof engine. Instead, it audited the statement structures already carried by proof steps and added or refined semantic rendering for those structures.

Representative semantic output now includes mathematical content such as:

$$
\Delta(\iota_{13})
\in
\{\nu_6,\eta_9,2\iota_{10}\}
\pmod{2\pi_{11}^{6}},
$$

$$
\ker\left(
\Delta:\pi_8^5\to\pi_6^2
\right)
=
\mathbb Z/2\{4\nu_5\},
$$

and the transported decomposition

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}.
$$

The Narrative layer preserves the distinction between a transported decomposition and the final standard-order group statement

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}.
$$

It also preserves direct-premise relocation behavior such as the single, dependency-ordered occurrence of

$$
2\nu_5=E^2\nu'.
$$

Phase 143 completion checks:

```text
Focused regression:
33 passed in 20.96s

Current-entrypoint completion audit:
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0

Repository-wide final regression:
9980 passed in 807.31s (0:13:27)
```

The Phase 143 boundary is presentation semantics only:

```text
semantic Narrative rendering
!= new theorem fact
!= new proof edge
!= proof search
!= operation evaluation
!= theorem ranking
```'''
text = append_once(text, "## Phase 143 closure", readme_section)
write(README, text, bom, nl)

text, bom, nl = read(DESIGN)
text = replace_if_present(
  text,
  "safe fallback != 推測した数学的説明",
  "semantic renderer != 新しい数学的事実\nrule-name fallback 除去 != proof semantics 変更\nsafe fallback != 推測した数学的説明",
)
design_section = r'''# Phase 143 semantic Narrative 設計

Phase 143 では Narrative の数学的表示を、内部 `rule.name` に依存した fallback から、`ProofStep.conclusion` が保持する semantic statement の構造を読む表示へ移行した。

基本経路は次のとおり。

```text
ProofStep
→ conclusion semantic statement
→ statement fields / relation / membership / group structure
→ semantic LaTeX renderer
→ Narrative block / argument renderer
→ multi-argument Narrative
```

重要な境界:

```text
semantic statement
!= 新しい theorem fact

semantic renderer
!= inference rule

semantic rendering
!= proof search

Narrative ordering
!= proof graph mutation

rule-name fallback elimination
!= provenance elimination
```

Phase 143 の完了監査では、現行の

```text
_method_evidence_data(n, k)
→ presentation / blocks / sidecar / arguments
→ render_toda_group_proof_narrative_multi_argument_markdown()
```

という実際の Narrative 入口を使用した。

監査結果:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

したがって、Phase 143 で監査した current-entrypoint Narrative については、内部 rule-name fallback を通常の数学表示として残さないことを現在の不変条件とする。

## semantic statement と dependency の役割分離

statement が nested theorem / bridge / short exact sequence 等を dependency として保持していても、親 statement の renderer が dependency の数学的内容を勝手に再構成してはならない。

```text
statement の直接 semantic fields
→ statement 自身の表示

dependency ProofStep
→ proof graph / Narrative ordering

dependency の存在
!= 親 statement の追加数学的結論
```

この原則により、保存された fields に零端点がない短完全列を renderer が推測して補う、といった表示上の theorem synthesis を避ける。

## direct premise suppression / relocation / preservation

Phase 143 終盤では、semantic statement の表示と既存の Narrative 重複抑制・relocation の境界を整理した。

特に direct premise は次の分類を混同しない。

```text
redundant direct premise
relocatable direct premise
context-hidden step
DERIVATION source block として保持すべき semantic premise
```

`context_hidden_step_ids` は引き続き最優先で非表示とする。

一方、DERIVATION source block として保持対象になった block 内の `redundant_direct_premise_step_ids` は、semantic な導出根拠そのものを失わないため表示を保持できる。

ただし `relocated_direct_premise_ids` の suppression は一律に解除しない。これにより、例えば

$$
2\nu_5=E^2\nu'
$$

は元位置と relocation 先に二重表示されず、既存の依存順序に従って一度だけ表示される。

また

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

という transported decomposition は、その後の標準順序

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

とは異なる導出上の意味を持つため、両方を保持する。

```text
transported decomposition
!= final standard-order conclusion

semantic preservation
!= duplicate preservation

relocation
!= deletion of proof provenance
```

Phase 143 は presentation semantics の改善であり、Toda の新しい数学定理、group-query semantics、operation evaluator、proof search algorithm は追加していない。'''
text = append_once(text, "# Phase 143 semantic Narrative 設計", design_section)
text = replace_if_present(
  text,
  "最新 repository-wide regression:\n\n```text\n9517 passed in 575.31s (0:09:35)\n```",
  "最新 repository-wide regression:\n\n```text\n9980 passed in 807.31s (0:13:27)\n```",
)
write(DESIGN, text, bom, nl)

text, bom, nl = read(DEVLOG)
dev_section = r'''# Phase 143 完了記録

Phase 143 は、Phase 139 以降に進めてきた「専用 Narrative ではなく、一般的な semantic structure から数学的証明文を生成する」方向を、横断的な statement inventory 監査まで進めた Phase である。

主目的:

```text
internal rule-name fallback
→ semantic statement structure
→ mathematical Narrative rendering
```

Phase 前半では既存 Narrative の statement / block / argument 構造を監査し、後半では fallback に残っていた statement type を順次 semantic renderer へ接続した。

代表的な対象には次が含まれる。

```text
Toda56Nu4Prop44SpecializationStatement
TodaLemma54WhiteheadCorrectionDataStatement
TodaLemma54HopfOddMultipleStatement
TodaLemma54DoubleSuspensionUpToSignStatement
TodaSuspensionZeroStatement
TodaProp44FirstSummandRestrictionStatement
TodaLemma510BracketModuloStatement
TodaLemma57TwoIota5ImageMembershipStatement
TodaProp59DeltaKernelStatement
Toda36Lemma54SpecializationStatement
TodaLemma514SigmaDoublePrimeStatement
Toda514FirstShortExactStatement
Toda514SecondShortExactStatement
Toda54IndeterminacyGeneratorStatement
FiniteHomotopyGroupStatement
Toda211OrdinaryEHPExactnessStatement
TodaLemma510HopfBracketContainsStatement
TodaLemma510IndexedHopfBracketContainsStatement
TodaLemma510Split115Statement
TodaLemma510OrdinaryBracketPlusSuspensionImageStatement
TodaLemma510OrdinarySuspensionImageFiniteStatement
TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement
TodaLemma510OrdinarySuspensionImageInDoubleStatement
TodaLemma510OrdinaryIndeterminacyDoubleStatement
TodaLemma510Nu6OrdinaryCompositionZeroStatement
Toda211OrdinaryEHPApplicabilityStatement
TodaLemma510Nu6OrdinaryCompositionReductionStatement
Toda515Sigma8TransportedDecompositionStatement
Toda515Sigma8Prop44SpecializationStatement
```

終盤では、semantic statement を表示可能にしたことで既存の duplicate suppression / direct-premise relocation と競合する箇所を監査した。

特に $\pi_{15}^{8}$ では transported decomposition

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

と final standard-order conclusion

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

を両方保持する必要があることを確認した。

一方 $\pi_8^5$ の

$$
2\nu_5=E^2\nu'
$$

は relocatable direct premise として既存の適切な位置へ移動し、一度だけ表示する必要がある。

最終修正では群名や statement type の専用分岐を追加せず、

```text
preserved DERIVATION source block
AND
redundant direct premise
```

という既存の構造分類を利用して semantic premise の保持範囲を限定した。`relocated_direct_premise_ids` の suppression は維持した。

focused regression:

```text
33 passed in 20.96s
```

現行 Narrative entrypoint completion audit:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

Phase 143 最終 repository-wide regression:

```text
9980 passed in 807.31s (0:13:27)
```

結果:

```text
Phase 143 完了
```

Phase 143 では proof graph、Toda theorem fact、group-query semantics、operation-query semantics、proof search semantics は変更していない。

次 Phase では、この semantic Narrative 基盤を前提として、証明文章全体の一般性・自然さ・依存関係の見せ方を改めて監査する。Phase 143 で解消した rule-name fallback を再導入してはならない。'''
text = append_once(text, "# Phase 143 完了記録", dev_section)
write(DEVLOG, text, bom, nl)

text, bom, nl = read(ROADMAP)
road_section = r'''# Phase 143 完了後のロードマップ

## 現在地

Phase 143 完了。

確定した基盤:

```text
group result
→ existing ProofStep provenance
→ presentation graph
→ argument / block structure
→ semantic statement rendering
→ Narrative
```

Phase 143 completion audit:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

final regression:

```text
9980 passed in 807.31s (0:13:27)
```

## Phase 144

次 Phase は、Phase 143 で semantic rendering を整備した Narrative を**証明全体として読む監査**から開始する。

優先事項:

1. $\pi_6^3$ で得た自然な証明文と、一般 semantic rules から生成される他群の Narrative を比較する。
2. statement 単体が数式化されていても、証明全体の順序・接続語・依存関係が数学書として不自然でないか確認する。
3. 専用 prose を増やす前に、block role、argument transition、direct premise、dependency reuse など既存の一般構造で改善できるか確認する。
4. Phase 143 で達成した rule-name fallback 0 を維持する。
5. 新しい数学的 theorem fact や proof-search capability が本当に必要になるまでは追加しない。

Phase 144 の開始時点では、実装を先取りしない。まず代表群を横断監査し、共通の presentation pressure が確認できた場合だけ最小変更を行う。

## その後の候補

Phase 144 以降、実際の利用圧が確認できたものから順に検討する。

```text
Narrative の theorem / lemma 参照から既存証明への navigation
Web 上の参照クリックによる proof replay
より広い群での自然な Narrative 品質監査
7-stem 全体の proof-backed coverage 監査
必要に応じた proof presentation graph の可視化
```

これらは Phase 143 の完了条件には含めない。

特に theorem / lemma reference の clickable navigation は有用な将来候補だが、

```text
reference navigation
!= proof inference
!= theorem ranking
!= new proof search
```

として presentation / navigation 層に限定して設計する。

## 維持する境界

```text
free part + 2-primary focus
odd-primary full integration は deferred
general E/H/Delta evaluator は未実装
general Toda bracket solver は未実装
unbounded proof search は未実装
theorem ranking は未実装
free-form LLM proof generation は採用しない
```'''
text = append_once(text, "# Phase 143 完了後のロードマップ", road_section)
write(ROADMAP, text, bom, nl)

text, bom, nl = read(PROOF)
proof_section = r'''# Phase 143 semantic Narrative provenance record

Phase 143 は新しい数学的証明を追加した Phase ではない。

目的は、既存 `ProofStep` が保持する statement の semantic structure を Narrative で可視化し、内部 rule name を数学的説明の代用として表示する箇所を解消することだった。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing proof ancestry
```

である。

Phase 143 の renderer は `ProofStep.conclusion` の型と保存済み fields を読む。

```text
stored semantic field
→ rendering source

renderer-generated inference
→ 禁止
```

したがって、保存されていない零端点、同型、単射性、位数、完全性などを renderer が推測して追加してはならない。

## representative semantic records

Toda Lemma 5.10 の bracket modulo statement:

$$
\Delta(\iota_{13})
\in
\{\nu_6,\eta_9,2\iota_{10}\}
\pmod{2\pi_{11}^{6}}.
$$

Toda Proposition 5.9 の kernel statement:

$$
\ker\left(
\Delta:\pi_8^5\to\pi_6^2
\right)
=
\mathbb Z/2\{4\nu_5\}.
$$

Toda Lemma 5.14 / Proposition 5.15 周辺では、保存された semantic relation、membership、Hopf relation、group decomposition を個別に表示する。

## transported decomposition provenance

$\pi_{15}^{8}$ の証明では transported decomposition

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

と final standard-order conclusion

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

は同じ文字列の重複ではない。

前者は導出途中の semantic decomposition、後者は最終的な標準順序の群表示である。

したがって:

```text
transported decomposition
→ preserve as derivation evidence

final group statement
→ preserve as conclusion
```

とする。

## direct-premise relocation provenance

$\pi_8^5$ の

$$
2\nu_5=E^2\nu'
$$

は依存関係に従って結論側へ relocation される direct premise である。

Phase 143 終盤の修正では、この premise を元位置にも復活させて二重表示することを避けた。

```text
relocated premise
→ one semantic occurrence in Narrative

Narrative relocation
!= ProofStep relocation
!= proof edge mutation
```

## completion audit

現行の実利用入口:

```text
_method_evidence_data(n, k)
→ presentation / blocks / sidecar / arguments
→ render_toda_group_proof_narrative_multi_argument_markdown()
```

を使用した completion audit:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

focused regression:

```text
33 passed in 20.96s
```

repository-wide final regression:

```text
9980 passed in 807.31s (0:13:27)
```

この結果を Phase 143 の provenance / presentation 完了境界とする。

```text
semantic Narrative
!= new proof

rule-name fallback 0
!= theorem completeness

render error 0
!= all mathematical statements proved

Narrative preservation / suppression / relocation
!= proof graph mutation
```'''
text = append_once(text, "# Phase 143 semantic Narrative provenance record", proof_section)
write(PROOF, text, bom, nl)

out = Path("phase143_docs_completion") / "updated_full_documents"
if out.exists():
  shutil.rmtree(out)
(out / "docs").mkdir(parents=True)

shutil.copy2(README, out / "README.md")
shutil.copy2(DESIGN, out / "docs" / "design.md")
shutil.copy2(DEVLOG, out / "docs" / "development_log.md")
shutil.copy2(ROADMAP, out / "docs" / "roadmap.md")
shutil.copy2(PROOF, out / "docs" / "proof_records.md")

print("Phase 143 documentation completion update applied.")
print("Full updated documents exported under:")
print("  phase143_docs_completion\\updated_full_documents")
