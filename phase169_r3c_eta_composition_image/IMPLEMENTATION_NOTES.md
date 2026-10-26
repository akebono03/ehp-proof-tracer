# Phase 169 R3C — 実装説明

## 変更対象

- `phase165_r12_r21_eta_generator_chain.py`：1ファイルのみ。
- import：`from expression import Composition, HomotopyElement` を追加。変更後の import 全文は `full_files/phase165_r12_r21_eta_generator_chain.py` に収録。
- 新規 `_composition_eta_suspensions(goal)`：`suspension_to_generator_image_rule()` の直後に追加。関数全文は `full_functions/_composition_eta_suspensions.py`。
- 新規 `composition_eta_suspension_image_rule(goal)`：前述の新規関数の直後に追加。関数全文は `full_functions/composition_eta_suspension_image_rule.py`。
- 既存 `expand_cited_eta_generator(goal)`：関数全体を置換。関数全文は `full_functions/expand_cited_eta_generator.py`。
- 新規 `tests/test_phase169_r3c_eta_composition_image.py`：import・補助関数・テスト関数7件の全文を収録。

## 数学的意味

既存の η 系列の定義に基づいて個々の懸垂 $E\eta_n=\eta_{n+1}$ を証明し、写像の合成と懸垂の交換を利用して $E(\eta_n\circ\eta_{n+1})=\eta_{n+1}\circ\eta_{n+2}$ を推論する。前提2件を ProofStep の INFERENCE として要求し、証明していない一般命題や群構造を GIVEN として追加しない。

## 実行対象

`run.ps1` は新規テストと既存の関連テストに限定した pytest を実行する。適用前状態は `output/phase165_r12_r21_eta_generator_chain.py.before` に保存。テスト・監査失敗時の復元はインストール直後の状態と一致する場合に限る。

## 完了条件と次 Phase

一般的なη合成生成元の像が前提2件から検証可能な推論候補として接続され、既存の単独η系列およびR3Bの探索を壊さないこと。次のR3Dは Toda (5.3) および EHP 完全列から $E:\pi_4^2\to\pi_5^3$ の同型性を導出するための不足前提を確認し、文献順と自己参照禁止を維持する。

Phase 169 終了時まで全体 pytest は実行しない。
