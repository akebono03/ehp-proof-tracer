# Phase 174 R3-R7-R8R1 Source Guard 修正

- 原因: `phase174_r3_r7_r8_composite_image_gap/audit.py` の `SOURCE_BLOBS` における `phase165_r14_r6_generic_iso.py` の SHA が39文字で、末尾の `7` が欠落していた。
- GitHub develop HEAD 確認時点: `95f37f2020a728b4951b8d26506059a8c54a685f`。
- GitHub の同ファイル SHA: `8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7`。
- 変更対象: `audit.py` の定数 `SOURCE_BLOBS`（該当1項目）、`tests/test_audit.py` の末尾に新規テスト関数を追加。
- 変更しないもの: 本体ソース、他の SHA、Git HEAD の受理条件、公開 Proof Search、GIVEN、Renderer、Web、共通5文書。
- 限定 pytest: `python -B -m pytest -q --import-mode=prepend -p no:cacheprovider phase174_r3_r7_r8_composite_image_gap/tests/test_audit.py`。`run.ps1` が R8 と旧 Phase のテストを別プロセスで行う。
- 完了条件: R8・回帰限定 pytest と Source Guard、DryRun、本実行が PASS、監査 JSON が生成される。
- R9 との境界: 今回は出典ガードの転記ミス修正のみ。証明探索の一般規則追加は行わない。
