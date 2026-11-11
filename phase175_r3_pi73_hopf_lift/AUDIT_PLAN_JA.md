# Phase 175 R3R1 — $\pi_7^3$ の生成元ID照合補正

## R3 の実測と原因

R3 本実行では Source Guard、R2 証拠、Git 系譜を PASS としたが、`HOPF_LIFT_CANDIDATES=0`、`search_failed`、`ISOLATED_COMPLETE=False` であった。公開 Group query も `generic-partial-proof` を維持している。

Toda (5.3) の出典付き $H(\nu')=\eta_5$ は、$\nu'$ を `GeneratorSymbol(family="ν", decoration="′")` として表している。他方、`HyoujiGen.csv` の ID 3 によるデータベース Goal は `GeneratorSymbol(family="\\nu'")` を用いる。両者は同じ元を指す記法であるが、Python の `Composition` をそのまま比較すると一致しない。もとの `rule.py` の二箇所の厳密な等値条件が原因候補である。実際の文献 Context で他にも不足がある可能性を残すため、新たにフィルター段階ごとの件数を記録する。

## 証明目標と数学的前提

$$
\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}.
$$

導出に必要な親は、すべて別途証明される次の3件である。

$$
H:\pi_7^3\to\pi_7^5\ \text{は単射},\qquad
\pi_7^5=\mathbb Z/2\{\eta_5^2\},\qquad
H(\nu'\eta_6)=\eta_5^2.
$$

今回の補正は、同じ元を表す記号が `HyoujiGen.csv` の同じ ID と次元で厳密に一致するかを既存の `same_registered_group_presentation` で判定するのみ。**名前の類似、次元の一致、生成元らしい表示だけでは認めない。** 3親のすべてが `ProofRule.INFERENCE` であることも維持する。

## 変更対象・クラス・関数

既存の production ファイルおよび既存クラスは変更しない。既存の R3 監査ディレクトリだけを置換する。

- `phase175_r3_pi73_hopf_lift/rule.py` の `hopf_lift_inputs()` 全体と `expand_cited_hopf_lift()` 全体を置換。import は変更しない。`hopf_lift_rule()` は変更しない。
- 同ディレクトリ `audit.py` の `inspect_pi73()` 全体と `write_report()`、`run()` 全体を置換。`inspect_pi73()` の関数内 import に既存ユーティリティを追加するが、top-level import は変えない。
- `tests/test_rule.py` の import は追加後の全文を収録。`cited_nu_prime_image()` をファイル末尾に追加し、ID 照合・candidate 候補・誤った記号・見た目だけの偽物を拒否するテストを4件追加。
- `tests/test_audit.py` で既存の報告テストを必要な計測フィールドに対応させ、新規2テストをファイル末尾に追加。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`（日本語）、`CODE_FULL_JA.md`（日本語）を全文置換。
- `run.ps1`、両 `__init__.py` は変更しない。README、design、development log、roadmap、proof records の主要文書は更新しない。

全文置換可能な全コードと全 import は `CODE_FULL_JA.md` に収録する。既存の関連テストは Phase 171 R2I、Phase 174 R5、Phase 175 R1/R2/R3 とした。

## Source-first と完了判定

R2 完了報告の再照合、develop の監査専用系譜、既存 Source PIN を従来どおり要求する。既存出典を変更しない。監査 Worker が以下を記録する。

- `R3R1_CITED_HOPF_CHAINS`：先行出典から構成できた Hopf 連鎖。
- `R3R1_EXACT_GENERATOR_MATCHES`：Python オブジェクトの完全一致。
- `R3R1_REGISTERED_ID_MATCHES`：HyoujiGen ID を用いた一致。
- `R3R1_CODOMAIN_SCHEMAS`：先行 Proposition 5.3 から特殊化できた $\pi_7^5$ の巡回群候補。
- `R3R1_SOURCE_PAIR_MATCHES`：上記と次元・像・位数を照合した親 Goal 一式。
- `R3_HOPF_LIFT_CANDIDATES`：最終的な逆向き推論候補。

`CANDIDATES>0` のみで証明完成とはしない。`ISOLATED_COMPLETE=True` かつ `ISOLATED_TRUST=True` で、実際の推論親がすべて検証された場合に限り独立証明完成とする。新 GIVEN、既存 production への Provider 接続、Proof Tree 再利用は一切しない。

## 検証・次の段階

この ZIP では限定 pytest、DryRun、Source Guard、元 R2 レポートと Git 系譜、実 Worker、追跡済みファイル不変を検証する。全体 pytest は Phase 175 の最終 Gate まで実施しない。

R3R1 で候補が増え未完成の場合は、実際の新しい Open Goal のみを追加監査する。独立証明完成ならば次 Phase で最小限の公開 Provider 接続を検討する。$n=5,6$ の探索機能は先取りしない。
