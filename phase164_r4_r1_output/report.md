# Phase 164 R4-R1 — 2前提の実台帳対応監査

## 判定

- 文献名・原本転記 Statement ID の候補を2件特定した。
- これは数学的な型一致・命題同値性・引用資格の承認ではない。
- source publication position は TeX 内の順序であり原本掲載順ではない。
- 実 Registry の typed assertion との接続は未確立。R3 の実データ実行は行わない。

## 前提ごとの対応候補

### prop51_finite_dimensional

- 既存 ProofStep 結論型: `TodaProp51FiniteDimensionalStatement`
- 登録出典: `Proposition 5.1`
- Statement ID: `toda:tex:ch5:0002`
- Reference ID: `toda:Proposition 5.1`
- TeX: `Toda_05_2.tex` 193行
- TeX の掲載順: 78（原本掲載順未確認）
- 祖先ステップ: 40、GIVEN 根: 17
- 判定: LOCATOR_CANDIDATE_ONLY。数学的な対応証明と引用資格の独立検証が必要。

### nu_prime_hopf

- 既存 ProofStep 結論型: `Relation`
- 登録出典: `(5.3)`
- Statement ID: `toda:tex:ch5:0005`
- Reference ID: `toda:(5.3)`
- TeX: `Toda_05_2.tex` 349行
- TeX の掲載順: 81（原本掲載順未確認）
- 祖先ステップ: 28、GIVEN 根: 14
- 判定: LOCATOR_CANDIDATE_ONLY。数学的な対応証明と引用資格の独立検証が必要。

## 次に必要な証拠

1. Proposition 5.1 の複合的な主張と `TodaProp51FiniteDimensionalStatement` の各成分を対応付ける。
2. (5.3) の `H(ν′)=η₅` と `Relation` を構造的に対応付ける。
3. 文献原本の確認、命題の利用可能位置、独立した数学的検証を記録する。
4. 既存の推論祖先が固定結果を展開したものか確認し、文献参照と内部証明を混同しない。

## 境界

Phase 164 R4-R1 は読み取り専用。Production、Registry、ProofStep、Renderer の変更はない。
全体 pytest は Phase 164 の最後のみ。
