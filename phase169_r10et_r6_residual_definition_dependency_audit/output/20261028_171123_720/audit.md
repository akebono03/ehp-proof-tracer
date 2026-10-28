# Phase 169 R10ET-R6 — 個別 Definition の残存依存監査

AUDIT_ONLY。既存 Proof Tree、命題台帳、Renderer、既存テスト、Git index は変更しない。

- Git HEAD: `232a92883b0cb009762b437cbb3cc550f00ab6bd`
- 本番 R4/R5 ファイル一致: `True`
- Git tracked/index 完全保持: `True`
- 全体 pytest: 実行しない

| 群 | 区分 | 完成/Trust | 共通Definition採用 | 置換可能な引用付き像 | Reference |
|---|---|---|---:|---:|---|
| `pi_69^43` | 必須 | complete / PASS | 30 | 0 | DB prior: sphere.csv (n=28, k=26), (4.5) |
| `pi_56^30` | 必須 | complete / PASS | 4 | 0 | DB prior: sphere.csv (n=28, k=26), (4.5) |
| `pi_41^30` | 必須 | complete / PASS | 17 | 0 | DB prior: sphere.csv (n=13, k=11), (4.5) |
| `pi_44^30` | 必須 | complete / PASS | 28 | 0 | DB prior: sphere.csv (n=16, k=14), (4.5) |
| `pi_46^30` | 必須 | complete / PASS | 24 | 0 | DB prior: sphere.csv (n=18, k=16), (4.5) |
| `pi_39^30` | 必須 | complete / PASS | 57 | 0 | DB prior: sphere.csv (n=11, k=9), (4.5) |
| `pi_3^2` | 必須 | complete / PASS | 0 | 0 | (5.1), Proposition 4.2 (4.4), Foundational: suspension identity, Proposition 5.1 |
| `pi_4^3` | 必須 | complete / PASS | 0 | 0 | Chapter V, i), (5.1), Proposition 5.1, Proposition 4.2 (4.4) |
| `pi_5^4` | 必須 | complete / PASS | 0 | 0 | Chapter V, i), Proposition 5.1, (4.5) |
| `pi_4^2` | 必須 | complete / PASS | 0 | 0 | Proposition 5.1, (5.2) |
| `pi_5^3` | 必須 | complete / PASS | 0 | 0 | DB prior: sphere.csv (n=2, k=2) [参考: Proposition 5.3], (5.3), Proposition 5.1, Proposition 4.2 (4.4), (5.1), Chapter V, i) |
| `pi_6^4` | 必須 | complete / PASS | 0 | 0 | DB prior: sphere.csv (n=3, k=2) [参考: Proposition 5.3], Proposition 4.4, Proposition 4.2 (4.4), (5.1), Chapter V, i) |
| `pi_28^22` | 必須 | complete / PASS | 14 | 0 | DB prior: sphere.csv (n=8, k=6), (4.5) |
| `pi_32^22` | 必須 | complete / PASS | 10 | 0 | DB prior: sphere.csv (n=12, k=10), (4.5) |
| `pi_23^15` | 必須 | complete / PASS | 10 | 0 | DB prior: sphere.csv (n=10, k=8), (4.5) |
| `pi_33^24` | 必須 | complete / PASS | 39 | 0 | DB prior: sphere.csv (n=11, k=9), (4.5) |
| `pi_10^8` | 追加調査 | complete / PASS | 4 | 0 | DB prior: sphere.csv (n=7, k=2) [参考: Proposition 5.3], DB prior: sphere.csv (n=4, k=2) [参考: Proposition 5.3], (4.5) |
| `pi_22^13` | 追加調査 | complete / PASS | 6 | 0 | DB prior: sphere.csv (n=11, k=9), (4.5) |
| `pi_24^15` | 追加調査 | complete / PASS | 12 | 0 | DB prior: sphere.csv (n=11, k=9), (4.5) |

## 残存依存と検証上の注意

- `pi_10^8`: citation is detached from root/GIVEN/Reference heading

Proof Tree で引用されない個別 Definition が命題台帳に残ることは、
その Definition が証明に依存していることを意味しない。
共通 Definition の適用範囲外に残る証明は無条件に削除しない。
この監査は対象ケースでの依存解消を確認するもので、全 stem への数学的な完全性を主張しない。
DB prior と Toda (4.5) は独立した証明根拠として維持する。
