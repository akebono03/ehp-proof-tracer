# Phase 169 R10EO-R2 — Definition Index 監査

採用済み転写 TeX の字面一致を索引化しただけであり、Source Attestation（出典の審査済み認証）ではない。
CSV・字面一致から FIXED_STATEMENT や GIVEN を生成しない。

| ID | 生成元 | k | n0 | 一意な候補 | 出典候補 |
|---:|---|---:|---:|---|---|
| 1 | ι | 0 | 1 | NO_EXACT_TEXT_CANDIDATE | — |
| 2 | η | 1 | 2 | NO_EXACT_TEXT_CANDIDATE | — |
| 4 | ν | 3 | 4 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_v:606 |
| 9 | σ | 7 | 8 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_v:2111 |
| 10 | ε | 8 | 3 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_vi:99 |
| 11 | ν̅ | 8 | 6 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_vi:501 |
| 12 | μ | 9 | 3 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_vi:1309 |
| 16 | ζ | 11 | 5 | UNIQUE_TEXT_CANDIDATE_NOT_AUTHORIZED | chapter_vi:2138 |
| 23 | κ | 14 | 7 | NO_EXACT_TEXT_CANDIDATE | — |
| 25 | ε̅ | 15 | 3 | NO_EXACT_TEXT_CANDIDATE | — |
| 30 | ρ | 15 | 13 | NO_EXACT_TEXT_CANDIDATE | — |
| 34 | ω | 16 | 14 | NO_EXACT_TEXT_CANDIDATE | — |
| 36 | η* | 16 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 38 | μ̅ | 17 | 3 | NO_EXACT_TEXT_CANDIDATE | — |
| 40 | ε* | 17 | 12 | NO_EXACT_TEXT_CANDIDATE | — |
| 46 | ξ | 18 | 12 | NO_EXACT_TEXT_CANDIDATE | — |
| 48 | ν* | 18 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 50 | ζ̅ | 19 | 5 | NO_EXACT_TEXT_CANDIDATE | — |
| 51 | σ̅ | 19 | 6 | NO_EXACT_TEXT_CANDIDATE | — |
| 56 | κ̅ | 20 | 7 | NO_EXACT_TEXT_CANDIDATE | — |
| 72 | σ* | 22 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 76 | φ | 23 | 5 | NO_EXACT_TEXT_CANDIDATE | — |
| 81 | ρ̅ | 23 | 9 | NO_EXACT_TEXT_CANDIDATE | — |
| 82 | ψ | 23 | 10 | NO_EXACT_TEXT_CANDIDATE | — |
| 85 | ε̅* | 23 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 86 | ν̅* | 23 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 88 | δ | 24 | 3 | NO_EXACT_TEXT_CANDIDATE | — |
| 89 | ζ̅' | 24 | 6 | NO_EXACT_TEXT_CANDIDATE | — |
| 90 | σ̅' | 24 | 6 | NO_EXACT_TEXT_CANDIDATE | — |
| 93 | ֮ε | 24 | 10 | NO_EXACT_TEXT_CANDIDATE | — |
| 97 | μ* | 24 | 16 | NO_EXACT_TEXT_CANDIDATE | — |
| 103 | μ3, | 25 | 3 | NO_EXACT_TEXT_CANDIDATE | — |
| 132 | ζ3, | 27 | 5 | NO_EXACT_TEXT_CANDIDATE | — |
| 174 | θ'_ | 30 | 23 | NO_EXACT_TEXT_CANDIDATE | — |
| 185 | κ* | 31 | 10 | NO_EXACT_TEXT_CANDIDATE | — |
| 188 | ω* | 31 | 14 | NO_EXACT_TEXT_CANDIDATE | — |
| 189 | ρ3, | 31 | 14 | NO_EXACT_TEXT_CANDIDATE | — |
| 219 | μ4, | 33 | 3 | NO_EXACT_TEXT_CANDIDATE | — |
| 223 | κ' | 33 | 6 | NO_EXACT_TEXT_CANDIDATE | — |

## 既存の審査済み Source Record との一致

既存の 5 件について、構造化した字面候補と整合。
既存の SOURCE_RECORDS と CHAPTER_VI_SOURCE_RECORDS は本工程で削除・変更しない。

## 11-stem の実行時監査

- 群: `pi_41^30`
- Status: `partial`
- Open Goal: `CyclicStructureStatement, GeneratorImage, Relation, Relation`
- Trust Boundary: `NOT_APPLICABLE_INCOMPLETE`

## 次工程との境界

次工程で、採用済み文献・命題の掲載位置・定義の適用範囲を検証し、
source attestation を明示した上で初めて既存の Definition GIVEN 経路に接続する。
生成元の名称ごとの推論規則追加は行わない。
完成証明が得られない限り Trust Boundary の PASS を主張しない。

全体 pytest は Phase 最終段階のみ。
