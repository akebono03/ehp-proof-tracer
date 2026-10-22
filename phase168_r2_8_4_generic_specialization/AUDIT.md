# Phase 168 R2-8④ 変更・監査記録

## 現行コード確認
- `phase166_r3t_goal_source_binding/goal_source.py` の `_same_group_structure()` と `resolve_specialized_goal_citing_id()` を確認。
- `phase165_r57_r8_eta_specialization.py` は Proposition 5.1 の 1-stem に限定されていることを確認。
- `phase166_r3aj_structured_generator.py` の `structured_generator_from_ids()`、R2-8③ の `identity.py` と関連テストを確認。
- R2-8② の JSON で、未解決対象は $\pi_7^5$ と $\pi_9^6$ であることを確認。

## 変更対象
1. `phase166_r3t_goal_source_binding/goal_source.py`：`resolve_specialized_goal_citing_id()` 関数全体を置換。変更後の関数全文は `replacement_function.py`。
2. 新規 `phase168_r2_8_4_generic_specialization/specialization.py`：`_symbolic_index()`、`_symbolic_factor()`、`_registered_clause_kind()`、`specialize_registered_higher_stem()`。新規ファイルの先頭から追加。
3. 新規 `phase168_r2_8_4_generic_specialization/tests/test_r2_8_4_generic_specialization.py`：6件の限定テスト。新規ファイル先頭から追加。
4. 新規 `apply.py`、`run.ps1`、`README.md`、`AUDIT.md`。

import 変更なし。既存クラス変更なし。既存 API 変更なし。

## 範囲と制限
- Proposition 5.3 の $n\ge 5$ の $\eta_n\eta_{n+1}$ および Proposition 5.6 の $n\ge 6$ の $\nu_n$ の構造化された登録命題だけを扱う。
- 数式パターン、位数、stem を検査し、既存の `HyoujiGen.csv` に基づき具体化する。
- 掲載順・成分順が欠落した主張を使用しない。別の命題や別の群への照合は不可。
- `ProofStep`、GIVEN、逆向き探索規則、Renderer、DB、命題登録は変更しない。
- この処理が保証するのは引用識別子の照合だけであり、証明完了や出版順による利用許可の認定ではない。

## 実行と完了条件
`run.ps1` により限定 pytest（新規6＋R2-8③6＋R2-8①4）を行い、R2-8①の9対象について `RESOLVED` 9件を期待する。全体 pytest は Phase 168 の最後に実施する。

## 次 Phase 境界
型付き一般命題の ProofStep を伴う推論・証明探索への接続はこの小修正には含めない。
