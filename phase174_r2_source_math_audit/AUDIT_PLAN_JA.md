# Phase 174 R2 — 数学的根拠と証明義務

## 実装上の変更対象

既存ファイル・クラス・関数・メソッドの変更はない。

新規ファイル:
- `phase174_r2_source_math_audit/audit.py`
  - 監査パッケージ直下に新規追加。
  - 新規関数 `extract_labeled_environment`, `source_evidence`, `audit_prior_record`,
    `inspect_pi85_root`, `make_report`, `main` ほか。
- `phase174_r2_source_math_audit/tests/test_audit.py`
  - 監査専用の単体テスト５件を追加。
- `phase174_r2_source_math_audit/run.ps1`
  - HEAD、SHA、既存試験修正版を検証する DryRun／通常実行を追加。
- `phase174_r2_source_math_audit/README.md`, `AUDIT_PLAN_JA.md`

## 原文の数学的命題（ここに書かれたことと、アプリ内証明の成立は異なる）

Toda Chapter IV (4.8) は偶数 $n$ における条件付き結論を与える。
$n=4$ の場合、$\Delta(\iota_7)=0$ が証明済みなら

$$
E^2:\pi_6^3\hookrightarrow\pi_8^5,\qquad
\pi_8^5/E^2\pi_6^3\cong\mathbb Z/2.
$$

Toda Chapter V Lemma 5.4 では

$$
H(\nu_4)=\iota_7,\quad 2E\nu_4=E^2\nu'
$$

を述べる。式 (5.5) は $n\ge 5$ に対して

$$
2\nu_n=E^{n-3}\nu',\qquad 4\nu_n=\eta_n^3
$$

を述べる。$n=5$ で $2\nu_5=E^2\nu'$ となる。

既証明の $\pi_6^3=\mathbb Z/4\{\nu'\}$ があり、上の二つの事実が
型付き証明でつながれば、$2\nu_5$ は位数4、$\nu_5$ は位数8となる。
指数2の単射像は位数4なので群全体は位数8となり、
$\nu_5$ が生成元であることが分かる。

ただし現行 `sources/toda/Toda_05_2.tex` の Proposition 5.6 の証明には
`(4.8) と (5.6)?` と疑問符を含む表記があるため、出典引用の確定と
数学的前提の厳密な接続を分けて監査する。

## R2 で記録すべき不足

1. $\Delta(\iota_7)=0$ の独立な型付き証明と出典。
2. (4.8) の前提を満たした場合だけ $E^2$ の単射性および商群位数2を導出する規則。
3. (5.5) の一般式から $2\nu_5=E^2\nu'$ を導出する型付き規則。
4. $\pi_6^3$ の先行完成証明の適切な再利用。
5. 上記前提から巡回位数8と記名生成元 $\nu_5$ を証明する一般的な群論規則。

必要な関係は「監査対象の証明義務」であり、監査時に GIVEN として登録しない。
R2 で作った JSON の `proposal_count` は ProofStep の検証・完成を意味しない。

## R2 と R3 の境界

R2 は既存の数理ソース・型付き Goal・推論候補を観測するだけ。
R3 の規則実装では数学的に証明済みと確認できた前提のみを採用する。
$n,k$・生成元名別の Narrative 専用分岐は禁止する。
全体 pytest は Phase 174 終了時だけ実行する。
