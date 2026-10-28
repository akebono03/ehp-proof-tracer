# Phase 169 R10ET-R5 本番探索の比較監査

| 対象 | 完成/Trust | 共通Definition | 残存する置換可能推論 | 巡回圧縮 | 直和圧縮 |
|---|---|---:|---:|---|---|
| `pi_69^43` | complete / PASS | 30 | 0 | False | True |
| `pi_56^30` | complete / PASS | 4 | 0 | False | True |
| `pi_41^30` | complete / PASS | 17 | 0 | False | False |
| `pi_44^30` | complete / PASS | 28 | 0 | False | True |
| `pi_46^30` | complete / PASS | 24 | 0 | False | True |
| `pi_39^30` | complete / PASS | 57 | 0 | False | True |
| `pi_3^2` | complete / PASS | 0 | 0 | False | False |
| `pi_4^3` | complete / PASS | 0 | 0 | False | False |
| `pi_5^4` | complete / PASS | 0 | 0 | False | False |
| `pi_4^2` | complete / PASS | 0 | 0 | False | False |
| `pi_5^3` | complete / PASS | 0 | 0 | False | False |
| `pi_6^4` | complete / PASS | 0 | 0 | False | False |
| `pi_28^22` | complete / PASS | 14 | 0 | True | False |
| `pi_32^22` | complete / PASS | 10 | 0 | True | False |
| `pi_23^15` | complete / PASS | 10 | 0 | False | True |
| `pi_33^24` | complete / PASS | 39 | 0 | False | True |

R2 の検証済み Shadow Proof Tree と群・引用・Definition 数を照合。
Reference の削除は表示フィルタではなく Proof Tree の依存変更の結果。
DB prior と Toda (4.5) の GIVEN 祖先は独立して検証。
全体 pytest は Phase 末まで実行しない。
