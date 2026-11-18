# Phase 175 R4R10 — テスト記録

## 作成環境

- GitHub `akebono03/ehp-proof-tracer` `develop` HEAD：`5c263cc69dc409842d3a13cb3fc65c2347df0bef`（R4R8 のコミット）。
- 対象 `phase165_r52_r9_shared_math.py` Git blob：`df4e0f834e9bc321f338ec10b363c79d82623457`、2関数と変更アンカーを確認済み。
- R4R7 一般規則 Git blob：`e957752baf93f75352d106e53205730af9a02b4d`。
- 出典：Toda chapter II の Proposition 2.5、chapter V の (5.8) の印刷式を確認済み。
- AST・置換の限定 pytest：8 passed（初期）。
- R4R10 の新設テスト（実 API の互換スタブ＋実 R4R7 rule.py）：43 passed。
- `python -m compileall`：PASS。
- **実リポジトリの限定 pytest、DryRun、本実行は未確認。**
- **全体 pytest は Phase 175 終了時まで実施しない。**

## 実環境で実行する限定 pytest

`run.ps1` は以下のみ実行する。

- `phase175_r4r10_cited_58_prop25_public/tests/test_installer.py`
- `phase175_r4r10_cited_58_prop25_public/tests/test_source.py`
- `phase175_r4r10_cited_58_prop25_public/tests/test_provider.py`
- `phase175_r4r10_cited_58_prop25_public/tests/test_audit.py`
- `phase175_r4r7_prop25_typed_composition/tests/test_rule.py`
- `phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py`

## 完了条件

- DryRun Gate：`PASS_R4R10_CITED_58_PROP25_DRYRUN`
- 本実行 Gate：`PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING`
- 共有 Registry で (5.8) と Prop 2.5 の独立した GIVEN が取得できる。
- 共有 Provider から型付き $\Delta(\eta_9)$ の条件付き推論候補と、その2件の親候補を取得でき、(5.8) と Prop 2.5 と $\eta$ 定義の証明連鎖が独立に検証できる。
- $\Delta(\iota_9)$ の $\pm$ は維持。$\pi_9^5$ を直接 GIVEN にしない。
- 本番変更は `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` と `shared_expansion_provider()` の2関数のみ。
- 完全な2関数と本番ファイル全体は監査フォルダーに出力する。
