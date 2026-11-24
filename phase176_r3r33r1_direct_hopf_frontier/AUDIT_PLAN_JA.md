# Phase 176 R3R33R1 — 直接 Hopf 合成の型付き境界監査

## 現行コードの確認

GitHub `akebono03/ehp-proof-tracer` の `develop`（確認時 HEAD `50134578bcbb201ec8efde54436655c3b67c8cd4`）にある `expression.py`、`phase171_r2h_prop22_cited_hopf/source.py`、`phase176_r3r30_generic_hopf_substitution_isolated/source.py`、`phase176_r3r31_generic_hopf_public_connection/installer.py`、`tests/test_hopf_rules.py` を確認した。

## 対象と変更

新規ディレクトリ `phase176_r3r33r1_direct_hopf_frontier/` のみ追加する。

- `audit.py`: `check_sources`, `git`, `read_only_direct_probe`, `output_path`, `run`, `main` を新規定義する。
- `tests/test_audit.py`: 監査ガード用テスト4件を新規追加する。
- `run.ps1`: Windows PowerShell 5.1 互換の実行スクリプトを追加する。
- `README.md`: 英語の利用案内。
- `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`: 日本語の監査計画・全コード。

既存クラス・関数・import は変更しない。新規 GIVEN、直接的な群構造結論、専用 Narrative は追加しない。

## 数学的な境界

$$
H(\nu'\circ E(\eta_5\circ\eta_6))
=H(\nu')\circ E(\eta_5\circ\eta_6)
$$

$$
E(\eta_5\circ\eta_6)=\eta_6\circ\eta_7
$$

は、既存 AST 上では自動的な構造同一視ではない。懸垂の函手性、η 生成元の懸垂、等式の合成・Hopf 写像への移送をそれぞれ検証済みの証明ステップとして接続する必要がある。

## テストと完了条件

新規テスト `python -m pytest -q -p no:cacheprovider phase176_r3r33r1_direct_hopf_frontier/tests/test_audit.py`、既存 Hopf 関連の限定テストを実行する。全体 pytest は実施しない。

DryRun と本実行の Gate が PASS となり、`report.json` に直接経路の候補・型付き障害が記録されれば監査完了とする。Hopf 像や群構造の証明完成を意味しない。

## 次段階との境界

R3R34 以降で、監査結果を踏まえて懸垂の合成保存と型付き等式移送の既存一般規則の再利用可能性を精査する。数学的に正しいとしても未検証の等式を勝手に GIVEN 化しない。
