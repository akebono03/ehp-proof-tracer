# Phase 166 R3-AU-6 監査

追加ファイル：`audit.py`（`inspect`, `main`）、`test_r3au6.py`（3つの限定テスト）、`run.ps1`、`README.md`、`AUDIT.md`。

既存の `repository.py`, `models.py`, `toda_human_readable_renderer.py`, `tests/test_repository.py`, `phase166_r2_generator_group_audit/audit.py` を確認した。これらは変更しない。

R3-AU-5 の `all_rows.csv` に記録された群内の成分 ID（昇順）の位置と、`gen_coe` の唯一の非零成分の位置を全行で比較する。非自明な一次結合、零ベクトル、位置不一致を区別する。`generator` 参考文字列は判定に使わない。

成立していても、位置対応が数学的に証明されたわけではない。合成因子の始域・終域や表示元の数学的型も未検証である。次段階は例外の原因と基底の順序規約の確認。全体 pytest は Phase 166 終了時のみ実施。
