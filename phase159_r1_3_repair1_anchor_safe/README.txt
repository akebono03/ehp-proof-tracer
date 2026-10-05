Phase 159-R1-3 repair1
========================

前回失敗の原因:
- target function の全文一致 anchor が ZIP 内で過剰 escape されていた。
- imports 2箇所だけが適用された状態で停止した。

repair1:
- その partial apply 状態を受け入れる。
- function boundary で target / normalizer を置換する。
- import は存在確認して重複追加しない。
- target section は既存 baseline text を再利用せず semantic target から再構成する。
- exactness component / map-property / PRECONDITION_FOR_DEFINITION を public 表示へ投影する。
- pi_3^2 dimension 専用 branch は追加しない。
- full pytest は実行しない。
