# R38 検証記録

- GitHub の現行コード・R6/R7/R9/R14/R36 およびテストを照合済み。
- 独立した静的検査：4 PASS（この実行環境）。
- 実行方法：`python -m pytest -q -p no:cacheprovider phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_static.py`。
- プロジェクト結合テストと限定 regression はユーザーの Windows 環境で実施し、出力で実測する。
- 全体 pytest：未実施。
- 未証明：$E\pi_{10}^{5}=0$、上側 Δ 全射性、$\pi_{12}^{7}=0$。
