# Phase 173 R4-R15R8 設計書

## 目的

R4-R15R7 が独立の引用と二つの先行 DB 群から導いた抽象群の証明を、一般の Group Query が使用する `PartialProofResult` に添付する。

数学的な結論は `TodaProp44AbstractGroupResult` であり、登録済みの生成元名を含む `Relation` とは別の型である。単なる型変換や見かけ上の構造一致によって記名群の証明を完成にしてはならない。

## 数学的前提

Toda Proposition 4.4 と `H(ν_4)=ι_7`（Lemma 5.4）から、先行結果を採用する条件下で

$$
\pi_{k+4}^{4}\cong\pi_{k+3}^{3}\oplus\pi_{k+4}^{7}\quad(k\ge 3)
$$

を用いる。`k=31` の登録群について抽象不変量は `(('finite',2),)*8`。`k=31` の登録生成元8個の等式は未証明のまま保持する。

## 変更範囲

1. `phase165_r52_partial_proof.py` — 新規 `CertifiedAbstractStructure` と `PartialProofResult.abstract_structure`。ルートの推論規則を再検証し、記名証明の `COMPLETE` や `KNOWN` との混同を拒否する。
2. `phase165_r55_nk_only_goal.py` — 既存の `search_group_from_registered_goal` の戻り値のうち、`n=4,k>=3` で未完成のものだけに付随結果を添える。特定の `k` の列挙はしない。
3. 新規 `phase173_r4_r15r8_public_abstract_sidecar/attach.py` — R15R7 の実証明からのみ `CertifiedAbstractStructure` を生成する。証明未発見時は従来結果をそのまま返す。
4. 同パッケージ内の Source Guard、変更実行・復元スクリプト、限定テスト、監査レポート。

## 不変条件

- 既存の `ProofSearchStatus`、`GroupStructureStatus`、`conclusion`、`open_goals`、`diagnostics` を変更しない。
- `ABSTRACT_CERTIFIED` を `GENERATOR_NAMED_COMPLETE` に変換しない。
- Source-first の文献引用・先行群・Hopf 条件の検証を一切省略しない。
- 生成元対応の新しい GIVEN を作らない。
- Renderer と Web の `generic-complete-proof` 判定を変更しない。
- `n!=4` または `k<3`、不一致の入力、出典が不足する入力では従来結果を返す。
- HEAD とソースが審査時と異なれば実装を拒否する。

## テストと Phase 境界

DryRun は変換の静的試験のみ。通常実行では R15R7、R15R6 と既存一般 Core の限定 pytest を実施し、`k=31` の実証明を `PartialProofResult` に添付した場合も未完成のままであることを確認する。監査では、人工的な未完成結果だけでなく `search_group_from_registered_goal` の実経路を `n=4,k=31` で呼び出し、抽象証明が添付され記名証明の `complete` に誤昇格しないことを確認する。

本 R15R8 は公開検索**結果型**への接続まで。Web Narrative に新しい専用表示経路を作ることは対象外。R15R9 以降で共通 Renderer の一般的な抽象証明表示を検討する。全体 pytest は Phase 173 最後に実施する。
