# Phase 169 R10ET-R2 — 共通 Definition 優先の影響比較

**AUDIT_ONLY。アプリケーション実装・既存テスト・文書は変更しない。**

- HEAD: `a5892721436effaf7be759ff17afd3bd427814ed`
- 基準 HEAD: `36e4dc41427ec4437009c96b01cacb07dc165bf6`
- 基準ソース Blob: `61cbadb06f770c51a9c1f5a3c8026acf9e3e14aa`
- 追跡対象差分は不変: `True`
- 全体 pytest: 未実行

| 群 | 完成 | Trust | 共通 Definition 実採用 | 引用付き適用可能 | 引用数 | 圧縮表示 |
|---|---|---|---:|---:|---:|---|
| `pi_69^43` | complete | PASS | 30 | 0 | 2 | True |
| `pi_56^30` | complete | PASS | 4 | 0 | 2 | True |
| `pi_41^30` | complete | PASS | 17 | 0 | 2 | False |
| `pi_44^30` | complete | PASS | 28 | 0 | 2 | True |
| `pi_46^30` | complete | PASS | 24 | 0 | 2 | True |
| `pi_39^30` | complete | PASS | 57 | 0 | 2 | True |
| `pi_3^2` | complete | PASS | 0 | 0 | 4 | False |
| `pi_4^3` | complete | PASS | 0 | 0 | 4 | False |
| `pi_5^4` | complete | PASS | 0 | 0 | 3 | False |
| `pi_4^2` | complete | PASS | 0 | 0 | 2 | False |
| `pi_5^3` | complete | PASS | 0 | 0 | 6 | False |
| `pi_6^4` | complete | PASS | 0 | 0 | 5 | False |
| `pi_28^22` | complete | PASS | 14 | 0 | 2 | False |
| `pi_32^22` | complete | PASS | 10 | 0 | 2 | False |
| `pi_23^15` | complete | PASS | 10 | 0 | 2 | True |
| `pi_33^24` | complete | PASS | 39 | 0 | 2 | True |

## 個別 Reference の比較

### `pi_69^43`
- 消えた Reference: ['Chapter V, ν-family definition (after Lemma 5.5)', 'Chapter V, i)']
- 新たな Reference: []
- 元の直和圧縮表示: True
- 試験経路の直和圧縮表示: True

### `pi_56^30`
- 消えた Reference: ['Chapter V, ν-family definition (after Lemma 5.5)', 'Chapter V, i)']
- 新たな Reference: []
- 元の直和圧縮表示: True
- 試験経路の直和圧縮表示: True

### `pi_41^30`
- 消えた Reference: ['Chapter VI, v) Definition of indexed elements']
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_44^30`
- 消えた Reference: ['Chapter V, σ-family definition (after Lemma 5.14)']
- 新たな Reference: []
- 元の直和圧縮表示: True
- 試験経路の直和圧縮表示: True

### `pi_46^30`
- 消えた Reference: ['Chapter V, σ-family definition (after Lemma 5.14)', 'Chapter VI, iii) The elements mu_n (definition)']
- 新たな Reference: []
- 元の直和圧縮表示: True
- 試験経路の直和圧縮表示: True

### `pi_39^30`
- 消えた Reference: ['Chapter V, ν-family definition (after Lemma 5.5)', 'Chapter VI, iii) The elements mu_n (definition)', 'Chapter V, i)', 'Chapter VI, i) The Elements epsilon_n (definition)']
- 新たな Reference: []
- 元の直和圧縮表示: True
- 試験経路の直和圧縮表示: True

### `pi_3^2`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_4^3`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_5^4`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_4^2`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_5^3`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

### `pi_6^4`
- 消えた Reference: []
- 新たな Reference: []
- 元の直和圧縮表示: False
- 試験経路の直和圧縮表示: False

## 巡回群の圧縮表示

- `pi_28^22`: PASS, projection=False
- `pi_32^22`: PASS, projection=False

## 実装判定

共通 Definition で Proof Tree を再構築して Trust が通っても、古い引用前提に依存する Projection が不成立になれば、単純な探索優先順変更は採用しない。
Proof Tree の不要な個別引用を表示側だけで消さない。
DB prior と Toda (4.5) は別の前提として維持する。
監査段階での PASS は、実装変更の完了を意味しない。
