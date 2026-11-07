# Phase 174 R3-R7-R25 — 一般型付き推論の独立実装

## 変更対象

新規ディレクトリ `phase174_r3_r7_r25_prop27_isolated_inference/` のみ追加。既存のクラス・関数・API・共通 Renderer を変更しない。

- `rule.py`：`Prop27GeneralTheoremPremise`、`Prop27TypedHopfDeltaStatement` と `typed_specialization`、`prop27_typed_specialization_rule` を新設。
- `audit.py`：Git HEAD、採用 TeX と既存ソース、型・符号の監査。
- `tests/test_rule.py`：新規テスト関数と必要な import を追加。
- `run.ps1`：DryRun と限定 pytest のみ。
- `README.md`：英語の説明。
- `CODE_FULL_JA.md`：新規コード全文。

## 数学的範囲

Toda Proposition 2.7 の式は $n\ge2$ 偶数について $H\Delta(\iota_{2n+1})=\pm2\iota_{2n-1}$。$n=6$ で $\pi_{13}^{13}\xrightarrow{\Delta}\pi_{11}^{6}\xrightarrow{H}\pi_{11}^{11}$。符号は未決定のまま保持。

`InferenceRule` は、*別途検証された* 一般命題の `INFERENCE` 前提と出典識別を要求する。今回その前提を捏造・GIVEN 登録せず、本番探索にも接続しない。テストに使う模擬 `ProofStep` は動作検査だけであり、公的な証明の証拠ではない。

## 完了条件

Git Source Guard と限定 pytest が PASS。新規 GIVEN 0、本番公開規則登録 0。根の証明は未完成。Phase 全体テストを実施しない。

## 次工程との境界

真正な source-certified 一般命題の型付き `ProofStep` を既存 Proof Search で生成・検証し、規則に接続する工程は次段階。専用 Narrative と結論直接 GIVEN は禁止。


## R25R1 Git 履歴ガード修正

旧版は HEAD を固定一致で検査したため、R24 のコミット後に拒否した。修正版はレビュー済み HEAD を祖先として要求し、介在コミットの変更パスを R24/R25 に限定する。リモートがレビュー済み HEAD でもローカルと一致でもない場合は拒否する。確認済みの文献・コード内容はレビュー済み HEAD のバイト列と比較する。数学規則は変更しない。

## R25R2 Git 履歴ガード最小修正

GitHub 比較で、`5349f850...` から `bfaf93f7...` は1コミット、R24 追加ファイルおよび `.pytest_cache/v/cache/nodeids` 20行追加のみと確認した。

`audit.py` の `classify_lineage()` におけるコミット済みパスの検査で、既存の `ALLOWED_TRACKED` に明示されている `.pytest_cache/v/cache/nodeids` も許容する。その他のキャッシュファイル、無関係なコード変更、レビュー済み資料の改変は引き続き拒否する。`tests/test_lineage.py` に正常／異常系の回帰テストを追加する。数学規則、公開登録、共通 Renderer は変更しない。

R25 の完了にはユーザー環境での DryRun と限定 pytest が必要であり、全体 pytest は実行しない。
