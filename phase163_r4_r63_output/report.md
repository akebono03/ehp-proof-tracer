# Phase 163 R4-R63：未番号 Definition 候補の TeX 範囲監査

出典の開始・終了行は**監査用の暫定候補**であり、定義全体の数学的範囲を確定したものではない。

|章|候補|暫定出典範囲|要注意|
|---:|---|---|---|
|1|`unit_sphere`|80–83|—|
|1|`pointed_homotopy_classes`|155–159|—|
|1|`composition_homotopy_classes`|163–170|MATHEMATICAL_CONTEXT_OUTSIDE_SPAN|
|1|`iterated_suspension`|283–288|—|
|1|`addition_inverse_suspension`|341–354|POTENTIAL_MULTIPLE_ASSERTIONS|
|1|`secondary_composition`|535–540|MATHEMATICAL_CONTEXT_OUTSIDE_SPAN|
|1|`reduced_cone`|1084–1087|—|
|1|`extension`|1099–1103|MATHEMATICAL_CONTEXT_OUTSIDE_SPAN|
|1|`coextension`|1105–1117|MATHEMATICAL_CONTEXT_OUTSIDE_SPAN|
|3|`stable_homotopy_group`|1199–1206|POTENTIAL_MULTIPLE_ASSERTIONS|
|3|`stable_composition`|1214–1221|—|
|3|`stable_toda_bracket`|1236–1266|MATHEMATICAL_CONTEXT_OUTSIDE_SPAN|
|5|`nu4_generator_notation`|567–579|—|
|5|`nu_n_notation`|605–607|POTENTIAL_MULTIPLE_ASSERTIONS, SHARED_ADJACENT_NOTATION_BLOCK|
|5|`eta_n_cubed_notation`|608–612|POTENTIAL_MULTIPLE_ASSERTIONS, SHARED_ADJACENT_NOTATION_BLOCK|
|5|`nu_n_squared_notation`|1320–1323|POTENTIAL_MULTIPLE_ASSERTIONS|

特記事項：第5章の ν 記法と η³ 記法は隣接した二つの数式に分かれる。各数式内にも複数記号がある。
第3章の stable Toda bracket は 1236–1266 行を確認したが、前後の仮定や既出の構成は別途照合が必要。
掲載順、定義対象の確定、数学的同値性、原本照合は未完了。本番 Registry と ID、証明探索は未変更。
全体 pytest は実施しない。
