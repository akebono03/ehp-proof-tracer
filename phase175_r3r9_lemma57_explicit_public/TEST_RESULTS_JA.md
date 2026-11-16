# Phase 175 R3R9 — テスト記録

## 現時点の作成環境での確認

- すべての新規 `.py` と `search_shared_group_goal_FULL.py.txt` の構文検査：**15対象 PASS**。
- 既存の関数全体と変更後関数の AST（抽象構文木）、API 引数、置換範囲の監査：実施。
- インストーラーの純粋関数による LF／CRLF 置換・未知の差分拒否：**限定テスト5件 PASS**（旧ガードへの import をテスト用スタブに置き換えた独立環境）。
- GitHub `develop` の公開接続対象ファイルを確認：`phase165_r52_r9_shared_math.py` Git blob `3426b223f94e839e77972801977d58a4ca182767`。
- Toda Chapter V の Lemma 5.7 原文と出典順序を確認：特別な零写像結論が明記されている。追加の単独 Source Guard テストで正規テキストを受理し、特別結論を改変したテキストを拒否。

## Windows 実リポジトリでは未実施

以下は同梱 `run.ps1` の本実行時に**限定して実行**する。

```text
python -B -m pytest -q -p no:cacheprovider \
  phase175_r3r9_lemma57_explicit_public/tests \
  phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py \
  phase175_r3r8r1_verified_prior_public/tests/test_public_search.py \
  phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py \
  phase175_r3_pi73_hopf_lift/tests/test_rule.py \
  phase173_r4_r1_public_connection/tests
```

同時に、`inspect_one_group(3,4)` を子プロセスで実行し、通常 Proof Search、Proof Tree Trust、共通 Narrative、Web `generic-complete-proof` を検証する。

**実リポジトリでの PASS 件数はまだ主張しない。**

## 完了条件

`PASS_R3R9_DIRECT_LEMMA57_PI73_PUBLIC_COMPLETE`

失敗時は `R3R9_REFUSED_OR_PUBLIC_VERIFICATION_FAILED` として本体の接続関数を自動復元する。

全体 pytest：Phase 175 完了時のみ実施。
