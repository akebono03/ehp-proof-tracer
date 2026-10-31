# Phase 171 R20R11 実装・検証範囲

## 変更対象

1. `phase171_r2j_r2_cyclic_hopf_surjective/source.py`
   - import 追加：`admitted_db_step`, `verified_db_step`
   - 新規関数：`verified_prior_cyclic_generator_image_surjectivity_rule`（既存の `cyclic_generator_image_surjectivity_rule` の直後）
   - 変更関数：`expand_cited_cyclic_hopf_surjectivity`
2. `phase165_r52_r9_shared_math.py`
   - 変更関数：`shared_expansion_provider`（既存の `expand_cited_cyclic_hopf_surjectivity` 呼出しのみ）
3. 新規限定テスト：`tests/test_r20r11_verified_prior.py`

## 認証上の条件

- 固定文献に由来する一般群定理を候補選択の前提として維持する。
- 先行群の `GIVEN` は既存の `admitted_db_step` と `verified_db_step` によって、依存順序、`sphere.csv` と `HyoujiGen.csv` の現行行、及び引用情報を再検証する。
- Hopf 像に関する前提は公開探索が自力で再構成した `INFERENCE` に限る。
- 偽造した `GIVEN`、未検証の DB 行、後続群、誤った写像・生成元を受け入れない。
- 既存の `INFERENCE + INFERENCE` 経路は維持し、First Successful Proof Search に影響しない。

## 実施しないもの

- `phase165_r3_recursive_search.py` の変更。
- 証明済み木の探索への注入。
- 新規 `GIVEN`、架空の出典、Web 完全性の先取り。
- 関係のないリファクタリング、Phase 終了前の全体 pytest。

## 完了条件

- DryRun が source blob・作業ツリー保護を PASS とする。
- 限定 pytest が PASS とする。
- 公開探索が Hopf 全射性 `H:π₇³→π₇⁵` を `proved` として記録する。
- 証明の完成、Web 表示は別の独立した検証対象とする。
- 監査結果は `output/audit.json` に残す。
