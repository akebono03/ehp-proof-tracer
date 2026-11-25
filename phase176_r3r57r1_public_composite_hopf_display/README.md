# Phase 176 R3R57R1 — Public Composite Hopf Display

## 目的

R3R57 で検証した合成右因子 Hopf 等式列の表示処理を完成証明の共通最終整形関数に接続する。数学的推論・GIVEN・探索順序は変更しない。

## 変更

- `phase171_r20r13_eta_sentence_layout/projection.py`: `format_complete_proof_sentences` に公開接続を追加。
- `phase176_r3r57_composite_hopf_display_isolated/tests/test_projection.py`: `verified` fixture で公開接続だけを無効化し、旧独立テストの入力を維持する。テスト関数と期待値は変更しない。
- `phase176_r3r56r3_public_cited_source_display/tests/test_connection.py`: `test_two_exact_replacements_are_idempotent` で R57R1 の変更を厳密に逆変換し、R56R3 の対象を復元して検査する。未知の変更を拒否する条件は維持する。

変更前後の全関数をテンプレートとして同梱。旧 Git blob の照合に成功した場合のみ書き換える。過去の preflight はその時点のハッシュを固定するため、今回の preflight では厳密な逆変換と各先行パッチの適用済み検査を使う。

## 実行

リポジトリルートで `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r57r1_public_composite_hopf_display\run.ps1 -DryRun` を実行し、成功後に `-DryRun` を外す。限定 pytest 29 件を予定。実環境での統合テストは未実施。

## 完了条件

`PASS_R3R57R1_PUBLIC_COMPOSITE_HOPF_DISPLAY_CONNECTED`。証明木 62 件（INFERENCE 51、GIVEN 11）、出典 10 件、Open Goals 0、本文 26→18 行、未完成表示不変。全体 pytest は実施しない。
