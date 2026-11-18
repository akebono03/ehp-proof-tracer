# Phase 175 R4R12R9 — (5.11) を一般生成元像として接続

## 数学的な証明の順序

1. Toda Proposition 2.5 と (5.8) から符号付き Δ 合成像を導出する（R4R10 の既存推論）。
2. 証明済み $2\eta_7=0$ と η-family 定義によって符号を解決し、$\Delta(\eta_9)=E\nu'\circ\eta_7$ を `Relation` として導出する（R4R11 の既存推論）。
3. **今回の R9**：証明済み `Relation` から同じ写像の `GeneratorImage` を導出する一般的な型付き変換を接続する。
4. その `GeneratorImage` を R4R12 の6前提のうち Δ 生成元像として使用する。E の生成元像など他の義務は残る。

採用出典：`sources/toda/Toda_05_2.tex` Proposition 5.8 の証明、(5.8)、(5.11)。原著印刷版との照合を完了したとは主張しない。

## 変更対象

- **既存** `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` のみ。追加 import は関数内部で完結する。`installer.py` が関数の全文を `output/SHARED_PROVIDER_FULL_AFTER.py` に出力する。その他の既存 API は変更しない。
- **新規** `phase175_r4r12r9_delta_generator_image_bridge/rule.py`：`delta_image_equality()`、`expand_proved_delta_equality_image()`。一般的な推論規則1件。
- **新規** `installer.py`：`replacement()`、`install()`。
- **新規** `audit.py`：`git()`、`verify()`、`audit()`、`main()`。
- **新規** `tests/test_rule.py`：4件の限定テスト。
- **新規** `run.ps1`、`README.md`、`CODE_FULL_JA.md`。

## 安全条件

- Git HEAD は検証済み R7 コミット `b7bbb103`、または GitHub 比較で R7 の1コミット先・変更ファイル0件と確認されたマージコミット `3ec001a` のいずれかだけを許可する。後者の場合、ローカルでもコミット数・差分・祖先関係を再検査する。その他のコミットは拒否する。
- 採用 TeX は前コミットの Git blob に一致すること。R8 の Source-first チェックを再利用する。
- ソース上の `GeneratorImage` 候補があっても証明済みとは扱わない。
- 正確な型および EHP Δ の次数を照合する。
- `ProofRule.INFERENCE` の写像等式が必要。`GIVEN` を直接 `GeneratorImage` に変換しない。
- R9 の数学規則は `Relation → GeneratorImage` の一般規則のみ。群構造を直接登録しない。
- 全体 pytest は Phase 175 完了時に限る。

## 完了条件と次の境界

`PASS_R4R12R9_GENERIC_BRIDGE_CONNECTED_PROOF_PENDING` は共有探索内で R9 変換候補を確認できたことを意味する。R4R11 の Relation 証明が最後まで成功したこと、および群の完成証明を意味しない。次段階では R9 監査レポート内の `shared.delta_equality_candidates` と、他の E 生成元像義務を調べる。

## R4R12R9R1 — Git HEAD マージ系譜修正（2026-11-18）

GitHub の `b7bbb103..3ec001a` 比較により1コミット先かつ変更ファイル0件と確認。
既存 `audit.py` の `PRIOR_COMMIT` 直後に `REVIEWED_MERGE_COMMIT` を追加し、`verify()` の全文を更新。
新規 `tests/test_lineage.py` の6テストで正常系・改変・不正系譜を検証。
`run.ps1` の限定テスト対象を拡張。証明規則 (`rule.py`)、本番コード (`phase165_r52_r9_shared_math.py`)、数学的出典は変更しない。
DryRun および本実行が PASS するまで、R9 について証明や接続成功を主張しない。
