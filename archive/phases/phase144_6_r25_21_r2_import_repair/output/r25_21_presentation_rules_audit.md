# Phase 144-6 R25-21 presentation rules audit

## 目的

旧 $\pi_6^3$ Narrative を presentation specification として分解し、
代表6群の generic production Narrative に不足する一般表示規則を確定する。

この監査は production code を変更しない。

## 旧 $\pi_6^3$ の番号依存構造

- (1), (2) → (3): Lemma 5.2 の仮定から $\nu'\in\pi_6^3$。
- (5), (15) → (16): $2\nu'=\eta_3^3$ と $\operatorname{ord}(\eta_3^3)=2$ から $\operatorname{ord}(\nu')=4$。
- (4), (17) → (18): $H(\nu')=\eta_5$ と $\pi_6^5=\mathbb Z/2\{\eta_5\}$ から $H$ の全射性。
- (8), (14), (18) → (19): EHP 完全列・$E$ の単射性・$H$ の全射性から短完全列。
- (7), (17), (19) および (3), (16) → (20): 群の位数と位数4の生成元から最終群構造。

したがって equation numbering は装飾ではなく Argument dependency の表示である。

## Presentation rule inventory

| rule | legacy $\pi_6^3$ | generic 6群 | 判定 |
|---|---:|---:|---|
| Section structure | yes | 6/6 | **一般化済み** |
| Reference labels [R1], [R2], ... | yes | 6/6 | **一般化済み** |
| Equation number assignment (1), (2), ... | yes | 6/6 | **一般化済み** |
| Equation dependency references | yes | 6/6 | **一般化済み** |
| Argument-level paragraph structure | yes | 0/6 | **不足** |
| Definition deduplication | yes | 0/6 | **不足** |
| Internal derivation suppression | yes | 1/6 | **不足** |
| Localized exactness/map-property prose | yes | 6/6 | **一般化済み** |
| Short exact sequence as a major result | yes | 6/6 | **一般化済み** |
| Explicit final conclusion | yes | 0/6 | **不足** |

## 6群の観測値

| group | chars | equation tags | [R#] labels | adjacent duplicate definitions | raw English map property | internal `22\\nu` |
|---|---:|---:|---:|---:|---:|---:|
| pi_6^3 | 3804 | 11 | 4 | 0 | 0 | 0 |
| pi_8^5 | 4264 | 19 | 4 | 0 | 0 | 3 |
| pi_10^4 | 17049 | 111 | 4 | 0 | 0 | 12 |
| pi_12^5 | 29840 | 186 | 4 | 0 | 0 | 21 |
| pi_15^8 | 31408 | 190 | 4 | 0 | 0 | 21 |
| pi_16^9 | 31491 | 190 | 4 | 0 | 0 | 21 |

## R25-22 以降に実装すべき一般 presentation rules

### P01. Section structure

- key: `section_structure`
- 目的: 証明対象・使用結果・証明本文・結論を視覚的に分離する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P02. Reference labels [R1], [R2], ...

- key: `reference_labels`
- 目的: 外部定理・補題を本文の式番号とは別 namespace で参照する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P03. Equation number assignment (1), (2), ...

- key: `equation_number_assignment`
- 目的: 読者が後続推論で参照する主要式・主要写像性質・最終結論だけに連番を付ける。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P04. Equation dependency references

- key: `equation_dependency_reference`
- 目的: 番号を単に表示するだけでなく、後続 Argument の根拠として参照する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P05. Argument-level paragraph structure

- key: `argument_sections`
- 目的: definition/membership・order・group structure を論証単位の段落として構成する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P06. Definition deduplication

- key: `deduplicate_definitions`
- 目的: 同一 definition を近接箇所で繰り返さず、最初の導入後は参照にする。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P07. Internal derivation suppression

- key: `hide_internal_derivations`
- 目的: 機械的正規化・内部 bookkeeping を主要 Narrative から隠す。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P08. Localized exactness/map-property prose

- key: `localized_map_properties`
- 目的: raw English statement suffix を出さず、日本語の数学文として表示する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P09. Short exact sequence as a major result

- key: `short_exact_sequence`
- 目的: 完全性・単射・全射をまとめ、短完全列を主要式として提示する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

### P10. Explicit final conclusion

- key: `final_conclusion`
- 目的: 最後に target group を明示し、証明本文から結論を分離する。
- 実装原則: 群座標や $\pi_6^3$ 固有条件ではなく、Semantic / NarrativeBlock / NarrativeArgument / contribution の役割から判定する。

## 実装順序案

1. Argument dependency に基づく主要式選択と equation numbering。
2. 番号付き主要式を根拠として参照する dependency prose。
3. Reference [R#] と equation number の namespace 分離。
4. definition / precondition / order / group structure の Argument 段落化。
5. 重複 definition と内部 derivation の抑制。
6. exact/injective/surjective の日本語化と EHP / short exact sequence の主要式化。
7. final conclusion の独立表示。

## Phase boundary

R25-21 は audit only。production source は変更しない。
R25-22 から、この一覧の一般 presentation rules を generic renderer に実装する。
$\pi_6^3$ 専用分岐を新設しない。

## Missing rule keys

argument_sections, deduplicate_definitions, hide_internal_derivations, final_conclusion

