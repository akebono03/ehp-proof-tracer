# Phase 163 R4-R53 数学的重複・包含の境界監査

R4-R47 のスナップショットは Reference/Assertion の ID を含むが、各 Assertion の型付き数学的内容を含まない。
従って、数学的同値・包含・重複の判定はできず、同じ TeX 掲載単位への所属のみを検査する。

## 集計

- 定義候補: 19 件
- CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE: 3 件
- NO_DIRECT_CATALOG_UNIT: 16 件
- 数学的内容の重複未判定: 19 件
- 新規 Statement 確定: 0 件

## 同一 TeX 掲載単位の候補

- 第2章 L926 delta_homomorphism → (2.9) (tex-unit:toda:ch02:0013) / CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE
- 第2章 L935 inverse_delta → (2.10) (tex-unit:toda:ch02:0014) / CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE
- 第4章 L92 pi_i_n_subgroup → (4.3) (tex-unit:toda:ch04:0003) / CATALOG_UNIT_WITHOUT_EXISTING_REFERENCE

## 判断境界

TeX 掲載単位の一致は Assertion の内容的同値を示さない。
対応 Assertion ID を推測しない。既存 ID の改変・本番台帳への登録・証明探索接続を行わない。
237件の未判定候補、原本未照合状態を維持する。全体 pytest は行わない。
