# Phase 175 R4R10 — (5.8)・Proposition 2.5 の公開利用計画

## 狙い

Toda の (5.8) を EHP の核から再証明せず、出典検証済みの文献命題として使用する。Proposition 2.5 は R4R7 の一般型条件で使用する。いずれも群の結論 $\pi_9^5$ を直接 GIVEN に登録しない。

## 変更対象

新規：`phase175_r4r10_cited_58_prop25_public/source.py`。`CitedToda58SignedDelta`、`CitedTodaProp25`、`git_blob_sha`、`vetted_source`、`source_positions`、`canonical_toda58`、`build_cited_58_prop25_sources`。

新規：`phase175_r4r10_cited_58_prop25_public/provider.py`。`screened_cited_facts`、`expand_cited_toda58`、`eta_identity_indices`、`expand_eta_identity`、`expand_cited_prop25`、`build_cited_58_prop25_provider`。

新規：`phase175_r4r10_cited_58_prop25_public/installer.py`。`git`、`git_blob_sha`、`replace_full_function`、`plan`、`install`。

新規：`phase175_r4r10_cited_58_prop25_public/audit.py`。`git`、`preflight`、`validate_prior`、`find_prior`、`sample_delta_eta9`、`replay_cited_prop25`、`inspect_public_connection`、`report_folder`、`run`、`main`。

既存：`phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` と `shared_expansion_provider()` のみを全文置換する。import は変更しない。他のクラス・関数は変更しない。変更後の完全な関数とファイルは `run.ps1` の監査フォルダーへ出力する。

新規テスト：`tests/test_installer.py`、`tests/test_source.py`、`tests/test_provider.py`、`tests/test_audit.py`。全テスト関数・import の全文は `CODE_FULL_JA.md` に収録する。

## 証明経路

1. `sources/toda/Toda_05_2.tex` の (5.8) を Git blob と内容で検証。$\Delta(\iota_9)=\pm(2\nu_4-E\nu')$ の符号を残した `CitedToda58SignedDelta` を GIVEN として登録。
2. `sources/toda/Toda_02_2.tex` の Proposition 2.5 を条件・範囲とともに検証し、一般 `CitedTodaProp25` を GIVEN として登録。
3. (5.8) の cited GIVEN → `TodaDeltaImageUpToSignStatement` の INFERENCE。これは文献命題の型付き読み取りであり、未知の事実を導出するものではない。
4. Chapter V の既存 $\eta_n=E^{n-2}\eta_2$ の GIVEN → $\iota_9\circ E^2\eta_7=\eta_9$ の INFERENCE。
5. Proposition 2.5 の GIVEN ＋ 前2件の INFERENCE → 符号を保った $\Delta(\eta_9)=\pm((2\nu_4-E\nu')\circ\eta_7)$ の INFERENCE。条件 $m=4,i=8,j=9$ で $j<3m-1$ を検証。

R4R7 の `prop25_inputs()` と `prop25_signed_composition_rule()` の条件チェックを再利用する。符号除去・位数2の演算・最終群の同定は今回の範囲外。

## 境界と誤用防止

- 同じ群構造・似た名前から数学的前提を生成しない。
- `SOURCE_ARCHIVE` や metadata-only claim から GIVEN に昇格させない。TeX 全体の固定 Git blob、原文の式、出典位置を検証して独立に登録する。
- source-first の公開登録だけ行う。既存証明の再実行、唯一性検査、専用 narrative、最終結論の GIVEN は行わない。
- 実行前に現在の Git HEAD の祖先性と変更対象を検証。作業ツリーの不許可変更を拒否。DryRun では本番コード変更を行わない。
- 全体 pytest は Phase 175 終了時まで行わない。

## Gate

- DryRun：`PASS_R4R10_CITED_58_PROP25_DRYRUN`
- 本実行：`PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING`

後者では、**共通 Provider から $\Delta(\eta_9)$ の候補が取得できる**ことを検証する。$\Delta(\eta_9)$ の ProofStep の親を実際に検証するが、$\pi_9^5$ の完成を意味しない。
