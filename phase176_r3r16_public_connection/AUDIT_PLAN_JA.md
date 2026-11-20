# Phase 176 R3R16 実装・監査計画

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge`：Toda Lemma 5.7 の出典登録を追加。
- 同ファイルの `shared_expansion_provider`：出典審査済み Provider を追加。
- 新規 `phase176_r3r16_public_connection/provider.py`：`build_public_lemma57_right_provider`。
- 新規 `phase176_r3r16_public_connection/installer.py`：監査済み Git blob に限定する変更適用。
- 新規 `phase176_r3r16_public_connection/audit.py`：公開二段階 ProofStep と Group query の実測。
- 新規 `phase176_r3r16_public_connection/tests/test_r3r16_connection.py`：限定テスト。

## 保証

群構造の直接 GIVEN を追加しない。出典の主張は出典つきの固定命題として登録し、像の等式は推論規則を経由させる。根の群構造の完成は監査結果による。開発中に全体 pytest を実行しない。

## 実装境界

R3R16 は二段階を公開再帰探索に接続する段階。群構造の追加義務を自動的に証明したことにはしない。
