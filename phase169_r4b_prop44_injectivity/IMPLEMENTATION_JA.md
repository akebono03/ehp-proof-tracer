# Phase 169 R4B — Proposition 4.4 に基づく単射性

## 変更対象

1. `phase165_r52_r9_shared_math.py` の既存関数 `shared_expansion_provider` のみ（関数内ローカル import 2行分）。
2. 新規 `phase169_r4b_prop44_injectivity/rule.py` の関数 `_is_hopf_four_suspension`、`prop44_hopf_four_injectivity_rule`、`expand_cited_prop44_injectivity`。
3. 新規テスト `tests/test_r4b_prop44_injectivity.py` の6関数。
4. 新規実行・検証 `patch.py`、`audit.py`、`run.ps1`。

既存モジュールの先頭 import に変更はない。新規モジュールの import は `rule.py` に全文収録する。

## 根拠と制約

Toda の採用原文 `sources/toda/Toda_04_2.tex` の Proposition 4.4 の直前に、$n=2,4,8$ の Hopf fibration が記されている。Proposition 4.4 は Hopf 不変量 $\pm1$ の写像が存在するとき、懸垂写像 $E$ の単射性を与える。この段階では $n=4$ の場合だけを接続する。

* 型付き `TodaProp44UniversalStatement` の引用順スクリーニングを必須とする。
* `MapInjective(E:\pi_5^3\to\pi_6^4)` を `INFERENCE` で証明し、根拠を `GIVEN` 命題へ遡る。
* Toda (4.5) の安定範囲を変更しない。
* $E$ の全射・同型、$\pi_6^4$ の群構造、Reference の表示に関する先取り変更を行わない。
* 文書 README.md/design.md/development_log.md/roadmap.md/proof_records.md は Phase 終了前につき変更しない。

## 完了条件

限定 pytest と実際の引用済み命題を用いた単射性 ProofStep の再構成が成功し、他の本番ファイルが変更されないこと。`output/shared_expansion_provider_FULL.py` は完全な置換可能関数を出力する。失敗時は元ファイルをバックアップから復旧する。

## 次段階の境界

EHP と (5.1) に基づく $E$ の全射性、単射性と全射性から `TodaSuspensionIsomorphismStatement` への橋渡し、さらに生成元の像の証明を経て、初めて $\pi_6^4$ の完全性を判定できる。Phase169 全体テストは Phase 末尾のみ。
