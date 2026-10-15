# Phase 165-R57-R4 削除監査

## 現行コード確認

GitHub の `toda_group_proof_narrative_renderer.py` には `render_toda_group_proof_narrative_markdown` が3回定義されている。最初の定義は次の定義で上書きされ、エイリアスにも捕捉されていない。2番目の定義は `_phase160_r7_previous_public_narrative_renderer` に保持されており、削除対象にしてはいけない。

## 対象

- `toda_group_proof_narrative_renderer.py`: 最初の未参照トップレベル関数定義を削除。
- `_phase159_render_pi_n_plus_1_n_stable_transport_narrative`: 当該最初の関数からしか呼ばれておらず、他の本番ルートに参照がない場合のみ削除。
- `phase165_r57_r4_shadowed_branch_cleanup/install.py`: 保護条件付き削除スクリプトを新設。
- `phase165_r57_r4_shadowed_branch_cleanup/test_phase165_r57_r4_shadowed_branch_cleanup.py`: 4件の対象テストを新設。

## 非対象・重要な制限

現行の `_phase160_r7_render_stable_finite_cyclic_transport_narrative` は **群別分岐を含み、現在も公開 Renderer から呼ばれる**。ここを削除すると出力が変わる可能性があるため R57-R4 では削除しない。その他の群別処理も証明データに基づく一般則への置換と既存テストの確認後に扱う。未完成証明や Backward Search は変更しない。

## 完了条件

死んだ関数の削除が実施され、現在の公開入口と既存のエイリアスを保持し、対象テストに成功すること。全体 pytest は Phase 165 最終時のみ。
