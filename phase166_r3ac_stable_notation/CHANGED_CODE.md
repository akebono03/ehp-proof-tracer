# Phase 166 R3-AC（改訂）

- `phase165_r52_r9_shared_math.py`: `shared_expansion_provider()` に、文献掲載順で認められた一般定義を使う正規化候補を追加。関数全文は適用後 `shared_expansion_provider_full.py.txt` に出力。
- `phase165_r57_r11_proof_order_gate.py`: `is_unordered_root_structure_specialization()` で、一般定義を要する正規化候補の構造を認める。関数全文は適用後 `is_unordered_root_structure_specialization_full.py.txt` に出力。
- `phase166_r3ac_stable_notation.py`（新規、プロジェクト直下）: `_stable_eta_renaming_shape()`、`stable_eta_notation_rule()`、`expand_stable_eta_notation()`。全文同梱。
- `tests/test_r3ac.py`（新規、ZIP 内）: 限定テスト2件、全文同梱。
- 元の Toda (4.5) 輸送規則・掲載順・renderer は無変更。

採用済みの Toda Chapter V の $\eta_n=E^{n-2}\eta_2$ から、$r\ge 2$ の生成元名を証明付きで正規化する。$r=1$ は既存の R3-V 経路を維持する。群構造輸送は任意の stem で既存の汎用規則を利用する。未登録の $\nu$、$\sigma$ 系列について名称正規化を仮定しない。

限定 pytest: `python -m pytest -q phase166_r3ac_stable_notation/tests/test_r3ac.py phase166_r3v_test_repair/test_r3v.py`。全体 pytest は Phase 166 終了時のみ。
