# Phase 174 R3-R7-R18R1：監査修正の対象と境界

## 確認済み原因

- GitHub の `map_facts.py` の Git Blob SHA は `86fbf404783e15d344595bf54df5a9a8bafc35fc`。
- GitHub 上の本文に CRLF と LF が混在する。旧 `matches_git_blob` は、ハッシュ一致を検査する前に混在改行を拒否する。
- 旧 `verify_git_and_sources` は、正当な Git Blob の checkout まで不一致と判定する。
- GitHub `develop` は R17 マージ `4d59298949c14dc02d8bfb6ec28da4624ed980da` から、R18 パッケージのみを含む `7ecd12f28b5943b105ac6a953be69b44eae4a26e` へ進行済み。

## 変更対象

1. `phase174_r3_r7_r18_delta_image_surjectivity/audit.py`：Git Source Guard のみ。
   - 追加定数：`R18_MERGED_HEAD`、`R18_AUDIT_PATH`。既存定数 `REVIEWED_HEAD` の直後。
   - 新規関数：`matches_reviewed_checkout`。既存 `matches_git_blob` の直後。
   - 全文置換関数：`checked_lineage`。
   - 全文置換関数：`verify_git_and_sources`。
   - import の変更なし。
2. `phase174_r3_r7_r18r1_git_mixed_eol_guard/patch.py`：新規・Source Guard 付き適用・復旧。
3. `phase174_r3_r7_r18r1_git_mixed_eol_guard/run.ps1`：新規・DryRun→限定 pytest→R18 再監査。
4. `phase174_r3_r7_r18r1_git_mixed_eol_guard/tests/test_patch.py`：新規・改行と Git HEAD の負例を含む契約テスト。

## 既存 API と Phase 境界

既存の `matches_git_blob` は変更せず、単独の既存テスト契約も維持。`map_facts.py`、公開 Proof Search、R18 の数学的規則、Narrative、DB、5つのプロジェクト文書は無変更。

完了条件は実環境で `PASS_ISOLATED_GENERIC_DELTA_IMAGE_SURJECTIVITY_FRONTIER` および `PASS_REVIEWED_GIT_MIXED_EOL_R18_PUBLIC` の両方が出ること。結論の完成は宣言しない。全体 pytest は Phase 末のみ。
