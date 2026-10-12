# Phase 164 R4-R2 — 数学的内容の構造照合

## 結論

- Proposition 5.1 の既存4フィールドを原文の部分表現と対応検査した。
- (5.3) の Relation について Hopf 写像・両辺の型と source/target を検査した。
- 文字列トークン存在は数学的な意味一致の証明ではない。
- TeX の掲載順は原本版の掲載順の認定ではない。
- typed assertion の本登録、引用資格の承認、Backward Search の本接続は行わない。

## Proposition 5.1

- Statement ID: `toda:tex:ch5:0002`

- `pi3_2_group_relation`: 型 `Relation`、構造存在=True、出典トークン一致=True
- `eta2_hopf_relation`: 型 `Relation`、構造存在=True、出典トークン一致=True
- `delta_iota5_relation`: 型 `TodaDeltaImageUpToSignStatement`、構造存在=True、出典トークン一致=True
- `higher_eta_group_relation`: 型 `Relation`、構造存在=True、出典トークン一致=True
- 安定群 $(G_1;2)$ の記述は原文に含まれる: True
- この安定群の節を4成分のいずれかと同一視しない。

## (5.3)

- Statement ID: `toda:tex:ch5:0005`
- 型 `Relation`、`EHP_H_MAP`、$\nu'\in\pi_6^3$、$H(\nu')=\eta_5$ の構造を検査。
- (5.3) の $2\nu'=\eta_3\eta_4\eta_5$ は別の主張であり、この Relation に含めない。

## 継続条件

- 原本確認と数学的な同値性の独立監査を実施する。
- 利用可能位置を確定する。
- 必要な場合だけ typed binding を別 Phase 操作で追加する。
- 全体 pytest は Phase 164 終了時のみ。
