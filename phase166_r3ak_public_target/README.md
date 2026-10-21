# Phase 166 R3-AK: Typed Goal in Web Proof Target

変更対象: `phase165_r52_r3_web_adapter.py` の
`build_partial_web_group_proof_view()` のみ。
変更後の関数全文は `build_partial_web_group_proof_view.py.txt` に収録。
import節は変更しない。既存クラス、証明探索、証明規則も変更しない。

既存 `_group_proof_statement_latex()` から型付きの証明対象全体を取得し、
Webの `Proof target` に渡す。型付きGoalがないときは群名表示を維持。
`Composition` の累乗正規化は既存 `render_toda_public_group_generator_latex()` を使用。
DB文字列を直接表示せず、Goalの型付き等式を唯一の情報源とする。

適用後は限定pytest 4件のみ実行する。全体pytestは実施しない。
今回の完了条件は `Proof target` の等式表示と既存証明状態の維持。
次段階で112群の構造および表示正規化を監査する。
