# R3V 監査対象と境界

## 対象ファイル・関数

新規ファイル `phase169_r3v_hopf_codomain_audit/audit.py`:
- `_screened_context()`：実際の完全証明から引用済み FIXED_STATEMENT の GIVEN を取得する。
- `examine()`：Proposition 5.1 の一般 $\eta$-群構造を特殊化し、出典の重複、文献順、実探索の可否を調べる。
- `main()`：監査結果を JSON と標準出力へ記録する。

新規ファイル `tests/test_phase169_r3v_hopf_codomain_audit.py`：限定テスト3件。

既存モジュール・関数・クラス・import は変更しない。

## 完了条件

- $\pi_5^3$ の COMPLETE を維持する。
- 引用済み Proposition 5.1 から $\pi_6^5$ の特殊化候補を調べる。
- $H(\nu')=\eta_5$ と群の生成元の型付き一致を確認する。
- 重複出典がある場合、その ID と位置を報告する。
- 既存の Hopf 全射性に群構造の前提が接続されているか区別する。

R3V では数学的推論規則を変更しない。次の実装工程で具体的な導出を接続する。
