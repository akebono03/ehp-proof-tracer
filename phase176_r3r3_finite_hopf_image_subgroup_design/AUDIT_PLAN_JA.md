# Phase 176 R3R3 — Finite Hopf Image-Subgroup Design Audit

## 目的

(n,k)=(3,5) の `CyclicStructureStatement`（生成元 $\nu'\eta_6\eta_7$、位数 2）について、既存の Hopf 持ち上げ一般規則が対象とする型・前提と、今回必要な **真部分群を像とする Hopf 単射**との境界を記録する。今回、証明を生成・完成しない。

## 重要な先行実装

`phase175_r3_pi73_hopf_lift/rule.py` に既存の一般推論 `injective Hopf preimage of a finite cyclic generator is cyclic` が実装されている。従って「有限巡回生成元規則そのものが存在しない」という判断は正しくない。ただしこの規則は終域全体の有限巡回位数が源の結論位数に一致することを要求する。

今回の Toda Proposition 5.9 の証明では、$\pi_8^5=\mathbb Z/8\{\nu_5\}$ に対し、$\operatorname{im}H=\ker\Delta=\mathbb Z/2\{\eta_5^3\}$ が真部分群である。終域の位数 8 と像の位数 2 を混同しない。

## 実行時監査

- 既存の登録 Goal と Open Goals を観測する。
- 先行完成群の DB 表示を観測するが、それを直接 GIVEN に変換しない。
- Phase 175 の一般持ち上げ規則の位数ガード、候補を観測する。
- $E:\pi_7^2\to\pi_8^3$ の像が零なら Hopf 単射性が出る一般規則と、零群からの別ルートを区別する。
- `Proposition 2.2` と `(5.3)` に対応する Hopf 像、および $\ker\Delta$ の位数 2 の部分群を生成元で同一視する義務を分ける。
- テスト用の表現候補は **仮定した表現であり、証明済みの Relation ではない** として記録する。

## 実装の境界

この R3R3 は read-only（既存ファイルを変更しない）。源・目標を直接 GIVEN に追加しない。新規数学規則を導入しない。既存の R56 自由巡回証明や Phase 175 R3 の有限巡回規則を置き換えない。全体 pytest は Phase 176 終了時だけ。Phase 174 Source Guard の既知4失敗は変更せず、未解決として保持する。
