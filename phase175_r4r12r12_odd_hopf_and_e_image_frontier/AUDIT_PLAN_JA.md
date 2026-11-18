# Phase 175 R4R12R12 — 監査計画

## 監査前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` にある以下の現行コード・関連テストを確認した。

- `phase175_r4r3_two_summand_quotient/rule.py`：6前提の一般商群規則。
- `phase175_r4r12_public_two_summand_quotient/provider.py`：Orientation 0/1 の独立候補。
- `phase165_r12_r12_ehp_consequences.py`：零 Hopf 標的からの E 全射性候補。
- `phase169_r10e5_composite_generator_image/rule.py`：合成の E 像を2因子に分解する既存規則。
- `phase169_r10d2_general_family_definition/family_citation.py`：引用済み ν-family の定義と生成元像。
- `phase175_r4r12r11_ehp_surjectivity_frontier/tests/test_audit.py`：直前の監査テスト。

## 変更対象

既存ファイル・import・クラス・関数・テストは変更しない。リポジトリ直下に新規ディレクトリ `phase175_r4r12r12_odd_hopf_and_e_image_frontier/` を設置し、以下を追加する。

- `audit.py`：`git()`、`inspect()`、`run()`、`main()` を新規追加。
- `tests/test_audit.py`：4件の限定テストを新規追加。
- `run.ps1`：PowerShell エントリ。
- `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 数学的検討

EHP 完全性（Proposition 4.2）により、$\operatorname{im} E=\ker H$ である。今回の $H:\pi_9(S^5)\to\pi_9(S^9)\cong\mathbb{Z}$ は通常の整数係数 Hopf invariant と整合する可能性があり、奇数 $n$ に対する一般定理 $H:\pi_{2n-1}(S^n)\to\mathbb{Z}$ が零写像であることが有力な経路である。これは graded commutativity と torsion-free な $H^{2n}$ から導かれる。

参考資料：Dugger, *A Geometric Introduction to K-Theory*（公開講義ノート）および *Encyclopedia of Mathematics*, Hopf invariant。元の Toda 本文の定理同定・公理登録はこの監査では行わない。

既存の E 全射性候補は $\pi_9(S^9)=0$ を要求するため、この具体例では不正な前提を伴う。これは規則一般の誤りと断定せず、不適用候補として記録する。

E 生成元像は $E(\nu_4\circ\eta_7)=\nu_5\circ\eta_8$ への候補を既存の合成規則で2因子に分解し、それぞれの Provider 候補数を調べる。推論の完成を主張しない。

## 完了条件と境界

DryRun・本実行で `PASS_R12_ODD_HOPF_AND_E_IMAGE_FRONTIER_NOT_COMPLETE` を得て、Orientation ごとの因子候補を JSON 出力する。新規 GIVEN 0、数学規則 0、既存本体変更 0、全体 pytest なし。次段階では典拠と型を精査した一般的な奇数次元 Hopf 零性の接続可能性を検討する。
