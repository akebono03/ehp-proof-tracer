# Phase 175 R3R8R1 — 公開探索の先行 DB 証明前提監査

## 実測された失敗

R3R8 の DryRun は PASS、限定 pytest は 44 PASS だったが、公開検索は `partial`、証明済み6ステップ、未解決7件、Web は `generic-partial-proof` となり、既存ファイルはロールバックされた。診断では以下の区別を確認した。

- `Relation(π_6^2, Z/4{η_2ν′})` は、既存 `admitted_db_step()` から返された先行 DB の `ProofRule.GIVEN` として証明探索に採用された。
- Toda Lemma 5.7 の一般出典は引用済み `GIVEN` である。
- Toda Lemma 5.4 の二重懸垂等式、そこからの所属、$E(\eta_2\nu')=0$ はそれぞれ出典と前提のある `INFERENCE` として成立した。
- `ImageZeroStatement(E:π_6^2→π_7^3)` では、既存 `zero_image_from_cyclic_generator_rule()` が群構造の `INFERENCE` を要求するため、先行 DB の `GIVEN` と一致しなかった。
- これを解消しても、Hopf リフトにおける先行群 $π_7^5$ が DB `GIVEN` として取得されると、旧リフト規則の群構造 `INFERENCE` 要求と一致しない可能性がある。

## 変更対象（開始前の監査）

- 既存 `phase165_r52_r9_shared_math.py`：変更対象は `search_shared_group_goal()` 全体のみ。トップレベル import の変更なし。
- 新規 `phase175_r3r8r1_verified_prior_public/rule.py`：`verified_prior_zero_image_rule()`、`expand_verified_prior_zero_image()`、`verified_prior_hopf_lift_rule()`、`expand_verified_prior_hopf_lift()`。
- 新規 `route.py`：`public_cited_ehp_extensions()`、`prepare_pi73_public_connection()` を全文収録。
- 新規 `install.py`、`audit.py`、`run.ps1`、`tests/test_install.py`、`tests/test_route.py`、`tests/test_verified_prior.py`、`tests/test_public_search.py`、`__init__.py`、`tests/__init__.py`、`README.md`、本書、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`、`search_shared_group_goal_FULL.py.txt`。
- 追加位置：新規 `rule.py` の import 節の直後に4関数。`route.py` の2関数は import 節の直後。既存関数の追加位置は、`search_shared_group_goal()` の既存 `(n,k)=(4,3)` 分岐の直後で、既存 `citing_assertion_id` 審査の直前。

## 数学的な許可条件

**有限巡回群の零像**：$G=\mathbb Z/m\{g\}$ が厳密な先行群として再確認でき、$E(g)=0$ を独立した推論で証明した場合に限り、$\operatorname{im}E=0$ を導く。群構造は `GIVEN` でも、`verified_db_step` で出典・順序・実際の ProofStep を再検証する。

**Hopf リフト**：$H:A\to B$ が単射で、$B=\mathbb Z/m\{h\}$ が再検証済み先行 DB の群であり、$H(x)=h$ を独立した推論で示した場合、$A=\mathbb Z/m\{x\}$ を得る。$B$ が単なる未証明 Goal なら適用しない。

元の `INFERENCE` のみを要求する2つの一般規則は一切変更しない。今回の追加規則は2つとも入力型と先行 DB の実証明を検査する一般規則であり、$(3,4)$ 専用の数学的な推論ではない。公開経路の選択のみ $(3,4)$ に制限する。

## 検証

1. 最新 `develop` の関連ソース・テストを確認し、既存 `phase165_r52_r9_shared_math.py` の Git blob `9fa11b383812570fae1a26868c98992a5934a327` に固定する。
2. R3R7 の成功監査レポートと Toda Lemma 5.4/5.7 の原典を再確認する。
3. 偽造 `GIVEN`、同一／後続 DB 結果、零像・Hopf 像の `GIVEN` 化を拒否する限定テストを実行する。
4. 通常 Group query の本物の再帰探索で `complete`、出典検証済みの証明木、`generic-complete-proof`、未解決0を確認する。
5. 失敗時は既存ファイルを byte-for-byte で元に戻す。全体 pytest は Phase 175 終了時だけ実行する。

## 次の Phase との境界

今回の対象は $\pi_7^3$ の公開検索接続のみ。$\pi_9^5$ と $\pi_{10}^6$ の未完成証明、共通 Renderer の文言、他の $k$ の一般化などは先取りしない。
