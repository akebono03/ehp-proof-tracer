# Phase 169 R10E5-R3 設計

GitHub develop HEAD `d6c4bd745b2537ffe4da72a7a77865d3c00f6e18` の `proof.py` を確認した。`_find_all_matching_premise_bindings` は与えられた `available_steps` から、各 `PremisePattern` に一致する前提を選び、そのパターン順で `InferenceMatch.premises` を返す。従って、二つの前提を入力時に逆順にしても、有効な二つの推論から同じ結論が得られる。

変更は既存テスト `test_r10e5_two_inferred_images_are_required_to_prove_composition` のみ。失敗した「逆順は拒否」を「逆順でも前提パターン順に正規化され、同じ合成懸垂像を証明する」に改める。前提不足、`GIVEN` 偽装の拒否検査は保持する。

本番の `proof.py`、`rule.py`、`phase165_r52_r9_shared_math.py` および Trust Boundary は変更しない。R10E5 本来の限定 pytest と audit を再実行し、Phase 169 全体 pytest は最後まで行わない。
