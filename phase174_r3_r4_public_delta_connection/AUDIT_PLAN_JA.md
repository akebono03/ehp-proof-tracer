# Phase 174 R3-R4 — 共通証明探索へ接続

## 変更対象の列挙

- **既存** `phase165_r52_r9_shared_math.py` — `shared_expansion_provider()` 関数全体（入れ子の `expand()` を含む）。
  - トップレベル import の変更なし。
  - `expand_cited_ehp_surjectivity_consequences(goal)` の直後に一般規則を追加。
  - 新しい import は既存関数の内部のみ。
- **新規** `phase174_r3_r4_public_delta_connection/patch.py` — 元の Git Blob を検証して上記関数を丸ごと置換。新規関数は同ファイル内。
- **新規** `phase174_r3_r4_public_delta_connection/audit.py` — 公開 Provider の型付き再構成監査。
- **新規** `phase174_r3_r4_public_delta_connection/tests/test_connection.py` — 限定テスト7件。
- **新規** `phase174_r3_r4_public_delta_connection/run.ps1` — 監査・適用・限定 pytest。
- **新規** `README.md` と `AUDIT_PLAN_JA.md` — 作業仕様。

## 置換コードの全文

R3-R4 を通常実行した時点で、変更後の `shared_expansion_provider()` 関数全体を
次の外部ファイルに出力する（完全な関数、コード中の省略記号なし）。

`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r4\shared_expansion_provider_FULL.py`

この関数だけを変更し、他のクラス・メソッド、トップレベル import 部分はそのまま維持する。

## 証明義務

- Proposition 4.4 に遡る、型付きの `$E:\pi_5^3\to\pi_6^4$` の単射性。
- Proposition 4.2 に遡る `im(Delta)=ker(E)` の型付き完全性。
- 2つの実際の INFERENCE ProofStep から `$\Delta:\pi_7^7\to\pi_5^3=0$` を推論する。
- Citation Gate を迂回せず、未検証 `GIVEN` を追加しない。
- $\pi_8^5$ の記名群構造を完成とみなさない。

## Phase の境界

本 R3-R4 は `Delta=0` の共通接続まで。
(4.8) の条件付き商群、二重懸垂の単射性、$2\nu_5=E^2\nu'$
および一般的な巡回群拡大の証明規則は、後続の別監査・実装対象。
全体 pytest は Phase 174 の最後だけに実施。
