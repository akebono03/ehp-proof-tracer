# Phase 176 R3R2 — 有限巡回 Hopf 生成元の充足性監査

## 目的

Phase 176 R3R1 で実測した `(n,k)=(3,5)` の3件の Open Goals のうち、`CyclicStructureStatement`（位数2の群構造）に共有 Provider が候補を生成しない理由を調査する。数学的規則・GIVEN・既存 Provider・Web Renderer は変更しない。

## 監査対象

- `phase165_r12_r2_quotient_rules.py` の `CyclicStructureStatement`。
- `phase165_r14_r6_generic_iso.py` の `MapInjective`、`GeneratorImage`。
- `phase165_r14_r9_ehp_exactness.py` の Hopf 単射性の一般規則。
- `phase165_r12_r12_ehp_consequences.py` の `EHPImageEqualsKernelStatement`。
- `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py` の自由巡回群専用橋渡し。
- `phase171_r2h_prop22_cited_hopf/source.py` の出典付き Proposition 2.2。
- `phase176_r3_n3_rule_sufficiency_audit` の Goal と出典照合に関する既存監査。

## 数学的義務

Toda Chapter V Proposition 5.9 本文に従い、次の前提を独立に検証する必要がある。

1. Lemma 5.7、Proposition 5.8、(5.2) から $E\pi_7^2=0$。
2. EHP 完全列 (4.4) から $H:\pi_8^3\to\pi_8^5$ の単射性、および $\operatorname{im}H=\ker\Delta$。
3. Lemma 5.7、Proposition 5.6、(5.5) から $\ker\Delta=\mathbb Z/2\{\eta_5^3\}$。
4. Proposition 2.2、(5.3) と $\eta$ family 定義から $H(\nu'\eta_6\eta_7)=\eta_5^3$。
5. 1〜4がそれぞれ ProofStep として検証済みならば、単射写像を通じて位数2の群構造と生成元を持ち上げる一般規則を検討できる。**結論を GIVEN として登録しない。**

## 監査の限界

`MapInjective` の候補数はその前提が証明されたことを意味しない。原文の存在と registry 上の出典リンクも数学的 ProofStep の完成とは異なる。本監査は「不足を発見する」工程であり、位数2の群構造の証明完成を宣言しない。

## 実行と境界

新規ディレクトリのみ追加。全体 pytest は Phase 176 の最後にのみ実行する。旧 Phase 174 Source Guard の4失敗は解消済みと扱わない。検査結果は `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r2_finite_cyclic_hopf_frontier/report.json` に保存する。
