# Phase 144-4 π₆³ legacy vs generic 残存差分監査

## 目的

Phase 139〜143 で構築した generic Narrative engine を作り直さず、
現在の legacy π₆³ Narrative と generic π₆³ proof text の差を機能単位で分類する。

分類:

- A: Phase 143 までに一般化済み。generic で表示可能。
- B: generic renderer の表示規則に残存不足がある。
- C: legacy にしかないが、不要または基準出力にも確認できない。
- D: 数学的情報が generic Semantic / Argument structure に届いていない疑い。

## 実行概要

- presentation nodes: 36
- narrative blocks: 25
- legacy chars: 3809
- generic chars: 2100

## 分類結果

| 機能 | 分類 | 判定理由 |
|---|---|---|
| Definition | **B** | legacy には表示され、generic semantic structure に関連情報もある。generic renderer 側の残存不足候補。 |
| Toda theorem / lemma references | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| EHP exact sequence | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| Calculation process | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| Order determination | **B** | legacy には表示され、generic semantic structure に関連情報もある。generic renderer 側の残存不足候補。 |
| Short exact sequence | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| Group structure | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| Equation numbering and references | **B** | legacy の presentation 機能。数学的事実の欠落ではなく generic renderer の一般表示規則として検討する。 |
| Paragraph flow / connective prose | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |
| Final conclusion | **A** | generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。 |

## 各監査項目

### Definition

- 分類: **B**
- 観点: ν′ の定義が generic structure / renderer に届いているか。
- 判定: legacy には表示され、generic semantic structure に関連情報もある。generic renderer 側の残存不足候補。

### Toda theorem / lemma references

- 分類: **A**
- 観点: 定理・補題の provenance が semantic structure にあり、本文に表示されるか。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### EHP exact sequence

- 分類: **A**
- 観点: EHP 完全列そのものの表示。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### Calculation process

- 分類: **A**
- 観点: 2η₃=0, 2ν′=η₃³ などの計算過程。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### Order determination

- 分類: **B**
- 観点: ν′ の位数 4 の決定。
- 判定: legacy には表示され、generic semantic structure に関連情報もある。generic renderer 側の残存不足候補。

### Short exact sequence

- 分類: **A**
- 観点: 完全性と写像の性質から得る短完全列。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### Group structure

- 分類: **A**
- 観点: π₆³ = Z/4{ν′} の最終群構造。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### Equation numbering and references

- 分類: **B**
- 観点: 式番号の付与と本文からの参照。semantic role から一般化すべき表示機能。
- 判定: legacy の presentation 機能。数学的事実の欠落ではなく generic renderer の一般表示規則として検討する。

### Paragraph flow / connective prose

- 分類: **A**
- 観点: 数学書としての段落構成・接続語。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

### Final conclusion

- 分類: **A**
- 観点: 証明の最終結論。
- 判定: generic renderer ですでに表示可能。本番経路で使われていない／legacy と表現差があるかを確認する。

## Phase 144-5 への入力

Phase 144-5 では、この監査で **B / D** に分類された項目だけを修正対象候補とする。
A は再実装しない。C は必要性を確認するまで実装しない。

特に、群座標 `n == 3 and k == 3` による本番 renderer の追加分岐は禁止する。
